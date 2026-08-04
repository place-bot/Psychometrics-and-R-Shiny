# 预训练数据、tokenizer 与优化

## 1. 数据来源

论文描述训练语料为“公开可获得来源的新混合”，没有使用 Meta 产品或服务的用户数据。作者移除了某些已知包含大量私人个体信息的网站，并对高事实性来源上采样，希望提高知识质量、减少 hallucination。

精确语料清单和各来源比例没有公开。这限制了外部污染审计、偏差复核和完全复现。

## 2. 2T token 的选择

Llama 2 全部规模训练 2 万亿 token。论文表示这是性能与成本的折中；训练曲线在 2T 时仍未出现明显饱和。

相对 Llama 1：

- 7B/13B 从 1.0T 增至 2.0T；
- 大模型从 1.4T 增至 2.0T；
- 上下文从 2048 增至 4096。

## 3. Tokenizer

沿用 Llama 1 的 SentencePiece BPE：

- vocabulary size 为 32K；
- 所有数字拆成单个 digit；
- unknown UTF-8 字符进一步拆成 bytes；
- 保留 BOS 与 EOS 特殊 token。

数字拆位例如：

\[
2026\longrightarrow 2,0,2,6.
\]

这减少未见数字组合，但加长数值序列，也没有自动赋予模型精确算术能力。

## 4. 优化器与调度

预训练使用 AdamW：

\[
\beta_1=0.9,
\quad
\beta_2=0.95,
\quad
\epsilon=10^{-5}.
\]

其他配置：

- warmup 2000 steps；
- cosine learning-rate decay；
- 最终学习率为 peak 的 10%；
- weight decay 0.1；
- gradient clipping 1.0；
- global batch size 4M token。

7B/13B peak learning rate 为 \(3\times10^{-4}\)，34B/70B 为 \(1.5\times10^{-4}\)。

## 5. 训练硬件

使用 Meta Research SuperCluster 与内部 production clusters，均配 NVIDIA A100。两套集群分别使用 InfiniBand 与 RoCE 网络，端点带宽 200 Gbps；GPU 功耗上限为 400W 或 350W。

论文称 RoCE 在最多约 2000 GPU 时可接近更昂贵 InfiniBand 的扩展表现，这是基础设施层面的经验结果。

## 6. GPU hours 与碳排估计

| 模型 | GPU hours | 估计功耗 | tCO2eq |
|---|---:|---:|---:|
| 7B | 184,320 | 400W | 31.22 |
| 13B | 368,640 | 400W | 62.44 |
| 34B | 1,038,336 | 350W | 153.90 |
| 70B | 1,720,320 | 400W | 291.42 |
| 合计 | 3,311,616 | — | 539.00 |

估计没有计入互联、非 GPU 服务器、冷却和硬件制造。Meta 表示通过可持续项目直接 offset 了 100% 排放；offset 不会消除训练实际消耗的能源。

## 7. 数据分析

fastText 语言识别结果约为：

- English 89.70%；
- unknown 8.38%，部分来自代码；
- 其余单个语言大多低于 0.2%。

论文用 HateBERT 对 10% 语料随机样本评分，约 0.2% 文档的 toxicity likelihood 不低于 0.5。作者没有大规模 scrub toxic data，理由包括下游泛化、避免 demographic erasure 以及让基础模型可用于有害内容识别；代价是 base model 部署前必须额外安全调优。

## 8. 基础模型与数据目标

上采样事实源、不过度清除敏感文本和后续安全对齐共同构成策略。它要求清楚区分：基础模型追求广泛覆盖；聊天模型再通过 alignment 调整可接受输出行为。
