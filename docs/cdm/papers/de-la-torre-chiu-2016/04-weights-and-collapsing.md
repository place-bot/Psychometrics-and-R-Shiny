# 后验权重、折叠分组与条件均值

## 完整模式的两个量

对每个完整属性模式 \(\boldsymbol\alpha\)，算法需要：

1. 模式权重

   \[
   w(\boldsymbol\alpha);
   \]

2. 题目成功概率

   \[
   p_j(\boldsymbol\alpha)
   =
   P(Y_j=1\mid\boldsymbol\alpha).
   \]

权重满足

\[
\sum_{\boldsymbol\alpha}w(\boldsymbol\alpha)=1.
\]

## 从学生后验得到权重

设学生 \(i\) 的属性模式后验为

\[
w_i(\boldsymbol\alpha)
=
P(\boldsymbol\alpha_i=\boldsymbol\alpha
\mid\boldsymbol Y_i,\widehat\Theta,Q_0).
\]

总体模式权重估计为

\[
\widehat w(\boldsymbol\alpha)
=
\frac{1}{N}\sum_{i=1}^{N}w_i(\boldsymbol\alpha).
\]

\(Q_0\) 是初始 Q，\(\widehat\Theta\) 是该 Q 下的项目和结构参数。

## 完整模式成功概率

对题目 \(j\)：

\[
\widehat p_j(\boldsymbol\alpha)
=
\frac{
\sum_{i=1}^{N}
w_i(\boldsymbol\alpha)Y_{ij}
}{
\sum_{i=1}^{N}
w_i(\boldsymbol\alpha)
}.
\tag{2}
\]

分子是模式 \(\boldsymbol\alpha\) 的后验期望答对人数，分母是后验期望人数。这个公式在 Liu (2017) 的评论中被明确写出，当前 `GDINA` 实现也采用相同计算。

## 候选 q-vector 怎样折叠类别

设候选只保留属性 \(K',\ldots,K''\)，约化模式写成

\[
\boldsymbol\alpha_{K':K''}.
\]

同一约化模式对应多个完整模式。折叠后的权重：

\[
w(\boldsymbol\alpha_{K':K''})
=
\sum_{\text{被省略属性}}
w(\boldsymbol\alpha_{1:K}).
\tag{3}
\]

折叠后的成功概率：

\[
p_j(\boldsymbol\alpha_{K':K''})
=
\frac{
\sum_{\text{被省略属性}}
w(\boldsymbol\alpha_{1:K})
p_j(\boldsymbol\alpha_{1:K})
}{
w(\boldsymbol\alpha_{K':K''})
}.
\tag{4}
\]

这是一个后验权重加权条件均值。

## 概率论写法

令 \(Z=\boldsymbol\alpha_{K':K''}\)，则

\[
p_j(Z)
=
E(Y_j\mid Z).
\]

候选验证实际上比较不同 \(Z\) 对 \(E(Y_j\mid\boldsymbol\alpha)\) 的信息压缩程度。

## 一个关键风险

\(w_i(\boldsymbol\alpha)\) 由初始 \(Q_0\) 拟合得到。若初始 Q 的错误足以严重扭曲属性分类，式 (2) 的权重也会偏，后续 GDI 会继承这种偏差。模拟只覆盖少量到中等误设，方法的适用性也建立在这个实践前提上。
