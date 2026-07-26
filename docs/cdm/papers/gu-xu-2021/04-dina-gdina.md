# DINA、G-DINA 与一般 RLCM

## 1. DINA 的理想反应

DINA 采用合取规则：

\[
\Gamma_{j,\boldsymbol\alpha}(Q)
=
I(\boldsymbol\alpha\succeq\boldsymbol q_j).
\]

只有掌握题目要求的全部属性，理想反应才为 1。

令

\[
c_j=1-s_j
\]

为能力潜类的答对概率，\(g_j\) 为非能力潜类的猜对概率，则

\[
\theta_{j,\boldsymbol\alpha}
=
c_j^{\Gamma_{j,\boldsymbol\alpha}}
g_j^{1-\Gamma_{j,\boldsymbol\alpha}},
\qquad c_j>g_j.
\]

所以每题只有两个反应概率。论文主文主要用 \(\boldsymbol s\) 和 \(\boldsymbol g\)，官方模拟代码大量使用 \(\boldsymbol c\) 和 \(\boldsymbol g\)。

## 2. DINA 的结构压缩

一般 \(\Theta\) 有 \(J2^K\) 个位置。DINA 把每一行压缩成：

\[
\theta_{j,\boldsymbol\alpha}
=
\begin{cases}
c_j,&\boldsymbol\alpha\succeq\boldsymbol q_j,\\
g_j,&\boldsymbol\alpha\nsucceq\boldsymbol q_j.
\end{cases}
\]

这种强结构使 Theorem 1 能把严格识别条件降到 A/B/C。

## 3. G-DINA

对题 \(j\)，G-DINA 将所需属性的主效应和交互效应全部纳入：

\[
\theta_{j,\boldsymbol\alpha}
=
\sum_{S\subseteq\{1,\ldots,K\}}
\beta_{j,S}
\prod_{k\in S}q_{jk}\alpha_k.
\]

只有当 \(S\) 中每个属性均被题 \(j\) 要求时，相应 \(\beta_{j,S}\) 才进入模型。

例如 \(\boldsymbol q_j=(1,1,0)\) 时，

\[
\theta_{j,\boldsymbol\alpha}
=
\beta_{j,\varnothing}
+\beta_{j,\{1\}}\alpha_1
+\beta_{j,\{2\}}\alpha_2
+\beta_{j,\{1,2\}}\alpha_1\alpha_2.
\]

## 4. 一般 RLCM

论文把 G-DINA、LCDM、GDM 等归入一般 RLCM。它们允许同一题对不同约化属性模式给出多个概率，参数自由度高于 DINA。

识别要求因模型族发生变化：

| 模型 | 严格联合识别 | 泛联合识别 |
| --- | --- | --- |
| DINA | A+B+C 必要充分 | Theorem 2 给出重要边界；\(K=2\) 完整刻画 |
| DINO | 可由 DINA 对偶性转移 | 相应结论可转移 |
| 一般 RLCM | A+B+C 仍是必要条件 | C 必要；D+E 充分；泛完整必要 |

## 5. 未知 Q 带来的额外困难

已知 \(Q\) 时只需比较

\[
(\Theta,\boldsymbol p)
\quad\text{与}\quad
(\bar\Theta,\bar{\boldsymbol p}).
\]

未知 \(Q\) 时还要比较

\[
(Q,\Theta,\boldsymbol p)
\quad\text{与}\quad
(\bar Q,\bar\Theta,\bar{\boldsymbol p}).
\]

候选模型可以同时改变结构和连续参数，使两个模型的反应分布完全重合。本文所有主定理都围绕排除这种联合替代展开。
