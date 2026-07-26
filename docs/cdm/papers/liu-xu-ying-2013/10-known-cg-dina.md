# 已知失误与猜测参数的 DINA

## 两个项目参数

对第 \(i\) 题：

- \(s_i\)：具备所需属性时仍答错的失误概率；
- \(c_i=1-s_i\)：具备所需属性时答对的概率；
- \(g_i\)：缺少至少一个所需属性时答对的猜测概率。

论文用 \(\boldsymbol c=(c_1,\ldots,c_m)^\top\) 与 \(\boldsymbol g=(g_1,\ldots,g_m)^\top\)。

## DINA 反应函数

\[
\Pr(R^i=1\mid\xi^i)
=
c_i^{\xi^i}g_i^{1-\xi^i}.
\tag{3.1}
\]

分两种情况：

\[
\Pr(R^i=1\mid\xi^i=1)=c_i,
\]

\[
\Pr(R^i=1\mid\xi^i=0)=g_i.
\]

也可以写成

\[
\Pr(R^i=1\mid\boldsymbol A)
=
g_i+(c_i-g_i)\xi^i(\boldsymbol A).
\]

后一写法直接导向 \(T_{c,g}(Q)\) 的构造。

## 局部独立

论文假设给定全部能力指示量后，各题反应联合独立：

\[
\Pr(\boldsymbol R=\boldsymbol r\mid\boldsymbol\xi)
=
\prod_{i=1}^m
\Pr(R^i=r_i\mid\xi^i).
\]

因此对题组 \(S=\{i_1,\ldots,i_\ell\}\)，

\[
\Pr(R^{i_1}=\cdots=R^{i_\ell}=1\mid\boldsymbol A)
=
\prod_{h=1}^{\ell}
\Pr(R^{i_h}=1\mid\boldsymbol A).
\]

这正好对应 B-vector 的逐元素乘法。

## 先看 \(g_i=0\)

若全部猜测概率为 0，缺少所需属性的人不可能答对。对单题定义

\[
B_{c,Q}(I_i)
=c_iB_Q(I_i).
\]

对题组定义

\[
B_{c,Q}(I_{i_1}\wedge\cdots\wedge I_{i_\ell})
=
\mathop{\Upsilon}_{h=1}^{\ell}
B_{c,Q}(I_{i_h}).
\tag{3.3}
\]

令 \(D_c\) 为对角矩阵。若某行对应题组 \(S\)，其对角元素是

\[
\prod_{i\in S}c_i.
\]

于是

\[
T_c(Q)=D_cT(Q).
\tag{3.2}
\]

只要所有 \(c_i\ne0\)，\(D_c\) 可逆，行缩放不会改变 \(T(Q)\) 的列秩。

## 一般 \(g_i>0\)

令

\[
\boldsymbol E=(1,\ldots,1)
\]

为全 1 行向量。对非零属性模式列，单题概率行是

\[
B_{c,g,Q}(I_i)
=
g_i\boldsymbol E
+(c_i-g_i)B_Q(I_i).
\tag{3.5}
\]

若某属性模式具备能力，\(B_Q(I_i)=1\)，该分量等于 \(c_i\)；若不具备能力，分量等于 \(g_i\)。

题组行继续逐元素相乘：

\[
B_{c,g,Q}(I_{i_1}\wedge\cdots\wedge I_{i_\ell})
=
\mathop{\Upsilon}_{h=1}^{\ell}
B_{c,g,Q}(I_{i_h}).
\]

## 为什么全零属性模式需要单独处理

无噪声时全零模式对所有联合答对概率贡献为 0。猜测存在时，它对题组 \(S\) 的贡献为

\[
\prod_{i\in S}g_i.
\]

因此论文保留 \(T_{c,g}(Q)\) 的非零属性列，并把全零模式贡献写成

\[
p_0\boldsymbol g_{\mathrm{joint}},
\]

其中 \(\boldsymbol g_{\mathrm{joint}}\) 按各题组排列猜测概率乘积。

## 常见条件 \(c_i>g_i\)

认知解释通常要求

\[
c_i>g_i.
\]

这表示具备全部所需属性会提高答对概率。Theorem 3.1 的原文条件稍宽，要求 \(c_i\ne g_i\)，并另加一个非零矩条件。后续 Proposition 6.6 通过 \(\boldsymbol c-\boldsymbol g\) 处理两者差异。

[下一页：噪声 T-matrix 与目标函数](11-noisy-tmatrix-objective.md)
