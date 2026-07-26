# 经验矩 \(\boldsymbol\alpha\) 与总体映射

## 每个 T 行都有一个观测对应量

若 \(T(Q)\) 的某行对应

\[
I_{i_1}\wedge\cdots\wedge I_{i_\ell},
\]

则记录样本中这些题全部答对的人数：

\[
N_{I_{i_1}\wedge\cdots\wedge I_{i_\ell}}
=
\sum_{r=1}^N
\prod_{h=1}^{\ell}
\mathbf 1(R_r^{i_h}=1).
\]

原文用指示函数的集合写法表达同一事件。乘积写法更直接地显示“全部为 1”。

对应的经验联合答对率为

\[
\alpha_{i_1,\ldots,i_\ell}
=
\frac{
N_{I_{i_1}\wedge\cdots\wedge I_{i_\ell}}
}{N}.
\]

把所有选定题组的比例按照 \(T(Q)\) 的行顺序堆叠，得到

\[
\boldsymbol\alpha.
\]

## \(\boldsymbol\alpha\) 完全可观测

\(\boldsymbol\alpha\) 只需要二元反应矩阵。它不需要知道：

- 学生属于哪个属性模式；
- 属性模式比例；
- 真 Q；
- 单个学生的属性分类。

因此它适合作为候选 Q 共同面对的观测目标。

## 无噪声下的恒等式

样本中非零属性模式的比例写作

\[
\widehat{\boldsymbol p}
=
(\widehat p_{\boldsymbol A}:
\boldsymbol A\in\{0,1\}^k\setminus\{\boldsymbol0\}).
\]

在 \(R^i=\xi^i\) 下，

\[
T(Q)\widehat{\boldsymbol p}
=
\boldsymbol\alpha.
\tag{2.5}
\]

这条式子可以逐行证明。取任意题组 \(S=\{i_1,\ldots,i_\ell\}\)，左侧对应分量为

\[
\sum_{\boldsymbol A\ne\boldsymbol0}
B_Q(I_{i_1}\wedge\cdots\wedge I_{i_\ell})_{\boldsymbol A}
\widehat p_{\boldsymbol A}.
\]

B-vector 对能够完成整组题的模式取 1，对其余模式取 0，因此求和恰好等于样本中能够完成该题组的人数比例。无噪声下“能够完成”与“实际全部答对”相同，所以等于对应的 \(\alpha\)。

## 总体版本

由大数定律，

\[
\widehat{\boldsymbol p}
\overset{\text{a.s.}}{\longrightarrow}
\boldsymbol p^*,
\]

从而

\[
\boldsymbol\alpha
=T(Q)\widehat{\boldsymbol p}
\overset{\text{a.s.}}{\longrightarrow}
T(Q)\boldsymbol p^*.
\]

这里

\[
\boldsymbol\mu_Q
=T(Q)\boldsymbol p^*
\]

是 Q 和总体属性分布共同决定的总体矩向量。

## 为什么用全部联合答对率

对 \(m\) 道二元题，完整反应分布有 \(2^m-1\) 个自由概率。所有非空题组的联合正响应概率

\[
\Pr(R^{i_1}=\cdots=R^{i_\ell}=1)
\]

也有 \(2^m-1\) 个，并能通过容斥关系还原完整反应分布。因此饱和 \(\boldsymbol\alpha\) 没有主动丢弃反应分布的信息。

## 一个四人样本

假设两道题的反应是

\[
\begin{array}{c|cc}
\text{学生}&R^1&R^2\\\hline
1&1&1\\
2&1&0\\
3&0&1\\
4&0&0
\end{array}
\]

则

\[
\alpha_1=\frac24,\qquad
\alpha_2=\frac24,\qquad
\alpha_{1,2}=\frac14.
\]

若只看边际，会看到两个正确率都为 \(1/2\)。联合矩再告诉我们两题同时答对的比例为 \(1/4\)，由此增加了对潜在结构的约束。

## 从恒等式到估计

真 Q 允许某个概率向量精确解释无噪声样本矩。对错误候选 \(Q'\)，同样的解释一般无法成立。下一页把这种无法解释的程度定义成距离。

[下一页：目标函数、Q 估计量与计算](05-objective-and-estimator.md)
