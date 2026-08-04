# 完整前向与生成例子

## 1. 简化设定

考虑 prompt：

```text
Article: Cats sleep for many hours each day.
TL;DR:
```

为便于手算，只保留四个 token：

\[
(x_1,x_2,x_3,x_4)
=
(\text{Cats},\text{sleep},\text{TL;DR},\text{:}).
\]

模型需要预测第 5 个 token。

## 2. 输入向量

每个位置：

\[
\mathbf h_t^{(0)}
=
\mathbf e(x_t)+\mathbf p_t.
\]

假设一个注意力头在最后位置产生 query \(\mathbf q_4\)，四个位置产生 keys \(\mathbf k_1,\ldots,\mathbf k_4\)。

## 3. causal attention 分数

最后位置允许看全部已有位置：

\[
s_{4j}
=
\frac{\mathbf q_4^\top\mathbf k_j}{\sqrt{d_h}},
\qquad j\le4.
\]

设分数为

\[
(s_{41},s_{42},s_{43},s_{44})
=(1.2,0.4,1.8,0.9).
\]

softmax 得到近似权重：

\[
\boldsymbol\alpha_4
\approx
(0.261,0.117,0.475,0.147).
\]

上下文向量为

\[
\mathbf a_4
=
0.261\mathbf v_1
+0.117\mathbf v_2
+0.475\mathbf v_3
+0.147\mathbf v_4.
\]

这里 `TL;DR` 位置权重较高，说明最后状态会强烈读取任务提示；它也读取文章词，才能决定摘要内容。

## 4. 经过残差、MLP 和最终 LayerNorm

简写为

\[
\mathbf h_4^{(1)}
=
\mathbf h_4^{(0)}
+\mathbf W_O\mathbf a_4
+\operatorname{MLP}(\cdot).
\]

真实 GPT-2 会重复 12–48 个 block，最后得到

\[
\mathbf h_4^{\mathrm{final}}.
\]

## 5. 输出 token 概率

设候选 token 只有三个，logits 为：

\[
z=(2.0,1.2,0.3)
\]

分别对应 `(Cats, They, Sleeping)`。softmax 为：

\[
p\approx(0.620,0.279,0.101).
\]

greedy decoding 会选 `Cats`；sampling 可能选到另外两个。

## 6. temperature 的影响

当 \(\tau=0.5\)：

\[
z/\tau=(4.0,2.4,0.6),
\]

分布更尖，最高概率 token 更容易被选。当 \(\tau=2\)：

\[
z/\tau=(1.0,0.6,0.15),
\]

分布更平，生成更多样也更不稳定。

## 7. top-k

若 \(k=2\)，第三个 token 被屏蔽，在前两个 token 内重新归一化：

\[
p_{\mathrm{top\text{-}2}}
\approx
(0.690,0.310,0).
\]

论文摘要实验使用很小的 \(k=2\)，目的是减少重复并限制离谱 token，但也显著收窄了生成空间。

## 8. 第二步与 KV cache

假设第一步生成 `Cats`。第二步条件变为：

\[
p(x_6\mid x_1,x_2,x_3,x_4,\text{Cats}).
\]

前四个 prompt token 的 K/V 已保存在 cache 中，只需计算新 token 的 query、key、value，再让新 query 对全部 cached keys 做 attention。

## 9. 任务行为从哪里来

这个前向过程没有“摘要模块”。`TL;DR:` 之所以有效，来自训练语料中它与摘要式后文的统计关联。模型把：

\[
\text{任务格式} + \text{文章内容} + \text{已有生成}
\]

共同编码进隐藏状态，再通过同一个 next-token head 输出。若训练语料中提示模式不足、文章超出上下文或解码策略不合适，摘要行为就会失败。
