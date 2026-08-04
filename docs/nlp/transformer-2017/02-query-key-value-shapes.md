# Query、Key、Value：含义与形状

## 1. 检索类比

attention 将一个 query 与多组 key–value 匹配：

- query：当前位置想寻找什么；
- key：每个候选位置用什么特征接受匹配；
- value：匹配后真正取回的内容。

key 决定权重，value 决定加权结果。两者可以来自同一输入，却通过不同参数投影。

## 2. 单头矩阵

设 batch 省略，输入

\[
\mathbf X\in\mathbb R^{n\times d_{\text{model}}}.
\]

\[
\begin{aligned}
\mathbf Q&=\mathbf X\mathbf W^Q
\in\mathbb R^{n_q\times d_k},\\
\mathbf K&=\mathbf M\mathbf W^K
\in\mathbb R^{n_k\times d_k},\\
\mathbf V&=\mathbf M\mathbf W^V
\in\mathbb R^{n_k\times d_v}.
\end{aligned}
\]

self-attention 中 \(\mathbf M=\mathbf X\)，且 \(n_q=n_k=n\)。cross-attention 中 \(\mathbf X\) 来自 decoder，\(\mathbf M\) 来自 encoder。

## 3. 分数与输出形状

\[
\mathbf S
=
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_k}}
\in\mathbb R^{n_q\times n_k}.
\]

第 \(i\) 行包含 query \(i\) 对全部 key 的分数。行 softmax 后

\[
\mathbf A=\operatorname{softmax}_{\text{key}}(\mathbf S)
\in\mathbb R^{n_q\times n_k},
\qquad
\sum_j A_{ij}=1.
\]

\[
\mathbf O=\mathbf A\mathbf V
\in\mathbb R^{n_q\times d_v}.
\]

## 4. Batch 与多头形状

常见实现使用

\[
[B,h,n,d_h].
\]

分数矩阵：

\[
[B,h,n_q,d_k]
\times
[B,h,d_k,n_k]
\rightarrow
[B,h,n_q,n_k].
\]

随后与 \(\mathbf V\) 相乘得到 \([B,h,n_q,d_v]\)，转置并拼回 \([B,n_q,hd_v]\)。

## 5. 为什么每层重新投影

输入表示同时携带多种特征。不同 \(\mathbf W^Q,\mathbf W^K,\mathbf W^V\) 允许模型学习：

- 用一组特征判断相关性；
- 用另一组特征作为被传递内容；
- 每层与每个头采用不同关系空间。

## 6. Self-attention 仍然是上下文化表示

同一 token 的 embedding 初始固定，但它的输出

\[
\mathbf o_i=\sum_j A_{ij}\mathbf v_j
\]

随整句 token、位置和层数变化。因此 Transformer 产生上下文化 token 表示。
