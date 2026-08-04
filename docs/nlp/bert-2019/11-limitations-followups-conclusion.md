# 局限、后续发展与结论

## 1. MLM 预训练—使用差异

`[MASK]` 很少出现在下游输入；80/10/10 只能缓解。MLM 也只在 15% token 上提供直接预测损失。

## 2. NSP

随机文档负例可能过于容易，混合了主题辨别与句子连续性。后续 RoBERTa 去掉 NSP，ALBERT 使用 sentence-order prediction，说明句间目标仍有设计空间。

## 3. 长度与成本

可学习位置最大 512，全局 attention 随长度二次增长。BERT Large 340M 在当时已需 64 TPU chips 训练约 4 天。

## 4. Encoder-only 的任务边界

BERT 擅长理解型表示与抽取式任务，原生不提供高效自回归文本生成接口。生成任务通常使用 decoder-only 或 encoder–decoder 架构。

## 5. 微调不稳定与灾难性遗忘

小数据上 Large 需要多随机重启。全量微调还要为每个任务保存完整参数；LoRA、adapter、prompt tuning 等后续 PEFT 方法用于降低成本。

## 6. 后续重要修正

| 工作 | 主要变化 |
|---|---|
| RoBERTa | 更多数据、更久训练、动态 mask、去 NSP |
| ALBERT | 参数共享、factorized embedding、SOP |
| SpanBERT | span masking 与 span boundary |
| ELECTRA | replaced-token detection，提高样本效率 |
| DistilBERT | 蒸馏压缩 |
| DeBERTa | disentangled attention |

## 7. 历史贡献

BERT 将 Transformer encoder、MLM、句对输入和端到端微调整合为统一预训练范式。它把大量 NLP 任务从“为每个任务设计主体网络”推进到“共享预训练模型 + 小任务头”。

## 8. 结论

BERT 的关键机制是用输入破坏消除双向预测泄漏，再将每层左右上下文预训练成可迁移表示。其强实验结果证明大规模无标注预训练可以显著降低下游架构工程，但 MLM、NSP、长度、成本和全量微调也为后续研究留下清晰问题。
