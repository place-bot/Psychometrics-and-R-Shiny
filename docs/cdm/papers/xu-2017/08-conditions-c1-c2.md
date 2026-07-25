# C1、C2 与三套单位阵

## 条件 C1

题目换序后，

\[
Q=
\begin{pmatrix}
I_K\\
I_K\\
Q'
\end{pmatrix}.
\tag{C1}
\]

前 \(K\) 题和第 \(K+1\) 到 \(2K\) 题分别形成一个完整单位块。C1 保证每个属性至少由两道单属性题测量。

## 条件 C2

对每个 \(k=1,\ldots,K\)，要求剩余题目上的两个概率向量不同：

\[
\left(
\theta_{j,\boldsymbol e_k}:j>2K
\right)^\top
\ne
\left(
\theta_{j,\boldsymbol 0}:j>2K
\right)^\top.
\tag{C2}
\]

等价说法：对每个属性 \(k\)，至少有一道 \(Q'\) 中的题满足

\[
\theta_{j,\boldsymbol e_k}
\ne
\theta_{j,\boldsymbol 0}.
\]

C2 是关于实际反应概率的条件，不单由一般 Q 结构完全决定。

## C2 在证明里的精确作用

定义两条向量

\[
\boldsymbol a_k
=
\left(
1,\theta_{2K+1,\boldsymbol e_k},
\ldots,\theta_{J,\boldsymbol e_k}
\right)^\top,
\]

\[
\boldsymbol a_0
=
\left(
1,\theta_{2K+1,\boldsymbol 0},
\ldots,\theta_{J,\boldsymbol 0}
\right)^\top.
\]

两者第一个元素都为 1。C2 说明 \(\boldsymbol a_k\ne\boldsymbol a_0\)，所以它们不可能成比例。线性代数保证存在行向量 \(\boldsymbol u_k\) 使

\[
\boldsymbol u_k\boldsymbol a_0=0,
\qquad
\boldsymbol u_k\boldsymbol a_k=b_k\ne0.
\]

这个 \(\boldsymbol u_k\) 在证明步骤 3 中消去零属性列并保留单属性列，从而识别两个单位块里的项目参数。

## 一个容易执行的更强条件

若所有剩余题都满足零属性类严格最低：

\[
\theta_{j,\boldsymbol 0}
<
\min_{\boldsymbol\alpha\ne\boldsymbol 0}
\theta_{j,\boldsymbol\alpha},
\qquad j>2K,
\]

只要 \(Q'\) 非空，C2 自动成立。

这比 C2 强，因为 C2 只要求每个 \(\boldsymbol e_k\) 在至少一道剩余题上与 \(\boldsymbol 0\) 不同。

## 三套单位块

若

\[
Q=
\begin{pmatrix}
I_K\\
I_K\\
I_K\\
\widetilde Q
\end{pmatrix},
\]

则第三个 \(I_K\) 位于 \(Q'\)。对于其第 \(k\) 道单属性题，式 (2.3) 给出

\[
\theta_{j,\boldsymbol e_k}
>
\theta_{j,\boldsymbol 0}.
\]

因此 C1 与 C2 都满足。这形成一个仅凭 Q 结构即可执行的充分设计：

> 每个属性至少配置三道只测该属性的题。

## 三个常见误读

### C1、C2 是充分条件

主定理证明满足它们就可识别。一般 RLCM 中有些不满足该结构的设计也可能可识别，论文没有给出完整的必要充分刻画。

### C2 不等于“每列至少三个 1”

一般模型里，某题的 Q 行含属性 \(k\) 并不自动保证
\(\theta_{j,\boldsymbol e_k}\ne\theta_{j,\boldsymbol 0}\)。若该题还要求其他属性，\(\boldsymbol e_k\) 可能仍是能力不足类；两个概率是否不同取决于模型。

### J ≥ 2K + 1 只是数量下界

C1、C2 蕴含 \(Q'\) 非空，从而

\[
J\ge2K+1.
\]

题目数达到这个下界不代表行结构和概率区分条件已经满足。

## 设计检查表

1. Q 中能否找到第一个 \(I_K\)？
2. 删除后能否再找到一个 \(I_K\)？
3. 对每个 \(k\)，\(Q'\) 是否有题能够区分 \(\boldsymbol e_k\) 与 \(\boldsymbol 0\)？
4. 若希望只做结构审查，能否直接加入第三个 \(I_K\)？
5. 属性层级是否使某些 \(\boldsymbol e_k\) 根本不在允许的潜在类空间中？

第 5 项超出原定理的正比例模型，需要使用后续的层级或 partial-identifiability 理论。
