# 三题两属性完整手算

## 属性模式顺序

论文按

\[
(0,0),(1,0),(0,1),(1,1)
\]

排列 \(\boldsymbol p=(p_{00},p_{10},p_{01},p_{11})^\top\)。

## 真 Q

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&1
\end{pmatrix}.
\tag{8}
\]

题 1 只需属性 1，题 2 只需属性 2，题 3 同时需要两项。先令 \(c_j=1,g_j=0\)，反应没有噪声。

## 三个单题 B-vector

\[
B(1)=(0,1,0,1),
\]

\[
B(2)=(0,0,1,1),
\]

\[
B(3)=(0,0,0,1).
\]

于是

\[
T(Q)=
\begin{pmatrix}
0&1&0&1\\
0&0&1&1\\
0&0&0&1
\end{pmatrix}.
\tag{9}
\]

乘以 \(\boldsymbol p\)：

\[
T(Q)\boldsymbol p
=
\begin{pmatrix}
p_{10}+p_{11}\\
p_{01}+p_{11}\\
p_{11}
\end{pmatrix}
=
\begin{pmatrix}
N_1/N\\
N_2/N\\
N_3/N
\end{pmatrix}
=
\boldsymbol\beta.
\]

\(N_j\) 是题 \(j\) 的答对人数。

## 一个错误候选

\[
Q'=
\begin{pmatrix}
1&0\\
0&1\\
1&0
\end{pmatrix}
\]

把题 3 改成只需属性 1。对应

\[
T(Q')=
\begin{pmatrix}
0&1&0&1\\
0&0&1&1\\
0&1&0&1
\end{pmatrix}.
\tag{10}
\]

第一行与第三行相同，候选模型强迫题 1 和题 3 的总体答对率相同。若数据中的 \(N_1/N\) 与 \(N_3/N\) 相差明显，这个候选无法很好匹配 \(\boldsymbol\beta\)。

## 加入题对约束

令

\[
N_{1\wedge2}
=
\sum_{i=1}^N
\mathbf 1(R_i^1=1,R_i^2=1).
\tag{12}
\]

真 Q 且无噪声时，同时答对题 1、2 等价于掌握两项属性，因此

\[
B(1,2)=B(1)\odot B(2)=(0,0,0,1)=B(3).
\]

扩充后的矩阵为

\[
T(Q)=
\begin{pmatrix}
0&1&0&1\\
0&0&1&1\\
0&0&0&1\\
0&0&0&1
\end{pmatrix},
\qquad
\boldsymbol\beta=
\begin{pmatrix}
N_1/N\\
N_2/N\\
N_3/N\\
N_{1\wedge2}/N
\end{pmatrix}.
\tag{13}
\]

无噪声逻辑要求 \(N_3=N_{1\wedge2}\)。实际数据一般存在偏离，\(s_j,g_j\) 用来吸收作答噪声。

## 这个例子真正说明的事

Q 通过一组跨题联合约束进入可观测分布。加入更多题组行，相当于从数据中提出更多必须同时满足的矩条件；错误 Q 更难借助 \(\boldsymbol p,\boldsymbol c,\boldsymbol g\) 完全补偿。
