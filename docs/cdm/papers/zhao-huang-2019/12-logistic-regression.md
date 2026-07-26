# L2 Logistic Regression

## 1. 概率模型

对二元 \(Y\)，令

\[
p_j
=
\Pr(Y_j=1\mid\boldsymbol x_j).
\]

logit 模型为

\[
\log
\frac{p_j}{1-p_j}
=
\alpha+\boldsymbol\beta^\top\boldsymbol x_j.
\]

因此

\[
p_j
=
\sigma
\left(
\alpha+\boldsymbol\beta^\top\boldsymbol x_j
\right),
\]

其中

\[
\sigma(z)=\frac{1}{1+e^{-z}}.
\]

## 2. 对数似然

\[
\ell(\alpha,\boldsymbol\beta)
=
\sum_{j=1}^{n}
\left[
y_j\log p_j
+(1-y_j)\log(1-p_j)
\right].
\]

论文 Equation (7) 写成

\[
\ell(\alpha,\boldsymbol\beta)
=
\sum_{j=1}^{n}
\log p(y_j\mid\boldsymbol x_j,\alpha,\boldsymbol\beta).
\]

## 3. L2 正则

论文使用

\[
\ell'(\alpha,\boldsymbol\beta)
=
\ell(\alpha,\boldsymbol\beta)
-
\frac{\lambda}{2}
\left(
\alpha^2+\sum_{r=1}^{m}\beta_r^2
\right).
\]

最大化 \(\ell'\) 等价于最小化负对数似然加 L2 惩罚。

## 4. 特征系数的解释

若把 \(Y=1\) 定义为 M，则：

\[
\beta_r>0
\]

表示特征 \(r\) 提高 M 类的 log-odds；

\[
\beta_r<0
\]

表示特征 \(r\) 更支持 O 类。

LR 可以提供可解释的关键词方向，但论文没有报告系数。

## 5. 论文结果

| 特征 | 有 IG accuracy | 全特征 accuracy |
| --- | ---: | ---: |
| unigram | 74.1% | 72.5% |
| unigram+bigram | 74.6% | 72.7% |
| unigram+bigram+trigram | **75.3%** | 72.5% |

相应 accuracy 提升为 1.6、1.9、2.8 个百分点。

## 6. 与 NB 的差异

LR 直接优化条件概率：

\[
p(Y\mid X).
\]

NB 建模：

\[
p(X\mid Y)p(Y).
\]

小样本时，NB 的强结构假设有时能降低估计方差；数据增大后，LR 的判别式学习可能更灵活。本文只有 805 道题，结果与这一经典比较相符。

## 7. “默认参数”仍不充分

scikit-learn 的默认值会随版本变化。至少需要：

- sklearn 版本；
- `solver`；
- `C`；
- `class_weight`；
- `max_iter`；
- intercept 是否惩罚；
- 收敛状态。

论文只说明 L2 正则和默认参数。

## 8. 本站重构

为靠近 2019 年常见设置，独立代码显式使用：

```python
LogisticRegression(
    C=1.0,
    penalty="l2",
    solver="liblinear",
    max_iter=5000,
    random_state=2019
)
```

这是一套透明、可重复的选择。
