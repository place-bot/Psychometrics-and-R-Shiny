# 代码状态与实现精读

## 原文代码状态

对论文正文、开放全文、arXiv 版本和书目信息进行核验后，可确认：

- 正文没有代码仓库链接；
- 没有补充材料入口；
- 没有软件版本；
- 没有数据文件；
- 没有随机种子；
- 没有可直接运行的伪代码。

这与论文的理论定位一致。原文的“估计量”是数学定义，计算讨论集中在二次规划、分块和截断建议。

本站提供独立教学实现：

[`tools/liu_xu_ying_2013_theory_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/liu_xu_ying_2013_theory_check.py)

它用于核对结构恒等式和小规模枚举结果，没有冒充作者实现。

## 论文公式到代码对象

| 论文对象 | 代码对象 | 含义 |
| --- | --- | --- |
| \(\{0,1\}^k\) | `attribute_profiles(k)` | 枚举全部属性模式 |
| \(\xi^i(\boldsymbol A)\) | `ideal_response(q, profiles)` | 计算题目—模式能力指示 |
| \(B_{c,g,Q}(I_i)\) | `item_response_probabilities(...)` | 条件正确概率行 |
| 全部非空题组 | `item_subsets(m)` | 饱和矩的行索引 |
| \(T_{c,g}(Q)\) | `t_matrix_full(...)` | 堆叠题组概率乘积 |
| \(T(Q)\) | `deterministic_t_nonzero(q)` | 无噪声且排除全零模式 |
| \(\boldsymbol\alpha\) | `empirical_moments(...)` | 经验联合答对率 |
| 对 \(\boldsymbol p\) 取下确界 | `fit_simplex(t_matrix, target)` | 单纯形约束二次规划 |
| Q 列置换等价类 | `canonical_q(q)` | 枚举列置换后取规范表示 |
| 候选 Q 空间 | `candidate_q_matrices(m, k)` | 枚举无全零行的候选 |
| Proposition 6.6 的 D | `guessing_removal_matrix(...)` | 容斥中心化变换 |

## 理想反应

代码使用广播比较：

```python
np.all(
    profiles[None, :, :] >= q[:, None, :],
    axis=2,
).astype(float)
```

输出形状为

\[
m\times2^k.
\]

第 \((i,a)\) 个元素等于

\[
\mathbf1(\boldsymbol A_a\ge\boldsymbol q_i).
\]

## 条件正确概率

代码实现

```python
g + (c - g) * xi
```

逐元素对应

\[
g_i+(c_i-g_i)\xi^i(\boldsymbol A).
\]

输出仍为“题目 × 属性模式”的矩阵。

## 饱和 T-matrix

对每个非空题目子集 `subset`：

```python
np.prod(probabilities[list(subset), :], axis=0)
```

局部独立下，这等于组内题目全部答对的条件概率。所有行按题组大小再按字典序排列。

## 论文写法与代码写法的一个差异

论文在 \(T_{c,g}(Q)\) 中排除全零属性模式，再把其贡献写成

\[
p_0\boldsymbol g_{\mathrm{joint}}.
\]

代码直接保留全部 \(2^k\) 个模式列：

\[
\overline T_{c,g}(Q)
=
\left(
\boldsymbol g_{\mathrm{joint}},T_{c,g}(Q)
\right).
\]

两种表示完全等价。完整列表示更适合单纯形优化和数值核验。

## 单纯形剖面优化

`fit_simplex` 最小化

\[
\frac12
\|T\boldsymbol p-\boldsymbol y\|_2^2
\]

并约束

\[
0\le p_a\le1,\qquad
\sum_a p_a=1.
\]

代码使用 SLSQP，并提供解析梯度

\[
\nabla_{\boldsymbol p}
\frac12\|T\boldsymbol p-\boldsymbol y\|_2^2
=
T^\top(T\boldsymbol p-\boldsymbol y).
\]

由于目标关于 \(\boldsymbol p\) 凸，固定 T 下不存在非全局的局部极小问题。

## D 的实现

对题组 \(S\)，中心化矩展开为

\[
E\!\left[\prod_{i\in S}(R^i-g_i)\right]
=
\sum_{U\subseteq S}
(-1)^{|S|-|U|}
\left(\prod_{i\in S\setminus U}g_i\right)
E\!\left[\prod_{i\in U}R^i\right].
\]

`guessing_removal_matrix` 枚举 \(U\subseteq S\)，把每个系数放入 D 的对应位置。这个实现给出了 Proposition 6.6 中“存在 D”的显式计算版本。

## Q 等价类规范化

`canonical_q` 枚举 \(k!\) 个列置换，把展平后的最小元组作为等价类标识。小 \(k\) 下这种做法透明可靠；大 \(k\) 下可以改用更高效的二部图规范标号。

## 实现范围

脚本覆盖：

- 饱和 T 构造；
- 已知 \(c,g\) 的属性分布剖面；
- 小规模 Q 全枚举；
- D 变换；
- DINA 数据生成；
- 有限样本演示。

脚本没有实现：

- 未知 \(c\) 的嵌套剖面；
- 式（4.4）的所有候选结构搜索；
- 大规模分块与对齐；
- 2012 论文的逐行爬山算法；
- 自动属性数选择。

这样的范围与本站“核验理论对象”的目的相符。

[下一页：本站可计算核验](25-computational-check.md)
