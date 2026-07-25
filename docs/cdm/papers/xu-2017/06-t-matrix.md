# 边际 T 矩阵

## 从 exact pattern 改写为 subset success

完整反应模式概率

\[
P(\boldsymbol R=\boldsymbol r)
\]

要求对每一题同时记录答对或答错。论文改用事件

\[
\boldsymbol R\succeq\boldsymbol r,
\]

即所有满足 \(r_j=1\) 的题都答对，其余题不作要求。

## 定义

\(T(Q,\Theta)\) 是一个

\[
2^J\times 2^K
\]

矩阵。行由题目子集指标
\(\boldsymbol r\in\{0,1\}^J\) 编号，列由属性模式
\(\boldsymbol\alpha\in\{0,1\}^K\) 编号：

\[
t_{\boldsymbol r,\boldsymbol\alpha}(Q,\Theta)
=
P(\boldsymbol R\succeq\boldsymbol r
\mid Q,\Theta,\boldsymbol\alpha).
\]

若 \(\boldsymbol r=\boldsymbol 0\)，事件没有要求：

\[
t_{\boldsymbol 0,\boldsymbol\alpha}=1.
\]

若 \(\boldsymbol r\ne\boldsymbol 0\)，局部独立给出

\[
t_{\boldsymbol r,\boldsymbol\alpha}
=
\prod_{j:r_j=1}
\theta_{j,\boldsymbol\alpha}.
\tag{T}
\]

## 单题行就是 Theta

令 \(\boldsymbol e_j\) 表示第 \(j\) 个位置为 1 的 \(J\) 维单位向量，则

\[
t_{\boldsymbol e_j,\boldsymbol\alpha}
=
P(R_j=1\mid\boldsymbol\alpha)
=
\theta_{j,\boldsymbol\alpha}.
\]

因此

\[
T_{\boldsymbol e_j,\cdot}(Q,\Theta)
=
\Theta_{j,\cdot}.
\]

只要最终证明两套 \(T\)-矩阵的全部单题行相等，就得到 \(\Theta=\bar\Theta\)。

## 行的 Hadamard 乘积

记 \(\odot\) 为逐元素乘积。任意题目子集行都可由单题行构造：

\[
T_{\boldsymbol r,\cdot}(Q,\Theta)
=
\bigodot_{j:r_j=1}
T_{\boldsymbol e_j,\cdot}(Q,\Theta).
\tag{3.3}
\]

这条乘法结构是后面“选一个平移量把某些单元消成零”的基础。

## 乘上属性分布

\[
\begin{aligned}
T_{\boldsymbol r,\cdot}(Q,\Theta)\boldsymbol p
&=
\sum_{\boldsymbol\alpha}
t_{\boldsymbol r,\boldsymbol\alpha}
p_{\boldsymbol\alpha}\\
&=
P(\boldsymbol R\succeq\boldsymbol r
\mid Q,\Theta,\boldsymbol p).
\end{aligned}
\]

所以 \(T(Q,\Theta)\boldsymbol p\) 收集全部题目子集的边际全对概率。

## 为什么它与完整观测分布等价

由 exact pattern 概率可以直接求子集边际：

\[
P(\boldsymbol R\succeq\boldsymbol r)
=
\sum_{\boldsymbol r'\succeq\boldsymbol r}
P(\boldsymbol R=\boldsymbol r').
\]

反向使用 inclusion--exclusion：

\[
P(\boldsymbol R=\boldsymbol r)
=
\sum_{\boldsymbol u\succeq\boldsymbol r}
(-1)^{|\boldsymbol u|-|\boldsymbol r|}
P(\boldsymbol R\succeq\boldsymbol u),
\]

其中求和对与 \(\boldsymbol r\) 的正反应位置相容的超集进行。两种表示是一一映射。

## 命题 1

\((\Theta,\boldsymbol p)\) 可识别，当且仅当对任意不同的
\((\bar\Theta,\bar{\boldsymbol p})\)，至少存在一个
\(\boldsymbol r\) 使

\[
T_{\boldsymbol r,\cdot}(Q,\Theta)\boldsymbol p
\ne
T_{\boldsymbol r,\cdot}(Q,\bar\Theta)\bar{\boldsymbol p}.
\tag{3.4}
\]

因此主证明只需建立

\[
T(Q,\Theta)\boldsymbol p
=
T(Q,\bar\Theta)\bar{\boldsymbol p}
\Longrightarrow
\Theta=\bar\Theta,\quad
\boldsymbol p=\bar{\boldsymbol p}.
\tag{3.5}
\]

## 两题小例子

若 \(J=2\)，行顺序取
\(\boldsymbol 0,\boldsymbol e_1,\boldsymbol e_2,\boldsymbol e_1+\boldsymbol e_2\)，则某一属性列为

\[
T_{\cdot,\boldsymbol\alpha}
=
\begin{pmatrix}
1\\
\theta_{1,\boldsymbol\alpha}\\
\theta_{2,\boldsymbol\alpha}\\
\theta_{1,\boldsymbol\alpha}\theta_{2,\boldsymbol\alpha}
\end{pmatrix}.
\]

最后一行是两题同时答对的条件概率。这个“常数、一次项、乘积项”结构使 \(T\)-矩阵具备可利用的多项式代数。
