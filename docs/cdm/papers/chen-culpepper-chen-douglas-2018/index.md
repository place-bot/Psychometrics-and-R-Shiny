# Chen、Culpepper、Chen 与 Douglas（2018）阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Yinghan Chen, Steven Andrew Culpepper, Yuguo Chen & Jeffrey Douglas. *Bayesian Estimation of the DINA Q Matrix*. |
| 期刊 | *Psychometrika*, 83(1), 89--108 |
| DOI | [10.1007/s11336-017-9579-4](https://doi.org/10.1007/s11336-017-9579-4) |
| 在线发表与卷期 | 2017 年在线发表；2018 年 3 月收入第 83 卷第 1 期 |
| 数据 | Tatsuoka 分数减法数据，\(N=536\)、\(J=20\) |
| 原始补充代码 | [Yuguo Chen 的软件页](https://publish.illinois.edu/yuguo/software/)提供 C++、R 与 README |
| 后续 R 包 | [`tmsalab/edina`](https://github.com/tmsalab/edina)，当前代码实现受限 Gibbs 版本并增加模型诊断与 \(K\) 比较 |
| 本站核验 | [`tools/chen_et_al_2018_bayesian_q_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/chen_et_al_2018_bayesian_q_check.py) |

## 一句话结论

论文把未知 Q 矩阵直接放入 DINA 的贝叶斯层级模型，并把 MCMC 的状态空间限制在满足三条可识别条件的 Q 上；受限 Gibbs 在 \(K=4\) 的模拟中明显优于另外两种采样器，真实数据分析也保证最终估计的 Q 位于可识别空间。

整条计算链可以写成：

\[
Q^{(t-1)}
\longrightarrow
(\boldsymbol s^{(t)},\boldsymbol g^{(t)},\boldsymbol\alpha^{(t)},\boldsymbol\pi^{(t)})
\longrightarrow
Q^{(t)}\in\mathcal Q
\longrightarrow
\widehat Q.
\]

\(\mathcal Q\) 是可识别 Q 的离散集合。算法每轮先更新题目参数、学生属性模式和潜在类比例，再在 \(\mathcal Q\) 中更新 Q。

## 这篇论文最重要的三点

### 1. 探索性估计整张 Q

输入只需要二元作答矩阵和属性数 \(K\)。方法无需专家先给一张接近真值的 Q，也无需逐行围绕专家 Q 做局部修订。

### 2. 可识别性进入采样器本身

每一个保留下来的 Q 样本都满足：

1. 行置换后含两套 \(I_K\)；
2. 每个属性至少被三道题要求；
3. 每道题至少要求一个属性。

因此，后验采样不会访问论文所排除的不可识别状态。

### 3. 理论、实验与代码形成闭环

论文给出依赖提议的不可约性与对称性证明；模拟比较受限 MH、受限 Gibbs 和无约束 Gibbs；补充材料给出三种方法的 Rcpp 实现；后续 `edina` 包把受限 Gibbs 封装成可安装的 R 接口。

## 推荐阅读顺序

1. [研究问题、贡献与证据边界](01-question-and-contribution.md)
2. [与已有 Q 学习方法的关系](02-relation-to-prior-work.md)
3. [DINA 模型、数据与全部符号](03-model-and-notation.md)
4. [理想反应、题目反应函数与似然](04-dina-likelihood.md)
5. [完整贝叶斯层级模型](05-bayesian-hierarchy.md)
6. [各层先验与完整条件分布](06-priors-and-conditionals.md)
7. [Q 的三条可识别条件](07-identifiability-conditions.md)
8. [为什么把后验限制在可识别空间](08-identified-space.md)
9. [Q 的条件后验与均匀先验](09-q-posterior.md)
10. [三类候选生成器总览](10-proposal-overview.md)
11. [独立提议与 DS1](11-independence-and-ds1.md)
12. [DS2 分块依赖提议逐步拆解](12-ds2.md)
13. [Theorem 1：不可约性](13-irreducibility.md)
14. [Theorem 2：对称性与接受率](14-symmetry-and-acceptance.md)
15. [Metropolis-within-Gibbs 完整算法](15-metropolis-within-gibbs.md)
16. [受限 Gibbs 完整算法](16-constrained-gibbs.md)
17. [单个 \(q_{jk}\) 的条件概率推导](17-q-full-conditional.md)
18. [整张 Q 的后验众数与列置换](18-posterior-summary.md)
19. [Experiment：模拟设计](19-simulation-design.md)
20. [Experiment：Table 1 的全部结果](20-table1-results.md)
21. [Experiment：题目参数 MSE 与收敛](21-item-parameter-results.md)
22. [Experiment：分数减法数据与分析设计](22-fraction-data.md)
23. [Experiment：\(K=3\) 的逐题结果](23-fraction-k3.md)
24. [Experiment：\(K=4\) 的逐题结果](24-fraction-k4.md)
25. [原始补充材料代码精读](25-original-code.md)
26. [当前 `edina` 包代码精读](26-edina-package.md)
27. [本站可计算核验与代码审查发现](27-computational-check.md)
28. [局限、结论与未来工作](28-limitations-conclusion-future.md)
29. [参考文献、代码与数据来源](references.md)

## 读完后应能回答

- Q 为何需要两套单位阵？
- “每个属性至少三题”和“两套单位阵”怎样对应？
- \(p(Q)\propto I(Q\in\mathcal Q)\) 实际上规定了什么？
- DS2 在一个列块中固定哪些 0 和 1？
- 不可约性、对称性各自解决 MCMC 的哪个问题？
- MH 与受限 Gibbs 怎样共享同一目标后验？
- 为什么整张 Q 的众数要先消除列标签交换？
- \(K=4\) 时受限 Gibbs 的优势有多大？
- 真实数据中为何只拟合 \(K=3,4\)，没有直接使用专家的 8 属性 Q？
- 原始补充代码、2018 年论文与当前 `edina` 包有哪些实质差异？
