# 可计算复现

## 本站脚本

[`tools/de_la_torre_2008_q_validation.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/de_la_torre_2008_q_validation.py) 实现：

- 原文 Table 3 的 \(30\times5\) Q；
- Table 4 的 Conditions 0--11；
- DINA 数据生成与 empirical-prior EM；
- 后验期望人数、答对人数；
- 任意候选 q-vector 的 \(\widehat g,\widehat s,\widehat\delta\)；
- \(2^K-1\) 穷举搜索；
- 原文 forward sequential search；
- \(\varepsilon\) 停止规则；
- 假想题的精确计算。

它复用本站对 de la Torre (2009) 编写的透明 DINA EM，不依赖 NumPy 或专有软件。

## 运行

在仓库根目录：

```bash
python3 tools/de_la_torre_2008_q_validation.py
```

默认：

- Condition 11；
- \(N=1200\)，便于快速检查；
- \(\varepsilon=.00,.01,.05,.10,.20\)；
- 随机种子 2008。

使用原文样本量：

```bash
python3 tools/de_la_torre_2008_q_validation.py \
  --condition 11 \
  --paper-scale \
  --compare-q
```

检查其他条件：

```bash
python3 tools/de_la_torre_2008_q_validation.py \
  --condition 5 \
  --examinees 5000
```

## 假想题的确定性输出

脚本首先输出：

```text
step 1: 10000:.30, 01000:.30, 00100:.00, 00010:.00, 00001:.00
step 2: 11000:.60, 10100:.20, 10010:.20, 10001:.20
step 3: 11100:.51, 11010:.51, 11001:.51
selected 11000 with g=.20, s=.20, delta=.60
```

这些数值精确复现原文 Tables 1--2 的搜索主线：

\[
.30\rightarrow.60\rightarrow.51,
\]

因此停在双属性向量 \(11000\)。

## 代码到公式的映射

| 代码 | 公式对象 |
| --- | --- |
| `posterior_expected_counts()` | \(N_{jl},R_{jl}\) |
| `candidate_from_counts()` | \(\widehat g_{jl'},\widehat s_{jl'},\widehat\delta_{jl'}\) |
| `all_nonzero_q_vectors()` | \(\{0,1\}^K\setminus\{\boldsymbol0\}\) |
| `exhaustive_search()` | 全部 \(2^K-1\) 候选 |
| `sequential_search()` | 原文逐步加属性 |
| `misspecified_q_matrix()` | Table 4 |
| `mean_guess_plus_slip()` | \(\bar g+\bar s\) |
| `proposed_q_matrix()` | 把 30 道题的建议行组成候选 Q |
| `continue_em()` | 候选 Q 下追加 5 个 EM cycles |

## 顺序搜索的停止代码

```python
if accepted is not None \
        and best.delta - accepted.delta <= cutoff:
    break
```

接受新增属性的条件等价于：

\[
\widehat\delta^{(s)}
-
\widehat\delta^{(s-1)}
>
\varepsilon.
\]

## 为什么随机输出不会逐格等于原表

原文没有公开：

- 随机数种子；
- Ox 初始化细节；
- empirical Bayesian prior 的全部实现设置；
- 每套候选 Q 的完整中间状态。

本站脚本用于核对算法和方向。随机模拟会因种子、后验估计与 EM 实现产生数值差异；原文的固定表格数值应以论文 Tables 5--6 为准。

## 可复现边界

脚本没有附带受版权与授权限制的：

- 2144 人分数减法反应矩阵；
- NAEP restricted-use 或抽样权重数据；
- 原作者 Ox 源码。

因此两项真实数据页面复现的是设计、公式与已报告结果，无法声称重新计算了原表。

## 可继续扩展的检查

可在脚本基础上增加：

- 多次 replication 的 Q 行恢复率；
- 不同 \(N,J,K\)；
- 属性相关与稀疏模式；
- 低 \(\delta\) 题目；
- leave-one-item-out posterior；
- bootstrap 推荐频率；
- 与 `CDM::din.validate.qmatrix()` 穷举解的逐题比较。
