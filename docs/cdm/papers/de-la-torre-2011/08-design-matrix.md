# design matrix

## 矩阵形式

对项目 \(j\)，将全部约化模式的变换后成功概率组成向量：

\[
h(\boldsymbol P_j)
=
\left(
h[P(\boldsymbol\alpha^*_{1j})],
\ldots,
h[P(\boldsymbol\alpha^*_{2^{K_j^*}j})]
\right)^\top.
\]

模型写成

\[
h(\boldsymbol P_j)
=
M_j\boldsymbol\phi_j.
\]

其中：

- \(M_j\)：design matrix；
- \(\boldsymbol\phi_j\)：截距、主效应和交互效应；
- \(h\)：identity、logit 或 log。

## 三属性饱和矩阵

按照论文的模式顺序

\[
000,100,010,001,110,101,011,111,
\]

参数顺序为

\[
1,\alpha_1,\alpha_2,\alpha_3,
\alpha_1\alpha_2,
\alpha_1\alpha_3,
\alpha_2\alpha_3,
\alpha_1\alpha_2\alpha_3.
\]

饱和 design matrix 是

\[
M_j^{(S)}
=
\begin{pmatrix}
1&0&0&0&0&0&0&0\\
1&1&0&0&0&0&0&0\\
1&0&1&0&0&0&0&0\\
1&0&0&1&0&0&0&0\\
1&1&1&0&1&0&0&0\\
1&1&0&1&0&1&0&0\\
1&0&1&1&0&0&1&0\\
1&1&1&1&1&1&1&1
\end{pmatrix}.
\]

每一列对应一个属性子集，每一行对应一个约化属性模式。

## 从概率得到参数

饱和矩阵是方阵且可逆。论文用最小二乘形式写成

\[
\widehat{\boldsymbol\phi}_j
=
\left[
(M_j^{(S)})^\top M_j^{(S)}
\right]^{-1}
(M_j^{(S)})^\top
h(\widehat{\boldsymbol P}_j).
\]

在方阵可逆情形，它等价于

\[
\widehat{\boldsymbol\phi}_j
=
(M_j^{(S)})^{-1}
h(\widehat{\boldsymbol P}_j).
\]

分别代入三种 \(h\)，即可得到

\[
\widehat{\boldsymbol\delta}_j,
\qquad
\widehat{\boldsymbol\lambda}_j,
\qquad
\widehat{\boldsymbol\nu}_j.
\]

## design matrix 如何定义约化模型

删除列或合并组，就能定义不同模型。

三属性 DINA 的矩阵只有两列：

\[
M_j^{(\mathrm{DINA})}
=
\begin{pmatrix}
1&0\\
1&0\\
1&0\\
1&0\\
1&0\\
1&0\\
1&0\\
1&1
\end{pmatrix}.
\]

三属性 DINO 则让除 \(000\) 外的全部模式进入第二组：

\[
M_j^{(\mathrm{DINO})}
=
\begin{pmatrix}
1&0\\
1&1\\
1&1\\
1&1\\
1&1\\
1&1\\
1&1\\
1&1
\end{pmatrix}.
\]

A-CDM 保留前 \(K_j^*+1\) 列，即截距和主效应列。

## 模式顺序必须一致

design matrix、\(\boldsymbol P_j\)、协方差矩阵和限制矩阵必须采用同一行顺序。顺序错误通常不会触发维度报错，却会得到完全错误的效应解释与 Wald 结果。

代码实现应同时保存：

- 约化模式标签；
- design matrix 行；
- 成功概率向量；
- covariance matrix 行列名。
