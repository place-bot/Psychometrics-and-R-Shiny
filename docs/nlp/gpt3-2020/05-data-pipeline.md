# 训练数据、过滤与混合采样

## 1. 五类数据

GPT-3 使用过滤后的 Common Crawl、WebText2、两个 books corpora 与英语 Wikipedia。

| 数据集 | 可用 token 数 | 训练混合权重 | 训练 300B token 时经过的 epoch |
|---|---:|---:|---:|
| Common Crawl（过滤后） | 410B | 60% | 0.44 |
| WebText2 | 19B | 22% | 2.9 |
| Books1 | 12B | 8% | 1.9 |
| Books2 | 55B | 8% | 0.43 |
| Wikipedia | 3B | 3% | 3.4 |

表中权重四舍五入后合计为 101%。核心思想是高质量小语料被过采样，Common Crawl 与 Books2 没有遍历完整一轮。

## 2. Common Crawl 的规模变化

补充材料给出：

```text
2016–2019 年 41 个 Common Crawl 月度分片
        ↓
约 45 TB 压缩纯文本
        ↓ 质量过滤、模糊去重
约 570 GB
        ↓ byte-level BPE
约 400B token
```

最终训练只从过滤 Common Crawl 中采样约 180B token，占 300B 训练 token 的 60%。

## 3. 质量分类器

作者以 WebText、Wikipedia 和 books 等 curated corpora 为正例，以未过滤 Common Crawl 为负例，用 Spark tokenizer、HashingTF 与 logistic regression 训练质量分类器。

每篇文档得到 `document_score`，随后使用带随机性的重采样规则，优先保留高分文档，也保留少量分布外文本。补充材料给出的 Pareto 参数为

\[
\alpha=9.
\]

这种方法不会把 Common Crawl 简单截成固定分数阈值，而是形成偏向高质量的概率采样。

## 4. 模糊去重

作者使用 Spark MinHashLSH，10 个 hashes，在每个数据集内部以及数据集之间删除高度相似文档，并从 Common Crawl 中模糊删除 WebText。平均数据规模下降约 10%。

去重目标包括：

- 减少重复样本的训练权重；
- 降低 validation 泄漏；
- 缓解模型记忆；
- 保持数据多样性。

## 5. 混合采样不是按原始规模

若完全按 token 数采样，Common Crawl 会压倒其余语料。论文人为提高 WebText2、Books 与 Wikipedia 的权重，相当于接受高质量语料被重复看到，以交换更好的平均训练质量。

训练分布可写为混合模型：

\[
p_{\mathrm{train}}(x)
=
\sum_{m=1}^{5}w_m p_m(x),
\qquad
\sum_m w_m\approx1.
\]

\(w_m\) 是研究者选择的采样权重，并非互联网自然分布。

## 6. 语言分布

论文估计训练数据按 word count 约 93% 为英语、7% 为非英语。byte-level BPE 来自英语中心设计，因此多语言文本虽然可编码，token 效率与模型性能仍不均衡。

## 7. 数据偏差

官方模型卡指出，互联网训练数据更代表联网人群，并偏向发达国家、年轻、富裕、男性和美国中心观点。过滤分类器还会把“与既有 curated corpora 相似”当成质量标准，进一步固化参考语料的文化与文体偏好。

## 8. 数据管线的证据边界

官方仓库发布了语言统计、样本和部分 overlap 记录，没有发布完整训练 corpus、质量分类器模型和可复现数据清单。因此外部读者能理解方法，无法精确重建每一个训练 token。
