# Theorem 3.1：已知 \(c,g\) 的一致性

## 定理条件

假设：

1. \(\boldsymbol c,\boldsymbol g\) 已知；
2. C1--C5 成立；
3. 给定属性后，各题独立生成；
4. 反应概率满足

\[
\Pr(R_r^i=1\mid\xi_r^i)
=
c_i^{\xi_r^i}g_i^{1-\xi_r^i};
\tag{3.10}
\]

5. 对所有题，

\[
c_i\ne g_i;
\]

6. 向量

\[
T_{c-g}(Q)\boldsymbol p^*
\]

没有零分量。

## Q 一致性

令 \(\widehat Q(\boldsymbol c,\boldsymbol g)\) 由式（3.9）定义，则

\[
\lim_{N\to\infty}
\Pr\!\left(
\widehat Q(\boldsymbol c,\boldsymbol g)\sim Q
\right)=1.
\]

## 属性分布一致性

定义

\[
\widetilde{\boldsymbol p}(\boldsymbol c,\boldsymbol g)
=
\arg\inf_{\boldsymbol p}
\left\|
T_{c,g}(\widehat Q)\boldsymbol p
+p_0\boldsymbol g_{\mathrm{joint}}
-\boldsymbol\alpha
\right\|_2^2,
\]

并约束全部模式概率和为 1。适当排列 \(\widehat Q\) 的列后，

\[
\widetilde{\boldsymbol p}(\boldsymbol c,\boldsymbol g)
\overset{p}{\longrightarrow}
\boldsymbol p^*.
\]

## 与 Theorem 2.4 的变化

| 无噪声 | DINA |
| --- | --- |
| 真 Q 的样本损失精确为 0 | 真 Q 的损失几乎必然趋于 0 |
| \(T(Q)\) 为 0/1 矩阵 | \(T_{c,g}(Q)\) 含概率 |
| 全零模式不贡献正响应矩 | 全零模式贡献猜测概率列 |
| 用 Corollary 6.5 分离 | 用 Proposition 6.6 分离 |
| \(T(Q)\) 满列秩 | 增广 \(\widetilde T_{c,g}(Q)\) 满列秩 |

## 条件 \(c_i\ne g_i\)

若某题 \(c_i=g_i\)，则

\[
\Pr(R^i=1\mid\xi^i=1)
=
\Pr(R^i=1\mid\xi^i=0).
\]

该题的反应与其能力指示无关，作答无法提供关于该题 q-vector 的信息。条件 \(c_i\ne g_i\) 保证每题仍保留属性结构信号。

## 非零矩条件

\[
T_{c-g}(Q)\boldsymbol p^*
\]

的每个分量是某个题组的“中心化能力信号”。若常见的

\[
c_i>g_i
\]

成立，再结合 C4，所有相关乘积均为正，该条件自然满足。

若允许某些 \(c_i<g_i\)，不同属性模式的正负贡献可能抵消为 0。定理排除这种退化。

## 证明的核心

经验增广矩满足

\[
\begin{pmatrix}
\boldsymbol\alpha\\
1
\end{pmatrix}
\overset{\text{a.s.}}{\longrightarrow}
\widetilde T_{c,g}(Q)
\begin{pmatrix}
p_0^*\\
\boldsymbol p^*
\end{pmatrix}.
\]

Proposition 6.6 说明，对任何 \(Q'\not\sim Q\) 和任何候选 \(\boldsymbol c'\)，右侧真矩都不属于

\[
\mathcal C\!\left(
\widetilde T_{c',g}(Q')
\right).
\]

由于 \(\boldsymbol c'\in[0,1]^m\) 是紧集，分离距离可以取统一正下界。经验矩收敛后，错误候选的损失仍与 0 保持距离。

## 为什么定理允许证明中遍历 \(c'\)

Theorem 3.1 的估计量使用真 \(\boldsymbol c\)。作者的 Proposition 6.6 给出更强分离：错误 Q 即使能自由调整 \(\boldsymbol c'\)，仍不能覆盖真矩。这个更强结果为第 4 节未知 \(\boldsymbol c\) 的估计铺路。

[下一页：未知 \(c\) 的估计](13-unknown-c-estimation.md)
