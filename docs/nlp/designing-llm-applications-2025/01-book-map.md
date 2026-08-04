# 全书地图与阅读策略

## 1. 为什么先讲模型原料

LLM 应用经常从 API demo 开始：

```text
prompt → model → answer
```

真正部署时会出现一系列问题：模型为什么不认识术语、为什么不同语言 token 成本差异大、为什么长上下文失效、为什么微调破坏原有能力、为什么 RAG 有证据仍会答错。

这本书把这些问题回溯到更长的因果链：

\[
\text{Behavior}
=
f(
\text{data},
\text{tokenizer},
\text{architecture},
\text{objective},
\text{adaptation},
\text{inference},
\text{system}
).
\]

Part I 因而不是背景知识附录，而是后续应用决策的原因层。

## 2. Part I：LLM Ingredients

### Chapter 1：Introduction

从 LLM 历史、prompting、API 与 chatbot prototype 进入问题，并提出 prototype 到 production 的距离。

### Chapter 2：Pre-Training Data

讨论数据需求、公开语料、synthetic data、过滤、去重、PII、decontamination、data mixture 和公平性。

### Chapter 3：Vocabulary and Tokenization

讨论 vocabulary size、normalization、pre-tokenization、BPE、WordPiece 与 special tokens。

### Chapter 4：Architectures and Learning Objectives

从 Transformer 部件推进到 encoder-only、encoder-decoder、decoder-only、MoE，以及 full、prefix、masked language modeling。

## 3. Part II：Utilizing LLMs

| 章节 | 核心决策 |
|---|---|
| 5. Adapting LLMs | 选哪个模型、怎样加载、怎样解码和评价 |
| 6. Fine-Tuning | 怎样设计优化参数、数据和 PEFT 流程 |
| 7. Advanced Fine-Tuning | continual pretraining、replay、adapter merging 和 model fusion |
| 8. Alignment and Reasoning | 人类反馈、幻觉、verifier 和 inference-time compute |
| 9. Inference Optimization | cache、early exit、distillation、speculative decoding 与 quantization |

这一部分的主线是：

\[
\text{已有基础模型}
\longrightarrow
\text{任务可用模型}
\longrightarrow
\text{可承受成本的服务}.
\]

## 4. Part III：LLM Application Paradigms

### Chapter 10：External Tools

从被动模型调用推进到显式 tool call 与自主 agent，讨论 model、tool、store、loop、guardrail、verifier 与 orchestration。

### Chapter 11：Representation Learning and Embeddings

覆盖 semantic search、embedding fine-tuning、Matryoshka、量化、chunking 与 vector database。

### Chapter 12：RAG

把 RAG 拆成 rewrite、retrieve、rerank、refine、insert、generate，并比较 long context 与 fine-tuning。

### Chapter 13：Design Patterns and System Architecture

讨论 multi-LLM、cascade、router、task-specialized models、DSPy 与 LMQL。

## 5. 三种阅读方式

### 模型研究路线

```text
Chapter 2 → 3 → 4 → 6 → 7 → 8 → 9
```

适合研究预训练、tokenizer、微调和模型机制。

### 应用工程路线

```text
Chapter 1 → 5 → 10 → 11 → 12 → 13 → 9
```

适合已有模型、需要构建系统的读者。

### CAT 研究路线

```text
Chapter 3
→ Chapter 5
→ Chapter 10
→ Chapter 11/12
→ Chapter 13
```

重点是题目内容编码、模型选型、工具约束、题库检索和自适应系统编排。

## 6. 推荐的阅读记录模板

每章都按五个问题记录：

1. 本章控制 LLM 生命周期的哪一层？
2. 输入、状态和输出分别是什么？
3. 优化目标或评价指标是什么？
4. 哪些结论来自实验，哪些是工程经验？
5. 与 CAT 的测量目标、内容约束和实时反馈怎样连接？

这样可以避免把大量技术名词读成互不相干的工具清单。

