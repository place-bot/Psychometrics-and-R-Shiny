# 与全量微调、Adapter、Prefix、BitFit 比较

| 方法 | 训练内容 | 额外深度 | 占用 token 长度 | 可合并进原权重 |
|---|---|---:|---:|---:|
| Full FT | 全部参数 | 无 | 无 | 已是完整权重 |
| BitFit | bias | 无 | 无 | 可 |
| Adapter | 插入瓶颈层 | 有 | 无 | 通常不可直接等价合并 |
| Prefix/Prompt tuning | 可学习前缀激活/token | 无 | 有 | 否 |
| LoRA | 权重低秩增量 | 并行分支 | 无 | 是 |

## 1. Adapter latency

adapter 位于层间，需要在主路径上额外执行。论文在 GPT-2 medium、batch 1、序列长 128 的例子中，两个 adapter 变体相对 FT/LoRA 增加约 20.7% 和 30.3% latency。大 batch 下相对开销较小。

## 2. Prefix 的序列预算

可学习 prefix 占据上下文位置，减少真实任务 token 可用长度。原论文还观察到 prefix 参数增加时性能不单调，并将优化困难作为问题之一。

## 3. LoRA 的独特权衡

优势：

- 不增加网络深度；
- 可合并；
- 不占上下文；
- 小 checkpoint 易切换；
- 可与其他方法组合。

代价：

- rank 和 target modules 需要选择；
- 每任务仍需训练；
- 混合任务 batch 与合并权重存在冲突；
- 极低 rank 可能限制分布差异较大的任务。

## 4. 比较要保持公平

需要统一基座、数据、步数、超参数搜索、可训练参数预算、随机种子与推理设置。原论文部分 baseline 来自既有文献，表中星号标出，并非全部在完全同一代码环境重跑。
