# Allman, Matias & Rhodes (2009)：潜在结构模型的可识别性

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Allman, E. S., Matias, C., & Rhodes, J. A. (2009). *Identifiability of parameters in latent structure models with many observed variables*. |
| 期刊 | *The Annals of Statistics*, 37(6A), 3099-3132. |
| DOI | [10.1214/09-AOS689](https://doi.org/10.1214/09-AOS689) |
| arXiv | [arXiv:0809.5032](https://arxiv.org/abs/0809.5032) |
| PDF | [arXiv PDF](https://arxiv.org/pdf/0809.5032) |

这篇论文不是 CDM 的模型论文，而是 CDM 可识别性理论的上游工具文献。它回答的问题是：当有很多观测变量（observed variables）由一个离散潜变量（latent variable）驱动，并且在给定潜变量后局部独立（conditional independence）时，观测联合分布能不能恢复潜在类比例和各类的反应概率。

## 为什么读

CDM 通常可以先看成一个受限潜在类模型（restricted latent class model, RLCM）：被试的属性掌握模式 \(\alpha\) 是潜在类别，项目反应 \(Y_1,\ldots,Y_J\) 是观测变量。若给定 \(\alpha\) 后项目局部独立，则有

\[
P(Y=y)
=
\sum_{\alpha} \nu_{\alpha}
\prod_{j=1}^{J} P(Y_j=y_j\mid \alpha).
\]

这篇论文给 CDM 一个很重要的第一步：

\[
P(Y)
\Longrightarrow
\{\nu_{\alpha},\ P(Y_j=1\mid \alpha)\}
\quad
\text{up to label swapping}.
\]

但它还不能直接给出 Q 矩阵（Q-matrix）、属性标签、DINA 的 guessing/slipping 参数，或者 CDM 的具体约束。也就是说，它解决的是“潜在类混合层是否能识别”，不是“CDM 结构参数是否能识别”。

## 模型设定

论文先考虑有限潜在类模型（finite latent class model）。设潜变量

\[
Z\in\{1,\ldots,r\},
\]

其中 \(r\) 是潜在类别数，\(\pi_i=P(Z=i)\) 是第 \(i\) 类的比例。观测变量为

\[
X_1,\ldots,X_p,
\]

第 \(j\) 个变量有 \(\kappa_j\) 个类别。核心假设是给定 \(Z=i\) 后观测变量相互独立：

\[
P(X_1=x_1,\ldots,X_p=x_p\mid Z=i)
=
\prod_{j=1}^{p}P(X_j=x_j\mid Z=i).
\]

用矩阵表示时，令 \(M_j\) 是一个 \(r\times \kappa_j\) 的条件概率矩阵。第 \(i\) 行是第 \(i\) 个潜在类在第 \(j\) 个观测变量上的条件分布：

\[
M_j(i,\cdot)=P(X_j=\cdot \mid Z=i).
\]

对于 CDM 的二分项目，\(\kappa_j=2\)，所以单个项目的 \(M_j\) 最多只有 2 列。这也是为什么论文需要把多个项目合并成更大的块（blocks）。

## 三变量情形：Kruskal 条件

论文的核心从三变量情形开始。若只有 \(X_1,X_2,X_3\)，观测联合分布可以写成三路张量（three-way tensor）：

\[
P(X_1=u,X_2=v,X_3=w)
=
\sum_{i=1}^{r}
\pi_i
M_1(i,u)M_2(i,v)M_3(i,w).
\]

为了使用 Kruskal 定理，需要定义 Kruskal 秩（Kruskal rank）：

\[
\operatorname{rank}_K(M)
=
\max\{k:\text{任意 } k \text{ 行都线性无关}\}.
\]

设

\[
I_j=\operatorname{rank}_K(M_j),\quad j=1,2,3.
\]

Kruskal 条件是：

\[
I_1+I_2+I_3\ge 2r+2.
\]

如果这个条件成立，则三变量潜在类模型的参数可以识别，除了潜在类别标签可以整体置换。这里的“整体置换”指同一套潜在类标签在所有 \(M_j\) 和 \(\pi\) 中同时重命名，不改变观测分布。

## 多变量情形：把很多变量分成三块

真正对 CDM 有用的是论文的 Theorem 4。因为 CDM 往往有很多项目，单个项目是二分变量，直接使用三变量版本不够。

论文的做法是把 \(p\) 个观测变量分成三个非空且互不重叠的块：

\[
S_1,\ S_2,\ S_3.
\]

每一块被看成一个新的“合并变量”。如果第 \(j\) 个原变量有 \(\kappa_j\) 个类别，那么第 \(a\) 个块的类别数是

\[
K_a=\prod_{j\in S_a}\kappa_j,\quad a=1,2,3.
\]

于是多变量模型被转化成三块模型。Theorem 4 给出的充分条件是：

\[
\min(r,K_1)+\min(r,K_2)+\min(r,K_3)\ge 2r+2.
\]

如果存在这样的三块划分，则模型参数泛可识别（generically identifiable），仍然只差潜在类标签置换。

这里“泛可识别”要读得很谨慎：它不是说所有参数点都可识别，而是说不可识别的参数点只落在一个很小的例外集合里。统计建模时可以把它理解为：一般位置的参数是可识别的，但边界点、重复类别、退化概率等特殊情形仍可能出问题。

## 二分变量的结论

对 CDM 最直接的是 Bernoulli product mixture 的结论。若 \(p\) 个观测变量都是二分变量，即

\[
\kappa_1=\cdots=\kappa_p=2,
\]

论文的 Corollary 5 说明：\(r\) 个潜在类的二分乘积分布混合模型在下面条件下泛可识别：

\[
p\ge 2\lceil\log_2 r\rceil+1.
\]

如果把 CDM 的所有属性掌握模式都看成潜在类别，且没有结构性缺失，那么 \(r=2^K\)，其中 \(K\) 是属性数。因此这个条件变成

\[
J\ge 2K+1.
\]

这不是 CDM 的最终识别条件，但它给了一个清晰的底层直觉：只要二分项目足够多，观测反应分布就有机会先恢复“潜在类比例 + 每个潜在类的项目反应概率轮廓”。

## 对 CDM 的正确用法

这篇论文在 CDM 里最适合放在“第一步识别”：

\[
P(Y)
\Longrightarrow
\text{latent class response profiles}.
\]

后面还需要 CDM 专门论文完成第二步：

\[
\text{response profiles}
\Longrightarrow
Q,\ \alpha,\ g,\ s,\ \text{model constraints}.
\]

也就是说，Allman, Matias & Rhodes (2009) 可以支撑“观测分布中含有足够信息恢复潜在类层”的说法，但不能单独证明 DINA、G-DINA 或 Q 矩阵可识别。

## 证明思路

这篇论文的证明可以按四步理解。

第一步，把三变量潜在类模型写成三路张量：

\[
\sum_{i=1}^{r}\pi_i m_{1i}\otimes m_{2i}\otimes m_{3i}.
\]

第二步，用 Kruskal 条件保证这个三路分解唯一。唯一性不是逐项绝对唯一，而是允许潜在类标签整体置换。

第三步，用“概率矩阵每行和为 1”去消除张量分解里的任意缩放。这样可以从张量因子回到真正的条件概率矩阵和混合比例 \(\pi\)。

第四步，对多变量模型，把很多观测变量合并成三块。合并块的条件概率矩阵等于原矩阵按行做乘积，因此块越大，类别数越多，Kruskal 秩越有机会达到 \(r\)。

## 这篇论文不解决什么

| 不解决的问题 | 为什么 |
| --- | --- |
| Q 矩阵是否可识别 | 论文没有 Q 矩阵，也没有项目-属性结构约束 |
| 属性标签是否可命名 | 潜在类模型只识别到 label swapping，属性标签需要额外结构 |
| DINA 的 \(g\) 和 \(s\) 是否唯一 | DINA 的 conjunctive 结构不在这篇论文的模型设定里 |
| 层级属性结构是否可恢复 | 属性层级会造成结构性零概率或受限类别，需要专门处理 |
| 所有参数点是否可识别 | 论文主线强调的是 generic identifiability，不是 everywhere identifiability |

## 读这篇时要记住的警告

1. 泛可识别不是严格可识别。边界概率、重复潜在类、类别比例为 0、两个反应轮廓完全相同等情形仍然可能导致不可识别。
2. CDM 是受限模型。一个 unrestricted latent class model 的泛可识别结果，不能自动推出某个 CDM 子模型在自己的参数空间里也泛可识别。
3. label swapping 在 CDM 中更麻烦。普通潜在类模型里只是类别重命名；CDM 中还涉及属性维度、属性模式和 Q 矩阵列的解释。
4. \(J\ge 2K+1\) 只能当作底层混合模型的直觉，不是测验设计的充分规则。实际 CDM 还要看 Q 矩阵 completeness、重复测量、项目质量和模型约束。

## 和后续论文的关系

| 后续文献 | 关系 |
| --- | --- |
| Xu (2017) | 把 restricted latent class models with binary responses 作为主对象，往 CDM 方向推进。 |
| Chen, Liu, Xu & Ying (2015) | 进入 Q 矩阵诊断分类模型，处理 Q 结构、估计和统计分析。 |
| Gu & Xu (2021) | 直接讨论 Q 矩阵本身的可识别性。 |
| Gu & Xu 的 DINA 识别论文 | 从 DINA 的必要充分条件角度回答 CDM 结构参数问题。 |

## 我自己的问题

- 如果 CDM 中属性分布有很多结构性零概率，应该把 \(r\) 看成 \(2^K\)，还是只看实际可达的属性模式数？
- 在 DINA 或 G-DINA 约束下，Allman et al. 的 generic 条件是否会落在 CDM 子模型的坏集合里？
- 如果两个属性模式在给定 Q 矩阵下产生相同理想反应，Kruskal 层面能否发现这个问题，还是必须用 Q 矩阵条件单独检查？
- 对 continuous-Q 或 partial-mastery 模型，潜在类别是否还存在，还是需要换成非离散潜变量的识别工具？

## 一句话总结

Allman, Matias & Rhodes (2009) 给 CDM 可识别性提供的是底层混合模型语言：当观测项目足够多并且三块 Kruskal 条件成立时，观测分布可以泛识别潜在类比例和类条件反应概率；但 Q 矩阵、属性命名和 CDM 结构参数还需要后续 CDM 专门理论来完成。
