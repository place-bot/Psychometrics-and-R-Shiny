# 局限、BERT/LoRA 接口与结论

## 1. 局限

- 单向 LSTM 无法像 BERT 同层融合左右上下文；
- 主要验证文本分类；
- 长文档依赖 truncated BPTT；
- 三阶段训练和多种 dropout/LR 策略较复杂；
- 每任务仍产生完整微调参数；
- tokenizer 与词级 LM 有 OOV 限制。

## 2. 与 BERT

BERT 把 ULMFiT 所体现的通用预训练—目标微调范式扩展到 Transformer encoder，并用 MLM 获得深层双向表示。BERT 的下游配置更统一，通常直接全量微调。

## 3. 与 LoRA

ULMFiT 研究如何稳定更新不同层；LoRA 研究如何用低秩参数表示更新。现代训练可组合：

\[
\text{layer-wise schedule}
\quad+\quad
\text{parameter-efficient update}.
\]

但 LoRA 参数的最优学习率层级未必照搬 ULMFiT 的 2.6 比例。

## 4. “Fine-tuning”的准确含义

从预训练参数出发，用目标数据继续优化。可能更新：

- 全部参数；
- 部分层；
- bias；
- adapter；
- prompt；
- LoRA 低秩增量。

ULMFiT 主方法更新逐步解冻的完整 LM；LoRA 是后来的一种参数高效 fine-tuning。

## 5. 结论

ULMFiT 证明微调策略会实质影响迁移效果。预训练 checkpoint 只是起点；学习率、层级更新顺序、目标域适配与分类读出共同决定能否保留通用知识并学习目标任务。
