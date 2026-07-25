# 三个 link function

## 统一形式

令

\[
\boldsymbol P_j
=
\left\{
P(\boldsymbol\alpha^*_{lj})
\right\}_{l=1}^{2^{K_j^*}}.
\]

论文在三个标度上展开属性主效应和交互效应：

\[
h\!\left[
P(\boldsymbol\alpha^*_{lj})
\right]
=
\phi_{j0}
+\sum_k\phi_{jk}\alpha_{lk}
+\sum_{k<k'}\phi_{jkk'}\alpha_{lk}\alpha_{lk'}
+\cdots.
\]

不同 \(h\) 对应不同模型家族。

## identity link

\[
h(P)=P.
\]

它直接分解成功概率：

\[
P(\boldsymbol\alpha^*_{lj})
=
\delta_{j0}
+\sum_k\delta_{jk}\alpha_{lk}
+\sum_{k<k'}\delta_{jkk'}\alpha_{lk}\alpha_{lk'}
+\cdots.
\]

解释最直接：

- \(\delta_{j0}\)：零属性组的成功概率；
- \(\delta_{jk}\)：单独增加属性 \(k\) 带来的概率变化；
- 交互项：联合掌握带来的额外变化。

该模型即论文命名的 G-DINA。

## logit link

\[
h(P)=\operatorname{logit}(P)
=
\log\frac{P}{1-P}.
\]

于是

\[
\operatorname{logit}
\left[
P(\boldsymbol\alpha^*_{lj})
\right]
=
\lambda_{j0}
+\sum_k\lambda_{jk}\alpha_{lk}
+\cdots.
\]

属性效应作用于 log-odds。论文称其为 log-odds CDM，并指出它与 log-linear CDM 等价，也可视为 GDM 的特殊形式。

## log link

\[
h(P)=\log P.
\]

于是

\[
\log
P(\boldsymbol\alpha^*_{lj})
=
\nu_{j0}
+\sum_k\nu_{jk}\alpha_{lk}
+\cdots.
\]

指数化以后，属性效应对成功概率产生乘法作用。

## 饱和时为什么拟合相同

若保留截距、全部主效应和全部阶数的交互效应，参数数目均为

\[
2^{K_j^*}.
\]

只要概率位于允许区间，三种 link 都能一一表示同一组 \(\boldsymbol P_j\)。因此：

\[
\text{相同的 }\widehat{\boldsymbol P}_j
\Longrightarrow
\text{相同的模型拟合}.
\]

区别出现在参数解释和坐标标度。

## 约化以后为什么结果不同

“删掉交互项”在三个标度上的含义分别是：

| link | 无交互的含义 |
| --- | --- |
| identity | 成功概率上的加法 |
| logit | log-odds 上的加法 |
| log | 成功概率上的乘法 |

它们参数数目可能相同，但预测概率集合不同。论文特别强调 A-CDM、LLM 和 G-NIDA/R-RUM 不能互换。

## 概率边界

logit link 自带

\[
0<P<1
\]

的归一化。

identity 和 log link 的约化模型需要显式保证预测概率有效。identity-link 的线性和可能超出 \([0,1]\)；log link 保证正数，但仍可能大于 1。实际估计时必须加入边界或单调约束。
