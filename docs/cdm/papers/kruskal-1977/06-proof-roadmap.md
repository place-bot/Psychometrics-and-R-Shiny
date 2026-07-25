# 证明思路

## 证明要排除什么

从

\[
[M_1,M_2,M_3]=[N_1,N_2,N_3]
\tag{7}
\]

出发，需要证明两组三个因子矩阵逐列对应，允许共同置换与缩放。

Kruskal 原文的主线依赖 **Permutation Lemma**：如果两个列集合在足够多的投影下保持同样的稀疏线性组合结构，它们必须逐列匹配。原始证明技术细节较长。

Rhodes (2010) 给出同一 Theorem 4a 的紧凑证明。本页用它展示代数机制，并把后续证明与 1977 原文区分开。

## 第一步：先处理两个因子满列秩

设

\[
M_1,M_2\in\mathbb F^{s\times R}
\]

都满列秩，\(M_3\) 没有零列。

取一个向量 \(\boldsymbol c\)，使

\[
\boldsymbol c^\mathsf T M_3
\]

的每个元素都非零。沿第三个方向收缩张量：

\[
A_{\boldsymbol c}
=
\boldsymbol c^\mathsf T*_{3}
[M_1,M_2,M_3].
\]

利用三重积，

\[
A_{\boldsymbol c}
=
M_1
\operatorname{diag}(\boldsymbol c^\mathsf T M_3)
M_2^\mathsf T.
\tag{8}
\]

中间对角矩阵可逆，所以

\[
\operatorname{rank}(A_{\boldsymbol c})=R.
\]

式 (7) 还给出

\[
A_{\boldsymbol c}
=
N_1
\operatorname{diag}(\boldsymbol c^\mathsf T N_3)
N_2^\mathsf T.
\]

因此 \(N_1,N_2\) 也必须有秩 \(R\)，并且与 \(M_1,M_2\) 分别张成相同的列空间。

## 第二步：换基后看张量切片

在共同列空间中换基，可把

\[
M_1=M_2=I_R
\]

作为规范化情形。

固定第三个坐标 \(i\)，得到矩阵切片

\[
S_i
=
\operatorname{diag}(\bar{\boldsymbol m}^{\,3}_i),
\]

其中 \(\bar{\boldsymbol m}^{\,3}_i\) 是 \(M_3\) 的第 \(i\) 行。

另一组分解给出

\[
S_i
=
N_1
\operatorname{diag}(\bar{\boldsymbol n}^{\,3}_i)
N_2^\mathsf T.
\]

再乘 \(A_{\boldsymbol c}^{-1}\)，得到一族可同时对角化的矩阵：

\[
S_iA_{\boldsymbol c}^{-1}.
\tag{9}
\]

## 第三步：共同特征子空间恢复列分组

在 \(M\) 表示下，式 (9) 的第 \(r\) 个特征值为

\[
\frac{m^3_{ir}}
{\boldsymbol c^\mathsf T\boldsymbol m^3_r}.
\]

两个编号 \(r,s\) 对所有 \(i\) 都产生同一组特征值，当且仅当

\[
\boldsymbol m^3_r
\quad\text{与}\quad
\boldsymbol m^3_s
\]

成比例。

所以共同特征子空间把 \(M_3\) 的列按“互相成比例”分组。由于同一族矩阵也来自 \(N\) 表示，两组分解必须给出相同的特征子空间分组，从而得到一个共同置换。

## 第四步：\(k_{M_3}\ge2\) 把分组缩成单列

若

\[
k_{M_3}\ge2,
\]

任意两列都独立，不可能成比例。每个共同特征子空间只对应一个列编号。

于是：

- \(M_1\) 与 \(N_1\) 的列逐个对应；
- \(M_2\) 与 \(N_2\) 使用同一个对应关系；
- 比较特征值后，\(M_3\) 与 \(N_3\) 也使用同一置换；
- 三个方向只剩逐列缩放。

这证明了“两因子满列秩，第三因子 \(k\)-rank 至少为 2”的特殊情形。

## 第五步：一般情形改写成缺陷量

令

\[
a_i=R-k_{M_i},
\qquad i=1,2,3.
\]

Kruskal 条件成为

\[
a_1+a_2+a_3\le R-2.
\]

Rhodes 把三元组称为 type

\[
(R;a_1,a_2,a_3).
\]

缺陷量越小，因子越接近满列秩。

## 第六步：投影、删列与归纳

一般证明的核心操作如下：

1. 选择一个列子集；
2. 构造投影 \(\Pi_i\)，让它的零空间恰好包含这些列张成的空间；
3. 对张量第 \(i\) 个方向作用 \(\Pi_i\)；
4. 被消掉的列对应零 triad，可以从三重积中删除；
5. 在剩余的较少列上使用特殊情形或归纳假设；
6. 恢复某个子集在 \(M_i\) 与 \(N_i\) 中张成的同一空间；
7. 改变被投影的子集，逐步把“子空间匹配”细化成“单列匹配”。

Kruskal rank 在这里发挥作用：无论删掉或保留的是哪一组列，只要数量没有超过阈值，剩余列的独立性就有保证。

## 第七步：为什么三个缩放必须相消

最终得到

\[
\boldsymbol n^1_r
=\lambda_r\boldsymbol m^1_{\sigma(r)},
\]

\[
\boldsymbol n^2_r
=\mu_r\boldsymbol m^2_{\sigma(r)},
\qquad
\boldsymbol n^3_r
=\nu_r\boldsymbol m^3_{\sigma(r)}.
\]

第 \(r\) 个 triad 变为

\[
\lambda_r\mu_r\nu_r
\left(
\boldsymbol m^1_{\sigma(r)}
\otimes
\boldsymbol m^2_{\sigma(r)}
\otimes
\boldsymbol m^3_{\sigma(r)}
\right).
\]

两边张量相同且列已经逐项对齐，故

\[
\lambda_r\mu_r\nu_r=1.
\]

这就得到共同置换与相互抵消的缩放。

## 证明主线的最短记忆版

\[
\text{张量相等}
\rightarrow
\text{收缩成矩阵}
\rightarrow
\text{共同对角化}
\rightarrow
\text{恢复成比例列的分组}
\]

\[
\rightarrow
\text{\(k\)-rank 排除组内混淆}
\rightarrow
\text{投影与归纳处理非满秩情形}
\rightarrow
\text{共同置换和缩放}.
\]
