# 规模曲线与实验结果怎样解释

## 1. 论文观察到的总体趋势

在汇总的 42 个 accuracy 类 benchmark 上：

- zero-shot 随模型规模稳定改善；
- one-shot 通常高于 zero-shot；
- few-shot 往往增长最快；
- 规模越大，三种设置的差距经常越明显。

这支持“大模型更善于利用上下文示例”的行为结论。

## 2. 与 loss scaling 的关系

早期 scaling law 研究发现 validation loss 近似随参数、数据和计算呈幂律下降。可概念化为：

\[
L(N)\approx L_\infty+aN^{-\alpha}.
\]

GPT-3 进一步检查下游任务表现是否也随 \(N\) 平滑变化。许多任务大致平滑，但 accuracy 有阈值和饱和效应，并不总能由单一幂律准确描述。

## 3. 为什么 loss 小幅下降会带来 accuracy 大幅变化

分类只关心正确候选是否超过错误候选。设 margin：

\[
m
=
\log p(y_{\mathrm{correct}}\mid c)
-
\log p(y_{\mathrm{wrong}}\mid c).
\]

只要规模增长让许多样本的 \(m\) 从略小于 0 变为略大于 0，accuracy 就可能突然上升，即使平均 LM loss 只平滑改善。

## 4. 任务异质性

尺度趋势没有消除任务结构差异：

- LAMBADA、TriviaQA、COPA、ReCoRD 很强；
- WiC、DROP、高位数算术仍弱；
- one-shot 有时低于 zero-shot；
- few-shot 示例可能引入格式困惑。

因此不存在“175B 后所有任务自动解决”的统一断点。

## 5. SuperGLUE 比较的训练信息量

论文图中：

- fine-tuned BERT-Large 使用 SuperGLUE 约 125K 训练示例；
- BERT++ 还预先微调 MultiNLI 392K 与 SWAG 113K，总计约 630K 微调示例；
- GPT-3 few-shot 在每个任务上下文中使用最多 32 个示例，不做梯度更新。

这显示 GPT-3 的任务专用标签效率高。但 GPT-3 已使用 300B 无标签预训练 token 和远大计算，两种“数据效率”不能只按下游标签数概括。

## 6. 参数效率与计算效率

175B 模型用极少任务标签实现适配，却在每次推理中激活全部模型参数并重复读取 demonstrations。它在任务切换上高效，在单次算力、显存和延迟上很昂贵。

## 7. 缺少哪些消融

论文主要比较模型规模与 shot 数，没有完全分离：

- 训练 token 数；
- 数据过滤与 mixture；
- dense/sparse attention；
- 宽度与深度；
- tokenizer；
- prompt 模板；
- 示例选择策略。

所以“规模”代表整个 scaling recipe 的合成变化。

## 8. 对涌现的谨慎理解

某些离散指标看似在大模型突然出现，可能来自：

- 底层概率 margin 平滑跨过决策阈值；
- 指标饱和或不连续；
- prompt 与 decoding 非线性；
- 小样本方差。

GPT-3 提供了大规模能力曲线的早期关键证据。判断真正的机制相变，还需要更密集模型规模、连续指标与统计不确定性。
