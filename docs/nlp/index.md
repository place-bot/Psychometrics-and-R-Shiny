# NLP

自然语言处理研究如何把文本转化为可计算的表示，并在这些表示上完成预测、生成、检索、推理与决策。本站的 NLP 部分按“表示层级”和“建模问题”组织，而非按软件工具罗列。

## 学习主线

```text
离散符号
   │
   ├── 分词与输入编码：BPE、Byte-level BPE、WordPiece
   │
   ├── 词与子词表示：Word2Vec、GloVe、fastText
   │
   ├── 上下文表示：ELMo、BERT 与预训练语言模型
   │
   ├── 序列建模：RNN、CNN、Transformer
   │
   ├── 任务学习：分类、标注、检索、生成
   │
   └── 评价与解释：相似性、迁移能力、偏差与稳健性
```

学习路线先从静态词向量理解“离散词怎样获得向量”，再补上字符串到 token ID 的子词分词层；随后进入带注意力的序列到序列模型，并衔接完全基于 attention 的 Transformer。这样可以依次看清输入单位怎样形成、模型怎样按生成步骤读取源句，以及怎样移除 RNN 的串行状态链。

## 词表示与 Word2Vec

### Mikolov et al. (2013)

[Efficient Estimation of Word Representations in Vector Space](word2vec-2013/index.md) 提出 Continuous Bag-of-Words（CBOW）和 Continuous Skip-gram 两种高效架构。论文的核心贡献包括：

- 删除传统神经语言模型中计算昂贵的非线性隐藏层；
- 用 CBOW 从上下文预测中心词；
- 用 Skip-gram 从中心词预测附近词；
- 结合 Huffman 树上的 hierarchical softmax，把输出计算从词表规模降到路径长度；
- 用语义—句法类比题系统评价向量中的线性规律；
- 证明简单模型、更多语料和更高维向量可以形成很强的词表示。

这篇论文适合作为 NLP 表示学习的起点，因为它同时连接了语言模型、表示学习、对比式预测目标、近似归一化、规模化训练和表示评价。

## 子词分词

### BPE、Byte-level BPE 与 WordPiece

[子词分词专题](subword-tokenization/index.md)解释文本怎样从字符串变成模型可处理的 token IDs，并区分三条经常被混写的路线：

- 原始 BPE 如何从数据压缩演化为基于高频 pair 的子词学习；
- GPT-2 如何用可逆 UTF-8 字节映射构造 byte-level BPE；
- BERT 如何把 BasicTokenizer 与 WordPiece longest-match-first 串联起来。

专题完整讲解训练算法、merge rank、WordPiece likelihood 思想、`Ġ` 与 `##`、手算过程、官方代码、offset mapping、多语言效率和 tokenizer 评价。它也明确标注 BERT 并未公开当年 WordPiece 词表训练器，因此不会把社区重构的 pair score 当成已公开的内部实现。

## 神经机器翻译与注意力

### Bahdanau, Cho & Bengio (2015)

[Neural Machine Translation by Jointly Learning to Align and Translate](bahdanau-attention-2015/index.md) 针对固定向量 Encoder–Decoder 的长句瓶颈，为每个目标步骤重新计算源位置权重：

\[
e_{ij}=a(\mathbf s_{i-1},\mathbf h_j),\qquad
\alpha_{ij}=\operatorname{softmax}_j(e_{ij}),\qquad
\mathbf c_i=\sum_j\alpha_{ij}\mathbf h_j.
\]

专题完整讲解双向 GRU、additive attention、端到端梯度、deep output、beam search、WMT14 实验和 GroundHog 代码，并设专节解释 RNN 的递归依赖为什么限制训练并行化。

## Transformer、预训练与参数高效适配

| 专题 | 核心问题 |
|---|---|
| [Attention Is All You Need](transformer-2017/index.md) | 怎样用 self-attention 移除 RNN 训练中的位置递归 |
| [LoRA](lora-2022/index.md) | 怎样用低秩增量高效适配 Transformer |
| [BERT](bert-2019/index.md) | 怎样用 MLM 预训练深层双向 Transformer encoder |

