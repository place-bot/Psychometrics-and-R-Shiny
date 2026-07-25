# BOBCAT 官方代码精读

本页精读官方仓库 [`arghosh/BOBCAT`](https://github.com/arghosh/BOBCAT)，并固定到提交
[`e6b6245`](https://github.com/arghosh/BOBCAT/tree/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec)，避免代码后续变化造成行号和行为对不上。

!!! info "先记住官方代码中的命名差异"

    论文把影响函数启发的低方差近似称为 **Approx**。官方命令和分支判断使用
    `biased`，所以 `biirt-biased`、`binn-biased` 对应论文中的
    BiIRT-Approx、BiNN-Approx。这里的 `biased` 描述梯度估计的统计性质，与数据偏差无关。

## 1. 仓库地图

| 文件 | 主要职责 | 论文中的位置 |
| --- | --- | --- |
| [`dataset.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/dataset.py) | 每名学生内部的 training/meta 划分；构造稠密标签和 mask | \(\Omega_i^{(1)}\)、\(\Gamma_i\) |
| [`model.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/model.py) | BiIRT/BiNN 响应模型、局部损失、状态和 Active/Random 选题 | \(g(j;\theta_i,\gamma)\)、\(\mathcal L'\) |
| [`policy.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/policy.py) | PPO 选题器和 straight-through 选题器 | Unbiased 与 Approx |
| [`train.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py) | 内层适应、四条训练路径、验证、测试和早停 | 双层优化主循环 |
| [`irt.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/irt.py) | 传统 1PL IRT 的 Random/Active 基线 | IRT-Random、IRT-Active |
| [`utils/configuration.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/utils/configuration.py) | 数据集规模、学习率、题长、batch 和早停参数 | 实验设置 |
| [`utils/utils.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/utils/utils.py) | 五折学生划分、accuracy、AUC | 实验评估 |
| [`utils/preprocessing.py`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/utils/preprocessing.py) | EdNet、Junyi、Eedi 的预处理 | 数据准备 |

主入口是 `train.py`。一次运行只训练一个“响应模型 × 选题法 × 数据集 × fold × 题长”组合。

## 2. 一条样本怎样进入模型

### 2.1 原始 JSON

预处理后的数据以学生为单位。每条记录至少包含：

```json
{
  "q_ids": [12321, 17794, 17795],
  "labels": [1, 0, 1]
}
```

`q_ids[k]` 和 `labels[k]` 共同表示该学生对一道题的历史作答。代码只保留二值正误标签，
没有把题干、知识点、作答用时或题目文本输入选题器。

### 2.2 学生内部的 80/20 划分

[`Dataset.__getitem__`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/dataset.py#L21-L43)
先打乱该学生的全部已观测作答，然后把末尾约 \(20\%\) 作为 meta 题：

```python
observed_index = np.arange(len(data["q_ids"]))
np.random.shuffle(observed_index)
target_index = observed_index[-N//5:]
trainable_index = observed_index[:-N//5]
```

对应关系为

\[
\texttt{trainable\_index}\leftrightarrow\Omega_i^{(1)},
\qquad
\texttt{target\_index}\leftrightarrow\Gamma_i.
\]

训练集的 `seed=None`，每次取样都会重新打乱，因此 training/meta 划分会持续变化。验证和
测试时把 `seed` 设为 `100,101,\ldots`，同一学生在同一次重复中获得确定划分。

!!! warning "Python 下标带来的细小差异"

    代码写的是 `-N//5`。Python 将它解释为 \((-N)//5\)，当 \(N\) 无法被 5 整除时，
    meta 题数等于 \(\lceil N/5\rceil\)。所以这里采用“约 80/20”，个别学生的比例会因
    向上取整略有变化。

### 2.3 `collate_fn` 变成四个稠密张量

一个 batch 被整理成：

| 张量 | 形状 | 含义 |
| --- | --- | --- |
| `input_labels` | \(B\times Q\) | training candidates 的历史正误 |
| `input_mask` | \(B\times Q\) | 哪些题属于该学生的候选集合 |
| `output_labels` | \(B\times Q\) | meta 题的历史正误 |
| `output_mask` | \(B\times Q\) | 哪些题属于该学生的 meta 集合 |

标签张量中，错误作答和未观测位置都写成 0；mask 负责区分这两种情况。这个实现便于逐元素
乘 mask，代价是内存随 \(B\times Q\) 增长。Eedi-1 有 27,613 道题，稠密 batch 会占用
可观的 CPU/GPU 内存。

## 3. 代码怎样实现“每答一题再选下一题”

这是理解自适应性的关键。

### 3.1 三值作答状态

[`MAMLModel.reset`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/model.py#L66-L80)
先把历史标签 \(0/1\) 映射成 \(-1/+1\)：

```python
obs_state = (input_labels - 0.5) * 2.0
train_mask = zeros(B, Q)
state = obs_state * train_mask
```

所以策略实际看到的状态是

\[
x_{ij}^{(t)}=
\begin{cases}
+1,&\text{题 }j\text{ 已选且学生 }i\text{ 答对},\\
-1,&\text{题 }j\text{ 已选且学生 }i\text{ 答错},\\
0,&\text{题 }j\text{ 尚未选择}.
\end{cases}
\]

`obs_state` 在离线数据中已经存着候选题的历史答案；`train_mask` 像遮挡板，只允许当前已选
题目的答案进入策略。

### 3.2 逐题闭环

Approx 路径
[`pick_biased_samples`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py#L95-L121)
的每一步都执行：

```python
state = model.step(env_states)
train_mask_sample, actions = st_policy.policy(state, action_mask)
action_mask[student_ids, actions] = 0
env_states["train_mask"] = train_mask + train_mask_sample.data
```

流程可以写成：

\[
x_i^{(t)}
\xrightarrow{\Pi_\phi}
j_i^{(t)}
\xrightarrow{\text{查询历史响应}}
Y_{i,j_i^{(t)}}
\xrightarrow{\text{写入 mask}}
x_i^{(t+1)}.
\]

第 \(t\) 步选中题目后，它的 \(+1/-1\) 作答会在第 \(t+1\) 步进入状态。答对和答错会形成
不同状态，策略能够给出不同的下一题。官方实现由此保持逐题实时反馈的 CAT 结构。

!!! note "离线实验怎样模拟现场作答"

    代码只能从 `input_mask=1` 的历史已观测题中选题。选中后直接从
    `input_labels` 查询答案，相当于回放学生过去的响应矩阵。真实部署时，这个查询位置应
    替换为“向学生呈现题目并等待新作答”。策略循环本身无需改变。

### 3.3 两种 mask 各管什么

- `action_mask`：该学生仍可选择且在离线数据中有答案的题；
- `train_mask`：当前 episode 已经选择的题。

选题 logits 加上

\[
\log m_j,\qquad m_j\in\{0,1\}.
\]

可选题加 \(\log 1=0\)，不可选题加一个数值上近似 \(-\infty\) 的量，softmax 后概率接近
0。题目选中后，`action_mask` 对应位置归零，避免重复选题。

## 4. 响应模型：BiIRT 与 BiNN

### 4.1 共享初始化和学生局部参数

[`clone_meta_params`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py#L19-L21)
把一个全局可学习向量复制到 batch 中每名学生：

```python
meta_params[0]                 # [1, d]
    .expand(batch_size, -1)    # [B, d]
    .clone()
```

论文中的对应关系是：

\[
\texttt{meta\_params[0]}\leftrightarrow
\text{全局学生参数初始化},
\qquad
\texttt{new\_params[0]}\leftrightarrow
\theta_i^{(k)}.
\]

### 4.2 BiIRT

当 `question_dim == 1` 时，
[`compute_output`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/model.py#L129-L135)
返回

```python
logit = student_embed - question_difficulty
```

也就是

\[
g(j;\theta_i,\gamma)=\theta_i-b_j,
\qquad
p(Y_{ij}=1)=\sigma(\theta_i-b_j).
\]

`student_embed` 是每名学生在内层更新的局部能力，`question_difficulty` 属于全局模型参数，
由外层优化器更新。

### 4.3 BiNN

当 `question_dim > 1` 时：

```python
h_i = Dropout(ReLU(Linear(theta_i)))
logits_i = Linear(h_i)  # Q 个题目的 logits
```

学生局部表示 \(\theta_i\in\mathbb R^d\) 先经过 256 个隐藏单元，再一次性输出 \(Q\) 道题
的作答 logits。每个输出坐标绑定一道固定题目。

这个结构能够表达比 1PL 更复杂的学生—题目交互，同时带来两个限制：

- 输出层尺寸与题库 \(Q\) 绑定，新增题没有可直接使用的输出节点；
- 模型没有题目特征编码器，无法依靠题干或知识点为冷启动题生成表示。

## 5. 内层优化逐行对应公式（6）

核心函数是
[`inner_algo`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py#L24-L35)：

```python
for _ in range(params.inner_loop):
    config["meta_param"] = new_params[0]
    res = model(batch, config)
    loss = res["train_loss"]
    grads = torch.autograd.grad(
        loss, new_params, create_graph=create_graph
    )
    new_params = [
        new_params[i] - inner_lr * grads[i]
        for i in range(len(new_params))
    ]
```

逐行对应

\[
\theta_i^{(k+1)}
=
\theta_i^{(k)}
-\alpha
\nabla_{\theta_i}
\mathcal L_i'
\left(\theta_i^{(k)};\,S_i\right).
\]

| 代码 | 数学含义 |
| --- | --- |
| `params.inner_loop` | \(K\)，默认 5 步 |
| `params.inner_lr` | \(\alpha\)，局部学习率 |
| `config["train_mask"]` | 当前已选集合 \(S_i\) |
| `res["train_loss"]` | 已选题二元交叉熵 \(\mathcal L_i'\) |
| `new_params[0]` | 学生局部参数 \(\theta_i^{(k)}\) |

`BCEWithLogitsLoss` 直接接收 logits，把 sigmoid 和交叉熵合并计算。`train_loss` 对所有已选题
求和；`output_loss` 对 batch 的 meta 题求和后除以学生数。

## 6. 外层怎样更新 \(\gamma\) 和学生初始化

以 [`run_biased`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py#L124-L144)
为例：

1. 策略逐步得到最终 `train_mask`；
1. 从共享初始化复制出每名学生的 `new_params`；
1. 用最终已选题做 \(K\) 步 `inner_algo`；
1. 用适应后的学生参数预测 `output_mask` 指定的 meta 题；
1. `loss.backward()` 更新响应模型和共享学生初始化。

```python
inner_algo(batch, config, new_params)
res = model(batch, config)
loss = res["loss"]
loss.backward()
optimizer.step()
meta_params_optimizer.step()
```

`optimizer` 是响应模型参数的 Adam；`meta_params_optimizer` 是共享学生初始化的 SGD。
常规外层更新调用 `inner_algo(..., create_graph=False)`，因此采用一阶 MAML 风格近似：
梯度保留从最终局部参数到初始化的直接路径，省略内层梯度更新的二阶导数项。

## 7. 四条选题路径

### 7.1 Random

[`pick_random_sample`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/model.py#L15-L21)
使用 `torch.multinomial(..., replacement=False)` 从候选题中一次抽取 \(n\) 题。随后用整组题
适应学生参数。

### 7.2 Active

[`pick_uncertain_sample`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/model.py#L119-L127)
计算

\[
s_{ij}=\min(p_{ij},1-p_{ij}),
\]

并选最大值。\(p_{ij}=0.5\) 时分数最高，因此这就是 1PL 中“选择难度最接近当前能力”的
不确定性规则。每选一道题，代码运行一次内层更新，再计算下一题。

### 7.3 Unbiased：PPO 路径

[`ActorCritic`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/policy.py#L26-L85)
包含 actor 和 critic：

\[
x_i^{(t)}
\xrightarrow{\text{Linear}}
h_i^{(t)}
\xrightarrow{\text{Tanh MLP}}
\begin{cases}
\text{题目 logits},\\
V(x_i^{(t)}).
\end{cases}
\]

actor 从 masked categorical distribution 抽样，`Memory` 保存每步状态、动作、旧
log probability 和 mask。选满 \(n\) 题后，
[`run_unbiased`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/train.py#L67-L92)
计算每名学生的代码级奖励：

\[
r_i
=
\operatorname{Accuracy}_{i,\text{policy}}
-
\operatorname{Accuracy}_{i,\text{random}}.
\]

同一个终点奖励复制到该 episode 的每个动作。PPO 使用概率比裁剪、critic MSE 和 entropy
bonus，默认更新 4 个 epoch，裁剪阈值为 0.2。

!!! warning "论文公式与开源实现的奖励写法"

    论文从外层 loss 推导 score-function 梯度；开源代码把“相对随机选题的 meta
    accuracy 提升”作为 PPO 奖励。两者服务于相同的 held-out 预测目标，但数值目标和
    优化器并未逐项照抄论文公式。复现论文时应记录采用的是论文推导版还是仓库 PPO 版。

### 7.4 Approx：代码名 `biased`

[`hard_sample`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/policy.py#L151-L156)
实现 straight-through one-hot：

```python
y_soft = softmax(logits)
index = argmax(y_soft)
y_hard = one_hot(index)
select = y_hard - y_soft.detach() + y_soft
```

前向计算时：

\[
\texttt{select}=y_{\text{hard}},
\]

所以每一步确实只选一道题。反向传播时：

\[
\frac{\partial\,\texttt{select}}{\partial z}
=
\frac{\partial y_{\text{soft}}}{\partial z},
\]

梯度可以从 meta loss 穿过软 softmax 回到策略参数。这是有偏、低方差近似的代码落点。

训练状态下，每选一道题便执行：

```python
config["train_mask"] = previous_mask + train_mask_sample
inner_algo(..., create_graph=True)
meta_loss = model(batch, config)["loss"]
st_policy.update(meta_loss)
```

`create_graph=True` 允许策略梯度穿过内层适应步骤。策略在每个选题步单独更新一次。完成整条
序列后，代码再用 hard mask 重做内层适应，更新响应模型和共享初始化。

!!! note "代码没有显式构造 Hessian 逆矩阵"

    论文用影响函数解释 Approx 梯度及其低方差性质。官方实现采用 unrolled inner
    optimization 加 straight-through estimator，通过 PyTorch 自动微分穿过 5 步内层
    更新。仓库中没有显式计算 \(H^{-1}\) 或单独实现 influence score。

## 8. 一次训练 batch 的完整调用链

```text
Dataset.__getitem__
  └─ 每名学生随机切 80% candidates / 20% meta
collate_fn
  └─ 构造 input/output labels 与 masks
train_model
  ├─ random/active  → run_random
  ├─ unbiased       → run_unbiased → PPO.update
  └─ biased/Approx  → run_biased   → StraightThrough.update
         ├─ 策略逐题选出 train_mask
         ├─ inner_algo：局部适应学生参数
         ├─ meta BCE：预测 output_mask 中的题
         └─ 更新响应模型、共享初始化和相应策略
test_model
  └─ 展平所有 meta 题，计算 accuracy 与 AUC
```

从算法角度，可以压缩成以下伪代码：

```python
for batch in students:
    candidates, meta = split_observed_answers(batch)
    state = all_unseen()

    for t in range(test_length):
        item = policy(state, available_items)
        answer = candidates[item]
        state = reveal(state, item, answer)

    local_student = adapt(global_init, selected_answers, steps=5)
    meta_logits = response_model(local_student)
    meta_loss = masked_bce(meta_logits, meta.answers)

    update_response_model_and_global_init(meta_loss)
    update_selection_policy(meta_loss_or_reward)
```

## 9. 验证、测试和早停

[`data_split`](https://github.com/arghosh/BOBCAT/blob/e6b6245e23c1065ba8b8c56de5f051dfbcdd89ec/utils/utils.py#L38-L61)
先按学生打乱，再用相邻 fold 作为 test 和 validation，其余三折作为 training：

\[
60\%\ \text{train}
+20\%\ \text{validation}
+20\%\ \text{test}.
\]

每个 epoch 后，代码用若干个固定 seed 重复验证。validation accuracy 创新高时，更新
`best_epoch` 并立即计算一次 test accuracy/AUC。超过 `wait` 个 epoch 没有新的 validation
accuracy 记录便停止。

accuracy 在 0.5 阈值处二值化；AUC 使用 `sklearn.metrics.roc_auc_score`。评估时把所有
学生的所有 meta 响应展平成一个向量，所以报告的是 interaction-level 指标。

!!! warning "严格复现时应改善的两点"

    - `len(data)//5` 会留下不能整除 5 的尾部学生；这些学生始终进入 training，无法进入
      validation/test。可以改用 `KFold` 或 `array_split`。
    - 代码在 validation 创新高时反复查看 test，并且没有保存/恢复最佳 checkpoint。更严谨
      的流程应只靠 validation 选定 checkpoint，训练结束后对 test 运行一次。

## 10. 超参数与代码中的真实控制项

| 参数 | 代码默认值 | 作用 |
| --- | ---: | --- |
| `inner_loop` | 5 | 每次局部适应的梯度步数 \(K\) |
| `inner_lr` | 0.1 | 局部适应步长 \(\alpha\) |
| `lr` | \(10^{-4}\) | 响应模型 Adam 学习率 |
| `meta_lr` | \(10^{-4}\) | 共享学生初始化 SGD 学习率 |
| `policy_lr` | \(2\times10^{-3}\) | PPO/straight-through 策略学习率 |
| `question_dim` | 4 | BiNN 学生局部向量维度 |
| `n_query` | 10 | 固定测试长度 |

README 列出 `hidden_dim=256`，但 `train.py` 和 `model.py` 没有读取
`params.hidden_dim`；隐藏层直接写死为 256。BiNN 的学生向量维度由 `--question_dim`
控制。若要检验论文中报告的 256 维学生参数设置，需要显式运行
`--question_dim 256`，不能依靠 `--hidden_dim 256`。

## 11. 传统 IRT 基线 `irt.py`

`irt.py` 独立于双层训练代码。它先把每条作答变成题目 one-hot 加学生 one-hot，用无截距
logistic regression 联合估计题目难度和训练学生能力：

\[
\operatorname{logit}p_{ij}=\theta_i-b_j.
\]

新学生的能力用一维根求解器 `brentq` 更新。Active 每步选择当前预测概率最接近 0.5 的题，
Random 直接抽题。这个文件承担 IRT-Active/IRT-Random 的经典基线功能。

!!! warning "`policy_lr` 在基线文件中被复用"

    `irt.py` 的能力估计导数把 `params.policy_lr` 当作能力先验/正则强度，并遍历
    \(10,1,0.1,0.01,10^{-4},0\)。它在这里不表示神经选题策略学习率。读实验脚本或整理
    超参数时要按文件语境区分。

## 12. 官方仓库能支持的结论

从代码可以直接确认：

1. BOBCAT 的动作是逐题产生的，下一步策略输入包含此前已选题的真实正误；
1. 离线实验通过遮挡—揭示历史作答模拟实时交互；
1. BiIRT 和 BiNN 共享同一套双层训练骨架；
1. Unbiased 使用 PPO，Approx 使用 greedy hard action 加 straight-through gradient；
1. 外层指标来自未用于适应的 meta 作答；
1. 固定 \(Q\) 维状态和动作头限制了新题冷启动与跨题库迁移。

代码也显示出论文未展开的工程边界：依赖稠密 \(B\times Q\) 张量、仅使用题号和正误、
缺少内容约束与曝光控制、环境只回放历史观测、依赖旧版 PyTorch/Neptune 接口。

## 13. 复现前建议修订

### 环境

README 只声明 `torch==1.7.1`，源码还依赖 NumPy、SciPy、pandas、scikit-learn 和
Neptune。建议建立完整 lock file，并把 Neptune 日志设为可选依赖。

### 数据和评估

- 用标准五折实现覆盖每名学生；
- 固定并保存学生划分、学生内部划分和随机 seed；
- 只在最终选定 checkpoint 上评估 test；
- 同时报告 interaction-level 与 student-level 指标；
- 记录每题曝光、试卷重叠、内容覆盖和群体差异。

### 模型

- 把 `question_dim`、隐藏层宽度和 dropout 都显式写入配置；
- 为模型、mask、内层梯度和策略分支增加单元测试；
- 用稀疏/集合表示降低大题库内存；
- 引入 item encoder，让策略可以根据题目特征给新题打分；
- 对正式 CAT 加入内容蓝图、曝光和停止约束。

### 最值得打印的诊断量

- 每步 policy entropy、top-\(k\) 动作概率和选中题号；
- `state` 中 \(-1/0/+1\) 的数量及其与 `train_mask` 的一致性；
- 每名学生是否只从 `input_mask=1` 的题中选择，是否存在重复；
- 内层每步 train loss 和 \(\lVert\nabla_{\theta_i}\mathcal L_i'\rVert\)；
- meta loss、accuracy、AUC 与 calibration；
- \(\lVert\nabla_\phi\mathcal J\rVert\) 和
  \(\lVert\nabla_\gamma\mathcal J\rVert\)；
- PPO ratio、advantage，或 straight-through 的 soft/hard action；
- 每题曝光率、学生间试卷重叠率和内容覆盖。
