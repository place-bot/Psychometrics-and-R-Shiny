# 整张 Q 的后验众数与列置换

## 属性标签交换

对任意 \(K\times K\) 列置换矩阵 \(R\)，同时变换

\[
Q^\star=QR,
\qquad
\boldsymbol\alpha_i^\star=R^{\mathsf T}\boldsymbol\alpha_i,
\]

会保持 DINA 的理想反应与观测分布。属性列名称由模型自身无法确定。

## 二进制列编码

令

\[
\boldsymbol v
=
(2^{J-1},2^{J-2},\ldots,2,1)^{\mathsf T}.
\]

Q 的第 \(k\) 列编码为整数

\[
z_k=\boldsymbol v^{\mathsf T}Q_k.
\]

于是整张 Q 对应一个 \(K\) 维整数向量：

\[
\boldsymbol z(Q)=(z_1,\ldots,z_K).
\]

## 规范化列顺序

把 \(\boldsymbol z(Q)\) 按降序排列：

\[
\widetilde{\boldsymbol z}(Q)
=
\operatorname{sort}_{\downarrow}
\{\boldsymbol z(Q)\}.
\]

列置换等价的 Q 会得到同一个规范编码。对 MCMC 保留样本统计各编码出现次数，频率最高者对应

\[
\widehat Q_{\text{mode}}.
\]

## 为什么使用整张矩阵众数

论文模拟的“\(\widehat Q=Q\)”要求每一个元素均正确。整张 Q 的后验众数直接面向这个 0--1 整体损失：

\[
L(\widehat Q,Q)
=
I(\widehat Q\not\sim Q),
\]

其中 \(\sim\) 表示列置换等价。

## 逐元素后验平均

另一种摘要是

\[
\overline q_{jk}
=
\frac1M\sum_{m=1}^{M}q_{jk}^{(m)},
\]

它表示当前标签对齐方案下某个边被包含的后验频率。逐元素阈值

\[
\widehat q_{jk}
=
I(\overline q_{jk}>0.5)
\]

面向 Hamming 损失，却不自动保持整张 Q 的结构约束。

## 原文自己的警告

论文指出，\(K\) 墑大时不同整张 Q 的数量指数增长。即使链访问了高概率区域，单张矩阵的出现频率也可能很低，可靠识别众数需要很长的链。作者把逐元素众数列为未来研究方向。

## 本站进一步发现

当前 `edina` 包采用逐元素平均后阈值 0.5。本站构造了 \(K=2,J=6\) 的三个合法后验样本，它们逐元素多数票后的第一列只有两个 1，违反每属性至少三题的限制。

因此使用逐元素摘要后应再次调用可识别性检查。可选修正包括：

- 在采样过的整张 Q 中选后验众数；
- 把逐元素均值投影到 \(\mathcal Q\)；
- 在满足约束的候选中最小化加权 Hamming 损失。

这个反例针对当前软件汇总策略，不改变原论文对整张 Q 众数的实验结论。

[下一页：Experiment——模拟设计](19-simulation-design.md)
