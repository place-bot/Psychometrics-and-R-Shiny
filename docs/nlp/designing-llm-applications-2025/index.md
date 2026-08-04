# 《Designing Large Language Model Applications》专题导读

本专题围绕 Suhas Pai 的 **Designing Large Language Model Applications: A Holistic Approach to LLMs** 建立一套中文阅读地图。该书由 O’Reilly Media 于 2025 年出版，目标读者为中级到高级实践者，正文把 LLM 应用从训练数据、tokenizer 和模型架构，一直连接到微调、推理优化、agent、embedding、RAG 与系统设计。

## 这本书的关键价值

书名中的 *Applications* 容易让人以为内容主要是 API 调用。它实际采用一条更完整的工程链：

```text
数据
  ↓
Vocabulary 与 Tokenizer
  ↓
架构与训练目标
  ↓
选择 / 微调 / 对齐 / 推理优化
  ↓
工具、Embedding、RAG
  ↓
多模型系统架构
```

也就是说，应用行为不仅由 prompt 决定。训练数据、输入编码、模型目标、解码、检索和系统控制共同决定最终结果。

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Suhas Pai |
| 全名 | *Designing Large Language Model Applications: A Holistic Approach to LLMs* |
| 出版社 | O’Reilly Media |
| 版本 | 第一版，2025 年 3 月 |
| 难度 | Intermediate to advanced |
| 结构 | 3 Parts，13 Chapters |
| 官方页面 | [O’Reilly 书籍页面](https://www.oreilly.com/library/view/designing-large-language/9781098150495/) |

## 三部分结构

| Part | 书中章节 | 要回答的问题 |
|---|---|---|
| I. LLM Ingredients | 1–4 | 一个语言模型由哪些数据、输入单位、架构和目标组成 |
| II. Utilizing LLMs | 5–9 | 怎样选择、微调、对齐并高效运行模型 |
| III. LLM Application Paradigms | 10–13 | 怎样把模型接入工具、知识库、embedding 与完整系统 |

## 本专题阅读路线

1. [全书结构、知识依赖与阅读策略](01-book-map.md)
2. [预训练数据：质量、去重、混合与污染](02-pretraining-data.md)
3. [Vocabulary 与 Tokenization：和 BPE/WordPiece 专题怎样衔接](03-vocabulary-tokenization.md)
4. [Transformer 架构、Backbone 与学习目标](04-architectures-objectives.md)
5. [模型选型、加载、解码与结构化输出](05-model-selection-inference.md)
6. [Fine-tuning、PEFT 与领域适配](06-finetuning-domain-adaptation.md)
7. [Alignment、幻觉缓解与推理能力](07-alignment-reasoning.md)
8. [KV Cache、量化、蒸馏与推理加速](08-inference-optimization.md)
9. [外部工具、Agent Loop 与安全控制](09-tools-agents.md)
10. [Embedding、Chunking 与 RAG](10-embeddings-rag.md)
11. [多模型架构、Router 与 CAT 系统接口](11-system-architecture-cat.md)
12. [证据边界、局限、结论与未来更新](12-limitations-conclusion.md)
13. [官方页面与延伸文献](references.md)

## 与本站已有专题的关系

本专题负责横向连接，不重复展开已经精读过的全部数学细节：

- 分词细节见 [BPE、Byte-level BPE 与 WordPiece](../subword-tokenization/index.md)；
- 架构细节见 [Attention Is All You Need](../transformer-2017/index.md)；
- 参数高效微调见 [LoRA](../lora-2022/index.md)；
- 对齐流程见 [Llama 2](../llama2-2023/index.md)；
- 运行与编排工具见 [LLM 软件栈](../llm-software-stack/index.md)；
- 模型选型见 [开放权重模型家族](../open-weight-model-families/index.md)。

!!! note "内容边界"
    本站提供结构化导读、方法推导和系统化延伸，不复制受版权保护的整章正文。具体案例、图表与作者完整论述应回到正版书籍阅读。

