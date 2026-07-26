# Experiment：accuracy 与 weighted F1

## 1. 二分类混淆表

| 真实\预测 | O | M |
| --- | ---: | ---: |
| O | \(TP_O\) | \(FN_O=FP_M\) |
| M | \(FP_O=FN_M\) | \(TP_M\) |

总题数为

\[
N=TP_O+FN_O+FP_O+TP_M.
\]

## 2. Accuracy

\[
\operatorname{Accuracy}
=
\frac{TP_O+TP_M}{N}.
\]

它易于解释，但在类别不平衡时可能被多数类主导。

## 3. 每类 precision 与 recall

\[
\operatorname{Precision}_O
=
\frac{TP_O}{TP_O+FP_O},
\]

\[
\operatorname{Recall}_O
=
\frac{TP_O}{TP_O+FN_O}.
\]

M 类同理。

## 4. 每类 F1

\[
F1_c
=
\frac{
2\operatorname{Precision}_c\operatorname{Recall}_c
}{
\operatorname{Precision}_c+\operatorname{Recall}_c
}.
\]

等价形式为

\[
F1_c
=
\frac{2TP_c}
{2TP_c+FP_c+FN_c}.
\]

## 5. scikit-learn 的 weighted F1

真实支持度为

\[
t_O=TP_O+FN_O,
\qquad
t_M=TP_M+FN_M.
\]

标准 support-weighted F1 为

\[
F1_{\mathrm{weighted}}
=
\frac{t_O}{N}F1_O
+
\frac{t_M}{N}F1_M.
\]

## 6. 为什么还应报告 macro-F1

\[
F1_{\mathrm{macro}}
=
\frac{F1_O+F1_M}{2}.
\]

它给两个类别相同权重，更容易暴露 M 类识别不足。

## 7. 论文报告的指标组合

论文的判断规则是 accuracy 和 weighted F1 同时较高。这个组合比只给 accuracy 更完整，但仍缺：

- M 类 recall；
- macro-F1；
- balanced accuracy；
- 混淆矩阵；
- 置信区间。

## 8. balanced accuracy

\[
\operatorname{BalancedAccuracy}
=
\frac12
\left(
\operatorname{Recall}_O
+
\operatorname{Recall}_M
\right).
\]

它适合本研究的 82.7%/17.3% 不平衡结构。

## 9. Q 行层面的后续指标

若推广到 multi-label Q，应加入：

\[
\operatorname{HammingLoss}
=
\frac{1}{JK}
\sum_{j,k}
\mathbb I
\left(
\widehat q_{jk}\ne q_{jk}
\right),
\]

以及 row exact match。二分类 accuracy 无法替代这些指标。
