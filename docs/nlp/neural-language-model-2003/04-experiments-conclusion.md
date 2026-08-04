# 数据、结果、局限与后续影响

## 1. Brown corpus

最佳验证设置对应的 neural + trigram mixture 测试 perplexity 为 252；最佳 n-gram/类别模型约 312，差异约 24%。删除插值 trigram为 336，比最佳 neural mixture 高约 33%。

增加上下文从 2 个词到 4 个词帮助 neural model，却没有明显帮助 n-gram，支持分布式表示利用较长上下文的主张。

## 2. AP News

neural mixture 测试 perplexity 109；最佳 Kneser–Ney 5-gram 为 117，约改善 8%。规模更大时差距缩小，但仍有优势。

## 3. 证据

实验支持：

- 联合学习表示与概率优于当时强 n-gram；
- hidden units 有帮助；
- neural 与 trigram mixture 进一步降低 perplexity；
- 分布式表示能从相似上下文泛化。

## 4. 局限

- 固定窗口，无法处理任意长依赖；
- 全词表 softmax昂贵；
- embedding 静态，一词多义共享一个向量；
- 训练资源巨大；
- 两个语料、perplexity 为主，任务迁移尚未验证；
- OOV 与输出词表示仍有限。

## 5. 历史影响

它建立了“embedding + 神经条件概率 + 端到端最大似然”的基本模板。RNN LM 移除固定窗口，Word2Vec简化表示训练，Transformer并行建模上下文，BERT再把语言目标用于大规模迁移学习。

## 6. 结论

语言建模给预训练提供了无需人工标签的预测信号。Bengio et al. (2003) 展示了词向量和语言概率可以共同学习，是理解后续神经预训练的关键起点。
