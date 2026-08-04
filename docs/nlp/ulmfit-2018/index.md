# 微调：ULMFiT (2018)

**Universal Language Model Fine-tuning for Text Classification** 把“怎样稳定微调语言模型”本身变成研究问题。fine-tuning 概念早于该文；选择 ULMFiT 是因为它系统提出 discriminative fine-tuning、slanted triangular learning rates 与 gradual unfreezing，并直接影响后来的 NLP 迁移范式。

## 阅读路线

1. [三阶段迁移流程与 AWD-LSTM](01-three-stage-method.md)
2. [Discriminative LR、STLR 与 gradual unfreezing](02-finetuning-techniques.md)
3. [Concat pooling 与分类算法](03-classifier-algorithm.md)
4. [实验、消融与低样本结果](04-experiments-results.md)
5. [局限、BERT/LoRA 接口与结论](05-limitations-conclusion.md)
6. [参考文献](references.md)
