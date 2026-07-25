# 约化属性模式与偏序

## 完整属性模式

设测验共有 \(K\) 个属性，完整属性模式为

\[
\boldsymbol\alpha_l
=
(\alpha_{l1},\ldots,\alpha_{lK})^\top,
\qquad
\alpha_{lk}\in\{0,1\}.
\]

索引 \(l\) 指向 \(2^K\) 个潜在类别中的一个。这里的模式是潜在类别层对象，不带学生索引。

## 项目只读取 Q 行中的属性

Q 矩阵元素

\[
q_{jk}=
\begin{cases}
1,&\text{项目 }j\text{ 需要属性 }k,\\
0,&\text{项目 }j\text{ 不需要属性 }k.
\end{cases}
\]

项目 \(j\) 所需属性数为

\[
K_j^*=\sum_{k=1}^{K}q_{jk}.
\]

从完整模式中取出 \(q_{jk}=1\) 的分量，形成约化属性模式

\[
\boldsymbol\alpha^*_{lj}.
\]

例如，

\[
\boldsymbol q_j=(1,0,1,0),
\qquad
\boldsymbol\alpha_l=(1,1,0,1)
\]

给出

\[
\boldsymbol\alpha^*_{lj}=(1,0).
\]

第二和第四个属性不会影响该项目的反应概率。

## 从 \(2^K\) 类压到 \(2^{K_j^*}\) 组

若 \(K=5\)，但项目只需要属性 1 和 4，则 32 个完整类别对该项目只形成四个组：

\[
(0,0),(1,0),(0,1),(1,1).
\]

这一步称为 latent-class-to-latent-group 映射。它同时解释了两个计算事实：

- E 步仍需在完整属性空间上计算后验；
- M 步更新某个项目时，只需汇总到该项目的约化组。

## 属性模式的偏序

论文定义

\[
\boldsymbol\alpha^*_{lj}
\preceq
\boldsymbol\alpha^*_{l'j}
\]

当且仅当每个分量都满足

\[
\alpha_{lk}\leq\alpha_{l'k}.
\]

若至少一个分量严格小于，则写作

\[
\boldsymbol\alpha^*_{lj}
\prec
\boldsymbol\alpha^*_{l'j}.
\]

这个关系表示后者包含前者掌握的全部属性，并至少多掌握一个属性。

## “1 的个数更多”不能替代偏序

比较

\[
(0,0,1)
\quad\text{和}\quad
(1,1,0).
\]

第二个模式包含两个 1，第一个包含一个 1，但二者不可比较：

\[
(0,0,1)\npreceq(1,1,0),
\]

因为第三个属性从 1 变成了 0。

因此，单纯按照掌握属性数量排序会丢失“掌握了哪些属性”的信息。

## 单调约束

饱和 G-DINA 在最一般形式下允许

\[
P(\boldsymbol\alpha^*_{lj})
>
P(\boldsymbol\alpha^*_{l'j})
\quad
\text{即使 }
\boldsymbol\alpha^*_{lj}\prec\boldsymbol\alpha^*_{l'j}.
\]

论文解释了一种可能情形：掌握部分属性者可能稳定选择某个强干扰项，而完全未掌握者随机猜测，后者反而有更高成功率。

许多教育应用仍会施加单调性：

\[
P(\boldsymbol\alpha^*_{lj})
\leq
P(\boldsymbol\alpha^*_{l'j})
\quad
\text{whenever }
\boldsymbol\alpha^*_{lj}\prec\boldsymbol\alpha^*_{l'j}.
\]

单调性属于额外的实质假设，不能从 G-DINA 形式自动推出。
