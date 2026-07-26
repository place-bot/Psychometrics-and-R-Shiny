# Propositions 6.3--6.6：列空间分离

## 目标命题

作者希望建立：

\[
Q'\not\sim Q
\quad\Longrightarrow\quad
T_c(Q)\boldsymbol p^*
\notin
\mathcal C(T_{c'}(Q'))
\]

对所有候选 \(\boldsymbol c'\) 成立。

它比“某个固定 \(\boldsymbol c'\) 拟合失败”更强，因为错误 Q 连调整行缩放参数也无法复制真矩。

## 先固定真 Q 的锚题

由完整性，不失一般性可设

\[
Q_{1:k}=I_k.
\]

对错误候选 \(Q'\)，前 \(k\) 行只有两种情况：

1. \(Q'_{1:k}\) 完整；
2. \(Q'_{1:k}\) 不完整。

这两类穷尽全部候选。

## Proposition 6.3：候选锚块完整

若 \(Q'_{1:k}\) 完整，可重排候选属性列，使

\[
Q'_{1:k}=I_k=Q_{1:k}.
\]

若 \(Q'\ne Q\)，差异一定出现在后续某一道题。论文证明，在 Theorem 4.2 的条件下，对任意 \(\boldsymbol c'\in\mathbb R^m\)，

\[
T_c(Q)\boldsymbol p^*
\notin
\mathcal C(T_{c'}(Q')).
\]

直觉上，候选 Q 会把某道后续题的属性要求与某个锚题组合错误地视为相同。候选 \(T\)-matrix 中相应两行具有固定比例；真模型中由于存在 C4 保证的区分人群，两行达不到该比例。

## Proposition 6.4：候选锚块不完整

若 \(Q'_{1:k}\) 不完整，则可能出现：

- 两个候选锚题拥有相同 q-vector；
- 某个候选锚题同时要求多个属性；
- 若干多属性行之间形成覆盖关系。

附录逐类证明，总能找到一对或一组三行，使错误候选列空间必须满足某个固定比例关系，而真矩因完全多样化人群而违反该关系。

结论同样是

\[
T_c(Q)\boldsymbol p^*
\notin
\mathcal C(T_{c'}(Q')).
\]

## Corollary 6.5

Propositions 6.3 与 6.4 合并后覆盖所有 \(Q'\not\sim Q\)。原文写成：

\[
T_c(Q)\boldsymbol p^*
\notin
\mathcal C(T_{c'}(Q'))
\]

对所有候选 \(\boldsymbol c'\in[0,1]^m\) 成立。

无噪声情形令

\[
\boldsymbol c=\boldsymbol1,
\qquad
\boldsymbol g=\boldsymbol0
\]

即可使用这条结论。

## Proposition 6.6：加入猜测

定义完整模式分布

\[
\boldsymbol p_0^*
=
\begin{pmatrix}
p_{\boldsymbol0}^*\\
\boldsymbol p^*
\end{pmatrix}
\]

和增广矩阵

\[
\widetilde T_{c,g}(Q)
=
\begin{pmatrix}
\boldsymbol g_{\mathrm{joint}}&T_{c,g}(Q)\\
1&\boldsymbol E
\end{pmatrix}.
\]

若 Q 完整、T 饱和、\(Q'\not\sim Q\)、每个 \(c_i\ne g_i\)，并满足 Theorem 4.2 的其余条件，则对全部 \(\boldsymbol c'\in[0,1]^m\)，

\[
\widetilde T_{c,g}(Q)\boldsymbol p_0^*
\notin
\mathcal C\!\left(
\widetilde T_{c',g}(Q')
\right).
\]

此外，

\[
\widetilde T_{c,g}(Q)
\]

满列秩。

## “任意 \(c'\)”为何重要

在未知 \(\boldsymbol c\) 的估计中，每个错误候选 Q 都会选择最有利于自己的

\[
\widehat{\boldsymbol c}(Q',\boldsymbol g).
\]

若分离只对真 \(\boldsymbol c\) 成立，错误 Q 可能通过改变 \(\boldsymbol c'\) 消除距离。Proposition 6.6 排除了整个紧参数集合 \([0,1]^m\)。

## 从集合排除到正距离

\(\mathcal C(\widetilde T)\) 是闭线性子空间。真矩不属于它，因此对固定错误 \(Q'\) 与 \(\boldsymbol c'\)，距离严格为正。

再利用：

- \(\boldsymbol c'\mapsto\widetilde T_{c',g}(Q')\) 连续；
- \([0,1]^m\) 紧；
- 候选 Q 数量有限；

可得到对全部错误候选统一的正分离间隔。这一步把线性代数识别结论转成统计一致性。

[下一页：消去猜测的矩阵 \(D\)](18-guessing-removal-transform.md)
