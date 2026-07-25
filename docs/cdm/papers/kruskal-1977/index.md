# Kruskal (1977) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Joseph B. Kruskal. *Three-way Arrays: Rank and Uniqueness of Trilinear Decompositions, with Application to Arithmetic Complexity and Statistics*. |
| 期刊 | *Linear Algebra and its Applications*, 18(2), 95--138, 1977 |
| DOI | [10.1016/0024-3795(77)90069-6](https://doi.org/10.1016/0024-3795(77)90069-6) |
| 出版商页面 | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/0024379577900696) |
| 开放索引 | [CORE 记录与全文索引](https://core.ac.uk/outputs/82529515) |
| 论文类型 | 多线性代数与唯一性理论；没有数据集、模拟实验或经验比较 |
| 官方代码 | 未提供 |

这篇论文同时研究三件相互关联、又需要严格区分的事：

1. 怎样定义三路数组的秩；
2. 怎样给三路数组秩建立下界；
3. 什么时候一个三线性分解只存在置换与缩放两类歧义。

CDM 文献最常调用第 3 部分，即后来写成

\[
k_A+k_B+k_C\ge 2R+2
\]

的 Kruskal 唯一性条件。原文的范围更广，还讨论了 slab-space、张量秩下界、算术复杂度和统计模型。

## 一句话主线

\[
\underbrace{\mathcal X
=\sum_{r=1}^{R}
\boldsymbol a_r\otimes\boldsymbol b_r\otimes\boldsymbol c_r}
_{\text{一个可观测三路数组}}
\quad+\quad
\underbrace{k_A+k_B+k_C\ge2R+2}
_{\text{三个方向都足够难以混淆}}
\]

\[
\Longrightarrow
\quad
\underbrace{A,B,C\text{ 可由 }\mathcal X\text{ 恢复}}
_{\text{允许共同置换与相互抵消的缩放}}.
\]

对潜在类模型，共同置换对应类别标签交换；概率向量的归一化约束可以固定缩放。因此，这条代数定理成为 Allman 等人以及大量 CDM 可识别性证明的底层工具。

## 推荐阅读顺序

1. [问题与历史位置](01-question-and-history.md)：矩阵分解为什么容易多解，三路数组增加了什么约束。
2. [三路数组、triad 与秩](02-array-rank-and-slabs.md)：逐字母解释 \(X,I,J,K\)、slab、\(\dim_\ell\) 和张量秩。
3. [三重积与固有歧义](03-triple-product.md)：写清 \([A,B,C]\)、CP/PARAFAC 表示、置换与缩放。
4. [Kruskal rank](04-kruskal-rank.md)：说明 \(k\)-rank 与普通矩阵秩的差别及计算方法。
5. [核心唯一性定理](05-uniqueness-theorem.md)：Theorem 4a、条件的读法、结论和边界。
6. [证明思路](06-proof-roadmap.md)：原文的置换引理主线，以及 Rhodes 的现代切片—投影证明。
7. [理论结果与应用](07-results-and-applications.md)：秩下界、算术复杂度、统计模型和证据边界。
8. [完整手算例子](08-worked-examples.md)：一个满足条件的 \(R=3\) 分解和一个多解反例。
9. [可计算检查](09-computational-check.md)：运行本站脚本，精确计算 \(k\)-rank 与张量等价性。
10. [与 CDM 的接口](10-cdm-connection.md)：三块项目反应、潜在属性模式、标签置换和 Q 矩阵。
11. [符号表](11-symbols.md)：统一查询原文记号、现代记号、维度和含义。
12. [总结与后续问题](12-summary.md)：结论、限制及其在后续论文中的发展。
13. [参考文献](references.md)：原文与本专题用于解释证明的直接来源。

## 本专题怎样处理原文与后续证明

Kruskal 的原始证明篇幅长，Theorem 4 还包含 4a、4b、4c 等由简到繁的版本。本站按两层整理：

- 原文的摘要、定义、秩下界、Theorem 4a、应用范围和历史结论按 1977 论文陈述；
- 证明页使用 Rhodes (2010) 的开放版本解释同一定理，因为它把关键切片、投影和归纳步骤写得更紧凑。

后续证明会明确标注来源。Theorem 4b、4c 比 4a 条件更细，本专题解释它们的地位，但 CDM 主线先完整掌握最常用的 4a。

!!! warning "理论结论的证据形态"
    这篇论文的证据由定义、引理、定理和证明组成。论文没有训练集、测试集、准确率表或软件仓库。本站的脚本只复现代数检查，不代表原作者提供了数值算法。
