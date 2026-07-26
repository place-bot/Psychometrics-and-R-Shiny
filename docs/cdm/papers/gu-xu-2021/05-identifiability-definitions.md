# 严格识别、泛识别与列标签交换

## 1. 观测等价

两组对象观测等价，指

\[
\Pr(\boldsymbol R=\boldsymbol r\mid Q,\Theta,\boldsymbol p)
=
\Pr(\boldsymbol R=\boldsymbol r\mid
\bar Q,\bar\Theta,\bar{\boldsymbol p})
\]

对所有

\[
\boldsymbol r\in\{0,1\}^{J}
\]

同时成立。

## 2. 列标签交换

若把 \(Q\) 的第 1、2 列互换，并同步重标记属性模式，观测分布保持不变。论文用

\[
\bar Q\sim Q
\]

表示两张 Q 只差一个列置换。

识别结论最多达到“在列置换意义下唯一”。这属于潜变量模型的固有标签对称性。

## 3. 联合严格识别

若观测等价必然推出

\[
(\bar Q,\bar\Theta,\bar{\boldsymbol p})
\sim
(Q,\Theta,\boldsymbol p),
\]

则称三者联合严格可识别。

“严格”表示参数空间中每个合法点均满足唯一性。一个特殊点失去唯一性，就足以破坏严格识别。

## 4. 联合泛识别

设给定 \(Q\) 的自由参数空间 \(\vartheta_Q\subset\mathbb R^m\)。定义不可识别集合

\[
\vartheta_{\mathrm{non}}
=
\left\{
(\Theta,\boldsymbol p):
\begin{array}{l}
\exists(\bar Q,\bar\Theta,\bar{\boldsymbol p})
\nsim(Q,\Theta,\boldsymbol p),\\
\Pr(\boldsymbol R\mid Q,\Theta,\boldsymbol p)
=
\Pr(\boldsymbol R\mid\bar Q,\bar\Theta,\bar{\boldsymbol p})
\end{array}
\right\}.
\]

若 \(\vartheta_{\mathrm{non}}\) 在 \(\mathbb R^m\) 中的 Lebesgue 测度为 0，则称联合泛可识别。

## 5. 局部与全局

- 局部识别：真参数的某个邻域内没有另一组等价参数；
- 全局识别：整个参数空间都没有另一组等价参数；
- 局部泛识别：除零测集外，真参数在局部邻域唯一；
- 全局泛识别：除零测集外，真参数在全空间唯一。

强弱关系可以写成

\[
\text{严格全局识别}
\Longrightarrow
\text{全局泛识别}
\Longrightarrow
\text{局部泛识别}.
\]

反向推导通常不成立。

## 6. 对有限样本的直觉

泛识别允许一个零测代数集合。真参数即使没有落在该集合上，只要离它很近，有限样本似然面也会变平，估计方差和优化难度都可能增大。

因此：

\[
\text{泛识别}
\]

给出几乎处处一致估计的理论基础；

\[
\text{离不可识别集合的距离}
\]

继续控制有限样本难度。
