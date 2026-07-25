# 潜在类模型与张量表示

## 有限潜在类模型

论文先考虑 \(p\) 个有限状态观测变量

\[
X_1,\ldots,X_p.
\]

第 \(j\) 个变量的状态数是 \(\kappa_j\)，取值集合可记作

\[
\mathcal X_j=\{1,\ldots,\kappa_j\}.
\]

潜变量

\[
Z\in\{1,\ldots,r\}
\]

有 \(r\) 个类别，并且 \(r\) 已知。类别比例为

\[
\pi_i=P(Z=i),\qquad
\pi_i>0,\qquad
\sum_{i=1}^{r}\pi_i=1.
\]

给定 \(Z=i\) 后，各观测变量相互独立：

\[
P(X_1=x_1,\ldots,X_p=x_p\mid Z=i)
=
\prod_{j=1}^{p}P(X_j=x_j\mid Z=i).
\]

## 条件概率向量与矩阵

对潜在类 \(i\) 和观测变量 \(j\)，定义

\[
\boldsymbol p_{ij}
=
\bigl(
p_{ij}(1),\ldots,p_{ij}(\kappa_j)
\bigr),
\]

其中

\[
p_{ij}(\ell)=P(X_j=\ell\mid Z=i).
\]

它是一个概率向量：

\[
p_{ij}(\ell)\ge 0,
\qquad
\sum_{\ell=1}^{\kappa_j}p_{ij}(\ell)=1.
\]

把同一观测变量在所有潜在类下的条件分布按行堆叠，得到

\[
M_j
=
\begin{bmatrix}
\boldsymbol p_{1j}\\
\boldsymbol p_{2j}\\
\vdots\\
\boldsymbol p_{rj}
\end{bmatrix}
\in\mathbb R^{r\times\kappa_j}.
\]

行 \(i\) 对应潜在类，列 \(\ell\) 对应 \(X_j\) 的一个状态。每行和为 1，所以 \(M_j\) 是行随机矩阵（row-stochastic matrix）。

## 类内联合分布

给定 \(Z=i\)，整个反应向量的联合概率表是向量外积

\[
P_i
=
\boldsymbol p_{i1}\otimes\boldsymbol p_{i2}
\otimes\cdots\otimes\boldsymbol p_{ip}.
\]

它的 \((x_1,\ldots,x_p)\) 元素为

\[
P_i(x_1,\ldots,x_p)
=
\prod_{j=1}^{p}p_{ij}(x_j).
\]

总体观测分布是这些乘积分布的有限混合：

\[
P
=
\sum_{i=1}^{r}\pi_iP_i
=
\sum_{i=1}^{r}
\pi_i
\bigotimes_{j=1}^{p}\boldsymbol p_{ij}.
\tag{1}
\]

论文把这个模型记作

\[
\mathcal M(r;\kappa_1,\ldots,\kappa_p).
\]

## 参数维度与观测分布维度

类别比例有 \(r-1\) 个自由参数。每个 \(M_j\) 的每行有
\(\kappa_j-1\) 个自由参数，共有 \(r\) 行。因此参数空间维度为

\[
L
=
(r-1)+r\sum_{j=1}^{p}(\kappa_j-1).
\]

观测联合概率表有

\[
K_{\mathrm{obs}}
=
\prod_{j=1}^{p}\kappa_j
\]

个单元格，扣除总和为 1 的约束后有 \(K_{\mathrm{obs}}-1\) 个自由度。

维度比较

\[
L\le K_{\mathrm{obs}}-1
\]

是识别的必要直觉，但不是充分条件。参数化映射可能在维度匹配时仍为多对一，也可能因为模型像的实际维度降低而出现连续不可识别。

## 三个观测变量时的张量

当 \(p=3\) 时，联合分布是

\[
P(X_1=u,X_2=v,X_3=w)
=
\sum_{i=1}^{r}
\pi_i
M_1(i,u)M_2(i,v)M_3(i,w).
\]

定义

