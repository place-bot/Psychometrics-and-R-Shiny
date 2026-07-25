# LLM、G-NIDA 与 R-RUM

## logit CDM 与 LLM

饱和 logit CDM 为

\[
\operatorname{logit}
\left[P(\boldsymbol\alpha^*_{lj})\right]
=
\lambda_{j0}
+\sum_k\lambda_{jk}\alpha_{lk}
+\sum_{k<k'}\lambda_{jkk'}\alpha_{lk}\alpha_{lk'}
+\cdots.
\]

删除全部交互项得到 LLM：

\[
\operatorname{logit}
\left[P(\boldsymbol\alpha^*_{lj})\right]
=
\lambda_{j0}
+\sum_{k=1}^{K_j^*}
\lambda_{jk}\alpha_{lk}.
\]

因此

\[
P(\boldsymbol\alpha^*_{lj})
=
\frac{
\exp\left(\lambda_{j0}+\sum_k\lambda_{jk}\alpha_{lk}\right)
}{
1+\exp\left(\lambda_{j0}+\sum_k\lambda_{jk}\alpha_{lk}\right)
}.
\]

属性在 odds 上具有乘法效应，在 log-odds 上具有加法效应。

## NIDA 的属性层噪声

传统 NIDA 把 guessing 和 slipping 放在属性层。项目成功需要每个所需属性都被成功执行：

\[
P(\boldsymbol\alpha^*_{lj})
=
\prod_{k=1}^{K_j^*}
g_k^{1-\alpha_{lk}}
(1-s_k)^{\alpha_{lk}}.
\]

这里的乘号表示各属性执行概率相乘。传统形式要求同一属性在不同项目上共享 \(g_k,s_k\)，限制很强。

## G-NIDA

G-NIDA 允许参数随项目变化：

\[
P(\boldsymbol\alpha^*_{lj})
=
\prod_{k=1}^{K_j^*}
g_{jk}^{1-\alpha_{lk}}
(1-s_{jk})^{\alpha_{lk}}.
\]

取对数：

\[
\log P(\boldsymbol\alpha^*_{lj})
=
\sum_k\log g_{jk}
+\sum_k
\alpha_{lk}
\log\frac{1-s_{jk}}{g_{jk}}.
\]

定义

\[
\nu_{j0}=\sum_k\log g_{jk},
\qquad
\nu_{jk}
=
\log\frac{1-s_{jk}}{g_{jk}},
\]

便得到无交互的 log CDM。

## R-RUM

R-RUM 写作

\[
P(\boldsymbol\alpha_l)
=
\pi_j^*
\prod_{k=1}^{K}
(r_{jk}^*)^{q_{jk}(1-\alpha_{lk})}.
\]

将它整理到约化属性模式上，可以和 G-NIDA 建立参数映射。因此论文把 R-RUM 视为 G-NIDA 的另一种参数化，也是 log CDM 的约化形式。

## 三个“加法模型”的实质差异

| 模型 | 加法发生在 | 属性贡献 |
| --- | --- | --- |
| A-CDM | \(P\) | 概率增加固定量 |
| LLM | \(\operatorname{logit}(P)\) | log-odds 增加固定量 |
| G-NIDA/R-RUM | \(\log P\) | 成功概率乘固定倍数 |

它们都有 \(K_j^*+1\) 个参数，但给出的成功概率通常不同。

## 边界问题

LLM 通过 logistic 变换自动给出合法概率。

A-CDM 要检查

\[
0\leq
\delta_{j0}+\sum_k\delta_{jk}\alpha_{lk}
\leq1.
\]

G-NIDA/R-RUM 要检查指数化结果不超过 1。现代软件会在优化时加入概率上下界和单调约束。
