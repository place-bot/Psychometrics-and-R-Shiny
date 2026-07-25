# 参考文献与来源边界

## 主论文

de la Torre, J. (2008). An empirically based method of Q-matrix validation for the DINA model: Development and applications. *Journal of Educational Measurement, 45*(4), 343--362. [DOI](https://doi.org/10.1111/j.1745-3984.2008.00069.x) · [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/j.1745-3984.2008.00069.x)

本站关于 sequential EM-based \(\delta\)-method、Tables 1--9、Figures 1--7、模拟、分数减法、NAEP、结论和原文未来工作的数字，均以 Wiley 正式全文为主。

## DINA 与数据来源

Junker, B. W., & Sijtsma, K. (2001). Cognitive assessment models with few assumptions, and connections with nonparametric item response theory. *Applied Psychological Measurement, 25*(3), 258--272. [DOI](https://doi.org/10.1177/01466210122032064)

Tatsuoka, K. K. (1990). Toward an integration of item-response theory and cognitive error diagnosis. In N. Frederiksen, R. Glaser, A. Lesgold, & M. G. Shafto (Eds.), *Diagnostic Monitoring of Skill and Knowledge Acquisition* (pp. 453--488). Erlbaum.

Mislevy, R. J. (1996). Test theory reconceived. *Journal of Educational Measurement, 33*(4), 379--416. [DOI](https://doi.org/10.1111/j.1745-3984.1996.tb00498.x)

de la Torre, J., & Douglas, J. A. (2004). Higher-order latent trait models for cognitive diagnosis. *Psychometrika, 69*(3), 333--353. [DOI](https://doi.org/10.1007/BF02295640)

## 后续 Q 验证

de la Torre, J., & Chiu, C.-Y. (2016). A general method of empirical Q-matrix validation. *Psychometrika, 81*(2), 253--273. [DOI](https://doi.org/10.1007/s11336-015-9467-8)

Chiu, C.-Y. (2013). Statistical refinement of the Q-matrix in cognitive diagnosis. *Applied Psychological Measurement, 37*(8), 598--618. [DOI](https://doi.org/10.1177/0146621613488436)

Liu, J., Xu, G., & Ying, Z. (2012). Data-driven learning of Q-matrix. *Applied Psychological Measurement, 36*(7), 548--564. [DOI](https://doi.org/10.1177/0146621612456591)

## 公开软件实现

Robitzsch, A., Kiefer, T., George, A. C., & Uenlue, A. `CDM`: Cognitive Diagnosis Modeling. [CRAN](https://cran.r-project.org/package=CDM) · [GitHub](https://github.com/alexanderrobitzsch/CDM)

重点源码：

- [`R/din.validate.qmatrix.R`](https://github.com/alexanderrobitzsch/CDM/blob/master/R/din.validate.qmatrix.R)
- [`src/cdm_rcpp_din_validate.cpp`](https://github.com/alexanderrobitzsch/CDM/blob/master/src/cdm_rcpp_din_validate.cpp)

该实现使用 de la Torre (2008) 的 EM expected-count 与 \(1-s-g\) 思想，当前函数穷举全部非零 q-vector；它与原文顺序搜索的路径和阈值含义不同。

## 本站计算材料

[`tools/de_la_torre_2008_q_validation.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/de_la_torre_2008_q_validation.py)

该脚本由本站编写，用于核对假想题、候选参数、顺序搜索、穷举搜索与 Table 4 条件。它不属于作者 Ox 代码。

## 数据与复现边界

本站没有重新发布分数减法与 NAEP 个体反应数据，也没有声称重新计算原文真实数据结果。真实数据页面整理的是原文报告的样本、算法设置、表格、图形数值和作者解释。

