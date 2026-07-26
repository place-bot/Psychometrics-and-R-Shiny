# 各层先验与完整条件分布

## 属性比例 \(\boldsymbol\pi\)

先验为

\[
\boldsymbol\pi\sim
\operatorname{Dirichlet}(\delta_{01},\ldots,\delta_{0C}).
\]

若当前属性类计数为

\[
n_c=\sum_{i=1}^{N}
I(\boldsymbol\alpha_i=\boldsymbol a_c),
\]

共轭更新是

\[
\boldsymbol\pi\mid\boldsymbol\alpha
\sim
\operatorname{Dirichlet}
(\delta_{01}+n_1,\ldots,\delta_{0C}+n_C).
\]

作者代码使用 \(\delta_{0c}=1\)。

## 学生属性 \(\boldsymbol\alpha_i\)

对每个候选类 \(c\) 计算

\[
w_{ic}
=
\pi_c
\prod_{j=1}^{J}
p(Y_{ij}=y_{ij}\mid
\boldsymbol a_c,s_j,g_j,\boldsymbol q_j).
\]

归一化后

\[
P(\boldsymbol\alpha_i=\boldsymbol a_c\mid-)
=
\frac{w_{ic}}{\sum_{d=1}^{C}w_{id}}.
\]

原始 C++ 的 `parm_update_nomiss()` 对每名学生循环全部 \(2^K\) 个类，计算 `pYit()`，再做一次 categorical 抽样。

## 猜测率 \(g_j\)

给定当前理想反应，设未全具备组中：

\[
G_j
=
\sum_i I(\eta_{ij}=0,Y_{ij}=1),
\]

\[
F_j
=
\sum_i I(\eta_{ij}=0,Y_{ij}=0).
\]

忽略单调截断时，

\[
g_j\mid-\sim
\operatorname{Beta}
(\alpha_g+G_j,\beta_g+F_j).
\]

由于要求 \(g_j<1-s_j\)，实际完整条件分布截断在

\[
[0,1-s_j).
\]

代码先计算 Beta CDF

\[
u_{\max}
=
F_{\text{Beta}}(1-s_j;
\alpha_g+G_j,\beta_g+F_j),
\]

再抽 \(u\sim U(0,u_{\max})\)，最后用 Beta 分位数函数得到 \(g_j\)。

## 失误率 \(s_j\)

在全具备组中，令

\[
S_j
=
\sum_i I(\eta_{ij}=1,Y_{ij}=0),
\]

\[
C_j
=
\sum_i I(\eta_{ij}=1,Y_{ij}=1).
\]

忽略截断时，

\[
s_j\mid-\sim
\operatorname{Beta}
(\alpha_s+S_j,\beta_s+C_j).
\]

在已更新的 \(g_j\) 下，把分布截断到

\[
[0,1-g_j).
\]

## Q 的完整条件

\[
p(Q\mid
\boldsymbol Y,\boldsymbol\alpha,\boldsymbol s,\boldsymbol g)
\propto
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q)
I(Q\in\mathcal Q).
\]

Q 的先验在合法空间内为常数，所以合法候选之间的后验比完全由条件似然决定。

## 超参数在论文和代码中的位置

正文把

\[
\boldsymbol\delta_0,\quad
\alpha_s,\beta_s,\alpha_g,\beta_g
\]

保留为一般超参数。补充 C++ 固定：

\[
\delta_{0c}=1,\qquad
\alpha_s=\beta_s=\alpha_g=\beta_g=1.
\]

这使潜在类比例和未截断题目参数先验均为均匀先验。复现原文时应记录这组实现选择。

## 更新顺序带来的条件关系

代码先按旧 \(s_j\) 截断 \(g_j\)，再按新 \(g_j\) 截断 \(s_j\)。二者构成对联合截断 Beta 密度的 Gibbs 更新。每一步都满足

\[
0\le g_j<1-s_j\le1.
\]

[下一页：Q 的三条可识别条件](07-identifiability-conditions.md)
