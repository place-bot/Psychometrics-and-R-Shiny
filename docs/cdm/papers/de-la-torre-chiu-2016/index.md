# de la Torre & Chiu (2016) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jimmy de la Torre & Chia-Yi Chiu. *A General Method of Empirical Q-matrix Validation*. |
| 期刊 | *Psychometrika*, 81(2), 253--273, June 2016 |
| DOI | [10.1007/s11336-015-9467-8](https://doi.org/10.1007/s11336-015-9467-8) |
| 正式版本 | [Cambridge Core](https://www.cambridge.org/core/journals/psychometrika/article/general-method-of-empirical-qmatrix-validation/678D0AF47D7F25FE8C5899AC12554690) |
| 在线发表 | 6 May 2015 |
| 原文实现 | 论文报告使用 Ox；正文没有给出代码下载地址 |
| 后续实现 | [`GDINA::Qval()`](https://wenchao-ma.github.io/GDINA/reference/Qval.html) |

## 一句话结论

给定一道题在全部属性模式下的答对概率，把考生按照候选 q-vector 划成若干组；组间答对概率的加权方差越大，该候选保留的题目区分信息越多。论文把这个方差记为

\[
\varsigma_j^2(\boldsymbol q)
=
\sum_{\boldsymbol\alpha_{\boldsymbol q}}
w(\boldsymbol\alpha_{\boldsymbol q})
\left[
p_j(\boldsymbol\alpha_{\boldsymbol q})-\bar p_j
\right]^2,
\]

再以

\[
\operatorname{PVAF}_j(\boldsymbol q)
=
\frac{\widehat{\varsigma}_j^2(\boldsymbol q)}
{\widehat{\varsigma}_j^2(\boldsymbol 1)}
\]

衡量候选保留了饱和分组的多少方差。达到阈值的候选中，所需属性最少者成为建议 q-vector。

## 论文在 2008 年方法上推进了什么

| de la Torre (2008) | de la Torre & Chiu (2016) |
| --- | --- |
| DINA 两组：\(\eta=0,1\) | G-DINA 的多个约化属性组 |
| 指标 \(\delta=1-s-g\) | 指标 \(\varsigma^2\)：组间成功概率方差 |
| 每轮增加一个属性 | 穷举 \(2^K-1\) 个非零 q-vector |
| \(\varepsilon\) 是相邻两步的 \(\delta\) 增量 | \(\varepsilon\) 是饱和 GDI 的保留比例 |
| 理论主要依靠 DINA 结构 | 用两个引理和一个定理覆盖 G-DINA 家族 |

两篇论文中的 \(\varepsilon\) 含义不同，数值也不能直接互换。

## 推荐阅读顺序

1. [研究问题、贡献与边界](01-question-and-contribution.md)
2. [G-DINA 基础与约化属性模式](02-gdina-foundation.md)
3. [五种成功概率剖面](03-response-profiles.md)
4. [后验权重、折叠分组与条件均值](04-weights-and-collapsing.md)
5. [GDI 的定义与统计解释](05-gdi-definition.md)
6. [Table 1 完整手算与原文排版错误](06-table1-worked-example.md)
7. [appropriate 与 correct q-vector](07-appropriate-correct-q.md)
8. [两个引理、主定理与证明](08-lemmas-and-theorem.md)
9. [PVAF 穷举搜索与阈值](09-pvaf-search.md)
10. [完整估计与验证算法](10-complete-algorithm.md)
11. [模拟实验的共同设计](11-simulation-design.md)
12. [Study 1：五种约化模型](12-study1-results.md)
13. [Study 2：无约束 G-DINA](13-study2-results.md)
14. [分数减法真实数据](14-fraction-data.md)
15. [真实数据结果与逐题解释](15-fraction-results.md)
16. [原文 Ox 与 `GDINA::Qval()` 代码精读](16-code-implementation.md)
17. [本站可计算复现](17-computational-reproduction.md)
18. [一致性评论、回应与方法定位](18-consistency-debate.md)
19. [局限、结论与未来工作](19-limitations-future.md)
20. [符号表](20-symbols.md)
21. [总结与后续阅读](21-summary.md)
22. [参考文献与来源边界](references.md)

## 读完后应能回答

- \(\varsigma^2\) 为什么就是条件期望的方差？
- 遗漏所需属性为何只能降低或保持 GDI？
- 加入无关属性为何可以与正确 q-vector 的 GDI 完全相同？
- PVAF 阈值和最简性规则怎样共同选出一行 Q？
- 后验权重 \(w\) 和完整属性模式成功率 \(p_j(\boldsymbol\alpha)\) 怎样从初始 Q 中估计？
- 论文的两组模拟分别检验了什么？
- 固定 \(\varepsilon=.95\) 在有限样本表现和渐近相合性之间有什么张力？
- 当前 `GDINA` 包在哪些地方延伸了原始算法？
