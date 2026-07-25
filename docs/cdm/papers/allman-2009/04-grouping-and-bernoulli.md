# 分块定理与 Bernoulli 混合

## 为什么要把变量分成三块

三变量定理要求三个因子矩阵有足够高的 Kruskal 秩。二分项目的单题矩阵只有两列，即使潜在类很多也有

\[
\operatorname{rank}_K(M_j)\le 2.
\]

将多道题合并成一个复合变量后，若一个块含 \(m\) 道二分题，复合变量有

\[
2^m
\]

种反应模式。对应的块条件概率矩阵有 \(2^m\) 列，可能达到更高行秩。

## 三块划分

把变量索引集合

\[
\{1,\ldots,p\}
\]

划分为三个非空、互不相交的集合

\[
S_1,\ S_2,\ S_3.
\]

第 \(a\) 个复合变量是

\[
X_{S_a}=(X_j:j\in S_a).
\]

它的状态数为

\[
K_a=\prod_{j\in S_a}\kappa_j,
\qquad a=1,2,3.
\]

原文在 Theorem 4 中用 \(\kappa_a\) 表示这个块状态数；本站改用 \(K_a\)，避免和单变量状态数 \(\kappa_j\) 混淆。

## 行张量积

若

\[
A_1\in\mathbb R^{r\times a_1},
\qquad
A_2\in\mathbb R^{r\times a_2},
\]

它们的行张量积记作

\[
A_1\otimes_{\mathrm{row}}A_2
\in\mathbb R^{r\times a_1a_2}.
\]

第 \(i\) 行等于两矩阵第 \(i\) 行的 Kronecker 积：

\[
\bigl(A_1\otimes_{\mathrm{row}}A_2\bigr)(i,\cdot)
=
A_1(i,\cdot)\otimes A_2(i,\cdot).
\]

对块 \(S_a\)，定义

\[
N_a
=
\mathop{\otimes_{\mathrm{row}}}_{j\in S_a}M_j
\in\mathbb R^{r\times K_a}.
\]

给定 \(Z=i\) 后原变量独立，所以 \(N_a\) 第 \(i\) 行就是复合变量 \(X_{S_a}\) 的条件联合分布。

## 一个两道二分题的块

若

\[
M_1(i,\cdot)=(1-\theta_{1i},\theta_{1i}),
\qquad
M_2(i,\cdot)=(1-\theta_{2i},\theta_{2i}),
\]

则两题块矩阵的第 \(i\) 行为

\[
\begin{aligned}
N(i,\cdot)
=\bigl(&
(1-\theta_{1i})(1-\theta_{2i}),\\
&(1-\theta_{1i})\theta_{2i},\\
&\theta_{1i}(1-\theta_{2i}),\\
&\theta_{1i}\theta_{2i}
\bigr).
\end{aligned}
\]

四列依次对应反应模式

\[
(0,0),(0,1),(1,0),(1,1).
\]

把某一道题边缘化回来，只需对另一题的状态求和。例如

\[
\theta_{1i}
=
N_i(1,0)+N_i(1,1).
\]

这就是论文 Lemma 14 的概率直觉：若块矩阵由若干随机矩阵做行张量积得到，原单变量矩阵可以通过边缘化唯一恢复。

## Lemma 12、13、14 各做什么

| 引理 | 作用 |
| --- | --- |
| Lemma 12 | 条件独立保证块条件概率矩阵等于单变量矩阵的行张量积 |
| Lemma 13 | 一般矩阵的行张量积具有最大可能 Kruskal 秩 \(\min(r,K_a)\) |
| Lemma 14 | 从随机块矩阵 \(N_a\) 通过边缘化唯一恢复块内每个 \(M_j\) |

这三条把“多变量问题”完整接回“三变量 Kruskal 问题”。

## Theorem 4：多变量泛可识别

若存在三块划分，使

\[
\min(r,K_1)+\min(r,K_2)+\min(r,K_3)
\ge 2r+2,
\tag{2}
\]

则

\[
\mathcal M(r;\kappa_1,\ldots,\kappa_p)
\]

的参数泛可识别到标签置换。固定正的类别比例也不改变结论。

证明链条是：

