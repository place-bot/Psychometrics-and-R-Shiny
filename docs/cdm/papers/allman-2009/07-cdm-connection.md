# 与 CDM 可识别性的接口

## 把一般潜在类翻译成 CDM

设测试测量 \(K\) 个二分属性。属性模式为

\[
\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_K)
\in\{0,1\}^K.
\]

允许的属性模式集合记作

\[
\mathcal A\subseteq\{0,1\}^K,
\]

其大小为

\[
r=|\mathcal A|.
\]

对项目 \(j\)，定义

\[
\theta_{j,\boldsymbol\alpha}
=
P(Y_j=1\mid\boldsymbol\alpha).
\]

在局部独立假设下，

\[
P(\boldsymbol Y=\boldsymbol y)
=
\sum_{\boldsymbol\alpha\in\mathcal A}
\nu_{\boldsymbol\alpha}
\prod_{j=1}^{J}
\theta_{j,\boldsymbol\alpha}^{y_j}
(1-\theta_{j,\boldsymbol\alpha})^{1-y_j}.
\tag{CDM-LCM}
\]

将每个属性模式当作一个潜在类别后：

| Allman 论文 | CDM |
| --- | --- |
| \(Z=i\) | 属性模式 \(\boldsymbol\alpha\) |
| \(r\) | 允许的属性模式数 \(|\mathcal A|\) |
| \(\pi_i\) | \(\nu_{\boldsymbol\alpha}\) |
| \(X_j\) | 项目反应 \(Y_j\) |
| \(M_j(i,\cdot)\) | \((1-\theta_{j,\boldsymbol\alpha},\theta_{j,\boldsymbol\alpha})\) |
| 条件独立 | CDM 的项目局部独立 |

## 第一层：恢复无约束类条件反应

若存在合适的三块题目并满足秩条件，Allman 路线可以得到

\[
P(\boldsymbol Y)
\longrightarrow
\left\{
\nu_{\boldsymbol\alpha},
\theta_{j,\boldsymbol\alpha}
\right\}
\quad
\text{up to an unknown common row permutation}.
\tag{Stage 1}
\]

此时恢复的是一张无名字的潜在类反应概率表。例如 \(K=2\) 时，理论上得到四行，但暂时不知道哪一行对应

\[
(0,0),(0,1),(1,0),(1,1).
\]

## 第二层：利用 CDM 结构解释这些行

CDM 识别还要证明

\[
\left\{
\nu_{\boldsymbol\alpha},
\theta_{j,\boldsymbol\alpha}
\right\}
\longrightarrow
\left\{
Q,\ \boldsymbol\alpha,\ \text{item parameters}
\right\}.
\tag{Stage 2}
\]

这一步依赖具体模型。

### DINA

项目 \(j\) 的 Q 向量为

\[
\boldsymbol q_j=(q_{j1},\ldots,q_{jK}).
\]

理想反应指标

\[
\eta_{j,\boldsymbol\alpha}
=
\prod_{k=1}^{K}\alpha_k^{q_{jk}}
\]

在掌握项目所需全部属性时为 1。DINA 反应概率为

\[
\theta_{j,\boldsymbol\alpha}
=
(1-s_j)^{\eta_{j,\boldsymbol\alpha}}
g_j^{1-\eta_{j,\boldsymbol\alpha}},
\]

等价地，

\[
\theta_{j,\boldsymbol\alpha}
=
\begin{cases}
1-s_j,&\eta_{j,\boldsymbol\alpha}=1,\\
g_j,&\eta_{j,\boldsymbol\alpha}=0.
\end{cases}
\]

Allman 定理可以帮助恢复 \(\theta\) 表，但从这张表恢复 \(\boldsymbol q_j,g_j,s_j\) 需要：

- 属性模式行可以被结构化命名；
- 项目中高、低反应概率组能和 \(\eta\) 对应；
- Q 矩阵有足够的完整性与重复测量；
- 参数满足区分掌握与未掌握的约束，例如 \(1-s_j>g_j\)。

### G-DINA

G-DINA 对项目所需属性的主效应和交互作用建模：

\[
P(Y_j=1\mid\boldsymbol\alpha)
=
\delta_{j0}
+
\sum_k\delta_{jk}\alpha_kq_{jk}
+
\sum_{k<\ell}
\delta_{jk\ell}
\alpha_k\alpha_\ell q_{jk}q_{j\ell}
+\cdots.
\]

一般潜在类层恢复的是每个属性模式下的反应概率。G-DINA 还要识别哪些效应存在、Q 行包含哪些属性，以及参数化是否唯一。

## 为什么一般空间的 generic 结论不能直接限制到 CDM

设一般潜在类参数空间为 \(\Theta_{\mathrm{LCM}}\)，DINA 参数空间通过约束映射嵌入其中：

