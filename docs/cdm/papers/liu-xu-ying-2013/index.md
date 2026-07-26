# Liu、Xu 与 Ying（2013）阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jingchen Liu, Gongjun Xu & Zhiliang Ying. *Theory of Self-Learning Q-Matrix*. |
| 期刊 | *Bernoulli*, 19(5A), 1790--1817 |
| DOI | [10.3150/12-BEJ430](https://doi.org/10.3150/12-BEJ430) |
| 收稿与修回 | 2011 年 3 月收稿，2011 年 11 月修回 |
| 开放全文 | [PubMed Central, PMC4011940](https://pmc.ncbi.nlm.nih.gov/articles/PMC4011940/)；[arXiv:1010.6120](https://arxiv.org/abs/1010.6120) |
| 原文代码 | 论文没有给出代码仓库、软件包、模拟程序或数据文件 |
| 本站核验 | [`tools/liu_xu_ying_2013_theory_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/liu_xu_ying_2013_theory_check.py) |

## 一句话结论

论文证明：在完整 Q、饱和 \(T\)-matrix、所有属性模式都有正概率、每个属性至少被两道题要求等条件下，响应数据足以把真 Q 的**列置换等价类**与其他候选 Q 分开；用经验联合答对率最小化距离，便能随着样本量增大以概率趋近 1 恢复这个等价类。

核心映射可以压缩成：

\[
Q
\longrightarrow
T_{c,g}(Q)
\longrightarrow
T_{c,g}(Q)\boldsymbol p+p_0\boldsymbol g
\longrightarrow
\boldsymbol\alpha .
\]

其中 \(\boldsymbol\alpha\) 由作答数据直接计算，\(\boldsymbol p\) 是属性模式分布。真 Q 能生成 \(\boldsymbol\alpha\) 的总体极限；任何不等价候选 Q 的列空间与该极限保持正距离，这一“列空间分离”构成一致性证明的核心。

## 这篇论文解决了什么

| 问题 | 论文给出的处理 |
| --- | --- |
| Q 的属性列名称可交换 | 把目标定义为恢复 \(Q\) 的列置换等价类 |
| Q 位于离散的二元矩阵空间 | 穷举候选 Q，并为每个候选剖面化属性分布 |
| 潜在属性不可观测 | 用单题与题组联合答对率组成 \(\boldsymbol\alpha\) |
| DINA 有失误与猜测 | 构造 \(T_{c,g}(Q)\)，再用线性变换消去已知 \(\boldsymbol g\) |
| 掌握者正确率 \(c_i\) 未知 | 对可直接识别的 \(c_i\) 用矩估计，其余分量用剖面优化 |
| 估计是否会收敛到真 Q | 分无噪声、已知 \(c,g\)、未知 \(c\) 三层给出一致性定理 |

## 推荐阅读顺序

1. [问题、创新与 2012 论文的关系](01-question-contribution-and-2012.md)
2. [基础模型、样本与全部对象](02-model-setup.md)
3. [理想反应、B-vector 与 T-matrix](03-ideal-response-and-tmatrix.md)
4. [经验矩 \(\boldsymbol\alpha\) 与总体映射](04-alpha-and-moment-map.md)
5. [目标函数、Q 估计量与计算](05-objective-and-estimator.md)
6. [三题两属性完整手算](06-worked-example.md)
7. [列置换等价、完整性与饱和性](07-equivalence-completeness-saturation.md)
8. [C1--C5：每个条件在控制什么](08-conditions-c1-c5.md)
9. [Theorem 2.4：无噪声一致性](09-theorem-2-4.md)
10. [已知失误与猜测参数的 DINA](10-known-cg-dina.md)
11. [噪声 T-matrix 与目标函数](11-noisy-tmatrix-objective.md)
12. [Theorem 3.1：已知 \(c,g\) 的一致性](12-theorem-3-1.md)
13. [未知 \(c\)：一般估计与矩估计](13-unknown-c-estimation.md)
14. [组合估计量与 Theorem 4.2](14-combined-estimator-theorem-4-2.md)
15. [全部证明的总路线](15-proof-roadmap.md)
16. [Propositions 6.1--6.2：满列秩](16-full-rank-propositions.md)
17. [Propositions 6.3--6.6：列空间分离](17-column-space-separation.md)
18. [Lemma 6.7 与消去猜测的矩阵 \(D\)](18-guessing-removal-transform.md)
19. [三个主定理的证明](19-main-theorem-proofs.md)
20. [附录证明与 C5 的关键作用](20-appendix-and-c5.md)
21. [反例、必要性与识别边界](21-counterexamples-and-boundaries.md)
22. [饱和矩、搜索复杂度与实用截断](22-computation-and-truncation.md)
23. [Experiment：原文证据的完整盘点](23-experiment-and-evidence.md)
24. [代码状态与实现精读](24-code-implementation.md)
25. [本站可计算核验](25-computational-check.md)
26. [局限、结论与未来工作](26-limitations-conclusion-future.md)
27. [符号表](27-symbol-table.md)
28. [总结与后续阅读](28-summary.md)
29. [参考文献与来源核对](references.md)

## 读完后应能回答

- \(T(Q)\) 的行、列和数值各代表什么？
- 为什么无噪声情形排除全零属性列，而有猜测时需要把它补回来？
- Q 的“可识别”为什么只能精确到列置换？
- C1--C5 分别进入了哪一步证明？
- \(\boldsymbol\alpha\) 怎样通过大数定律接近总体矩？
- 满列秩与列空间分离分别解决唯一性和排错中的哪一个问题？
- 矩阵 \(D\) 怎样把 \(T_{c,g}(Q)\) 化成 \(T_{c-g}(Q)\)？
- Theorem 4.2 为什么能保证 Q 一致，却还不能自动保证 \(\boldsymbol p\) 一致？
- 原文为何没有实验结果页，本站的数值核验能支持到什么程度？
