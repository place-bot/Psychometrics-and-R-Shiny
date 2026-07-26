# 基础模型、样本与全部对象

## 三个维度

论文使用：

- \(N\)：学生人数；
- \(m\)：题目数；
- \(k\)：属性数。

作者假设 \(m\) 与 \(k\) 已知。Q 是

\[
Q=(Q_{ij})_{m\times k}\in\{0,1\}^{m\times k}.
\]

每一行描述一道题，每一列描述一个属性。

## 学生的潜在属性

对任意学生，

\[
\boldsymbol A=(A^1,\ldots,A^k)^\top
\in\{0,1\}^k.
\]

\(A^j=1\) 表示学生掌握属性 \(j\)，\(A^j=0\) 表示未掌握。

第 \(r\) 位学生的属性写作

\[
\boldsymbol A_r=(A_r^1,\ldots,A_r^k)^\top.
\]

属性不可直接观测。总体中某一模式 \(\boldsymbol A\) 的概率记为

\[
p_{\boldsymbol A}^*
=
\Pr(\boldsymbol A_r=\boldsymbol A).
\]

全部 \(2^k\) 个概率之和为 1。

## 学生的观测反应

对任意学生，

\[
\boldsymbol R=(R^1,\ldots,R^m)^\top
\in\{0,1\}^m,
\]

其中 \(R^i=1\) 表示第 \(i\) 题答对。

第 \(r\) 位学生的反应写作

\[
\boldsymbol R_r=(R_r^1,\ldots,R_r^m)^\top.
\]

数据集由

\[
\boldsymbol R_1,\ldots,\boldsymbol R_N
\]

组成。估计 Q 时看不到 \(\boldsymbol A_1,\ldots,\boldsymbol A_N\)。

## Q 的逐元素解释

\[
Q_{ij}=
\begin{cases}
1,&\text{题目 \(i\) 要求属性 \(j\)},\\
0,&\text{题目 \(i\) 不要求属性 \(j\)}.
\end{cases}
\]

论文假设真 Q 没有全零行。这表示每道题至少测量一个属性。

例如

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&1
\end{pmatrix}
\]

可解释为：

- 第 1 题只需要属性 1；
- 第 2 题只需要属性 2；
- 第 3 题同时需要两个属性。

## 合取规则

第 \(i\) 题的能力指示量为

\[
\xi^i
=
\prod_{j=1}^k (A^j)^{Q_{ij}}
=
\mathbf 1(A^j\ge Q_{ij},\ j=1,\ldots,k).
\tag{2.1}
\]

两个写法完全等价。

若 \(Q_{ij}=0\)，则

\[
(A^j)^0=1,
\]

该属性不会影响乘积。若 \(Q_{ij}=1\)，乘积中保留 \(A^j\)；只要缺少一个所需属性，乘积便为 0。

因此：

\[
\xi^i=1
\quad\Longleftrightarrow\quad
\boldsymbol A\ge \boldsymbol q_i
\]

逐元素成立。

## 第 2 节的无噪声模型

文章先研究

\[
R^i=\xi^i,
\qquad i=1,\ldots,m.
\tag{2.2}
\]

此时：

- 能力指示为 1，学生必定答对；
- 能力指示为 0，学生必定答错。

这一层把识别问题中的组合结构单独暴露出来。第 3 节再加入失误与猜测。

## 样本属性比例

如果潜在属性在概念上可见，样本中模式 \(\boldsymbol A\) 的比例为

\[
\widehat p_{\boldsymbol A}
=
\frac1N
\sum_{r=1}^N
\mathbf 1(\boldsymbol A_r=\boldsymbol A).
\tag{2.4}
\]

这些比例实际不可直接计算。它们在理论中承担连接观测矩与总体分布的桥梁：

\[
\widehat p_{\boldsymbol A}
\overset{\text{a.s.}}{\longrightarrow}
p_{\boldsymbol A}^*.
\]

## 本页对象关系

\[
\boldsymbol A_r
\xrightarrow[\text{合取规则}]{Q}
\boldsymbol\xi_r
\xrightarrow[\text{无噪声或 DINA}]{c,g}
\boldsymbol R_r.
\]

统计推断沿反方向进行：从全部 \(\boldsymbol R_r\) 的联合信息推断 Q，并同时剖面化属性分布。

[下一页：理想反应、B-vector 与 T-matrix](03-ideal-response-and-tmatrix.md)
