# 严格可识别性的定义

## 定义 1

论文把 \((\Theta,\boldsymbol p)\) 的可识别性定义为：

\[
\begin{aligned}
&P(\boldsymbol R=\boldsymbol r
\mid Q,\Theta,\boldsymbol p)
=
P(\boldsymbol R=\boldsymbol r
\mid Q,\bar\Theta,\bar{\boldsymbol p})
\quad
\forall\boldsymbol r\in\{0,1\}^J\\
&\hspace{3em}\Longleftrightarrow
(\Theta,\boldsymbol p)
=
(\bar\Theta,\bar{\boldsymbol p}).
\end{aligned}
\tag{3.2}
\]

左侧表示两组参数生成完全相同的观测反应分布，右侧要求两组参数逐项相同。

## 为什么没有 label swapping

普通 latent class model 的潜在类只有编号。交换两类的参数列和混合比例，不改变观测分布，因此最多识别到标签置换。

这里的列标签具有预先规定的含义：

\[
(0,0),\ (1,0),\ (0,1),\ (1,1)
\]

分别代表具体的属性掌握状态，Q 矩阵也按这些属性定义限制。因此论文要求固定语义标签下的严格相等。

## strict 与 generic

| 概念 | 量词 | 允许的失败集合 |
| --- | --- | --- |
| strict identifiability | 对参数空间中每个允许参数点成立 | 不允许 |
| generic identifiability | 除去测度为零的集合后成立 | 允许异常参数点 |
| local identifiability | 某参数点附近没有另一个等价点 | 远处仍可能有等价点 |

Xu 的主定理给出 strict identifiability。C1、C2 是确保这个强结论的充分条件。

## 可识别性与估计表现

可识别性是总体分布层面的性质。它假设我们知道精确的

\[
\left\{
P(\boldsymbol R=\boldsymbol r):
\boldsymbol r\in\{0,1\}^J
\right\}.
\]

因此：

- 可识别说明无限信息下参数唯一；
- 有限样本估计仍可能方差很大；
- 条件接近失效时，似然面可能非常平；
- 优化算法收敛不等于理论可识别；
- 理论可识别也不保证某次优化到达全局最优。

## 与可估计性的联系

若模型不可识别，则不同参数点对应同一分布，任何基于响应数据的估计方法都无法一致选中其中一个真值。

若模型严格可识别，并且满足常规正则性、参数空间和似然条件，最大似然估计才有建立一致性的基础。论文在主定理后给出了这条大样本连接，详见[从可识别性到一致性](15-consistency.md)。

## 与 CAT 的联系

CAT 中每名学生只回答自适应选择的一部分题。Xu 的定义基于固定 \(Q\) 下完整 \(J\) 维反应分布，并未直接处理自适应缺失机制。

因此该定理可以指导题库和反应模型的基础设计，但不能直接推出：

- 任意 adaptive policy 下参数仍可识别；
- 每个学生的属性模式都能准确恢复；
- 测试长度足够短；
- 动态题目曝光后仍有足够覆盖。

将此理论用于 CAT，还需要研究选题策略产生的数据支持集及其可忽略性或探索条件。
