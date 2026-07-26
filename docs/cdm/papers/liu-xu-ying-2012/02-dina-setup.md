# DINA 模型与全部基础符号

## 数据

\[
\boldsymbol R_i=(R_i^1,\ldots,R_i^J)^\top,
\qquad
R_i^j\in\{0,1\}.
\]

- \(i=1,\ldots,N\)：学生；
- \(j=1,\ldots,J\)：题目；
- \(R_i^j=1\)：学生 \(i\) 答对题目 \(j\)。

全部观测组成 \(N\times J\) 反应矩阵。

## 潜在属性模式

\[
\boldsymbol\alpha_i=(\alpha_{i1},\ldots,\alpha_{iK})^\top
\in\{0,1\}^K.
\]

\(\alpha_{ik}=1\) 表示学生掌握属性 \(k\)。共有 \(2^K\) 个可能模式。论文假设

\[
\Pr(\boldsymbol\alpha_i=\boldsymbol\alpha)=p_{\boldsymbol\alpha},
\qquad
\sum_{\boldsymbol\alpha}p_{\boldsymbol\alpha}=1.
\]

\(\boldsymbol p\) 是长度 \(2^K\) 的类别比例向量。

## Q 矩阵

\[
Q=(Q_{jk})_{J\times K},\qquad Q_{jk}\in\{0,1\}.
\]

第 \(j\) 行

\[
\boldsymbol q_j=(Q_{j1},\ldots,Q_{jK})
\]

描述题目 \(j\) 需要哪些属性。

## DINA 理想反应

\[
\xi^j(\boldsymbol\alpha,Q)
=
\mathbf 1
\left(
\alpha_k\ge Q_{jk},\ \forall k
\right).
\tag{1}
\]

若学生覆盖题目要求的全部属性，\(\xi^j=1\)；只要缺少一项，\(\xi^j=0\)。额外掌握未要求属性不会改变该题的理想状态。

也可写为

\[
\xi^j(\boldsymbol\alpha,Q)
=
\prod_{k=1}^K \alpha_k^{Q_{jk}}.
\]

## slipping、guessing 与 \(c\)

- \(s_j\)：具备全部所需属性者答错的概率；
- \(g_j\)：未覆盖全部所需属性者答对的概率；
- \(c_j=1-s_j\)：具备全部所需属性者答对的概率。

令

\[
\pi_{j\boldsymbol\alpha}
=
\Pr(R^j=1\mid \boldsymbol\alpha,Q,\boldsymbol c,\boldsymbol g),
\]

则

\[
\pi_{j\boldsymbol\alpha}
=
c_j^{\xi^j}
g_j^{1-\xi^j}
=
g_j+(c_j-g_j)\xi^j.
\tag{2}
\]

通常需要 \(c_j>g_j\)，题目才具有正向诊断意义；原文的自然约束只写 \([0,1]\)，没有在式 (15) 中额外写出这一顺序约束。

## 局部独立

给定 \(\boldsymbol\alpha_i\)，各题反应条件独立：

\[
\Pr(\boldsymbol R_i=\boldsymbol r\mid\boldsymbol\alpha_i)
=
\prod_{j=1}^J
\pi_{j\boldsymbol\alpha_i}^{r_j}
(1-\pi_{j\boldsymbol\alpha_i})^{1-r_j}.
\]

局部独立使多题联合答对概率变成单题概率的乘积，这正是 \(T\)-matrix 构造可以成立的关键。
