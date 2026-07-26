# Theorem 2：对称性与接受率

## 对称性结论

令

\[
T(x,y)
\]

表示 DS2 从状态 \(x\) 提议到 \(y\) 的概率。Theorem 2 证明

\[
T(Q^\star,Q^{(t)})
=
T(Q^{(t)},Q^\star).
\]

## \(B=1\) 的直观证明

若一个位置属于以下三类，DS2 会固定它：

1. 单位行中的 1；
2. 列和恰为 3 的列中的 1；
3. 只有两份单位行时，其中单位行在目标列上的 0。

这些位置不会产生 \(Q^\star\ne Q^{(t)}\)。

其余合法位置可以取 0 或 1，且两个方向的选择概率均为

\[
\frac12.
\]

## \(B>1\) 的路径概率

给定一条具体提议路径 \(p_i\)，概率由三部分组成：

\[
\frac{1}{K\binom JB}
\times
\frac{1}{
\prod_{i\ne k}
\binom{b_i}{2-l_i}^{I(l_i<2)}
}
\times
\frac{1}{M_B}.
\]

三项依次对应：

1. 选择第 \(k\) 列与大小为 \(B\) 的题目子集；
2. 在需要保护的 \(b_i\) 个位置中选出固定 0；
3. 在 \(M_B\) 个合法自由配置中均匀抽取。

对固定块而言，\(k_1,l_i,b_i,k_0,m\) 在正向和反向中一致。每条从 \(Q^{(t)}\) 到 \(Q^\star\) 的路径都能配对一条选择同样块与保护位置的逆路径，二者概率相同。对所有路径求和即可得到转移对称。

## MH 接受概率

一般 MH 接受率是

\[
r
=
\min\left\{
1,
\frac{
p(Q^\star\mid-)
T(Q^\star,Q^{(t-1)})
}{
p(Q^{(t-1)}\mid-)
T(Q^{(t-1)},Q^\star)
}
\right\}.
\]

由对称性，提议比抵消：

\[
r
=
\min\left\{
1,
\frac{
p(Q^\star\mid
\boldsymbol Y,\boldsymbol\alpha,\boldsymbol s,\boldsymbol g)
}{
p(Q^{(t-1)}\mid
\boldsymbol Y,\boldsymbol\alpha,\boldsymbol s,\boldsymbol g)
}
\right\}.
\]

再利用合法空间内的均匀 Q 先验：

\[
r
=
\min\left\{
1,
\frac{
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q^\star)
}{
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q^{(t-1)})
}
\right\}.
\]

## 接受步骤

抽

\[
U\sim\operatorname{Uniform}(0,1).
\]

若 \(U\le r\)，令 \(Q^{(t)}=Q^\star\)；否则保留 \(Q^{(t-1)}\)。

## 对称性的重要性

DS2 的合法配置数依赖当前矩阵边界。论文的路径配对证明说明这些依赖在正反方向精确抵消。缺少该证明时，直接省略提议比可能把链导向错误平稳分布。

[下一页：Metropolis-within-Gibbs 完整算法](15-metropolis-within-gibbs.md)
