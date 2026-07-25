# 反应概率与似然

## slip 与 guessing

对题目 \(j\)：

\[
s_j
=
P(X_{ij}=0\mid\eta_{ij}=1),
\]

\[
g_j
=
P(X_{ij}=1\mid\eta_{ij}=0).
\]

于是

\[
P(X_{ij}=1\mid\eta_{ij}=1)=1-s_j,
\]

\[
P(X_{ij}=0\mid\eta_{ij}=0)=1-g_j.
\]

## Equation 2

\[
P_j(\boldsymbol\alpha_i)
=
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=
g_j^{1-\eta_{ij}}
(1-s_j)^{\eta_{ij}}.
\tag{3}
\]

分情况看：

\[
P_j(\boldsymbol\alpha_i)
=
\begin{cases}
g_j,&\eta_{ij}=0,\\
1-s_j,&\eta_{ij}=1.
\end{cases}
\]

无噪声时 \(g_j=s_j=0\)，观测反应等于理想反应。实际模型允许两类偏离。

通常希望

\[
1-s_j>g_j,
\]

这样掌握全部所需属性者更可能答对。本文的附录更新式没有额外推导这个不等式约束；软件实现是否强制单调性需要单独检查。

## 给定属性模式的题目似然

对学生 \(i\) 的反应向量

\[
\boldsymbol X_i=(X_{i1},\ldots,X_{iJ}),
\]

在给定 \(\boldsymbol\alpha_i\) 后假设题目局部独立：

\[
L(\boldsymbol X_i\mid\boldsymbol\alpha_i)
=
\prod_{j=1}^{J}
P_j(\boldsymbol\alpha_i)^{X_{ij}}
\left[
1-P_j(\boldsymbol\alpha_i)
\right]^{1-X_{ij}}.
\tag{4}
\]

局部独立使一名学生的联合反应概率分解成 \(J\) 个 Bernoulli 项。

## 已知属性模式时

若所有 \(\boldsymbol\alpha_i\) 已知，可把每道题的学生分成：

- \(\eta_{ij}=0\) 组；
- \(\eta_{ij}=1\) 组。

此时

\[
\widehat g_j
=
\frac{\eta_{ij}=0\text{ 组的答对人数}}
{\eta_{ij}=0\text{ 组人数}},
\]

\[
\widehat s_j
=
\frac{\eta_{ij}=1\text{ 组的答错人数}}
{\eta_{ij}=1\text{ 组人数}}.
\]

EM 只是把未知组别换成后验期望人数。

## 边际似然

属性模式未知。枚举

\[
\boldsymbol\alpha_1,\ldots,\boldsymbol\alpha_L,
\qquad L=2^K,
\]

并设

\[
\pi_l=P(\boldsymbol\alpha_l).
\]

单名学生的边际似然为

\[
L(\boldsymbol X_i)
=
\sum_{l=1}^{L}
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
\pi_l.
\tag{5}
\]

全样本似然：

\[
L(X)
=
\prod_{i=1}^{I}
\sum_{l=1}^{L}
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
\pi_l.
\tag{6}
\]

这就是一个有 \(2^K\) 类、类条件概率受 DINA 约束的有限混合模型。

## 对数形式

数值实现使用

\[
\ell(X)
=
\sum_{i=1}^{I}
\log
\left[
\sum_{l=1}^{L}
\pi_l
\exp\{
\ell_{il}^{\text{conditional}}
\}
\right].
\]

为防止许多小概率相乘下溢，代码使用 log-sum-exp：

\[
\log\sum_l e^{a_l}
=
m+\log\sum_l e^{a_l-m},
\qquad
m=\max_l a_l.
\]

这属于数值实现细节，原文用乘积公式表达统计模型。
