# 代码实现精读

## 原始代码状态

论文写明：

- DINA EM 用 Ox 实现；
- Ox 控制台版当时可供学术研究与教学免费使用；
- EM 代码可向作者索取；
- HO-DINA MCMC 来自 de la Torre and Douglas (2004)。

论文没有给出：

- 代码清单；
- 下载链接；
- 版本控制仓库；
- 软件许可证；
- 运行参数文件；
- 分数减法数据文件。

所以当前无法对原始 Ox 源码逐行审计。

## 本站教学实现

仓库提供：

```text
tools/de_la_torre_2009_dina_em.py
```

它只使用 Python 标准库，实现：

1. Table 1 的 30×5 Q 矩阵；
2. 等概率属性模式模拟；
3. Equation 1 的理想反应；
4. Equation 5 的边际似然；
5. Equations A10--A11 的 EM 更新；
6. Equation A15 的观测信息标准误；
7. 按所需属性数汇总参数恢复。

## 快速运行

默认用较小设置：

```bash
python3 tools/de_la_torre_2009_dina_em.py
```

默认参数为：

```text
500 students
30 items
5 attributes
3 replications
g = s = 0.20
```

## 对齐论文设计

```bash
python3 tools/de_la_torre_2009_dina_em.py \
  --examinees 2000 \
  --replications 100 \
  --seed 2009
```

这是纯 Python 教学实现，运行时间不能与论文的 Ox/3.0 GHz 数字直接比较。

## 复现固定先验

脚本默认：

\[
\pi_l=\frac{1}{32}
\]

且 EM 过程中保持不变，对齐论文模拟的等概率模式和基础附录算法。

论文讨论的经验 Bayes 扩展可通过：

```bash
python3 tools/de_la_torre_2009_dina_em.py \
  --update-prior
```

启用。输出会明确显示 `fixed uniform prior = False`。

## 公式到函数的映射

| 论文对象 | 代码 |
| --- | --- |
| \(\eta_{lj}\) | `ideal_response()` |
| 全部 \(2^K\) 模式 | `all_attribute_patterns()` |
| \(w_{il}=P(\alpha_l\mid X_i)\) | `e_step()` |
| \(I_j^{(z)},R_j^{(z)}\) | `m_step()` 内的期望计数 |
| \(\hat g_j=R_j^{(0)}/I_j^{(0)}\) | `m_step()` |
| \(\hat s_j=(I_j^{(1)}-R_j^{(1)})/I_j^{(1)}\) | `m_step()` |
| A15 信息矩阵 | `appendix_standard_errors()` |
| EM 外循环 | `fit_dina_em()` |

## E 步的数值稳定性

代码先计算每个模式的对数权重：

```python
log_weight = log(prior)
log_weight += log(P) if x else log(1 - P)
```

然后减去最大对数权重再指数化。它实现 log-sum-exp，避免 30 个概率连乘下溢。

## A15 的实现

对每名学生生成长度 \(2J\) 的期望得分向量：

```python
score[2 * j] = posterior_eta_zero * (x - g) / (g * (1 - g))
score[2 * j + 1] = (
    posterior_eta_one
    * ((1 - s) - x)
    / ((1 - s) * s)
)
```

信息矩阵为：

```python
information += score @ score.T
```

脚本用高斯—Jordan 消元求逆，并取对角线平方根。

## 单次论文规模检查

运行

```bash
python3 tools/de_la_torre_2009_dina_em.py \
  --examinees 2000 \
  --replications 1
```

应看到与 Table 2 同样的标准误结构：

```text
required  mean(SE_g)  mean(SE_s)
       1       ~.016       ~.015
       2       ~.011       ~.021
       3       ~.010       ~.030
```

随机种子会影响单次点估计，100 次汇总才与论文 Table 2 属于同一证据层次。

## 实现边界

脚本没有：

- 拟合 HO-DINA 或 MCMC；
- 读取原始分数减法数据；
- 搜索或验证 Q 矩阵；
- 强制 \(1-s_j>g_j\)；
- 处理缺失反应；
- 提供生产级优化；
- 复刻未知的原始 Ox 内部结构。

它的用途是把附录公式变成可检查的执行路径。
