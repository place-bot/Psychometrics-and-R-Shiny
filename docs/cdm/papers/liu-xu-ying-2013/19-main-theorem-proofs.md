# 三个主定理的证明

## Theorem 2.4

### 真候选

无噪声下逐样本成立

\[
\boldsymbol\alpha=T(Q)\widehat{\boldsymbol p}.
\]

因此

\[
S(Q)=0
\]

的概率为 1。

### 任意错误候选

对 \(Q'\not\sim Q\)，Corollary 6.5 给出

\[
T(Q)\boldsymbol p^*
\notin\mathcal C(T(Q')).
\]

所以存在 \(\delta_{Q'}>0\)。又因

\[
\boldsymbol\alpha
=T(Q)\widehat{\boldsymbol p}
\longrightarrow
T(Q)\boldsymbol p^*,
\]

有

\[
\Pr\!\left[
\inf_{\boldsymbol p}
\|T(Q')\boldsymbol p-\boldsymbol\alpha\|_2
>\delta_{Q'}
\right]
\longrightarrow1.
\]

### 同时排除全部错误候选

二元 Q 数量有限，因此可对全部错误候选同时成立。全局最小化者最终属于 \([Q]\)。

### \(\boldsymbol p\) 一致

Proposition 6.1 使

\[
T(Q)\boldsymbol p=\boldsymbol\alpha
\]

的解唯一。事件 \(\widehat Q=Q\) 上，

\[
\widetilde{\boldsymbol p}=\widehat{\boldsymbol p}.
\]

由大数定律得到 \(\widetilde{\boldsymbol p}\to\boldsymbol p^*\)。

## Theorem 3.1

### 真候选损失趋于 0

局部独立和大数定律给出

\[
\left\|
T_{c,g}(Q)\boldsymbol p^*
+p_0^*\boldsymbol g_{\mathrm{joint}}
-\boldsymbol\alpha
\right\|_2
\overset{\text{a.s.}}{\longrightarrow}0.
\]

所以

\[
S_{c,g}(Q)\overset{\text{a.s.}}{\longrightarrow}0.
\]

### 错误候选存在统一间隔

经验增广矩收敛：

\[
\begin{pmatrix}\boldsymbol\alpha\\1\end{pmatrix}
\longrightarrow
\widetilde T_{c,g}(Q)\boldsymbol p_0^*.
\]

Proposition 6.6 说明右侧不属于任何错误 \(Q'\) 的候选列空间。对每个 \(\boldsymbol c'\) 的距离记为 \(\delta(\boldsymbol c')\)。连续性与紧性给出

\[
\delta
=
\inf_{\boldsymbol c'\in[0,1]^m}
\delta(\boldsymbol c')
>0.
\]

经验矩足够接近总体矩后，错误 Q 的最优损失大于 \(\delta/2\)，真 Q 的损失接近 0。

### \(\boldsymbol p\) 一致

Proposition 6.6 还证明

\[
\widetilde T_{c,g}(Q)
\]

满列秩。Q 等价类恢复后，增广线性方程的属性分布解唯一，故估计分布收敛到 \(\boldsymbol p^*\)。

## Theorem 4.2

### 真 Q 下组合 \(c\) 估计使损失趋于 0

满足（4.2）的分量由 Proposition 4.1 一致估计。其余分量通过式（4.1）的剖面最小化处理。目标函数关于 \(\boldsymbol c\) 连续，所以

\[
\inf_{\boldsymbol p_0}
\left\|
\widetilde T_{\widehat c(Q,g),g}(Q)\boldsymbol p_0
-
\begin{pmatrix}\boldsymbol\alpha\\1\end{pmatrix}
\right\|_2
\overset{p}{\longrightarrow}0.
\]

### 错误 Q 仍保持距离

Proposition 6.6 的分离对任意

\[
\boldsymbol c'\in[0,1]^m
\]

成立，因而包括错误候选自己选出的 \(\widehat{\boldsymbol c}(Q',g)\)。沿用 Theorem 3.1 的紧集论证即可得到 Q 一致。

### 属性分布部分

若

\[
\widetilde{\boldsymbol c}(Q,g)
\overset{p}{\longrightarrow}\boldsymbol c,
\]

组合估计 \(\widehat{\boldsymbol c}(Q,g)\) 也一致。再结合 Q 一致与增广矩阵满列秩，推出

\[
\widetilde{\boldsymbol p}_{\widehat c}(g)
\overset{p}{\longrightarrow}
\boldsymbol p^*.
\]

## 三个证明共用的统计模板

\[
\text{经验矩收敛}
\quad+\quad
\text{错误模型正距离}
\quad+\quad
\text{候选空间有限}
\]

\[
\Longrightarrow
\Pr(\widehat Q\sim Q)\to1.
\]

无噪声、已知参数和未知 \(c\) 的差别集中在两点：

- 怎样证明真 Q 的最优损失趋于 0；
- 怎样构造适合当前噪声结构的列空间分离。

[下一页：附录证明与 C5](20-appendix-and-c5.md)
