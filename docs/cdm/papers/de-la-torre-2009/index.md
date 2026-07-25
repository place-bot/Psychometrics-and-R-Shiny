# de la Torre (2009) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jimmy de la Torre. *DINA Model and Parameter Estimation: A Didactic*. |
| 期刊 | *Journal of Educational and Behavioral Statistics*, 34(1), 115--130, 2009 |
| DOI | [10.3102/1076998607309474](https://doi.org/10.3102/1076998607309474) |
| 出版商页面 | [SAGE Journals](https://journals.sagepub.com/doi/10.3102/1076998607309474) |
| 原文 PDF | [Carnegie Mellon University 课程存档](https://www.stat.cmu.edu/~brian/PIER-methods/For%202013-03-04/Readings/de%20la%20Torre-dina-est-115-30-jebs.pdf) |
| 论文类型 | 教学性模型论文；包含公式推导、模拟研究和真实数据分析 |
| 原始实现 | 作者用 Ox 编写 EM 程序；论文说明代码可向作者索取，没有给出公开仓库 |

这篇论文完成了 DINA 入门中最关键的一次闭环：

\[
\text{属性与 Q 矩阵}
\longrightarrow
\text{理想反应}
\longrightarrow
\text{guess/slip 观测模型}
\longrightarrow
\text{边际似然}
\longrightarrow
\text{EM 估计与标准误}.
\]

论文还介绍 HO-DINA 的高阶属性分布和 MCMC 估计，并用模拟数据与分数减法数据比较估计结果。

## 一句话主线

对每个学生 \(i\) 和题目 \(j\)，先由

\[
\eta_{ij}
=
\prod_{k=1}^{K}
\alpha_{ik}^{q_{jk}}
\]

判断学生是否掌握该题要求的全部属性，再用

\[
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=
g_j^{1-\eta_{ij}}
(1-s_j)^{\eta_{ij}}
\]

允许未达到理想状态的学生猜对、达到理想状态的学生失误。EM 在全部 \(2^K\) 个属性模式上计算后验权重，然后用期望答对人数更新 \(g_j,s_j\)。

## 推荐阅读顺序

1. [问题、对象与模型假设](01-problem-and-model.md)：CDM 为什么提供属性画像，DINA 需要哪些输入。
2. [Q 矩阵与理想反应](02-q-matrix-and-ideal-response.md)：逐字母解释 \(\alpha,q,\eta\) 和 AND gate。
3. [反应概率与似然](03-response-function-and-likelihood.md)：guess、slip、局部独立、条件似然与边际似然。
4. [三种估计路线](04-estimation-overview.md)：JML、边际 ML/EM、HO-DINA/MCMC 的差别。
5. [EM 完整推导](05-em-algorithm.md)：E 步、期望计数、A10--A11 闭式更新和复杂度。
6. [标准误与分类](06-standard-errors-and-classification.md)：Appendix A12--A15、观测信息矩阵与后验属性模式。
7. [HO-DINA 与 MCMC](07-ho-dina-and-mcmc.md)：高阶能力、属性依赖、参数降维和论文证据边界。
8. [模拟实验](08-simulation.md)：完整实验设计、Q 矩阵、运行设置和 Table 2 结果。
9. [分数减法真实数据](09-fraction-subtraction.md)：2,144 名学生、15 题、Table 3--4 和结果解释。
10. [代码实现精读](10-code-implementation.md)：原始 Ox 实现状态与本站 EM 复现脚本逐段映射。
11. [手算一个 EM 的 E 步](11-worked-example.md)：\(K=2\) 时逐类计算似然、后验与 MAP 属性模式。
12. [限制与未来工作](12-limitations-and-future.md)：固定 Q、指数复杂度、固定先验和分类研究问题。
13. [符号表](13-symbols.md)：统一查询全文符号、维度和代码对象。
14. [总结与后续阅读](14-summary.md)：论文贡献、结论强度以及通向 G-DINA 的路线。
15. [参考文献](references.md)：原文和直接相关来源。

## 论文真正提供了哪些算法细节

| 部分 | 本文详细程度 |
| --- | --- |
| DINA EM | 附录完整推导参数更新和标准误 |
| 饱和属性模式分布 | 给出 \(2^K\) 类的边际化形式 |
| HO-DINA | 给出高阶属性分布和参数数量 |
| MCMC | 说明用途并引用 de la Torre & Douglas (2004)，本文没有重写采样器 |
| Ox 程序 | 说明可向作者索取；论文没有公开下载地址 |

本站不会用后续软件替代原文算法。`tools/de_la_torre_2009_dina_em.py` 按附录写成可运行的教学实现，并明确列出与原始 Ox 代码的差别。
