# 逐题 Wald 检验

## 检验目标

先拟合饱和 G-DINA，再对项目 \(j\) 检验约化模型 \(r\) 的等式约束：

\[
H_0:
R_{jr}
f(\boldsymbol P_j)
=
\boldsymbol 0.
\]

\(f(\boldsymbol P_j)\) 可以是概率本身，也可以是 identity、logit 或 log 标度上的效应参数。

## Wald 统计量

\[
\begin{aligned}
W
=\;&
\left[
R_{jr}f(\widehat{\boldsymbol P}_j)
\right]^\top\\
&\times
\left\{
R_{jr}
\widehat{\operatorname{Var}}
\left[
f(\widehat{\boldsymbol P}_j)
\right]
R_{jr}^\top
\right\}^{-1}\\
&\times
\left[
R_{jr}f(\widehat{\boldsymbol P}_j)
\right].
\end{aligned}
\]

若约化模型有 \(p\) 个自由参数，则渐近分布为

\[
W
\overset{a}{\sim}
\chi^2_{2^{K_j^*}-p}.
\]

## 两属性题的约束

### DINA

\[
P_{00}=P_{10}=P_{01}.
\]

可以写成

\[
R_{\mathrm{DINA}}
\boldsymbol P
=
\begin{pmatrix}
1&-1&0&0\\
0&1&-1&0
\end{pmatrix}
\begin{pmatrix}
P_{00}\\P_{10}\\P_{01}\\P_{11}
\end{pmatrix}
=
\boldsymbol0.
\]

自由度为

\[
4-2=2.
\]

### A-CDM

\[
\delta_{12}=0,
\]

等价于

\[
P_{11}-P_{10}-P_{01}+P_{00}=0.
\]

自由度为

\[
4-3=1.
\]

## 计算上的重要优势

论文的 Wald test 不要求重新估计约化模型。只需：

1. 饱和模型的 \(\widehat{\boldsymbol P}_j\)；
2. 相应协方差矩阵；
3. 约化模型的限制矩阵 \(R_{jr}\)。

因此可以高效地对每道题比较多个候选模型。

## 统计决策的含义

- 未拒绝 \(H_0\)：数据没有显示该约化约束造成显著损失；
- 拒绝 \(H_0\)：饱和模型中至少一个被约束方向与约化模型明显不符。

未拒绝不能证明认知过程必然等于该简洁模型。样本量小、模式稀疏或协方差估计不稳定都可能降低检验力。

## 多重比较

若对多道题和多个模型反复检验，原始显著性水平会累积 Type I error。论文在讨论中建议研究：

- Bonferroni 等多重比较校正；
- AIC 等兼顾复杂度与拟合的指标；
- 项目层和测验层的联合决策。

后续 `GDINA` 软件的 `modelcomp()` 已加入 Holm、Bonferroni、BH、BY 等调整方法，也提供 Wald、LR 和 LM 路线。这些是后续软件扩展，不能倒推为 2011 年论文已经验证的内容。
