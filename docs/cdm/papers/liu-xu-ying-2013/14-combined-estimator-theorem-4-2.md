# 组合估计量与 Theorem 4.2

## 把 \(c\) 分成两部分

对固定候选 Q，把

\[
\boldsymbol c
=
(\boldsymbol c^*,\boldsymbol c^{**})
\]

分组：

- \(\boldsymbol c^*\)：对应满足条件（4.2）的题目；
- \(\boldsymbol c^{**}\)：对应无法直接使用矩比值的题目。

## 第一部分：矩估计

逐元素使用

\[
\overline{\boldsymbol c}^{\,*}(Q,\boldsymbol g).
\]

Proposition 4.1 保证在真 Q 下这些分量一致。

## 第二部分：条件剖面

固定 \(\overline{\boldsymbol c}^{\,*}\) 后，对剩余分量优化：

\[
\widetilde{\boldsymbol c}^{\,**}(Q,\boldsymbol g)
=
\arg\inf_{\boldsymbol c^{**}}
S_{(\overline{\boldsymbol c}^{\,*},\boldsymbol c^{**}),g}(Q).
\]

组合后得到

\[
\widehat{\boldsymbol c}(Q,\boldsymbol g)
=
\left(
\overline{\boldsymbol c}^{\,*}(Q,\boldsymbol g),
\widetilde{\boldsymbol c}^{\,**}(Q,\boldsymbol g)
\right).
\]

任何大于 1 的分量截到 1，任何小于 0 的分量截到 0，因此

\[
\widehat{\boldsymbol c}(Q,\boldsymbol g)\in[0,1]^m.
\]

## Q 估计量

把每个候选 Q 自己对应的 \(\widehat{\boldsymbol c}(Q,\boldsymbol g)\) 代入：

\[
\widehat Q_{\widehat c}(g)
=
\arg\inf_{Q'}
S_{\widehat c(Q',g),g}(Q').
\]

算法概念上是：

1. 枚举候选 \(Q'\)；
2. 检查每道题是否满足（4.2）；
3. 可用的分量计算矩估计；
4. 其余分量与属性分布一起剖面化；
5. 比较候选 Q 的最终矩距离。

## Theorem 4.2：Q 的一致性

假设 \(\boldsymbol g\) 已知，并且 Theorem 3.1 的条件成立，则

\[
\lim_{N\to\infty}
\Pr\!\left(
\widehat Q_{\widehat c}(g)\sim Q
\right)=1.
\]

这是文章最强的 Q 恢复结论：掌握者正确概率可以未知。

## 属性分布一致性的额外条件

定义最终属性分布估计

\[
\widetilde{\boldsymbol p}_{\widehat c}(g)
=
\arg\inf_{\boldsymbol p}
\left\|
T_{\widehat c(\widehat Q,g),g}(\widehat Q)\boldsymbol p
+p_0\boldsymbol g_{\mathrm{joint}}
-\boldsymbol\alpha
\right\|_2.
\]

若一般估计量

\[
\widetilde{\boldsymbol c}(Q,\boldsymbol g)
\]

在真 Q 下也一致，则适当排列属性列后，

\[
\widetilde{\boldsymbol p}_{\widehat c}(g)
\overset{p}{\longrightarrow}
\boldsymbol p^*.
\]

## 为什么 Q 一致不要求全部 \(c_i\) 一致

Proposition 6.6 给出一个很强的结论：

\[
Q'\not\sim Q
\]

时，不论错误候选怎样选择

\[
\boldsymbol c'\in[0,1]^m,
\]

它的增广列空间都无法包含真总体矩。

因此只要真 Q 对应的组合估计能把损失压到 0，错误 Q 即使带着不一致的 \(\boldsymbol c'\) 也无法追上。

## 为什么 \(\boldsymbol p\) 一致需要 \(c\) 一致

给定 Q 后，\(\boldsymbol p\) 是通过

\[
\widetilde T_{c,g}(Q)\boldsymbol p_0
\]

反演出来的。若所用 \(\widehat{\boldsymbol c}\) 收敛到错误值，设计矩阵本身会收敛到错误矩阵；满列秩只能保证该错误矩阵下的解唯一，无法保证解等于真 \(\boldsymbol p^*\)。

## 一个不可识别维数例

原文 Remark 4.1 取

\[
Q=I_k.
\]

\(k\) 道二元题的联合分布有

\[
2^k-1
\]

个自由度，而 \((\boldsymbol p^*,\boldsymbol c)\) 的参数维数是

\[
(2^k-1)+k.
\]

仅靠该反应表无法一般地同时识别 \(\boldsymbol p^*\) 和 \(\boldsymbol c\)。额外结构、参数模型或先验信息可能提供帮助。

[下一页：全部证明的总路线](15-proof-roadmap.md)
