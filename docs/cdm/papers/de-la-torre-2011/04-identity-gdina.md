# identity-link G-DINA

## 饱和反应函数

对需要 \(K_j^*\) 个属性的项目 \(j\)，G-DINA 写作

\[
\begin{aligned}
P(\boldsymbol\alpha^*_{lj})
=\;&
\delta_{j0}
+\sum_{k=1}^{K_j^*}\delta_{jk}\alpha_{lk}\\
&+
\sum_{k<k'}\delta_{jkk'}
\alpha_{lk}\alpha_{lk'}
+\cdots\\
&+
\delta_{j12\cdots K_j^*}
\prod_{k=1}^{K_j^*}\alpha_{lk}.
\end{aligned}
\]

这相当于在二元属性立方体上进行完整的主效应与交互分解。

## 两属性项目

当 \(K_j^*=2\) 时，

\[
P(\alpha_1,\alpha_2)
=
\delta_0
+\delta_1\alpha_1
+\delta_2\alpha_2
+\delta_{12}\alpha_1\alpha_2.
\]

四个模式的概率为

\[
\begin{aligned}
P(00)&=\delta_0,\\
P(10)&=\delta_0+\delta_1,\\
P(01)&=\delta_0+\delta_2,\\
P(11)&=\delta_0+\delta_1+\delta_2+\delta_{12}.
\end{aligned}
\]

反向解得

\[
\begin{aligned}
\delta_0&=P(00),\\
\delta_1&=P(10)-P(00),\\
\delta_2&=P(01)-P(00),\\
\delta_{12}
&=
P(11)-P(10)-P(01)+P(00).
\end{aligned}
\]

\(\delta_{12}\) 衡量联合掌握超出两个单独增量之和的部分。

## 三属性项目

当 \(K_j^*=3\) 时共有八个参数：

\[
\delta_0,
\delta_1,\delta_2,\delta_3,
\delta_{12},\delta_{13},\delta_{23},
\delta_{123}.
\]

三阶交互可由包含-排除形式得到：

\[
\begin{aligned}
\delta_{123}
=\;&P(111)
-P(110)-P(101)-P(011)\\
&+P(100)+P(010)+P(001)
-P(000).
\end{aligned}
\]

## 参数符号

论文给出的典型解释是：

- \(\delta_0\geq 0\)；
- 主效应通常非负；
- 交互效应可以为正或负。

负交互并不自动表示模型异常。它表示联合效应小于低阶效应的简单相加。例如两个属性各自带来显著提升时，成功概率接近上界后，二者联合的额外增量可能为负。

## 饱和模型的参数代价

每题参数量取决于 \(K_j^*\)：

| \(K_j^*\) | 成功概率/参数数 |
| ---: | ---: |
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |

G-DINA 的灵活性随所需属性数指数增长。样本量有限时，某些约化模式后验人数很少，概率估计和标准误会迅速变得不稳定。

## 与 DINA 的直接关系

DINA 把

\[
P(000),P(100),\ldots
\]

中除全掌握组以外的概率约束为同一个 \(g_j\)。G-DINA 允许这些部分掌握组呈现不同水平，从而揭示：

- 哪个属性贡献更大；
- 是否存在补偿；
- 是否存在必要的联合掌握；
- DINA 的二组压缩是否过强。
