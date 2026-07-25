# 一致性评论、回应与方法定位

## 后续文献

2017 年 *Psychometrika* 同一期刊登：

1. Jingchen Liu, *On the Consistency of Q-Matrix Estimation: A Commentary*；
2. de la Torre & Chiu, *On the Consistency of Q-Matrix Estimation: A Rejoinder*。

这组讨论把原论文中较隐含的估计问题拆成三部分。

## 问题 1：总体定理依赖 \(w\) 吗

Liu 用全方差公式重写 GDI：

\[
\varsigma^2(\boldsymbol q)
=
\operatorname{Var}_w
\{E(Y\mid\boldsymbol\alpha_{\boldsymbol q})\}.
\]

单调关系

\[
\varsigma^2(\boldsymbol q)
\le
\varsigma^2(\boldsymbol1)
\]

对任意概率分布 \(w\) 成立。因此定理的方差排序对 \(w\) 的具体形式相当稳健。

严格不等号还要求：被遗漏的真实属性无法由候选保留的属性完全预测，并且它确实改变成功概率。

## 问题 2：样本中的 \(\widehat p\) 依赖初始 Q

\[
\widehat p(\boldsymbol\alpha)
=
\frac{\sum_iw_i(\boldsymbol\alpha)Y_i}
{\sum_iw_i(\boldsymbol\alpha)}.
\]

其中 \(w_i\) 由 provisional \(Q_0\) 拟合产生。若 \(Q_0\) 的误设严重扭曲学生后验，\(\widehat p\) 会有不可忽略偏差。总体定理不能自动消除该偏差。

Liu 因此建议：

- 只在有理由相信初始测量足够准确时使用单次算法；
- 研究迭代更新 \(Q_0\to Q_1\to Q_2\to\cdots\)；
- 刻画错误平衡点和真实 Q 的吸引域。

## 作者回应：少量误设的实践鲁棒性

de la Torre 与 Chiu 认为，在少量到中等 Q 错误下，正确题目的联合似然仍能较好恢复学生后验。模拟中的约 5% entry 误设支持这种有限条件下的鲁棒性。

他们同时承认，某些特殊误设组合可能造成更大后验扭曲。这是一条经验适用条件，没有形成一般保证。

## 问题 3：固定 \(\varepsilon<1\) 的相合性

若一个真实属性效应很弱，某个漏设候选可能满足：

\[
\varsigma^2(\boldsymbol q)
>
\varepsilon\varsigma^2(\boldsymbol1)
\]

即使样本量趋于无穷也会通过固定阈值。Liu 提议让

\[
\varepsilon_n\to1,
\]

并给出例子：

\[
\varepsilon_n
=
1-(\log n)^{-1}.
\]

其趋近 1 的速度慢于常见 \(n^{-1/2}\) 估计误差，可在一定条件下兼顾估计噪声和真实微小差异。

## 作者对动态阈值的回应

当

\[
n=200\sim2000,
\]

该公式给出约

\[
\varepsilon_n=.81\sim.87,
\]

明显低于原模拟中表现较好的 .95。达到 .95 需要约 \(5\times10^8\) 的样本量。

作者由此指出：

- 渐近构造未必给常见样本量带来理想有限样本表现；
- 固定 .95 也没有跨情境的普适理论；
- 阈值仍需要实际条件下的研究。

## 迭代也可能停在错误平衡点

即使每轮以建议 Q 重拟合：

\[
Q^{(t+1)}=\mathcal A(Q^{(t)}),
\]

仍可能存在

\[
Q'\ne Q^*,
\qquad
\mathcal A(Q')=Q'.
\]

这解释了当前 `GDINA` 代码为何检测循环，并记录不收敛类型。迭代可以降低初始 Q 依赖，但无法单独建立相合性。

## 两类目标

| 目标 | 关注点 | 合适证据 |
| --- | --- | --- |
| 有限样本 Q 验证工具 | 在常见 \(N,J,K\) 下保留正确行、纠正错误行 | 模拟、重抽样、内容审核、外部效度 |
| 渐近相合 Q 估计量 | \(P(\widehat Q=Q^*)\to1\) | 可识别性、阈值序列、初值条件、统一收敛证明 |

2016 年论文对第一类目标提供了较强方法与实验；第二类目标由评论提出，尚需额外理论。

## 对应用者的直接建议

1. 报告初始 Q 的来源和预期错误比例；
2. 检查多组 \(\varepsilon\) 和 mesa path；
3. 使用 bootstrap 观察建议频率；
4. 比较单次与迭代结果；
5. 对弱效应属性保留不确定性；
6. 将建议 Q 与内容专家 Q 并列呈现；
7. 用重新拟合后的整体和逐题拟合做补充证据。
