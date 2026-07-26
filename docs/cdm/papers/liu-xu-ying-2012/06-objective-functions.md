# 目标函数与三种估计量

## 参数已知

\[
S_{\boldsymbol c,\boldsymbol g,\boldsymbol p}(Q)
=
\left\|
T_{\boldsymbol c,\boldsymbol g}(Q)\boldsymbol p
-\boldsymbol\beta
\right\|_2.
\tag{14}
\]

原文用 Euclidean distance。参数和 Q 正确时，

\[
S_{\boldsymbol c,\boldsymbol g,\boldsymbol p}(Q)\to0.
\]

自然估计量为

\[
\widehat Q
=
\arg\inf_{Q'}S_{\boldsymbol c,\boldsymbol g,\boldsymbol p}(Q').
\]

## 参数未知：联合剖面

\[
S(Q')
=
\inf_{\boldsymbol c,\boldsymbol g,\boldsymbol p}
S_{\boldsymbol c,\boldsymbol g,\boldsymbol p}(Q'),
\tag{15}
\]

约束为

\[
c_j,g_j,p_{\boldsymbol\alpha}\in[0,1],
\qquad
\sum_{\boldsymbol\alpha}p_{\boldsymbol\alpha}=1.
\]

然后

\[
\widehat Q=\arg\inf_{Q'}S(Q').
\tag{16}
\]

固定 \((Q',\boldsymbol c,\boldsymbol g)\) 时，对 \(\boldsymbol p\) 的优化是带单纯形约束的二次规划。对 \(\boldsymbol c,\boldsymbol g\) 联合优化更复杂。

## 参数未知：MLE 插入

对每个候选 \(Q'\)，先用 DINA 边际似然得到

\[
\widehat{\boldsymbol c}(Q'),
\quad
\widehat{\boldsymbol g}(Q'),
\quad
\widehat{\boldsymbol p}(Q').
\]

再定义

\[
\widehat S(Q')
=
S_{
\widehat{\boldsymbol c}(Q'),
\widehat{\boldsymbol g}(Q'),
\widehat{\boldsymbol p}(Q')
}(Q').
\tag{17}
\]

最终

\[
\widetilde Q
=
\arg\inf_{Q'}\widehat S(Q').
\tag{18}
\]

Algorithm 1 的计算段明确采用式 (17)--(18) 的路线。

## 似然与 S 的分工

| 对象 | 用途 |
| --- | --- |
| DINA marginal likelihood | 固定候选 Q 后估计 \(\widehat c,\widehat g,\widehat p\) |
| \(\widehat S(Q)\) | 比较候选 Q 对所选联合矩的匹配程度 |

这意味着每评价一个新 Q，都要重新拟合 nuisance parameters。若仅把同一组 \((\widehat c,\widehat g,\widehat p)\) 固定后比较所有候选，得到的是另一种近似算法。

## 为什么写 \(\inf\)

Q 的空间是有限离散集合，合适条件下可以写 \(\min\)。原文保持 \(\inf\) 记号，以便同时表达连续参数的剖面优化。

## 一个重要风险

错误 Q 也可能通过重新调整 \(c,g,p\) 获得很小的 \(S\)。可识别性讨论要回答的核心问题正是：不同 Q 是否可能生成相同的可观测分布或相同的一组矩。
