# GPT-2：语言模型中的零样本任务迁移

本专题精读 Radford et al. 的技术报告 **Language Models are Unsupervised Multitask Learners**。报告于 2019 年由 OpenAI 发布，研究对象是后来被称为 GPT-2 的 decoder-only Transformer。

## 一句话抓住论文

只用大规模、多来源网页文本训练同一个自回归语言模型，不为下游任务更新参数；再把文档、问题、任务提示或少量示例写进上下文，让模型通过“继续写下去”完成阅读理解、摘要、翻译和问答。

训练目标仍然只有 next-token prediction：

\[
\mathcal L_{\mathrm{LM}}(\theta)
=
-\sum_{t=1}^{T}\log p_\theta(x_t\mid x_{<t}).
\]

论文的重要主张是：当语料中自然包含很多“输入—输出”形式的文本，容量足够大的语言模型为了更好地预测文本，会顺带学习其中潜藏的任务结构。

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Alec Radford、Jeffrey Wu、Rewon Child、David Luan、Dario Amodei、Ilya Sutskever |
| 发布 | OpenAI technical report，2019 |
| 官方报告 | [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) |
| 官方说明 | [Better language models and their implications](https://openai.com/index/better-language-models/) |
| 官方代码 | [openai/gpt-2](https://github.com/openai/gpt-2) |
| 模型类型 | 仅含 Transformer decoder 的自回归语言模型 |

这份文献通常按 OpenAI 技术报告引用。有些二手文献列表将它写成 “OpenAI Blog 1.8 (2019): 9”，那不是正式的期刊卷期信息。

## 阅读路线

1. [研究问题、创新与证据边界](01-question-contributions.md)
2. [从语言模型到隐式多任务学习](02-lm-to-multitask.md)
3. [WebText：数据如何构造](03-webtext-data.md)
4. [Byte-level BPE：任何字符串都能编码](04-byte-bpe.md)
5. [GPT-2 架构与 GPT-1 的差别](05-architecture.md)
6. [任务如何写成上下文](06-zero-shot-protocol.md)
7. [语言建模实验与规模效应](07-language-modeling-experiments.md)
8. [阅读理解、摘要、翻译与问答结果](08-transfer-experiments.md)
9. [泛化、记忆与数据重叠](09-generalization-memorization.md)
10. [官方代码精读](10-code-reading.md)
11. [完整前向与生成例子](11-worked-example.md)
12. [局限、结论与通向 GPT-3](12-limitations-conclusion.md)
13. [参考文献与一手资料](references.md)

## 读完应形成的主线

```text
多样网页语料
   ↓ 只做 next-token prediction
共享的 decoder-only Transformer
   ↓ 任务描述、输入和示例都写成 token
条件生成 p(output | prompt)
   ↓ 不更新参数
跨任务零样本或上下文示例迁移
```

GPT-2 把“预训练后针对每个任务微调”的路线向前推了一步：下游任务可以直接通过文本上下文调用。GPT-3 随后把上下文中的 zero-shot、one-shot 与 few-shot 明确定义并系统比较。
