# 预训练数据、配置与优化

## 1. 语料

| 语料 | 规模 |
|---|---:|
| BooksCorpus | 约 8 亿词 |
| English Wikipedia | 约 25 亿词 |
| 合计 | 约 33 亿词 |

Wikipedia 只保留文本段落，忽略列表、表格和标题。

## 2. 训练长度

总计 1,000,000 步、batch 256 序列：

- 前 90% 步最大长度 128；
- 后 10% 步最大长度 512。

后 10% 用于学习长位置 embedding。满长 batch 相当于

\[
256\times512=131{,}072
\]

token，论文近似写作 128k words/batch。

## 3. 优化器

- Adam with weight decay；
- learning rate \(10^{-4}\)；
- \(\beta_1=0.9,\beta_2=0.999\)；
- \(L_2\) weight decay 0.01；
- 前 10,000 步 warmup；
- 之后线性衰减；
- dropout 0.1；
- GELU 激活。

## 4. 硬件与时间

论文附录：

- Base：4 个 Cloud TPU，共 16 个 TPU chips；
- Large：16 个 Cloud TPU，共 64 个 TPU chips；
- 两者预训练约 4 天。

## 5. 初始化与结构

所有层 FFN 维度为 \(4H\)。BERT 延续原始 Transformer encoder 的多头 attention、残差与 LayerNorm，使用可学习位置 embedding 和 GELU。

## 6. 微调建议

GLUE 使用 batch 32、3 epochs，从

\[
\{5,4,3,2\}\times10^{-5}
\]

中选择学习率。Large 在小数据集上有不稳定性，论文使用多次随机重启并按开发集选择。

## 7. 预训练与微调 checkpoint

每个下游任务从同一预训练权重初始化，随后形成独立微调模型。今天也可用 LoRA 等 PEFT 方法代替原论文的全量微调，但这属于后续适配策略。
