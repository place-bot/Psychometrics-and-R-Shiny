# 低秩更新的线性代数

## 1. 形状

\[
\mathbf W_0\in\mathbb R^{d_{\text{out}}\times d_{\text{in}}},
\quad
\mathbf A\in\mathbb R^{r\times d_{\text{in}}},
\quad
\mathbf B\in\mathbb R^{d_{\text{out}}\times r}.
\]

\[
\Delta\mathbf W=\mathbf B\mathbf A
\in\mathbb R^{d_{\text{out}}\times d_{\text{in}}}.
\]

由矩阵秩不等式：

\[
\operatorname{rank}(\mathbf B\mathbf A)
\le r.
\]

## 2. 前向路径

\[
\mathbf h
=
\mathbf W_0\mathbf x
+
s\mathbf B(\mathbf A\mathbf x),
\qquad
s=\alpha/r.
\]

先用 \(A\) 将输入压到 \(r\) 维，再用 \(B\) 映射回输出维度。

## 3. 参数量

全矩阵更新参数：

\[
d_{\text{out}}d_{\text{in}}.
\]

LoRA 参数：

\[
r(d_{\text{in}}+d_{\text{out}}).
\]

当方阵 \(d_{\text{in}}=d_{\text{out}}=d\)：

\[
\frac{\text{LoRA params}}{\text{full params}}
=
\frac{2dr}{d^2}
=
\frac{2r}{d}.
\]

例如 \(d=4096,r=8\)，比例为

\[
\frac{16}{4096}\approx0.3906\%.
\]

## 4. LoRA 约束的是更新

\[
\mathbf W_{\text{task}}
=
\mathbf W_0+\mathbf B\mathbf A.
\]

\(\mathbf W_0\) 可以保持满秩。最终矩阵也通常满秩；只有增量被约束在 rank 不超过 \(r\) 的集合中。

## 5. 表达能力

任意矩阵 \(\Delta W\) 的秩若为 \(r^\star\)，当 LoRA rank \(r\ge r^\star\) 时可精确表示该更新。rank 增大时可表示的更新集合扩大；参数效率与容量之间形成权衡。

## 6. 与 SVD 的关系

SVD 将已经给定的矩阵写成

\[
\Delta W=U\Sigma V^\top.
\]

LoRA 在训练开始时不知道理想 \(\Delta W\)，直接用梯度学习 \(A,B\)。它不要求每一步执行 SVD，也不保证 \(A,B\) 正交或等于奇异向量。

## 7. 因子不唯一

对任意可逆 \(\mathbf R\in\mathbb R^{r\times r}\)：

\[
\mathbf B\mathbf A
=
(\mathbf B\mathbf R)
(\mathbf R^{-1}\mathbf A).
\]

因此 \(A,B\) 本身没有唯一解释，分析时更应关注乘积 \(\Delta W\) 或其子空间。
