# Experiment：主文泛识别模拟

## 1. 目标

主文 Section 3.1 用

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&0\\
0&1
\end{pmatrix}
\]

展示三件事：

1. 零测集上存在多组完全等价参数；
2. 零测集外的 MLE 随样本量增大而收敛；
3. 靠近零测集时收敛明显变慢。

## 2. Scenario (a)：精确不可识别

设置

\[
s_j=g_j=0.2,\qquad j=1,\ldots,4,
\]

\[
\boldsymbol p=(0.25,0.25,0.25,0.25).
\]

此时

\[
p_{01}p_{10}=p_{00}p_{11}.
\]

作者依照 Theorem 2(b.2) 的证明构造另外两组合法 DINA 参数。Figure 1(a) 显示三组参数明显不同，Figure 1(b) 显示 16 个反应模式概率完全重合。

## 3. Scenario (b)：随机参数

生成 \(B=100\) 组真参数：

\[
s_j\sim U(0.1,0.3),
\qquad
g_j\sim U(0.1,0.3),
\]

\[
\boldsymbol p\sim
\operatorname{Dirichlet}(3,3,3,3).
\]

官方代码实际使用

\[
c_j=1-s_j\sim U(0.7,0.9).
\]

## 4. 样本量与重复

对每组真参数，在每个

\[
N\in\{10^2,10^3,10^4,10^5\}
\]

下生成 200 个独立数据集。

总拟合次数为

\[
100\times4\times200=80,000
\]

个数据集。每个数据集再用 10 个随机初值运行 EM，所以候选 EM 运行数达到

\[
800,000.
\]

## 5. 估计与指标

每个数据集保留对数似然最大的 EM 解。对一组真参数，分别计算 200 次重复的平均逐元素平方误差：

\[
\operatorname{MSE}(\hat{\boldsymbol p})
=
\frac{1}{200\cdot2^K}
\sum_{b=1}^{200}
\|\hat{\boldsymbol p}^{(b)}-\boldsymbol p\|_2^2,
\]

\[
\operatorname{MSE}(\hat{\boldsymbol c})
=
\frac{1}{200J}
\sum_{b=1}^{200}
\|\hat{\boldsymbol c}^{(b)}-\boldsymbol c\|_2^2,
\]

\[
\operatorname{MSE}(\hat{\boldsymbol g})
=
\frac{1}{200J}
\sum_{b=1}^{200}
\|\hat{\boldsymbol g}^{(b)}-\boldsymbol g\|_2^2.
\]

Figure 2 对 100 组真参数的 MSE 画箱线图。

## 6. 结果

随着 \(N\) 从 \(10^2\) 增至 \(10^5\)，三类 MSE 的箱体和中位数均向 0 收缩，支持零测集外的泛识别与一致估计。

箱线图中仍有收敛较慢的离群点。Figure 3 把 \(N=10^5\) 时 \(\boldsymbol p\) MSE 最大的 20% 参数点标红，红点更靠近

\[
p_{00}p_{11}=p_{01}p_{10}
\]

对应的对角线。

## 7. 结果应怎样解读

实验支持“识别难度具有连续梯度”：

\[
\left|
p_{00}p_{11}-p_{01}p_{10}
\right|
\downarrow
\quad\Longrightarrow\quad
\text{有限样本 MSE 上升}.
\]

论文没有报告每个箱线图的数值表，所以可精确引用的结果是趋势、离群点比例和实验设置。
