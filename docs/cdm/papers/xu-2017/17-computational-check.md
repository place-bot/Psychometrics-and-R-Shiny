# 代码实现与可计算核验

## 原文代码状态

论文没有报告软件包、GitHub 仓库、补充代码或数值算法实现。正文的研究对象是总体分布中的参数识别，证明不依赖某个估计程序。

因此本页进行公式到教学代码的映射，没有可供逐行审查的作者官方代码。

## 本站脚本

[`tools/xu_2017_rlcm_identifiability.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/xu_2017_rlcm_identifiability.py)
只使用 Python 标准库，并用 `Fraction` 保留精确有理数运算。

## Q 结构检查

| 函数 | 数学对象 |
| --- | --- |
| `is_complete()` | Q 是否含一个 \(I_K\) |
| `has_c1()` | 能否依次移除两个互不重叠的 \(I_K\) |
| `dina_structural_c2()` | 移除两个单位块后，是否仍含每个 \(\boldsymbol e_k\) |

最后一项专门针对 DINA 且 \(1-s_j>g_j\)。在 DINA 中，剩余题能区分
\(\boldsymbol e_k\) 与 \(\boldsymbol0\) 的结构条件是该题只要求属性 \(k\)。

一般 RLCM 的 C2 需要直接查看
\(\theta_{j,\boldsymbol e_k}\) 与
\(\theta_{j,\boldsymbol0}\)，不能只靠函数名中的 structural check。

## 构造 Theta

`dina_theta()` 实现

\[
\theta_{j,\boldsymbol\alpha}
=
\begin{cases}
1-s_j,&\boldsymbol\alpha\succeq\boldsymbol q_j,\\
g_j,&\text{其他}.
\end{cases}
\]

属性模式由 `binary_vectors(K)` 按 Hamming weight 排列，便于对应论文证明中的

\[
\boldsymbol0,\ \boldsymbol e_k,\ 
\boldsymbol e_{h_1}+\boldsymbol e_{h_2},\ldots
\]

顺序。

## 构造 T 矩阵

`t_matrix()` 对每个题目子集 \(\boldsymbol r\) 与属性模式
\(\boldsymbol\alpha\) 计算

\[
t_{\boldsymbol r,\boldsymbol\alpha}
=
\prod_{j:r_j=1}
\theta_{j,\boldsymbol\alpha}.
\]

`observed_distribution()` 独立枚举 exact response pattern：

\[
\sum_{\boldsymbol\alpha}
p_{\boldsymbol\alpha}
\prod_j
\theta_{j,\boldsymbol\alpha}^{r_j}
(1-\theta_{j,\boldsymbol\alpha})^{1-r_j}.
\]

`subset_marginals()` 再把 exact pattern 汇总为
\(P(\boldsymbol R\succeq\boldsymbol r)\)。两条计算路线相等才通过测试。

## 命题 3

`translation_matrix()` 构造

\[
d_{\boldsymbol r,\boldsymbol r'}
=
(-1)^{|\boldsymbol r|-|\boldsymbol r'|}
\prod_{j:r_j-r'_j=1}\theta_j^*
\]

并在
\(\boldsymbol r'\npreceq\boldsymbol r\) 时填 0。

程序分别计算：

\[
T(Q,\Theta-\boldsymbol\theta^*\boldsymbol1^\top)
\]

和

\[
D(\boldsymbol\theta^*)T(Q,\Theta),
\]

随后逐个有理数比较。它还验证 \(D\) 的对角元全为 1。

## 命题 2 的数值碰撞

脚本内置[反例页](14-counterexample.md)的两套参数，并用
`observed_distribution()` 枚举全部

\[
(0,0),(1,0),(0,1),(1,1)
\]

反应模式。`maximum_difference()` 返回精确分数 0。

## 运行方法

```bash
python3 tools/xu_2017_rlcm_identifiability.py
python3 tools/xu_2017_rlcm_identifiability.py --attributes 3
```

默认 \(K=2\)。属性数增大时，三个单位块产生 \(J=3K\) 道题，完整 \(T\)-矩阵有

\[
2^{3K}\times2^K
\]

个单元，因此该脚本定位为小规模教学检查。

## 实现边界

脚本没有：

- 拟合 RLCM；
- 实现 EM 或 MCMC；
- 从数据估计 Q；
- 证明 C1、C2 的一般定理；
- 把某个数值 \(T\)-矩阵满秩解释成联合参数识别；
- 实现 CAT 选题。

若要做真实数据估计，应使用经过验证的 CDM 软件，并在估计前后分别检查理论设计条件和数值稳定性。
