# 语言建模实验与规模效应

## 1. 实验设计

作者训练四个近似对数均匀分布的模型规模。每个模型的学习率根据 WebText 5% 留出集 perplexity 手工调整。报告指出，所有模型仍在欠拟合 WebText，继续训练时训练与留出 perplexity 都会改善。

语言建模迁移的关键限制是 tokenizer 不同。GPT-2 直接对字节级 BPE token 建模，而很多 benchmark 已经过强制小写、PTB tokenization、句子打乱或 UNK 替换。作者使用可逆 detokenizer 尽量恢复文本，再计算目标数据的对数概率。

## 2. 评价指标

### 2.1 Perplexity

若以词为规范单位，平均负对数似然为

\[
\operatorname{NLL}
=
-\frac{1}{N}\sum_{t=1}^{N}\log p(x_t\mid x_{<t}),
\]

perplexity 为

\[
\operatorname{PPL}=\exp(\operatorname{NLL}).
\]

PPL 越低越好。

### 2.2 Bits per byte / character

\[
\operatorname{BPB}
=
-\frac{1}{N_{\mathrm{byte}}}
\sum_t\log_2 p(x_t\mid x_{<t}).
\]

不同 tokenization 的模型可以按 byte 或 character 归一化，但文本预处理仍会影响可比性。

## 3. 论文表 3 的核心结果

| 数据集/指标 | 当时列出的 SOTA | 117M | 345M | 762M | 1542M |
|---|---:|---:|---:|---:|---:|
| LAMBADA PPL ↓ | 99.8 | 35.13 | 15.60 | 10.87 | **8.63** |
| LAMBADA Acc ↑ | 59.23 | 45.99 | 55.48 | 60.12 | **63.24** |
| CBT-CN Acc ↑ | 85.7 | 87.65 | 92.35 | **93.45** | 93.30 |
| CBT-NE Acc ↑ | 82.3 | 83.4 | 87.1 | 88.0 | **89.05** |
| WikiText-2 PPL ↓ | 39.14 | 29.41 | 22.76 | 19.93 | **18.34** |
| PTB PPL ↓ | 46.54 | 65.85 | 47.33 | 40.31 | **35.76** |
| enwik8 BPB ↓ | 0.99 | 1.16 | 1.01 | 0.97 | **0.93** |
| text8 BPC ↓ | 1.08 | 1.17 | 1.06 | 1.02 | **0.98** |
| WikiText-103 PPL ↓ | 18.3 | 37.50 | 26.37 | 22.05 | **17.48** |
| 1BW PPL ↓ | 21.8 | 75.20 | 55.72 | 44.575 | **42.16** |

最大模型在论文统计的 8 个主要语言建模数据集中，7 个达到当时零样本 SOTA；1BW 是明显例外。

## 4. 为什么 1BW 表现较差

One Billion Word Benchmark 规模更大，而且预处理打乱了句子顺序。GPT-2 从 WebText 学到的跨句、长距离结构在这个 benchmark 上无法充分利用；强预处理也造成域和 tokenization 偏移。

因此模型在自然文档上的优势不保证能转移到高度规范化、句序被破坏的分布。

## 5. LAMBADA

LAMBADA 要预测段落最后一个词，通常需要至少约 50 token 上下文。最大模型的原始预测常是合理续写，却未必是句末合法词。作者加入近似 stop-word 过滤后，accuracy 从文中讨论的 52.66% 提高到 63.24%，超过当时结果。

这说明该结果同时包含：

- 模型的长程条件能力；
- 任务输出空间的人工约束；
- 评测格式与自然生成之间的差异。

## 6. CBT

Children’s Book Test 需要在 10 个候选词中补空。最大模型在 common nouns 上达到 93.3%，named entities 上达到 89.1%。由于测试书目中的一本《The Jungle Book》出现在 WebText，论文改报没有显著重叠的 validation 结果。

## 7. 规模曲线应怎样解读

多项任务随模型规模改善，支持“容量有助于隐式任务学习”。不过只有四个点，而且架构深度、宽度、学习率与训练动态同时变化。它展示了经验趋势，还不是后来意义上严格拟合的 scaling law。

更稳妥的结论是：在这组训练配置和数据上，扩大 decoder-only LM 通常同时改善 WebText 建模与多种零样本迁移指标。
