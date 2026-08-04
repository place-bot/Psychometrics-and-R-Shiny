# Scaled Dot-Product Attention

## 1. 公式

\[
\boxed{
\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)
=
\operatorname{softmax}\!\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_k}}
\right)\mathbf V
}
\]

计算顺序是矩阵乘法、缩放、mask、行 softmax、value 加权和。

## 2. 点积表示什么

单个分数

\[
s_{ij}=\mathbf q_i^\top\mathbf k_j
\]

衡量 query 与 key 在学习到的投影空间中的兼容程度。它不是预先规定的语义相似度；投影参数由任务损失训练。

## 3. 为什么除以 \(\sqrt{d_k}\)

假设 \(q_\ell,k_\ell\) 独立、均值 0、方差 1：

\[
\mathbf q^\top\mathbf k
=
\sum_{\ell=1}^{d_k}q_\ell k_\ell.
\]

其方差约为

\[
\operatorname{Var}(\mathbf q^\top\mathbf k)=d_k.
\]

标准差随 \(\sqrt{d_k}\) 增长。缩放后

\[
\operatorname{Var}\!\left(
\frac{\mathbf q^\top\mathbf k}{\sqrt{d_k}}
\right)\approx1.
\]

没有缩放时，大幅度 logits 容易把 softmax 推入接近 one-hot 的饱和区，使多数位置梯度很小。

## 4. 稳定 softmax

\[
\operatorname{softmax}(s_j)
=
\frac{\exp(s_j-\max_k s_k)}
{\sum_\ell\exp(s_\ell-\max_k s_k)}.
\]

减去行最大值不改变概率，并防止指数溢出。现代框架的 softmax 通常已做稳定化。

## 5. 与 additive attention

Bahdanau：

\[
e_{ij}
=
\mathbf v^\top\tanh(
\mathbf W\mathbf q_i+\mathbf U\mathbf k_j).
\]

Transformer：

\[
e_{ij}
=
\mathbf q_i^\top\mathbf k_j/\sqrt{d_k}.
\]

两者理论复杂度相近；点积形式可以把所有位置对交给高度优化的矩阵乘法。

## 6. 梯度直觉

令 \(\mathbf o_i=\sum_j A_{ij}\mathbf v_j\)，下游梯度为 \(\mathbf g_i\)。对分数有

\[
\frac{\partial\mathcal L}{\partial s_{ik}}
=
A_{ik}\,
\mathbf g_i^\top(\mathbf v_k-\mathbf o_i).
\]

某个 value 相对当前平均输出更符合下降方向时，其分数会被提高。这与 Bahdanau soft attention 的梯度结构一致。
