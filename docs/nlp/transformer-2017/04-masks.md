# Padding Mask 与 Causal Mask

mask 决定一个 query 可以读取哪些 key。它在 softmax 前作用于分数矩阵。

## 1. Padding mask

不同长度句子补齐后，padding key 不应被读取。设有效 key 为 1：

\[
M_{ij}^{\text{pad}}
=
\begin{cases}
0,&\text{key }j\text{ 有效},\\
-\infty,&\text{key }j\text{ 是 padding}.
\end{cases}
\]

## 2. Causal mask

decoder 的位置 \(i\) 只能读到位置 \(j\le i\)：

\[
M_{ij}^{\text{causal}}
=
\begin{cases}
0,&j\le i,\\
-\infty,&j>i.
\end{cases}
\]

总分数为

\[
\widetilde{\mathbf S}
=
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_k}}
+\mathbf M.
\]

非法位置经过 softmax 后权重为 0。

## 3. 目标右移

训练目标为

\[
[y_1,y_2,\ldots,y_T].
\]

decoder 输入为

\[
[\langle BOS\rangle,y_1,\ldots,y_{T-1}].
\]

位置 \(i\) 的输出预测 \(y_i\)。右移提供真实前缀，causal mask 阻止网络通过 self-attention 偷看未来标签。

## 4. 为什么 mask 不妨碍训练并行

causal mask 改变可见连接，没有建立递归变量：

\[
\mathbf O
=
\operatorname{softmax}(
\mathbf Q\mathbf K^\top/\sqrt{d_k}+\mathbf M)\mathbf V.
\]

全部行可以一次矩阵计算。位置 \(i\) 的结果数学上只依赖前缀，但计算调度无需等待位置 \(i-1\) 的隐藏状态。

## 5. 三种 attention 的 mask

| 子层 | query | key/value | mask |
|---|---|---|---|
| Encoder self-attention | 源位置 | 源位置 | source padding |
| Decoder self-attention | 目标位置 | 目标位置 | causal + target padding |
| Cross-attention | 目标位置 | encoder 输出 | source padding |

cross-attention 不使用 causal source mask；每个目标位置都可读取完整源句。

## 6. 常见实现错误

- mask 方向颠倒；
- 在 softmax 后才置零却未重新归一化；
- query padding 与 key padding 混淆；
- 使用有限负数时在低精度下不够小；
- 一整行全部 mask，导致 `NaN`；
- 推理 cache 的位置偏移与 causal mask 不一致。