\[
\Theta_{\mathrm{DINA}}
\subset
\Theta_{\mathrm{LCM}}.
\]

Allman 结果说坏集合

\[
\mathcal V\subset\Theta_{\mathrm{LCM}}
\]

在一般空间中测度为 0。仍可能出现

\[
\Theta_{\mathrm{DINA}}\subseteq\mathcal V.
\]

低维结构化子空间可能恰好落在一般空间的例外集合内。因此需要在 CDM 自己的参数空间中重新证明满秩或利用额外结构建立识别。

这也是后续 RLCM 识别论文的重要任务。

## Q 矩阵制造的行重复

若两个属性模式 \(\boldsymbol\alpha\) 与 \(\boldsymbol\alpha'\) 对所有项目都有相同理想反应，

\[
\eta_{j,\boldsymbol\alpha}
=
\eta_{j,\boldsymbol\alpha'},
\qquad
j=1,\ldots,J,
\]

在 DINA 下它们满足

\[
\theta_{j,\boldsymbol\alpha}
=
\theta_{j,\boldsymbol\alpha'}
\quad\forall j.
\]

于是两类的完整反应轮廓相同，只能识别比例之和

\[
\nu_{\boldsymbol\alpha}
+
\nu_{\boldsymbol\alpha'}.
\]

这个问题最终要由 Q 矩阵对属性模式的区分能力解决。

## 结构性零比例

若属性层级使某些模式不可能出现，则

\[
\nu_{\boldsymbol\alpha}=0
\]

对这些模式成立。Allman 的正类别比例假设不允许把零比例类别当成可识别的现存类别。

更合理的做法是把

\[
\mathcal A
=
\{\boldsymbol\alpha:\nu_{\boldsymbol\alpha}>0\}
\]

当作实际潜在类集合，再研究：

1. \(\mathcal A\) 是否已知；
2. 它能否从数据恢复；
3. 层级关系是否能由 \(\mathcal A\) 推断；
4. 在受限类别集合上 Q 是否仍可识别。

这会连接到属性模式学习、属性层级和稀疏潜在类模型。

## 标签置换在 CDM 中更复杂

普通潜在类模型只关心类 1、类 2 的名字。CDM 的标签包含多层含义：

- 潜在类行对应哪个 \(\boldsymbol\alpha\)；
- 属性坐标的顺序；
- Q 矩阵列对应哪种技能；
- 某个技能标签如何与内容专家解释对应。

即使恢复了潜在类表，仍可能存在属性列置换：

\[
(Q,\boldsymbol\alpha)
\mapsto
(QP,P^\top\boldsymbol\alpha),
\]

其中 \(P\) 是属性维度置换矩阵。统计分布可能不变，但教育解释中的“代数”“几何”等属性名字需要外部内容锚定。

## 对 continuous-Q 与 partial mastery 的影响

### continuous-Q

若 Q 元素从 \(\{0,1\}\) 放宽到连续权重，项目反应概率的结构约束改变。只要潜在属性模式仍离散，模型仍可先写成有限潜在类混合，但一般潜在类恢复后的第二阶段映射可能更难唯一。

### partial mastery

若每个属性掌握度连续，

\[
\boldsymbol a\in[0,1]^K,
\]

潜变量不再是有限类别。Corollary 5 不能直接使用。需要连续潜变量、非参数混合、积分变换或特定响应函数的识别工具。

Theorem 8 的非参数混合结果仍假定有限个混合分量，只是每个观测方向的分量分布非参数；它不等同于连续属性分布。

## 这篇论文在 CDM 证明中的合适位置

可以把识别论证组织成三步：

\[
\boxed{
P(\boldsymbol Y)
\overset{\text{三块满秩}}{\longrightarrow}
\text{无名字的潜在类响应表}
}
\]

\[
\boxed{
\text{响应表}
\overset{\text{Q 与模型约束}}{\longrightarrow}
\text{属性模式、项目结构和参数}
}
\]

\[
\boxed{
\text{统计结构}
\overset{\text{内容锚定}}{\longrightarrow}
\text{可解释的属性名称}
}
\]

Allman 等人主要支撑第一步。CDM 专门论文完成第二步，专家审查与测验内容设计支撑第三步。

## 后续精读链

| 后续论文 | 要补上的问题 |
| --- | --- |
| Kruskal (1977) | 三路分解唯一性定理本身怎样证明、条件怎样理解 |
| Xu (2017) | 二分 RLCM 如何利用三块条件建立可识别性 |
| Gu & Xu：DINA 识别 | DINA 参数的充分与必要条件 |
| Gu & Xu (2021) | Q 矩阵本身何时可识别 |
| Xu & Shang (2018) | 潜在结构与受限潜在类如何共同恢复 |
| Chen et al. (2015/2017) | Q 结构和潜在类的估计、正则化及有限样本行为 |

