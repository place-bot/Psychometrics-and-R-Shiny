# Q 的条件后验与均匀先验

## 条件后验

给定当前学生属性、失误率和猜测率，

\[
p(Q\mid
\boldsymbol Y,\boldsymbol\alpha,\boldsymbol s,\boldsymbol g)
\propto
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q)
I(Q\in\mathcal Q).
\]

由于 \(\mathcal Q\) 有限，可以把先验写得更明确：

\[
p(Q)
=
\begin{cases}
1/|\mathcal Q|,&Q\in\mathcal Q,\\
0,&Q\notin\mathcal Q.
\end{cases}
\]

## 合法候选之间的后验比

若 \(Q,Q^\star\in\mathcal Q\)，则

\[
\frac{p(Q^\star\mid-)}{p(Q\mid-)}
=
\frac{
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q^\star)
}{
p(\boldsymbol Y\mid
\boldsymbol\alpha,\boldsymbol s,\boldsymbol g,Q)
}.
\]

先验常数完全抵消。

## 只更新一个题目子集时

若候选只改变题目集合 \(\mathcal B\) 中的 q 元素，其余题目的似然贡献相消：

\[
\frac{p(Q^\star\mid-)}{p(Q\mid-)}
=
\prod_{i=1}^{N}
\prod_{j\in\mathcal B}
\frac{
p(Y_{ij}\mid
\boldsymbol\alpha_i,s_j,g_j,\boldsymbol q_j^\star)
}{
p(Y_{ij}\mid
\boldsymbol\alpha_i,s_j,g_j,\boldsymbol q_j)
}.
\]

补充代码的 `updateQ_MH()` 正是对选中的 `index` 行计算该比值。

## 对数域实现

原始 C++ 逐学生累乘概率比：

```cpp
ratio = ratio * pynext / pyold;
```

在更大的 \(N\) 或 \(J\) 下容易下溢。稳健实现应计算

\[
\log r
=
\min\left\{
0,\
\ell(Q^\star)-\ell(Q)
\right\},
\]

再比较

\[
\log U\le \log r.
\]

这是本站代码精读提出的数值工程建议，论文公式本身允许这种等价实现。

## 均匀先验的含义

均匀是对**整张有标签矩阵**均匀。Q 的不同列置换代表属性标签交换，会产生相同观测模型。论文在汇总阶段把列编码排序，从而把这些状态合并。

若每个等价类含同样数量的列置换，合并后仍对应类上的均匀权重。存在重复列时轨道大小会变化；本文的两套单位阵使不同属性列具有各自单位行结构，列本身不会完全相同。

## 后验学习依赖什么

Q 的信息来自当前属性样本与作答之间的匹配。例如把 \(q_{jk}\) 从 0 改成 1 后，只有满足其他所需属性且缺少属性 \(k\) 的学生会改变 \(\eta_{ij}\)。这些学生的答对与答错计数决定该翻转的后验倾向。

[下一页：三类候选生成器总览](10-proposal-overview.md)
