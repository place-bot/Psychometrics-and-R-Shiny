# 理想反应、B-vector 与 T-matrix

## 列：非零属性模式

第 2 节的 \(T(Q)\) 有

\[
2^k-1
\]

列。每列对应一个非零属性模式

\[
\boldsymbol A\in\{0,1\}^k\setminus\{\boldsymbol0\}.
\]

全零模式被暂时排除，因为无噪声且每道题至少要求一个属性时，全零模式对任何“答对”事件的概率贡献都为 0。

例如 \(k=2\) 时，列可以按

\[
(1,0),\ (0,1),\ (1,1)
\]

排列。

## 单题 B-vector

用 \(I_i\) 表示“第 \(i\) 题答对”这个事件。定义

\[
B_Q(I_i)
\]

为长度 \(2^k-1\) 的行向量。其属性模式 \(\boldsymbol A\) 对应的分量是

\[
\left\{B_Q(I_i)\right\}_{\boldsymbol A}
=
\prod_{j=1}^k(A^j)^{Q_{ij}}
=
\xi^i(\boldsymbol A).
\]

所以这一行在回答：

> 对每个属性模式，它是否具备答对第 \(i\) 题所需的全部属性？

## 题组 B-vector

\(I_{i_1}\wedge\cdots\wedge I_{i_\ell}\) 表示这些题全部答对。论文定义

\[
B_Q(I_{i_1}\wedge\cdots\wedge I_{i_\ell})
=
\mathop{\Upsilon}_{h=1}^{\ell}B_Q(I_{i_h}),
\tag{2.3}
\]

其中 \(\Upsilon\) 表示逐元素相乘。

若

\[
\boldsymbol W
=
\mathop{\Upsilon}_{h=1}^{\ell}\boldsymbol V_h,
\]

则第 \(a\) 个分量为

\[
W^a=\prod_{h=1}^{\ell}V_h^a.
\]

题组行在某个属性模式下取 1，当且仅当该模式能同时完成组内全部题。

## 行：非空题目子集

每一行对应一个非空题目子集：

\[
\{i_1,\ldots,i_\ell\}
\subseteq
\{1,\ldots,m\}.
\]

可能的行依次包括：

- 所有单题 \(I_1,\ldots,I_m\)；
- 所有题对 \(I_i\wedge I_j\)；
- 所有三题组合；
- 一直到全部 \(m\) 道题的组合。

若全部组合都纳入，行数为

\[
\sum_{\ell=1}^m {m\choose \ell}
=2^m-1.
\]

论文称这样的 \(T(Q)\) 为**饱和**。

## 一个具体 B-vector

取

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&1
\end{pmatrix},
\]

列顺序为 \(10,01,11\)。

第 1 题只要求属性 1：

\[
B_Q(I_1)=(1,0,1).
\]

第 2 题只要求属性 2：

\[
B_Q(I_2)=(0,1,1).
\]

第 3 题要求两个属性：

\[
B_Q(I_3)=(0,0,1).
\]

题对 \(I_1\wedge I_2\) 的行是

\[
(1,0,1)\odot(0,1,1)
=(0,0,1).
\]

这里 \(\odot\) 表示逐元素乘法。

## T-matrix 的含义

把选定的 B-vector 逐行堆叠：

\[
T(Q)=
\begin{pmatrix}
B_Q(I_1)\\
\vdots\\
B_Q(I_{i_1}\wedge\cdots\wedge I_{i_\ell})\\
\vdots
\end{pmatrix}.
\]

它是一个由 Q 决定的设计矩阵：

- 列枚举潜在属性模式；
- 行枚举可观测的联合答对事件；
- 元素说明某模式是否具备完成该题组的能力。

## T-matrix 为什么比逐题正确率更有信息

只看单题正确率时，两个候选 Q 可能通过调整属性分布得到相同边际概率。题对与高阶题组添加了潜在类别之间的联合限制。

例如第三题和“第一、二题同时答对”在上例的理想结构中拥有相同行：

\[
B_Q(I_3)=B_Q(I_1\wedge I_2).
\]

这类结构相等式会对观测联合概率施加额外约束，并在证明中帮助区分候选 Q。

[下一页：经验矩 \(\boldsymbol\alpha\) 与总体映射](04-alpha-and-moment-map.md)
