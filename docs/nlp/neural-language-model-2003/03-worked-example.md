# 手算：条件概率与 Perplexity

设词表 \(\{a,b,c\}\)，当前上下文经网络得到 logits：

\[
y=(1.2,\;0.3,\;-0.5).
\]

## 1. Softmax

\[
e^{1.2}\approx3.320,\quad
e^{0.3}\approx1.350,\quad
e^{-0.5}\approx0.607.
\]

\[
Z\approx5.277.
\]

\[
P(a)\approx0.629,\quad
P(b)\approx0.256,\quad
P(c)\approx0.115.
\]

真实下一个词为 \(b\)：

\[
L=-\log0.256\approx1.363.
\]

logits 梯度：

\[
\frac{\partial L}{\partial y}
\approx(0.629,\;-0.744,\;0.115).
\]

它继续更新输出层、隐藏层和上下文词 embedding。

## 2. Perplexity

测试集 \(N\) 个 token：

\[
\operatorname{PPL}
=
\exp\!\left(
-\frac1N\sum_t\log P(w_t\mid context_t)
\right).
\]

若平均 NLL 为 1.363：

\[
\operatorname{PPL}=e^{1.363}\approx3.91.
\]

它可理解为模型平均不确定性的指数尺度；越低越好。不同 tokenization、词表与 OOV 处理的 perplexity 不能直接横比。

## 3. 向量泛化

若 §cat§ 与 §dog§ 的 \(C(w)\) 接近，那么包含 cat 的已见上下文可通过共享网络参数帮助 dog 的相似上下文。这是论文对抗离散组合稀疏性的核心路径。
