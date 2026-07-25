# 三路数组、triad 与秩

## 三路数组

设

\[
\mathcal X=(x_{ijk})
\in\mathbb F^{I\times J\times K},
\]

其中：

- \(i=1,\ldots,I\) 是第一个方向；
- \(j=1,\ldots,J\) 是第二个方向；
- \(k=1,\ldots,K\) 是第三个方向；
- \(\mathbb F\) 在原文主要取实数域，现代版本也讨论更一般的域。

可把 \(\mathcal X\) 想成 \(K\) 张 \(I\times J\) 矩阵叠在一起，也可以沿另外两个方向切片。

## triad：三路秩一数组

给定

\[
\boldsymbol a\in\mathbb F^I,\qquad
\boldsymbol b\in\mathbb F^J,\qquad
\boldsymbol c\in\mathbb F^K,
\]

它们的外积

\[
\boldsymbol a\otimes\boldsymbol b\otimes\boldsymbol c
\]

在位置 \((i,j,k)\) 的元素为

\[
x_{ijk}=a_i b_j c_k.
\]

Kruskal 把这种乘法形式称为 **triad**。现代文献常称它为 rank-one tensor。

## 三路数组的秩

\[
\operatorname{rank}(\mathcal X)
=
\min\left\{
R:
\mathcal X
=\sum_{r=1}^{R}
\boldsymbol a_r\otimes
\boldsymbol b_r\otimes
\boldsymbol c_r
\right\}.
\]

这里的 \(R\) 是秩一三路数组的最少数量。它与把数组展开成矩阵以后计算的普通矩阵秩属于不同对象。

### 为什么“展开矩阵的秩”只能给下界

把 \(\mathcal X\) 沿第一个方向展开为

\[
X_{(1)}\in\mathbb F^{I\times JK}.
\]

每个 triad 展开后仍是秩一矩阵，所以任何 \(R\) 项分解都满足

\[
\operatorname{rank}(X_{(1)})\le R.
\]

同理，

\[
\max\left\{
\operatorname{rank}(X_{(1)}),
\operatorname{rank}(X_{(2)}),
\operatorname{rank}(X_{(3)})
\right\}
\le
\operatorname{rank}(\mathcal X).
\]

展开会丢失一部分三路结构，因而这个下界可能不紧。

## slab 与 slab-space

固定一个指标就得到二维矩阵。例如固定 \(i\)：

\[
X_{i::}
=
(x_{ijk})_{j,k}
\in\mathbb F^{J\times K}.
\]

原文把这种二维切片称为 slab。所有第 1 方向 slabs 张成的矩阵空间维数记作

\[
\dim_1(\mathcal X)
=
\dim\operatorname{span}\{
X_{1::},\ldots,X_{I::}
\}.
\]

类似地可定义 \(\dim_2(\mathcal X)\) 和 \(\dim_3(\mathcal X)\)。

在现代展开记号下，

\[
\dim_1(\mathcal X)
=\operatorname{rank}(X_{(1)}),
\]

具体取决于展开时把 slabs 排成行还是列。原文强调：

\[
\dim_\ell(\mathcal X)
\quad\text{与}\quad
\operatorname{rank}(\mathcal X)
\]

通常没有矩阵情形中“行秩等于列秩等于秩”的简单等式。

## 模式方向上的线性变换

设 \(U\) 作用于第一个方向，\(W\) 作用于第三个方向。可写成

\[
U*_{1}\mathcal X,
\qquad
W*_{3}\mathcal X.
\]

若

\[
\mathcal X=[A,B,C],
\]

则

\[
U*_{1}\mathcal X=[UA,B,C],
\qquad
W*_{3}\mathcal X=[A,B,WC].
\]

这使“先对某个方向压缩或投影，再考察剩余秩”成为可能。

## 原文 Theorem 1 的秩下界思想

原文给出若干张量秩下界。摘要列出的一个特例可写为

\[
\operatorname{rank}(\mathcal X)
\ge
\dim_1(U*_{1}\mathcal X)
+
\operatorname{rank}(W*_{3}\mathcal X)
-
\dim_1\!\left(U*_{1}W*_{3}\mathcal X\right).
\tag{1}
\]

公式中：

- 第一项看 \(U\) 变换后，第 1 方向还留下多少独立 slabs；
- 第二项看 \(W\) 变换后的三路秩；
- 第三项扣除同时经过两种变换后被重复计算的部分。

它具有类似“两个信息来源相加，再减交叠”的结构，并推广了 Frobenius 的一个矩阵秩不等式。

!!! note "与 CDM 主线的关系"
    CDM 可识别性最常使用论文后半部分的分解唯一性定理。秩下界仍然重要，因为唯一性首先要求写下的 \(R\) 项确实构成一个最短分解；现代 Kruskal 定理通常把“张量秩等于 \(R\)”和“该分解本质唯一”一起陈述。
