# Q-learning 与经验回放：从一次选题到一次网络更新

这一页先暂时放下 attention，只研究一个问题：

> 已知学生当前已经答过哪些题、每题答对还是答错，NCAT 怎样学会选择下一道题？

Q-learning 位于 NCAT 的“选题器”内部。它不负责估计学生能力；学生能力仍由 IRT、NCDM 等响应模型更新。Q-learning 负责比较各道候选题的**长期选题价值**。

整条训练链是：

```text
当前作答历史
    ↓
Q 网络给每道题一个长期价值
    ↓
从合法候选题中选择一道题
    ↓
读取该学生对这道题的历史答案
    ↓
响应模型更新该学生参数
    ↓
在 query 题上计算预测损失
    ↓
负损失作为 reward
    ↓
把本次交互放进 replay buffer
    ↓
用 TD target 更新 Q 网络
```

下面始终使用同一个小例子，把每个字母和每一步计算串起来。

## 1. 从一次 CAT 交互开始

### 1.1 先看一条完整的交互记录

假设题库只有五道题：

\[
\mathcal J=\{q_1,q_2,q_3,q_4,q_5\}.
\]

学生已经：

- 答对 \(q_2\)；
- 答错 \(q_5\)；
- 尚未回答 \(q_1,q_3,q_4\)。

在第 \(t\) 步做决定之前，系统掌握的状态是

\[
s_t=\{(q_2,1),(q_5,0)\}.
\]

其中：

- \(s\) 是 state，即状态；
- 下标 \(t\) 表示当前是第 \(t\) 个决策时刻；
- \((q_2,1)\) 表示题 \(q_2\) 答对；
- \((q_5,0)\) 表示题 \(q_5\) 答错。

当前合法候选题集合为

\[
\mathcal A_t=\{q_1,q_3,q_4\}.
\]

假设 NCAT 选择了

\[
q_t=q_3.
\]

离线日志显示，该学生对 \(q_3\) 的答案是 0。系统把这条答案加入历史：

\[
s_{t+1}
=
\{(q_2,1),(q_5,0),(q_3,0)\}.
\]

响应模型用这三道已选题重新估计学生参数，然后在 query 集上得到

\[
\mathcal L_{t}=0.42.
\]

NCAT 把 query 损失的相反数作为奖励：

\[
r_t=-\mathcal L_t=-0.42.
\]

若测验还没有结束，则

\[
d_t=0.
\]

这一步最终形成一条 transition：

\[
\left(
s_t,q_t,r_t,s_{t+1},d_t
\right)
=
\left(
s_t,q_3,-0.42,s_{t+1},0
\right).
\tag{1}
\]

**一条 transition 中每个量的含义**

| 记号 | 全称 | 在例子中的值 | 表示什么 |
|---|---|---|---|
| \(s_t\) | current state | \(\{(q_2,1),(q_5,0)\}\) | 选题前已知的作答历史 |
| \(q_t\) | action | \(q_3\) | 本步真正选择的题 |
| \(r_t\) | reward | \(-0.42\) | 选题并更新学生后得到的测量质量 |
| \(s_{t+1}\) | next state | 再加入 \((q_3,0)\) | 学生回答后的新状态 |
| \(d_t\) | done | 0 | 本步后测验是否结束 |

学生对 \(q_3\) 的答案已经包含在 \(s_{t+1}\) 中，所以最简 transition 通常不再单独保存 \(a_t\)。实际实现为了调试，也可以额外保存答案。

!!! tip "时间顺序一定要记清"

    \(s_t\) 是答 \(q_t\) **之前**的状态；\(s_{t+1}\) 是得到 \(q_t\) 的答案**之后**的状态。Q 网络使用 \(s_t\) 决定 \(q_t\)，不能提前看到 \(s_{t+1}\)。

### 1.2 reward 到底在奖励什么

NCAT 在第 \(t\) 步的 reward 定义为

\[
r_t
=
-\mathcal L_M
\left(
\mathcal D_i^u,\widehat\theta_i^{\,t}
\right).
\tag{2}
\]

逐个拆开：

| 记号 | 含义 |
|---|---|
| \(i\) | 当前训练学生 |
| \(\mathcal D_i^u\) | 学生 \(i\) 的 query 集 |
| \(\widehat\theta_i^{\,t}\) | 用前 \(t\) 道已选题估计出的学生参数 |
| \(M\) | IRT、NCDM 等响应模型 |
| \(\mathcal L_M\) | 响应模型在 query 题上的平均 BCE |
| \(r_t\) | query BCE 的相反数 |

假设两种选题结果如下：

| 本步选题 | 更新后的 query BCE | reward |
|---|---:|---:|
| 选择 \(q_3\) | 0.42 | \(-0.42\) |
| 选择 \(q_4\) | 0.55 | \(-0.55\) |

比较 reward：

\[
-0.42>-0.55.
\]

