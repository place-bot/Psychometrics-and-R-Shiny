# NCAT：用神经强化学习学习逐题选题策略

NCAT（Neural Computerized Adaptive Testing）由 Zhuang 等人在 AAAI 2022 提出。它把 CAT 的逐题选题过程写成强化学习问题：系统读取当前学生已经答对和答错的题，估计每道候选题的长期价值，选择一道题；学生作答后，状态立即更新，系统再决定下一题。

\[
\text{当前作答历史 }s_t
\xrightarrow{Q_\phi}
\text{选择题目 }q_t
\xrightarrow{\text{学生作答 }a_t}
s_{t+1}.
\]

因此，NCAT 学到的是一个**闭环策略**。施测过程中每一步都会重新运行策略，后续题目取决于该学生刚刚给出的真实反馈。

!!! info "和“预先生成一整套题”有什么区别"

    NCAT 在训练时学习函数 \(Q_\phi(s,q)\)，部署时一次只选择一道题。学生在第 \(t\) 步的答案会进入 \(s_{t+1}\)，并改变第 \(t+1\) 步各候选题的 Q 值。论文中的 “fully adaptive” 指这种逐题反馈闭环。

## 一张图看完整流程

```text
历史学生日志
    │
    ├── 每个学生的 support 题：允许策略逐题选择并读取历史答案
    └── 每个学生的 query 题：只用于检验当前能力估计
             │
             ▼
答对/答错双通道状态 ──► NCAT Q 网络 ──► 下一道题
             ▲                              │
             │                              ▼
             └──────── 新作答 ◄──── 响应模型更新学生参数
                                            │
                                            ▼
                              query BCE 的相反数作为 reward
                                            │
                                            ▼
                                  经验回放与 TD 更新
```

这里有三个相互配合的对象：

| 对象 | 记号 | 作用 |
|---|---:|---|
| 响应模型 | \(M\) | 根据学生参数预测答对概率，并用已选题更新学生参数 |
| 选题网络 | \(Q_\phi\) | 根据当前作答历史给每道候选题计算长期价值 |
| 历史作答环境 | \(\mathcal D\) | 离线提供“若选到这道题，该学生当时答对还是答错” |

论文把 IRT、MIRT、NCDM 等学生响应模型统称为 CDM。本站沿用论文记号 \(M\)，同时在需要严格区分时使用“响应模型”这一更宽的说法。

## NCAT 的核心创新

NCAT 的推进发生在三个层面。

1. **目标层面**：用未选 query 题上的预测损失评价一段已选题是否真正帮助测量，并把所有测试步的 query 损失纳入目标。
2. **算法层面**：把逐题选题建模为 MDP，用 Q-learning 学习长期选题价值。
3. **表示层面**：把答对题和答错题分成两个通道，先做通道内的 Performance Learning，再做跨通道的 Contradiction Learning，以识别猜测、失误或知识结构不一致造成的反应组合。

## 推荐阅读路线

第一次读时按下面顺序即可：

1. [问题、CAT 与离线数据](01-cat-and-data.md)
2. [双层目标、MDP 与奖励](02-objective-and-mdp.md)
3. [Q-learning 与经验回放](03-q-learning.md)
4. [状态编码与双通道 attention](04-neural-encoder.md)
5. [训练与真实学生部署](05-training-and-deployment.md)
6. [完整手算示例](06-worked-example.md)

准备复现或研究时继续读：

- [实验设计、完整结果与结果分析](07-experiments.md)
- [官方代码精读与最小实现](08-implementation.md)
- [局限、方法比较与未来工作](09-limitations-comparison-future.md)
- [符号表与 FAQ](10-symbols-faq.md)

## 读完后应能回答的问题

- support/query 切分怎样把历史日志变成一个离线 CAT 环境？
- 为什么 query BCE 可以用来监督选题，而训练 reward 在部署时不需要计算？
- \(Q_\phi(s_t,q)\) 为什么既不是答对概率，也不是 Fisher 信息？
- 学生每回答一道题后，NCAT 怎样让下一道题随之改变？
- 双通道 attention 怎样表示答对、答错与二者之间的矛盾？
- 论文的结果支持哪些结论，哪些约束仍需另外处理？

## 与 BOBCAT 的衔接

[BOBCAT](../bobcat/index.md) 和 NCAT 都从历史作答数据学习逐题选题策略，也都用 held-out 题上的预测表现评价已选题。两者的训练路径不同：

- BOBCAT 对“选题后再适应学生参数”的双层计算求 meta-gradient；
- NCAT 把每次选题视为动作，以 query 预测损失构造 reward，用 Q-learning 学习累计回报。

更完整的逐项比较见[局限、方法比较与未来工作](09-limitations-comparison-future.md)。
