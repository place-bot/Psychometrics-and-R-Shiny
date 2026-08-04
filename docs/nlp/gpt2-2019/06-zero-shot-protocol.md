# 任务如何写成上下文

## 1. 统一接口

GPT-2 没有为摘要、翻译、问答分别添加输出头。每个任务都被转写成一个 prefix，再让语言模型续写：

\[
\hat y
=
\arg\max_y p_\theta(y\mid \text{prefix}).
\]

prefix 的内容与格式决定模型当前推断的任务。

## 2. 阅读理解 CoQA

输入由文档、对话历史以及最后的 `A:` 组成：

```text
Document: ...
Q: ...
A: ...
Q: ...
A:
```

论文使用 greedy decoding 生成回答，在开发集达到 55 F1。模型没有使用 CoQA 的 127,000 多个训练问答对更新参数。

## 3. 摘要

作者把文章放在前面，在末尾添加：

```text
TL;DR:
```

然后用 top-k sampling 生成 100 token，\(k=2\)，取前三个生成句子作为摘要。删除 `TL;DR:` 后，论文报告的 ROUGE 平均值下降 6.4 分，表明短提示确实改变了条件生成行为。

## 4. 翻译

上下文中放入若干配对格式：

```text
English sentence = French sentence
English sentence = French sentence
New English sentence =
```

最后使用 greedy decoding 取第一条生成句子。按 GPT-3 后来的术语，只要前面放了配对示例，这就属于 in-context few-shot，而不是严格的 zero-shot。

## 5. 事实问答 Natural Questions

同样先放若干短答案式问答对，让模型推断输出风格，然后输入新问题。模型的参数没有更新，但示例影响隐藏状态和后续 token 概率。

## 6. 多项选择与 cloze

若候选答案集合为 \(\mathcal A\)，可以给每个候选补全文本打分：

\[
S(a)
=
\sum_{r=1}^{|a|}
\log p_\theta(a_r\mid c,a_{<r}).
\]

选择

\[
\hat a=\arg\max_{a\in\mathcal A}S(a).
\]

对于 CBT，论文不只计算候选词本身，还计算把候选填回去后余下句子的概率，使候选受到后续一致性约束。

## 7. 生成策略也是实验设定的一部分

| 策略 | 规则 | 典型用途 |
|---|---|---|
| greedy | 每步选最高概率 token | 翻译、短答案 |
| beam search | 保留多条高分序列 | 结构较稳定的生成 |
| top-k | 只在概率最高的 \(k\) 个 token 中采样 | 摘要、开放生成 |
| temperature | logits 除以温度 \(\tau\) | 控制分布尖锐程度 |

同一模型、同一 prompt 在不同 decoding 下可能得到明显不同结果。因此零样本表现由模型、prompt、答案打分与解码规则共同决定。

## 8. 评测公平性问题

比较 GPT-2 与监督系统时应同时标注：

- GPT-2 没有使用该任务训练集做梯度更新；
- 它已经在大规模网页语料上训练；
- 网页里可能自然出现相同任务或相似文本；
- 有些“zero-shot”实验使用了上下文示例；
- 监督基线可能规模更小、训练域更窄；
- prompt 与输出后处理包含人工设计。

“没有下游训练”不能等同于“没有使用任何任务相关信息”。
