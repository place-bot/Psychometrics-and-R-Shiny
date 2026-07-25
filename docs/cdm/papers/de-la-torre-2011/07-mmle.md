# MMLE 与 EM

## 边际似然

设 \(I\) 名学生、\(J\) 道题、\(L=2^K\) 个完整属性模式。学生 \(i\) 的反应向量为

\[
\boldsymbol X_i=(X_{i1},\ldots,X_{iJ}).
\]

给定属性模式 \(\boldsymbol\alpha_l\)，局部独立似然为

\[
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
=
\prod_{j=1}^{J}
P(\boldsymbol\alpha^*_{lj})^{X_{ij}}
\left[
1-P(\boldsymbol\alpha^*_{lj})
\right]^{1-X_{ij}}.
\]

边际似然把属性模式积分掉：

\[
L(\boldsymbol X)
=
\prod_{i=1}^{I}
\sum_{l=1}^{L}
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
p(\boldsymbol\alpha_l).
\]

论文最大化其对数，得到 marginal maximum likelihood estimates。

## E 步：完整模式后验

\[
\tau_{il}
=
P(\boldsymbol\alpha_l\mid\boldsymbol X_i)
=
\frac{
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
p(\boldsymbol\alpha_l)
}{
\sum_{l'=1}^{L}
L(\boldsymbol X_i\mid\boldsymbol\alpha_{l'})
p(\boldsymbol\alpha_{l'})
}.
\]

某个项目只关心约化模式 \(\boldsymbol a\)。因此把所有映射到 \(\boldsymbol a\) 的完整模式后验相加：

\[
\tau_{ij}(\boldsymbol a)
=
\sum_{l:
\boldsymbol\alpha^*_{lj}=\boldsymbol a}
\tau_{il}.
\]

## M 步：概率的闭式更新

论文定义

\[
I_{\boldsymbol a j}
=
\sum_{i=1}^{I}
\tau_{ij}(\boldsymbol a)
\]

为项目 \(j\) 约化组 \(\boldsymbol a\) 的期望人数，并定义

\[
R_{\boldsymbol a j}
=
\sum_{i=1}^{I}
\tau_{ij}(\boldsymbol a)X_{ij}
\]

为该组的期望答对人数。

于是

\[
\widehat P_j(\boldsymbol a)
=
\frac{
R_{\boldsymbol a j}
}{
I_{\boldsymbol a j}
}.
\]

这就是论文公式 (15)。

## 为什么更新很简单

在约化组内部，项目反应服从共享成功概率的 Bernoulli 模型。若组成员身份已知，MLE 就是答对比例；EM 用后验概率替代未知的组成员指示变量，因此得到期望答对数除以期望人数。

## 属性模式分布

饱和属性分布可以用

\[
\widehat p(\boldsymbol\alpha_l)
=
\frac{1}{I}
\sum_{i=1}^{I}\tau_{il}
\]

更新。论文也讨论在 \(K\) 很大时使用：

- higher-order latent trait；
- 属性层级；
- 其他结构化分布。

这些结构可减少 \(2^K\) 个模式概率带来的计算和样本量压力。

## 数值实现要点

直接连乘大量概率会下溢。代码通常使用

\[
\log L
=
\sum_j
\left[
X_{ij}\log P_{lj}
+(1-X_{ij})\log(1-P_{lj})
\right]
\]

并用 log-sum-exp 归一化后验。

还需处理：

- 概率贴近 0 或 1；
- 约化组期望人数过小；
- 多起点；
- 单调约束；
- 迭代上限和收敛准则。

## 与 2009 DINA EM 的关系

两篇论文使用相同 EM 逻辑。差异集中在每题 M 步：

| 模型 | 每题约化组 |
| --- | ---: |
| DINA | 2 |
| G-DINA | \(2^{K_j^*}\) |

G-DINA 保留更多组，因此能够发现属性主效应与交互，同时也需要更多数据。
