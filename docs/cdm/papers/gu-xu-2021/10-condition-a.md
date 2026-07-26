# Condition A：完整性

## 1. 定义

DINA 下 \(Q\) 完整，指经过行置换后包含

\[
I_K=
\begin{pmatrix}
1&0&\cdots&0\\
0&1&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&1
\end{pmatrix}.
\]

每个属性至少有一道只要求该属性的题。

## 2. 为什么单属性题能分开潜类

对单位行 \(\boldsymbol e_k\)，DINA 理想反应为

\[
\Gamma_{j,\boldsymbol\alpha}
=I(\alpha_k=1).
\]

所以这道题把潜类按第 \(k\) 个属性直接分成两组。\(K\) 道单位行合起来，使任意两个不同属性模式至少在一题的理想反应上不同。

形式上，完整性保证

\[
\boldsymbol\alpha\ne\boldsymbol\alpha'
\quad\Longrightarrow\quad
\Gamma_{\cdot,\boldsymbol\alpha}(Q)
\ne
\Gamma_{\cdot,\boldsymbol\alpha'}(Q).
\]

## 3. 缺少完整性的后果

若没有属性 \(k\) 的单属性题，一些潜类可能在全部题上具有相同能力状态。它们的比例只能以和的形式进入观测分布。

假设两个模式 \(\boldsymbol\alpha,\boldsymbol\alpha'\) 对所有题满足

\[
\Gamma_{j,\boldsymbol\alpha}
=
\Gamma_{j,\boldsymbol\alpha'}.
\]

则观测分布只依赖

\[
p_{\boldsymbol\alpha}
+p_{\boldsymbol\alpha'},
\]

无法单独恢复两个比例。

## 4. Study IV 的构造

补充材料取 \(J=20\)，分别构造：

- \(K=3\) 的不完整 \(Q_1\)；
- \(K=5\) 的不完整 \(Q_2\)。

作者再给出两张替代矩阵 \(Q_i'\)、\(Q_i''\)，保持题目参数相同，把无法区分潜类的比例重新合并或分配。

三组模型对全部

\[
2^{20}=1,048,576
\]

种反应模式给出相同概率，最大数值差在

\[
2.17\times10^{-19}
\quad\text{到}\quad
6.51\times10^{-19}
\]

之间。

## 5. 严格识别与泛识别

对 DINA，Condition A 也不能在泛识别中整体放松。潜类理想反应列一旦结构性重合，比例不可分的现象覆盖整个参数区域，具有正维数。

## 6. 测验设计解释

完整性给每个属性提供语义锚点。没有单属性题时，即使多属性题很多，也可能只能识别属性组合，无法给每一列稳定命名和分离。

这条要求依赖 DINA 的合取规则。一般 RLCM 的泛识别可把它放松为泛完整性，允许锚题同时要求其他属性。
