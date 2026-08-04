# 实验结果

## 1. GLUE

| 模型 | MNLI m/mm | QNLI | SST-2 | CoLA | MRPC | RTE | 平均 |
|---|---:|---:|---:|---:|---:|---:|---:|
| OpenAI GPT | 82.1/81.4 | 87.4 | 91.3 | 45.4 | 82.3 | 56.0 | 75.1 |
| BERT Base | 84.6/83.4 | 90.5 | 93.5 | 52.1 | 88.9 | 66.4 | 79.6 |
| BERT Large | **86.7/85.9** | **92.7** | **94.9** | **60.5** | **89.3** | **70.1** | **82.1** |

平均列排除 WNLI，与当时官方 GLUE score 略不同。各任务使用 accuracy、F1、Spearman 或 Matthews correlation，不能把列值当同一种统计量。

## 2. SQuAD 1.1

- BERT Large 单模型 + TriviaQA：test EM 85.1、F1 91.8；
- 7 模型 ensemble + TriviaQA：EM 87.4、F1 93.2；
- 不使用 TriviaQA 时开发 F1 只低约 0.1–0.4。

额外 TriviaQA 数据与 ensemble 都应和基础单模型区分。

## 3. SQuAD 2.0

BERT Large 单模型 test EM 80.0、F1 83.1，比论文列出的此前最佳 F1 高 5.1。

## 4. SWAG

| 模型 | Test accuracy |
|---|---:|
| ESIM + ELMo | 59.2 |
| OpenAI GPT | 78.0 |
| BERT Large | 86.3 |

论文报告的人类 expert 约 85.0、5 人标注约 88.0；小样本人类估计需谨慎比较。

## 5. 结果为何重要

同一个预训练 encoder 通过极少任务头，在句子分类、句对推断、常识选择和 token span 预测上都达到强结果，支持可迁移通用表示这一主张。

## 6. 证据边界

- 很多结果按开发集挑学习率/随机重启；
- 大模型在小数据微调中不稳定；
- leaderboard 结果可能含额外数据与 ensemble；
- benchmark 提升不等同于全面语言理解；
- 数据集可能含捷径、标注偏差和领域限制。
