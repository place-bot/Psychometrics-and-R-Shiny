# RLCM 模型与局部独立

## 观测反应

一名被试对 \(J\) 道题的反应向量为

\[
\boldsymbol R=(R_1,\ldots,R_J)^\top,
\qquad R_j\in\{0,1\}.
\]

\(R_j=1\) 表示第 \(j\) 题作出正反应，在教育测量中通常表示答对。

## 潜在属性模式

被试拥有 \(K\) 个二分属性：

\[
\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_K)^\top
\in\{0,1\}^K.
\]

\(\alpha_k=1\) 表示掌握第 \(k\) 个属性。共有 \(2^K\) 个潜在类。群体中属性模式的比例为

\[
p_{\boldsymbol\alpha}
=P(\boldsymbol\alpha_i=\boldsymbol\alpha),
\qquad
p_{\boldsymbol\alpha}>0,
\qquad
\sum_{\boldsymbol\alpha}p_{\boldsymbol\alpha}=1.
\]

论文把全部比例排成

\[
\boldsymbol p
=
\left(
p_{\boldsymbol\alpha}:
\boldsymbol\alpha\in\{0,1\}^K
\right)^\top.
\]

严格正比例假设很重要：证明中的隔离等式需要每个潜在类都有正质量。允许结构零时要另做识别分析。

## 条件反应概率

给定属性模式，第 \(j\) 题的正反应概率为

\[
\theta_{j,\boldsymbol\alpha}
=P(R_j=1\mid\boldsymbol\alpha).
\]

于是

\[
P(R_j=r\mid\boldsymbol\alpha)
=
\theta_{j,\boldsymbol\alpha}^{\,r}
(1-\theta_{j,\boldsymbol\alpha})^{1-r},
\qquad r\in\{0,1\}.
\]

把所有项目和潜在类的概率排成

\[
\Theta
=
\left(\theta_{j,\boldsymbol\alpha}\right)_
{J\times 2^K}.
\]

行对应题目，列对应属性模式。

## 局部独立

论文的联合反应概率采用 Bernoulli product：

\[
P(\boldsymbol R=\boldsymbol r
\mid\boldsymbol\alpha,Q,\Theta)
=
\pi_{\boldsymbol r,\boldsymbol\alpha}(Q,\Theta)
=
\prod_{j=1}^J
(1-\theta_{j,\boldsymbol\alpha})^{1-r_j}
\theta_{j,\boldsymbol\alpha}^{r_j}.
\]

这表示给定 \(\boldsymbol\alpha\) 后，各题反应条件独立。边缘化潜在类得到观测分布：

\[
P(\boldsymbol R=\boldsymbol r
\mid Q,\Theta,\boldsymbol p)
=
\sum_{\boldsymbol\alpha\in\{0,1\}^K}
\pi_{\boldsymbol r,\boldsymbol\alpha}(Q,\Theta)
p_{\boldsymbol\alpha}.
\]

## 参数的两个来源

| 参数 | 大小 | 解释 |
| --- | ---: | --- |
| \(\Theta\) | \(J\times 2^K\) | 每个潜在类在每道题上的正反应概率 |
| \(\boldsymbol p\) | \(2^K\times1\) | 潜在类的群体比例 |

RLCM 与无约束 latent class model 的差异来自 \(\Theta\) 的结构：Q 矩阵规定哪些 \(\theta_{j,\boldsymbol\alpha}\) 必须相等，以及哪些应该保持次序。

## 一个两属性例子

若 \(K=2\)，列顺序取

\[
\boldsymbol 0=(0,0),\quad
\boldsymbol e_1=(1,0),\quad
\boldsymbol e_2=(0,1),\quad
\boldsymbol 1=(1,1),
\]

则

\[
\Theta=
\begin{pmatrix}
\theta_{1,00}&\theta_{1,10}&\theta_{1,01}&\theta_{1,11}\\
\vdots&\vdots&\vdots&\vdots\\
\theta_{J,00}&\theta_{J,10}&\theta_{J,01}&\theta_{J,11}
\end{pmatrix},
\qquad
\boldsymbol p=
\begin{pmatrix}
p_{00}\\p_{10}\\p_{01}\\p_{11}
\end{pmatrix}.
\]

后面的识别证明要从所有反应模式概率中唯一恢复这两组对象。
