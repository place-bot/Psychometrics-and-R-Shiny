# de la Torre (2008) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jimmy de la Torre. *An Empirically Based Method of Q-Matrix Validation for the DINA Model: Development and Applications*. |
| 期刊 | *Journal of Educational Measurement*, 45(4), 343--362, 2008 |
| DOI | [10.1111/j.1745-3984.2008.00069.x](https://doi.org/10.1111/j.1745-3984.2008.00069.x) |
| 正式版本 | [Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1111/j.1745-3984.2008.00069.x) |
| 原文实现 | 论文报告使用 Ox 编程，没有给出代码下载地址 |
| 后续实现 | [CRAN `CDM::din.validate.qmatrix`](https://cran.r-project.org/package=CDM) |

## 一句话结论

先在暂定 Q 矩阵下拟合 DINA，再用同一组学生属性模式后验权重，把每道题按照候选 q-vector 重新分成“具备全部所需属性”和“至少缺一项”两组；候选向量的

\[
\widehat\delta_j=1-\widehat s_j-\widehat g_j
\]

越大，两组答对率分得越开。论文用逐步加属性的搜索、阈值 \(\varepsilon\) 和少量追加 EM 循环，将这个想法变成 Q 矩阵验证流程。

## 这篇论文解决的具体问题

许多 CDM 分析把专家给出的 Q 矩阵当作已知输入，只检查项目参数或反应残差。若某行 Q 写错：

- DINA 会把结构错误吸收到 guessing 与 slipping；
- 学生属性模式后验会随之偏移；
- 后续项目参数、属性分类和模型拟合判断都可能受到影响；
- 只看已经拟合出的 DINA 参数，很难知道问题来自题目参数、属性定义还是 Q 行。

de la Torre 提供了一个数据驱动的候选生成器：对每道题提出可能的 q-vector，并用题目区分度衡量该候选是否改善两组分离。作者反复强调，最终判断仍需结合题目内容、作答过程和领域专家意见。

## 论文贡献

1. 用候选 q-vector 下的 DINA 区分度 \(\delta\) 定义经验验证目标。
2. 从穷举 \(2^K-1\) 个候选，推导出最多检查 \(K(K+1)/2\) 个候选的顺序搜索。
3. 借助一次 EM 拟合产生的后验期望计数，避免为每个候选向量完整重估模型。
4. 用 \(\varepsilon\) 控制是否接受新增属性，并以全测验平均 guessing 与 slipping 选择候选 Q。
5. 用模拟、分数减法和 2003 NAEP 八年级数学数据展示该方法能保留、质疑或替换已有 Q 行。

## 推荐阅读顺序

1. [问题、贡献与证据边界](01-question-and-contribution.md)
2. [DINA、Q 矩阵与理想反应](02-dina-q-foundation.md)
3. [区分度指标与验证目标](03-delta-index.md)
4. [假想题与穷举搜索](04-hypothetical-exhaustive.md)
5. [顺序搜索算法](05-sequential-search.md)
6. [EM 后验期望计数](06-em-expected-counts.md)
7. [完整验证流程](07-complete-algorithm.md)
8. [阈值与最终决策](08-epsilon-and-decision.md)
9. [模拟实验设计](09-simulation-design.md)
10. [模拟结果与解释](10-simulation-results.md)
11. [分数减法数据与设计](11-fraction-data.md)
12. [分数减法结果与反例](12-fraction-results.md)
13. [NAEP 数据与设计](13-naep-data.md)
14. [NAEP 结果与题目案例](14-naep-results.md)
15. [代码库实现精读](15-code-implementation.md)
16. [可计算复现](16-computational-reproduction.md)
17. [局限、结论与未来工作](17-limitations-future.md)
18. [符号表](18-symbols.md)
19. [总结与后续阅读](19-summary.md)
20. [参考文献与来源边界](references.md)

## 读完后应能回答

- 为什么遗漏所需属性主要抬高 slip，加入无关属性主要抬高 guess？
- 为什么 \(\delta=1-s-g\) 可以比较候选 q-vector？
- 原文的顺序搜索怎样把候选数从指数级降到二次级？
- EM 后验怎样让候选参数重算无需反复完整拟合？
- \(\varepsilon\) 太小或太大分别造成什么风险？
- 论文的三个实验各自支持了哪些结论？
- 当前 `CDM` 包为何属于“穷举版后续实现”，与原文顺序搜索有什么差异？

