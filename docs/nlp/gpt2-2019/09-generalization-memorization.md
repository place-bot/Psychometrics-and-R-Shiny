# 泛化、记忆与数据重叠

## 1. 为什么需要重叠审计

训练集来自互联网，benchmark 的原文也可能公开在互联网。若测试文本或近重复文本进入 WebText，零样本结果可能混入记忆效应。

论文把这个问题写成：某个评测 token 8-gram 是否也出现在 WebText training set。

## 2. Bloom filter 方法

作者先把字符串规范化为小写字母数字词，并用单空格连接，然后把 WebText 训练集的 8-gram 放入 Bloom filter。

Bloom filter 可能产生 false positive，但不会产生 false negative。参数被设定为理论 false positive rate 不高于

\[
10^{-8}.
\]

作者用 100 万个生成字符串检查，未发现 false positive。

## 3. 语言模型 benchmark 的重叠率

| 测试集 | 与自身 train 重叠 | 与 WebText train 重叠 |
|---|---:|---:|
| PTB | 2.67% | 0.88% |
| WikiText-2 | 0.66% | 1.63% |
| enwik8 | 7.50% | 6.31% |
| text8 | 2.34% | 3.94% |
| WikiText-103 | 9.09% | 2.42% |
| 1BW | 13.19% | 3.75% |

常见 LM test set 与 WebText 的平均重叠约 3.2%；这些 benchmark 自己的 train/test 平均重叠约 5.9%。这说明重叠并非 WebText 独有，但也不能因此忽略污染。

## 4. 分任务分析

### 4.1 Winograd

只有 10 个 schema 与 WebText 出现 8-gram 重叠；其中 2 个是伪匹配，剩余 8 个里只有 1 个上下文泄露了答案。

### 4.2 CoQA

新闻域约 15% 文档已在 WebText 中，模型在这些文档上约高 3 F1。综合 5 个开发域，作者估计重叠带来约 0.5–1.0 F1。CoQA 在 WebText 时间截点后发布，因此训练语料里没有正式训练问题与答案。

### 4.3 LAMBADA

平均重叠约 1.2%。移除所有存在重叠的例子后：

- perplexity 从 8.6 变为 8.7；
- accuracy 从 63.2% 变为 62.9%。

整体变化较小，因为显著重叠样本比例很低。

## 5. 训练与留出损失一起改善意味着什么

论文展示随着模型增大，WebText train 与 held-out loss 同时下降，而且差距没有显示严重扩大。作者据此判断最大 GPT-2 仍处于欠拟合状态。

这项证据反映整体分布层面的拟合，不足以排除个别文档被逐字记忆。一个模型可以总体欠拟合，同时精确记住少数高频或重复片段。

## 6. 方法局限

8-gram overlap 只能发现表面相同片段：

- 改写、翻译和格式变化可能漏检；
- 常见短语会产生无害匹配；
- 文档出现不等于答案出现；
- overlap 比例没有直接等价于性能膨胀；
- WebText 未公开，外部研究者无法复核完整索引。

论文建议在新数据集切分中使用 n-gram 去重作为 sanity check。GPT-3 把这个问题扩大到 13-gram 清洗集评测，并暴露出大规模训练中更复杂的污染检测难题。
