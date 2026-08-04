# 研究问题、创新与核心证据

## 1. 出发点

预训练加微调已经能在很多 NLP benchmark 上达到很强结果，但每个新任务往往还需要数千乃至数万条标注样本。作者把这种成本与人类快速理解新任务的能力对照：人通常能从一句说明或几个例子开始执行任务。

论文提出的问题是：

> 扩大通用语言模型后，能否仅通过推理上下文中的任务描述和少量示例完成新任务，并避免任何任务专用梯度更新？

## 2. 实验操作化

作者训练八种规模模型：

\[
125\mathrm M,350\mathrm M,760\mathrm M,1.3\mathrm B,
2.7\mathrm B,6.7\mathrm B,13\mathrm B,175\mathrm B.
\]

随后在大量任务上同时改变：

- 模型规模；
- 上下文示例数 \(K\)；
- zero-shot、one-shot、few-shot 设置；
- prompt 与答案格式。

主要问题因此可以写成：

\[
\operatorname{Performance}=f(N,K,\text{task},\text{prompt}),
\]

其中 \(N\) 是参数量。

## 3. 主要贡献

### 3.1 175B 自回归模型

最大模型有 96 层、隐藏宽度 12,288、96 个 attention heads，上下文长度 2048。论文训练使用 3000 亿 token。

### 3.2 系统定义四种学习设置

论文清楚区分 fine-tuning、few-shot、one-shot 与 zero-shot，使 GPT-2 中混在一起的“无参数更新迁移”得到可比较的实验定义。

### 3.3 规模与上下文学习共同增长

zero-shot 通常随参数量改善；few-shot 往往增长得更快，导致大模型中 zero/one/few-shot 之间的差距扩大。作者把它解释为更大模型更善于从上下文示例推断任务。

### 3.4 广泛任务评测

任务覆盖：

- 语言建模与 cloze；
- 闭卷事实问答；
- 翻译；
- 常识与阅读理解；
- SuperGLUE；
- 算术、单词重排与新词使用；
- 新闻生成与人工辨别。

### 3.5 污染与社会影响分析

论文为 benchmark 构造 clean subset，检查训练数据 13-gram 重叠；还讨论误用、偏差、能耗、新闻生成和部署难度。

## 4. 最强证据是什么

最有说服力的模式并非某一项 SOTA，而是二维趋势：

1. 模型规模增大，整体表现改善；
2. 上下文示例增多，尤其在大模型上带来更大收益。

例如 SuperGLUE 中，175B 模型从更少示例到 32 个示例时继续改善；论文汇总的 42 个 accuracy 类任务也呈现 few-shot 曲线比 zero-shot 更快上升。

## 5. 创新边界

GPT-3 沿用了 GPT-2 的 decoder-only Transformer、pre-normalization、可逆 tokenizer 和自回归目标，只把 attention pattern 部分替换为 dense 与 locally banded sparse attention 交替。

因此论文贡献集中于：

- 模型、数据与计算规模；
- 上下文学习的系统化评测；
- 能力、污染和社会影响的广泛分析。

## 6. 不能从论文直接推出的结论

- in-context learning 已经等价于人类学习；
- 模型形成了可解释的内层优化算法；
- 更大参数量在所有任务上都更好；
- few-shot 结果不受 prompt 与示例选择影响；
- benchmark 成绩等于开放环境可靠性；
- next-token prediction 单独足以达到通用智能。

论文自身列出了双向任务弱点、长文一致性、算术失败、污染、偏差、缺乏现实 grounding 和部署成本等限制。
