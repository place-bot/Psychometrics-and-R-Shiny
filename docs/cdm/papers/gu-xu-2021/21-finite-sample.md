# 有限样本误差界

## 1. 识别分析的理想化

识别问题假设完整总体反应分布已知。实际数据只有

\[
\boldsymbol R_1,\ldots,\boldsymbol R_N.
\]

论文在 Discussion 中进一步给出有限样本错误概率的指数界。

## 2. 稀疏 B 参数化

一般 RLCM 可把题目概率写成主效应和交互效应：

\[
\theta_{j,\boldsymbol\alpha}
=
\sum_{S\subseteq\{1,\ldots,K\}}
\beta_{j,S}
\prod_{k\in S}\alpha_k.
\]

把全部 \(\beta_{j,S}\) 排成矩阵 \(B\)。Q 指定哪些效应允许非零，所以识别 Q 可以转化为识别 \(B\) 的非零支撑：

\[
\mathcal S_0=\operatorname{supp}(B^0).
\]

## 3. 分离常数

对支撑 \(\mathcal S\ne\mathcal S_0\) 且

\[
|\mathcal S|\le|\mathcal S_0|,
\]

比较候选分布与真分布的 Hellinger 距离。论文定义

\[
C_{\min}(\eta^0)
=
\inf_{\substack{\mathcal S\ne\mathcal S_0\\
|\mathcal S|\le|\mathcal S_0|}}
\frac{h^2(\eta^0,\eta)}
{|\mathcal S_0\setminus\mathcal S|}.
\]

它衡量真结构与错误稀疏结构之间的最小概率分离。

## 4. Proposition 4

若真 Q 满足严格联合识别的充分条件，则存在

\[
c_0>0
\]

使

\[
C_{\min}(\eta^0)\ge c_0.
\]

对带 \(L_0\) 支撑约束的联合 MLE \(\hat\eta\) 和已知真 Q 的 oracle MLE \(\hat\eta^0\)，

\[
\Pr(\hat Q\nsim Q^0)
\le
\Pr(\hat\eta\ne\hat\eta^0)
\le
c_2\exp\{-c_1NC_{\min}(\eta^0)\}.
\]

## 5. 解释

严格识别使错误结构与真结构之间存在正分离：

\[
\text{结构错误概率}
\lesssim
e^{-cN}.
\]

识别失败时，

\[
C_{\min}=0,
\]

上界退化到 \(O(1)\)，增加样本量也无法保证排除错误结构。

## 6. 泛识别附近

泛识别参数点的 \(C_{\min}\) 依赖它到不可识别零测集的距离。距离趋近 0 时，

\[
C_{\min}\downarrow0,
\]

达到同一精度所需的 \(N\) 会增大。

这和四题两属性模拟完全一致：靠近

\[
p_{00}p_{11}=p_{01}p_{10}
\]

的参数点具有更慢的 MSE 收敛。

## 7. 边界

该命题提供理论概率界，没有给出可直接计算的 \(c_1,c_2,c_0\)，也没有把它转化为样本量公式。它连接了“总体唯一性”和“有限样本结构恢复”，未替代具体算法分析。
