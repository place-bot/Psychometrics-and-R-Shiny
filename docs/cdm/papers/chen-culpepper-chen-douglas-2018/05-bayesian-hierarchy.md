# 完整贝叶斯层级模型

## 五层未知量

论文联合估计：

\[
\Theta
=
\left(
Q,\boldsymbol s,\boldsymbol g,
\boldsymbol\alpha,\boldsymbol\pi
\right).
\]

层级结构如下：

```text
π ──> α_i ──┐
             ├──> η_ij(Q, α_i) ──> Y_ij
Q ──────────┘                    ↑
                         (s_j, g_j)
```

## 作答层

\[
Y_{ij}\mid
\boldsymbol\alpha_i,s_j,g_j,\boldsymbol q_j
\sim
\operatorname{Bernoulli}
\left(
(1-s_j)^{\eta_{ij}}g_j^{1-\eta_{ij}}
\right).
\]

## 属性模式层

\[
P(\boldsymbol\alpha_i=\boldsymbol a_c\mid\boldsymbol\pi)
=\pi_c.
\]

学生之间条件独立，同一名学生的作答在给定属性与题目参数后条件独立。

## 潜在类比例层

\[
\boldsymbol\pi
\sim
\operatorname{Dirichlet}(\boldsymbol\delta_0).
\]

补充代码使用

\[
\boldsymbol\delta_0=\boldsymbol1_{2^K},
\]

即对单纯形均匀的 Dirichlet 先验。

## 题目参数层

对每道题，

\[
p(s_j,g_j)
\propto
s_j^{\alpha_s-1}(1-s_j)^{\beta_s-1}
g_j^{\alpha_g-1}(1-g_j)^{\beta_g-1}
I(0\le g_j<1-s_j\le1).
\]

补充代码把四个 Beta 超参数均设为 1，并通过截断抽样维持

\[
g_j<1-s_j.
\]

## Q 层

\[
p(Q)\propto I(Q\in\mathcal Q).
\]

这等价于在有限的可识别集合 \(\mathcal Q\) 上使用均匀先验。集合外的 Q 先验概率为 0。

## 联合后验

忽略归一化常数：

\[
\begin{aligned}
p(&Q,\boldsymbol s,\boldsymbol g,
\boldsymbol\alpha,\boldsymbol\pi\mid\boldsymbol Y)
\propto
\prod_{i=1}^{N}\prod_{j=1}^{J}
p(Y_{ij}\mid
\boldsymbol\alpha_i,s_j,g_j,\boldsymbol q_j)\\
&\times
\prod_{i=1}^{N}\pi_{c(i)}
\times
p(\boldsymbol\pi)
\times
\prod_{j=1}^{J}p(s_j,g_j)
\times
I(Q\in\mathcal Q),
\end{aligned}
\]

其中 \(c(i)\) 是学生 \(i\) 当前所属的属性类。

## 一轮 MCMC 的依赖关系

论文的 MH 版本按以下顺序：

\[
\boldsymbol g^{(t)}
\leftarrow
p(\boldsymbol g\mid
\boldsymbol Y,\boldsymbol s^{(t-1)},
\boldsymbol\alpha^{(t-1)},Q^{(t-1)}),
\]

\[
\boldsymbol s^{(t)}
\leftarrow
p(\boldsymbol s\mid
\boldsymbol Y,\boldsymbol g^{(t)},
\boldsymbol\alpha^{(t-1)},Q^{(t-1)}),
\]

\[
\boldsymbol\alpha^{(t)}
\leftarrow
p(\boldsymbol\alpha\mid
\boldsymbol Y,\boldsymbol s^{(t)},\boldsymbol g^{(t)},
\boldsymbol\pi^{(t-1)},Q^{(t-1)}),
\]

\[
\boldsymbol\pi^{(t)}
\leftarrow
p(\boldsymbol\pi\mid\boldsymbol\alpha^{(t)}),
\]

\[
Q^{(t)}
\leftarrow
\text{MH}\{p(Q\mid
\boldsymbol Y,\boldsymbol s^{(t)},\boldsymbol g^{(t)},
\boldsymbol\alpha^{(t)})\}.
\]

受限 Gibbs 只替换最后一步。

## Q 更新为何条件于当前属性样本

一旦 \(\boldsymbol\alpha\) 已抽样，Q 的条件后验无需再对 \(2^K\) 个类求和。对一个只改变少量 q 元素的候选，似然比只涉及理想反应发生变化的题目，代码可以局部计算。

[下一页：各层先验与完整条件分布](06-priors-and-conditionals.md)
