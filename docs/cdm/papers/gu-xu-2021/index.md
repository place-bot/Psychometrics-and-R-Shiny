# Gu 与 Xu（2021）阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Yuqi Gu & Gongjun Xu. *Sufficient and Necessary Conditions for the Identifiability of the Q-matrix* |
| 期刊 | *Statistica Sinica*, 31, 449--472 |
| DOI | [10.5705/ss.202018.0410](https://doi.org/10.5705/ss.202018.0410) |
| 正式论文 | [期刊页面](https://www3.stat.sinica.edu.tw/statistica/j31n1/j31n118/j31n118.html) · [24 页 PDF](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A31n118.pdf) |
| 主文与补充材料 | [arXiv:1810.03819](https://arxiv.org/abs/1810.03819)，共 83 页，含全部证明和 Simulation Studies I--VII |
| 官方代码 | [`yuqigu/Identify_Q`](https://github.com/yuqigu/Identify_Q)，MATLAB 条件检查器与模拟代码 |
| 本站核验 | [`tools/gu_xu_2021_identifiability_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/gu_xu_2021_identifiability_check.py) |

## 一句话结论

当 \(Q\) 也未知时，DINA 模型中 \(Q\)、失误参数、猜测参数和潜类比例能够严格联合识别，当且仅当 \(Q\) 同时满足完整性 A、去掉一套单位阵后的列互异性 B，以及每个属性至少出现三次的重复性 C。

论文同时说明了两层更细的边界：

- DINA 的泛识别可以在个别属性只被两题测量时成立，结论取决于两题的 \(q\)-向量形状和潜类比例是否落在零测集上；
- 一般 RLCM 的泛识别可用“两块泛完整子矩阵＋剩余题覆盖全部属性”的 D/E 条件保证。

## 这篇论文回答了什么

```text
观测反应分布
      │
      ├── 能否恢复已知 Q 下的题目参数与潜类比例？
      │
      └── 当 Q 也未知时，能否同时恢复 Q、题目参数与潜类比例？
                         │
                         ├── 严格识别：所有合法参数点均唯一
                         └── 泛识别：除零测集外几乎处处唯一
```

本文解决第二个问题。它和 Gu 与 Xu 关于“已知 \(Q\) 的 DINA 参数识别”论文共享 A/B/C 条件名称，研究对象和结论强度均有差别。

## 推荐阅读顺序

1. [研究问题、贡献与证据边界](01-question-contribution.md)
2. [与已有识别结果的关系](02-prior-work.md)
3. [RLCM 数据生成过程与全部对象](03-rlcm-setup.md)
4. [DINA、G-DINA 与一般 RLCM](04-dina-gdina.md)
5. [严格识别、泛识别与列标签交换](05-identifiability-definitions.md)
6. [四题两属性的泛识别例子](06-q42-generic-example.md)
7. [T-matrix 与识别等价式](07-t-matrix.md)
8. [零行、单调性和等价关系](08-preliminaries.md)
9. [Theorem 1：A/B/C 必要且充分](09-theorem1-overview.md)
10. [Condition A：完整性](10-condition-a.md)
11. [Condition B：\(Q^\star\) 的列互异](11-condition-b.md)
12. [Condition C：每个属性至少三次](12-condition-c.md)
13. [最少题数与 \(K=8,J=12\) 构造](13-minimum-items.md)
14. [Theorem 1 的证明路线](14-theorem1-proof.md)
15. [Theorem 2：只测两次时的三种结构](15-theorem2.md)
16. [\(K=2\) 的完整泛识别刻画](16-k2-characterization.md)
17. [一般 RLCM 中重复性的必要性](17-general-rlcm-theorem3.md)
18. [泛完整性与二分图匹配](18-generic-completeness.md)
19. [Theorem 4：D/E 泛识别条件](19-theorem4.md)
20. [Theorem 5 与 \(K=2\) 必要充分条件](20-theorem5.md)
21. [有限样本误差界](21-finite-sample.md)
22. [Experiment：主文泛识别模拟](22-main-simulation.md)
23. [Experiment：补充材料共同设计](23-supplement-design.md)
24. [Experiment：DINA Studies I--II](24-studies1-2.md)
25. [Experiment：DINA Studies III--IV](25-studies3-4.md)
26. [Experiment：G-DINA Study V](26-study5.md)
27. [Experiment：G-DINA Studies VI--VII](27-studies6-7.md)
28. [官方条件检查代码精读](28-code-condition-checkers.md)
29. [官方模拟代码精读](29-code-simulations.md)
30. [本站可计算核验与代码审查](30-computational-check.md)
31. [局限、结论与未来工作](31-limitations-conclusion-future.md)
32. [符号表](32-symbol-table.md)
33. [参考文献与来源](references.md)

## 读完后应能回答

- 为什么“已知 \(Q\) 的参数识别”和“未知 \(Q\) 的联合识别”是两个问题？
- A、B、C 分别排除哪一种观测等价？
- 为什么 DINA 的严格识别只需一套 \(I_K\)，仍能少于 \(2K+1\) 道题？
- 四题两属性例子中，\(p_{00}p_{11}=p_{01}p_{10}\) 为何等价于两个属性独立？
- 局部泛识别、全局泛识别和严格识别如何排序？
- 一般 RLCM 中的“泛完整”为什么可以写成二分图完美匹配？
- 七组模拟各自在核验充分性、必要性还是零测集现象？
- 官方 MATLAB 代码的判断逻辑、计算瓶颈和注释偏差在哪里？
