# 计算机化自适应测验（CAT）

计算机化自适应测验（Computerized Adaptive Testing, CAT）根据考生此前的作答，逐步决定下一道题。它的核心循环是：

\[
\text{当前作答历史}
\longrightarrow
\text{更新考生状态}
\longrightarrow
\text{从剩余题库选择下一题}
\longrightarrow
\text{获得新作答}.
\]

因此，CAT 的试卷在施测前通常没有完全固定。两名考生即使从相同起点出发，只要某一步的答案不同，后续题目就可能分叉。这种“每作答一次便重新决策”的闭环，是理解 CAT 与一次性生成整套推荐序列差异的关键。

## 本栏目怎样组织

本站将 CAT 作为与 CDM 同级的主题。每一种具体方法在 CAT 下建立独立子模块，便于后续继续加入传统 Fisher 信息选题、认知诊断 CAT、约束 CAT 和生成式 CAT 等内容。

当前已收录：

- [Adaptive Testing with Self-Evaluation](adaptive-testing-self-evaluation/index.md)：让受测者的自我判断参与选题或初始化，研究这种额外信息能否改善 CAT 的冷启动、测验体验与效率。
- [BOBCAT](bobcat/index.md)：用双层优化从历史作答数据中学习自适应选题策略。
- [NCAT](ncat/index.md)：把逐题选题写成强化学习问题，用双通道 attention 和 Q-learning 学习长期选题价值。
- [Deep RL 自适应学习](adaptive-learning-drl/index.md)：把连续潜在能力作为状态、学习材料作为动作，用 DQN 学习闭环教学路径，并用转移模型提高小样本数据利用率。

## 两种数据驱动方法在 CAT 中的位置

传统 IRT-CAT 通常先估计能力，再按 Fisher 信息或后验不确定性选择下一题。BOBCAT 保留逐题交互的 CAT 流程，同时把选题准则改造成可由数据训练的策略：

\[
\Pi_\phi\!\left(x_i^{(t)}\right)
\longrightarrow
j_i^{(t)}.
\]

其中 \(x_i^{(t)}\) 汇总学生 \(i\) 截至第 \(t\) 步的作答历史，\(\Pi_\phi\) 输出下一题的分布或题号。新作答会立刻写回状态，随后重新运行策略，所以 BOBCAT 学到的是闭环选题规则。

NCAT 使用同样的逐题反馈结构，并把长期选题价值写成 Q 函数：

\[
Q_\phi(s_t,\cdot)
\longrightarrow
q_t
\longrightarrow
a_t
\longrightarrow
s_{t+1}.
\]

它以 held-out query 题上的预测损失构造 reward，通过 Q-learning 训练策略；答对题和答错题由双通道 attention 编码。BOBCAT 与 NCAT 都会在每个真实答案到达后重新选择下一题，差别主要在训练目标的求解方法和状态表示。

Deep RL 自适应学习研究外层教学决策。材料会改变学生能力，学习后通过测试或 CAT 重新估计能力，再选择下一份材料。它与 NCAT 都使用 Q-learning，但前者优化达成学习目标所需的路径，后者优化测量质量。