因此 \(q_3\) 的本步结果更好。reward 虽然是负数，但大小关系完全正常：

- query loss 越小；
- reward 越接近 0；
- 该结果越好。

**reward 评价的是累计已选题**

第 \(t\) 步的 query loss 使用

\[
\mathcal D_i^s(t)
=
\{(q_1,a_1),\ldots,(q_t,a_t)\}
\]

估计学生。因此 \(r_t\) 评价的是“截至目前这组题的测量结果”，并不只评价第 \(t\) 道题孤立产生的效果。

前面的题已经改变了学生参数和当前状态，所以同一道题在不同状态下可能得到不同 reward。

## 2. Q 值怎样表示长期选题价值

### 2.1 即时 reward 和 Q 值为什么要分开

reward \(r_t\) 只描述**本次选题之后**的结果。Q 值还要考虑这道题会把系统带到什么新状态，以及后面还能怎样选题。

假设当前有两个候选动作。

**路径 A：现在选择题 3**

未来三步 reward 为

\[
-0.42,\quad -0.30,\quad -0.24.
\]

**路径 B：现在选择题 4**

未来三步 reward 为

\[
-0.35,\quad -0.50,\quad -0.45.
\]

只看第一步，路径 B 的 \(-0.35\) 大于路径 A 的 \(-0.42\)。但是路径 B 把学生带入了一个后续测量效果较差的状态。

设折扣因子为

\[
\gamma=0.8.
\]

路径 A 的折扣累计 reward 是

\[
G_t^{A}
=
-0.42
+0.8(-0.30)
+0.8^2(-0.24)
=
-0.8136.
\]

路径 B 的折扣累计 reward 是

\[
G_t^{B}
=
-0.35
+0.8(-0.50)
+0.8^2(-0.45)
=
-1.038.
\]

因为

\[
-0.8136>-1.038,
\]

考虑整条后续路径时，选择 \(q_3\) 更好。

这就是 Q-learning 的核心动机：**选题时比较长期结果，而不只比较下一秒的即时结果。**

### 2.2 从累计 reward 定义 Q 值

从第 \(t\) 步开始的折扣累计 reward 记为 return：

\[
G_t
=
r_t
+\gamma r_{t+1}
+\gamma^2r_{t+2}
+\cdots
+\gamma^{T-t}r_T.
\tag{3}
\]

动作价值函数定义为

\[
Q^\pi(s_t,q)
=
\mathbb E_\pi
\left[
G_t
\;\middle|\;
s_t,\ q_t=q
\right].
\tag{4}
\]

把式 (3) 代回去：

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
\tag{5}
\]

**式 (5) 逐段翻译**

| 片段 | 中文含义 |
|---|---|
| \(Q^\pi(s_t,q)\) | 在状态 \(s_t\) 先选题 \(q\)，之后按策略 \(\pi\) 行动的长期价值 |
| \(q_t=q\) | 强制本步先选择题 \(q\) |
| \(\pi\) | 从下一步开始使用的选题策略 |
| \(r_k\) | 第 \(k\) 步的 reward |
| \(\gamma^{k-t}\) | 第 \(k\) 步 reward 的折扣权重 |
| \(T\) | 测验终止步 |
| \(\mathbb E_\pi\) | 对未来学生答案和后续选题路径取平均 |

之所以出现期望 \(\mathbb E\)，是因为未来还没有发生：

- 学生下一题可能答对，也可能答错；
- 不同答案会产生不同状态；
- 策略可能含随机探索或温度采样；
- 不同未来路径会产生不同 reward。

Q 值把这些可能路径的长期结果汇总成一个期望分数。

### 2.3 三种 Q 记号的关系

读论文和代码时常看到三种写法。

**给定策略的真实价值**

\[
Q^\pi(s,q)
\]

表示之后一直按指定策略 \(\pi\) 行动时的真实期望价值。

**最优价值**

\[
Q^*(s,q)
=
\max_\pi Q^\pi(s,q)
\]

表示本步先选 \(q\)，之后始终采用最佳选题方式时能达到的价值。

**神经网络的近似值**

\[
Q_\phi(s,q)
\approx
Q^*(s,q).
\]

\(\phi\) 是神经网络参数。训练开始时 \(Q_\phi\) 基本是随机预测；经过大量 transition 的 TD 更新后，它逐渐逼近 \(Q^*\)。

**和 CAT 中其他分数放在一起看**

| 数量 | 谁计算 | 数值含义 |
|---|---|---|
| \(M(q\mid\theta)\) | 响应模型 | 学生答对题 \(q\) 的概率 |
| Fisher 信息 | IRT criterion | 该题在某能力位置提供的局部测量信息 |
| \(r_t\) | 离线训练环境 | 本步更新后 query loss 的相反数 |
| \(Q_\phi(s_t,q)\) | NCAT 选题网络 | 现在选 \(q\) 后的预计长期累计 reward |

