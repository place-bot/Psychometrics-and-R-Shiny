# 区分度指标与验证目标

## 原文的正确性准则

对题目 \(j\)，让 \(\boldsymbol\alpha_{l'}\) 充当候选 q-vector，并按该向量计算 \(\eta_{ll'}\)。作者把最优候选写成

\[
\boldsymbol q_j
=
\underset{\boldsymbol\alpha_{l'}}{\arg\max}
\left[
P(X_j=1\mid\eta_{ll'}=1)
-
P(X_j=1\mid\eta_{ll'}=0)
\right].
\]

记括号中的差为

\[
\delta_{jl'}
=
P(X_j=1\mid\eta_{ll'}=1)
-
P(X_j=1\mid\eta_{ll'}=0).
\]

在 DINA 下，

\[
\delta_{jl'}=1-s_{jl'}-g_{jl'}.
\]

因此最大化 \(\delta\) 等价于最小化 \(s+g\)。

## 为什么它可以当作候选比较量

若 q-vector 合理：

- \(\eta=1\) 组应有较高答对率 \(1-s\)；
- \(\eta=0\) 组应有较低答对率 \(g\)；
- 两组差距较大。

若 q-vector 错分许多属性模式，两组答对率会向中间收缩，\(\delta\) 下降。

## 数值解释

| \(g\) | \(s\) | \(1-s\) | \(\delta\) | 含义 |
| ---: | ---: | ---: | ---: | --- |
| .20 | .20 | .80 | .60 | 两组相差 .60 |
| .20 | .50 | .50 | .30 | mastery 组被污染 |
| .50 | .20 | .80 | .30 | nonmastery 组被污染 |
| .48 | .49 | .51 | .03 | 两组几乎无法区分 |

## 它和 IRT discrimination 的差异

这里的 \(\delta\) 是两类条件答对率之差：

\[
\delta=P(X=1\mid\eta=1)-P(X=1\mid\eta=0).
\]

它依赖于：

- DINA 的 conjunctive 分组；
- 当前候选 q-vector；
- 当前后验属性模式分布；
- 当前样本的反应数据。

因此同一道题换一个 q-vector，\(\delta\) 就会改变。它没有在连续能力轴上定义斜率。

## 小参数充分，但不构成必要条件

作者专门提醒：

- 小 \(g\) 和小 \(s\) 可以支持当前 q-vector 的良好分离；
- 某题可能在现有属性集合下始终有较高 \(g\) 或 \(s\)；
- 换遍已有属性也不能改善时，问题可能来自遗漏属性、题目质量或 DINA 结构。

所以低 \(\delta\) 会触发诊断，无法单独确定该改哪一格 Q。

## 项目级和测验级目标

项目级搜索比较

\[
\widehat\delta_j(\boldsymbol q).
\]

当多个 \(\varepsilon\) 产生多套候选 Q 时，论文用测验级指标

\[
\overline{\widehat g}+\overline{\widehat s}
=
\frac{1}{J}\sum_{j=1}^{J}\widehat g_j
+
\frac{1}{J}\sum_{j=1}^{J}\widehat s_j
\]

比较整套解，并在候选 Q 下追加少量 EM 循环更新参数和后验。

两个层级的关系是：

\[
\text{逐题提出候选}
\longrightarrow
\text{组成候选 Q}
\longrightarrow
\text{全测验重新比较}.
\]

