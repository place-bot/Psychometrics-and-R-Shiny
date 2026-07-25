# Xu (2017) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Gongjun Xu. *Identifiability of Restricted Latent Class Models with Binary Responses*. |
| 期刊 | *The Annals of Statistics*, 45(2), 675--707, 2017 |
| DOI | [10.1214/16-AOS1464](https://doi.org/10.1214/16-AOS1464) |
| 期刊页面 | [Project Euclid](https://projecteuclid.org/journals/annals-of-statistics/volume-45/issue-2/Identifiability-of-restricted-latent-class-models-with-binary-responses/10.1214/16-AOS1464.full) |
| 开放版本 | [arXiv:1603.04140](https://arxiv.org/abs/1603.04140) |
| 原文代码 | 论文没有报告公开代码库；本站提供可计算核验脚本 |

## 一句话结论

对论文定义的二分反应 Q-restricted latent class model，若 Q 矩阵经题目换序后含两个 \(I_K\) 块，并且剩余题目能把每个单属性类 \(\boldsymbol e_k\) 与零属性类 \(\boldsymbol 0\) 区分开，则项目参数矩阵 \(\Theta\) 与属性分布 \(\boldsymbol p\) 都具有**严格可识别性**。

## 论文主线

\[
\text{观测反应分布}
\Longleftrightarrow
T(Q,\Theta)\boldsymbol p
\overset{\mathrm{C1,C2}}{\Longrightarrow}
(\Theta,\boldsymbol p)\text{ 唯一}.
\]

其中：

- \(T(Q,\Theta)\) 收集“某个题目子集全部答对”的边际概率；
- C1 提供两套单属性锚定题；
- C2 让剩余题目区分 \(\boldsymbol 0\) 与每个 \(\boldsymbol e_k\)；
- 一个可逆的行变换 \(D(\boldsymbol\theta^*)\) 把选定的 \(T\)-矩阵元素消成零；
- 证明先识别零属性列，再识别单属性列，最后按属性个数归纳到全部 \(2^K\) 个潜在类。

## 推荐阅读顺序

1. [问题、贡献与证据边界](01-question-and-scope.md)
2. [RLCM 模型与局部独立](02-model-setup.md)
3. [Q 矩阵限制与单调性](03-q-restrictions.md)
4. [六类诊断模型如何进入框架](04-model-examples.md)
5. [严格可识别性的定义](05-identifiability.md)
6. [边际 \(T\)-矩阵](06-t-matrix.md)
7. [完整 Q 矩阵与理想反应](07-completeness.md)
8. [C1、C2 与三套 \(I_K\)](08-conditions-c1-c2.md)
9. [主定理与测验设计含义](09-main-theorem.md)
10. [命题 3：可逆平移变换](10-transform.md)
11. [证明步骤 1--2](11-proof-steps-one-two.md)
12. [证明步骤 3--5](12-proof-steps-three-five.md)
13. [两个技术引理](13-lemmas.md)
14. [C1 单独不够的反例](14-counterexample.md)
15. [从可识别性到一致性](15-consistency.md)
16. [原文证据与 Experiment 边界](16-experiment-and-evidence.md)
17. [代码实现与可计算核验](17-computational-check.md)
18. [局限、后续修正与未来工作](18-limitations-and-future.md)
19. [符号表](19-symbols.md)
20. [总结与后续阅读](20-summary.md)
21. [参考文献](references.md)

## 阅读时反复区分的四件事

| 层面 | 论文中的对象 | 能回答的问题 |
| --- | --- | --- |
| 观测层 | \(P(\boldsymbol R=\boldsymbol r)\) | 无限样本下可以知道什么 |
| 潜在层 | \(\boldsymbol\alpha\in\{0,1\}^K\) | 学生属于哪个属性模式 |
| 参数层 | \(\Theta,\boldsymbol p\) | 项目反应规律与群体组成能否唯一恢复 |
| 设计层 | \(Q\)、C1、C2 | 哪些测验结构保证参数唯一 |

这篇论文研究群体模型的参数识别。它没有研究 CAT 的逐人实时选题，也没有提供项目选择准则。它对 CAT 的价值位于反应模型与题库设计这一层：若底层诊断模型缺乏可识别性，再精细的 adaptive policy 也可能建立在无法唯一估计的学生模型之上。
