# 符号表、结论与阅读地图

## 1. 主要符号

| 符号 | 含义 |
|---|---|
| \(\mathcal S\) | 状态空间 |
| \(s,s'\) | 当前状态与下一状态 |
| \(S^{(t)}\) | 第 \(t\) 步状态随机变量 |
| \(\mathcal A\) | 动作空间 |
| \(a,a'\) | 当前动作与候选下一动作 |
| \(A^{(t)}\) | 第 \(t\) 步动作随机变量 |
| \(\mathcal P(s'\mid s,a)\) | 状态转移核 |
| \(\mathcal R(s,a,s')\) | 奖励函数 |
| \(r,R^{(t)}\) | 奖励取值与奖励随机变量 |
| \(\gamma\) | 折扣因子 |
| \(\pi\) | 材料选择策略 |
| \(Q^\pi(s,a)\) | 策略 \(\pi\) 下的动作价值 |
| \(Q^*(s,a)\) | 最优动作价值 |
| \(\widehat Q(s,a;\mathbf w)\) | DQN 对最优 Q 值的近似 |
| \(\mathbf w\) | DQN 参数 |
| \(D\) | 能力维数 |
| \(L\) | 材料数量 |
| \(\boldsymbol\theta\) | 潜在能力向量 |
| \(\widehat{\boldsymbol\theta}\) | 估计能力 |
| \(h_d\) | 第 \(d\) 维的目标能力 |
| \(\mathbf1_D\) | \(D\) 维全 1 目标向量 |
| \(\|\cdot\|_\infty\) | 向量分量绝对值的最大值 |
| \(\Delta\boldsymbol\theta\) | 一轮学习后的能力增量 |
| \(\varepsilon\) | epsilon-greedy 探索概率 |
| \(\alpha\) | DQN 学习率 |
| \(\mathcal H\) | 历史经验回放池 |
| \(\mathcal M\) | 一次更新的 mini-batch |
| \(M\) | mini-batch 大小 |
| \(E\) | 训练 episode 数 |
| \(y\) | Bellman/TD target |
| \(\delta\) | TD 误差 |
| \(\psi_v(s,a)\) | 转移模型的下一状态预测 |
| \(v\) | 转移模型参数 |
| \(b_t(\theta)\) | 潜在状态的 belief 或后验分布 |

## 2. 公式主线

### 测量

\[
\Pr(U=u\mid\boldsymbol\theta)
=
f(\boldsymbol\theta,\boldsymbol\eta,u).
\]

### 状态与动作

\[
s=\boldsymbol\theta\in[0,1]^D,
\qquad
a\in\{1,\ldots,L\}.
\]

### 转移

\[
s'\sim\mathcal P(\cdot\mid s,a).
\]

### 奖励

\[
r
=
\begin{cases}
-1,
&
\|s'-\mathbf1_D\|_\infty\ge10^{-3},
\\
0,
&
\|s'-\mathbf1_D\|_\infty<10^{-3}.
\end{cases}
\]

### Q 函数

\[
Q^\pi(s,a)
=
\mathbb E
\left[
\sum_{t=0}^{\infty}
\gamma^tR^{(t)}
\mid
S^{(0)}=s,
A^{(0)}=a;
\pi
\right].
\]

### Bellman 方程

\[
Q^*(s,a)
=
\mathbb E
\left[
R+\gamma\max_{a'}Q^*(S',a')
\mid s,a
\right].
\]

### TD target

\[
y
=
r+\gamma\max_{a'}\widehat Q(s',a';\mathbf w).
\]

终止状态使用 \(y=r\)。

### 转移模型

\[
\widehat s'=\psi_v(s,a),
\]

\[
\min_v
\sum_i
\|\psi_v(s_i,a_i)-s_i'\|_2^2.
\]

## 3. 论文的算法闭环

```text
当前能力估计
    │
    ▼
DQN 计算所有材料的长期价值
    │
    ▼
epsilon-greedy 选择一份材料
    │
    ▼
真实学生学习，或转移模型生成下一状态
    │
    ▼
未达标得 -1，达标得 0
    │
    ▼
transition 进入 replay buffer
    │
    ▼
TD 更新 DQN
    │
    └────────► 下一轮重新决策
```

## 4. 六条核心结论

1. 自适应学习是一个闭环序列决策问题，每轮反馈都会改变下一动作。
2. 连续能力向量为 DQN 提供细粒度状态，并可通过 IRT/MIRT 测量。
3. 每步 \(-1\) 把“尽快达到目标”转成最大化长期回报。
4. DQN 用 Bellman target 从转移样本学习，不要求预先知道真实转移核。
5. 转移模型可以复用少量真实学生数据，但会引入模型偏差与长轨迹误差。
6. 论文结果来自二维人工模拟，真实教育有效性仍需离线因果评价和在线试验。

## 5. 实验数字速查

| 项目 | 结果 |
|---|---|
| DQN reward | \(-13.49\pm4.59\) |
| 启发式 reward | \(-21.55\pm4.76\) |
| 随机 reward | \(-24.85\pm5.59\) |
| 约稳定所需 episode | 约 600 |
| 转移模型测试 \(R^2\) | 0.95–0.97 |
| 转移模型 RMSE | 0.08–0.11 |
| virtual model 明显有利区间 | 不超过约 200 名真实学生 |

这些数字属于论文设定的模拟环境。

## 6. 从论文走向研究问题

若把这篇论文作为生成式 CAT 或教育推荐研究的起点，可以沿四层推进：

### 状态层

- 点估计升级为后验分布；
- 纳入作答历史、材料历史、时间和疲劳；
- 使用序列模型或大模型表示语义状态。

### 动作层

- 从材料编号扩展到语义内容；
- 生成候选题或候选材料；
- 通过 mask、shadow test 或约束优化保证可行。

### 目标层

- 学习增益；
- 测量精度；
- 内容平衡；
- 学习时间；
- 认知负荷；
- 曝光、公平与安全。

### 评价层

- 模拟验证；
- 离线策略评价；
- 转移模型校准；
- 小流量在线试验；
- 长期保持与迁移。

## 7. 推荐的跨专题阅读

- [NCAT：Q-learning 学习逐题 CAT 策略](../ncat/index.md)
- [BOBCAT：双层优化学习 CAT 选题](../bobcat/index.md)
- [CAT 总览](../index.md)
- [本专题参考文献](references.md)

## 8. 最终图景

\[
\boxed{
\begin{aligned}
\text{学生反馈}
&\longrightarrow
\text{能力测量}
\\
&\longrightarrow
\text{闭环材料策略}
\\
&\longrightarrow
\text{真实能力变化}
\\
&\longrightarrow
\text{再次反馈与重规划}.
\end{aligned}
}
\]

论文的核心产物是一条可反复调用的决策规则。学生实际经历的学习序列由这条规则与逐轮真实反馈共同生成。
