# GPT-3：语言模型中的上下文学习

本专题精读 Brown et al. 的 **Language Models are Few-Shot Learners**，正式发表于 NeurIPS 2020。论文把 GPT-2 的上下文任务调用扩大到 1750 亿参数，并系统区分 zero-shot、one-shot 与 few-shot。

## 一句话抓住论文

先用 3000 亿 token 训练一个通用自回归语言模型；面对新任务时，把任务说明和少量“输入—答案”示例放进 2048-token 上下文，让模型直接预测新答案，全程不进行梯度更新。

## 核心机制

对 demonstrations

\[
D_K=\{(x_1,y_1),\ldots,(x_K,y_K)\}
\]

和新输入 \(x_*\)，模型计算

\[
p_\theta(y_*\mid D_K,x_*).
\]

预训练参数 \(\theta\) 保持固定。示例改变的是当前上下文中的隐藏状态与条件分布。

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Tom B. Brown 等 31 位作者 |
| 发表 | Advances in Neural Information Processing Systems 33，2020，1877–1901 |
| 正式论文 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) |
| 完整版本 | [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) |
| 官方发布仓库 | [openai/gpt-3](https://github.com/openai/gpt-3) |
| 模型 | 125M–175B 的八个 decoder-only Transformer |

## 阅读路线

1. [研究问题、创新与核心证据](01-question-contributions.md)
2. [Zero-shot、One-shot、Few-shot 与 Fine-tuning](02-learning-settings.md)
3. [In-context learning 的概率形式](03-in-context-mechanism.md)
4. [模型架构、八种规模与 sparse attention](04-architecture-scaling.md)
5. [训练数据、过滤与混合采样](05-data-pipeline.md)
6. [训练过程、并行化与计算成本](06-training-compute.md)
7. [Prompt 构造与评测协议](07-evaluation-protocol.md)
8. [语言建模、问答、翻译与 SuperGLUE](08-core-experiments.md)
9. [算术、词操作、新闻生成等能力](09-synthetic-qualitative.md)
10. [为什么作者称它为 Meta-learning](10-meta-learning-interpretation.md)
11. [规模曲线与实验结果怎样解释](11-scaling-analysis.md)
12. [Benchmark 污染与 clean subset](12-contamination.md)
13. [官方仓库、复现边界、局限与结论](13-repository-limitations-conclusion.md)
14. [参考文献与一手资料](references.md)

## 与前文的关系

```text
GPT-2
  大模型可在没有下游参数更新时显露多任务行为
       ↓ 规模扩大约两个数量级
GPT-3
  系统研究上下文中的 0/1/K 个示例如何改变任务表现
       ↓ 后续问题
指令微调、检索、工具使用、对齐与更可靠的推理
```

GPT-3 的核心创新主要来自规模化实验和接口验证。它没有发明新的训练目标，也没有为每个任务训练新模块；论文的关键贡献是证明大模型的 in-context adaptation 随规模显著增强。
