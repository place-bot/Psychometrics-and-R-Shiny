# Equation (9) 的 weighted F1 审计

## 1. 原文变量

论文定义：

- \(p_O\)：预测为 O 的题数；
- \(tp_O\)：其中真实为 O 的题数；
- \(fp_O\)：其中真实为 M 的题数；
- \(t_O\)：真实 O 题总数。

M 类同理。

所以

\[
p_O=tp_O+fp_O.
\]

## 2. 原文打印公式

Equation (9) 为

\[
F1
=
\frac{tp_O+fp_O}{t_O+t_M}F1_O
+
\frac{tp_M+fp_M}{t_O+t_M}F1_M.
\]

代入 \(p_c\)：

\[
F1_{\text{Eq.9}}
=
\frac{p_O}{N}F1_O
+
\frac{p_M}{N}F1_M.
\]

它按**预测类别规模**加权。

## 3. scikit-learn 的定义

`f1_score(..., average="weighted")` 使用真实支持度：

\[
F1_{\text{sklearn}}
=
\frac{t_O}{N}F1_O
+
\frac{t_M}{N}F1_M.
\]

两式只有在

\[
p_O=t_O,
\qquad
p_M=t_M
\]

时相等。

## 4. 用相容混淆矩阵核验

考虑：

| 真实\预测 | O | M |
| --- | ---: | ---: |
| O | 60 | 7 |
| M | 5 | 9 |

得到：

\[
t_O=67,\quad t_M=14,
\]

\[
p_O=65,\quad p_M=16.
\]

标准 weighted F1 为

\[
85.57\%\approx85.6\%.
\]

Equation (9) 给出

\[
84.80\%.
\]

表中 85.6% 与标准定义相容，与打印公式不相容。

## 5. all-O 反例

若所有题都预测为 O：

\[
p_O=N,\qquad p_M=0.
\]

Equation (9) 退化为

\[
F1_{\text{Eq.9}}=F1_O=90.55\%.
\]

这会让恒预测多数类的 F1 高于论文最佳 85.6%，显然偏离 weighted F1 用来综合两类表现的常见目的。

标准加权结果为：

\[
F1_{\text{sklearn}}=74.92\%.
\]

## 6. 最可能的解释

论文说明实验用 sklearn 完成。结合 85.6% 与相容混淆矩阵，较合理的推断是：

1. 实际计算采用 sklearn 的 support-weighted F1；
2. Equation (9) 把权重中的真实支持度误写成预测数量。

这是基于数值一致性的推断，源码和预测文件均未公开。

## 7. 引用结果时的处理

可以引用表中 85.6%，同时注明：

> 论文打印的 Equation (9) 与 scikit-learn weighted F1 定义不一致；表格数值更接近后者。

## 8. 本站代码

[`zhao_huang_2019_audit.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_audit.py) 同时实现两种定义，并输出相容混淆矩阵。
