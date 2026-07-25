# DINA、DINO 与 A-CDM

## DINA

DINA 的成功概率为

\[
P(\boldsymbol\alpha^*_{lj})
=
\begin{cases}
g_j,
&\boldsymbol\alpha^*_{lj}\prec\boldsymbol 1,\\
1-s_j,
&\boldsymbol\alpha^*_{lj}=\boldsymbol 1.
\end{cases}
\]

在 identity-link G-DINA 中，只保留

\[
\delta_{j0}
\quad\text{和}\quad
\delta_{j12\cdots K_j^*}.
\]

因此

\[
g_j=\delta_{j0},
\qquad
1-s_j
=
\delta_{j0}
+\delta_{j12\cdots K_j^*}.
\]

DINA 表达严格合取过程：全部属性同时具备后才出现概率跃升。

## DINO

DINO 的成功概率为

\[
P(\boldsymbol\alpha^*_{lj})
=
\begin{cases}
g'_j,
&\boldsymbol\alpha^*_{lj}=\boldsymbol 0,\\
1-s'_j,
&\boldsymbol\alpha^*_{lj}\neq\boldsymbol 0.
\end{cases}
\]

它表达析取过程：掌握任意一个所需属性即可进入高成功组。

identity-link 参数必须满足交替符号与相同绝对值约束。两属性时：

\[
\delta_1=\delta_2=-\delta_{12}.
\]

于是

\[
P(10)=P(01)=P(11).
\]

## A-CDM

令全部交互效应为零：

\[
P(\boldsymbol\alpha^*_{lj})
=
\delta_{j0}
+\sum_{k=1}^{K_j^*}\delta_{jk}\alpha_{lk}.
\]

每个属性在概率标度上贡献固定增量，因此参数数为

\[
K_j^*+1.
\]

两属性时，A-CDM 要求

\[
P(11)
=
P(10)+P(01)-P(00).
\]

这条等式后来直接用于论文的临床数据解释。

## 三种模型的几何约束

设两属性题四个概率为

\[
\boldsymbol P_j=
\left(P_{00},P_{10},P_{01},P_{11}\right)^\top.
\]

则：

| 模型 | 等式约束 | 自由参数 |
| --- | --- | ---: |
| G-DINA | 无 | 4 |
| DINA | \(P_{00}=P_{10}=P_{01}\) | 2 |
| DINO | \(P_{10}=P_{01}=P_{11}\) | 2 |
| A-CDM | \(P_{11}-P_{10}-P_{01}+P_{00}=0\) | 3 |

Wald 检验就是检验估计的 \(\boldsymbol P_j\) 距离这些约束是否显著。

## guessing 与 slipping 的解释边界

论文沿用 \(g,s\) 作为方便记忆的名称，同时提醒：

- 高 \(g\) 可能来自 Q 矩阵遗漏；
- 高 \(g\) 可能来自替代策略；
- 高 \(s\) 可能来自粗心、题目歧义或额外能力需求。

它们是反应概率参数，不能单凭名称还原学生的真实认知过程。
