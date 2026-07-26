# Lemma 6.7 与消去猜测的矩阵 \(D\)

## Lemma 6.7

若

\[
T_1\boldsymbol p\in\mathcal C(T_2),
\]

则存在某个 \(\boldsymbol b\)，使

\[
T_1\boldsymbol p=T_2\boldsymbol b.
\]

左乘任意维度相容的 D：

\[
DT_1\boldsymbol p
=
DT_2\boldsymbol b
\in
\mathcal C(DT_2).
\]

所以逆否命题为：

\[
DT_1\boldsymbol p
\notin\mathcal C(DT_2)
\quad\Longrightarrow\quad
T_1\boldsymbol p
\notin\mathcal C(T_2).
\]

这允许先对矩阵做方便的行变换。

## D 的目标

作者构造一个只依赖已知 \(\boldsymbol g\) 的矩阵 D，使

\[
D\widetilde T_{c,g}(Q)
=
\left(
\boldsymbol0,\,
T_{c-g}(Q)
\right).
\]

第一列对应全零属性模式。变换后它完全为 0；其余列变成没有猜测项、行缩放为 \(c_i-g_i\) 的 T-matrix。

## 单题行

由

\[
B_{c,g,Q}(I_i)
=
g_i\boldsymbol E+(c_i-g_i)B_Q(I_i),
\]

可得

\[
\left(
0,\,
B_{c-g,Q}(I_i)
\right)
=
\left(
g_i,\,
B_{c,g,Q}(I_i)
\right)
-g_i\boldsymbol E.
\tag{6.3}
\]

右侧只用到增广矩阵中的单题行与最后的全 1 行，系数只依赖 \(g_i\)。

## 题组行的归纳

假设所有不超过 \(j\) 道题的中心化行都能由增广行线性表示。对 \(j+1\) 道题，

\[
\left(
\prod_{h=1}^{j+1}g_{i_h},\,
B_{c,g,Q}(I_{i_1}\wedge\cdots\wedge I_{i_{j+1}})
\right)
\]

等于单题增广行的逐元素乘积。把每个单题行拆成

\[
g_{i_h}\boldsymbol E
+
\left(0,B_{c-g,Q}(I_{i_h})\right)
\]

并展开：

- 最后一项是所需的 \(j+1\) 题中心化行；
- 其余项只包含不超过 \(j\) 个中心化因子；
- 归纳假设保证其余项已经属于增广矩阵行空间。

因此目标行也属于该行空间。对全部非空题组执行即可组成 D。

## 两题时的显式容斥

把总体矩按

\[
1,\quad
\mu_1=E(R^1),\quad
\mu_2=E(R^2),\quad
\mu_{12}=E(R^1R^2)
\]

排列。

中心化单题矩为

\[
E(R^1-g_1)=\mu_1-g_1,
\]

\[
E(R^2-g_2)=\mu_2-g_2.
\]

中心化题对矩为

\[
\begin{aligned}
E[(R^1-g_1)(R^2-g_2)]
&=
\mu_{12}
-g_2\mu_1
-g_1\mu_2
+g_1g_2.
\end{aligned}
\]

对应行变换矩阵可以写成

\[
D=
\begin{pmatrix}
-g_1&1&0&0\\
-g_2&0&1&0\\
g_1g_2&-g_2&-g_1&1
\end{pmatrix}.
\]

它正是多项式展开或容斥变换。

## 为什么全零属性列变成 0

全零模式下每题条件正确率为 \(g_i\)。所以

\[
E(R^i-g_i\mid\boldsymbol A=\boldsymbol0)=0.
\]

任意非空题组的中心化乘积也为 0。由此，变换后的第一列全为 0。

## 为什么其他列变成 \(T_{c-g}(Q)\)

给定非零属性模式，

\[
E(R^i-g_i\mid\boldsymbol A)
=
(c_i-g_i)\xi^i(\boldsymbol A).
\]

局部独立给出题组乘积：

\[
E\!\left[
\prod_{i\in S}(R^i-g_i)
\mid\boldsymbol A
\right]
=
\prod_{i\in S}(c_i-g_i)
\prod_{i\in S}\xi^i(\boldsymbol A).
\]

这恰好是 \(T_{c-g}(Q)\) 对应元素。

## 变换完成了什么

D 把带基线猜测的概率矩化成“净能力信号矩”。随后无猜测情形的列空间分离命题可直接应用。D 不依赖 Q 或 \(\boldsymbol c\)，所以真模型与全部候选模型能用同一变换比较。

[下一页：三个主定理的证明](19-main-theorem-proofs.md)
