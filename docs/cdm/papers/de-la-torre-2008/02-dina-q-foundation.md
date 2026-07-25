# DINA、Q 矩阵与理想反应

## 基本对象

| 符号 | 含义 |
| --- | --- |
| \(i=1,\ldots,N\) | 学生 |
| \(j=1,\ldots,J\) | 题目 |
| \(k=1,\ldots,K\) | 属性 |
| \(X_{ij}\in\{0,1\}\) | 第 \(i\) 个学生对第 \(j\) 题的作答 |
| \(\boldsymbol\alpha_i\in\{0,1\}^K\) | 学生属性掌握模式 |
| \(\boldsymbol q_j\in\{0,1\}^K\) | 第 \(j\) 题的属性要求 |

论文把 \(2^K\) 个属性模式编号为

\[
\boldsymbol\alpha_l,\qquad l=0,1,\ldots,2^K-1,
\]

其中 \(\boldsymbol\alpha_0=\boldsymbol 0\)。

## DINA 的 AND gate

候选 q-vector 为 \(\boldsymbol q\) 时，学生模式 \(\boldsymbol\alpha_l\) 的理想反应是

\[
\eta_l(\boldsymbol q)
=
\prod_{k=1}^{K}\alpha_{lk}^{q_k}.
\]

解释：

- \(q_k=0\) 时，第 \(k\) 个属性不参与判断；
- \(q_k=1\) 时，只有 \(\alpha_{lk}=1\) 才不会使乘积变成 0；
- 全部所需属性都掌握时 \(\eta=1\)；
- 任一所需属性缺失时 \(\eta=0\)。

本文原式用 \(\eta_{ll'}\) 表示：学生模式是 \(\boldsymbol\alpha_l\)，候选 q-vector 取第 \(l'\) 个非零属性模式。

## 两个项目参数

\[
g_j=P(X_{ij}=1\mid\eta_{ij}=0),
\]

\[
s_j=P(X_{ij}=0\mid\eta_{ij}=1).
\]

因此

\[
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=
g_j^{1-\eta_{ij}}(1-s_j)^{\eta_{ij}}.
\]

也可以写成

\[
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=g_j+(1-s_j-g_j)\eta_{ij}.
\]

后一种形式直接显出两组答对率之差：

\[
(1-s_j)-g_j=1-s_j-g_j.
\]

## 同一道题换 Q 行会发生什么

题目反应 \(X_{ij}\) 没有改变，变化的是：

1. 哪些属性模式进入 \(\eta=1\)；
2. 哪些模式进入 \(\eta=0\)；
3. 两组的后验人数；
4. 两组的后验答对人数；
5. 据此计算的 \(g,s,\delta\)。

所以 \(\delta\) 是“题目与当前 q-vector 组合”的性质。论文明确指出，Q 行改变时它也会改变。

## 三种错误的参数方向

假定真实题目要求属性 1 和 2。

| 候选错误 | 错分方向 | 典型参数变化 |
| --- | --- | --- |
| 漏掉属性 1 | 缺属性 1 的学生混入 \(\eta^*=1\) | \(s^*\) 增大 |
| 多加属性 3 | 掌握 1、2 但没掌握 3 的学生混入 \(\eta^*=0\) | \(g^*\) 增大 |
| 同时漏掉 1、加入 3 | 两侧都发生错分 | \(g^*,s^*\) 都可能增大 |

符号上的星号表示依据候选 q-vector 得到的新分组。

## 局部独立与后验

给定属性模式，DINA 假定各题反应局部独立：

\[
P(\boldsymbol X_i\mid\boldsymbol\alpha_l)
=
\prod_{j=1}^{J}
P(X_{ij}\mid\boldsymbol\alpha_l).
\]

结合属性模式先验 \(\pi_l\)，EM 的 E-step 得到

\[
\widehat p(\boldsymbol\alpha_l\mid\boldsymbol X_i).
\]

这组后验权重是后面快速验证所有候选 q-vector 的计算基础。
