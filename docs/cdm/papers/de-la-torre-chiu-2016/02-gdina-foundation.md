# G-DINA 基础与约化属性模式

## 题目只读取所需属性

全属性模式写成

\[
\boldsymbol\alpha_l
=
(\alpha_{l1},\ldots,\alpha_{lK}),
\qquad
\alpha_{lk}\in\{0,1\}.
\]

题目 \(j\) 的 q-vector 为 \(\boldsymbol q_j\)。所需属性数：

\[
K_j^*
=
\sum_{k=1}^{K}q_{jk}.
\]

删除所有 \(q_{jk}=0\) 的位置，得到题目约化属性模式：

\[
\boldsymbol\alpha^*_{lj}.
\]

例如 \(K=4\)，\(\boldsymbol q_j=1011\)。全模式 \(1101\) 对该题的约化模式为

\[
\boldsymbol\alpha^*_{lj}=101.
\]

属性 2 没有进入该题反应函数。

## identity-link 饱和 G-DINA

题目需要 \(K_j^*\) 个属性时，G-DINA 为全部主效应和交互效应留出参数：

\[
\begin{aligned}
P_j(\boldsymbol\alpha^*_{lj})
= {}&
\delta_{j0}
+\sum_{k=1}^{K_j^*}\delta_{jk}\alpha_{lk}\\
&+\sum_{k<k'}\delta_{jkk'}
\alpha_{lk}\alpha_{lk'}
+\cdots\\
&+\delta_{j12\cdots K_j^*}
\prod_{k=1}^{K_j^*}\alpha_{lk}.
\end{aligned}
\tag{1}
\]

这里：

- \(\delta_{j0}\)：零属性组的基线成功概率；
- \(\delta_{jk}\)：属性 \(k\) 的主效应；
- \(\delta_{jkk'}\)：双属性交互；
- 最高阶项：全部所需属性同时掌握产生的额外效应。

## 三属性例子

当 \(K_j^*=3\)：

\[
P_j(101)
=
\delta_{j0}
+\delta_{j1}
+\delta_{j3}
+\delta_{j13},
\]

\[
\begin{aligned}
P_j(111)
= {}&
\delta_{j0}
+\delta_{j1}
+\delta_{j2}
+\delta_{j3}\\
&+\delta_{j12}
+\delta_{j13}
+\delta_{j23}
+\delta_{j123}.
\end{aligned}
\]

一题有 \(2^{K_j^*}\) 个约化模式，也有同样多的饱和参数。概率向量与效应参数向量之间是一一线性变换。

## 为什么验证算法使用完整模式

初始 Q 只为项目模型规定局部分组。Q 验证时还要比较其它候选 q-vector，所以算法保留全部 \(2^K\) 个完整属性模式：

\[
\{000\cdots0,\ldots,111\cdots1\}.
\]

每个候选向量都对同一组完整模式重新分组。这样候选之间可以在同一个后验权重系统下比较。

## 与 2011 G-DINA 论文的接口

[de la Torre (2011) 专题](../de-la-torre-2011/index.md)解释了：

- G-DINA 的 design matrix；
- identity、logit 和 log link；
- MMLE/EM；
- DINA、DINO、A-CDM 等约化模型。

2016 年论文直接使用这个框架，将关注点转到 Q 行的经验验证。
