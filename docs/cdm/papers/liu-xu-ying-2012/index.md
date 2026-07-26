# Liu、Xu 与 Ying（2012）阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jingchen Liu, Gongjun Xu & Zhiliang Ying. *Data-Driven Learning of Q-Matrix*. |
| 期刊 | *Applied Psychological Measurement*, 36(7), 548--564 |
| DOI | [10.1177/0146621612456591](https://doi.org/10.1177/0146621612456591) |
| OnlineFirst | 16 August 2012 |
| Version of Record | 13 September 2012 |
| 开放全文 | [PubMed Central, PMC3733574](https://pmc.ncbi.nlm.nih.gov/articles/PMC3733574/) |
| 原文代码 | 正文与开放版本均未给出代码仓库、软件版本或随机种子 |
| 本站复现 | [`tools/liu_xu_ying_2012_q_learning.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/liu_xu_ying_2012_q_learning.py) |

## 一句话结论

论文把每个候选 Q 矩阵转换成一个 \(T\)-matrix，用它预测单题、题对乃至更高阶题组的联合答对率；候选 Q 越合适，

\[
T_{\widehat{\boldsymbol c},\widehat{\boldsymbol g}}(Q)
\widehat{\boldsymbol p}
\]

就越接近样本中直接算出的联合答对率向量 \(\boldsymbol\beta\)。算法从专家初始矩阵 \(Q_0\) 出发，每轮只改一道题的整行 q-vector，并选择使距离下降最多的改法。

## 这篇论文推进了什么

| 既有经验验证 | 本文的数据驱动学习 |
| --- | --- |
| 逐题看某个区分指标 | 同时匹配许多题组的联合反应矩 |
| 通常围绕给定 q-vector 做局部修正 | 把完整 Q 作为离散优化对象 |
| 指标直接依赖某种项目分组 | 用 \(T\)-matrix 统一写成 \(T(Q)\boldsymbol p\) |
| 主要输出逐题建议 | 输出局部搜索得到的整体 Q |

本文仍需要一个“足够接近真值”的 \(Q_0\)。因此这里的 data-driven learning 更适合解释成由反应数据驱动的整体校准与结构搜索。

## 推荐阅读顺序

1. [研究问题、贡献与证据边界](01-question-and-contribution.md)
2. [DINA 模型与全部基础符号](02-dina-setup.md)
3. [从完整反应分布到可观测矩](03-observable-moments.md)
4. [B-vector 与 T-matrix](04-t-matrix.md)
5. [三题两属性完整手算](05-t-matrix-example.md)
6. [目标函数与三种估计量](06-objective-functions.md)
7. [未知 \(c,g,p\) 与 DINA EM](07-nuisance-estimation.md)
8. [Algorithm 1 逐行爬山搜索](08-algorithm-one.md)
9. [T-matrix 截断与计算量](09-truncation-computation.md)
10. [部分已知 Q 与新题校准](10-partial-information.md)
11. [可识别性、标签交换与反例](11-identifiability.md)
12. [模拟实验共同设计与三个 Q](12-simulation-design.md)
13. [Table 1：样本量、属性数与恢复率](13-main-simulation-results.md)
14. [Figures 1--2 与 4.5% 早停](14-early-stopping.md)
15. [Table 3：相关且不均衡的属性](15-correlated-attributes.md)
16. [Table 4：单道新题校准](16-partial-information-results.md)
17. [模型验证、样本量与证据边界](17-model-validation.md)
18. [公开代码状态与实现精读](18-code-implementation.md)
19. [本站可计算复现](19-computational-reproduction.md)
20. [局限、结论与未来工作](20-limitations-conclusion-future.md)
21. [符号表](21-symbol-table.md)
22. [总结与后续阅读](22-summary.md)
23. [参考文献与来源核对](references.md)

## 读完后应能回答

- \(T\)-matrix 的每一行和每一列分别代表什么？
- \(\boldsymbol\beta\) 为什么可以直接从作答矩阵计算？
- \(S(Q)\)、\(\widehat S(Q)\) 与 DINA 似然怎样分工？
- Algorithm 1 每轮为什么需要约 \(J2^K\) 次候选评价？
- 4.5% 早停为什么会在小样本下提高真 Q 恢复率？
- Table 1 的 94 与正文的 98 应怎样处理？
- 论文给出的理论保证依赖哪些额外条件？
- 这套方法能否从零发现属性含义？
