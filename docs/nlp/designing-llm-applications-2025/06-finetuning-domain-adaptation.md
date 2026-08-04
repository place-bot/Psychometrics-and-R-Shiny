# Fine-tuning、PEFT 与领域适配

## 1. 什么时候需要微调

微调适合改变稳定行为：

- 固定输出格式；
- 专业文体和术语；
- 分类、抽取与评分规则；
- 工具调用模式；
- 特定任务决策边界。

频繁变化的事实更适合检索。Prompt 已能稳定解决的问题可能无需训练。

## 2. 监督微调目标

给定 instruction \(x\) 与目标回答 \(y\)：

\[
\mathcal L_{\mathrm{SFT}}
=
-\sum_{t=1}^{|y|}
\log p_\theta(y_t\mid x,y_{<t}).
\]

通常只在 assistant 输出上计算 loss，system/user token 用作条件。

## 3. 优化参数

需要共同决定：

- learning rate 与 scheduler；
- batch size 与 gradient accumulation；
- sequence packing；
- epochs 与 early stopping；
- weight decay；
- max sequence length；
- mixed precision；
- gradient checkpointing。

数据量小并不意味着可以忽略验证集。过大学习率会破坏已有能力，过多 epochs 会记忆格式和样本。

## 4. LoRA

冻结原权重 \(W_0\)，训练低秩增量：

\[
W=W_0+\frac{\alpha}{r}BA,
\]

\[
A\in\mathbb R^{r\times d_{\mathrm{in}}},
\quad
B\in\mathbb R^{d_{\mathrm{out}}\times r}.
\]

LoRA 降低可训练参数和 optimizer state，详细机制见 [LoRA 专题](../lora-2022/index.md)。

## 5. Continual pre-training

领域语料没有 instruction-output 标签时，可继续使用 language-model objective：

\[
\mathcal L_{\mathrm{DAPT}}
=
-\sum_t\log p_\theta(x_t\mid x_{<t}).
\]

它改变领域语言分布，随后通常还需 instruction tuning 恢复任务接口。

## 6. Replay 与遗忘

只训练新领域数据会造成 catastrophic forgetting。Replay 混入通用数据：

\[
\mathcal L
=
\lambda\mathcal L_{\mathrm{domain}}
+(1-\lambda)\mathcal L_{\mathrm{general}}.
\]

\(\lambda\) 控制领域适配和通用能力保持。

## 7. Adapter merging 与 model fusion

多个 adapter 可以按任务动态加载、加权组合或合并。风险包括：

- 目标模块不兼容；
- tokenizer 和 base revision 不一致；
- 参数方向相互干扰；
- 每个 adapter 单独有效，组合后退化。

需要在组合版本上重新评价，不能从单 adapter 分数推断。

## 8. 数据质量大于格式数量

高质量 SFT 数据应包含清晰 instruction、正确 output、失败边界、拒答与难例。大量模板化合成数据可能造成风格坍缩和过度迎合。

## 9. CAT 适配

可微调模型理解题目内容、抽取知识点或生成反馈，但能力估计和选题约束仍应有显式测量层。训练集必须按学生与题目隔离，避免模型记住具体作答结果。

