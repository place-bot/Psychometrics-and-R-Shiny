# NLP

自然语言处理研究如何把文本转化为可计算的表示，并在这些表示上完成预测、生成、检索、推理与决策。本站的 NLP 部分按“表示层级”和“建模问题”组织，而非按软件工具罗列。

## 学习主线

```text
离散符号
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

第一条主线从静态词向量开始，随后进入带注意力的序列到序列模型，再衔接完全基于 attention 的 Transformer。这样可以依次看清“词怎样获得向量”“模型怎样按生成步骤读取源句”以及“怎样移除 RNN 的串行状态链”。

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

## 后续专题接口

后续论文可以沿以下关系接入：

| 方向 | 要解决的问题 | 代表性方法 |
|---|---|---|
| 训练目标改进 | 全词表归一化仍然昂贵 | Negative Sampling、NCE |
| 子词表示 | 未登录词和形态信息缺失 | fastText |
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
