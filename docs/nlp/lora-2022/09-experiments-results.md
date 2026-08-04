# 实验设计与结果

## 1. 模型与任务

| 模型 | 任务 |
|---|---|
| RoBERTa base/large | GLUE |
| DeBERTa XXL 1.5B | GLUE |
| GPT-2 medium/large | E2E、DART、WebNLG |
| GPT-3 175B | WikiSQL、MNLI、SAMSum |

实验使用 NVIDIA V100；部分 baseline 数字引用既有论文，作者自己的运行报告均值/区间或典型波动。

## 2. GLUE

- RoBERTa base：LoRA 0.3M 参数，平均 87.2；全量 125M，平均 86.4；
- RoBERTa large：LoRA 0.8M，平均 89.0；全量 355M，平均 88.9；
- DeBERTa XXL：LoRA 4.7M，平均 91.3；全量 1.5B，平均 91.1。

不同 GLUE 子任务指标并不完全相同，平均值用于概要，不能替代逐任务阅读。

## 3. GPT-2 E2E

| 方法 | GPT-2 M 参数 | BLEU | GPT-2 L 参数 | BLEU |
|---|---:|---:|---:|---:|
| Full FT | 354.92M | 68.2 | 774.03M | 68.5 |
| LoRA | 0.35M | \(70.4\pm0.1\) | 0.77M | \(70.4\pm0.1\) |

论文还报告 NIST、METEOR、ROUGE-L、CIDEr，以及 DART/WebNLG 结果。

## 4. GPT-3

| 方法 | 可训练参数 | WikiSQL | MNLI-m | SAMSum R1/R2/RL |
|---|---:|---:|---:|---:|
| Full FT | 175,255.8M | 73.8 | 89.5 | 52.0/28.0/44.5 |
| LoRA | 4.7M | 73.4 | 91.7 | 53.8/29.8/45.9 |
| LoRA | 37.7M | 74.0 | 91.6 | 53.4/29.2/45.1 |

增加 LoRA 参数没有在每项指标上单调提升，说明预算之外还存在优化与任务匹配问题。

## 5. 训练与部署资源

GPT-3 案例报告训练显存约 1.2TB 降至 350GB，训练吞吐提高约 25%，task checkpoint 约 35MB。部署仍要持有 350GB 基座；100 个任务约为基座加 100 个小 LoRA，而非 100 份完整基座。

## 6. 证据边界

- GPT-3 训练成本使完整多种子实验受限；
- 一些 baseline 来自不同论文；
- 测试模型和任务代表 2021 年环境；
- 结果支持这些场景中的参数效率，没有证明低秩更新对所有任务、模态和训练规模都最优。
