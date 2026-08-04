# 完整手算：一个头怎样更新三个 token

## 1. 输入投影

设三个 token 的二维 Q/K/V 为

\[
\mathbf Q=
\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix},
\quad
\mathbf K=
\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix},
\quad
\mathbf V=
\begin{bmatrix}1&2\\3&0\\2&1\end{bmatrix}.
\]

\(d_k=2\)，缩放因子为 \(\sqrt2\)。

## 2. 分数矩阵

\[
\mathbf Q\mathbf K^\top
=
\begin{bmatrix}
1&0&1\\
0&1&1\\
1&1&2
\end{bmatrix}.
\]

第一行缩放后为

\[
(0.7071,\;0,\;0.7071).
\]

## 3. 第一位置的 softmax

\[
\exp(0.7071)\approx2.028,\qquad
\exp(0)=1.
\]

\[
\mathbf a_1
\approx
(0.401,\;0.198,\;0.401).
\]

输出为

\[
\begin{aligned}
\mathbf o_1
&=
0.401(1,2)+0.198(3,0)+0.401(2,1)\\
&\approx(1.797,\;1.203).
\end{aligned}
\]

位置 1 的新表示由三个位置共同决定。

## 4. 加 causal mask

若这是 decoder self-attention 的第一位置，未来位置 2、3 不可见：

\[
\widetilde{\mathbf s}_1
=(0.7071,-\infty,-\infty).
\]

于是

\[
\mathbf a_1=(1,0,0),
\qquad
\mathbf o_1=(1,2).
\]

第二位置可见位置 1、2：

\[
\widetilde{\mathbf s}_2=(0,0.7071,-\infty),
\]

\[
\mathbf a_2\approx(0.330,\;0.670,\;0),
\]

\[
\mathbf o_2\approx0.330(1,2)+0.670(3,0)
=(2.340,\;0.660).
\]

## 5. 两个头

若另一个头使用不同投影，可能产生输出 \(\mathbf O^{(2)}\)。多头输出先拼接：

\[
\mathbf H
=
[\mathbf O^{(1)};\mathbf O^{(2)}],
\]

再乘 \(\mathbf W^O\) 混合。每个头拥有独立 attention 分布。

## 6. 残差与 LayerNorm

设 attention 投影结果为 \(\mathbf m_i\)，原输入为 \(\mathbf x_i\)：

\[
\mathbf r_i=\mathbf x_i+\mathbf m_i,
\qquad
\mathbf z_i=\operatorname{LN}(\mathbf r_i).
\]

随后 FFN 对每个 \(\mathbf z_i\) 独立变换，再做第二次 Add & Norm。至此完成一个 encoder layer。

## 7. 训练时的并行性

虽然手算逐行展示，实际一次计算完整

\[
\mathbf S\in\mathbb R^{3\times3},
\quad
\mathbf A\in\mathbb R^{3\times3},
\quad
\mathbf O\in\mathbb R^{3\times2}.
\]

causal mask 也是一次加到整个矩阵上。
