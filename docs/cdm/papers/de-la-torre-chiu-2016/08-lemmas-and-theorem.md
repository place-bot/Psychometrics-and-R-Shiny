# 两个引理、主定理与证明

## 引理 1：折叠不改变总均值

对任意更粗或更细的属性分组：

\[
\bar p(\boldsymbol\alpha_{K:K''})
=
\bar p(\boldsymbol\alpha_{1:K''}).
\tag{9}
\]

证明直接代入折叠概率：

\[
\begin{aligned}
\bar p(\boldsymbol\alpha_{K:K''})
&=
\sum_{\boldsymbol\alpha_{K:K''}}
w(\boldsymbol\alpha_{K:K''})
p(\boldsymbol\alpha_{K:K''})\\
&=
\sum_{\boldsymbol\alpha_{K:K''}}
\sum_{\boldsymbol\alpha_{1:K-1}}
w(\boldsymbol\alpha_{1:K''})
p(\boldsymbol\alpha_{1:K''})\\
&=
\bar p(\boldsymbol\alpha_{1:K''}).
\end{aligned}
\]

所以所有候选 GDI 中的 \(-\bar p^2\) 是同一个常数。比较 GDI 等价于比较

\[
\sum w p^2.
\]

## 引理 2：恢复一个有效属性不会降低 \(\sum wp^2\)

将粗组按一个真正影响成功率的属性拆成两组。记两子组的权重和成功率为

\[
w_0,p_0,
\qquad
w_1,p_1.
\]

粗组贡献为

\[
(w_0+w_1)
\left(
\frac{w_0p_0+w_1p_1}{w_0+w_1}
\right)^2.
\]

细组贡献为

\[
w_0p_0^2+w_1p_1^2.
\]

两者之差：

\[
\begin{aligned}
&w_0p_0^2+w_1p_1^2
-
\frac{(w_0p_0+w_1p_1)^2}{w_0+w_1}\\
&\qquad=
\frac{w_0w_1}{w_0+w_1}(p_0-p_1)^2
\ge 0.
\end{aligned}
\tag{10}
\]

把所有其余属性组合上的差相加，便得到论文 Lemma 2：

\[
\sum w_{\text{粗}}p_{\text{粗}}^2
\le
\sum w_{\text{细}}p_{\text{细}}^2.
\]

等号成立的条件是每次拆分的两个子组满足 \(p_0=p_1\)。

## 主定理

令 \(\boldsymbol q^*\) 为正确 q-vector，任意候选 \(\boldsymbol q\) 满足

\[
\varsigma_j^2(\boldsymbol q)
\le
\varsigma_j^2(\boldsymbol q^*).
\tag{11}
\]

### 情形 1：只增设属性

候选包含全部真实所需属性，并加入若干无关属性。正确分组已经组内同质，继续细分后的子组成功概率相同：

\[
p(\boldsymbol\alpha_{\boldsymbol q})
=
p(\boldsymbol\alpha_{\boldsymbol q^*}).
\]

所以

\[
\varsigma_j^2(\boldsymbol q)
=
\varsigma_j^2(\boldsymbol q^*).
\]

### 情形 2：同时漏设与增设

先忽略增设的无关属性，它们不改变 GDI；再逐个恢复遗漏的真实属性。每恢复一个属性，根据引理 2，\(\sum wp^2\) 非减。根据引理 1，\(\bar p^2\) 不变。最终得到式 (11)。

### 情形 3：只漏设属性

这是情形 2 没有增设属性的特例，同样由引理 2 得到。

## 定理能够支持的结论

- 总体成功概率和总体权重已知时，正确 q-vector 达到最大 GDI；
- 严格增设的向量可能与正确向量并列；
- 最少属性规则可以从并列最大值中选择正确向量。

## 从定理到样本算法还差什么

实践中使用

\[
\widehat w,\qquad
\widehat p,\qquad
\widehat{\varsigma}^2.
\]

这些量由初始 Q 拟合产生。有限样本噪声可能让全属性向量的估计 GDI略高于正确向量；初始 Q 的系统偏差也可能改变排序。因此定理给出总体目标的合理性，样本估计性质还需要额外条件。
