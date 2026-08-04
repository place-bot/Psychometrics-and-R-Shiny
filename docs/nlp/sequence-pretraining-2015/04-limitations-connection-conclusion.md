# 局限、BERT 接口与结论

## 1. 局限

- 单向 LSTM 与最终状态瓶颈；
- sequence autoencoder 重构超长文档昂贵；
- truncated BPTT 限制远端梯度；
- 词级词表与 OOV；
- 无统一大规模通用预训练 checkpoint；
- 主要任务是文档分类；
- pretrain/fine-tune 的学习率、冻结策略尚不成熟。

## 2. 从该文到 ULMFiT

ULMFiT 保留语言模型预训练与目标微调，进一步：

- 用大规模通用 WikiText-103 预训练；
- 先做目标域 LM fine-tuning；
- 使用 discriminative LR、STLR 和 gradual unfreezing；
- 提供更通用、稳定的分类流程。

## 3. 从该文到 BERT

BERT 将 LSTM 换成双向 Transformer encoder，把 next-token 目标换成 MLM，并扩大到统一句对、token 与 span 任务。共同范式仍是：

\[
\text{无标注预测任务}
\rightarrow
\text{参数初始化}
\rightarrow
\text{监督任务微调}.
\]

## 4. 结论

Dai 与 Le 的实验清楚显示：无标注序列目标学习到的参数能改善监督 LSTM 的稳定性与泛化。预训练的价值超越静态词向量，扩展到整个序列模型。
