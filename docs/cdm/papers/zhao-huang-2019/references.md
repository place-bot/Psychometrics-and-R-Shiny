# 参考文献与核验来源

## 原论文

- Zhao, S., & Huang, X. (2019). Automated Q-matrix identification using text classification techniques. In *Proceedings of the 11th International Conference on Education Technology and Computers* (pp. 273--277). ACM. [DOI](https://doi.org/10.1145/3369255.3369308) · [ACM 页面](https://dl.acm.org/doi/10.1145/3369255.3369308) · [DBLP](https://dblp.org/rec/conf/icetc/ZhaoH19)

书目信息按会议年份 2019 记录。ACM 页面同时显示会议日期 2019-10-28 至 2019-10-31，以及页面正式上线日期 2020-01-21。

## 原文参考文献

1. Frederiksen, N., Mislevy, R. J., & Bejar, I. I. (1993). *Test Theory for a New Generation of Tests*. Lawrence Erlbaum Associates.
2. Nichols, P. D., Chipman, S. F., & Brennan, R. L. (1995). *Cognitively Diagnostic Assessment*. Routledge.
3. Templin, J., & Bradshaw, L. (2013). Measuring the reliability of diagnostic classification model examinee estimates. *Journal of Classification, 30*(2), 251--275. [DOI](https://doi.org/10.1007/s00357-013-9129-4)
4. von Davier, M., Cheng, Y., & Cheng, Y. (2014). Multistage testing using diagnostic models. In *Computerized Multistage Testing* (pp. 219--227).
5. Junker, B. W., & Sijtsma, K. (2001). Cognitive assessment models with few assumptions, and connections with nonparametric item response theory. *Applied Psychological Measurement, 25*(3), 258--272.
6. Huebner, A. (2010). An overview of recent developments in cognitive diagnostic computer adaptive assessments. *Practical Assessment, Research & Evaluation, 15*(3).
7. de la Torre, J., & Minchen, N. (2014). Cognitively diagnostic assessments and the cognitive diagnosis model framework. *Psicología Educativa, 20*(2), 89--97.
8. Gierl, M. J., Lai, H., & Turner, S. R. (2012). Using automatic item generation to create multiple-choice test items. *Medical Education, 46*(8), 757--765.
9. Liu, Y., Yang, C., & Ma, W. (2009). Automatic pronunciation scoring for Mandarin proficiency test based on speech recognition. In *2009 International Symposium on Intelligent Ubiquitous Computing and Education* (pp. 168--171).
10. Li, S., Zhao, Z., Hu, R., Li, W., Liu, T., & Du, X. (2018). Analogical reasoning on Chinese morphological and semantic relations. [arXiv:1805.06504](https://arxiv.org/abs/1805.06504)
11. Forman, G. (2003). An extensive empirical study of feature selection metrics for text classification. *Journal of Machine Learning Research, 3*, 1289--1305.
12. Kim, H., Howland, P., & Park, H. (2005). Dimension reduction in text classification with support vector machines. *Journal of Machine Learning Research, 6*, 37--53.
13. Ting, S. L., Ip, W. H., & Tsang, A. H. C. (2011). Is Naive Bayes a good classifier for document classification? *International Journal of Software Engineering and Its Applications, 5*(3), 37--46.
14. Yang, Y., Zhang, J., & Kisiel, B. (2003). A scalability analysis of classifiers in text categorization. In *Proceedings of SIGIR 2003* (pp. 96--103).
15. Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825--2830.
16. Ng, A. Y., & Jordan, M. I. (2002). On discriminative vs. generative classifiers: A comparison of logistic regression and naive Bayes. In *Advances in Neural Information Processing Systems*.
17. Tjoe, H., & de la Torre, J. (2014). The identification and validation process of proportional reasoning attributes: An application of a cognitive diagnosis modeling framework. *Mathematics Education Research Journal, 26*(2), 237--255.
18. Mukhlash, I., Arham, A. Z., Rozi, F., Kimura, M., & Adzkiya, D. (2018). Opinion mining on book review using convolutional neural network algorithm--Long short term memory. *International Journal of Machine Learning and Computing, 8*(5), 437--441.

## 本站复现与审计

- [数值审计脚本](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_audit.py)
- [三阶段管线独立重构](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_reimplementation.py)
- [scikit-learn F1 文档](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
- [scikit-learn TF--IDF 文档](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn mutual information 文档](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_classif.html)

## 来源边界

- Tables 1--3、Figure 1、Figure 2、公式与作者结论均来自正式 PDF；
- 多数类基线、Wilson 区间、相容混淆表和 Equation (9) 比较来自本站计算；
- 没有公开数据和作者源码，本站没有声称逐数值复现分类结果。
