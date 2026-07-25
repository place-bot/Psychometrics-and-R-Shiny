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

- [BOBCAT](bobcat/index.md)：用双层优化从历史作答数据中学习自适应选题策略。

## BOBCAT 在 CAT 中的位置

传统 IRT-CAT 通常先估计能力，再按 Fisher 信息或后验不确定性选择下一题。BOBCAT 保留逐题交互的 CAT 流程，同时把选题准则改造成可由数据训练的策略：

\[
\Pi_\phi\!\left(x_i^{(t)}\right)
\longrightarrow
j_i^{(t)}.
\]

其中 \(x_i^{(t)}\) 汇总学生 \(i\) 截至第 \(t\) 步的作答历史，\(\Pi_\phi\) 输出下一题的分布或题号。新作答会立刻写回状态，随后重新运行策略，所以 BOBCAT 学到的是闭环选题规则。
