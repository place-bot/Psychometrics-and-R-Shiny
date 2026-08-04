# Ghost Attention 与多轮一致性

## 1. 问题

系统指令常要求整个对话持续遵守约束，例如：

- 始终用法语；
- 回答简短；
- 扮演某位人物；
- 保持固定风格。

早期 RLHF 模型经过几轮后会忘记第一轮指令。虽然 system message 仍在上下文里，模型没有学会长期把它作为高优先级条件。

## 2. 对话表示

多轮数据写成：

\[
[u_1,a_1,u_2,a_2,\ldots,u_n,a_n],
\]

全局指令为 \(I\)。理想行为要求：

\[
a_t\sim p_\theta(a_t\mid I,u_1,a_1,\ldots,u_t)
\]

对所有 \(t\) 都持续受 \(I\) 约束。

## 3. GAtt 数据构造

第一步，在合成版本中把指令拼到每个 user turn：

\[
[I+u_1,a_1,I+u_2,a_2,\ldots,I+u_n].
\]

让最新 RLHF 模型在这个强提醒上下文中生成最后回答 \(a_n^+\)。

第二步，训练输入只在第一轮保留指令：

\[
[I+u_1,a_1,u_2,a_2,\ldots,u_n,a_n^+].
\]

对前面所有轮次 token 的 loss 置零，只在最后回答上反向传播。模型学习在没有逐轮重复提醒时复现强提醒版本的行为。

## 4. 为什么叫 Ghost Attention

训练目标让后期回答继续依赖已经远离当前位置的最初指令。指令没有在每轮真实出现，却像“幽灵”一样持续影响对话。

论文的 attention visualization 显示 GAtt 后模型在更长对话中对 system instruction 维持较强 attention activation。这是相关机制证据，不能证明单个 attention 权重就完整解释行为。

## 5. 合成约束

训练使用：

- hobbies；
- language；
- public figure。

最终指令随机组合多个约束，并有一半概率改成更短表达，例如把完整扮演指令压成简短标签，以增加措辞多样性。

## 6. 泛化

GAtt 在训练中未直接出现的约束，例如 “Always answer with Haiku”，也能表现出一定 zero-shot 延续。论文报告在达到 4K context limit 前可保持 20 多轮一致性。

## 7. Loss mask 的关键作用

若训练时对所有历史 assistant answer 也计算 loss，这些旧答案可能来自没有 GAtt 行为的原对话，与新系统指令不一致。把历史 token loss 置零，训练只要求最后回答遵循 system message：

\[
\mathcal L_{\mathrm{GAtt}}
=
-\sum_{t\in a_n^+}
\log p_\theta(t\mid I,\text{history}).
\]

## 8. 局限

- 指令仍受 4096-token window 限制；
- 训练约束类型较少；
- 冲突 system/user 指令的优先级没有完全解决；
- 论文版本不支持对话中途正式修改 system message；
- 长对话安全性可能下降；
- 持续 attention 不保证事实与任务状态正确。

GAtt 的价值是把“多轮记住系统指令”变成专门的数据构造与 loss mask 问题。
