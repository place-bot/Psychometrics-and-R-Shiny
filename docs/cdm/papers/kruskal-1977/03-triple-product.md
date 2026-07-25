# 三重积与固有歧义

## 三个因子矩阵

把 \(R\) 个向量分别排成列：

\[
A=
\begin{bmatrix}
\boldsymbol a_1&\cdots&\boldsymbol a_R
\end{bmatrix}
\in\mathbb F^{I\times R},
\]

\[
B=
\begin{bmatrix}
\boldsymbol b_1&\cdots&\boldsymbol b_R
\end{bmatrix}
\in\mathbb F^{J\times R},
\qquad
C=
\begin{bmatrix}
\boldsymbol c_1&\cdots&\boldsymbol c_R
\end{bmatrix}
\in\mathbb F^{K\times R}.
\]

Kruskal 定义三重积

\[
[A,B,C]
=
\sum_{r=1}^{R}
\boldsymbol a_r\otimes
\boldsymbol b_r\otimes
\boldsymbol c_r.
\]

逐元素写成

\[
[A,B,C]_{ijk}
=
\sum_{r=1}^{R}
a_{ir}b_{jr}c_{kr}.
\tag{2}
\]

现代文献把它称为 CP 或 CANDECOMP/PARAFAC 分解。

## 三重积中的“逐列配对”

第 \(r\) 项固定使用

\[
\boldsymbol a_r,\quad
\boldsymbol b_r,\quad
\boldsymbol c_r.
\]

所以三重积对列顺序有一条特殊规则：

- 三个矩阵同时交换第 \(r\) 与第 \(s\) 列，数组不变；
- 只交换其中一个矩阵的两列，通常会改变数组。

这就是“共同置换”出现的原因。

## 置换歧义

设 \(P\) 是 \(R\times R\) 置换矩阵。则

\[
[AP,BP,CP]=[A,B,C].
\]

它只改变求和项的排列顺序。

在潜在类模型里，列 \(r\) 对应第 \(r\) 个潜在类，因此 \(P\) 对应类别标签交换。

## 缩放歧义

设

\[
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_R),
\]

\[
M=\operatorname{diag}(\mu_1,\ldots,\mu_R),
\qquad
N=\operatorname{diag}(\nu_1,\ldots,\nu_R),
\]

且

\[
\lambda_r\mu_r\nu_r=1
\quad
\text{对所有 }r.
\tag{3}
\]

那么

\[
[A\Lambda,BM,CN]=[A,B,C],
\]

因为第 \(r\) 个 triad 被乘以

\[
\lambda_r\mu_r\nu_r=1.
\]

把共同置换也加入后，可写成

\[
\bar A=AP\Lambda,\qquad
\bar B=BPM,\qquad
\bar C=CPN,
\tag{4}
\]

并对置换后的对应分量要求三个缩放乘积为 1。也有文献写成 \(A\Lambda P\)；两种记号只差对角元素的重新排列。

## 本质唯一

若

\[
[A,B,C]=[\bar A,\bar B,\bar C]
\]

必然推出式 (4)，该分解称为 **essentially unique**，即本质唯一。

“本质”保留了模型结构本身无法排除的对称性。要求三个因子矩阵逐元素完全相同会把等价分解错误地判为不同。

## 展开形式

令 \(\odot\) 表示 Khatri--Rao 积，即两个矩阵按对应列做 Kronecker 积。三种展开可写为

\[
X_{(1)}=A(C\odot B)^\mathsf T,
\]

\[
X_{(2)}=B(C\odot A)^\mathsf T,
\]

\[
X_{(3)}=C(B\odot A)^\mathsf T.
\]

这些公式把三路分解连接到矩阵代数，但单独看任意一个展开仍存在一般可逆变换歧义。Kruskal 条件联合利用三个方向，才能把歧义压缩到置换和缩放。

## 概率模型怎样消除缩放

若 \(A,B,C\) 的每一列都是条件概率向量，则

\[
\boldsymbol 1^\mathsf T\boldsymbol a_r
=
\boldsymbol 1^\mathsf T\boldsymbol b_r
=
\boldsymbol 1^\mathsf T\boldsymbol c_r
=1.
\]

任意非 1 缩放都会破坏归一化。因此，从等价分解中把列重新归一化以后，缩放被固定；共同置换仍然存在。

这正是张量“置换与缩放唯一性”转化为潜在类模型“标签置换唯一性”的桥梁。
