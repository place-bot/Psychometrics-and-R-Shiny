# 局限、Transformer 接口与后续工作

## 1. 原模型的主要局限

### 词级 30k 词表

低频词统一映射为 \([UNK]\)，完整测试集 BLEU 明显受词表覆盖影响。后来的 subword/BPE 把开放词表问题转化为可组合子词预测。

### 递归计算

编码器与解码器沿时间步串行，限制长序列训练吞吐。attention 改善信息访问，没有移除 RNN 状态链。

### 二维对齐成本

每个目标步比较全部源位置，attention 矩阵规模为 \(T_xT_y\)。长源句、长目标句会同时增加时间与存储。

### 缺少显式覆盖

原模型没有累计记录哪些源内容已翻译。重复关注可能造成重复翻译，低覆盖位置可能导致漏译。

### Teacher forcing

训练看到真实前缀，推理看到模型前缀，产生 exposure bias。

### 证据范围

主实验集中在 WMT14 英法单方向，未报告多种子区间、组件消融与人工对齐指标。

## 2. 后续改进线索

- Luong attention：提出 global/local attention 与不同 score；
- coverage：把累计注意力反馈给后续步骤；
- pointer/copy：直接从输入位置复制稀有词；
- BPE/subword：显著缓解 \([UNK]\)；
- multi-head：让多个子空间并行建立关系；
- self-attention：用全位置交互替代循环编码；
- non-autoregressive decoding：进一步研究输出端并行。

## 3. Bahdanau 与 Transformer attention

| 维度 | Bahdanau attention | Transformer attention |
|---|---|---|
| query | 前一解码状态 | 线性投影后的每个位置 |
| key/value | 双向 RNN 注释 | 线性投影后的序列表示 |
| score | MLP/additive | scaled dot product |
| 头数 | 单个对齐机制 | multi-head |
| 位置间状态 | RNN 递归 | self-attention + position |
| 训练位置并行 | 受递归限制 | 可矩阵化 |

Transformer cross-attention 延续了“目标端 query 读取源端表示”的思想；它重写了 query、key、value 的生成方式和兼容函数。

## 4. 从加法打分到点积打分

Bahdanau：

\[
e_{ij}
=
\mathbf v_a^\top
\tanh(\mathbf W_a\mathbf s_{i-1}+\mathbf U_a\mathbf h_j).
\]

Transformer：

\[
e_{ij}
=
\frac{\mathbf q_i^\top\mathbf k_j}{\sqrt{d_k}}.
\]

前者用小型神经网络学习兼容度，后者利用矩阵乘法高效计算所有位置对，并用 \(\sqrt{d_k}\) 控制内积尺度。

## 5. 研究问题

从这篇论文可继续追问：

1. attention 权重与人工对齐、因果贡献分别有何关系？
2. 如何加入覆盖、术语与词典约束？
3. 如何在长序列上降低 \(T_xT_y\) 成本？
4. 如何把自回归生成的质量与并行速度同时提高？
5. 动态检索思想如何迁移到推荐、CAT 与自适应教学？

## 本页小结

Bahdanau attention 解决了固定向量的动态访问问题。Transformer 随后保留 query—key—value 检索思想，去掉训练中的循环状态链，并引入多头与位置表示。两篇论文构成一条清晰的架构演化线。