\[
\widetilde M_1=\operatorname{diag}(\boldsymbol\pi)M_1.
\]

论文用

\[
[\widetilde M_1,M_2,M_3]
\]

表示三路张量

\[
[\widetilde M_1,M_2,M_3]
=
\sum_{i=1}^{r}
\widetilde{\boldsymbol m}_{1i}
\otimes
\boldsymbol m_{2i}
\otimes
\boldsymbol m_{3i},
\]

其中 \(\boldsymbol m_{ji}\) 是 \(M_j\) 的第 \(i\) 行。该张量的
\((u,v,w)\) 元素恰好是观测联合概率：

\[
[\widetilde M_1,M_2,M_3]_{u,v,w}
=
P(X_1=u,X_2=v,X_3=w).
\]

于是总体分布的识别问题变成三路张量分解的唯一性问题。

## 两种不可避免的不唯一

### 同时置换三组行

若用同一个置换矩阵 \(P\) 改写三个因子：

\[
(\widetilde M_1,M_2,M_3)
\mapsto
(P\widetilde M_1,PM_2,PM_3),
\]

各潜在类求和项只改变排列顺序，张量不变。这就是标签置换。

### 三个因子之间的缩放

对第 \(i\) 个秩一分量，若

\[
\widetilde{\boldsymbol m}_{1i}
\mapsto a_i\widetilde{\boldsymbol m}_{1i},
\quad
\boldsymbol m_{2i}
\mapsto b_i\boldsymbol m_{2i},
\quad
\boldsymbol m_{3i}
\mapsto c_i\boldsymbol m_{3i},
\]

并满足

\[
a_ib_ic_i=1,
\]

外积不变。一般张量分解只能恢复到这种缩放。

概率模型额外知道 \(M_1,M_2,M_3\) 的每行和为 1。对恢复出的行重新归一化后，缩放被消除，剩余尺度进入 \(\pi_i\)。这一步把纯代数唯一性转成概率参数唯一性。

## 普通秩与 Kruskal 秩

矩阵 \(M\) 的普通行秩是所有行所张成空间的维度。Kruskal 行秩定义为

\[
\operatorname{rank}_K(M)
=
\max\left\{
k:
\text{\(M\) 的任意 \(k\) 行都线性无关}
\right\}.
\]

始终有

\[
\operatorname{rank}_K(M)\le \operatorname{rank}(M).
\]

例如

\[
M=
\begin{bmatrix}
1&0\\
1&0\\
0&1
\end{bmatrix}
\]

的普通秩为 2，但前两行线性相关，因此

\[
\operatorname{rank}_K(M)=1.
\]

Kruskal 秩比普通秩更强，因为张量唯一性需要保证任意若干潜在类行都不发生退化。

若一个 \(r\times\kappa\) 矩阵有满行秩 \(r\)，那么所有 \(r\) 行线性无关，从而

\[
\operatorname{rank}_K(M)=r.
\]

## 为什么两路表通常不够

两个观测变量只能给出矩阵分解

\[
P_{12}=M_1^\top\operatorname{diag}(\pi)M_2.
\]

矩阵分解可以插入可逆变换及其逆，通常不唯一。三路张量的第三个方向提供了额外耦合约束，Kruskal 定理正是利用这三组因子共同出现来保证唯一性。

## 对 CDM 的矩阵翻译

二分 CDM 中 \(\kappa_j=2\)，可以写

\[
M_j(i,\cdot)
=
\bigl(1-\theta_{j,i},\ \theta_{j,i}\bigr),
\]

其中

\[
\theta_{j,i}=P(Y_j=1\mid Z=i).
\]

单道题的 \(M_j\) 只有两列，所以

\[
\operatorname{rank}_K(M_j)\le 2.
\]

当潜在类数 \(r\) 很大时，单题矩阵无法提供足够高的 Kruskal 秩。论文后续把多道题合成一个大观测块，使块状态数从 2 增长到 \(2^{|S|}\)，这就是多变量定理的关键。

