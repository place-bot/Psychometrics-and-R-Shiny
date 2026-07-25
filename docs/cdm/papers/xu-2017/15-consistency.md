# 从可识别性到一致性

## 经验边际向量

对 \(N\) 名独立被试，论文考虑全部题目子集的经验全对比例。记

\[
\widehat\gamma_{\boldsymbol r}
=
\frac1N\sum_{i=1}^N
\mathbb I(\boldsymbol R_i\succeq\boldsymbol r),
\qquad
\boldsymbol r\in\{0,1\}^J.
\]

把这些量按 \(T\)-矩阵行顺序排成

\[
\widehat{\boldsymbol\gamma}.
\]

大数定律给出

\[
\widehat{\boldsymbol\gamma}
\xrightarrow{\mathrm{a.s.}}
T(Q,\Theta)\boldsymbol p.
\]

## 最大似然估计的拟合

记 MLE 为

\[
(\widehat\Theta,\widehat{\boldsymbol p}).
\]

论文写出

\[
\left\|
\widehat{\boldsymbol\gamma}
-
T(Q,\widehat\Theta)
\widehat{\boldsymbol p}
\right\|_2
\longrightarrow0.
\]

结合经验边际收敛，得到

\[
\left\|
T(Q,\Theta)\boldsymbol p
-
T(Q,\widehat\Theta)
\widehat{\boldsymbol p}
\right\|_2
\longrightarrow0
\quad\mathrm{a.s.}
\]

## 可识别性关闭最后一步

如果总体映射一对一，任何产生同一极限边际的参数极限点都只能是
\((\Theta,\boldsymbol p)\)。因此主定理支持

\[
(\widehat\Theta,\widehat{\boldsymbol p})
\xrightarrow{\mathrm{a.s.}}
(\Theta,\boldsymbol p).
\]

这个逻辑链是：

\[
\text{经验分布收敛}
\;+\;
\text{MLE 拟合经验分布}
\;+\;
\text{总体参数唯一}
\Longrightarrow
\text{参数一致}.
\]

## 渐近正态性

论文随后简要指出：在标准正则条件下，对真参数处的 log-likelihood 作 Taylor 展开，再结合中心极限定理，可以得到 MLE 的渐近正态性。

原文没有在此处单列正式定理、信息矩阵公式或完整正则条件。因此阅读时应把两层证据分开：

- strict identifiability 有完整定理与详细证明；
- consistency 与 asymptotic normality 作为定理后的大样本推论进行说明。

## 边界与非正则点

论文假设

\[
p_{\boldsymbol\alpha}>0
\quad\forall\boldsymbol\alpha.
\]

若某些类比例为零，或项目参数位于等值/边界位置：

- Fisher information 可能奇异；
- 通常的 \(\sqrt N\) 渐近正态性可能失效；
- 原定理证明中依赖正质量的严格不等式需要重做；
- 潜在结构本身可能发生变化。

## 有限样本含义

一致性描述 \(N\to\infty\)。它没有给出以下保证：

- 某个 \(N\) 下偏差有多大；
- 罕见属性类能否稳定估计；
- EM 是否找到全局 MLE；
- 接近 C2 失效时标准误是否可接受；
- 自适应抽题产生的非均匀题目覆盖是否满足同一收敛条件。

实际分析仍需检查多起点稳定性、信息矩阵、类比例、参数边界和题目覆盖。
