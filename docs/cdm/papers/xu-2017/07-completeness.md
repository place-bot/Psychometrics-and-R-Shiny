# 完整 Q 矩阵与理想反应

## 先看无噪声 DINA

在理想情形中

\[
R_j=\xi_{j,\boldsymbol\alpha},
\qquad
\xi_{j,\boldsymbol\alpha}
=
\mathbb I(\boldsymbol\alpha\succeq\boldsymbol q_j),
\]

项目参数已知，未知量只剩属性分布 \(\boldsymbol p\)。

若两个属性模式的理想反应向量相同：

\[
\left(
\xi_{j,\boldsymbol\alpha}:j=1,\ldots,J
\right)
=
\left(
\xi_{j,\boldsymbol\alpha'}:j=1,\ldots,J
\right),
\]

它们在 \(T\)-矩阵中对应相同列。数据只能识别

\[
p_{\boldsymbol\alpha}
+
p_{\boldsymbol\alpha'},
\]

无法分别识别两项比例。

## 完整性的定义

Q 矩阵称为 complete，如果每个属性都有一道只要求该属性的题。等价地，Q 的若干行经排序后构成

\[
I_K.
\]

即

\[
\{\boldsymbol e_1^\top,\ldots,\boldsymbol e_K^\top\}
\subseteq
\{\boldsymbol q_1,\ldots,\boldsymbol q_J\}.
\]

## 为什么一个单位阵能区分理想模式

在单位块中，第 \(k\) 道题的理想反应为

\[
\xi_{k,\boldsymbol\alpha}
=
\mathbb I(\alpha_k=1)
=
\alpha_k.
\]

这 \(K\) 道题的理想反应向量就是

\[
(\alpha_1,\ldots,\alpha_K)^\top
=
\boldsymbol\alpha.
\]

不同属性模式自然有不同向量。因此，在项目参数已知的理想 DINA 中，完整性足以区分全部潜在类。

## 不完整例子

论文给出

\[
Q=
\begin{pmatrix}
1&1\\
0&1
\end{pmatrix}.
\]

对

\[
\boldsymbol\alpha=(1,0)^\top
\quad\text{与}\quad
\boldsymbol\alpha'=(0,0)^\top,
\]

第一题都缺属性 2，第二题都缺属性 2，因此理想反应均为

\[
(0,0)^\top.
\]

于是两列不可区分，\(\boldsymbol p\) 不可识别。

## 已知项目参数与未知项目参数

| 情形 | 一个 \(I_K\) 的作用 |
| --- | --- |
| 理想 DINA、\(\Theta\) 已知 | 区分全部属性模式，识别 \(\boldsymbol p\) |
| 有噪声、\(\Theta\) 未知 | 还要同时拆开题目概率与类比例，完整性不充分 |

论文引用既有 DINA 结果指出：当 guessing、slipping 与 \(\boldsymbol p\) 全部未知时，每个属性至少要被三道题要求才可能识别全部参数。

## 从完整性到 C1

Xu 对一般 RLCM 采用两个单位块：

\[
\begin{pmatrix}
I_K\\
I_K
\end{pmatrix}.
\]

两个块使证明可以用一套题构造选择性非零行，同时借另一套题补足对称位置。不过两个块只让每个属性出现两次；命题 2 表明这仍可能留下连续等价参数族，因此还需要 C2。

## 完整性是结构条件

检查 Q 是否 complete 只需检查每个单位向量是否出现。它与样本量、估计算法和拟合优度无关。若 Q 不完整，增加相同结构的被试数据不会产生缺失的区分信息。
