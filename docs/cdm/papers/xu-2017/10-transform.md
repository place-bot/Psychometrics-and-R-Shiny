# 命题 3：可逆平移变换

## 命题内容

对任意

\[
\boldsymbol\theta^*
=
(\theta_1^*,\ldots,\theta_J^*)^\top
\in\mathbb R^J,
\]

存在一个只依赖 \(\boldsymbol\theta^*\) 的可逆矩阵
\(D(\boldsymbol\theta^*)\)，满足

\[
T\!\left(
Q,\Theta-\boldsymbol\theta^*\boldsymbol 1^\top
\right)
=
D(\boldsymbol\theta^*)T(Q,\Theta).
\tag{P3}
\]

\(D(\boldsymbol\theta^*)\) 是下三角矩阵，且全部对角元为 1。

## 左侧做了什么

\(\boldsymbol\theta^*\boldsymbol 1^\top\) 的第 \(j\) 行是

\[
(\theta_j^*,\ldots,\theta_j^*).
\]

因此新的单题行元素为

\[
\theta_{j,\boldsymbol\alpha}-\theta_j^*.
\]

如果选

\[
\theta_j^*
=
\theta_{j,\boldsymbol\alpha_0},
\]

则属性列 \(\boldsymbol\alpha_0\) 在该单题行变为零。若 Q 限制让一批潜在类共享同一概率，这一选择会同时消掉整批单元。

## 两题展开

对 \(J=2\)，原 \(T\)-矩阵的一列是

\[
\begin{pmatrix}
1\\
\theta_1\\
\theta_2\\
\theta_1\theta_2
\end{pmatrix}.
\]

平移后为

\[
\begin{pmatrix}
1\\
\theta_1-\theta_1^*\\
\theta_2-\theta_2^*\\
(\theta_1-\theta_1^*)
(\theta_2-\theta_2^*)
\end{pmatrix}.
\]

最后一项展开为

\[
\theta_1\theta_2
-\theta_2^*\theta_1
-\theta_1^*\theta_2
+\theta_1^*\theta_2^*.
\]

所以平移后的每一行都是原 \(T\)-矩阵较低阶行的线性组合。

对应的变换矩阵可写成

\[
D(\boldsymbol\theta^*)
=
\begin{pmatrix}
1&0&0&0\\
-\theta_1^*&1&0&0\\
-\theta_2^*&0&1&0\\
\theta_1^*\theta_2^*&-\theta_2^*&-\theta_1^*&1
\end{pmatrix}.
\]

它是下三角，行列式为 1，必然可逆。

## 一般元素

若行指标按子集包含关系排序，对
\(\boldsymbol r'\preceq\boldsymbol r\)，
\(D\) 的系数来自多项式展开：

\[
d_{\boldsymbol r,\boldsymbol r'}
=
(-1)^{|\boldsymbol r|-|\boldsymbol r'|}
\prod_{j:r_j-r'_j=1}\theta_j^*.
\]

当 \(\boldsymbol r'\npreceq\boldsymbol r\) 时系数为 0；当
\(\boldsymbol r'=\boldsymbol r\) 时系数为 1。

## 为什么不改变可观测等式

若

\[
T(Q,\Theta)\boldsymbol p
=
T(Q,\bar\Theta)\bar{\boldsymbol p},
\]

两侧同乘同一个可逆矩阵得到

\[
T(Q,\Theta-\boldsymbol\theta^*\boldsymbol 1^\top)
\boldsymbol p
=
T(Q,\bar\Theta-\boldsymbol\theta^*\boldsymbol 1^\top)
\bar{\boldsymbol p}.
\]

因此研究平移后的矩阵与研究原观测分布完全等价。

## 证明中的“消元器”

命题 3 的用法可以概括为：

1. 选择一组 \(\theta_j^*\)；
2. 借 Q 限制把大量列变为零；
3. 取若干单题行的 Hadamard 乘积；
4. 得到只在一个或少数属性列上非零的行；
5. 将该行乘 \(\boldsymbol p\)，隔离一个概率或一个类比例；
6. 在 \((\Theta,\boldsymbol p)\) 与
   \((\bar\Theta,\bar{\boldsymbol p})\) 之间比较。

它相当于对 \(T\)-矩阵做面向潜在类列的符号消元。

## 为什么允许平移后离开概率区间

\(\Theta-\boldsymbol\theta^*\boldsymbol 1^\top\) 的元素可能为负，也不再是概率。论文把式 (3.3) 的代数定义扩展到
\(\Theta\notin[0,1]^{J\times2^K}\)。证明只使用多项式等式与可逆行变换，不要求变换后的数值仍具有概率解释。
