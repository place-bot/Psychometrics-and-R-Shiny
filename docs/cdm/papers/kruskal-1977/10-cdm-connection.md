# 与 CDM 的接口

## 把项目分成三块

设潜在属性模式为

\[
\boldsymbol\alpha\in\mathcal A,
\qquad
|\mathcal A|=R.
\]

把项目划分为三个互不重叠的块：

\[
\mathcal J_1,\qquad
\mathcal J_2,\qquad
\mathcal J_3.
\]

对第 \(t\) 块，把属性模式 \(\boldsymbol\alpha_r\) 下所有块反应模式的概率排成列

\[
\boldsymbol m_{t,r}
=
\left[
P(\boldsymbol X_{\mathcal J_t}=\boldsymbol x
\mid
\boldsymbol\alpha_r)
\right]_{\boldsymbol x}.
\]

再组成矩阵

\[
M_t=
\begin{bmatrix}
\boldsymbol m_{t,1}&\cdots&\boldsymbol m_{t,R}
\end{bmatrix}.
\]

## 条件独立产生三重积

若给定属性模式后，三个项目块条件独立，则总体联合分布为

\[
\mathcal P
=
\sum_{r=1}^{R}
\pi_r
\boldsymbol m_{1,r}
\otimes
\boldsymbol m_{2,r}
\otimes
\boldsymbol m_{3,r}.
\tag{11}
\]

把混合权重吸收到第一个矩阵：

\[
\widetilde M_1
=
M_1\operatorname{diag}(\boldsymbol\pi),
\]

于是

\[
\mathcal P
=[\widetilde M_1,M_2,M_3].
\]

这就是 Kruskal 定理可以进入 CDM 的位置。

## Kruskal 条件

若

\[
k_{M_1}+k_{M_2}+k_{M_3}\ge2R+2,
\tag{12}
\]

并且所有 \(\pi_r>0\)，则乘以正对角权重不会降低相应列之间的线性独立关系：

\[
k_{\widetilde M_1}=k_{M_1}.
\]

因此总体反应分布决定三个块条件概率矩阵，允许共同列置换与缩放。

## 概率归一化怎样固定缩放

对 \(M_2,M_3\) 的任一列，

\[
\boldsymbol 1^\mathsf T\boldsymbol m_{t,r}=1.
\]

把恢复出的列重新归一化，就能固定这两个方向的缩放。第一个方向归一化后的列给出 \(M_1\)，被吸收的列和给出

\[
\pi_r.
\]

因此，最终保留的歧义是所有矩阵使用同一个列置换。

## 共同置换在 CDM 中表示什么

Kruskal 定理恢复的是 \(R\) 个无名字潜在成分。它能说明：

\[
\{\text{成分 1},\ldots,\text{成分 \(R\)}\}
\]

可恢复为一个集合，却不会自动告诉我们哪一列对应

\[
(0,0,\ldots,0),\quad
(1,0,\ldots,0),\quad\ldots
\]

这样的具体属性模式。

把成分标签固定到认知含义，需要使用：

- 已知或可识别的 Q 矩阵；
- DINA、DINO、G-DINA 等项目反应约束；
- 单调性或理想反应结构；
- 属性层级或其他结构假设。

## Allman (2009) 做了哪一步

Allman、Matias 与 Rhodes 把多个观测变量组合成三个超级变量，并证明块矩阵在一般参数点上具有足够高的 Kruskal rank。

因此两篇论文的分工是：

| 论文 | 完成的桥 |
| --- | --- |
| Kruskal (1977) | 三个因子满足 \(k\)-rank 总和条件 \(\Rightarrow\) 三重积分解本质唯一 |
| Allman et al. (2009) | 多个观测变量怎样分成三块，以及块矩阵为何泛满足秩条件 |
| CDM 识别论文 | Q 矩阵和具体响应模型怎样把无名字潜在类固定为属性模式 |

## 条件失败后的正确处理

若式 (12) 失败，可按以下顺序继续：

1. 改变三块项目的划分；
2. 合并更多题目，提高每个块的反应模式数；
3. 使用模型结构直接证明某些块矩阵满秩；
4. 查找比 Theorem 4a 更细的张量唯一性条件；
5. 使用 CDM 专门的可识别性定理；
6. 构造等价参数，判断是否真的不可识别。

“不等式未通过”是诊断结果；最终识别结论仍需正面证明或反例。

## 对有限样本研究的提醒

Kruskal 条件作用于总体概率矩阵。有限样本中即使模型可识别，也可能出现：

- 两个潜在类反应概率非常接近；
- 某些子式接近 0；
- 经验张量噪声放大；
- 估计具有很大标准误；
- 数值算法对初值敏感。

代数唯一性与稳定估计属于两个层次。后续 CDM 模拟研究需要同时报告识别条件和有限样本表现。
