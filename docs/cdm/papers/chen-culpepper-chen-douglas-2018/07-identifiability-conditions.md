# Q 的三条可识别条件

## 条件一：两套单位阵

存在一个 \(J\times J\) 的题目行置换矩阵 \(P\)，使

\[
PQ=
\begin{bmatrix}
I_K\\
I_K\\
\widetilde Q
\end{bmatrix},
\]

其中 \(\widetilde Q\) 有 \(J-2K\) 行。

这表示每个属性 \(k\) 都至少有两道“纯题”：

\[
\boldsymbol q_j=\boldsymbol e_k.
\]

题目顺序没有限制；\(P\) 只是把这些单位行搬到矩阵顶部以便表达。

## 条件二：每个属性至少三题

\[
Q_k^{\mathsf T}\boldsymbol1_J\ge3,
\qquad k=1,\ldots,K.
\]

前两套单位阵已经让每列至少有两个 1，因此还要求

\[
\widetilde Q_k^{\mathsf T}\boldsymbol1_{J-2K}>0.
\]

也就是每个属性必须在剩余题目中至少再出现一次。

## 条件三：没有全零题目

\[
\boldsymbol q_j^{\mathsf T}\boldsymbol1_K>0,
\qquad j=1,\ldots,J.
\]

每道题至少要求一个属性。全零行会让

\[
\eta_{ij}=1
\]

对所有学生成立，使该题无法提供任何属性结构信息。

## 集合写法

论文把合法空间写为

\[
\mathcal Q
=
\left\{
Q:
Q_k^{\mathsf T}\boldsymbol1_J\ge3\ \forall k,\
\boldsymbol q_j^{\mathsf T}\boldsymbol1_K>0\ \forall j,\
(PQ)^{\mathsf T}
=
[I_K,I_K,\widetilde Q^{\mathsf T}]
\right\}.
\]

## 三条条件之间的关系

| 条件 | 控制对象 | 算法中的保护动作 |
| --- | --- | --- |
| 两套 \(I_K\) | 每个属性的纯题锚点 | 不允许删掉只剩两份的单位行 |
| 每列至少 3 个 1 | 属性覆盖 | 列和为 3 时，不允许把 1 翻成 0 |
| 每行至少 1 个 1 | 题目有效性 | 单位行中的唯一 1 不允许翻成 0 |

受限 Gibbs 中原文列出的三个“保持不动”位置正是这三类边界的局部表现。

## 一个合法例子

当 \(K=2,J=6\)：

\[
Q=
\begin{bmatrix}
1&0\\
0&1\\
1&0\\
0&1\\
1&1\\
1&1
\end{bmatrix}.
\]

两种单位行各出现两次，两列列和均为 4，每行非零，所以 \(Q\in\mathcal Q\)。

## 一个只差一格的非法例子

\[
Q'=
\begin{bmatrix}
1&0\\
0&1\\
1&0\\
0&1\\
0&1\\
0&1
\end{bmatrix}.
\]

第一列列和为 2，违反第二条。即使每行仍非零、两种单位行也都至少出现两次，模型仍被排除。

## 充分条件的历史位置

本文引用 Chen et al.（2015）的 DINA 可识别结果，并据此定义采样空间。后来的文献进一步研究更弱、必要且充分或一般可识别条件。阅读 2018 论文时，应按作者当时采用的这组充分条件理解算法。

[下一页：为什么把后验限制在可识别空间](08-identified-space.md)
