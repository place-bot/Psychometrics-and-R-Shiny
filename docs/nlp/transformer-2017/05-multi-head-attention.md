# Multi-Head Attention

## 1. 完整公式

\[
\operatorname{head}_i
=
\operatorname{Attention}(
\mathbf Q\mathbf W_i^Q,
\mathbf K\mathbf W_i^K,
\mathbf V\mathbf W_i^V),
\]

\[
\operatorname{MultiHead}(\mathbf Q,\mathbf K,\mathbf V)
=
\operatorname{Concat}(
\operatorname{head}_1,\ldots,\operatorname{head}_h)
\mathbf W^O.
\]

## 2. 原论文 base 的维度

\[
d_{\text{model}}=512,\qquad
h=8,\qquad
d_k=d_v=64.
\]

每个头输出 64 维，拼接后

\[
8\times64=512.
\]

\(\mathbf W^O\in\mathbb R^{512\times512}\) 再混合各头信息。

## 3. 参数形状

\[
\mathbf W_i^Q,\mathbf W_i^K,\mathbf W_i^V
\in\mathbb R^{512\times64},
\qquad
\mathbf W^O\in\mathbb R^{512\times512}.
\]

实际代码常用一块 \([512,3\times512]\) 权重同时产生 QKV，再 reshape 为 8 个头。

## 4. 多头的作用

单头输出会把多个位置压成一次加权平均。多个头使用不同投影，可以在不同子空间和位置模式中独立检索，例如局部搭配、长距离指代或句法关系。论文的 attention 可视化显示不同头形成不同结构，但不能保证每个头都有稳定的人类标签。

## 5. 计算量为何没有乘八倍

若单头使用完整 512 维，QK 点积规模约为 \(n^2\cdot512\)。八头各用 64 维，总计仍为

\[
8\cdot n^2\cdot64=n^2\cdot512.
\]

投影与输出矩阵会增加常数开销，主 attention 乘法量保持同阶。

## 6. 论文消融

在相近计算预算下，单头开发集 BLEU 为 24.9，base 八头为 25.8；16 头同为 25.8，32 头降到 25.4。头数过少限制子空间，头数过多会使每头维度过窄。

## 7. 与 LoRA 的接口

后续 LoRA 论文将 attention 的

\[
\mathbf W^Q,\mathbf W^K,\mathbf W^V,\mathbf W^O
\]

视为可适配权重。它冻结原矩阵，只学习低秩增量；原 LoRA 实验常优先适配 \(W_q\) 与 \(W_v\)。
