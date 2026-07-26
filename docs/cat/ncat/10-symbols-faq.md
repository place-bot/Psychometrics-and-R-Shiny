# 符号表与 FAQ

## 1. 核心符号

| 符号 | 含义 |
|---|---|
| \(i\) | 学生索引 |
| \(t\) | CAT 测试步 |
| \(T\) | 最大测试长度 |
| \(q_j\) | 第 \(j\) 道题 |
| \(\mathcal J\) | 完整题库 |
| \(\mathcal A_i^t\) | 学生 \(i\) 在第 \(t\) 步的合法动作集合 |
| \(a_{i(t)}\) | 学生 \(i\) 在第 \(t\) 步的二元答案 |
| \(\theta_i^0\) | 学生真实但未知的能力/知识状态 |
| \(\widehat\theta_i^{\,t}\) | 用前 \(t\) 道已选题估计的学生参数 |
| \(M(q\mid\theta)\) | 响应模型预测的答对概率 |
| \(\mathcal D_i^s\) | 学生 \(i\) 的 support 题与答案 |
| \(\mathcal D_i^u\) | 学生 \(i\) 的 query 题与答案 |
| \(\mathcal D_i^s(t)\) | 截至第 \(t\) 步实际已选的 support 记录 |
| \(s_t\) | 第 \(t\) 步决策前的作答历史状态 |
| \(\pi\) | 选题策略 |
| \(\phi\) | Q 网络参数 |
| \(Q_\phi(s,q)\) | 状态 \(s\) 下先选题 \(q\) 的预计长期价值 |
| \(r_t\) | 第 \(t\) 步 reward |
| \(\gamma\) | 未来 reward 折扣因子 |
| \(\varepsilon\) | epsilon-greedy 的训练探索概率 |
| \(\nu_t\) | 测试时 softmax 温度 |
| \(\mathcal B\) | replay buffer |
| \(d_t\) | transition 是否终止的指示量 |
| \(y_t\) | TD target |
| \(E^0,E^1\) | 答错与答对题目的 embedding 表 |
| \(\mathbf F_t^0,\mathbf F_t^1\) | 两个 Performance Learning 输出 |
| \(A,\widetilde A^0,\widetilde A^1\) | contradiction 分数及两个归一化矩阵 |
| \(\mathbf u_t\) | 四路池化后拼接的状态向量 |

## 2. 常见 shape

设 batch size 为 \(B\)，最长答错/答对序列长度为 \(L_0,L_1\)，embedding 维度为 \(d\)，题数为 \(J\)。

| 张量 | shape |
|---|---:|
| 答错题 ID | \(B\times L_0\) |
| 答对题 ID | \(B\times L_1\) |
| 答错 embedding | \(B\times L_0\times d\) |
| 答对 embedding | \(B\times L_1\times d\) |
| cross score | \(B\times L_0\times L_1\) |
| 四路拼接状态 | \(B\times4d\) |
| 所有题 Q 值 | \(B\times J\) |
| 动作题号 | \(B\) |
| reward / done / target | \(B\) |

## 3. NCAT 每次生成整套试卷吗？

每次决策只输出下一道题。得到学生实时答案后更新状态，再输出下一道题。因此最终序列是学生与策略交互生成的。

## 4. 训练完成后策略参数不更新，为什么仍然 adaptive？

因为输入状态实时改变：

\[
Q_\phi(s_t,\cdot)
\longrightarrow
Q_\phi(s_{t+1},\cdot).
\]

同一组固定参数对不同作答历史产生不同题目排序。

## 5. Q 值是答对概率吗？

Q 值是选择某题后的折扣累计 reward 估计。答对概率由响应模型 \(M(q\mid\theta)\) 给出。

## 6. 为什么还需要 IRT 或 NCDM？

NCAT 负责决定问哪道题；响应模型负责把已观察答案转换成学生参数，并在 query 题上计算预测损失。二者分工不同。

## 7. 为什么 query 题不能参与学生更新？

query 是 held-out 评价集。若它同时参与学生参数拟合，外层损失会发生信息泄漏，无法评价已选 support 题的泛化价值。

## 8. 部署时没有 query 答案，怎样计算 reward？

