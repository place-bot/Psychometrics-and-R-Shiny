# DINA 模型、数据与全部符号

## 数据结构

有 \(N\) 名学生、\(J\) 道二元计分题、\(K\) 个二元属性。

\[
\boldsymbol Y=(Y_{ij})_{N\times J},
\qquad
Y_{ij}\in\{0,1\}.
\]

\(Y_{ij}=1\) 表示学生 \(i\) 答对题目 \(j\)。

## 学生属性

学生 \(i\) 的潜在属性模式是

\[
\boldsymbol\alpha_i
=
(\alpha_{i1},\ldots,\alpha_{iK})^{\mathsf T},
\qquad
\alpha_{ik}\in\{0,1\}.
\]

共有

\[
C=2^K
\]

种属性模式。论文用 \(\boldsymbol a_c\) 表示第 \(c\) 种模式，并令

\[
\pi_c=P(\boldsymbol\alpha_i=\boldsymbol a_c).
\]

于是

\[
\boldsymbol\pi=(\pi_1,\ldots,\pi_C)^{\mathsf T},
\qquad
\sum_{c=1}^{C}\pi_c=1.
\]

## Q 矩阵

\[
Q=(q_{jk})_{J\times K}
=
(\boldsymbol q_1,\ldots,\boldsymbol q_J)^{\mathsf T}
=
(Q_1,\ldots,Q_K).
\]

这里两种大写/小写写法要分清：

- \(\boldsymbol q_j^{\mathsf T}\)：Q 的第 \(j\) 行，表示第 \(j\) 题要求哪些属性；
- \(Q_k\)：Q 的第 \(k\) 列，表示哪些题要求第 \(k\) 个属性；
- \(q_{jk}=1\)：题目 \(j\) 要求属性 \(k\)；
- \(q_{jk}=0\)：题目 \(j\) 不要求属性 \(k\)。

## 题目参数

每道题有两个参数：

\[
g_j=P(Y_{ij}=1\mid \eta_{ij}=0),
\]

\[
s_j=P(Y_{ij}=0\mid \eta_{ij}=1).
\]

\(g_j\) 是缺少至少一个所需属性时的猜对概率；\(s_j\) 是具备全部所需属性时的失误概率。

单调性限制是

\[
0\le g_j<1-s_j\le1.
\]

它保证全具备者的答对概率高于未全具备者。

## 理想反应指标

\[
\eta_{ij}
=
I(\alpha_{ik}\ge q_{jk},\ \forall k)
=
I(\boldsymbol\alpha_i^{\mathsf T}\boldsymbol q_j
=\boldsymbol q_j^{\mathsf T}\boldsymbol q_j).
\]

- \(\eta_{ij}=1\)：学生具备题目要求的全部属性；
- \(\eta_{ij}=0\)：至少缺一个。

第二个等式利用二元向量：

\[
\boldsymbol q_j^{\mathsf T}\boldsymbol q_j
\]

等于题目要求的属性数，而

\[
\boldsymbol\alpha_i^{\mathsf T}\boldsymbol q_j
\]

等于学生已经具备的所需属性数。二者相等时全部要求均满足。

## 随机变量与观测值

原文特意区分：

- 大写 \(\boldsymbol Y\)：随机作答矩阵；
- 小写 \(\boldsymbol y\)：实际观测到的作答矩阵。

推导中作者有时直接把 \(\boldsymbol Y\) 写进似然。理解时按上下文判断即可。

## 一张符号总表

| 符号 | 维度 | 含义 |
| --- | --- | --- |
| \(N\) | 标量 | 学生数 |
| \(J\) | 标量 | 题目数 |
| \(K\) | 标量 | 属性数 |
| \(C=2^K\) | 标量 | 潜在类数 |
| \(Y_{ij}\) | 标量 | 二元作答 |
| \(\boldsymbol\alpha_i\) | \(K\times1\) | 学生属性模式 |
| \(\boldsymbol a_c\) | \(K\times1\) | 第 \(c\) 个可能模式 |
| \(Q\) | \(J\times K\) | 题目—属性映射 |
| \(\boldsymbol q_j\) | \(K\times1\) | Q 的第 \(j\) 行 |
| \(Q_k\) | \(J\times1\) | Q 的第 \(k\) 列 |
| \(\eta_{ij}\) | 标量 | DINA 理想反应 |
| \(s_j,g_j\) | 标量 | 失误率与猜测率 |
| \(\pi_c\) | 标量 | 第 \(c\) 类的总体比例 |
| \(\mathcal Q\) | 集合 | 满足可识别限制的 Q 空间 |
| \(P\) | \(J\times J\) | 题目行置换矩阵 |
| \(B\) | 标量 | DS2 更新的列块大小 |

[下一页：理想反应、题目反应函数与似然](04-dina-likelihood.md)
