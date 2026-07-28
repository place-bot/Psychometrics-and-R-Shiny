# 从 Bellman 方程到 DQN

## 1. 为什么需要函数逼近

状态空间是连续集合：

\[
\mathcal S=[0,1]^D.
\]

任意两个能力值都可能不同，无法建立有限 Q 表。论文用神经网络近似：

\[
Q^*(s,a)
\approx
\widehat Q(s,a;\mathbf w),
\tag{1}
\]

其中 \(\mathbf w\) 汇总全部网络权重和偏置。

## 2. DQN 的输入输出

输入层接收 \(D\) 维能力：

\[
s\in\mathbb R^D.
\]

输出层有 \(L\) 个单元：

\[
\widehat{\mathbf Q}(s;\mathbf w)
=
\begin{bmatrix}
\widehat Q(s,1;\mathbf w)\\
\vdots\\
\widehat Q(s,L;\mathbf w)
\end{bmatrix}.
\tag{2}
\]

一次前向传播就得到所有材料的长期价值。

## 3. 论文的神经网络基础表达

以一个隐藏层为例：

\[
\mathbf h
=
\phi(\mathbf W_{hx}\mathbf x+\mathbf b_h),
\tag{3}
\]

\[
\mathbf y
=
\mathbf W_{yh}\mathbf h+\mathbf b_y.
\tag{4}
\]

论文使用 ReLU 作为典型激活函数：

\[
\phi(z)=\max(z,0).
\]

用于 DQN 时，\(\mathbf x=s\)，\(\mathbf y=\widehat{\mathbf Q}(s;\mathbf w)\)。

## 4. 理想监督目标为何不可直接获得

若真实 \(Q^*(s,a)\) 已知，可以最小化：

\[
\min_{\mathbf w}
\mathbb E
\left[
\left(
\widehat Q(S,A;\mathbf w)-Q^*(S,A)
\right)^2
\right].
\tag{5}
\]

实际中 \(Q^*\) 未知，状态分布也受策略和转移影响。Q-learning 用 Bellman 一步展开构造可计算目标。

## 5. Bellman target

对转移

\[
(s,a,r,s'),
\]

若 \(s'\) 尚未终止：

\[
y
=
r+\gamma
\max_{a'\in\mathcal A}
\widehat Q(s',a';\mathbf w).
\tag{6}
\]

若 \(s'\) 已达到目标：

\[
y=r=0.
\tag{7}
\]

合写为：

\[
y
=
\begin{cases}
r,
&
\|s'-\mathbf1_D\|_\infty<10^{-3},
\\
r+\gamma\max_{a'}\widehat Q(s',a';\mathbf w),
&
\text{其他情况}.
\end{cases}
\tag{8}
\]

## 6. TD 误差与损失

\[
\delta
=
y-\widehat Q(s,a;\mathbf w).
\tag{9}
\]

mini-batch \(\mathcal M\) 上的平方损失可写成：

\[
\mathcal L_Q(\mathbf w)
=
\frac{1}{|\mathcal M|}
\sum_{(s,a,r,s')\in\mathcal M}
\left[
\widehat Q(s,a;\mathbf w)-y
\right]^2.
\tag{10}
\]

梯度下降更新：

\[
\mathbf w
\leftarrow
\mathbf w
-\alpha\nabla_{\mathbf w}\mathcal L_Q(\mathbf w).
\tag{11}
\]

## 7. 数字例子

设：

\[
r=-1,\qquad
\gamma=0.9,
\qquad
\max_{a'}\widehat Q(s',a')=-4.0.
\]

则：

\[
y=-1+0.9(-4.0)=-4.6.
\]

若当前预测

\[
\widehat Q(s,a)=-3.8,
\]

则

\[
\delta=-4.6-(-3.8)=-0.8.
\]

该动作的预测过于乐观，更新会把其 Q 值向更负的方向推。

若 \(s'\) 为终止状态：

\[
y=0.
\]

此时不能再加下一状态价值，否则会在 episode 结束后继续计算虚构回报。

## 8. 论文算法中的同网 bootstrap

初稿式 (15)–(16) 使用同一组参数 \(\mathbf w^{(t)}\)：

\[
y
=
r+\gamma\max_{a'}
\widehat Q(s',a';\mathbf w^{(t)}).
\]

目标随正在更新的网络一起移动，可能导致估计震荡和过估计。

现代 DQN 常加入 target network：

\[
y
=
r+\gamma\max_{a'}
\widehat Q(s',a';\mathbf w^-),
\tag{12}
\]

并周期性执行：

\[
\mathbf w^-\leftarrow\mathbf w.
\]

这属于工程稳定化。复刻论文时应明确使用初稿算法还是现代版本。

## 9. Double DQN

Double DQN 用在线网络选动作、目标网络估值：

\[
a^*
=
\arg\max_{a'}
\widehat Q(s',a';\mathbf w),
\]

\[
y
=
r+\gamma
\widehat Q(s',a^*;\mathbf w^-).
\tag{13}
\]

它可缓解最大化运算导致的 Q 值过估计。

## 10. Q 值的教育含义

\[
\widehat Q(s,a)
\]

表示：

> 当前能力为 \(s\) 时先推荐材料 \(a\)，之后继续采用当前最优策略，预期能得到多少折扣累计奖励。

在论文奖励下，它与“预期还需多少轮到达目标”高度相关。它不等同于：

- 下一次能力增量；
- 学生完成材料的概率；
- 材料难度；
- 答题正确率；
- 题目信息量。

## 11. DQN 学到策略的条件

神经网络有表示能力并不保证策略可靠。还需要：

1. 训练数据覆盖关键状态—动作区域；
2. 每个动作有足够转移样本；
3. 奖励与终止规则正确；
4. 能力估计误差可控；
5. 训练分布与部署分布接近；
6. 外推动作受到安全约束。

下一页把这些对象放入完整训练循环。
