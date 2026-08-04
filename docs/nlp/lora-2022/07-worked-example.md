# 完整手算：一个 \(3\times4\) 线性层

## 1. 冻结权重与 rank 1 分支

\[
W_0=
\begin{bmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&1&0
\end{bmatrix},
\quad
A=\begin{bmatrix}1&-1&0&2\end{bmatrix},
\quad
B=\begin{bmatrix}0.5\\-1\\0.25\end{bmatrix}.
\]

\(A\in\mathbb R^{1\times4}\)，\(B\in\mathbb R^{3\times1}\)，所以 \(\operatorname{rank}(BA)\le1\)。

## 2. 计算增量

\[
BA=
\begin{bmatrix}
0.5&-0.5&0&1\\
-1&1&0&-2\\
0.25&-0.25&0&0.5
\end{bmatrix}.
\]

设 \(\alpha=r=1\)，缩放 \(s=1\)。

## 3. 一个输入

\[
x=(2,1,-1,0)^\top.
\]

基座输出：

\[
W_0x=(2,1,-1)^\top.
\]

低秩路径先降维：

\[
Ax=2-1+0+0=1.
\]

再升维：

\[
B(Ax)=(0.5,-1,0.25)^\top.
\]

最终：

\[
h=(2.5,0,-0.75)^\top.
\]

## 4. 参数节省

全矩阵更新有 \(3\times4=12\) 个参数。rank 1 LoRA 有 \(4+3=7\) 个参数。这个小例子节省有限；当 \(d\) 为数千且 \(r\) 为个位数时比例迅速下降。

## 5. 一个梯度

若损失对输出的梯度

\[
g_h=(1,-2,0.5)^\top,
\]

令 \(u=Ax=1\)，则

\[
\frac{\partial L}{\partial B}
=
g_hu^\top
=
\begin{bmatrix}1\\-2\\0.5\end{bmatrix}.
\]

\[
\frac{\partial L}{\partial A}
=
B^\top g_h\,x^\top.
\]

\[
B^\top g_h
=
0.5(1)+(-1)(-2)+0.25(0.5)
=
2.625.
\]

\[
\frac{\partial L}{\partial A}
=
2.625(2,1,-1,0)
=(5.25,2.625,-2.625,0).
\]

\(W_0\) 的梯度不存储，但输入梯度仍通过基座与 LoRA 两条路径传播。

## 6. 合并验证

\[
W_{\text{merged}}=W_0+BA.
\]

直接计算 \(W_{\text{merged}}x\) 必须得到同样的 \((2.5,0,-0.75)^\top\)。这就是“合并后无额外推理层”的代数依据。
