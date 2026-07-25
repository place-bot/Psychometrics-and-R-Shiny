# MLE、不变性与标准误

## 饱和概率的信息矩阵

论文对项目 \(j\) 的概率向量

\[
\boldsymbol P_j
\]

构造观测信息矩阵。对两个约化模式 \(\boldsymbol a,\boldsymbol b\)，信息元素可以写成后验 score 的乘积和：

\[
\mathcal I_{ab}
=
\sum_{i=1}^{I}
u_{ia}u_{ib},
\]

其中

\[
u_{ia}
=
\tau_{ij}(\boldsymbol a)
\frac{
X_{ij}-P_j(\boldsymbol a)
}{
P_j(\boldsymbol a)
[1-P_j(\boldsymbol a)]
}.
\]

代入 \(\widehat{\boldsymbol P}_j\) 后，

\[
\widehat{\operatorname{Var}}
(\widehat{\boldsymbol P}_j)
\approx
\mathcal I(\widehat{\boldsymbol P}_j)^{-1}.
\]

单个概率的标准误是协方差矩阵相应对角元素的平方根。

## 饱和参数为什么也是 MLE

对饱和模型，效应参数是概率向量的一一变换：

\[
\widehat{\boldsymbol\phi}_j
=
f(\widehat{\boldsymbol P}_j).
\]

由于 MLE 的不变性，

\[
\widehat{\boldsymbol P}_j
\text{ 是 MLE}
\Longrightarrow
f(\widehat{\boldsymbol P}_j)
\text{ 是相应参数的 MLE}.
\]

这适用于：

\[
\widehat{\boldsymbol\delta}_j,
\qquad
\widehat{\boldsymbol\lambda}_j,
\qquad
\widehat{\boldsymbol\nu}_j.
\]

## 多元 delta method

若

\[
\boldsymbol\phi_j=f(\boldsymbol P_j),
\]

则

\[
\operatorname{Var}
\left[
f(\widehat{\boldsymbol P}_j)
\right]
\approx
G_j
\operatorname{Var}(\widehat{\boldsymbol P}_j)
G_j^\top,
\]

其中

\[
G_j
=
\left.
\frac{\partial f(\boldsymbol P_j)}
{\partial\boldsymbol P_j^\top}
\right|_{\widehat{\boldsymbol P}_j}.
\]

identity link 下，

\[
G_j=(M_j^{(S)})^{-1}.
\]

logit 与 log link 还要乘相应的逐元素导数：

\[
\frac{d\,\operatorname{logit}(P)}{dP}
=
\frac{1}{P(1-P)},
\qquad
\frac{d\log P}{dP}
=
\frac{1}{P}.
\]

## 边界概率的影响

当 \(\widehat P\) 接近 0 或 1：

- logit 与 log 导数会迅速变大；
- 协方差矩阵可能病态；
- Wald 近似可能不稳定；
- 某些约化组的有效样本量可能很小。

因此，标准误的数值可计算性和渐近可靠性需要分别判断。

## 论文没有完成的验证

论文指出仍需系统研究：

- 不同样本量下参数与 SE 的准确性；
- 属性分布不均衡时的表现；
- \(K_j^*\) 增长时 Wald 近似的质量；
- 非特殊约化类两步估计的统计性质。

这些内容属于论文提出的研究议程，模拟部分只直接验证了 A-CDM Wald test 的部分性质。
