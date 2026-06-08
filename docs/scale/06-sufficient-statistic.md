# 6. 概念补充12：充分统计量的完整推导

充分统计量是Rasch模型的另一个重要特性，让我们完整推导这个概念。

## 6.1 充分统计量的定义

充分统计量的严格定义

统计量\(T(\mathbf{X})\)是参数\(\theta\)的充分统计量，当且仅当：

\(P(\mathbf{X} = \mathbf{x} | T(\mathbf{X}) = t, \theta) = P(\mathbf{X} = \mathbf{x} | T(\mathbf{X}) = t)\)

即给定统计量\(T\)的值后，数据的分布不再依赖于参数\(\theta\)。

## 6.2 Rasch模型中的充分统计量推导

**Rasch模型的概率质量函数：**

\(P(\mathbf{X} = \mathbf{x} | \theta) = \prod_{i=1}^{I} \frac{\exp[x_i(\theta - \beta_i)]}{1 + \exp(\theta - \beta_i)}\)

**重新整理：**

\(P(\mathbf{X} = \mathbf{x} | \theta) = \frac{\exp[\theta \sum_{i=1}^{I} x_i] \prod_{i=1}^{I} \exp(-x_i \beta_i)}{\prod_{i=1}^{I} [1 + \exp(\theta - \beta_i)]}\)

\(= \frac{\exp[\theta \sum_{i=1}^{I} x_i]}{\prod_{i=1}^{I} [1 + \exp(\theta - \beta_i)]} \prod_{i=1}^{I} \exp(-x_i \beta_i)\)

注意到这个表达式只通过\(\sum_{i=1}^{I} x_i\)（总分）依赖于数据。

## 6.3 条件概率的计算

给定总分\(r = \sum_{i=1}^{I} x_i\)，具体反应模式的条件概率为：

\(P(\mathbf{X} = \mathbf{x} | \sum_{i=1}^{I} x_i = r) = \frac{P(\mathbf{X} = \mathbf{x})}{P(\sum_{i=1}^{I} x_i = r)}\)

由于分子分母中的\(\exp(\theta r)\)项会相消，结果不依赖于\(\theta\)！

## 6.4 充分统计量的实际含义

充分统计量的实际应用

**情况1：** 学生A答对了题目1、3、5，总分=3

**情况2：** 学生B答对了题目2、4、6，总分=3

**Rasch模型的结论：** 两个学生的能力估计完全相同！

**含义：** 只要总分相同，具体答对哪些题目并不重要

这个特性使得Rasch模型具有很强的实用性，因为我们可以用简单的总分来代替复杂的反应模式。
