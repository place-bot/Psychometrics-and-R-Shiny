# BOBCAT 阅读导引

BOBCAT（Bilevel Optimization-Based Computerized Adaptive Testing）是 CAT 栏目下的一种数据驱动选题方法。它把每名学生的短测适应过程放在内层，把未用于适应的题目预测表现放在外层，并联合学习响应模型与选题策略。

## 一句话主线

\[
\underbrace{\text{策略逐题选题}}_{\phi}
\longrightarrow
\underbrace{\text{根据已选作答适应学生参数}}_{\theta_i^*}
\longrightarrow
\underbrace{\text{预测留出的 meta 题}}_{\mathcal L}
\longrightarrow
\underbrace{\text{更新全局模型与策略}}_{\gamma,\phi}.
\]

部署时，这条链仍然逐题运行：第 \(t\) 题的真实作答进入状态后，系统才选择第 \(t+1\)
题。因此，论文中的“学习选题算法”具有实时自适应性；整条题序会随作答逐步展开。

## 推荐阅读顺序

1. [基础准备](01-foundations.md)：CAT、IRT、响应模型、状态和 meta-learning 的基础概念。
1. [双层优化](02-bilevel.md)：先独立理解 outer/inner problem 和 meta-gradient。
1. [Framework 与算法](03-framework.md)：逐字母解释论文公式和三类选题算法。
1. [手算示例](04-worked-example.md)：用小题库走完一次 BOBCAT 流程。
1. [实验、结论与未来工作](05-experiments.md)：数据、比较方法、指标、全部主要结果及其边界。
1. [符号与推导](06-symbols-and-derivations.md)：查符号、维度和关键导数。
1. [官方代码精读](07-implementation.md)：把论文公式逐段映射到 `arghosh/BOBCAT`。
1. [总结](08-summary.md)：快速回顾整篇论文。
1. [参考文献](references.md)：论文及相关方法来源。

## 阅读时始终抓住三个对象

| 对象 | 论文记号 | 它回答的问题 |
| --- | --- | --- |
| 全局响应模型 | \(\gamma\) | 学生和题目的共同响应规律怎样表示？ |
| 学生局部参数 | \(\theta_i\) | 看过当前短测作答后，怎样表征学生 \(i\)？ |
| 选题策略 | \(\Pi_\phi\) | 给定当前作答历史，下一题选哪一道？ |

外层 meta loss 把三者串在一起：一组题的价值取决于它能否帮助局部模型预测该学生其余题目的作答。
