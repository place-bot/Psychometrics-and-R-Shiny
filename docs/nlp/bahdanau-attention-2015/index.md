# Bahdanau Attention：联合学习对齐与翻译

本专题精读 Dzmitry Bahdanau、Kyunghyun Cho 与 Yoshua Bengio 的论文 **Neural Machine Translation by Jointly Learning to Align and Translate**。

论文从早期神经机器翻译的固定向量瓶颈出发，提出后来常称为 **Bahdanau attention** 或 **additive attention** 的机制。它在生成每个目标词之前，根据当前解码状态重新计算一组源端权重，再用加权和形成当前步骤的上下文。

## 一张图看论文

```text
源句 x1, x2, ..., xTx
        │
        ├── 正向 GRU ──► h→1, h→2, ..., h→Tx
        │
        └── 反向 GRU ──► h←1, h←2, ..., h←Tx
                           │
                           ▼
              双向注释 hj = [h→j ; h←j]
                           │
             对每个目标位置 i 重新计算
                           ▼
    上一步解码状态 si-1 ─► additive alignment score eij
                           │ 对全部源位置做 softmax
                           ▼
                    注意力权重 αij
                           │
                           ▼
                  ci = Σj αij hj
                           │
                           ▼
        上一目标词 yi-1 + si-1 + ci
                           │
                           ▼
                 解码状态与下一个词 yi
```

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Dzmitry Bahdanau、Kyunghyun Cho、Yoshua Bengio |
| 正式发表 | ICLR 2015 Conference Paper，Oral Presentation |
| arXiv | [1409.0473](https://arxiv.org/abs/1409.0473) |
| 首次提交 | 2014 年 9 月 1 日 |
| 本专题核对版本 | v7，2016 年 5 月 19 日 |
| 作者公开实现 | [lisa-groundhog/GroundHog](https://github.com/lisa-groundhog/GroundHog/tree/master/experiments/nmt) |

论文最早在 2014 年以 arXiv 预印本出现，随后作为 ICLR 2015 会议论文发表。ICLR 的正式日程将其列为 2015 年 5 月 9 日的 oral presentation。

## 论文要解决的核心问题

早期 RNN Encoder–Decoder 把整个源句压缩进一个固定维度向量：

\[
\mathbf x
\longrightarrow
\mathbf c
\longrightarrow
\mathbf y.
\]

当源句变长时，\(\mathbf c\) 要同时保存实体、修饰关系、长距离依赖、词序与全部细节。论文把这个固定向量视为影响长句翻译的主要瓶颈。

RNNsearch 保留一整列源端注释：

\[
\mathbf h_1,\mathbf h_2,\ldots,\mathbf h_{T_x},
\]

并为目标端每一步生成独立上下文：

\[
\mathbf c_i
=
\sum_{j=1}^{T_x}
\alpha_{ij}\mathbf h_j.
\]

因此，同一句源文本在生成不同目标词时可以提供不同的信息摘要。

## 论文贡献的四层结构

### 1. 表示层

双向 RNN 为每个源词生成同时包含左、右语境的注释 \(\mathbf h_j\)。

### 2. 检索层

对齐网络 \(a(\mathbf s_{i-1},\mathbf h_j)\) 计算前一解码状态与每个源位置的匹配分数。

### 3. 概率层

分数经过源位置上的 softmax，得到归一化权重 \(\alpha_{ij}\)，再形成期望注释 \(\mathbf c_i\)。

### 4. 学习层

权重是连续、可微的。翻译负对数似然的梯度能够穿过上下文、softmax、对齐网络和双向编码器，使翻译与对齐共同学习。

## 原文范围

论文正文和附录明确给出：

- 固定向量 RNN Encoder–Decoder 的概率分解；
- RNNsearch 的逐步上下文；
- additive alignment model；
- 双向 RNN 编码器；
- gated hidden unit 的完整公式；
- deep output 与 maxout 输出层；
- WMT 2014 英法数据、预处理与模型规模；
- Adadelta、梯度范数约束、批次排序和参数初始化；
- BLEU 结果、长度分组曲线、对齐热图与长句译例；
- RNNencdec、RNNsearch 和 Moses 的比较；
- GroundHog/Theano 实现链接。

专题会在这些内容上补充形状检查、梯度推导、手算例子和现代 PyTorch 实现，并把补充推导与原文陈述分开。

## 推荐阅读路线

### 第一次：建立完整信息流

1. [论文身份、问题与创新](01-paper-identity-motivation.md)
2. [神经机器翻译概率基础与固定向量瓶颈](02-nmt-probability-and-fixed-vector.md)
3. [双向编码器与源端注释](03-bidirectional-encoder.md)
4. [逐步解码与条件生成](04-decoder-and-generation.md)
5. [Additive Attention 完整推导](05-additive-attention.md)

### 第二次：吃透训练与推理

1. [端到端目标与反向传播](06-end-to-end-training.md)
2. [GRU、初始化与 Deep Output](07-gru-and-deep-output.md)
3. [Beam Search 与推理](08-beam-search-and-inference.md)
4. [逐步手算：从注意力到梯度](09-worked-example.md)

### 第三次：判断实验证据

1. [实验设计、数据与训练配置](10-experiment-design.md)
2. [BLEU 结果与长度分析](11-results-and-length-analysis.md)
3. [软对齐与长句案例](12-alignment-and-long-sentences.md)

### 第四次：连接代码与现代模型

1. [GroundHog 原始代码精读](13-groundhog-code-reading.md)
2. [现代 PyTorch 实现](14-modern-pytorch-implementation.md)
3. [注意力解释、复杂度与边界](15-attention-interpretation-and-complexity.md)
4. [局限、Transformer 接口与后续工作](16-limitations-transformer-future.md)
5. [符号表、结论与阅读地图](17-symbols-conclusion.md)

## 阅读完成后应能解释

- 固定向量瓶颈具体发生在哪条信息路径；
- 为什么每个源位置的注释需要双向语境；
- \(\mathbf s_{i-1}\)、\(\mathbf h_j\)、\(e_{ij}\)、\(\alpha_{ij}\) 和 \(\mathbf c_i\) 分别表示什么；
- additive attention 的每一步矩阵形状；
- soft alignment 为什么可以用标准反向传播训练；
- 论文中的 gated hidden unit 与现代 GRU 记号有何差异；
- deep output 与 maxout 怎样产生词表概率；
- 训练阶段与 beam-search 推理阶段怎样不同；
- RNNsearch-50 的实验优势具体来自哪些结果；
- “No UNK” BLEU 为什么要和全测试集 BLEU 分开解释；
- 对齐热图能够支持什么结论，又无法单独证明什么；
- GroundHog 代码怎样实现预计算、mask、动态上下文和束搜索；
- Bahdanau attention 与 Transformer cross-attention、自注意力之间的联系和差别。
