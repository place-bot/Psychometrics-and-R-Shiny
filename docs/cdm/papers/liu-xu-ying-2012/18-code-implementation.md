# 公开代码状态与实现精读

## 原文实现状态

正式文章说明：

- MLE 可由 EM 计算；
- Q 搜索使用 Algorithm 1；
- 模拟采用 100 次重复。

正文、PMC 开放版本和作者论文页面均未给出：

- 源码仓库；
- 编程语言；
- 软件版本；
- EM 初值与容差；
- T 行的完整清单；
- 随机种子；
- 平局处理。

因此无法对原始实现逐行审计。

## 当前通用软件的关系

`CDM` 和 `GDINA` 等 R 包可以拟合给定 Q 的 DINA/G-DINA，也提供若干 Q 验证工具。它们的公开主接口没有把本文“低阶 T 矩 + 式 (17) + Algorithm 1”作为同名复现暴露出来。用这些包完成 EM 后仍需自行构造 T、\(\boldsymbol\beta\) 和离散搜索。

## 本站独立实现

[`tools/liu_xu_ying_2012_q_learning.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/liu_xu_ying_2012_q_learning.py) 提供一条透明教学链。

| Python 对象 | 论文对象 |
| --- | --- |
| `attribute_profiles()` | \(2^K\) 个 \(\boldsymbol\alpha\) |
| `ideal_response()` | 式 (1) 的 \(\xi^j\) |
| `response_probabilities()` | 式 (2) 的 \(g+(c-g)\xi\) |
| `item_subsets()` | T 的题组行集合 |
| `t_matrix()` | B-vector 堆叠 |
| `empirical_beta()` | 样本联合答对率 |
| `s_objective()` | 式 (14) |
| `fit_dina_em()` | 固定 Q 的 nuisance MLE |
| `profiled_objective()` | 式 (17) |
| `hill_climb_q()` | Algorithm 1 |
| `simulate_dina()` | 模拟反应 |

## `t_matrix()` 的核心

```python
item_prob = response_probabilities(q, c, g, profiles)
return np.vstack([
    np.prod(item_prob[list(s), :], axis=0)
    for s in subsets
])
```

每个题组取相应单题概率行的逐列乘积，直接对应 B-vector 定义。

## `empirical_beta()` 的核心

```python
np.mean(np.prod(y[:, list(s)], axis=1))
```

对每个学生先把题组反应相乘，再对学生平均。

## EM 的数值处理

实现使用：

- log-sum-exp 后验；
- 概率截断避免 \(\log0\)；
- 一致的初始化；
- 边际对数似然差作为收敛标准。

这些属于本站工程选择，原文没有给值。

## 搜索边界

函数库支持纳入全零行，以贴近 \(2^K\) 邻域定义。演示运行用 `include_zero=False`，因为六道教学题均应要求至少一个属性。该差异在命令输出和文档中明确记录。

## 复现层级

- 式 (9)、(10)、(13)：确定性精确核对；
- Tables 1--3：录入正式表值并做范围检查；
- 小型模拟：独立教学复现；
- 原文 100 次表格：缺少原始代码与若干设置，未宣称逐格重现。
