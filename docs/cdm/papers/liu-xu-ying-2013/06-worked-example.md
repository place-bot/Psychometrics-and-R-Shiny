# 三题两属性完整手算

## Q 矩阵

原文用“加法”和“乘法”两个属性：

\[
Q=
\begin{array}{c|cc}
&\text{加法}&\text{乘法}\\\hline
2+3&1&0\\
5\times2&0&1\\
(2+3)\times2&1&1
\end{array}.
\tag{2.8}
\]

记三道题为 \(I_1,I_2,I_3\)，非零属性模式列按

\[
10,\ 01,\ 11
\]

排列。

## 三个单题行

第 1 题只要求加法：

\[
B_Q(I_1)=(1,0,1).
\]

第 2 题只要求乘法：

\[
B_Q(I_2)=(0,1,1).
\]

第 3 题同时要求二者：

\[
B_Q(I_3)=(0,0,1).
\]

所以只使用单题时

\[
T(Q)=
\begin{pmatrix}
1&0&1\\
0&1&1\\
0&0&1
\end{pmatrix}.
\tag{2.11}
\]

## 属性比例

样本属性比例可排列为

\[
\widehat{\boldsymbol p}
=
\begin{pmatrix}
\widehat p_{10}\\
\widehat p_{01}\\
\widehat p_{11}
\end{pmatrix}.
\]

全零模式比例为

\[
\widehat p_{00}
=1-\widehat p_{10}-\widehat p_{01}-\widehat p_{11}.
\]

观测矩向量为

\[
\boldsymbol\alpha
=
\begin{pmatrix}
N_{I_1}/N\\
N_{I_2}/N\\
N_{I_3}/N
\end{pmatrix}.
\]

矩方程展开后是

\[
\begin{aligned}
\widehat p_{10}+\widehat p_{11}
&=\frac{N_{I_1}}N,\\
\widehat p_{01}+\widehat p_{11}
&=\frac{N_{I_2}}N,\\
\widehat p_{11}
&=\frac{N_{I_3}}N.
\end{aligned}
\tag{2.9}
\]

## 解出属性比例

由第三式：

\[
\widehat p_{11}
=
\frac{N_{I_3}}N.
\]

再代回前两式：

\[
\widehat p_{10}
=
\frac{N_{I_1}-N_{I_3}}N,
\qquad
\widehat p_{01}
=
\frac{N_{I_2}-N_{I_3}}N.
\]

矩阵 \(T(Q)\) 为上三角且对角线全为 1，因此满秩，解唯一。

## 加入题对

能够完成第 1、2 题的属性模式只有 \(11\)，所以

\[
B_Q(I_1\wedge I_2)
=(0,0,1).
\]

扩展矩阵变为

\[
T(Q)=
\begin{pmatrix}
1&0&1\\
0&1&1\\
0&0&1\\
0&0&1
\end{pmatrix},
\qquad
\boldsymbol\alpha=
\begin{pmatrix}
N_{I_1}/N\\
N_{I_2}/N\\
N_{I_3}/N\\
N_{I_1\wedge I_2}/N
\end{pmatrix}.
\tag{2.12}
\]

于是无噪声模型还要求

\[
\frac{N_{I_3}}N
=
\frac{N_{I_1\wedge I_2}}N
=
\widehat p_{11}.
\]

## 一个数值样本

假设

\[
\widehat p_{00}=0.10,\quad
\widehat p_{10}=0.25,\quad
\widehat p_{01}=0.35,\quad
\widehat p_{11}=0.30.
\]

则

\[
T(Q)\widehat{\boldsymbol p}
=
\begin{pmatrix}
0.55\\
0.65\\
0.30\\
0.30
\end{pmatrix}.
\]

这表示：

- 第 1 题正确率为 \(0.25+0.30=0.55\)；
- 第 2 题正确率为 \(0.35+0.30=0.65\)；
- 第 3 题正确率为 \(0.30\)；
- 第 1、2 题同时答对率也为 \(0.30\)。

## 噪声会怎样改变等式

加入失误与猜测后，实际完成第 3 题和同时答对第 1、2 题是两个随机事件，其概率一般不同。第 3 节的 \(T_{c,g}(Q)\) 会把每个 B-vector 从 0/1 能力指示改成具体答对概率，使矩匹配继续成立。

[下一页：列置换等价、完整性与饱和性](07-equivalence-completeness-saturation.md)
