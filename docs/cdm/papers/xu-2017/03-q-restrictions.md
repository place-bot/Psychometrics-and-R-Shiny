# Q 矩阵限制与单调性

## Q 矩阵

\[
Q=(q_{jk})_{J\times K},
\qquad q_{jk}\in\{0,1\}.
\]

第 \(j\) 行

\[
\boldsymbol q_j=(q_{j1},\ldots,q_{jK})
\]

给出该题所需属性。若 \(q_{jk}=1\)，第 \(j\) 题与属性 \(k\) 相连。

对二分向量使用逐分量偏序：

\[
\boldsymbol\alpha\succeq\boldsymbol q_j
\iff
\alpha_k\ge q_{jk}\quad\forall k.
\]

此时 \(\boldsymbol\alpha\) 具备该题要求的全部属性。若至少一个所需属性缺失，记为

\[
\boldsymbol\alpha\nsucceq\boldsymbol q_j.
\]

## 限制式 (2.2)

论文要求

\[
\max_{\boldsymbol\alpha:\,
\boldsymbol\alpha\succeq\boldsymbol q_j}
\theta_{j,\boldsymbol\alpha}
=
\min_{\boldsymbol\alpha:\,
\boldsymbol\alpha\succeq\boldsymbol q_j}
\theta_{j,\boldsymbol\alpha}
\ge
\theta_{j,\boldsymbol\alpha'}
\ge
\theta_{j,\boldsymbol 0}.
\tag{2.2}
\]

逐项解释：

1. 具备全部所需属性的潜在类具有相同的成功概率；
2. 这个共同概率不低于任意能力不足类的概率；
3. 零属性类的成功概率最低。

第一部分是等值限制，后两部分是次序限制。若某道题只要求属性 1，\((1,0)\) 和 \((1,1)\) 在该题上的成功概率相等。

## 限制式 (2.3)

当某题只测第 \(k\) 个属性，即

\[
\boldsymbol q_j=\boldsymbol e_k,
\]

论文另外要求

\[
\theta_{j,\boldsymbol 1}
>
\max_{\boldsymbol\alpha:\,
\boldsymbol\alpha\nsucceq\boldsymbol e_k}
\theta_{j,\boldsymbol\alpha}.
\tag{2.3}
\]

由于式 (2.2) 使所有掌握属性 \(k\) 的人共享最高概率，式 (2.3) 给出严格分离：

\[
\theta_{j,\alpha_k=1}
>
\theta_{j,\alpha_k=0}.
\]

证明中的非零乘积依赖这个严格不等式。

## 原文的算术例子

两项属性是“加法”和“乘法”，三道题为

\[
Q=
\begin{array}{c|cc}
&\text{加法}&\text{乘法}\\\hline
2+1&1&0\\
3\times2&0&1\\
(2+1)\times2&1&1
\end{array}.
\]

对第一题：

\[
\theta_{1,(1,0)}
=
\theta_{1,(1,1)}
>
\theta_{1,(0,0)},\theta_{1,(0,1)}.
\]

第二个属性不会改变第一题对“掌握加法者”的最高成功概率。

## 这些限制影响参数维数

无约束模型每题有 \(2^K\) 个类别概率。Q 限制把若干单元合并。以 \(K=2\)、\(\boldsymbol q_j=(1,0)\) 为例：

\[
\theta_{j,10}=\theta_{j,11},
\qquad
\theta_{j,10}>\theta_{j,00},
\qquad
\theta_{j,10}>\theta_{j,01}.
\]

受约束空间相对于无约束空间维数更低。这正是通用 generic identifiability 结果不能直接移植的原因。

## 一项细节

式 (2.2) 只保证全部所需属性组达到共同最高概率，并允许不同能力不足类拥有不同概率。DINA 把所有能力不足类进一步压成一个猜测概率；G-DINA、LLM 和 reduced RUM 可以保留更细的差异。Xu 的定理覆盖的是这个更宽的模型族。
