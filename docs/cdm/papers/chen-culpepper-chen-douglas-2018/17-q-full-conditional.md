# 单个 \(q_{jk}\) 的条件概率推导

## 哪些学生会受翻转影响

固定题目 \(j\) 和属性 \(k\)，设

\[
\eta_{ij,-k}
=
I(\alpha_{ih}\ge q_{jh},\ \forall h\ne k).
\]

只有满足

\[
\eta_{ij,-k}=1,\qquad
\alpha_{ik}=0
\]

的学生，其理想反应会随 \(q_{jk}\) 改变：

- 若 \(q_{jk}=0\)，则 \(\eta_{ij}=1\)；
- 若 \(q_{jk}=1\)，则 \(\eta_{ij}=0\)。

其他学生对条件似然比的贡献相消。

## 两个关键计数

在受影响学生中定义

\[
a_0
=
\sum_i
I(\eta_{ij,-k}=1,\alpha_{ik}=0,Y_{ij}=0),
\]

\[
a_1
=
\sum_i
I(\eta_{ij,-k}=1,\alpha_{ik}=0,Y_{ij}=1).
\]

原始代码的 `abcounts()` 返回这两个数。

## 条件似然比

当 \(q_{jk}=0\) 时，这些学生被视为全具备：

\[
L_0
\propto
s_j^{a_0}(1-s_j)^{a_1}.
\]

当 \(q_{jk}=1\) 时，他们被视为未全具备：

\[
L_1
\propto
(1-g_j)^{a_0}g_j^{a_1}.
\]

所以

\[
\frac{L_0}{L_1}
=
\left(\frac{s_j}{1-g_j}\right)^{a_0}
\left(\frac{1-s_j}{g_j}\right)^{a_1}.
\]

## \(q_{jk}=1\) 的条件概率

在 0 和 1 都合法、先验相同的情况下：

\[
P(q_{jk}=1\mid-)
=
\frac{L_1}{L_0+L_1}
=
\frac{1}{
1+
\left(\frac{s_j}{1-g_j}\right)^{a_0}
\left(\frac{1-s_j}{g_j}\right)^{a_1}
}.
\]

令

\[
\tau
=
a_0\log\frac{s_j}{1-g_j}
+
a_1\log\frac{1-s_j}{g_j},
\]

则

\[
P(q_{jk}=1\mid-)
=
\frac{1}{1+e^\tau}.
\]

## 与 C++ 判断式对应

代码抽 \(u\sim U(0,1)\)，然后判断

```cpp
log(1-u) - log(u) > tau
```

因为

\[
\log\frac{1-u}{u}>\tau
\quad\Longleftrightarrow\quad
u<\frac{1}{1+e^\tau},
\]

所以该判断精确实现了 Bernoulli 条件抽样。

## 一个数值例子

设

\[
s_j=0.10,\qquad
g_j=0.20,\qquad
a_0=8,\qquad
a_1=2.
\]

则

\[
\tau
=
8\log(0.1/0.8)
+
2\log(0.9/0.2)
\approx-13.63.
\]

因此

\[
P(q_{jk}=1\mid-)
\approx0.999999.
\]

受影响学生大多答错，数据强烈支持把他们归入未全具备组，也就支持 \(q_{jk}=1\)。

## 合法性先于概率

若某个取值让 Q 离开 \(\mathcal Q\)，它的条件先验概率为 0。此时无需计算似然，直接保留唯一合法值。

[下一页：整张 Q 的后验众数与列置换](18-posterior-summary.md)
