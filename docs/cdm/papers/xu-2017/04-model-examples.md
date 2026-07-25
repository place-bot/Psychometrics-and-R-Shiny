# 六类诊断模型如何进入框架

论文用六个模型例子说明式 (2.2)--(2.3) 的覆盖范围。

## DINA

理想反应指标为

\[
\xi^{\mathrm{DINA}}_{j,\boldsymbol\alpha}
=
\mathbb I(\boldsymbol\alpha\succeq\boldsymbol q_j).
\]

以失误参数 \(s_j\) 和猜测参数 \(g_j\) 加入噪声：

\[
\theta_{j,\boldsymbol\alpha}
=
(1-s_j)^{
\xi^{\mathrm{DINA}}_{j,\boldsymbol\alpha}}
g_j^{
1-\xi^{\mathrm{DINA}}_{j,\boldsymbol\alpha}}.
\]

因此

\[
\theta_{j,\boldsymbol\alpha}
=
\begin{cases}
1-s_j,&\boldsymbol\alpha\succeq\boldsymbol q_j,\\
g_j,&\boldsymbol\alpha\nsucceq\boldsymbol q_j.
\end{cases}
\]

式 (2.2)--(2.3) 在 DINA 中对应 \(1-s_j>g_j\)。

## DINO

DINO 使用析取门。只要至少掌握一项所需属性，理想反应就是 1：

\[
\xi^{\mathrm{DINO}}_{j,\boldsymbol\alpha}
=
\mathbb I
\left(
\exists k:\ q_{jk}=1,\ \alpha_k=1
\right).
\]

成功概率仍由 \(1-s_j\) 与 \(g_j\) 两组构成。对于单属性题，DINA 与 DINO 的理想分组一致，所以式 (2.3) 同样由 \(1-s_j>g_j\) 保证。

## G-DINA

identity-link G-DINA 把所需属性的主效应与全部交互效应展开：

\[
\theta_{j,\boldsymbol\alpha}
=
\beta_{j0}
+
\sum_k\beta_{jk}q_{jk}\alpha_k
+
\sum_{k<k'}
\beta_{jkk'}
(q_{jk}\alpha_k)(q_{jk'}\alpha_{k'})
+
\cdots.
\]

没有被 \(\boldsymbol q_j\) 要求的属性不会进入该题反应函数。只要两个属性模式在该题所需属性上的约化模式相同，它们的成功概率相同。

## 线性 logistic model / logit-CDM

\[
\operatorname{logit}
\theta_{j,\boldsymbol\alpha}
=
\beta_{j0}
+
\sum_{k=1}^K
\beta_{jk}q_{jk}\alpha_k.
\]

等价概率形式为

\[
\theta_{j,\boldsymbol\alpha}
=
\frac{
\exp\left(
\beta_{j0}+\sum_k\beta_{jk}q_{jk}\alpha_k
\right)}
{1+
\exp\left(
\beta_{j0}+\sum_k\beta_{jk}q_{jk}\alpha_k
\right)}.
\]

它也称 compensatory RUM。

## reduced RUM / log-CDM

\[
\theta_{j,\boldsymbol\alpha}
=
\pi_j
\prod_{k=1}^K
r_{jk}^{\,q_{jk}(1-\alpha_k)},
\qquad 0<r_{jk}<1.
\]

\(\pi_j\) 是具备全部所需属性时的成功概率；每缺失一项属性，就乘以一个小于 1 的 penalty。取对数后得到加法形式：

\[
\log\theta_{j,\boldsymbol\alpha}
=
\beta_{j0}
+
\sum_k\beta_{jk}q_{jk}\alpha_k.
\]

## 论文列举的更广模型族

正文还提到 NIDA、NIDO、fusion model、rule-space method、attribute hierarchy method 与 general diagnostic model。主定理不依赖某一个具体 link function，只要 \(\Theta\) 满足论文的限制式即可。

## 统一视角

| 模型 | 能力充分组 | 能力不足组 | 题内参数化 |
| --- | --- | --- | --- |
| DINA | 一个高概率 | 一个共同低概率 | 两参数 |
| DINO | 至少一项所需属性即高 | 一个共同低概率 | 两参数 |
| G-DINA | 全部所需属性达到共同最高 | 可有多个概率 | 主效应与交互 |
| logit-CDM | 全部所需属性达到共同最高 | 随掌握组合变化 | logit 加法 |
| reduced RUM | 全部所需属性为 \(\pi_j\) | 按缺失属性乘 penalty | log 加法 |

论文识别的是统一表示中的 \(\Theta\) 与 \(\boldsymbol p\)。在具体模型内，若从模型参数到 \(\Theta\) 的参数化本身一对一，便可进一步识别相应的 \(s,g,\beta,\pi,r\) 等参数。
