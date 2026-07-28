# MDP、Q 函数与 Bellman 方程

本页对应预印本式 (3)–(7)，重点说明每个随机变量、条件概率和期望的含义。

## 1. MDP 五元组

一个马尔可夫决策过程写为

\[
\mathcal M
=
\left(
\mathcal S,
\mathcal A,
\mathcal P,
\mathcal R,
\gamma
\right).
\]

| 对象 | 含义 | 自适应学习中的对应物 |
|---|---|---|
| \(\mathcal S\) | 状态空间 | 所有可能的能力向量 |
| \(\mathcal A\) | 动作空间 | 所有可推荐材料 |
| \(\mathcal P\) | 状态转移规律 | 学完材料后能力怎样变化 |
| \(\mathcal R\) | 奖励函数 | 当前一步对目标的数值反馈 |
| \(\gamma\) | 折扣因子 | 未来奖励的相对权重 |

策略 \(\pi\) 是待学习的决策规则，通常不放在环境五元组内。

## 2. 转移样本

一次交互产生：

\[
(s,a,r,s').
\tag{8}
\]

时间顺序为：

1. 当前处于状态 \(s\)；
2. 策略选择动作 \(a\)；
3. 环境进入下一状态 \(s'\)；
4. 根据 \(s,a,s'\) 得到奖励 \(r=\mathcal R(s,a,s')\)。

下一状态 \(s'\) 决定后续价值，因此经验数据必须保存它。

## 3. 随机变量与具体取值

论文使用：

- \(S^{(t)}\)：第 \(t\) 步状态随机变量；
- \(A^{(t)}\)：第 \(t\) 步动作随机变量；
- \(R^{(t)}\)：第 \(t\) 步奖励随机变量；
- \(s,a,r\)：这些随机变量的具体取值。

区分大小写可以避免把“下一状态的分布”与“实际观察到的一个下一状态”混为一谈。

## 4. 一步转移概率

初稿式 (3) 为

\[
\mathcal P^{(t)}(s'\mid s,a)
=
\Pr\!\left(
S^{(t+1)}=s'
\mid
S^{(t)}=s,
A^{(t)}=a
\right).
\tag{9}
\]

它回答：

> 当前能力为 \(s\)，本轮选择材料 \(a\)，下一轮能力落在 \(s'\) 的概率是多少？

连续状态下，\(\mathcal P\) 应理解为条件概率密度或转移核。

## 5. 马尔可夫性

初稿式 (4) 为

\[
\Pr\!\left(
S^{(t+1)}
\mid
A^{(t)},S^{(t)},\ldots,A^{(0)},S^{(0)}
\right)
=
\Pr\!\left(
S^{(t+1)}
\mid
A^{(t)},S^{(t)}
\right).
\tag{10}
\]

给定当前状态和当前动作后，更早历史不再额外改善对下一状态的预测。

这项性质要求状态包含与未来有关的历史摘要。若疲劳、学习时长、材料重复次数和先修路径仍影响学习效果，状态可以扩展为

\[
s_t
=
\left(
\boldsymbol\theta_t,
f_t,
\Delta t_t,
\mathbf c_t
\right),
\]

其中 \(f_t\) 表示疲劳，\(\Delta t_t\) 表示距上次学习的时间，\(\mathbf c_t\) 表示材料使用计数。

## 6. 时间齐性

初稿式 (5) 为

\[
\mathcal P^{(t_1)}(s'\mid s,a)
=
\mathcal P^{(t_2)}(s'\mid s,a).
\tag{11}
\]

它表示同一状态和动作在不同时间具有相同转移规律。满足后可省略时间上标：

\[
\mathcal P(s'\mid s,a).
\]

马尔可夫性讨论历史条件，时间齐性讨论规律是否随时间改变。两者是不同条件。

## 7. 策略

确定性策略为

\[
\pi:\mathcal S\rightarrow\mathcal A,
\qquad
a=\pi(s).
\]

随机策略为

\[
\pi(a\mid s)
=
\Pr(A^{(t)}=a\mid S^{(t)}=s).
\]

DQN 部署常使用贪心策略，训练时使用 \(\varepsilon\)-greedy 引入随机探索。

## 8. 折扣累计回报

从时刻 0 开始：

\[
G^{(0)}
=
\sum_{k=0}^{\infty}
\gamma^k R^{(k)}.
\tag{12}
\]

若奖励依次为 \(-1,-1,-1,0\)，且 \(\gamma=0.9\)，则

\[
G^{(0)}
=
-1-0.9-0.9^2
=
-2.71.
\]

更快到达目标时，负奖励项更少，回报更接近 0。

## 9. 策略下的动作价值

初稿式 (6)：

\[
Q^\pi(s,a)
=
\mathbb E
\left[
\sum_{t=0}^{\infty}
\gamma^tR^{(t)}
\;\middle|\;
S^{(0)}=s,
A^{(0)}=a;
\pi
\right].
\tag{13}
\]

它表示：

> 现在处于 \(s\)，第一步固定选择 \(a\)，之后遵循 \(\pi\)，最终折扣回报的期望是多少？

期望同时平均：

- 学习转移的随机性；
- 后续随机策略的动作；
- 由这些随机性产生的全部轨迹。

## 10. 最优动作价值

\[
Q^*(s,a)
=
\max_\pi Q^\pi(s,a).
\tag{14}
\]

得到 \(Q^*\) 后：

\[
\pi^*(s)
\in
\arg\max_{a\in\mathcal A}
Q^*(s,a).
\tag{15}
\]

若所有 Q 值均为负，仍选择数值最大的一个，因为它最接近 0，对应较少的预期剩余步骤。

## 11. Bellman 最优方程

初稿式 (7)：

\[
Q^*(s,a)
=
\mathbb E\!\left[R^{(0)}\mid s,a\right]
+
\gamma
\int_{\mathcal S}
\mathcal P(ds'\mid s,a)
\max_{a'\in\mathcal A}
Q^*(s',a').
\tag{16}
\]

离散状态时，积分写成求和：

\[
Q^*(s,a)
=
\mathbb E\!\left[R^{(0)}\mid s,a\right]
+
\gamma
\sum_{s'\in\mathcal S}
\mathcal P(s'\mid s,a)
\max_{a'}Q^*(s',a').
\tag{17}
\]

右侧包含：

1. 当前一步的期望奖励；
2. 下一状态中可获得的最优后续价值。

## 12. Bellman 方程的逐步推导

从最优回报定义出发：

\[
Q^*(s,a)
=
\mathbb E
\left[
R^{(0)}
+\gamma R^{(1)}
+\gamma^2R^{(2)}
+\cdots
\mid s,a
\right].
\]

提出第一项：

\[
Q^*(s,a)
=
\mathbb E
\left[
R^{(0)}
+\gamma
\left(
R^{(1)}
+\gamma R^{(2)}
+\cdots
\right)
\mid s,a
\right].
\]

括号内是从下一状态开始的最优回报：

\[
R^{(1)}
+\gamma R^{(2)}
+\cdots
\longrightarrow
\max_{a'}Q^*(S^{(1)},a').
\]

于是得到：

\[
Q^*(s,a)
=
\mathbb E
\left[
R^{(0)}
+\gamma\max_{a'}Q^*(S^{(1)},a')
\mid s,a
\right].
\tag{18}
\]

这也是 TD target 的理论来源。

## 13. 唯一性与压缩映射直觉

定义 Bellman 最优算子：

\[
(\mathcal TQ)(s,a)
=
\mathbb E
\left[
R+\gamma\max_{a'}Q(S',a')
\mid s,a
\right].
\]

当 \(0\le\gamma<1\) 时：

\[
\|\mathcal TQ_1-\mathcal TQ_2\|_\infty
\le
\gamma
\|Q_1-Q_2\|_\infty.
\tag{19}
\]

\(\mathcal T\) 把两个函数之间的最大差距至少缩小为原来的 \(\gamma\) 倍，因此存在唯一固定点 \(Q^*=\mathcal TQ^*\)。DQN 用神经网络近似这个固定点。
