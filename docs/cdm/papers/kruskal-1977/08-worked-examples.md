# 完整手算例子

## 一个满足条件的 \(R=3\) 分解

取

\[
A=
\begin{bmatrix}
1&0&1\\
0&1&1\\
1&1&0
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
1&1&0\\
1&0&1\\
0&1&1
\end{bmatrix},
\]

\[
C=
\begin{bmatrix}
1&2&1\\
0&1&1\\
1&0&1
\end{bmatrix}.
\]

三个矩阵都是 \(3\times3\)，并且行列式均非零：

\[
\det(A)=-2,\qquad
\det(B)=-2,\qquad
\det(C)=2.
\]

因此它们都满列秩：

\[
k_A=k_B=k_C=3.
\]

Kruskal 条件为

\[
k_A+k_B+k_C
=9
\ge
8
=2R+2.
\]

所以

\[
\mathcal X=[A,B,C]
\]

的张量秩为 3，并且这个三项分解本质唯一。

## 算一个张量元素

位置 \((1,1,1)\) 的值为

\[
x_{111}
=
\sum_{r=1}^{3}
a_{1r}b_{1r}c_{1r}.
\]

代入三行：

\[
x_{111}
=
(1)(1)(1)
+
(0)(1)(2)
+
(1)(0)(1)
=1.
\]

整张 \(3\times3\times3\) 数组都由同样的逐成分乘积得到。

## 构造一个等价分解

把三个成分循环置换，并取

\[
\Lambda
=\operatorname{diag}\left(2,\frac12,1\right),
\]

\[
M
=\operatorname{diag}\left(3,1,\frac13\right),
\qquad
N
=\operatorname{diag}\left(\frac16,2,3\right).
\]

逐成分检查：

\[
2\cdot3\cdot\frac16=1,
\]

\[
\frac12\cdot1\cdot2=1,
\qquad
1\cdot\frac13\cdot3=1.
\]

令 \(P\) 表示同一个循环置换，并定义

\[
\bar A=AP\Lambda,\qquad
\bar B=BPM,\qquad
\bar C=CPN.
\]

每个新 triad 都来自一个旧 triad，三个方向上的缩放乘积为 1，所以

\[
[\bar A,\bar B,\bar C]=[A,B,C].
\]

这两组矩阵数值不同，却属于同一个本质分解。

## 一个条件失败且确实多解的构造

取 \(R=2\)：

\[
A=B=I_2,
\qquad
C=
\begin{bmatrix}
1&1
\end{bmatrix}.
\]

第三个因子的两列相同，

\[
k_C=1,
\]

而

\[
k_A=k_B=2.
\]

所以

\[
k_A+k_B+k_C=5<6=2R+2.
\]

此时三路数组只有一个第三方向切片：

\[
\mathcal X(:,:,1)
=
\boldsymbol e_1\boldsymbol e_1^\mathsf T
+
\boldsymbol e_2\boldsymbol e_2^\mathsf T
=I_2.
\]

问题已经退化成矩阵 \(I_2\) 的秩一分解。

取任意可逆矩阵

\[
Q=
\begin{bmatrix}
1&1\\
0&1
\end{bmatrix}.
\]

令

\[
\bar A=Q,
\qquad
\bar B=Q^{-\mathsf T}
=
\begin{bmatrix}
1&0\\
-1&1
\end{bmatrix},
\qquad
\bar C=C.
\]

那么

\[
\bar A\bar B^\mathsf T
=QQ^{-1}
=I_2,
\]

从而

\[
[\bar A,\bar B,\bar C]=[A,B,C].
\]

这个 \(Q\) 不是置换与对角缩放的乘积，故两组分解不属于 Kruskal 允许的固有歧义。改变 \(Q\) 还能得到无穷多组分解。

## 两个例子共同说明什么

| 情形 | \(k\)-rank 总和 | 结论 |
| --- | ---: | --- |
| 三个 \(3\times3\) 因子满列秩 | \(9\ge8\) | 定理认证本质唯一 |
| 第三个因子两列相同 | \(5<6\) | 定理失效，且该构造确实多解 |

第二行展示了一个真实反例，但不能把它推广成“所有不满足条件的分解都多解”。充分条件失败后的结论仍需逐个模型分析。