\[
\{M_j\}_{j=1}^{p}
\overset{\text{行张量积}}{\longrightarrow}
(N_1,N_2,N_3)
\overset{\text{Kruskal}}{\longrightarrow}
(\pi,N_1,N_2,N_3)
\overset{\text{边缘化}}{\longrightarrow}
(\pi,M_1,\ldots,M_p).
\]

## Lemma 13 为什么能得到最大秩

论文用一个 Vandermonde 构造证明“至少存在一个满秩点”。

对第 \(a\) 个单变量矩阵选择互异素数 \(x_{a1},\ldots,x_{a\kappa_a}\)，令行 \(i\) 由这些数的 \(i-1\) 次幂组成：

\[
A_a(i,\ell)=x_{a\ell}^{i-1}.
\]

行张量积中的列对应乘积

\[
\prod_a x_{a,\ell_a}.
\]

素因数分解唯一性保证不同列索引给出不同乘积，因此行张量积成为一个 Vandermonde 型矩阵，达到最大可能秩。

满秩子式是原矩阵元素的多项式，而且该构造让某个子式非零，所以子式并非恒等于 0。秩下降只发生在它的零点集合上。

## Corollary 5：二分变量的简洁上界

现在令所有变量都是 Bernoulli：

\[
\kappa_1=\cdots=\kappa_p=2.
\]

设

\[
k=\lceil\log_2r\rceil.
\]

取三个块的大小为

\[
|S_1|=k,\qquad
|S_2|=k,\qquad
|S_3|=1.
\]

块状态数为

\[
K_1=2^k,\qquad
K_2=2^k,\qquad
K_3=2.
\]

由于 \(2^k\ge r\)，Theorem 4 的左边变成

\[
\min(r,2^k)+\min(r,2^k)+\min(r,2)
=
r+r+2
=
2r+2.
\]

因此只要

\[
p\ge 2\lceil\log_2r\rceil+1,
\tag{B}
\]

\(r\) 个 Bernoulli 乘积分布的有限混合就泛可识别到标签置换。

## 上界随潜在类数怎样增长

| 潜在类数 \(r\) | \(\lceil\log_2r\rceil\) | Corollary 5 给出的充分变量数 |
| ---: | ---: | ---: |
| 2 | 1 | 3 |
| 3 | 2 | 5 |
| 4 | 2 | 5 |
| 5--8 | 3 | 7 |
| 9--16 | 4 | 9 |
| 17--32 | 5 | 11 |

该上界按 \(\log_2r\) 增长。论文还用维度比较指出最少变量数的增长阶也是 \(\log_2r\)，所以 Corollary 5 得到了正确的增长阶，但常数未必最优。

## 翻译成完整属性模式 CDM

若有 \(K\) 个二分属性，并允许全部

\[
r=2^K
\]

个属性模式，则

\[
\lceil\log_2r\rceil=K.
\]

Corollary 5 变成

\[
J\ge 2K+1.
\tag{CDM intuition}
\]

这条式子只描述无约束 Bernoulli 潜在类混合的泛识别上界。它不能直接替代 CDM 的 Q 矩阵设计条件，原因包括：

1. CDM 的 \(\theta_{j,\boldsymbol\alpha}\) 受 Q 矩阵和模型函数约束，不是一般位置的自由参数；
2. 某些属性模式可能结构性缺失，实际类别数小于 \(2^K\)；
3. 不同属性模式可能在给定 Q 下产生相同理想反应；
4. 一般潜在类识别只保留无名字的类别，无法自动恢复属性坐标；
5. DINA 的 \(g_j,s_j\) 需要利用模型的合取结构进一步识别。

因此 \(J\ge 2K+1\) 适合解释“为什么足够多二分项目可以支撑潜在类恢复”，不适合直接充当 CDM 测验组卷规则。

## 一般 \(\kappa\) 状态变量

若每个观测变量都有相同的 \(\kappa\) 个状态，同样的分块论证给出

\[
p\ge 2\lceil\log_\kappa r\rceil+1.
\]

单变量状态越丰富，达到 \(r\) 个可区分块状态所需的变量数越少。这一规律也出现在论文的 HMM 结果中：可观测状态数增加时，识别所需的连续观测长度可以下降。

