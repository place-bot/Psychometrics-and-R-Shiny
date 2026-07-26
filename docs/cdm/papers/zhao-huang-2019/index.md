# Zhao 与 Huang（2019）阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Shuai Zhao & Xiaoting Huang. *Automated Q-matrix Identification Using Text Classification Techniques* |
| 会议 | *Proceedings of the 11th International Conference on Education Technology and Computers*, 273--277 |
| DOI | [10.1145/3369255.3369308](https://doi.org/10.1145/3369255.3369308) |
| 会议时间 | 2019-10-28 至 2019-10-31，Amsterdam |
| ACM 记录 | [论文页面与 5 页 PDF](https://dl.acm.org/doi/10.1145/3369255.3369308)；ACM 页面标记为 Free access，页面记录的正式上线日期为 2020-01-21 |
| 数据 | 1,069 道三年级数学题；实验只使用其中属于两个高频属性的 805 道题 |
| 官方代码 | 论文没有给出仓库、数据下载地址或补充材料；截至 2026-07-26 未检索到作者公开实现 |
| 本站代码 | [数值审计](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_audit.py) · [泄漏安全的独立重构](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_reimplementation.py) |

## 一句话结论

这篇论文把题干文本经过中文分词、\(n\)-gram、信息增益选词和 TF--IDF 表示，再用 LR、线性 SVM 与 Gaussian NB 预测题目的认知属性；最佳结果为 NB 在 unigram+bigram+trigram 下的 85.2% accuracy 与 85.6% weighted F1。

该数字需要和实验边界同时阅读：

- 原始九属性 \(Q\) 矩阵被裁成两个互斥属性的分类问题；
- 805 道题中 666 道属于整数运算，多数类 accuracy 已有 82.7%；
- 最佳 accuracy 相对多数类基线提高约 2.5 个百分点；
- 10% 测试集很可能只有 81 道题，一道题约对应 1.24 个百分点；
- 论文打印的 weighted F1 公式使用预测类规模加权，与 scikit-learn 的真实类支持度加权定义存在差异。

## 这篇论文放在 Q 矩阵研究的哪个位置

```text
题干文本 + 少量专家标签
              │
              ▼
       文本监督分类器
              │
              ▼
   新题的属性标签 / Q 行初稿
              │
       ┌──────┴──────┐
       ▼             ▼
  专家复核       CDM 数据校准
       └──────┬──────┘
              ▼
         可用 Q 矩阵
```

论文处理的是**新题入库时的语义标注**。它没有使用学生反应数据，也没有估计 DINA、G-DINA 或其他 CDM，更没有进行 CAT 选题。

## 推荐阅读顺序

1. [研究问题、贡献与证据边界](01-question-contribution.md)
2. [CDM、Q 矩阵与文本分类的接口](02-cdm-q-context.md)
3. [原始数据：1,069 道题与九个属性](03-data-1069.md)
4. [实验裁剪：805 道题与两个互斥类别](04-binary-reduction.md)
5. [监督学习任务的数学表述](05-problem-formulation.md)
6. [三阶段框架总览](06-three-stage-framework.md)
7. [中文分词与 \(n\)-gram 特征](07-tokenization-ngrams.md)
8. [信息增益特征选择](08-information-gain.md)
9. [TF--IDF 题目向量](09-tfidf.md)
10. [C-SVM 的目标函数与实现歧义](10-svm.md)
11. [Gaussian Naive Bayes](11-naive-bayes.md)
12. [L2 Logistic Regression](12-logistic-regression.md)
13. [Experiment：数据划分、\(k\) 调参与算法选择](13-experiment-design.md)
14. [Experiment：accuracy 与 weighted F1](14-performance-measures.md)
15. [Experiment：Table 1 的 unigram 结果](15-results-unigram.md)
16. [Experiment：Table 2 的 unigram+bigram 结果](16-results-bigram.md)
17. [Experiment：Table 3 的 trigram 结果](17-results-trigram.md)
18. [关键词结果与教育语义解释](18-feature-interpretation.md)
19. [多数类基线与类别不平衡](19-imbalance-baselines.md)
20. [小测试集、分辨率与不确定性](20-finite-sample-uncertainty.md)
21. [Equation (9) 的 weighted F1 审计](21-f1-equation-audit.md)
22. [复现性审计：论文没有报告的实现选择](22-reproducibility-audit.md)
23. [独立代码重构：训练、验证、测试严格分离](23-independent-reimplementation.md)
24. [本站数值核验及其输出](24-computational-audit.md)
25. [文本分类与完整 Q 矩阵生成的差距](25-classification-vs-q-generation.md)
26. [与 CDM、CAT 和 RecCAT 的接口](26-cdm-cat-interface.md)
27. [局限、结论与未来工作](27-limitations-conclusion-future.md)
28. [符号表](28-symbol-table.md)
29. [参考文献与核验来源](references.md)

## 读完后应能回答

- 为什么 1,069×9 的原始 \(Q\) 最后变成 805×2？
- 论文的任务在什么条件下等价于二分类？
- \(n\)-gram、信息增益和 TF--IDF 分别承担什么职责？
- 为何特征选择对 NB 的影响远大于 LR 与 SVM？
- 85.2% accuracy 和 82.7% 多数类基线应如何比较？
- Equation (9) 与 scikit-learn weighted F1 有什么差别？
- 这篇论文能支持“自动生成完整多标签 \(Q\) 矩阵”到什么程度？
- 若把语义模型接入 CAT，哪些模块仍需学生逐题反应驱动？