这四个量可以排序不同，因为它们回答的是不同问题。

### 2.4 折扣因子 gamma 怎样影响长期价值

\(\gamma\) 的取值范围通常是

\[
0\le\gamma\le1.
\]

它控制未来 reward 在当前 Q 值中占多大比重。

| \(\gamma\) | 解释 |
|---:|---|
| 0 | 只看本步 reward |
| 0.5 | 后续每远一步，权重再乘 0.5 |
| 0.8 | 保留较多长期信息 |
| 1 | 所有未来步不折扣 |

假设未来 reward 都是 \(-0.4\)，三步 return 为：

**当 gamma 等于 0**

\[
G_t=-0.4.
\]

**当 gamma 等于 0.5**

\[
G_t
=
-0.4+0.5(-0.4)+0.5^2(-0.4)
=
-0.7.
\]

**当 gamma 等于 1**

\[
G_t
=
-0.4-0.4-0.4
=
-1.2.
\]

!!! warning "NCAT 理论目标与代码折扣"

    论文的双层外层目标把第 1 到第 \(T\) 步的 query loss 等权相加，对应未折扣目标。DQN 若设置 \(\gamma<1\)，较早步骤会获得更高权重。公开 shell 示例使用 \(\gamma=0.8\)，所以复现时应把 \(\gamma\) 视为会改变目标权重的超参数。

## 3. Bellman 方程怎样把长期问题拆开

### 3.1 Bellman 递推从哪里来

return 可以把第一步单独拆出来：

\[
\begin{aligned}
G_t
&=
r_t+\gamma r_{t+1}+\gamma^2r_{t+2}+\cdots\\
&=
r_t+\gamma
\left(
r_{t+1}+\gamma r_{t+2}+\cdots
\right)\\
&=
r_t+\gamma G_{t+1}.
\end{aligned}
\tag{6}
\]

这句话非常关键：

> 从现在开始的长期结果 = 当前 reward + 折扣后的下一状态长期结果。

若下一步之后都采用最优动作，得到 Bellman 最优方程：

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
\tag{7}
\]

**式 (7) 中每个符号**

