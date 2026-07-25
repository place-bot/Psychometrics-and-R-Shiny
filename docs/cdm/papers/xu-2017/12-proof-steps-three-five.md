# 证明步骤 3--5

## 步骤 3：完成零阶与一阶属性列

步骤 3 要证明

\[
\theta_{j,\boldsymbol0}
=
\bar\theta_{j,\boldsymbol0},
\qquad
\theta_{j,\boldsymbol e_k}
=
\bar\theta_{j,\boldsymbol e_k},
\qquad j\le2K,
\]

以及

\[
p_{\boldsymbol0}
=
\bar p_{\boldsymbol0},
\qquad
p_{\boldsymbol e_k}
=
\bar p_{\boldsymbol e_k}.
\]

### C2 产生对比向量

由步骤 1--2，剩余题在 \(\boldsymbol0\) 与
\(\boldsymbol e_k\) 列的参数已经跨两套模型相等。C2 保证

\[
\left(
1,\theta_{2K+1,\boldsymbol e_k},\ldots,
\theta_{J,\boldsymbol e_k}
\right)^\top
\]

和

\[
\left(
1,\theta_{2K+1,\boldsymbol0},\ldots,
\theta_{J,\boldsymbol0}
\right)^\top
\]

不成比例。于是存在 \(\boldsymbol u_k\) 使前一向量保留为
\(b_k\ne0\)，后一向量被消成 0。

把 \(\boldsymbol u_k\) 作用到由常数行与剩余题单题行组成的矩阵，相当于构造一个在
\(\boldsymbol e_k\) 列保留信息、在 \(\boldsymbol0\) 列消失的线性组合。

### 与锚定题选择行结合

论文把这个线性组合与前 \(2K\) 个锚定题的变换行逐元素相乘。比较“未加入第 \(k\) 道锚定题”和“加入后”的两条行等式，得到

\[
\theta_{k,\boldsymbol e_k}
=
\bar\theta_{k,\boldsymbol e_k}.
\tag{4.11}
\]

对第二单位块同理：

\[
\theta_{K+k,\boldsymbol e_k}
=
\bar\theta_{K+k,\boldsymbol e_k}.
\]

交换保留与消除的角色，可识别前 \(2K\) 题的零属性概率。

### 隔离类比例

当锚定题参数已经相等，选择只在
\(\boldsymbol0\) 列非零的变换行，式 (3.5) 直接给出

\[
p_{\boldsymbol0}
=
\bar p_{\boldsymbol0}.
\]

再对每个 \(\boldsymbol e_h\) 构造只在该列非零的行，得到

\[
p_{\boldsymbol e_h}
=
\bar p_{\boldsymbol e_h}.
\tag{4.13}
\]

最后把任意一条前 \(2K\) 题加入对应选择行，通过已识别的
\(p_{\boldsymbol e_h}>0\) 得到其单属性列项目概率相等。

## 步骤 4：两个属性的列

固定 \(1\le h_1<h_2\le K\)。目标是

\[
p_{\boldsymbol e_{h_1}+\boldsymbol e_{h_2}}
=
\bar p_{\boldsymbol e_{h_1}+\boldsymbol e_{h_2}},
\]

\[
\theta_{j,\boldsymbol e_{h_1}+\boldsymbol e_{h_2}}
=
\bar\theta_{j,\boldsymbol e_{h_1}+\boldsymbol e_{h_2}}
\quad\forall j.
\]

论文选择新的 \(\boldsymbol\theta^*\)，使前 \(K\) 个锚定行的乘积最多只在两列上非零：

\[
\boldsymbol e_{h_2},
\qquad
\boldsymbol e_{h_1}+\boldsymbol e_{h_2}.
\]

前一列的项目参数和类比例已由步骤 3 识别。将两套模型的边际等式相减后，已知列抵消，只剩二属性列，因此识别

\[
p_{\boldsymbol e_{h_1}+\boldsymbol e_{h_2}}.
\]

把第 \(j\) 题加入题目子集，又能隔离
\(\theta_{j,\boldsymbol e_{h_1}+\boldsymbol e_{h_2}}\)。

对 \(j>K\) 使用第一个单位块构造；对 \(j\le K\) 对称地使用第二个单位块，最终覆盖所有题。

## 步骤 5：按属性个数归纳

假设所有含少于 \(k\) 个属性的模式已经识别，即对 \(l<k\)：

\[
p_{\sum_{i=1}^l\boldsymbol e_{h_i}}
=
\bar p_{\sum_{i=1}^l\boldsymbol e_{h_i}},
\]

\[
\theta_{j,\sum_{i=1}^l\boldsymbol e_{h_i}}
=
\bar\theta_{j,\sum_{i=1}^l\boldsymbol e_{h_i}}.
\]

对一个含 \(k\) 个属性的目标模式

\[
\boldsymbol\alpha^*
=
\sum_{i=1}^k\boldsymbol e_{h_i},
\]

取

\[
\theta_i^*
=
\begin{cases}
\theta_{i,\boldsymbol0},
&i\in\{h_1,\ldots,h_k\},\\
\theta_{i,\boldsymbol1},
&i\in\{1,\ldots,K\}
\setminus\{h_1,\ldots,h_k\},\\
0,&\text{其他题}.
\end{cases}
\]

所得选择行的非零列只会来自目标属性集合的子集。所有真子集项已经由归纳假设识别，所以边际等式中唯一的新未知类比例是

\[
p_{\boldsymbol\alpha^*}.
\]

先识别该比例，再加入第 \(j\) 题识别
\(\theta_{j,\boldsymbol\alpha^*}\)。对第二单位块做对称构造后覆盖其余题。

从 \(k=3\) 一直推进到 \(K\)，所有潜在类列都被识别。

## 五步合起来

| 步骤 | 新识别的对象 |
| --- | --- |
| 1 | \(Q'\) 题的 \(\boldsymbol0\) 列 |
| 2 | \(Q'\) 题的全部 \(\boldsymbol e_k\) 列 |
| 3 | 两个 \(I_K\) 块的零/单属性列及对应 \(p\) |
| 4 | 全部二属性列及对应 \(p\) |
| 5 | 三属性直到全属性列及对应 \(p\) |

最终

\[
\Theta=\bar\Theta,
\qquad
\boldsymbol p=\bar{\boldsymbol p},
\]

完成定理 1。

## 证明策略的抽象形式

\[
\text{锚定块消零}
\longrightarrow
\text{低阶属性模式先识别}
\longrightarrow
\text{已知真子集项抵消}
\longrightarrow
\text{归纳识别高阶模式}.
\]

这解释了作者为何按属性模式的 Hamming weight 排列 \(\Theta\) 的列。
