# 参考文献与来源核对

## 核心论文

Liu, J., Xu, G., & Ying, Z. (2013). Theory of self-learning Q-matrix. *Bernoulli, 19*(5A), 1790--1817. [DOI](https://doi.org/10.3150/12-BEJ430) · [PubMed Central 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC4011940/) · [arXiv](https://arxiv.org/abs/1010.6120)

本站按 28 页发表版电子重印核验了：

- 题名、作者、卷期、页码与 DOI；
- Sections 2--4 的全部模型、估计量与定理；
- Section 5 的结论与未来工作；
- Section 6 的 Propositions 6.1--6.6、Lemma 6.7 和三个定理证明；
- Appendix 中 Propositions 6.3--6.4 的技术证明；
- 原文没有实验、数据集、图表与代码入口这一证据边界。

## 直接相关论文

Liu, J., Xu, G., & Ying, Z. (2012). Data-driven learning of Q-matrix. *Applied Psychological Measurement, 36*(7), 548--564. [DOI](https://doi.org/10.1177/0146621612456591) · [本站精读](../liu-xu-ying-2012/index.md)

Chiu, C.-Y., Douglas, J. A., & Li, X. (2009). Cluster analysis for cognitive diagnosis: Theory and applications. *Psychometrika, 74*, 633--665. [DOI](https://doi.org/10.1007/s11336-009-9125-0)

de la Torre, J. (2008). An empirically based method of Q-matrix validation for the DINA model: Development and applications. *Journal of Educational Measurement, 45*(4), 343--362. [DOI](https://doi.org/10.1111/j.1745-3984.2008.00069.x) · [本站精读](../de-la-torre-2008/index.md)

Junker, B. W., & Sijtsma, K. (2001). Cognitive assessment models with few assumptions, and connections with nonparametric item response theory. *Applied Psychological Measurement, 25*(3), 258--272. [DOI](https://doi.org/10.1177/01466210122032064)

Rupp, A. A., Templin, J. L., & Henson, R. A. (2010). *Diagnostic Measurement: Theory, Methods, and Applications*. Guilford Press.

Tatsuoka, K. K. (2009). *Cognitive Assessment: An Introduction to the Rule Space Method*. Routledge.

## 本站实现

独立教学脚本：

[`tools/liu_xu_ying_2013_theory_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/liu_xu_ying_2013_theory_check.py)

实现使用 NumPy 与 SciPy，覆盖：

- 理想反应与饱和 T-matrix；
- 经验联合正响应矩；
- 单纯形约束剖面优化；
- Q 列置换等价类；
- Proposition 6.6 的显式容斥矩阵 D；
- 小规模总体分离枚举；
- C4 失败反例；
- 固定种子的有限样本演示。

脚本由本站独立编写。原论文没有发布源码，本站数值结果也没有归入论文原始证据。
