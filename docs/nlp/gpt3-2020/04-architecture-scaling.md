# 模型架构、八种规模与 sparse attention

## 1. 架构继承

GPT-3 沿用 GPT-2 的主要设计：

- decoder-only Transformer；
- causal self-attention；
- pre-LayerNorm；
- residual initialization scaling；
- byte-level BPE 可逆 tokenizer；
- 输入输出 embedding 权重共享；
- 自回归 next-token loss。

主要结构改动是不同层交替采用 dense attention 和 locally banded sparse attention，设计参考 Sparse Transformer。

## 2. 八种规模

| 模型 | 参数量 | 层数 | \(d_{\mathrm{model}}\) | 头数 | \(d_{\mathrm{head}}\) | batch tokens | 学习率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Small | 125M | 12 | 768 | 12 | 64 | 0.5M | \(6.0\times10^{-4}\) |
| Medium | 350M | 24 | 1024 | 16 | 64 | 0.5M | \(3.0\times10^{-4}\) |
| Large | 760M | 24 | 1536 | 16 | 96 | 0.5M | \(2.5\times10^{-4}\) |
| XL | 1.3B | 24 | 2048 | 24 | 128 | 1M | \(2.0\times10^{-4}\) |
| 2.7B | 2.7B | 32 | 2560 | 32 | 80 | 1M | \(1.6\times10^{-4}\) |
| 6.7B | 6.7B | 32 | 4096 | 32 | 128 | 2M | \(1.2\times10^{-4}\) |
| 13B | 13.0B | 40 | 5140 | 40 | 128 | 2M | \(1.0\times10^{-4}\) |
| GPT-3 | 175.0B | 96 | 12,288 | 96 | 128 | 3.2M | \(0.6\times10^{-4}\) |

所有模型训练 3000 亿 token，上下文长度均为 2048。前馈层宽度为

\[
d_{\mathrm{ff}}=4d_{\mathrm{model}}.
\]

## 3. Dense causal attention

完整因果注意力计算：

\[
\mathbf A
=
\operatorname{softmax}
\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_h}}+\mathbf M_{\mathrm{causal}}
\right).
\]

长度 \(T\) 的 score matrix 有 \(T^2\) 个位置，attention 时间与显存主项约为

\[
O(T^2d).
\]

## 4. Locally banded sparse attention

局部带状模式让位置 \(t\) 只读附近窗口 \(W(t)\)：

\[
\alpha_{t,s}=0,
\qquad s\notin W(t).
\]

若窗口宽度 \(w\ll T\)，注意力连接数从 \(T^2\) 降为约 \(Tw\)。GPT-3 在不同层交替 dense 与 sparse pattern：

- sparse 层降低部分 attention 计算；
- dense 层仍提供全局信息连接；
- 多层堆叠扩大有效感受野。

论文没有公开足够训练代码来完整复刻其稀疏 kernel 和分布式实现。

## 5. 参数量为何会如此大

一个 Transformer block 的主要矩阵近似包括：

- QKV 与输出投影：约 \(4d^2\)；
- 两层 MLP：约 \(8d^2\)。

每层主项约

\[
12d^2.
\]

96 层、\(d=12{,}288\) 时，仅 block 矩阵就进入千亿参数量级，再加 embedding、LayerNorm 与 bias。

## 6. 模型并行

单个 175B 模型无法放在单张 V100 上。论文沿两个方向切分：

1. 层间切分：不同 Transformer layers 分到不同设备；
2. 层内切分：单次 matrix multiply 的宽度维也跨 GPU 分片。

目标是让通信与计算重叠，并减少节点间数据传输。论文只给出高层说明，没有发布完整训练系统。

## 7. 扩大参数量并不只改变“容量”

表中更大模型同时使用：

- 更多层和更宽隐藏状态；
- 更大 batch；
- 更小初始学习率；
- 不同并行规模与训练动力学。

因此尺度实验研究的是一整套协同扩展方案。参数量是主要横轴，但不能把所有差异都归因于单一数字。
