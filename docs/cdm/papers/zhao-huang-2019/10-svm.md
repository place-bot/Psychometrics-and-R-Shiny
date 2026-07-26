# C-SVM 的目标函数与实现歧义

## 1. 决策超平面

对二分类标签

\[
y_j\in\{-1,+1\},
\]

线性 SVM 使用

\[
f(\boldsymbol x_j)
=
\boldsymbol w^\top\boldsymbol x_j+b.
\]

预测为

\[
\widehat y_j
=
\operatorname{sign}
\left(
\boldsymbol w^\top\boldsymbol x_j+b
\right).
\]

## 2. 论文打印的目标函数

原文 Equation (2) 为

\[
\min_{\boldsymbol w,b,\boldsymbol\xi}
\left\{
\frac12\boldsymbol w^\top\boldsymbol w
+
\frac C2\sum_{j=1}^{n}\xi_j^2
\right\}
\]

满足

\[
y_j
\left(
\boldsymbol w^\top\boldsymbol x_j+b
\right)
\ge 1-\xi_j,
\]

\[
\xi_j\ge0.
\]

这是 L2 slack / squared-hinge 风格的软间隔线性 SVM。

## 3. \(C\) 的作用

\[
C\uparrow
\]

会提高违反间隔约束的代价，倾向于更贴合训练数据；

\[
C\downarrow
\]

会强化对 \(\|\boldsymbol w\|_2\) 的相对约束。

论文使用 \(C=1\)，并称其为应用中的常见值。

## 4. 文本分类为何常用线性 SVM

TF--IDF 向量具有：

- 维度高；
- 稀疏；
- 大量局部关键词；
- 类别常可由线性组合区分。

线性 SVM 可直接学习每个词的正负权重，计算成本也低。

## 5. 原文中的实现歧义

作者说“使用 sklearn 默认参数”，但没有写明类名：

- `sklearn.svm.SVC` 在当时通常默认 RBF kernel；
- `sklearn.svm.LinearSVC` 更接近论文打印的线性平方 hinge 目标。

二者的模型、计算复杂度和预测结果有明显差别。

## 6. 本站重构的选择

独立实现使用：

```python
LinearSVC(
    C=1.0,
    loss="squared_hinge",
    random_state=2019
)
```

理由是它和 Equation (2) 的结构最接近。该选择属于重构决策，不能据此断言作者当年的具体调用。

## 7. 论文结果

SVM 在三个特征范围下的最佳 accuracy 为：

| 特征 | 有 IG | 全特征 |
| --- | ---: | ---: |
| unigram | 74.3% | 71.1% |
| unigram+bigram | 74.9% | 71.1% |
| unigram+bigram+trigram | 74.9% | 71.3% |

IG 带来 3.2、3.8、3.6 个百分点的提升。

## 8. 未报告的诊断

论文没有给出：

- \(C\) 的验证曲线；
- 支持向量数量；
- 类别权重；
- 词权重；
- 混淆矩阵；
- 少数类 recall。

因此无法判断 SVM 的 74% accuracy 主要来自哪一类。