| 符号 | 含义 |
|---|---|
| \(s_t\) | 本步选题前的状态 |
| \(q_t\) | 本步选择的题 |
| \(r_t\) | 学生回答并更新响应模型后得到的 reward |
| \(s_{t+1}\) | 加入本题真实答案后的状态 |
| \(\mathcal A_{t+1}\) | 下一状态的合法候选题集合 |
| \(q'\) | 下一步可能选择的某道题 |
| \(\max_{q'}\) | 在下一步所有合法题中取价值最高者 |
| \(\gamma\) | 下一状态价值的折扣 |
| \(\mathbb E\) | 对未知学生反应和状态转移取期望 |

Bellman 方程让我们不必等整场测验结束后才学习。每一条一步 transition 都可以产生一个训练信号。

### 3.2 Q 网络怎样同时评价所有题

NCAT 的 Q 网络输入当前状态 \(s_t\)，输出长度为题库大小的向量：

\[
Q_\phi(s_t,\cdot)
=
\left[
Q_\phi(s_t,q_1),
Q_\phi(s_t,q_2),
\ldots,
Q_\phi(s_t,q_5)
\right].
\tag{8}
\]

延续前面的五题例子，假设网络输出

\[
Q_\phi(s_t,\cdot)
=
[-0.62,-0.31,-0.44,-0.28,-0.57].
\]

当前已经回答 \(q_2,q_5\)，所以合法集合为

\[
\mathcal A_t=\{q_1,q_3,q_4\}.
\]

屏蔽非法题后：

\[
\widetilde Q_\phi(s_t,\cdot)
=
[-0.62,-\infty,-0.44,-0.28,-\infty].
\]

最大值是

\[
-0.28,
\]

对应题 \(q_4\)。若当前采用 greedy 策略，就选择

\[
q_t=q_4.
\]

这里的“最大”表示最接近 0。由于 reward 来自负损失，长期损失较小的题通常得到更大的 Q 值。

## 4. 一条 transition 怎样更新 Q 网络

### 4.1 选一道题后，训练数据怎样产生

假设本步选择 \(q_4\)。离线训练环境按以下顺序运行。

**第一步：查询历史答案**

学生历史上对 \(q_4\) 答对：

\[
a_t=1.
\]

**第二步：更新状态**

\[
s_{t+1}
=
s_t\cup\{(q_4,1)\}.
\]

**第三步：更新学生参数**

响应模型只使用累计已选 support 题：

\[
\widehat\theta_i^{\,t}
=
\arg\min_{\theta_i}
\sum_{(q,a)\in\mathcal D_i^s(t)}
\ell
\left(
a,M(q\mid\theta_i)
\right).
\]

**第四步：在 query 集上评价**

假设 query BCE 为

\[
\mathcal L_t=0.35.
\]

**第五步：构造 reward**

\[
r_t=-0.35.
\]

**第六步：判断终止**

若还没达到最大题数：

\[
d_t=0.
\]

**第七步：存入 replay buffer**

\[
\left(
s_t,q_4,-0.35,s_{t+1},0
\right).
\]

至此只产生了一条训练经验。下一步要把这条经验转换成 Q 网络的监督目标。

### 4.2 TD target：给当前 Q 预测制作一个学习目标

我们不知道真实的 \(Q^*(s_t,q_t)\)，所以无法像普通监督学习那样直接拿到标签。TD learning 使用 Bellman 方程制作一个临时目标：

\[
y_t
=
r_t
+
\gamma(1-d_t)
\max_{q'\in\mathcal A_{t+1}}
Q_{\bar\phi}(s_{t+1},q').
\tag{9}
\]

这个 \(y_t\) 叫 temporal-difference target，简称 TD target。

**式 (9) 逐项解释**

| 项 | 含义 |
|---|---|
| \(y_t\) | 希望当前 Q 预测接近的目标值 |
| \(r_t\) | 已经真实观察到的即时 reward |
| \(Q_{\bar\phi}\) | 用于制作目标的 target network |
| \(\bar\phi\) | target network 的参数 |
| \(\max_{q'}\) | 下一状态所有合法动作中的最高预计价值 |
| \(1-d_t\) | 终止开关 |

**为什么叫 bootstrap**

目标 \(y_t\) 的一部分来自真实观察到的 \(r_t\)，另一部分来自模型自己对下一状态的估计：

\[
\underbrace{r_t}_{\text{真实观察}}
+
\underbrace{
\gamma\max_{q'}Q_{\bar\phi}(s_{t+1},q')
}_{\text{用已有估计推下一步}}.
\]

这种“用当前估计帮助构造新的学习目标”叫 bootstrap。

### 4.3 done 为什么要进入 TD target

若本步后测验继续：

\[
d_t=0,
\]

所以

\[
1-d_t=1,
\]

目标包含下一状态价值。

若本步已经是最后一题：

\[
d_t=1,
\]

所以

\[
1-d_t=0.
\]

此时

\[
y_t=r_t.
\tag{10}
\]

终止之后没有下一题，继续加入下一状态 Q 值会凭空创造不存在的未来 reward。

### 4.4 一次 TD 更新完整算一遍

继续使用刚才选择 \(q_4\) 的例子。

**已知量**

当前网络对所选动作的预测是

\[
Q_\phi(s_t,q_4)=-0.28.
\]

真实即时 reward 是

\[
r_t=-0.35.
\]

设

\[
\gamma=0.8,
\qquad
d_t=0.
\]

在新状态 \(s_{t+1}\) 中，\(q_4\) 也已经作答。假设 target network 对下一状态输出：

\[
Q_{\bar\phi}(s_{t+1},\cdot)
=
[-0.50,-0.40,-0.26,-0.33,-0.61].
\]

下一状态只剩 \(q_1,q_3\) 合法，因此 mask 后为

\[
[-0.50,-\infty,-0.26,-\infty,-\infty].
\]

合法题中的最大值是

\[
\max_{q'\in\mathcal A_{t+1}}
Q_{\bar\phi}(s_{t+1},q')
=
-0.26.
\]

**计算 TD target**

\[
\begin{aligned}
y_t
&=
r_t+\gamma(1-d_t)(-0.26)\\
&=
-0.35+0.8(1)(-0.26)\\
&=
-0.35-0.208\\
&=
-0.558.
\end{aligned}
\]

**计算 TD error**

定义

\[
\delta_t
=
y_t-Q_\phi(s_t,q_t).
\]

代入数值：

\[
\delta_t
=
-0.558-(-0.28)
=
-0.278.
\]

**计算平方损失**

\[
\mathcal L_t^{\mathrm{TD}}
=
\left(
y_t-Q_\phi(s_t,q_t)
\right)^2
=
(-0.278)^2
=
0.077284.
\tag{11}
\]

当前预测 \(-0.28\) 高于目标 \(-0.558\)，所以梯度更新会把该状态下 \(q_4\) 的预测向更负的方向调整。

**若本步已经终止**

若

\[
d_t=1,
\]

则

\[
y_t=-0.35.
\]

此时损失为

\[
\left(
-0.35-(-0.28)
\right)^2
=
0.0049.
\]

终止与非终止 transition 的目标不同，代码必须逐样本处理 `done`。

### 4.5 为什么只训练本次真正选择的题

网络一次输出五个 Q 值：

\[
Q_\phi(s_t,\cdot)
=
[-0.62,-0.31,-0.44,-0.28,-0.57].
\]

本次真正选择的是 \(q_4\)。环境只观察到了“选择 \(q_4\) 后发生什么”，所以本条 transition 直接监督：

\[
Q_\phi(s_t,q_4).
\]

其余四题在这个状态下的反事实结果没有发生，不能用同一个 \(y_t\) 监督。

PyTorch 使用 `gather` 取出每个样本实际动作对应的值：

```python
all_q = online_net(state)                         # [B, J]
q_taken = all_q.gather(1, action[:, None])       # [B, 1]
q_taken = q_taken.squeeze(1)                     # [B]
```

其中：

- \(B\) 是 batch size；
- \(J\) 是题库大小；
- `action[b]` 是第 \(b\) 条 transition 真实选择的题号。

### 4.6 target network 为什么能让训练更稳

如果同一网络同时承担两件事：

1. 产生当前预测 \(Q_\phi(s_t,q_t)\)；
2. 产生学习目标中的下一状态价值；

那么参数每更新一次，预测和目标会同时移动。模型像在追一个不断快速移动的目标。

DQN 复制一份更新较慢的网络：

| 网络 | 参数 | 用途 |
|---|---|---|
| online network | \(\phi\) | 产生当前 Q 预测，接受梯度更新 |
| target network | \(\bar\phi\) | 计算 TD target，暂时固定 |

**硬同步**

每隔 \(C\) 次更新：

\[
\bar\phi\leftarrow\phi.
\]

例如每 500 个 gradient steps 复制一次。

**软同步**

每一步做小幅移动：

\[
\bar\phi
\leftarrow
\tau\phi+(1-\tau)\bar\phi,
\]

其中 \(\tau\) 常取很小的数，例如 0.005。

target network 的输出在计算 \(y_t\) 时应停止梯度：

```python
with torch.no_grad():
    next_q = target_net(next_state)
```

官方 NCAT 仓库快照没有独立 target network。复刻仓库时应如实保留；构建较稳定的现代版本时建议加入并做消融。

## 5. 经验回放怎样组织训练数据

### 5.1 经验回放存的是什么

replay buffer 记为

\[
\mathcal B
=
\left\{
(s_t,q_t,r_t,s_{t+1},d_t)
\right\}.
\tag{12}
\]

它可以理解成一个有限容量的“交互记忆库”。

训练一个学生时可能依次产生：

```text
transition 1: 空状态 → 选择 q2 → 答对
transition 2: 已知 q2 答对 → 选择 q5 → 答错
transition 3: 已知 q2 对、q5 错 → 选择 q4 → 答对
transition 4: 再加入 q4 对 → 选择 q1 → 答错并终止
```

训练下一个学生时继续向同一个 buffer 添加 transition。容量满后，最旧经验被移除。

一个最小实现：

```python
from collections import deque
import random


class ReplayBuffer:
    def __init__(self, capacity):
        self.data = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        transition = (
            state,
            action,
            reward,
            next_state,
            done,
        )
        self.data.append(transition)

    def sample(self, batch_size):
        return random.sample(self.data, batch_size)

    def __len__(self):
        return len(self.data)
```

### 5.2 为什么不按产生顺序直接训练

连续 transition 高度相关。

例如同一个学生的相邻状态：

\[
s_{t+1}
=
s_t\cup\{(q_t,a_t)\}.
\]

它们只相差一条作答；相邻 reward 又都在同一个 query 集上计算。若网络连续只看这一名学生的这一条轨迹，gradient 会过度受最近局部数据影响。

经验回放随机抽样：

\[
(s,q,r,s',d)\sim\mathcal B.
\]

一个 mini-batch 可以同时包含：

- 不同学生；
- 不同测试步；
- 不同答对/答错组合；
- 不同动作；
- 终止与非终止 transition。

经验回放带来三项直接作用：

1. **打散相关性**：相邻轨迹不再按原顺序连续进入网络；
2. **提高数据利用率**：一条昂贵的环境交互可以被抽到多次；
3. **平滑更新**：一个 batch 的梯度来自多种状态，而非一条局部路径。

!!! info "replay buffer 不会创造新答案"

    它只重用已经发生的 transition。旧日志没有覆盖的状态—动作组合不会因为经验回放自动出现，离线支持域限制仍然存在。

### 5.3 一个 mini-batch 怎样更新

假设从 buffer 随机抽出 \(B\) 条 transition：

\[
\left\{
(s_b,q_b,r_b,s'_b,d_b)
\right\}_{b=1}^{B}.
\]

对每条样本分别计算：

\[
y_b
=
r_b
+
\gamma(1-d_b)
\max_{q'\in\mathcal A'_b}
Q_{\bar\phi}(s'_b,q').
\tag{13}
\]

batch 平均 TD loss：

\[
\mathcal L_{\mathrm{TD}}(\phi)
=
\frac1B
\sum_{b=1}^{B}
\left[
y_b-Q_\phi(s_b,q_b)
\right]^2.
\tag{14}
\]

完整代码骨架：

```python
all_q = online_net(state)                          # [B, J]
q_taken = all_q.gather(1, action[:, None]).squeeze(1)

with torch.no_grad():
    next_q = target_net(next_state)                # [B, J]
    next_q = next_q.masked_fill(
        ~next_valid_mask,
        float("-inf"),
    )
    next_best = next_q.max(dim=1).values           # [B]
    next_best = torch.where(
        done,
        torch.zeros_like(next_best),
        next_best,
    )
    target = reward + gamma * next_best

loss = torch.nn.functional.mse_loss(
    q_taken,
    target,
)

optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(
    online_net.parameters(),
    max_norm=5.0,
)
optimizer.step()
```

注意：

- `target` 的 shape 是 `[B]`；
- `q_taken` 的 shape 也应是 `[B]`；
- `next_valid_mask` 属于 \(s_{t+1}\)，不是 \(s_t\)；
- `done=True` 的样本把 `next_best` 设为 0。

## 6. 合法动作 mask：当前选择与未来估值都要合法

设状态 \(s\) 下的合法动作集合为 \(\mathcal A(s)\)。屏蔽后的 Q 值定义为

\[
\widetilde Q_\phi(s,q)
=
\begin{cases}
Q_\phi(s,q), & q\in\mathcal A(s),\\
-\infty, & q\notin\mathcal A(s).
\end{cases}
\tag{15}
\]

取最大值时，\(-\infty\) 永远不会胜出。

**第一次：选择当前动作**

在 \(s_t\) 中，已经回答 \(q_2,q_5\)：

\[
\mathcal A_t=\{q_1,q_3,q_4\}.
\]

当前行为策略只能从这三题选择。

**第二次：计算 TD target**

若本步又选择了 \(q_4\)，下一状态合法集合变成

\[
\mathcal A_{t+1}=\{q_1,q_3\}.
\]

因此 bootstrap 的最大值也只能在 \(q_1,q_3\) 中计算。

**mask 可以同时表达哪些约束**

在离线训练中，非法题通常包括：

- 该学生已经回答的题；
- 该学生 support 外、没有可查询历史答案的题；
- padding 题号。

正式部署中还可以屏蔽：

- 超出内容类别上限的题；
- 与已选题构成敌题的题；
- 已达到曝光配额的题；
- 时间预算内无法完成的题；
- 不符合题型、语言或可访问性要求的题。

一个通用函数：

```python
def apply_action_mask(q_values, valid_mask):
    if q_values.shape != valid_mask.shape:
        raise ValueError("Q values and mask must have the same shape")

    if not valid_mask.any(dim=1).all():
        raise ValueError("Every active state needs a legal action")

    return q_values.masked_fill(
        ~valid_mask,
        float("-inf"),
    )
```

!!! warning "下一状态 mask 是高风险实现点"

    行为选题时做了 mask，并不代表 TD target 自动正确。若下一状态最大值来自已答题或 support 外题，target 会建立在一个实际无法执行的未来动作上。官方仓库快照的 TD target 只屏蔽题号 0，因此复现和改进版本需要明确记录这一差异。

## 7. 探索、利用与施测随机化

### 7.1 epsilon-greedy：训练时怎样主动探索

训练开始时，Q 网络参数随机，最高 Q 值通常没有真实意义。若每一步都选择当前 argmax，模型会反复走少数早期偶然偏高的路径，很难收集其他动作的结果。

epsilon-greedy 定义为

\[
q_t
=
\begin{cases}
\text{从 }\mathcal A_t\text{ 均匀随机选题},
& \text{概率 }\varepsilon,\\
\displaystyle
\arg\max_{q\in\mathcal A_t}
Q_\phi(s_t,q),
& \text{概率 }1-\varepsilon.
\end{cases}
\tag{16}
\]

**三道合法题的概率例子**

假设：

\[
|\mathcal A_t|=3,
\qquad
\varepsilon=0.30.
\]

有 30% 的概率进入随机分支。随机分支中三题各占三分之一，所以每题从随机分支获得

\[
\frac{0.30}{3}=0.10.
\]

当前 greedy 题还会获得 70% 的确定性分支。因此：

| 题目类型 | 被选概率 |
|---|---:|
| 当前最大 Q 值题 | \(0.70+0.10=0.80\) |
| 其他合法题 1 | 0.10 |
| 其他合法题 2 | 0.10 |

**epsilon 怎样调度**

常见做法：

```text
训练早期：epsilon 接近 1，广泛探索
训练中期：epsilon 逐渐降低
训练后期：epsilon 接近 0，主要利用已学策略
```

论文报告 \(\varepsilon\) 从 1 衰减到 0。公开代码采用随训练计数变化的另一条随机动作概率曲线。

无论走随机分支还是 greedy 分支，都必须先应用合法动作 mask。随机探索只是在合法候选题之间随机。

### 7.2 温度采样：评价或部署时怎样分散路径

NCAT 论文在测试阶段把合法题 Q 值转成概率：

\[
\Pr(q\mid s_t)
=
\frac{
\exp
\left(
Q_\phi(s_t,q)/\nu_t
\right)
}{
\displaystyle
\sum_{q'\in\mathcal A_t}
\exp
\left(
Q_\phi(s_t,q')/\nu_t
\right)
}.
\tag{17}
\]

\(\nu_t>0\) 是 temperature。

为了计算稳定，可以先减去合法题中的最大 Q 值。假设三道合法题的 Q 值为

\[
[-0.62,-0.44,-0.28].
\]

减去最大值 \(-0.28\)：

\[
[-0.34,-0.16,0].
\]

**温度等于 1**

\[
\exp([-0.34,-0.16,0])
\approx
[0.712,0.852,1].
\]

归一化后约为

\[
[0.278,0.332,0.390].
\]

三道题都有明显概率，路径较分散。

**温度等于 0.2**

\[
\exp([-0.34,-0.16,0]/0.2)
\approx
[0.183,0.449,1].
\]

归一化后约为

\[
[0.112,0.275,0.613].
\]

最高 Q 值题已经占主要概率。

**温度等于 0.05**

归一化概率约为

\[
[0.001,0.039,0.960].
\]

选择几乎退化为 argmax。

**论文的温度调度**

论文设置

\[
\nu_t=2^{-0.1t}.
\tag{18}
\]

几个测试步的温度为：

| 测试步 | 温度 |
|---:|---:|
| \(t=1\) | 约 0.933 |
| \(t=10\) | 0.5 |
| \(t=20\) | 0.25 |

测试早期路径更分散，后期更集中于高 Q 值题。

温度采样可以降低平均曝光，但最大曝光率、内容蓝图和题目安全仍需硬约束机制。

### 7.3 epsilon 和温度采样的区别

两者都会产生随机动作，但概率结构和使用阶段不同。

| 对比 | epsilon-greedy | temperature softmax |
|---|---|---|
| 主要阶段 | Q 网络训练 | 论文的评价/部署选题 |
| 随机部分 | 在合法题中均匀随机 | 仍偏向 Q 值较高的题 |
| 核心参数 | \(\varepsilon\) | \(\nu_t\) |
| 参数变小 | 减少随机分支 | 概率更集中于 argmax |
| 主要目的 | 探索状态—动作空间 | 分散测验路径和题目曝光 |

例如 Q 值排名第二的题与最高题非常接近时：

- epsilon 随机分支不关心二者接近程度；
- temperature softmax 会给排名第二的题较高概率。

### 7.4 gamma、epsilon 和 temperature 一次分清

| 参数 | 它回答的问题 | 它改变哪里 | 是否改变 TD target |
|---|---|---|---|
| \(\gamma\) | 多重视未来 reward？ | Bellman target | 是 |
| \(\varepsilon\) | 训练时多大概率随机探索？ | 训练行为策略 | 不直接改变公式 |
| \(\nu_t\) | Q 值转成多尖锐的选题概率？ | 评价/部署动作分布 | 不直接改变公式 |

可以用三句话记忆：

- \(\gamma\) 管“未来值多少钱”；
- \(\varepsilon\) 管“训练时试多少没走过的路”；
- \(\nu_t\) 管“施测时选题概率有多集中”。

## 8. 把所有步骤放回 NCAT

### 8.1 一名学生的一整条训练轨迹

把前面所有部分连起来，一名历史学生的 episode 如下。

```text
初始化空状态 s1
初始化合法 support 候选集 A1
重置该学生的局部参数

第 1 步：
    Q 网络读取 s1
    epsilon-greedy 从 A1 选择 q1
    环境读取 q1 的历史答案
    形成 s2
    响应模型用已选题更新学生参数
    在 query 集计算 loss，得到 r1
    存储 (s1, q1, r1, s2, done1)

第 2 步：
    Q 网络读取 s2
    合法集合删除 q1
    选择 q2
    读取真实答案并形成 s3
    更新学生参数与 query reward
    存储 (s2, q2, r2, s3, done2)

继续到停止：
    最后一条 transition 的 done = True

若 replay buffer 样本足够：
    随机抽 mini-batch
    计算 masked TD target
    更新 online Q 网络
    按计划同步 target network
```

注意，策略每一步读取的状态都已经包含学生上一题的真实反馈。因此两名学生即使前两题相同，只要某一步答案不同，后续 Q 向量和题目路径就可能分叉。

### 8.2 训练和真实施测在哪一步分开

**离线训练**

离线环境能访问历史日志和 held-out query 答案，因此可以：

- 查询被选 support 题的历史反应；
- 计算 query BCE；
- 构造 reward；
- 保存 transition；
- 更新 Q 网络。

**真实施测**

新学生部署时：

- 下一题答案来自学生实时提交；
- 系统更新状态和学生参数；
- Q 网络重新选择下一题；
- 没有隐藏 query 真值；
- 不计算训练 reward；
- 不需要 replay buffer 或 TD 更新。

训练得到的 \(Q_\phi\) 已经把历史数据中的选题规律编码进参数。部署阶段只执行策略。

## 9. 更稳定的 DQN 版本

### 9.1 Double DQN 在改什么

普通 DQN 的下一状态最大值为

\[
\max_{q'}
Q_{\bar\phi}(s_{t+1},q').
\]

同一组有噪声的数值既参与“挑最大者”，又参与“评价最大者”，容易产生 max bias。

Double DQN 把两项任务分开。

**online network 负责选题号**

\[
q^{\mathrm{select}}
=
\arg\max_{q'\in\mathcal A_{t+1}}
Q_\phi(s_{t+1},q').
\tag{19}
\]

**target network 负责评价该题**

\[
y_t
=
r_t
+
\gamma(1-d_t)
Q_{\bar\phi}
\left(
s_{t+1},
q^{\mathrm{select}}
\right).
\tag{20}
\]

动作 mask 必须在式 (19) 的 argmax 前应用。Double DQN 主要改善 Q-learning 的估值偏差与稳定性，不改变 NCAT 的状态表示、query reward 或逐题反馈结构。

### 9.2 一个较稳妥的 NCAT-DQN 训练配置

建议把以下部件分别实现并单元测试：

1. **online Q network**：读取答对/答错状态并接受梯度；
2. **target Q network**：慢速同步，制作 TD target；
3. **response model**：用累计已选题更新学生参数；
4. **offline environment**：读取历史答案并计算 query reward；
5. **replay buffer**：保存 transition 并随机抽 batch；
6. **current valid mask**：控制本步行为动作；
7. **next valid mask**：控制 bootstrap 最大值；
8. **epsilon schedule**：训练探索；
9. **temperature schedule**：评价或部署随机化；
10. **gradient clipping**：限制异常 TD error 造成的梯度爆炸；
11. **checkpoint**：同时保存网络、target、optimizer 和训练计数。

## 10. 实现检查与最终总结

### 10.1 最常见的实现错误

**错误一：把 Q 值当成答对概率**

检查：Q 网络是否被强制经过 sigmoid。标准 DQN 输出通常不需要 sigmoid；Q 值可以是任意实数。

**错误二：reward 符号写反**

NCAT 原定义为

\[
r_t=-L_t.
\]

若直接使用正 BCE，最大化 reward 会偏向更大的预测损失。

**错误三：query 题进入学生参数更新**

query 只能用于外层评价。若 query 答案参与 \(\widehat\theta_i^{\,t}\) 的估计，reward 会发生信息泄漏。

**错误四：当前动作做 mask，下一状态最大值没做**

这会让 TD target 依赖已答题或无历史答案的题。

**错误五：终止样本仍然 bootstrap**

对 `done=True`：

\[
y_t=r_t.
\]

**错误六：target 没有停止梯度**

制作 target 的分支应放在 `torch.no_grad()` 中。

**错误七：训练状态提前包含本题答案**

选择 \(q_t\) 时输入必须是 \(s_t\)，答案只能出现在 \(s_{t+1}\)。

**错误八：`gather` 取错题号**

应检查每个 batch 样本的 `action` 与 `q_taken` 一一对应，并统一题号是否从 0 或 1 开始。

**错误九：合法集合为空**

若硬约束把所有题都屏蔽，`argmax` 将没有意义。部署系统需要预先检测约束可行性并设计 fallback。

### 10.2 读完这一页后的完整心智模型

Q-learning 在 NCAT 中做了四层连接：

1. **一次真实作答**把 \(s_t\) 变成 \(s_{t+1}\)；
2. **响应模型与 query 集**把新状态变成 reward \(r_t\)；
3. **Bellman target**把即时 reward 和下一状态价值合成 \(y_t\)；
4. **TD loss 与 replay**让 Q 网络逐渐学会长期选题价值。

最核心的更新可以浓缩为：

\[
\boxed{
\text{当前预测}
\quad
Q_\phi(s_t,q_t)
\quad
\longleftarrow
\quad
\underbrace{r_t}_{\text{当前测量结果}}
+
\underbrace{
\gamma(1-d_t)
\max_{q'\in\mathcal A_{t+1}}
Q_{\bar\phi}(s_{t+1},q')
}_{\text{未来选题价值}}
}
\]

而 \(s_{t+1}\) 中包含学生刚刚提交的答案，所以这个更新始终建立在逐题实时反馈闭环上。

下一页进入 Q 网络内部，解释它怎样把答对题和答错题编码成状态向量：[状态编码与双通道 attention](04-neural-encoder.md)。
