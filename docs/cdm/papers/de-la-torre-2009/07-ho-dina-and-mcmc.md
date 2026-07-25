# HO-DINA 与 MCMC

## 饱和属性分布的瓶颈

\(K\) 个二元属性产生

\[
2^K-1
\]

个自由模式概率：

| \(K\) | 模式数 \(2^K\) | 自由比例参数 |
| ---: | ---: | ---: |
| 5 | 32 | 31 |
| 10 | 1,024 | 1,023 |
| 20 | 1,048,576 | 1,048,575 |

EM 的 E 步还需要为每名学生存储或计算所有模式后验。

## 高阶能力

HO-DINA 引入

\[
\theta_i\sim N(0,1),
\]

把它解释为某领域的一般能力。给定 \(\theta_i\) 后，各属性条件独立：

\[
P(\boldsymbol\alpha_i\mid\theta_i)
=
\prod_{k=1}^{K}
P(\alpha_{ik}\mid\theta_i).
\]

属性掌握概率为

\[
p_k(\theta_i)
=
P(\alpha_{ik}=1\mid\theta_i)
=
\frac{
\exp(\lambda_{0k}+\lambda_1\theta_i)
}{
1+\exp(\lambda_{0k}+\lambda_1\theta_i)
}.
\tag{18}
\]

完整 Bernoulli 概率写成

\[
P(\boldsymbol\alpha_i\mid\theta_i)
=
\prod_{k=1}^{K}
p_k(\theta_i)^{\alpha_{ik}}
\left[
1-p_k(\theta_i)
\right]^{1-\alpha_{ik}}.
\tag{19}
\]

原文 Equation 6 用 \(P(\alpha_k\mid\theta)\) 的简写表达这一层；式 (19) 把二元状态补全。

## 参数减少

论文采用：

- 每个属性一个截距 \(\lambda_{0k}\)；
- 所有属性共享一个正斜率 \(\lambda_1>0\)。

属性分布参数总数为

\[
K+1.
\]

正斜率保证一般能力越高，掌握各属性的概率越大。

## 属性为什么会相关

条件于 \(\theta\) 时属性独立；边际化 \(\theta\) 后，它们共享同一连续来源：

\[
P(\boldsymbol\alpha)
=
\int
P(\boldsymbol\alpha\mid\theta)
\phi(\theta)\,d\theta.
\]

因此属性之间产生正向依赖。

## 与 DINA 观测层的组合

HO-DINA 只改变属性模式分布。题目反应层仍是：

\[
\eta_{ij}
=
\prod_k\alpha_{ik}^{q_{jk}},
\]

\[
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=
g_j^{1-\eta_{ij}}
(1-s_j)^{\eta_{ij}}.
\]

所以 DINA 与 HO-DINA 的 “DINA” 部分相同，差别位于 \(P(\boldsymbol\alpha)\)。

## MCMC 在本文中的角色

论文说明：

- HO-DINA 参数使用 MCMC；
- 项目参数点估计用后验均值；
- 标准误用后验标准差；
- 可靠性证据来自 de la Torre and Douglas (2004)。

本文没有给出：

- 完整条件分布；
- 先验超参数；
- 链长、burn-in、thin；
- 收敛诊断；
- MCMC 伪代码。

因此，只靠这篇 2009 论文无法逐行重建原 MCMC 实现。完整代码精读需要同时进入 2004 HO-DINA 论文或后续公开软件。

## 建模权衡

| 饱和 DINA | HO-DINA |
| --- | --- |
| 任意属性模式分布 | 单一高阶能力诱导依赖 |
| \(2^K-1\) 个比例参数 | \(K+1\) 个高阶参数 |
| 小 \(K\) 时灵活 | 大 \(K\) 时更紧凑 |
| EM 有闭式项目参数更新 | 论文使用 MCMC |
| 能表示复杂或负向依赖 | 共享正斜率主要表达正向依赖 |

Table 4 中两者项目参数接近，只能说明 HO 约束对该分数减法数据较为合理；它没有建立对所有 CDM 数据的普遍等价。
