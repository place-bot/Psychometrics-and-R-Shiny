# GDI 的定义与统计解释

## 定义

候选 q-vector 产生若干约化属性组。G-DINA discrimination index 定义为

\[
\begin{aligned}
\varsigma_j^2(\boldsymbol q)
&=
\sum_{\boldsymbol\alpha_{\boldsymbol q}}
w(\boldsymbol\alpha_{\boldsymbol q})
\left[
p_j(\boldsymbol\alpha_{\boldsymbol q})
-\bar p_j
\right]^2\\
&=
\sum_{\boldsymbol\alpha_{\boldsymbol q}}
w(\boldsymbol\alpha_{\boldsymbol q})
p_j^2(\boldsymbol\alpha_{\boldsymbol q})
-\bar p_j^2,
\end{aligned}
\tag{5}
\]

其中

\[
\bar p_j
=
\sum_{\boldsymbol\alpha_{\boldsymbol q}}
w(\boldsymbol\alpha_{\boldsymbol q})
p_j(\boldsymbol\alpha_{\boldsymbol q}).
\tag{6}
\]

## 条件期望方差

因为

\[
p_j(\boldsymbol\alpha_{\boldsymbol q})
=
E(Y_j\mid\boldsymbol\alpha_{\boldsymbol q}),
\]

所以

\[
\varsigma_j^2(\boldsymbol q)
=
\operatorname{Var}_w
\left\{
E(Y_j\mid\boldsymbol\alpha_{\boldsymbol q})
\right\}.
\tag{7}
\]

它测量候选分组能够解释多少“组间成功率差异”。

## 全方差公式

完整模式的 GDI 可分解为

\[
\begin{aligned}
\operatorname{Var}
\{E(Y_j\mid\boldsymbol\alpha)\}
= {}&
E\!\left[
\operatorname{Var}
\{E(Y_j\mid\boldsymbol\alpha)
\mid\boldsymbol\alpha_{\boldsymbol q}\}
\right]\\
&+
\operatorname{Var}
\{E(Y_j\mid\boldsymbol\alpha_{\boldsymbol q})\}.
\end{aligned}
\tag{8}
\]

第二项就是候选 GDI，第一项非负。因此：

\[
\varsigma_j^2(\boldsymbol q)
\le
\varsigma_j^2(\boldsymbol 1).
\]

## 与 \(R^2\) 的关系

Liu (2017) 指出，

\[
\frac{\varsigma_j^2(\boldsymbol q)}
{\operatorname{Var}(Y_j)}
\]

具有类似 \(R^2\) 的解释：候选属性分组解释了二分反应总变异的多少。

论文实际使用的 PVAF 分母是饱和属性分组 GDI：

\[
\operatorname{PVAF}_j(\boldsymbol q)
=
\frac{\varsigma_j^2(\boldsymbol q)}
{\varsigma_j^2(\boldsymbol 1)}.
\]

它衡量候选保留了完整分组可解释方差的比例。

## 与 2008 年 \(\delta\) 的关系

DINA 只有两个成功概率：

\[
p_0=g,
\qquad
p_1=1-s.
\]

两组差为

\[
p_1-p_0=1-s-g=\delta.
\]

二组情况下：

\[
\varsigma^2
=
w_0w_1(p_1-p_0)^2
=
w_0w_1\delta^2.
\]

所以 GDI 将 DINA 的两组区分推广为多组成功概率的加权方差。
