# Deep RL 自适应学习：连续能力、DQN 与学习路径

本专题精读 Xiao Li、Hanchen Xu、Jinming Zhang 与 Hua-hua Chang 的论文 **Deep Reinforcement Learning for Adaptive Learning Systems**。论文研究的核心循环是：

\[
\text{测量当前能力}
\longrightarrow
\text{选择一份学习材料}
\longrightarrow
\text{学生学习并发生能力变化}
\longrightarrow
\text{重新测量并再次选择}.
\]

系统每轮只决定当前材料。学习后的新能力会反馈给策略，因此同一位学生在不同反馈下会走向不同路径。

## 文献身份

| 阶段 | 文献信息 |
|---|---|
| 预印本 | arXiv:2004.08410，2020 年 4 月 17 日提交 |
| 在线发表 | *Journal of Educational and Behavioral Statistics*，2022 年 11 月 3 日 |
| 正式卷期 | 2023 年 4 月，48(2), 220–243 |
| DOI | [10.3102/10769986221129847](https://doi.org/10.3102/10769986221129847) |

用户提供的 TeX 所解释的式 (3)–(8) 与 2020 年 arXiv 初稿完全对应。初稿首页标有 “Psychometrika Submission”，但最终发表期刊是 *Journal of Educational and Behavioral Statistics*。本站在讲公式时保留初稿编号，引用文献信息时使用正式发表版本。

## 一张图看论文

```text
作答数据
   │
   ▼
IRT / MIRT 能力估计器 ──────────────┐
   │ 当前连续能力 s_t              │
   ▼                              │
DQN 给每份材料计算 Q(s_t, a)       │
   │ ε-greedy 选材料 a_t           │
   ▼                              │
真实学生或转移模型 ψ(s_t, a_t)     │
   │                              │
   ├── 产生下一能力 s_{t+1} ───────┘
   └── 未达到目标得 -1，到达目标得 0
```

论文包含两条相互配合的学习线：

1. **策略线**：DQN 从转移样本中学习长期动作价值，并逐步形成材料选择策略。
2. **模型线**：神经网络学习状态转移 \(s_{t+1}\approx\psi(s_t,a_t)\)，再用虚拟学生扩大策略训练数据。

## 核心研究问题

论文要回答四个问题：

1. 连续潜在能力能否作为自适应学习的状态？
2. 学生学习转移未知时，DQN 能否直接从交互数据学到材料选择策略？
3. 学生人数不足时，能否先学习转移模型，再用虚拟交互提高数据效率？
4. 能力估计含有噪声时，策略是否仍有优势？

## 与 NCAT 的位置关系

这篇论文的动作是**学习材料**，目标是改变学生能力；[NCAT](../ncat/index.md) 的动作是**测试题目**，目标是用更少题准确测量学生。两者都采用逐步反馈与 Q-learning，但状态转移含义不同：

| 维度 | 本文自适应学习 | NCAT |
|---|---|---|
| 动作 | 教材、视频、练习或教学支持 | 一道测试题 |
| 主要变化 | 学生的真实知识与能力 | 系统掌握的作答证据 |
| 目标 | 尽快达到学习目标 | 尽快提高测量质量 |
| 每步反馈 | 学习后测得的新能力 | 当前题的答对/答错 |
| 论文实验 | 人工转移模型上的模拟 | 真实作答日志上的离线 CAT |

CAT 在本文系统中承担测量组件：每轮学习后可用一段短 CAT 估计潜在能力，再把估计值交给材料推荐策略。

## 推荐阅读路线

第一次阅读：

1. [论文问题、贡献与发表版本](01-publication-and-problem.md)
2. [测量模型、能力状态与假设](02-measurement-and-assumptions.md)
3. [MDP、Q 函数与 Bellman 方程](03-mdp-foundations.md)
4. [把自适应学习写成 MDP](04-adaptive-learning-mdp.md)
5. [从 Bellman 方程到 DQN](05-bellman-and-dqn.md)
6. [深度 Q-learning 完整算法](06-deep-q-learning-algorithm.md)
7. [转移模型估计器与虚拟学生](07-transition-model-estimator.md)

准备复现或研究时继续阅读：

- [完整手算与逐步反馈](08-worked-example.md)
- [模拟环境与实验设计](09-simulation-design.md)
- [实验结果与证据边界](10-results-and-analysis.md)
- [实现蓝图与检查清单](11-implementation-blueprint.md)
- [局限、CAT 接口与未来工作](12-limitations-cat-comparison-future.md)
- [符号表、结论与阅读地图](13-symbols-summary.md)
