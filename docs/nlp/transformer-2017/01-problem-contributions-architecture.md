# 问题、创新与架构全景

## 1. 论文面对的瓶颈

RNN 将位置与计算时间绑定：

\[
\mathbf h_t=f(\mathbf h_{t-1},\mathbf x_t).
\]

同一训练样本内部需要依次计算 \(n\) 个状态。序列变长后，batch 又受显存限制，这条串行关键路径成为训练吞吐瓶颈。

CNN 能并行计算位置，但任意远距离位置建立联系需要多层卷积：普通卷积的最长路径随距离线性增长，膨胀卷积约为对数增长。

## 2. 论文的核心提案

Transformer 完全移除序列对齐的 recurrence 与 convolution，使用：

- self-attention 交换不同位置的信息；
- position-wise FFN 在每个位置内变换特征；
- residual connection 和 LayerNorm 稳定深层训练；
- positional encoding 注入顺序；
- encoder–decoder attention 连接源序列与目标序列。

## 3. Encoder

原论文堆叠 \(N=6\) 层，每层包含：

1. multi-head self-attention；
2. position-wise FFN。

每个子层外使用

\[
\operatorname{LayerNorm}(
\mathbf x+\operatorname{Sublayer}(\mathbf x)).
\]

这是 **Post-LN**：先残差相加，再 LayerNorm。

## 4. Decoder

每个 decoder 层有三个子层：

1. masked multi-head self-attention；
2. 对 encoder 输出的 multi-head cross-attention；
3. position-wise FFN。

目标 token embedding 右移一位，配合 causal mask，位置 \(i\) 只能依赖 \(y_{<i}\)。

## 5. 原论文 base 配置

| 参数 | 数值 |
|---|---:|
| 层数 \(N\) | 6 encoder + 6 decoder |
| \(d_{\text{model}}\) | 512 |
| \(d_{\text{ff}}\) | 2048 |
| 头数 \(h\) | 8 |
| \(d_k=d_v\) | 64 |
| dropout | 0.1 |
| label smoothing | 0.1 |
| 参数量 | 约 65M |

big 模型采用 \(d_{\text{model}}=1024\)、\(d_{\text{ff}}=4096\)、16 头、约 213M 参数。

## 6. “Attention Is All You Need”的准确范围

标题强调序列位置之间的信息交换不再依赖 RNN 或卷积。完整模型仍包含 embedding、位置编码、FFN、残差、LayerNorm、softmax 和自回归搜索。attention 是架构中的关系建模主体，并非整张网络唯一运算。

## 7. 与 Bahdanau 的连接

Bahdanau attention 用一个解码状态查询双向 RNN 注释。Transformer 将 query、key、value 全部矩阵化：

- encoder self-attention：每个源位置查询全部源位置；
- decoder self-attention：每个目标位置查询已知目标前缀；
- cross-attention：每个目标位置查询全部源表示。

动态读取思想得到保留，递归 query 生成方式被移除。
