# Theorem 1：A/B/C 必要且充分

## 1. 矩阵分块

Condition A 允许经行置换写成

\[
Q=
\begin{pmatrix}
I_K\\
Q^\star
\end{pmatrix}.
\]

Theorem 1 断言：在 DINA 模型和

\[
p_{\boldsymbol\alpha}>0
\]

的参数空间中，以下三条合取是

\[
(Q,\boldsymbol s,\boldsymbol g,\boldsymbol p)
\]

严格联合识别的必要充分条件。

## 2. 三条条件

### A：完整性

\[
Q\ \text{含一套}\ I_K.
\]

### B：列互异性

\[
Q^\star_{\cdot k}\ne Q^\star_{\cdot \ell},
\qquad k\ne\ell.
\]

### C：重复测量

\[
\sum_{j=1}^{J}q_{jk}\ge3,
\qquad k=1,\ldots,K.
\]

## 3. “必要充分”的读法

充分性：

\[
A+B+C
\Longrightarrow
\text{所有合法参数点均联合唯一}.
\]

必要性：

\[
\neg A\ \text{或}\ \neg B\ \text{或}\ \neg C
\Longrightarrow
\text{至少存在一组不可区分的替代对象}.
\]

必要性不表示每个违反条件的参数点都失去泛识别。四题两属性例子违反 C，却在零测集之外可识别。

## 4. 三条条件的分工

| 条件 | 排除的歧义 |
| --- | --- |
| A | 潜类在理想反应层面无法区分 |
| B | 两个属性列在非锚题部分携带相同结构编码 |
| C | 单个属性只有一题或两题，题目参数和潜类比例可连续补偿 |

它们共同把三类对象锁定：

\[
\Gamma(Q)
\longrightarrow Q,
\qquad
\Gamma(Q),\text{反应分布}
\longrightarrow
(\boldsymbol s,\boldsymbol g,\boldsymbol p).
\]

## 5. 与 Chen et al.（2018）的条件对照

Chen et al. 的 Bayesian DINA Q 估计把采样空间限制为：

- 两套 \(I_K\)；
- 每列至少三个 1；
- 每行至少一个 1。

本文 Theorem 1 允许一套 \(I_K\)，用 \(Q^\star\) 列互异替代第二套单位阵。两套 \(I_K\) 会自动帮助列互异和重复测量，属于更容易执行的充分设计。

## 6. 直接实践含义

若测试开发者希望在 DINA 下联合学习整张 Q：

1. 每个属性设置一题单属性锚题；
2. 在其余题中给每个属性安排互异的二元编码；
3. 确保每个属性总计至少被三题要求。

这三步针对总体识别。有限样本下仍需考虑题目区分度、潜类稀疏、样本量和优化算法。
