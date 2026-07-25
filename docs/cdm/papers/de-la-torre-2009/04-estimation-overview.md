# 三种估计路线

## Joint Maximum Likelihood

联合极大似然同时优化：

\[
\boldsymbol\beta
=(g_1,s_1,\ldots,g_J,s_J)
\]

和每名学生的离散属性模式

\[
\boldsymbol\alpha_1,\ldots,\boldsymbol\alpha_I.
\]

目标为条件似然

\[
L(X\mid\boldsymbol\alpha)
=
\prod_i
L(\boldsymbol X_i\mid\boldsymbol\alpha_i).
\]

论文指出，学生属性模式属于随样本量增加而增加的 incidental parameters。和传统 IRT 的 JML 类似，联合估计可能导致结构参数 \(\widehat{\boldsymbol\beta}\) 不一致。

## Marginal Maximum Likelihood 与 EM

边际极大似然把属性模式积分掉：

\[
L(X)
=
\prod_i
\sum_l
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
\pi_l.
\]

因为属性分布是离散的，积分变成对 \(2^K\) 个模式求和。

EM 交替：

- E 步：计算每名学生属于每个属性模式的后验概率；
- M 步：用后验期望计数更新 \(g_j,s_j\)。

附录完整推导了这条路线。

## 饱和属性分布

若给每个属性模式独立概率：

\[
\boldsymbol\pi=(\pi_1,\ldots,\pi_{2^K}),
\qquad
\sum_l\pi_l=1,
\]

自由参数数为

\[
2^K-1.
\]

它能表示任意属性依赖，但计算和存储都随 \(K\) 指数增长。

本文的 EM 使用固定的 \(\pi_l\)。讨论部分提出可以在每次迭代中用经验 Bayes 更新模式比例。

## HO-DINA 与 MCMC

HO-DINA 用一个连续高阶能力 \(\theta_i\) 解释属性间依赖：

\[
P(\alpha_{ik}=1\mid\theta_i)
=
\operatorname{logit}^{-1}
(\lambda_{0k}+\lambda_1\theta_i),
\qquad
\theta_i\sim N(0,1).
\]

属性分布从 \(2^K-1\) 个自由模式概率降到：

\[
K\text{ 个截距}+1\text{ 个共同斜率}.
\]

论文说明该模型用 MCMC 估计，并把采样器细节指向 de la Torre and Douglas (2004)。

## 三条路线对照

| 路线 | 属性模式处理 | 优点 | 主要代价 |
| --- | --- | --- | --- |
| JML | 每人直接估一个模式 | 概念直接 | incidental parameter 问题 |
| MML + EM | 对 \(2^K\) 模式求和 | 附录有闭式 M 步 | 指数级类别数 |
| HO-DINA + MCMC | 用 \(\theta\) 生成相关属性 | 参数量随 \(K\) 线性增长 | 增加高阶结构假设；采样细节在另一篇论文 |

## 真实数据比较时还有两处差别

论文强调 DINA-EM 与 HO-DINA-MCMC 的结果无需逐项完全相同：

1. DINA 使用饱和多项属性分布，HO-DINA 使用高阶能力约束；
2. DINA 报告似然众数/极大值，HO-DINA 报告后验均值。

所以 Table 4 同时比较了潜变量结构和点估计准则。
