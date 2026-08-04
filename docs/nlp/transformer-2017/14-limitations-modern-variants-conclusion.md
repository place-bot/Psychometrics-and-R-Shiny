# 局限、现代变体与结论

## 1. 二次 attention 成本

全局 self-attention 产生 \(n\times n\) 分数矩阵。短句训练高效，长文档、音频和高分辨率视觉 token 会带来显著显存与计算成本。

## 2. 自回归生成延迟

训练跨位置并行，生成仍依赖前缀。KV cache、speculative decoding 和并行解码研究用于降低这一瓶颈，属于后续工作。

## 3. 顺序归纳偏置

Transformer 用位置编码注入顺序，没有 RNN 的时间递归或 CNN 的局部邻域先验。它获得全局关系和硬件效率，也可能更依赖数据学习局部结构。

## 4. 原始 Post-LN 的深度稳定性

原论文六层 Post-LN 可有效训练。更深模型常改为 Pre-LN 或使用其他归一化、残差缩放与初始化方案。

## 5. 原论文与现代 LLM

| 原始 Transformer | 常见现代变体 |
|---|---|
| encoder–decoder | decoder-only、encoder-only |
| 正弦绝对位置 | RoPE、relative bias、ALiBi |
| ReLU FFN | GELU、SwiGLU |
| Post-LN | Pre-LN/RMSNorm |
| multi-head attention | GQA/MQA |
| 机器翻译监督训练 | 大规模自监督预训练与指令微调 |

这些发展沿用 attention、残差和逐位置 FFN 主体，但具体方程已变化。

## 6. 论文的历史创新

贡献组合包括：

- 完整移除 sequence-aligned recurrence/convolution；
- scaled dot-product attention；
- multi-head attention；
- encoder 与 decoder 的全 attention 堆叠；
- 位置编码；
- 并行训练与短长距离路径分析；
- 在 WMT14 上以较低训练成本取得强结果。

## 7. 与 LoRA 的下一步连接

Transformer 把大量能力放进矩阵

\[
\mathbf W^Q,\mathbf W^K,\mathbf W^V,\mathbf W^O,
\mathbf W_1,\mathbf W_2.
\]

全量微调会更新这些大矩阵的每个元素。LoRA 假设下游任务所需的更新 \(\Delta\mathbf W\) 具有低内在秩，用两个小矩阵表示，从而只训练极少参数。

## 8. 结论

Transformer 的关键突破是把位置间依赖改写成可矩阵化的 attention，并用 mask 保留因果约束。它缩短了长距离信息路径，显著提升训练并行性，同时留下长上下文二次成本和自回归推理串行问题。
