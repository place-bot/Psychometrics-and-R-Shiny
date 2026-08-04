# 逐步手算：从注意力到梯度

## 1. 三个源注释

\[
\mathbf h_1=\begin{bmatrix}1\\0\end{bmatrix},
\quad
\mathbf h_2=\begin{bmatrix}0\\1\end{bmatrix},
\quad
\mathbf h_3=\begin{bmatrix}1\\1\end{bmatrix}.
\]

当前目标步的分数为

\[
e_{i1}=1,\qquad e_{i2}=0,\qquad e_{i3}=2.
\]

## 2. Softmax

\[
\exp(1)\approx2.7183,\quad
\exp(0)=1,\quad
\exp(2)\approx7.3891,
\]

\[
\boldsymbol\alpha_i
\approx
(0.2447,\;0.0900,\;0.6652).
\]

三项之和约为 1。

## 3. 上下文

\[
\begin{aligned}
\mathbf c_i
&=\sum_j\alpha_{ij}\mathbf h_j\\
&\approx
0.2447\begin{bmatrix}1\\0\end{bmatrix}
+0.0900\begin{bmatrix}0\\1\end{bmatrix}
+0.6652\begin{bmatrix}1\\1\end{bmatrix}\\
&\approx
\begin{bmatrix}0.9099\\0.7552\end{bmatrix}.
\end{aligned}
\]

## 4. 词表输出

假设 \(A,B,C\) 的 logits 是

\[
\mathbf o_i=(0.2,\;1.0,\;-0.5)^\top,
\]

则

\[
\mathbf p_i\approx(0.2687,\;0.5979,\;0.1334)^\top.
\]

正确词为 \(B\) 时

\[
\mathcal L_i=-\log(0.5979)\approx0.514,
\]

\[
\frac{\partial\mathcal L_i}{\partial\mathbf o_i}
\approx
(0.2687,\;-0.4021,\;0.1334)^\top.
\]

## 5. Attention score 梯度

假设下游传到上下文的梯度为

\[
\mathbf g_i
=
\frac{\partial\mathcal L}{\partial\mathbf c_i}
=
(0.4,\;-0.2)^\top.
\]

\[
\mathbf g_i^\top\mathbf c_i\approx0.2129.
\]

利用

\[
\frac{\partial\mathcal L}{\partial e_{ik}}
=
\alpha_{ik}
\left(
\mathbf g_i^\top\mathbf h_k
-
\mathbf g_i^\top\mathbf c_i
\right)
\]

可得

\[
\begin{aligned}
\frac{\partial\mathcal L}{\partial e_{i1}}&\approx0.0458,\\
\frac{\partial\mathcal L}{\partial e_{i2}}&\approx-0.0372,\\
\frac{\partial\mathcal L}{\partial e_{i3}}&\approx-0.0086.
\end{aligned}
\]

三项和约为 0，反映 softmax 对全部 logits 同时平移不敏感。

## 6. 梯度下降后的方向

\[
e_{ik}^{\text{new}}
=
e_{ik}
-
\eta
\frac{\partial\mathcal L}{\partial e_{ik}}.
\]

因此位置 1 分数下降，位置 2 上升，位置 3 略微上升。在这个假设梯度下，模型希望上下文第二维增加、第一维减少。

## 7. 继续传入对齐网络

\[
e_{ij}
=
\mathbf v_a^\top\tanh(\mathbf q_{ij}),
\qquad
\mathbf q_{ij}
=
\mathbf W_a\mathbf s_{i-1}
+\mathbf U_a\mathbf h_j.
\]

记 \(\delta_{ij}=\partial\mathcal L/\partial e_{ij}\)，则

\[
\frac{\partial\mathcal L}{\partial\mathbf q_{ij}}
=
\delta_{ij}
\left[
\mathbf v_a\odot
(1-\tanh^2(\mathbf q_{ij}))
\right].
\]

再与 \(\mathbf s_{i-1}\) 和 \(\mathbf h_j\) 做外积，就得到 \(\mathbf W_a,\mathbf U_a\) 的梯度。单句误差由此转化为可跨样本复用的对齐规则。

## 8. Padding 例子

若位置 3 是 padding，应在 softmax 前令 \(e_{i3}=-\infty\)。有效权重变为

\[
\alpha_{i1}\approx0.7311,\qquad
\alpha_{i2}\approx0.2689,\qquad
\alpha_{i3}=0.
\]

直接在 softmax 后把第三项乘 0 会破坏归一化，除非再次归一化。

## 本页小结

\[
\text{对齐分数}
\rightarrow
\text{softmax}
\rightarrow
\text{上下文}
\rightarrow
\text{目标词损失}
\rightarrow
\text{attention 梯度}.
\]

从 \(e_{ij}\) 到翻译损失的操作连续可微，因此软对齐可以和翻译联合学习。
