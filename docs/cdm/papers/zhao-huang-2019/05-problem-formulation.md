# 监督学习任务的数学表述

## 1. 输入与标签

对第 \(j\) 道题，记：

- 原始题干：\(d_j\)；
- 专家类别：\(y_j\in\{O,M\}\)；
- 特征向量：\(\boldsymbol x_j\in\mathbb R^p\)。

训练样本为

\[
\mathcal D
=
\{(\boldsymbol x_j,y_j)\}_{j=1}^{n}.
\]

## 2. 文本到 Q 行

分类器给出

\[
\widehat y_j=f_{\widehat\theta}(\boldsymbol x_j).
\]

类别与 Q 行的映射为

\[
\widehat{\boldsymbol q}_j
=
\begin{cases}
(1,0),&\widehat y_j=O,\\
(0,1),&\widehat y_j=M.
\end{cases}
\]

## 3. 训练目标

三类模型采用不同损失：

### Logistic Regression

\[
\widehat\theta_{\mathrm{LR}}
=
\arg\min_\theta
\left\{
-\sum_{j\in\mathcal T}
\log p_\theta(y_j\mid\boldsymbol x_j)
+\lambda\|\theta\|_2^2
\right\}.
\]

### SVM

\[
(\widehat{\boldsymbol w},\widehat b)
=
\arg\min_{\boldsymbol w,b}
\left\{
\frac12\|\boldsymbol w\|_2^2
+C\sum_{j\in\mathcal T}\ell_{\mathrm{hinge},j}
\right\}.
\]

论文打印的是平方松弛变量形式，详见 SVM 章节。

### Gaussian NB

\[
\widehat y_j
=
\arg\max_{c\in\{O,M\}}
\widehat p(c)
\prod_{r=1}^{p}
\widehat p(x_{jr}\mid c).
\]

## 4. 特征数量也是超参数

信息增益先对全部文本特征排序。对

\[
k\in\{5,10,\ldots,300\},
\]

只保留前 \(k\) 个特征。于是每个模型还包含一个经验证集选择的超参数：

\[
\widehat k
=
\arg\max_{k}
\operatorname{Score}_{\mathcal V}
\left(f_{\widehat\theta(k)}\right).
\]

## 5. 最终测试

固定 \(\widehat k\) 后，在测试集 \(\mathcal E\) 上计算：

\[
\operatorname{Accuracy}_{\mathcal E},
\qquad
\operatorname{WeightedF1}_{\mathcal E}.
\]

若训练、验证和测试严格分离，则测试集只应在最后使用一次。

## 6. 论文任务的核心假设

该方法依赖：

\[
p(y\mid d)
\]

在训练题和新题之间保持相对稳定。

当课程术语、题型模板、语言风格或属性定义改变时，文本到属性的映射会发生 domain shift。论文的单题库随机划分无法测量这种变化。
