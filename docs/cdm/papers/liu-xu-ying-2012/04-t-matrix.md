# B-vector 与 T-matrix

## 列：全部属性模式

\(T\)-matrix 有 \(2^K\) 列。每一列对应一个属性模式 \(\boldsymbol\alpha\)。列顺序可以任意选择，但 \(T\) 与 \(\boldsymbol p\) 必须使用同一顺序。

## 单题 B-vector

对题目 \(j\)，定义长度 \(2^K\) 的行向量

\[
B_{Q',\boldsymbol c,\boldsymbol g}(j)
=
\left(
\Pr(R^j=1\mid\boldsymbol\alpha,Q',\boldsymbol c,\boldsymbol g)
:
\boldsymbol\alpha\in\{0,1\}^K
\right).
\tag{5}
\]

若属性模式按 \(\boldsymbol\alpha_1,\ldots,\boldsymbol\alpha_{2^K}\) 排列，第 \(a\) 个元素就是

\[
g_j+(c_j-g_j)\xi^j(\boldsymbol\alpha_a,Q').
\]

## 多题 B-vector

局部独立给出

\[
B(j_1,j_2)
=
B(j_1)\odot B(j_2),
\]

其中 \(\odot\) 表示逐元素乘法。一般地，

\[
B(j_1,\ldots,j_\ell)
=
\bigodot_{h=1}^{\ell}B(j_h).
\]

第 \(a\) 个元素是属性模式 \(\boldsymbol\alpha_a\) 下同时答对这 \(\ell\) 道题的概率。

## 行：所选择的题目组合

选定题组集合

\[
\mathcal C=\{A_1,\ldots,A_L\},
\]

把相应 B-vector 堆叠：

\[
T_{\boldsymbol c,\boldsymbol g}(Q')
=
\begin{pmatrix}
B(A_1)\\
\vdots\\
B(A_L)
\end{pmatrix}.
\]

因此 \(T\) 的维度是

\[
L\times 2^K.
\]

## 乘以属性分布

\[
T_{\boldsymbol c,\boldsymbol g}(Q')\boldsymbol p
\tag{6}
\]

对每个属性模式的条件联合答对概率做加权平均，得到总体联合答对率。

若候选结构和参数正确，

\[
\boldsymbol\beta
\xrightarrow{\text{a.s.}}
T_{\boldsymbol c,\boldsymbol g}(Q)\boldsymbol p,
\qquad N\to\infty.
\tag{7}
\]

## 维度检查

\[
\underbrace{T}_{L\times2^K}
\underbrace{\boldsymbol p}_{2^K\times1}
=
\underbrace{\text{模型矩}}_{L\times1},
\qquad
\underbrace{\boldsymbol\beta}_{L\times1}.
\]

每次推公式先做这个检查，可以避免把学生后验矩阵、类别比例和题组矩混在一起。

## T 与 Q 的关系

Q 改变某题的理想反应分组，进而改变该题 B-vector；所有包含这道题的多题 B-vector也会改变。因此一次 q-vector 更新会同时影响多条矩约束。
