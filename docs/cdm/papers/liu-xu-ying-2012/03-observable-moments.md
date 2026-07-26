# 从完整反应分布到可观测矩

## 候选模型给出的反应分布

用 \(Q'\) 表示任意候选矩阵。对反应模式 \(\boldsymbol r\in\{0,1\}^J\)，

\[
\Pr(\boldsymbol R=\boldsymbol r\mid Q',\boldsymbol p,\boldsymbol c,\boldsymbol g)
=
\sum_{\boldsymbol\alpha}
p_{\boldsymbol\alpha}
\prod_{j=1}^J
\pi_{j\boldsymbol\alpha}^{r_j}
(1-\pi_{j\boldsymbol\alpha})^{1-r_j}.
\tag{3}
\]

这是一个含 \(2^K\) 个潜在类的 Bernoulli 乘积分布混合。

## 经验反应分布

\[
\widehat P(\boldsymbol r)
=
\frac1N\sum_{i=1}^N
\mathbf 1(\boldsymbol R_i=\boldsymbol r).
\tag{4}
\]

若 Q 和参数正确，经验分布会随 \(N\) 增大逼近模型分布。

直接使用完整反应表需要处理 \(2^J\) 个反应模式。\(J=20\) 时已有 1,048,576 个格子，许多格子在一般样本中为空。论文转而使用从反应分布中抽取的低阶联合答对矩。

## 单题矩

对题目 \(j\)，

\[
\beta_{\{j\}}
=
\frac1N\sum_{i=1}^N R_i^j.
\]

它就是样本答对率。

## 题对矩

\[
\beta_{\{j_1,j_2\}}
=
\frac1N\sum_{i=1}^N
R_i^{j_1}R_i^{j_2}.
\]

乘积只有在两题均答对时等于 1，因此这是两题联合答对率。

## 一般题组矩

对非空题目集合 \(A\subseteq\{1,\ldots,J\}\)，

\[
\beta_A
=
\frac1N\sum_{i=1}^N
\prod_{j\in A}R_i^j.
\]

将选中的所有 \(\beta_A\) 按固定顺序堆成向量 \(\boldsymbol\beta\)。

## 关键区分

\(\boldsymbol\beta\) 完全由反应矩阵计算，不需要估计学生的属性模式。另一方面，模型对同一批矩的预测依赖 \(Q'\)、\(\boldsymbol c\)、\(\boldsymbol g\) 和 \(\boldsymbol p\)。Q 学习由“样本矩”和“模型矩”的差距驱动。

## 为什么联合矩有额外信息

只看单题答对率时，属性比例、slipping、guessing 和 q-vector 可以互相补偿。题对与更高阶矩加入“哪些题会被同一批学生共同答对”的结构，能排除更多错误 Q。阶数提高会带来更强约束，也会产生更稀疏、更不稳定的样本比例。
