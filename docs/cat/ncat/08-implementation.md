# 官方代码精读与最小实现

官方仓库为 [bigdata-ustc/NCAT](https://github.com/bigdata-ustc/NCAT)。本页核对的公开快照 commit 是 `58f88b30cb6ecdcd7ed35a8ad9ce2aa23a9cd95f`。仓库规模较小，核心逻辑集中在四处。

| 文件 | 职责 |
|---|---|
| `functionApproximation/NCAT.py` | 双通道 Q 网络、attention、TD MSE 更新 |
| `envs/env.py` | support/query 环境、响应模型更新、query reward |
| `agents/Train.py` | 轨迹收集、探索、replay、Bellman target |
| `launch.py` 与 `model_train.sh` | 参数、训练入口与示例配置 |

## 1. 从数据到训练入口

README 给出的顺序是：

```bash
cd data/assist1213
python data_preprocess.py

cd ../..
python divide_data.py

cd envs/pre_train
python main.py

cd ../..
sh model_train.sh
```

预处理完成后，`env.py` 读取：

```text
data/<data_name>/log_data_filtered.json
```

并从 `envs/model_file/<data_name>/...` 载入预训练 IRT/NCDM。

!!! warning "仓库不是即开即跑的完整实验包"

    数据原文件、绝对路径、预训练模型目录和 GPU 环境需要用户补齐。`config.py` 中的 `pwd_path = 'xxx/NCAT/...'` 是占位符，核心模型还硬编码了 CUDA。

## 2. 环境怎样构造 support/query

`env.__init__` 中：

```python
self.setup_train_test()
self.sup_rates, self.query_rates = self.split_data(ratio=0.5)
```

`split_data` 对每名学生的题目打乱后切成两半：

```python
sup_rates[u] = {
    item: self.rates[u][item]
    for item in all_items[:int(ratio * len(all_items))]
}
query_rates[u] = {
    item: self.rates[u][item]
    for item in all_items[int(ratio * len(all_items)):]
}
```

这与论文的 70%/30% 不同。每个训练 epoch 末尾 `re_split_data()` 再切一次，与论文“每轮重切”一致。

候选集只来自该学生的 support：

```python
@property
def candidate_items(self):
    uid = self.state[0][0]
    return set(self.sup_rates[uid].keys())
```

## 3. 一次环境 step

`env.step(action)` 的次序是：

1. 断言动作属于 support 且未选过；
2. 调用 `reward(action)`；
3. 判断是否到 \(T\)；
4. 把动作、reward、终止标志和指标写入状态；
5. 返回新状态。

`reward` 是整条 NCAT 目标的代码核心：

```python
items = selected_items + [action]
correct = [historical_response[it] for it in items]

dataset.add_record([uid] * len(items), items, correct)
model.update(dataset, learning_rate, epoch=1)

loss, pred = model.cal_loss(
    [uid] * len(query_items),
    query_items,
    query_answers,
    know_map,
)
model.init_stu_emb()
return -loss, ACC, AUC, correct[-1]
```

它先用累计已选题适应学生 embedding，再在 query 上计算 loss，最后重置学生 embedding。这个重置意味着下一步再次从全局初始状态出发，用**全部累计已选题**重新拟合，而非在上一步学生参数上继续一小步。

## 4. 四个输入 tensor

Q 网络 forward 接受：

```python
p_0_rec, p_1_rec, p_0_target, p_1_target
```

含义如下：

| tensor | shape | 含义 |
|---|---|---|
| `p_0_rec` | \(B\times L_0\) | 答错题序列，前面带 padding 题 0 |
| `p_1_rec` | \(B\times L_1\) | 答对题序列，前面带 padding 题 0 |
| `p_0_target` | \(B\) | 每行最后有效位置索引 |
| `p_1_target` | \(B\) | 每行最后有效位置索引 |

`convert_item_seq2matrix` 将不同长度序列补成矩阵：

```python
matrix = np.zeros((batch_size, max_length), dtype=np.int32)
target_index = [len(seq) - 1 for seq in item_seq]
```

初始时两个通道都是 `[0]`，因此题号 0 同时充当 padding 和空状态 token。

## 5. embedding 与 Performance Learning

模型定义两张表：

```python
self.q_embed_0 = nn.Embedding(n_question, d_model)
self.q_embed_1 = nn.Embedding(n_question, d_model)
```

之后生成长度 mask，并分别送入两个 encoder：

```python
item_emb_0 = self.q_embed_0(p_0_rec)
item_emb_1 = self.q_embed_1(p_1_rec)

src_mask_0 = mask(p_0_rec, p_0_target + 1).unsqueeze(-2)
src_mask_1 = mask(p_1_rec, p_1_target + 1).unsqueeze(-2)

item_per_0 = self.self_atten_0(item_emb_0, src_mask_0)
item_per_1 = self.self_atten_1(item_emb_1, src_mask_1)
```

`EncoderLayer` 使用 pre-norm 残差：

```python
x = x + dropout(self_attention(layer_norm(x)))
x = x + dropout(feed_forward(layer_norm(x)))
```

## 6. Contradiction Learning 的代码路径

仓库把原始 embedding 作为 query/key，把 Performance Learning 输出作为 value：

```python
input_01, input_10 = self.contradiction(
    item_emb_0,
    item_emb_1,
    item_per_1,
    item_per_0,
)
```

`MultiHeadedAttention_con` 先计算

\[
\operatorname{softmax}
\left(
\frac{Q_0K_1^\top}{\sqrt{d_h}}
\right)V_1,
\]

再使用该 attention 的转置聚合另一方向：

\[
A^\top V_0.
\]

这是一套共享 pair score 的双向聚合。代码没有给 contradiction attention 传 padding mask，随后直接：

```python
input_01 = input_01.mean(-2)
input_10 = input_10.mean(-2)
```

因此 mini-batch 内的 padding 长度可能影响跨通道均值。稳定复现应为两个方向构造 pairwise mask，并采用 masked mean。

## 7. pooling 与输出层

仓库对 self-attention 通道取最后有效位置：

```python
input_0 = item_per_0[batch_index, p_0_target]
input_1 = item_per_1[batch_index, p_1_target]
```

对 cross 通道取 mean，然后拼接：

```python
state_vector = torch.cat(
    [input_0, input_1, input_01, input_10],
    dim=-1,
)
q_values = self.policy_layer(state_vector)
```

`policy_layer` 为：

```python
Linear(4 * d_model, 512)
ReLU()
Dropout()
Linear(512, n_question)
```

论文描述的四路平均池化与这里的“self 取最后位置、cross 取均值”应分别报告。

## 8. 行为策略怎样屏蔽动作

收集轨迹时，`Train.py` 先计算所有题 Q 值，再屏蔽：

```python
for item in actions:
    policy[item] = -np.inf

for item in range(item_num):
    if item not in env.candidate_items:
        policy[item] = -np.inf

action = np.argmax(policy[1:]) + 1
```

这部分正确保证了：

- 不重复选题；
- 只从当前学生的 support 题选；
- 题号 0 不作为动作。

训练探索通过一定概率把整条 `policy` 替换成随机数，然后再应用同一套 mask。

## 9. replay 与 Bellman target

仓库保存：

```python
[state, action, reward, done, next_state]
```

抽样后用下一状态预测最大 Q 值：

```python
value = self.fa.predict(next_state_data)
value[:, 0] = -500

goal = reward + (
    np.max(value, axis=-1)
    * not_done
    * effective_gamma
)
```

这里存在一个重要实现风险：下一状态求最大值时只屏蔽题号 0，没有屏蔽已选题和 support 外题。行为策略的合法动作 mask 没有进入 TD target，网络可能用一个实际不可选的题 bootstrap。

推荐改成：

```python
next_q = target_net(next_state)
next_q = next_q.masked_fill(~next_valid_mask, float("-inf"))
next_best = next_q.max(dim=1).values
target = reward + gamma * (~done).float() * next_best
```

## 10. optimizer 生命周期

官方 `optimize_model` 每次更新都重新创建 Adam：

```python
optimizer = optim.Adam(self.parameters(), lr=lr)
```

这样 Adam 的一阶、二阶动量在每个 batch 后丢失，行为更接近带自适应缩放的单步优化。推荐在模型或 trainer 初始化时只创建一次 optimizer：

```python
optimizer = torch.optim.Adam(
    online_net.parameters(),
    lr=learning_rate,
)
```

训练循环持续复用它，并把 optimizer state 一起存 checkpoint。

## 11. 论文、仓库与推荐复现对照

| 组件 | 论文 | 公开仓库快照 | 推荐复现 |
|---|---|---|---|
| support/query | 70%/30% | 50%/50% | 按目标协议配置化 |
| 学生切分 | 60%/20%/20%，5 折 | 约 80%/10%/10% | 学生隔离并记录 fold |
| 四路 pooling | 全部平均 | self 最后位置，cross mean | 两种都做消融 |
| contradiction padding | 公式未展开 | 未传 mask | pairwise mask |
| TD 下一动作 | 合法题集合 | 仅屏蔽题 0 | 完整合法动作 mask |
| target network | 未明确 | 没有独立 target | 加入 target/Double DQN |
| replay 容量 | 10,000 | 50,000 | 超参数化 |
| optimizer | 常规训练语义 | 每 batch 重建 Adam | 持久化 optimizer |
| 设备 | GPU 实验 | 硬编码 CUDA | `device` 参数化 |

## 12. 先做一个可验证的最小版本

在引入 attention 前，可先用三值状态向量验证环境：

\[
x_{t,j}
=
\begin{cases}
-1, & q_j\text{ 已答错},\\
1, & q_j\text{ 已答对},\\
0, & q_j\text{ 尚未作答}.
\end{cases}
\]

```python
class TinyQNetwork(torch.nn.Module):
    def __init__(self, n_items, hidden=128):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(n_items, hidden),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden, n_items),
        )

    def forward(self, state):
        return self.net(state)
```

最小版本必须先通过：

1. 题目被选后下一状态对应位置改变；
2. 已选题永远不再被选；
3. support 外题永远不进入 argmax；
4. 终止样本 target 等于 reward；
5. 改变一条实时答案会改变下一步 Q 向量；
6. query 题没有进入学生参数拟合；
7. 测试学生不参与响应模型或策略训练。

通过这些测试后，把 `TinyQNetwork` 替换为 NCAT encoder，环境、replay 和 TD 更新保持不变。这样可以把“强化学习管线错误”和“attention 表示错误”分开定位。

## 13. 最小 NCAT 接口

一个清晰的网络接口只需接受状态张量并输出 Q 值：

```python
class NCATQNetwork(torch.nn.Module):
    def forward(
        self,
        incorrect_ids,
        incorrect_mask,
        correct_ids,
        correct_mask,
    ):
        incorrect = self.incorrect_encoder(
            self.incorrect_embedding(incorrect_ids),
            incorrect_mask,
        )
        correct = self.correct_encoder(
            self.correct_embedding(correct_ids),
            correct_mask,
        )

        cross_incorrect, cross_correct = self.cross_encoder(
            incorrect,
            incorrect_mask,
            correct,
            correct_mask,
        )

        state = torch.cat(
            [
                masked_mean(incorrect, incorrect_mask),
                masked_mean(correct, correct_mask),
                masked_mean(cross_incorrect, incorrect_mask),
                masked_mean(cross_correct, correct_mask),
            ],
            dim=-1,
        )
        return self.policy_head(state)
```

网络内负责表示；trainer 负责动作合法性、探索、replay、target 和优化。职责分离后更容易做单元测试与消融。

## 14. 复杂度与性能瓶颈

若两个通道长度为 \(k_0,k_1\)，单层 attention 的主要复杂度约为

\[
O(k_0^2d+k_1^2d+k_0k_1d).
\]

短测 \(T\le20\) 时通常可控。更大的瓶颈往往来自每个 environment step 都重新拟合学生参数、遍历整个 query 集并计算 reward。可考虑：

- batch 化多个学生的局部更新；
- 缓存题目全局表示；
- 用增量局部参数更新替代每步从头拟合；
- 控制 query 样本量并检查 reward 方差；
- 并行环境与向量化合法动作 mask。

方法的边界和下一步研究空间见[局限、方法比较与未来工作](09-limitations-comparison-future.md)。
