# Word2Vec 原始论文：CBOW、Skip-gram 与高效词表示

本专题精读 Tomas Mikolov、Kai Chen、Greg Corrado 与 Jeffrey Dean 的论文 **Efficient Estimation of Word Representations in Vector Space**。

论文面对的规模是数十亿词元、百万级词表和数百至上千维的向量。研究问题可以压缩为一句话：

> 怎样在有限计算预算下，从极大语料中学习高质量词向量？

## 一张图看论文

```text
大规模文本语料
      │ 滑动上下文窗口
      ▼
训练样本中的中心词与上下文词
      │
      ├── CBOW：多个上下文向量聚合 ──► 预测中心词
      │
      └── Skip-gram：中心词向量 ─────► 预测多个附近词
                              │
                              ▼
                 Huffman hierarchical softmax
                              │
                              ▼
                    每个词的连续向量
                              │
             ┌────────────────┴───────────────┐
             ▼                                ▼
       余弦近邻与类比                     下游 NLP 任务
```

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Tomas Mikolov、Kai Chen、Greg Corrado、Jeffrey Dean |
| 会议 | ICLR 2013 Workshop Poster |
| arXiv | [1301.3781](https://arxiv.org/abs/1301.3781) |
| 初次提交 | 2013 年 1 月 16 日 |
| 当前版本 | v3，2013 年 9 月 7 日 |
| 官方论文页 | [Google Research](https://research.google/pubs/efficient-estimation-of-word-representations-in-vector-space/) |

## 论文的真正主线

这篇文章常被概括成“两种词向量模型”，但全文的论证主线由四步组成：

1. 传统 NNLM 和 RNNLM 能学习词向量，但隐藏层与大词表输出层造成高计算成本。
2. 去掉非线性隐藏层后，每个训练样本的计算显著下降。
3. 节省下来的预算可以换成更多训练词元、更高向量维度和更大词表。
4. 规模扩张后的简单模型在语义—句法类比任务上超过更复杂的基线。

因此，CBOW 与 Skip-gram 的价值来自“目标设计 + 结构简化 + 数据规模”这一组合。

## 原文范围

论文明确讨论：

- 训练复杂度 \(O=E\times T\times Q\)；
- 前馈 NNLM、RNNLM、CBOW 与 Skip-gram 的复杂度；
- Huffman hierarchical softmax；
- 分布式 DistBelief 训练；
- 语义—句法类比数据集；
- 8 张实验表及其结果；
- Microsoft Sentence Completion Challenge；
- 词向量关系的若干例子。

论文没有完整写出 CBOW、Skip-gram 的概率目标与梯度。专题会依据文中的模型描述和 hierarchical softmax 机制补全推导，并明确标注这些展开。

## 推荐阅读路线

### 第一次：先建立模型直觉

1. [问题、文献身份与创新](01-paper-question-and-contributions.md)
2. [分布式词表示基础](02-distributed-representations.md)
3. [CBOW：从上下文预测中心词](05-cbow.md)
4. [Skip-gram：从中心词预测上下文](06-skip-gram.md)
5. [类比评测与向量运算](08-analogy-evaluation.md)

### 第二次：吃透计算与训练

1. [计算复杂度与神经语言模型基线](03-complexity-and-baselines.md)
2. [Huffman Hierarchical Softmax](04-hierarchical-softmax.md)
3. [SGD、反向传播与完整算法](07-training-algorithm.md)
4. [公开代码与最小实现](12-code-and-implementation.md)

### 第三次：判断证据强度

1. [实验设计与数据](09-experiment-design.md)
2. [实验结果与分析](10-results-and-analysis.md)
3. [线性规律的含义与边界](11-linear-regularities.md)
4. [局限、后续工作与现代位置](13-limitations-followups.md)
5. [符号表、结论与阅读地图](14-symbols-conclusion.md)

## 阅读完成后应能解释

- one-hot 编号与分布式表示的差别；
- 为什么删除隐藏层会带来数量级上的计算节省；
- CBOW 和 Skip-gram 各自构造什么条件概率；
- Huffman 树怎样把一个 \(V\) 类问题分解成若干二分类；
- 输入词向量和输出节点向量为何是两套参数；
- 动态窗口怎样改变远近上下文的采样频率；
- 类比题如何构造、怎样判定命中；
- Table 2–6 分别支持什么结论；
- negative sampling 为什么不应写进这篇论文的原始目标；
- 静态词向量在多义词、词序、形态和社会偏差方面有哪些限制。