部署时不计算训练 reward。策略已经在离线阶段学到状态-动作价值，上线只需当前真实作答和训练好的网络。

## 9. 第一题对每个学生都一样吗？

在无学生协变量、同一空状态、同一可用题集合且使用确定性 argmax 时，第一题相同。温度采样、不同可用集、先验信息或人口学/历史协变量都可能使第一题不同。

## 10. 为什么把答对和答错分通道？

两个反应类型的频率和含义不同。分通道可分别建模同类反应，再用 cross-attention 比较相关题上的不一致。

## 11. Contradiction Learning 能直接识别猜测和失误吗？

它学习与这些现象相符的反应矛盾表示。attention 分数本身不是经校准的 guess/slip 概率。需要带真值的模拟、外部标注或专门的潜变量模型才能做更强识别。

## 12. 平均池化会丢失作答顺序吗？

会。论文采用短测期间能力稳定、顺序不重要的假设。若存在学习、疲劳或时间效应，应加入位置、时间和反馈信息。

## 13. epsilon、gamma、temperature 有什么区别？

- \(\varepsilon\)：训练时随机探索动作；
- \(\gamma\)：TD target 中未来 reward 的权重；
- \(\nu_t\)：测试时 Q 值 softmax 的平滑程度。

## 14. 温度采样能保证曝光安全吗？

它能分散路径并降低论文中的平均曝光，但不保证任何一道题低于指定最大曝光率。硬配额或接受/拒绝控制仍需单独实现。

## 15. NCAT 自动满足内容平衡吗？

论文观察到知识点覆盖增长较快，但没有蓝图约束。内容上下限应通过动作 mask、约束 reward 或 shadow test 明确加入。

## 16. 为什么 reward 常为负数？

论文使用 query BCE 的相反数：

\[
r_t=-L_t\le0.
\]

损失越小，reward 越接近 0，Q 值越大。

## 17. 为什么每一步都算 query loss？

CAT 可能在不同长度停止。把各步损失都纳入目标，可以训练较早阶段也有效的选题策略。

## 18. 折扣因子小于 1 会改变论文目标吗？

会。论文外层式对每一步等权；折扣回报更重视早期 reward。复现时应明确该近似并做 \(\gamma\) 敏感性分析。

## 19. 为什么离线候选题限制在学生答过的题？

环境只有这些题的真实历史答案，可以模拟选中后的状态转移。未答题的反事实结果未知。

## 20. 怎样支持新题？

原模型的 embedding 和输出层绑定固定题号。可改为状态编码器与题目内容编码器的匹配函数，并用题目参数、知识点和文本语义表示新题。

## 21. NCAT 与 BOBCAT 最核心的算法差别是什么？

BOBCAT通过双层优化的 meta-gradient 学策略；NCAT通过 reward、Bellman target 和 TD 更新学 Q 函数。两者都在每次新作答后重新决定下一题。

## 22. 复现时最先检查什么？

优先检查：

1. 学生级数据泄漏；
2. support/query 泄漏；
3. 当前与下一状态动作 mask；
4. `done` 的 bootstrap；
5. padding mask；
6. 响应模型学生参数的重置语义；
7. 论文配置与仓库配置差异；
8. 多随机种子和每折结果。

## 23. 中英术语

| English | 中文 |
|---|---|
| computerized adaptive testing | 计算机化自适应测验 |
| response model | 响应模型 |
| cognitive diagnosis model | 认知诊断模型 |
| question selection algorithm | 选题算法 |
| support set | 支持集 / 适应集 |
| query set | 查询集 / 外层评价集 |
| state | 状态 |
| action | 动作 |
| reward | 奖励 |
| action-value function | 动作价值函数 |
| temporal-difference target | 时序差分目标 |
| replay buffer | 经验回放池 |
| performance learning | 表现学习 |
| contradiction learning | 矛盾学习 |
| exposure control | 曝光控制 |
| action mask | 动作掩码 |
| shadow test | 影子测验 |
| logging policy | 日志策略 / 历史呈现策略 |
| off-policy evaluation | 离策略评价 |

来源与延伸阅读见[参考文献](references.md)。
