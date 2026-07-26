# 训练与真实学生部署

这一页把前面的目标、状态、响应模型和 Q-learning 串成两个完整算法：离线训练与线上逐题施测。

## 1. 阶段一：预训练响应模型

先用训练学生的历史作答估计响应模型 \(M\) 的全局参数：

- IRT：题目难度、区分度等；
- MIRT：多维题目向量；
- NCDM：学生、题目与知识点的神经参数。

进入 NCAT 训练后，全局题目参数保持固定。对每个模拟学生，只用当前已选 support 题更新该学生的局部参数。

这样可以把 reward 的变化主要归因于选题轨迹，而非响应模型全局参数同时漂移。

## 2. 阶段二：为一个历史学生生成 trajectory

对训练学生 \(i\)：

1. 随机划分 \(\mathcal D_i^s\) 和 \(\mathcal D_i^u\)；
2. 初始化空状态 \(s_1\) 和学生局部参数；
3. 在合法 support 题中按 epsilon-greedy 选择 \(q_t\)；
4. 从历史日志读取 \(a_{i(t)}\)；
5. 用 \(\mathcal D_i^s(t)\) 更新 \(\widehat\theta_i^{\,t}\)；
6. 计算 query BCE 和 \(r_i^t\)；
7. 形成 \(s_{t+1}\)；
8. 存入 \((s_t,q_t,r_i^t,s_{t+1},d_t)\)。

状态的逐题演化例如：

\[
s_1=\varnothing,
\]

\[
s_2=\{(q_7,1)\},
\]

\[
s_3=\{(q_7,1),(q_3,0)\}.
\]

第二步动作在看过 \(q_7\) 的正确反应后才决定；第三步动作又会受到 \(q_3\) 错误反应影响。

## 3. 阶段三：从 replay batch 更新 Q 网络

抽取 mini-batch 后：

1. 把每个 \(s_t\) 转为答错序列、答对序列和 mask；
2. 计算 \(Q_\phi(s_t,\cdot)\)；
3. `gather` 出真实动作 \(q_t\) 的预测；
4. 对 \(s_{t+1}\) 计算合法动作中的最大 Q 值；
5. 构造 TD target；
6. 最小化 TD MSE；
7. 更新 online network；
8. 按计划同步 target network。

```python
q_all = online_net(state)
q_taken = q_all.gather(1, action[:, None]).squeeze(1)

with torch.no_grad():
    next_q = target_net(next_state)
    next_q = next_q.masked_fill(~next_valid_mask, float("-inf"))
    next_best = next_q.max(dim=1).values
    next_best = torch.where(done, torch.zeros_like(next_best), next_best)
    target = reward + gamma * next_best

loss = torch.nn.functional.mse_loss(q_taken, target)
optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(online_net.parameters(), 5.0)
optimizer.step()
```

## 4. 离线训练伪代码

```text
输入：
    历史学生数据 D
    预训练响应模型 M
    最大测试长度 T

初始化：
    online Q 网络 Q_phi
    target 网络 Q_bar_phi
    replay buffer B

重复若干 epoch：
    对抽到的每个训练学生 i：
        随机切分 support D_i^s 与 query D_i^u
        state <- empty
        重置该学生的局部参数

        对 t = 1,...,T：
            valid <- 尚未选过的 support 题及其他硬约束
            action <- epsilon-greedy(Q_phi(state), valid)
            answer <- 历史日志中该题的答案
            更新学生局部参数 theta_hat_i^t
            reward <- - query_BCE(D_i^u, theta_hat_i^t)
            next_state <- state + (action, answer)
            done <- 是否到达 T 或停止条件
            B.add(state, action, reward, next_state, done)
            state <- next_state

    若 B 中样本足够：
        从 B 抽 mini-batch
        构造 masked Bellman target
        更新 phi

    定期同步 bar_phi <- phi
    在验证学生上选超参数并早停
```

## 5. 部署新学生的完整闭环

训练结束后，新学生没有 support/query 切分，也没有隐藏 reward。系统使用真实题库：

```text
输入：
    训练好的响应模型全局参数
    训练好的 Q 网络
    真实题库与约束

初始化：
    state <- empty
    theta_hat <- 先验或初始学生表示
    asked <- empty

重复：
    valid <- 题库减去 asked，再应用内容、敌题、曝光等约束
    计算 Q(state, ·)
    从 valid 中 argmax 或按温度分布抽一道题 q
    向学生呈现 q
    接收实时答案 a
    state <- state + (q, a)
    asked <- asked + q
    用累计作答更新 theta_hat

    若满足停止规则：
        输出 theta_hat、标准误或诊断结果
        结束
```

!!! tip "实时反馈进入哪里"

    学生每次提交答案后，\((q_t,a_t)\) 立即写入状态；响应模型更新学生参数；NCAT encoder 重新计算双通道 attention；动作 mask 删除已答题；随后才选择 \(q_{t+1}\)。这正是逐题自适应。

## 6. 停止规则

原论文实验为固定长度 \(T=20\)，但真实 CAT 可以采用：

- 达到最大题数；
- 能力估计标准误低于阈值；
- 后验可信区间足够窄；
- 分类决策置信度达到阈值；
- 知识点蓝图已经满足；
- 时间预算耗尽；
- 预计再问一道题的边际效用低于成本。

若训练阶段始终固定 \(T\)，而部署采用变量长度停止，训练目标最好显式覆盖不同停止步，或把 `done` 机制和停止状态纳入环境。

## 7. 训练、评价、部署三个策略

| 阶段 | 选题方式 | 目的 |
|---|---|---|
| 训练 | epsilon-greedy | 探索状态-动作空间 |
| 离线评价 | argmax 或论文温度采样 | 比较测量与曝光指标 |
| 部署 | 受约束的 argmax/采样 | 在精度、安全和蓝图中折中 |

评价时应固定随机种子并多次采样；否则温度策略产生的单条随机轨迹会让结果方差很大。

## 8. 内容与安全约束怎样接入

设题 \(q\) 属于内容类别 \(c(q)\)，每类题有下限 \(L_k\) 和上限 \(U_k\)。在第 \(t\) 步可先构造可行集合：

\[
\mathcal A_t^{\mathrm{feasible}}
=
\left\{
q\in\mathcal A_t:
\text{选择 }q\text{ 后仍存在完成蓝图的可行路径}
\right\}.
\tag{1}
\]

然后只在该集合上比较 Q 值：

\[
q_t
=
\arg\max_{q\in\mathcal A_t^{\mathrm{feasible}}}
Q_\phi(s_t,q).
\tag{2}
\]

简单上限可以用 mask 处理；同时满足多内容下限、敌题、题组、时间和曝光约束时，shadow test 或整数规划更可靠。软惩罚可加入 reward：

\[
r_t^{\mathrm{total}}
=
r_t^{\mathrm{measure}}
-\lambda_{\mathrm{content}}C_t
-\lambda_{\mathrm{exposure}}E_t
-\lambda_{\mathrm{time}}H_t.
\tag{3}
\]

其中 \(C_t,E_t,H_t\) 分别表示内容偏差、曝光风险和时间成本。软惩罚用于权衡，硬 mask 或组合优化层用于保证可行性。

下一页用一组小数据完整走过[状态编码、选题、学生更新、reward 和 TD 更新](06-worked-example.md)。
