# 总结与后续阅读

## 一条主线

\[
\text{初始 Q 拟合 DINA}
\rightarrow
\widehat P(\boldsymbol\alpha\mid\boldsymbol X)
\rightarrow
(N_{jl},R_{jl})
\rightarrow
\widehat\delta_j(\boldsymbol q)
\rightarrow
\text{顺序搜索}
\rightarrow
\widehat Q(\varepsilon)
\rightarrow
\text{追加 EM 与专家审核}.
\]

## 五个核心公式

### 理想反应

\[
\eta_l(\boldsymbol q)
=
\prod_{k=1}^{K}\alpha_{lk}^{q_k}.
\]

### 候选 guessing

\[
\widehat g
=
\frac{R^{(0)}}{N^{(0)}}.
\]

### 候选 slipping

\[
\widehat s
=
\frac{N^{(1)}-R^{(1)}}{N^{(1)}}.
\]

### 候选区分度

\[
\widehat\delta
=
1-\widehat s-\widehat g.
\]

### 新增属性准则

\[
\widehat\delta^{(s)}
-
\widehat\delta^{(s-1)}
>
\varepsilon.
\]

## 原文三个实验的结论

| 实验 | 主要结果 | 不能推出 |
| --- | --- | --- |
| 模拟 | 当前 12 条件下恢复所有错误行，保留所有正确行 | 一般情形错误率恒为 0 |
| 分数减法 | \(\varepsilon=.009\)--.012 完整保留原 Q | 原 Q 在所有群体都是真实认知结构 |
| NAEP | 最优 \(\bar g+\bar s\) 从 .6923 降到 .6847 | Q 修改已经解决明显模型失配 |

## 最重要的实质结论

分数减法反例中，给题 1 加入无关属性 5 后：

\[
\bar g+\bar s:.2461\rightarrow.2379.
\]

统计指标改善，内容解释却变差。Q 矩阵验证需要把两类证据放在同一决策中：

\[
\text{response-data evidence}
+
\text{substantive evidence}.
\]

## 原文算法与当前 CDM 包

| 方面 | 原文 | `CDM::din.validate.qmatrix()` |
| --- | --- | --- |
| 候选搜索 | 逐步加属性 | 穷举所有非零向量 |
| 候选数 | 最多 \(K(K+1)/2\) | \(2^K-1\) |
| 阈值 | 相邻步骤增量 | 候选相对原行的 IDI 改善 |
| 后验计数 | EM expected counts | 同一思想 |
| 最终比较 | 多 \(\varepsilon\)、追加 EM、内容审核 | 返回建议 Q，后续需用户完成 |

## 与后续论文的关系

下一篇建议读：

[de la Torre & Chiu (2016)：一般经验 Q 矩阵验证](../categories/q-matrix.md)

重点比较：

- 2008 年方法为何依赖 DINA；
- generalized discrimination index 怎样适配更广 CDM；
- sequential search 的局部路径问题怎样处理；
- cutoff 怎样解释；
- 后验误差和多属性项目怎样影响恢复。

再往后读：

1. Chiu (2013)：基于残差的统计 Q 细化；
2. Liu, Xu and Ying (2012, 2013)：数据驱动 Q 学习及理论；
3. Chen et al. (2018)：Bayesian DINA Q estimation；
4. Gu and Xu (2021)：Q 自身可识别的必要充分条件。

## 与 CAT 的边界

本文没有逐学生实时选题、停止规则或测试序列生成。它处理题库中“题目需要哪些认知属性”这一层。对 cognitive CAT，经过验证的 Q 会进入：

- 学生属性后验；
- 候选题成功概率；
- 属性覆盖约束；
- 诊断信息与选题效用。

因此它是 adaptive policy 的模型基础文献。
