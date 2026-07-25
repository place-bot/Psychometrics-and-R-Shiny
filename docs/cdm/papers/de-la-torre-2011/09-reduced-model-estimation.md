# 约化模型与权重矩阵

## 为什么需要权重

饱和 G-DINA 给出 \(2^{K_j^*}\) 个概率，但约化模型只有 \(P\) 个参数：

\[
2^{K_j^*}>P.
\]

多个约化模式需要共同决定较少的参数。如果不同模式的后验人数差异很大，直接等权拟合会让稀少模式获得过大影响。

## 权重矩阵

论文使用约化组期望人数：

\[
W_j
=
\operatorname{diag}
\left(
I_{\boldsymbol\alpha^*_{1j}},
\ldots,
I_{\boldsymbol\alpha^*_{2^{K_j^*}j}}
\right).
\]

identity-link 约化模型的加权最小二乘估计为

\[
\widehat{\boldsymbol\delta}_j
=
\left[
(M_j^{(r)})^\top
W_j
M_j^{(r)}
\right]^{-1}
(M_j^{(r)})^\top
W_j
\widehat{\boldsymbol P}_j.
\]

## 论文定义的特殊约化类

令 \(M_j^{(r-)}\) 表示去掉截距列后的 design matrix。若

\[
(M_j^{(r-)})^\top
M_j^{(r-)}
\]

是对角矩阵，论文称该模型属于一个特殊约化类。

所有两参数分组模型都满足这个条件，包括：

- DINA；
- DINO；
- multiple-strategy DINA。

按照“掌握属性数量”合并组的某些模型也满足。

## 分组均值解释

这个特殊类将 \(2^{K_j^*}\) 个模式分成 \(P\) 个互不重叠的组 \(g_{jp}\)。组成功概率的 MLE 为

\[
\widehat P(g_{jp})
=
\frac{
\sum_{\boldsymbol a\in g_{jp}}
R_{\boldsymbol a j}
}{
\sum_{\boldsymbol a\in g_{jp}}
I_{\boldsymbol a j}
}.
\]

也可以写成饱和概率的后验人数加权均值：

\[
\widehat P(g_{jp})
=
\frac{
\sum_{\boldsymbol a\in g_{jp}}
I_{\boldsymbol a j}
\widehat P_j(\boldsymbol a)
}{
\sum_{\boldsymbol a\in g_{jp}}
I_{\boldsymbol a j}
}.
\]

论文证明这与上面的加权最小二乘结果一致，因此属于 MLE。

## A-CDM 为什么需要额外处理

A-CDM 的主效应列彼此不正交，一名掌握多个属性的学生会同时贡献给多列，因此它不属于论文定义的特殊约化类。

论文建议给定 \(W_j\) 与 \(\widehat{\boldsymbol P}_j\)，逐题使用带概率边界的数值优化估计：

\[
0\leq M_j^{(r)}\boldsymbol\delta_j\leq1.
\]

LLM 与 G-NIDA/R-RUM 也需要相应 link 下的优化。

## 两步估计的性质边界

论文明确指出：

- 饱和模型变换得到的是 MLE；
- 特殊约化类的加权估计也是 MLE；
- 特殊类之外的逐题两步估计，其渐近性质在当时尚未建立。

因此，计算方便不能自动转化为严格的最大似然保证。

## 逐题拟合的收益

若有 \(J^*\) 道多属性题、\(m\) 个候选约化模型，整测验重新拟合需要大量全数据估计。两步框架先拟合一次饱和模型，随后只进行

\[
J^*\times m
\]

个项目参数层计算，显著降低探索混合模型组合的成本。
