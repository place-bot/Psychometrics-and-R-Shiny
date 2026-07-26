# Gaussian Naive Bayes

## 1. Bayes 分类

对类别 \(c\in\{O,M\}\)：

\[
p(c\mid\boldsymbol x)
=
\frac{p(c)p(\boldsymbol x\mid c)}
{p(\boldsymbol x)}.
\]

预测时 \(p(\boldsymbol x)\) 对所有类别相同，所以

\[
\widehat c
=
\arg\max_c
p(c)p(\boldsymbol x\mid c).
\]

## 2. 条件独立假设

Naive Bayes 假定给定类别后各特征条件独立：

\[
p(\boldsymbol x\mid c)
=
\prod_{r=1}^{k}
p(x_r\mid c).
\]

于是

\[
\widehat c
=
\arg\max_c
p(c)
\prod_{r=1}^{k}
p(x_r\mid c).
\]

实际计算通常取对数：

\[
\widehat c
=
\arg\max_c
\left[
\log p(c)
+\sum_{r=1}^{k}\log p(x_r\mid c)
\right].
\]

## 3. Gaussian 假设

论文明确使用 Gaussian NB：

\[
x_r\mid c
\sim
\mathcal N(\mu_{cr},\sigma_{cr}^2).
\]

密度为

\[
p(x_r\mid c)
=
\frac{1}
{\sqrt{2\pi\sigma_{cr}^2}}
\exp
\left[
-\frac{(x_r-\mu_{cr})^2}
{2\sigma_{cr}^2}
\right].
\]

## 4. 为什么 Gaussian NB 用于 TF--IDF 有争议

TF--IDF 维度通常：

- 非负；
- 大量精确为 0；
- 分布高度偏斜；
- 很难呈正态。

文本任务更常见的选择是 Multinomial NB 或 Complement NB。论文没有比较这些变体。

## 5. 为何特征选择影响巨大

unigram 的 NB 结果：

\[
21.3\%
\longrightarrow
84.0\%
\]

accuracy 提升 62.7 个百分点。

可能机制为：

1. 2,943 个特征中大部分极低频；
2. Gaussian NB 为每个“类别×特征”估计均值与方差；
3. 弱特征的似然贡献不断累加；
4. top-\(k\) 把维度压到最多 300；
5. 高信息词的类别信号占据主导。

## 6. 三个最佳结果

| 特征 | 有 IG accuracy | 有 IG F1 |
| --- | ---: | ---: |
| unigram | 84.0% | 84.7% |
| unigram+bigram | 84.6% | 85.2% |
| unigram+bigram+trigram | **85.2%** | **85.6%** |

## 7. 类别先验

若直接按频率估计：

\[
\widehat p(O)\approx0.827,
\qquad
\widehat p(M)\approx0.173.
\]

先验本身强烈偏向 O。高质量结论需要同时检查 M 类 precision 与 recall，论文只报告加权总指标。

## 8. 可复现性缺口

Gaussian NB 仍有未报告设置：

- `priors`；
- `var_smoothing`；
- 输入是否转成 dense array；
- TF--IDF 的归一化；
- \(k\) 的最终选择值。

这些设置影响小样本少数类表现。
