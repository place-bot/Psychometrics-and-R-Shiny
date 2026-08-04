# 为什么作者称它为 Meta-learning

## 1. 两个时间尺度

作者提出一种解释：语言模型预训练像慢速 outer loop，上下文适配像快速 inner loop。

### Outer loop

在海量文本上通过梯度下降更新参数：

\[
\theta_{s+1}
=
\theta_s-eta\nabla_\theta
\mathcal L_{\mathrm{LM}}(\theta_s).
\]

模型跨越大量文档、格式和隐式任务，逐渐形成通用序列处理能力。

### Inner loop

推理时给定 demonstrations \(D_K\)：

\[
\mathbf H
=
F_{\theta}(D_K,x_*),
\]

再从 \(\mathbf H\) 产生答案。这里没有显式的

\[
\theta' = \theta-\alpha\nabla_\theta\mathcal L_{D_K}.
\]

快速适配由 activations 实现。

## 2. 与 MAML 对照

| 维度 | MAML | GPT-3 in-context learning |
|---|---|---|
| 外层训练 | 任务分布上的 meta-gradient | 网页文本上的 LM gradient |
| 内层输入 | support set | prompt demonstrations |
| 内层适配 | 参数梯度更新 | hidden states / attention |
| query 预测 | 用适配后参数 | 用同一参数、不同上下文 |
| 任务边界 | 训练中显式给出 | 自然文本中通常隐式存在 |

结构类比很有启发，但 GPT-3 预训练没有显式构造 MAML 的 episode，也没有直接优化“看 K 个示例后 query loss”。

## 3. 一个概念化算法

```text
预训练阶段：
  对海量文本执行 next-token gradient descent
  参数逐渐吸收跨文档、跨格式的规律

推理阶段：
  把 K 个示例编码进上下文
  self-attention 读取示例之间的共同结构
  对新输入生成答案
  不更新、不保存任务专用参数
```

## 4. 为什么大模型的 few-shot 增益更快

若仅有通用语言流畅性，增加示例未必产生额外收益。论文观察到大模型中 few-shot 曲线相对 zero-shot 拉开，说明容量可能被用于：

- 识别字段和标签；
- 推断示例映射；
- 在上下文中临时绑定新概念；
- 从相似示例检索模式；
- 根据多个示例消除任务歧义。

这些机制可能同时存在。论文只通过行为曲线支持 meta-learning 解释，没有唯一确定内部算法。

## 5. 一个贝叶斯式理解

可以把任务 \(z\) 当成潜变量：

\[
p(y_*\mid D_K,x_*)
=
\sum_z
p(y_*\mid x_*,z)
p(z\mid D_K).
\]

示例越多，\(p(z\mid D_K)\) 可能越集中，任务歧义减少。Transformer 不一定真的执行显式贝叶斯计算，这个公式提供了理解 prompt demonstrations 的抽象视角。

## 6. “快适配”仍受训练分布约束

模型能快速适配的任务，通常与预训练中见过的语言结构、算法片段或任务族有关。若规则完全陌生、需要超出上下文的记忆、精确长程计算或外部感知，激活层适配可能不足。

因此 in-context learning 更适合描述一种能力接口：从上下文改变行为。它本身不保证新任务来自真正的分布外归纳。
