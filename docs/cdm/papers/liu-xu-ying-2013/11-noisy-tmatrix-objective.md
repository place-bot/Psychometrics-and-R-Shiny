# 噪声 T-matrix 与目标函数

## 三题示例的 \(T_{c,g}(Q)\)

继续使用

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&1
\end{pmatrix}
\]

以及非零属性列 \(10,01,11\)。

若行选择 \(I_1,I_2,I_3,I_1\wedge I_2\)，则

\[
T_{c,g}(Q)=
\begin{pmatrix}
c_1&g_1&c_1\\
g_2&c_2&c_2\\
g_3&g_3&c_3\\
c_1g_2&g_1c_2&c_1c_2
\end{pmatrix}.
\tag{3.6}
\]

逐行解释：

- 模式 \(10\) 能做第 1 题，不能做第 2、3 题；
- 模式 \(01\) 能做第 2 题，不能做第 1、3 题；
- 模式 \(11\) 能做全部三题；
- 题对行由前两行逐元素相乘。

## 全零模式的猜测列

对同样四个题组，全零属性模式的概率列为

\[
\boldsymbol g_{\mathrm{joint}}
=
\begin{pmatrix}
g_1\\
g_2\\
g_3\\
g_1g_2
\end{pmatrix}.
\]

饱和情形会继续包含所有题组的猜测概率乘积。

## 总体矩映射

把非零模式概率记为 \(\boldsymbol p\)，全零模式概率记为 \(p_0\)。则

\[
\boldsymbol\mu
=
T_{c,g}(Q)\boldsymbol p
+p_0\boldsymbol g_{\mathrm{joint}}.
\]

经验矩满足

\[
\boldsymbol\alpha
\overset{\text{a.s.}}{\longrightarrow}
\boldsymbol\mu.
\]

这里已没有逐样本精确等式。条件反应随机性会造成抽样残差，但大数定律保证经验联合比例收敛。

## 固定 \(c,g,Q\) 的剖面目标

论文定义

\[
S_{c,g}(Q)
=
\inf_{\boldsymbol p'}
\left\|
T_{c,g}(Q)\boldsymbol p'
+p_0'\boldsymbol g_{\mathrm{joint}}
-\boldsymbol\alpha
\right\|_2,
\tag{3.7}
\]

约束为

\[
p_{\boldsymbol A}'\in[0,1],
\qquad
\sum_{\boldsymbol A\in\{0,1\}^k}
p_{\boldsymbol A}'=1.
\]

把全零模式并入矩阵，可写成更紧凑的形式：

\[
\overline T_{c,g}(Q)
=
\left(
\boldsymbol g_{\mathrm{joint}},\,
T_{c,g}(Q)
\right),
\]

\[
S_{c,g}(Q)
=
\inf_{\boldsymbol p_0'}
\left\|
\overline T_{c,g}(Q)\boldsymbol p_0'
-\boldsymbol\alpha
\right\|_2.
\]

其中 \(\boldsymbol p_0'\) 包含全部 \(2^k\) 个模式概率。

## Q 估计量

\[
\widehat Q(\boldsymbol c,\boldsymbol g)
=
\arg\inf_{Q'}
S_{c,g}(Q').
\tag{3.9}
\]

括号中的 \((\boldsymbol c,\boldsymbol g)\) 强调估计量依赖这两个已知向量。

## 增广矩阵

证明需要同时编码概率和为 1。定义

\[
\widetilde T_{c,g}(Q)
=
\begin{pmatrix}
\boldsymbol g_{\mathrm{joint}}&T_{c,g}(Q)\\
1&\boldsymbol E
\end{pmatrix}.
\tag{6.2}
\]

于是

\[
\widetilde T_{c,g}(Q)
\begin{pmatrix}
p_0\\
\boldsymbol p
\end{pmatrix}
=
\begin{pmatrix}
\boldsymbol\mu\\
1
\end{pmatrix}.
\]

最后一行把概率和约束直接放进线性映射。

## 欧氏距离的角色

原文 Remark 3.1 指出，只要距离诱导与欧氏空间相同的拓扑，一致性思路仍可成立。作者选欧氏距离的原因是每个固定 Q 下都能用成熟的二次规划求解。

似然也可作为原则化目标，但计算更复杂。本文的理论重点在 Q 的可分离性，因此采用了容易分析和优化的矩距离。

[下一页：Theorem 3.1](12-theorem-3-1.md)
