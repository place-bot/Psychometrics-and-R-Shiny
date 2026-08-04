# In-context learning 的概率形式

## 1. 预训练目标没有改变

GPT-3 仍最小化自回归交叉熵：

\[
\mathcal L_{\mathrm{pretrain}}(\theta)
=
-\mathbb E_{x\sim\mathcal D}
\sum_{t=1}^{T}
\log p_\theta(x_t\mid x_{<t}).
\]

训练时没有专门的 few-shot loss，也没有显式把每个网页切成 support set 与 query set。

## 2. Prompt 把任务变成条件概率

设一个分类任务有示例：

```text
Review: wonderful movie
Sentiment: positive

Review: boring plot
Sentiment: negative

Review: delightful acting
Sentiment:
```

模型比较：

\[
p_\theta(\text{positive}\mid c)
\quad\text{与}\quad
p_\theta(\text{negative}\mid c).
\]

示例既说明标签语义，也说明输出格式和输入到输出的映射。

## 3. 序列级答案打分

若答案 \(y=(y_1,\ldots,y_m)\)，其条件对数概率为

\[
\log p_\theta(y\mid c)
=
\sum_{r=1}^{m}
\log p_\theta(y_r\mid c,y_{<r}).
\]

多项选择任务可以对每个候选 \(a\in\mathcal A\) 计算分数后取最大值：

\[
\hat a
=
\arg\max_{a\in\mathcal A}
S(a;c).
\]

根据任务，论文会使用 raw probability、长度归一化或候选间归一化；这些细节会改变准确率。

## 4. 示例如何进入每一层

对 query 位置 \(t\)，self-attention 可以读取整个左侧 prompt：

\[
\mathbf h_t^{(\ell)}
=
F_\ell
\left(
\mathbf h_{\le t}^{(\ell-1)}
\right).
\]

较早示例的 token 通过 K/V 影响当前 query 的 attention 输出。层层组合后，当前隐藏状态可以编码：

- 当前任务类别；
- 输入和输出字段边界；
- 标签词含义；
- 示例中共同的转换规律；
- 当前新输入与示例的相似性。

论文没有直接识别每一层具体实现了哪种算法。这些是机制上允许的计算，不是已被逐层证明的内部解释。

## 5. 为什么示例数量受上下文限制

上下文总长度满足：

\[
\sum_{i=1}^{K}
\left(|x_i|+|y_i|+|\text{format}_i|\right)
+|x_*|
+|y_*|
\le 2048.
\]

示例越长，可放的 \(K\) 越小；若给太多示例，最早内容会被截断或留给答案的空间不足。

## 6. 上下文学习的暂时性

设两个 prompt 分别定义任务 A 与 B：

\[
p_\theta(y\mid c_A,x)
\ne
p_\theta(y\mid c_B,x).
\]

区别由上下文造成，\(\theta\) 相同。任务切换几乎没有训练成本，但模型不会把新规则写入长期参数。

## 7. “学习”一词的三个层次

| 层次 | 变化对象 | 时间尺度 |
|---|---|---|
| 预训练 | 参数 \(\theta\) | 数十亿至数千亿 token |
| 上下文适配 | activations / KV states | 一个 prompt 内 |
| 自回归生成 | 已生成 token 条件 | 每个生成步骤 |

区分这三层可以避免把 in-context learning 误写成小样本微调。
