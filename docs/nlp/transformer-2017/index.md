# Attention Is All You Need：Transformer 精读

本专题精读 Vaswani et al. (2017) 的 **Attention Is All You Need**。论文将序列建模的主体从 RNN/CNN 改为 self-attention，提出 Transformer encoder–decoder。

## 核心变化

\[
\text{RNN 逐位置状态链}
\quad\Longrightarrow\quad
\text{全位置 attention 矩阵}.
\]

每层接收 \(\mathbf X\in\mathbb R^{n\times d_{\text{model}}}\)，生成

\[
\mathbf Q=\mathbf X\mathbf W^Q,\quad
\mathbf K=\mathbf X\mathbf W^K,\quad
\mathbf V=\mathbf X\mathbf W^V,
\]

\[
\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)
=
\operatorname{softmax}\!\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_k}}
\right)\mathbf V.
\]

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Ashish Vaswani 等 8 位作者 |
| 发表 | NeurIPS 2017 |
| 正式论文 | [NeurIPS Proceedings](https://papers.nips.cc/paper/7181-attention-is-all-you-need) |
| arXiv | [1706.03762](https://arxiv.org/abs/1706.03762) |
| 原始实现 | [Tensor2Tensor](https://github.com/tensorflow/tensor2tensor) |

## 阅读路线

1. [问题、创新与架构全景](01-problem-contributions-architecture.md)
2. [Q、K、V 的含义与矩阵形状](02-query-key-value-shapes.md)
3. [Scaled Dot-Product Attention](03-scaled-dot-product-attention.md)
4. [Padding mask 与 causal mask](04-masks.md)
5. [Multi-Head Attention](05-multi-head-attention.md)
6. [Encoder、Decoder 与三种 attention](06-encoder-decoder.md)
7. [位置编码](07-positional-encoding.md)
8. [FFN、残差、LayerNorm 与原始 Post-LN](08-ffn-residual-layernorm.md)
9. [训练目标、优化器与自回归推理](09-training-and-inference.md)
10. [复杂度、路径长度与并行化](10-complexity-and-parallelism.md)
11. [完整手算](11-worked-example.md)
12. [实验设计、结果与消融](12-experiments-results.md)
13. [Tensor2Tensor 与现代 PyTorch 实现](13-code-reading-implementation.md)
14. [局限、现代变体与结论](14-limitations-modern-variants-conclusion.md)
15. [参考文献与一手资源](references.md)

## 阅读后应能回答

- query、key、value 分别来自哪里；
- 为什么除以 \(\sqrt{d_k}\)；
- causal mask 为什么不妨碍训练时跨位置并行；
- 八个头如何切分 512 维表示；
- encoder self-attention、decoder masked self-attention、cross-attention 的区别；
- 正弦位置编码怎样表达相对位移；
- 原论文为何是 Post-LN，以及它和现代 Pre-LN 的差别；
- Transformer 训练可并行而自回归生成仍逐 token 的原因；
- base/big 的参数、训练配置和 BLEU 证据；
- LoRA 后续会改动 Transformer 中哪些线性投影。
