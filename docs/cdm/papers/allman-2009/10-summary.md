# 总结与后续阅读

## 一条公式概括主结果

对有限潜在类模型，若能把观测变量分成三个非空块，并令

\[
K_a=\prod_{j\in S_a}\kappa_j,
\]

使

\[
\min(r,K_1)+\min(r,K_2)+\min(r,K_3)
\ge2r+2,
\]

则一般参数点上的

\[
\pi,\ M_1,\ldots,M_p
\]

可以由观测联合分布恢复到潜在类共同置换。

## 证明方法的最短版本

\[
P(X_1,\ldots,X_p)
\longrightarrow
[\operatorname{diag}(\pi)N_1,N_2,N_3]
\]

\[
\overset{\text{Kruskal}}{\longrightarrow}
\pi,N_1,N_2,N_3
\overset{\text{边缘化}}{\longrightarrow}
\pi,M_1,\ldots,M_p.
\]

其中

\[
N_a
=
\mathop{\otimes_{\mathrm{row}}}_{j\in S_a}M_j.
\]

## 五个必须记住的结论

1. 三路张量比两路矩阵提供更强的分解唯一性。
2. Kruskal 秩条件是点态充分条件；最大可能秩条件给出泛识别。
3. 多个观测变量可以合并成三个复合变量，块状态数以乘法增长。
4. \(r\) 类 Bernoulli 乘积混合在
   \[
   p\ge2\lceil\log_2r\rceil+1
   \]
   时泛可识别到标签置换。
5. 同一套条件独立分块思想还能处理 HMM、随机图和非参数乘积混合。

## 五个边界

1. 潜在类别数 \(r\) 假定已知。
2. generic 允许测度为 0 的不可识别参数点。
3. 理论唯一性不保证有限样本估计稳定。
4. 论文没有估计算法、数据实验或官方代码。
5. 一般潜在类识别没有直接恢复 Q 矩阵和属性含义。

## 对 CDM 的准确结论

若把属性模式当潜在类别，本篇支持

\[
P(\boldsymbol Y)
\longrightarrow
\text{潜在类比例和类条件项目反应概率}
\]

这一步的理论思路。后续仍需 CDM 专门条件完成

\[
\text{无名字的潜在类表}
\longrightarrow
Q,\boldsymbol\alpha,g,s
\quad\text{或其他 CDM 参数}.
\]

完整属性模式下 \(r=2^K\)，Corollary 5 给出

\[
J\ge2K+1
\]

的底层混合模型充分上界。它提供理论直觉，不替代 Q 矩阵完整性、属性重复测量和模型专门的识别条件。

## Kruskal (1977) 专题已经补齐

Allman 等人的证明把 Kruskal 定理当作核心工具。对应的数学工具专题已经完成：

> Kruskal, J. B. (1977). Three-way arrays: Rank and uniqueness of trilinear decompositions, with application to arithmetic complexity and statistics.

[进入 Kruskal (1977) 完整专题](../kruskal-1977/index.md)，可继续查看：

- Kruskal rank 与普通 rank 的本质差别；
- \(I_1+I_2+I_3\ge2r+2\) 从哪里来；
- 唯一性中的 permutation 与 scaling 怎样严格表达；
- 条件是充分的还是必要的；
- 张量退化和数值不稳定怎样区分；
- 后续 CDM 三块证明具体调用了定理的哪一部分。

## CDM 主线的后续顺序

完成 Kruskal 工具后，CDM 主线依次进入：

1. de la Torre (2009)：DINA 模型与参数估计；
2. de la Torre (2011)：G-DINA 框架；
3. Xu (2017)：二分 RLCM 可识别性；
4. Gu 与 Xu：DINA 识别与可估计条件；
5. Gu and Xu (2021)：Q 矩阵的必要充分识别条件。

这样读可以把“模型是什么”“为什么能识别”“怎样估计”三条线连起来。
