# 标准误与分类

## 附录的目标

参数点估计为

\[
\widehat{\boldsymbol\beta}
=
(\widehat g_1,\widehat s_1,\ldots,\widehat g_J,\widehat s_J)^\mathsf T.
\]

论文用边际对数似然的观测信息矩阵近似协方差：

\[
\widehat{\operatorname{Cov}}
(\widehat{\boldsymbol\beta})
\approx
\mathcal I(\widehat{\boldsymbol\beta})^{-1}.
\tag{13}
\]

标准误是逆矩阵对角元素的平方根。

## 把属性后验压到题目理想状态

定义

\[
p_j(z\mid\boldsymbol X_i)
=
\sum_{l:\eta_{lj}=z}
P(\boldsymbol\alpha_l\mid\boldsymbol X_i).
\tag{14}
\]

它表示给定学生完整反应向量后，该生在题 \(j\) 上处于理想状态 \(z\) 的后验概率。

## 单个学生对参数的期望得分

令

\[
P_j(0)=g_j,
\qquad
P_j(1)=1-s_j.
\]

对于 \(\beta_{j0}=g_j\)：

\[
u_{i,j0}
=
p_j(0\mid\boldsymbol X_i)
\frac{
X_{ij}-g_j
}{
g_j(1-g_j)
}.
\tag{15}
\]

对于 \(\beta_{j1}=s_j\)，因为

\[
\frac{\partial(1-s_j)}{\partial s_j}=-1,
\]

得：

\[
u_{i,j1}
=
p_j(1\mid\boldsymbol X_i)
\frac{
(1-s_j)-X_{ij}
}{
(1-s_j)s_j
}.
\tag{16}
\]

## Equation A15

把所有 \(2J\) 个参数得分排成向量 \(\boldsymbol u_i\)。论文的 A15 可以写成：

\[
\mathcal I(\widehat{\boldsymbol\beta})
\approx
\sum_{i=1}^{I}
\boldsymbol u_i\boldsymbol u_i^\mathsf T
\bigg|_{\boldsymbol\beta=\widehat{\boldsymbol\beta}}.
\tag{17}
\]

这会产生一个

\[
2J\times2J
\]

信息矩阵，包含不同题目参数之间因属性模式不确定性而产生的协方差。

## 为什么不能只用两个二项分布公式

若每人的 \(\eta_{ij}\) 已知，可近似写

\[
\operatorname{SE}(\widehat g_j)
\approx
\sqrt{
\frac{g_j(1-g_j)}{I_j^{(0)}}
}.
\]

在 DINA 中，\(\eta_{ij}\) 是后验不确定的，并且同一属性模式同时影响多道题。A15 通过完整后验和交叉乘积保留这部分依赖。

## 模拟中怎样验证标准误

100 次重复中，论文比较：

- 每次拟合得到的模型标准误，再取平均；
- 100 个参数估计的经验标准差。

两者非常接近。论文报告模型标准误平均约比经验标准差保守 2%。

## 边界估计

真实数据 Item 1 的 DINA 结果为

\[
\widehat g_1=0.00,
\qquad
\operatorname{SE}(\widehat g_1)=0.050.
\]

当参数接近 0 或 1 时：

- 正态近似可能不对称；
- 信息矩阵可能病态；
- 不同先验或约束会显著影响结果；
- Wald 区间可能越出 \([0,1]\)。

Table 4 中 HO-DINA 对同一 \(g_1\) 给出标准误 0.004，显示潜变量分布和贝叶斯估计会改变边界附近的不确定性。

## 属性模式分类

EM 已经产生

\[
w_{il}
=
P(\boldsymbol\alpha_l\mid\boldsymbol X_i).
\]

可据此定义：

### MAP 模式分类

\[
\widehat l_i^{\text{MAP}}
=
\arg\max_l w_{il}.
\]

### 单属性 EAP

\[
\widehat P(\alpha_{ik}=1\mid\boldsymbol X_i)
=
\sum_{l:\alpha_{lk}=1}
w_{il}.
\]

本文主要研究项目参数校准。讨论部分明确把模式可识别性、分类方法、测验长度和 Q 矩阵规格列为需要系统研究的后续问题。
