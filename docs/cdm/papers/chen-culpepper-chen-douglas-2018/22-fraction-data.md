# Experiment：分数减法数据与分析设计

## 数据

Tatsuoka 分数减法数据包含：

\[
N=536\ \text{名中学生},
\qquad
J=20\ \text{道题}.
\]

每个作答按 0/1 计分。该数据可从 R 包 `CDM` 的 `fraction.subtraction.data` 取得，也是 Q 矩阵研究中反复使用的经典数据。

## 专家定义的八个属性

原文 Table 2 列出：

1. 把整数转换成分数；
2. 从分数中分离整数部分；
3. 在相减前先约分；
4. 寻找公分母；
5. 从整数部分借位；
6. 借位后用第一分子的变换值减第二分子；
7. 分子相减；
8. 把计算结果约成最简形式。

## 专家 Q 的结构问题

专家 Q 有 \(K=8\)。几乎所有题都要求属性 7，许多题同时要求多个属性。对只有 20 道题的测验：

- 两套 \(I_8\) 已经需要 16 道纯题；
- 每个属性至少三题还需要额外覆盖；
- Table 2 的专家 Q 不满足本文使用的可识别结构。

作者因此没有把 \(K=8\) Q 直接放进受限算法，而分别探索

\[
K=3
\quad\text{和}\quad
K=4.
\]

## 分析目标

比较：

- 受限 MH；
- 受限 Gibbs；
- Chung（2014）无约束 Gibbs。

对每个 \(K\) 报告：

\[
\widehat Q,\qquad
\widehat s_j,\qquad
\widehat g_j.
\]

受限 Gibbs 和 MH 得到同一张后验众数 Q，因此 Tables 3--4 只并排展示 MH 与无约束 Gibbs，并在表下注明 CGibbs 的 Q 与 MH 相同。

## 补充 R 脚本

原作者脚本：

```r
data(fraction.subtraction.data)
Y = as.matrix(fraction.subtraction.data)
K = 3
burnin = 20000
chain_length = burnin + 10000
B = 2*K
```

随后依次调用：

```r
dina_Gibbs_Q(Y, K, burnin, chain_length)
DINA_MH_Q(Y, K, B, burnin, chain_length)
DINA_Gibbs_Q_unconst(Y, K, burnin, chain_length)
```

这段公开脚本设定 20,000 次 burn-in、10,000 个保留样本。若要复现 \(K=4\)，需把 `K` 改为 4 后重新运行。

## 解释属性的方式

探索性 Q 的列标签由模型无法命名。作者观察哪些题只加载某一列，再结合题目操作内容，给三个属性赋予解释：

1. 找公分母；
2. 从整数部分借位；
3. 对整数和分数部分分别执行减法。

这些名称是对估计列的事后内容解释，并非算法输入。

## 实证证据边界

论文没有报告：

- \(K=3\) 与 \(K=4\) 的边际似然或信息准则比较；
- 后验预测检验；
- 学生分类准确性；
- 专家对探索性属性解释的独立复核；
- 不同链初值的稳定性。

因此结果展示两种低维探索结构，无法据此断言 \(K=3\) 或 \(K=4\) 是唯一正确的属性数。

[下一页：Experiment——K=3 的逐题结果](23-fraction-k3.md)
