# 架构、Backbone 与学习目标

## 1. Transformer 的共同骨架

核心 attention 为：

\[
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}
\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.
\]

\(M\) 决定可见性：双向 encoder 通常只遮住 padding；自回归 decoder 使用 causal mask。

完整细节见 [Transformer 论文精读](../transformer-2017/index.md)。

## 2. 三种 Backbone

| 架构 | 可见上下文 | 典型目标 | 适用 |
|---|---|---|---|
| Encoder-only | 双向 | MLM、判别任务 | 表征、分类、抽取 |
| Decoder-only | 左到右 | full LM | 通用生成与 in-context learning |
| Encoder-decoder | encoder 双向、decoder 因果 | conditional generation | 翻译、摘要、受条件生成 |

模型能力不能只由参数量解释；backbone 与 objective 决定训练信号和推理接口。

## 3. Full Language Modeling

\[
\mathcal L_{\mathrm{CLM}}
=
-\sum_{t=1}^{n}
\log p_\theta(x_t\mid x_{<t}).
\]

适合 decoder-only 模型，训练和生成形式一致。

## 4. Masked Language Modeling

随机选择位置集合 \(M\)：

\[
\mathcal L_{\mathrm{MLM}}
=
-\sum_{t\in M}
\log p_\theta(x_t\mid \widetilde x).
\]

模型可以利用左右文。BERT 使用 MLM 预训练，再针对下游任务微调。

## 5. Prefix Language Modeling

prefix 内部允许双向可见，生成区保持因果：

```text
[bidirectional prefix] → [causal continuation]
```

它在条件理解与生成之间提供另一种 mask 结构。

## 6. Mixture of Experts

路由器为每个 token 选择少数专家：

\[
h'
=
\sum_{e\in\operatorname{TopK}(g(h))}
g_e(h)E_e(h).
\]

MoE 增加总参数容量而控制 active parameters，但增加权重驻留、专家均衡和通信难度。

## 7. 架构选择原则

应用需求应映射到模型性质：

```text
需要高质量 embedding / token classification
→ encoder 或专门 embedding model

需要开放式生成 / tool use
→ instruction-tuned decoder

需要严格输入到输出转换
→ encoder-decoder 或受控 decoder
```

“统一用最大的 chat model”会增加成本，也可能降低可控性。

## 8. 内在损失与应用评价

perplexity：

\[
\operatorname{PPL}=\exp\left(
-\frac1n\sum_t\log p_\theta(x_t\mid x_{<t})
\right).
\]

低 perplexity 不保证工具参数正确、引用忠实或 CAT 测量有效。模型内在评价与应用级评价必须分开。

