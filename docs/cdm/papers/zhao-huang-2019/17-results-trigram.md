# Experiment：Table 3 的 trigram 结果

## 1. 完整结果

| 模型 | IG top-\(k\) accuracy | IG top-\(k\) F1 | 全特征 accuracy | 全特征 F1 |
| --- | ---: | ---: | ---: | ---: |
| LR | 75.3% | 73.1% | 72.5% | 69.4% |
| SVM | 74.9% | 72.0% | 71.3% | 68.3% |
| NB | **85.2%** | **85.6%** | 68.9% | 67.2% |

## 2. 特征选择增益

| 模型 | accuracy 增益 | F1 增益 |
| --- | ---: | ---: |
| LR | +2.8 pp | +3.7 pp |
| SVM | +3.6 pp | +3.7 pp |
| NB | **+16.3 pp** | **+18.4 pp** |

## 3. 三种 \(n\)-gram 下的最佳模型

| 特征范围 | 最佳模型 | accuracy | F1 |
| --- | --- | ---: | ---: |
| unigram | NB | 84.0% | 84.7% |
| unigram+bigram | NB | 84.6% | 85.2% |
| unigram+bigram+trigram | NB | **85.2%** | **85.6%** |

## 4. 逐步变化

NB accuracy：

\[
84.0
\rightarrow
84.6
\rightarrow
85.2.
\]

NB weighted F1：

\[
84.7
\rightarrow
85.2
\rightarrow
85.6.
\]

总变化为：

\[
+1.2\text{ pp accuracy},
\qquad
+0.9\text{ pp F1}.
\]

## 5. LR 与 SVM

LR 的最佳 accuracy 从 74.1% 升到 75.3%。SVM 从 74.3% 升到 74.9%，在 bigram 和 trigram 两种配置下相同。

两者都低于 82.7% 的多数类 accuracy。

## 6. 原文的解释

作者认为不同阶 \(n\)-gram 可以互补：

- unigram 表示核心词；
- bigram 表示局部搭配；
- trigram 表示更完整的短语。

随着特征范围扩大，筛选阶段能从更丰富的候选中挑出有用信号。

## 7. 证据强度

最佳 85.2% 很可能等于

\[
\frac{69}{81}=85.185\%.
\]

前一配置 84.6% 无法在 81 道题上由整数正确数精确产生，因此不同配置的四舍五入、测试规模或指标计算细节存在未报告信息。即便把表格视为精确到一位小数，0.6 pp 也小于单题分辨率。

## 8. 更稳健的比较方式

应对同一测试题记录逐题预测，使用：

- McNemar test；
- paired bootstrap；
- repeated splits；
- 每次划分的均值和标准差。

原文没有提供这些分析。