## BERT 术语对应的四篇代表文献

“先进行语言建模预训练，再针对任务微调”涉及不同抽象层级。本站按用户指定顺序在 BERT 后分别展开：

1. [迁移学习：Pan & Yang (2010)](transfer-learning-2010/index.md)
2. [语言建模：Bengio et al. (2003)](neural-language-model-2003/index.md)
3. [预训练：Dai & Le (2015)](sequence-pretraining-2015/index.md)
4. [微调：ULMFiT (2018)](ulmfit-2018/index.md)

## 自回归大语言模型与对话对齐

从 GPT-2 到 GPT-3 再到 Llama 2，可以连续看到三次重点转移：先检验大规模语言模型能否零样本迁移，再系统研究 in-context learning，随后把重点推进到开放权重基础模型的 SFT、偏好建模与 RLHF。

1. [GPT-2：Language Models are Unsupervised Multitask Learners](gpt2-2019/index.md)
2. [GPT-3：Language Models are Few-Shot Learners](gpt3-2020/index.md)
3. [Llama 2：Open Foundation and Fine-Tuned Chat Models](llama2-2023/index.md)

## 模型家族与 LLM 软件栈

论文路线之外，两个专题负责建立现代模型选型和系统实现的横向地图：

| 专题 | 核心问题 |
|---|---|
| [Command R、Mistral、Phi 与 Llama](open-weight-model-families/index.md) | 怎样比较模型家族的架构、定位、部署与开放权重许可证 |
| [Transformers、llama.cpp 与 LangChain](llm-software-stack/index.md) | 模型库、推理运行时与应用编排框架分别负责哪一层 |

“代码公开”“权重可下载”“允许商用”“完整训练可复现”需要分别判断。本站在介绍模型时会落实到精确检查点和许可证，不按品牌统一贴上“开源”标签。

## LLM 应用全景与书籍导读

### Pai (2025)

[《Designing Large Language Model Applications》专题导读](designing-llm-applications-2025/index.md)把单篇论文路线扩展为一张端到端系统地图。专题依照“模型从哪里来—怎样适配与运行—怎样组成应用”三层结构，讲解预训练数据、词表与 tokenizer、架构与学习目标、模型选择、微调、对齐、推理优化、工具调用、embedding、RAG 和系统架构。

书中关于 tokenizer 的讨论在这里作为全系统入口：tokenization 会同时影响上下文预算、跨语言效率、延迟、embedding 和下游数据管线；BPE、Byte-level BPE 与 WordPiece 的算法推导和官方代码则由[子词分词专题](subword-tokenization/index.md)承接。导读还单独给出 CAT 场景的映射，说明实时选题、状态更新、约束检查和生成模型分别处在系统的哪一层。

## 后续专题接口

后续论文可以沿以下关系接入：

| 方向 | 要解决的问题 | 代表性方法 |
|---|---|---|
| 训练目标改进 | 全词表归一化仍然昂贵 | Negative Sampling、NCE |
| 词内子串特征 | 静态词向量缺少形态信息 | fastText |
| 全局共现 | 局部预测与矩阵分解的关系 | GloVe、SGNS-PMI 分析 |
| 一词多义 | 每个词只有一个静态向量 | 多原型词向量、上下文表示 |
| 上下文预训练 | 同一个词随句子改变表示 | ELMo、BERT |
| 现代序列模型 | 长距离依赖与并行计算 | Transformer |

## 阅读约定

专题会区分三种证据：

1. **论文明确写出的模型与实验**；
2. **由论文公式直接展开的推导**；
3. **后续工作或公开实现补充的细节**。

这种区分很重要。以 Word2Vec 为例，2013 年 1 月的论文主要采用 hierarchical softmax；常与 Word2Vec 绑定的 negative sampling、频繁词下采样和短语学习来自同年后续工作。
