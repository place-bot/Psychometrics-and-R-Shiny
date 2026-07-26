# Q-learning 与经验回放

## 1. Q 值回答的问题

给定当前状态 \(s_t\) 和候选题 \(q\)，动作价值函数定义为

\[
Q^\pi(s_t,q)
=
\mathbb E_\pi
\left[
\sum_{k=t}^{T}
\gamma^{k-t}r_k
\;\middle|\;
s_t,\ q_t=q
\right].
\tag{1}
\]

它表示：现在先选择 \(q\)，之后继续按策略 \(\pi\) 选题，预期能得到多少折扣累计 reward。

!!! warning "Q 值的单位"

    \(Q_\phi(s_t,q)\) 不是学生答对题 \(q\) 的概率，也不是题目难度、Fisher 信息或知识点覆盖率。论文 reward 来自负 query BCE，因此 Q 值学习的是未来测量损失所对应的长期价值，数值可以为负。

## 2. Bellman 最优递推

最优 Q 函数满足

\[
Q^*(s_t,q_t)
=
\mathbb E
\left[
r_t
+
\gamma
\max_{q'\in\mathcal A_{t+1}}
Q^*(s_{t+1},q')
\right].
\tag{2}
\]

该式把“整段测验是否好”拆成两部分：

- 当前选题带来的即时 reward \(r_t\)；
- 进入新状态后，下一步可获得的最佳长期价值。

神经网络 \(Q_\phi\) 同时给所有题输出一个分数向量：

\[
Q_\phi(s_t,\cdot)
=
\left[
Q_\phi(s_t,q_1),\ldots,Q_\phi(s_t,q_{|\mathcal J|})
\right].
\tag{3}
\]

## 3. TD target

对一条 transition

\[
(s_t,q_t,r_t,s_{t+1},d_t),
\]

其中 \(d_t=1\) 表示本步后测验终止，目标值写为

\[
y_t
=
r_t
+
\gamma(1-d_t)
\max_{q'\in\mathcal A_{t+1}}
Q_{\bar\phi}(s_{t+1},q').
\tag{4}
\]

\(Q_{\bar\phi}\) 是 target network；若严格复刻没有 target network 的旧实现，也可以暂用当前网络计算 bootstrap，但训练通常更不稳定。

TD 损失为

\[
\mathcal L_{\mathrm{TD}}(\phi)
=
\mathbb E_{(s,q,r,s',d)\sim\mathcal B}
\left[
\left(
y-Q_\phi(s,q)
\right)^2
\right].
\tag{5}
\]

只有本次动作 \(q_t\) 对应的输出进入 MSE：

\[
Q_\phi(s_t,q_t)
=
\operatorname{gather}
\left(
Q_\phi(s_t,\cdot),q_t
\right).
\]

## 4. 一个 TD 数字例子

设某一步：

\[
r_t=-0.50,\qquad
\gamma=0.80,\qquad
\max_{q'}Q_{\bar\phi}(s_{t+1},q')=-0.20.
\]

若尚未终止，

\[
y_t
=
-0.50+0.80(-0.20)
=
-0.66.
\]

当前网络若预测

\[
Q_\phi(s_t,q_t)=-0.40,
\]

则该样本的平方误差为

\[
(-0.66+0.40)^2
=
0.0676.
\]

若这一步已经终止，bootstrap 项必须消失：

\[
y_t=r_t=-0.50.
\]

## 5. 经验回放

训练过程中把 transition 存入 replay buffer：

\[
\mathcal B
=
\{
(s_t,q_t,r_t,s_{t+1},d_t)
\}.
\]

每隔若干交互，从 \(\mathcal B\) 随机抽一个 mini-batch 更新网络。这样做有三个作用：

1. 重复利用昂贵的离线轨迹；
2. 打散相邻时间步的强相关性；
3. 让每次更新同时覆盖不同学生、不同测试步和不同动作。

一个简化的数据结构是：

```python
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity):
        self.data = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.data.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.data, batch_size)
```

## 6. 合法动作 mask

在求 argmax 和 bootstrap 最大值之前，都必须屏蔽不合法题：

\[
\widetilde Q_\phi(s_t,q)
=
\begin{cases}
Q_\phi(s_t,q), & q\in\mathcal A_t,\\
-\infty, & q\notin\mathcal A_t.
\end{cases}
\tag{6}
\]

否则网络可能重复选择已答题，或在离线训练中选到没有历史答案的题。

```python
masked_q = q_values.masked_fill(~valid_mask, float("-inf"))
action = masked_q.argmax(dim=-1)
```

同样的 `valid_mask` 逻辑必须用于：

- 行为策略选动作；
- TD target 中的 `max Q(next_state, ·)`；
- 部署时的 argmax 或温度采样；
- 内容、敌题、题型和曝光等硬约束。

## 7. epsilon-greedy 用于训练探索

训练阶段，若总选当前最大 Q 值题，状态-动作空间会探索不足。epsilon-greedy 定义为：

\[
q_t
=
\begin{cases}
\text{从 }\mathcal A_t\text{ 随机选题}, & \text{概率 }\varepsilon,\\
\arg\max_{q\in\mathcal A_t}Q_\phi(s_t,q), & \text{概率 }1-\varepsilon.
\end{cases}
\tag{7}
\]

论文报告 \(\varepsilon\) 在训练中从 1 衰减到 0。公开代码使用另一条随训练计数衰减的随机动作概率，应以实际配置记录为准。

## 8. 温度采样用于施测路径随机化

论文在测试过程中把 Q 值转成概率：

\[
\Pr(q\mid s_t)
=
\frac{
\exp\!\left(Q_\phi(s_t,q)/\nu_t\right)
}{
\sum_{q'\in\mathcal A_t}
\exp\!\left(Q_\phi(s_t,q')/\nu_t\right)
}.
\tag{8}
\]

并设置

\[
\nu_t=2^{-0.1t}.
\tag{9}
\]

早期温度较高，题目路径更分散；后期温度变低，选择更接近最大 Q 值。若 \(\nu\to0\)，式 (8) 退化为确定性 argmax。

## 9. 三个参数不要混用

| 参数 | 出现位置 | 控制内容 | 常见调度 |
|---|---|---|---|
| \(\gamma\) | TD target | 未来 reward 的权重 | 固定或训练期调度 |
| \(\varepsilon\) | 训练行为策略 | 随机探索动作的概率 | 从高到低 |
| \(\nu_t\) | 部署/评价选题分布 | Q 值分布的尖锐程度 | 随测试步降低 |

温度随机化可以降低平均曝光，但它不自动保证最大曝光率上限、内容蓝图或题目安全。正式约束应进入合法动作 mask、shadow test 或约束优化层。

## 10. 建议的稳定 DQN 版本

一个较稳妥的现代实现通常包含：

1. online network \(Q_\phi\)；
2. target network \(Q_{\bar\phi}\)；
3. replay buffer；
4. 合法动作 mask；
5. 梯度裁剪；
6. 周期性硬同步或 Polyak 软更新；
7. Double DQN，以 online network 选动作、target network 估值。

Double DQN target 可写成

\[
q^*
=
\arg\max_{q'\in\mathcal A_{t+1}}
Q_\phi(s_{t+1},q'),
\]

\[
y_t
=
r_t+\gamma(1-d_t)
Q_{\bar\phi}(s_{t+1},q^*).
\]

这些是工程强化，并不改变 NCAT 的状态编码思想。下一页进入网络核心：[状态编码与双通道 attention](04-neural-encoder.md)。
