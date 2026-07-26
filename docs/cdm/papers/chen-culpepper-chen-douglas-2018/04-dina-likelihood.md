# 理想反应、题目反应函数与似然

## 单题答对概率

DINA 把学生分成两组：

\[
P(Y_{ij}=1\mid\eta_{ij}=1)=1-s_j,
\]

\[
P(Y_{ij}=1\mid\eta_{ij}=0)=g_j.
\]

合并后得到原文式（2）：

\[
P(Y_{ij}=1\mid
\boldsymbol\alpha_i,s_j,g_j,\boldsymbol q_j)
=
(1-s_j)^{\eta_{ij}}g_j^{1-\eta_{ij}}.
\]

若 \(\eta_{ij}=1\)，右侧为 \(1-s_j\)；若 \(\eta_{ij}=0\)，右侧为 \(g_j\)。

## Bernoulli 概率质量

令

\[
p_{ij}
=(1-s_j)^{\eta_{ij}}g_j^{1-\eta_{ij}},
\]

则

\[
P(Y_{ij}=y_{ij}\mid\cdots)
=
p_{ij}^{y_{ij}}(1-p_{ij})^{1-y_{ij}}.
\]

展开 \(1-p_{ij}\)：

\[
1-p_{ij}
=
s_j^{\eta_{ij}}(1-g_j)^{1-\eta_{ij}}.
\]

因此单题贡献为

\[
\left[
(1-s_j)^{\eta_{ij}}g_j^{1-\eta_{ij}}
\right]^{y_{ij}}
\left[
s_j^{\eta_{ij}}(1-g_j)^{1-\eta_{ij}}
\right]^{1-y_{ij}}.
\]

## 已知学生属性时的完整数据似然

条件于 \(\boldsymbol\alpha=(\boldsymbol\alpha_1,\ldots,\boldsymbol\alpha_N)^{\mathsf T}\)，并采用局部独立：

\[
\begin{aligned}
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q)
&=
\prod_{i=1}^{N}\prod_{j=1}^{J}
\left[
(1-s_j)^{\eta_{ij}}g_j^{1-\eta_{ij}}
\right]^{y_{ij}}\\
&\quad\times
\left[
s_j^{\eta_{ij}}(1-g_j)^{1-\eta_{ij}}
\right]^{1-y_{ij}}.
\end{aligned}
\]

这就是 Q 的 MH 接受率和逐元素 Gibbs 条件概率所用的核心量。

## 边际似然

学生属性不可观测。对第 \(i\) 名学生，把 \(2^K\) 种属性模式积分掉：

\[
\begin{aligned}
p(\boldsymbol Y\mid\boldsymbol s,\boldsymbol g,\boldsymbol\pi,Q)
=
\prod_{i=1}^{N}
\sum_{\boldsymbol a_c\in\{0,1\}^K}
\pi_c
\prod_{j=1}^{J}
&\left[
(1-s_j)^{\eta_{cj}}g_j^{1-\eta_{cj}}
\right]^{y_{ij}}\\
\times&
\left[
s_j^{\eta_{cj}}(1-g_j)^{1-\eta_{cj}}
\right]^{1-y_{ij}},
\end{aligned}
\]

其中

\[
\eta_{cj}
=
I(\boldsymbol a_c^{\mathsf T}\boldsymbol q_j
=
\boldsymbol q_j^{\mathsf T}\boldsymbol q_j).
\]

## 为什么采样 \(\boldsymbol\alpha_i\)

直接使用边际似然时，每个学生都含一个 \(2^K\) 项的求和。数据增强把每名学生的属性模式作为潜变量抽样。条件于当前参数，

\[
P(\boldsymbol\alpha_i=\boldsymbol a_c\mid-)
\propto
\pi_c
\prod_{j=1}^{J}
P(Y_{ij}=y_{ij}\mid
\boldsymbol a_c,s_j,g_j,\boldsymbol q_j).
\]

归一化这 \(2^K\) 个权重后即可做一次 categorical 抽样。

## 一个两属性例子

设某题

\[
\boldsymbol q_j=(1,1)^{\mathsf T},
\qquad
s_j=0.10,\quad g_j=0.20.
\]

四种属性模式的答对概率为：

| \(\boldsymbol\alpha\) | \(\eta\) | 答对概率 |
| --- | ---: | ---: |
| \((0,0)\) | 0 | 0.20 |
| \((1,0)\) | 0 | 0.20 |
| \((0,1)\) | 0 | 0.20 |
| \((1,1)\) | 1 | 0.90 |

DINA 只识别“全部具备”和“至少缺一个”两组。某个具体属性缺失的影响无法由这道题单独区分；Q 中的单位行和多题覆盖帮助全局模型区分各属性。

[下一页：完整贝叶斯层级模型](05-bayesian-hierarchy.md)
