# 未知 \(c\)：一般估计与矩估计

## 第 4 节的设定

作者进一步假设：

- 猜测概率 \(\boldsymbol g\) 已知；
- 掌握者正确概率 \(\boldsymbol c\) 未知；
- Q 也未知。

开放作答题可把 \(g_i\) 近似设为 0。选择题若每个干扰项同等吸引，可用选项数给出粗略猜测率。原文也承认，这一已知 \(g_i\) 假设较强。

## 一般剖面估计量

给定候选 Q 与已知 \(\boldsymbol g\)，定义

\[
\widetilde{\boldsymbol c}(Q,\boldsymbol g)
=
\arg\inf_{\boldsymbol c\in[0,1]^m}
S_{c,g}(Q).
\tag{4.1}
\]

它适用于任意 Q 结构。计算上需要：

1. 外层搜索 \(\boldsymbol c\)；
2. 每次给定 \(\boldsymbol c\) 后，再对属性分布 \(\boldsymbol p\) 做内层优化。

因此原文称它计算密集。

## 可快速估计某个 \(c_i\) 的结构条件

对题目 \(i\)，若存在不含 \(i\) 的题组 \(i_1,\ldots,i_\ell\)，满足

\[
B_Q(I_i\wedge I_{i_1}\wedge\cdots\wedge I_{i_\ell})
=
B_Q(I_{i_1}\wedge\cdots\wedge I_{i_\ell}),
\tag{4.2}
\]

则题目 \(i\) 要求的属性集合已经被其余题组覆盖。

用集合写法：

\[
\mathcal K_i
\subseteq
\mathcal K_{i_1}\cup\cdots\cup\mathcal K_{i_\ell}.
\]

在真 Q 下，能完成其余题组的人也一定具备完成题 \(i\) 的属性。

## 先消去猜测

定义增广矩阵

\[
\widetilde T_{c,g}(Q)
=
\begin{pmatrix}
\boldsymbol g_{\mathrm{joint}}&T_{c,g}(Q)\\
1&\boldsymbol E
\end{pmatrix}.
\]

Proposition 6.6 的证明构造一个只依赖 \(\boldsymbol g\) 的矩阵 \(D\)，满足

\[
D\widetilde T_{c,g}(Q)
=
\left(
\boldsymbol0,\,
T_{c-g}(Q)
\right).
\]

令 \(\boldsymbol a_g^\top\) 为 D 中对应题组

\[
I_{i_1}\wedge\cdots\wedge I_{i_\ell}
\]

的行，\(\boldsymbol a_{*g}^\top\) 为对应加入 \(I_i\) 后题组的行。

## 两个中心化矩之比

由总体矩映射，

\[
\boldsymbol a_g^\top
\begin{pmatrix}
\boldsymbol\alpha\\1
\end{pmatrix}
\overset{p}{\longrightarrow}
B_{c-g,Q}(I_{i_1}\wedge\cdots\wedge I_{i_\ell})
\boldsymbol p^*,
\]

\[
\boldsymbol a_{*g}^\top
\begin{pmatrix}
\boldsymbol\alpha\\1
\end{pmatrix}
\overset{p}{\longrightarrow}
B_{c-g,Q}(I_i\wedge I_{i_1}\wedge\cdots\wedge I_{i_\ell})
\boldsymbol p^*.
\]

条件（4.2）使加入题 \(i\) 只多出一个因子 \(c_i-g_i\)，所以二者比值趋于

\[
c_i-g_i.
\tag{4.3}
\]

## 矩估计量

论文定义

\[
\overline c_i(Q,\boldsymbol g)
=
g_i+
\frac{
\boldsymbol a_{*g}^\top
\begin{pmatrix}\boldsymbol\alpha\\1\end{pmatrix}
}{
\boldsymbol a_g^\top
\begin{pmatrix}\boldsymbol\alpha\\1\end{pmatrix}
}.
\tag{4.4}
\]

Proposition 4.1 给出：

\[
\overline c_i
\overset{p}{\longrightarrow}
c_i.
\]

## 这个估计量为何快

给定 Q 和 \(\boldsymbol g\) 后：

- D 可以预先构造；
- 分子、分母是对经验矩的仿射变换；
- 不需要数值优化；
- 每个满足（4.2）的题都能独立计算。

代价是它依赖候选 Q 中明确的属性包含结构，且分母过小时会在有限样本中不稳定。

[下一页：组合估计量与 Theorem 4.2](14-combined-estimator-theorem-4-2.md)
