# 目标函数、Q 估计量与计算

## 固定候选 Q：先拟合属性分布

对任意候选

\[
Q'\in\{0,1\}^{m\times k},
\]

定义

\[
S(Q')
=
\inf_{\boldsymbol p\in[0,1]^{2^k-1}}
\left\|
T(Q')\boldsymbol p-\boldsymbol\alpha
\right\|_2,
\tag{2.6}
\]

并要求

\[
0\le
\sum_{\boldsymbol A\ne\boldsymbol0}p_{\boldsymbol A}
\le1.
\]

缺少的概率质量对应全零属性模式：

\[
p_{\boldsymbol0}
=
1-
\sum_{\boldsymbol A\ne\boldsymbol0}p_{\boldsymbol A}.
\]

## \(S(Q')\) 的几何解释

\(T(Q')\boldsymbol p\) 随 \(\boldsymbol p\) 变化形成候选 Q 能生成的一组矩向量。概率约束使它成为 \(T(Q')\) 各列与原点的凸包。

\[
S(Q')
=
\operatorname{dist}
\left(
\boldsymbol\alpha,\,
\{T(Q')\boldsymbol p:\boldsymbol p\ge0,\ \mathbf1^\top\boldsymbol p\le1\}
\right).
\]

所以：

- \(S(Q')=0\)：候选 Q 可用某个属性分布精确解释样本矩；
- \(S(Q')>0\)：任何合法属性分布都留下残差；
- 距离越小：候选 Q 的矩结构与数据越接近。

## 外层 Q 估计

论文定义

\[
\widehat Q
=
\arg\inf_{Q'}S(Q').
\tag{2.7}
\]

这是一个双层离散优化：

1. 内层：固定 \(Q'\)，优化连续的 \(\boldsymbol p\)；
2. 外层：比较所有二元矩阵 \(Q'\)。

内层是带线性约束的二次规划。若最小化平方距离，

\[
\frac12
\left\|T(Q')\boldsymbol p-\boldsymbol\alpha\right\|_2^2,
\]

目标关于 \(\boldsymbol p\) 为凸二次函数。

## 真 Q 为什么总是最小化者

无噪声样本满足

\[
T(Q)\widehat{\boldsymbol p}
=\boldsymbol\alpha.
\]

而 \(\widehat{\boldsymbol p}\) 满足概率约束，因此

\[
S(Q)=0.
\]

距离不会小于 0，所以真 Q 一定属于全局最小化集合。

问题随即转化为：

> 还会有哪些 \(Q'\) 也能使距离为 0？

列置换等价的候选一定能达到 0。主定理要证明，在 C1--C5 下，随着样本量增大，其他候选无法继续达到最小值。

## 最小化者为何可能不唯一

若 \(Q'\) 只是交换 Q 的属性列，那么其 \(T\)-matrix 只交换属性模式列。把 \(\boldsymbol p\) 按相同方式重排，乘积保持不变。

因此

\[
Q'\sim Q
\quad\Longrightarrow\quad
S(Q')=S(Q).
\]

论文把整个等价类都视为正确恢复。

## 计算规模

候选空间最多包含

\[
2^{mk}
\]

个二元矩阵。若排除全零题目行，每行有 \(2^k-1\) 种选择，候选数仍为

\[
(2^k-1)^m.
\]

饱和 \(T\)-matrix 又有

\[
2^m-1
\]

行。因此定义清晰的全局估计量在大 \(m,k\) 下计算昂贵。

## 论文提出的实用缓解

Remark 2.6 建议把 \(m\) 道题拆成若干可能重叠的题组，对每个较小 Q 子矩阵分别估计，再合并结果。

Remark 2.7 还建议只保留：

- 单题组合；
- 题对；
- 直到某个最高阶数 \(j\) 的题组。

这会降低计算和抽样噪声，但主定理的饱和性条件不再原样成立。实践算法与理论估计量之间需要清楚区分。

[下一页：三题两属性完整手算](06-worked-example.md)
