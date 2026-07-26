# 双层目标、MDP 与奖励

NCAT 的数学主线可以压缩为一句话：

> 选择一小组题来估计学生，使估计后的响应模型在未用于估计的 query 题上也预测准确；把每一步的 query 预测质量写成 reward，便可用强化学习训练选题策略。

## 1. 二元交叉熵

对真实答案 \(a\in\{0,1\}\) 和预测答对概率 \(p\)，单题二元交叉熵为

\[
\ell(a,p)
=
-a\log p-(1-a)\log(1-p).
\]

若学生答对且模型给出 \(p=0.8\)，则

\[
\ell(1,0.8)=-\log 0.8\approx 0.223.
\]

若仍答对但模型只给出 \(p=0.2\)，则

\[
\ell(1,0.2)=-\log 0.2\approx 1.609.
\]

损失越小，当前学生参数对这道题的反应预测越准确。

## 2. 内层：用已选题估计当前学生

在第 \(t\) 步，响应模型的全局题目参数已预训练并冻结。学生 \(i\) 的局部参数由累计 support 作答估计：

\[
\widehat\theta_i^{\,t}
=
\arg\min_{\theta_i}
\sum_{(q,a)\in\mathcal D_i^s(t)}
\ell\!\left(a,M(q\mid\theta_i)\right).
\tag{1}
\]

这里的输入只包含真正已经选择并揭示答案的题。随着 \(t\) 增加，\(\mathcal D_i^s(t)\) 扩大，学生参数随之更新。

!!! info "内层在做什么"

    它回答的是：在目前已经问过这些题、得到这些答案之后，响应模型认为这个学生的能力或知识掌握状态是什么？

## 3. 外层：评价每一步的泛化测量质量

学生 \(i\) 的 query 集平均损失定义为

\[
\mathcal L_M
\!\left(
\mathcal D_i^u,\widehat\theta_i^{\,t}
\right)
=
\frac{1}{|\mathcal D_i^u|}
\sum_{(q,a)\in\mathcal D_i^u}
\ell\!\left(a,M(q\mid\widehat\theta_i^{\,t})\right).
\tag{2}
\]

NCAT 让每个测试步都保持较低 query 损失：

\[
\pi^*
=
\arg\min_{\pi}
\frac{1}{n}
\sum_{i=1}^{n}
\sum_{t=1}^{T}
\mathcal L_M
\!\left(
\mathcal D_i^u,\widehat\theta_i^{\,t}
\right),
\tag{3}
\]

其中 \(\widehat\theta_i^{\,t}\) 受式 (1) 约束，且 \(\mathcal D_i^s(t)\) 是策略 \(\pi\) 逐步选择出来的。

将所有 \(t=1,\ldots,T\) 的损失相加有一个实际含义：测验可能在任意一步停止，因此策略不能只在最后一步表现好。

## 4. 三种损失的分工

NCAT 中经常同时出现三个损失：

```text
support BCE
    │ 估计学生参数
    ▼
当前 θ_hat
    │ 在 query 题上预测
    ▼
query BCE
    │ 取相反数
    ▼
reward
    │ 构造 Bellman target
    ▼
TD MSE
    │ 更新
    ▼
Q 网络参数 φ
```

| 损失 | 优化对象 | 使用数据 | 作用 |
|---|---|---|---|
| support BCE | 学生局部参数 \(\theta_i\) | 已选 support 题 | 让响应模型适应该学生 |
| query BCE | 选题策略的评价信号 | held-out query 题 | 衡量已选题是否帮助泛化 |
| TD MSE | Q 网络参数 \(\phi\) | replay transition | 逼近长期动作价值 |

把三者混成一个“模型损失”会掩盖算法结构。

## 5. 从最小化损失到最大化 reward

定义第 \(t\) 步 reward：

\[
r_i^t
=
-\mathcal L_M
\!\left(
\mathcal D_i^u,\widehat\theta_i^{\,t}
\right).
\tag{4}
\]

于是式 (3) 可写成最大化期望累计回报：

\[
\max_\pi
\mathbb E_{i,\pi}
\left[
\sum_{t=1}^{T} r_i^t
\right].
\tag{5}
\]

因为 query BCE 非负，所以论文定义下的 reward 通常非正。“更好的动作”意味着 reward 更接近 0。

!!! warning "reward 是绝对损失的相反数"

    论文使用 \(r_i^t=-\mathcal L_t\)，没有使用损失改善量 \(\mathcal L_{t-1}-\mathcal L_t\)。因此相邻 reward 高度相关。做后续研究时可以比较绝对损失、损失下降量、能力后验收缩量和决策风险等设计。

## 6. 写成 MDP

一个马尔可夫决策过程记为

\[
\langle\mathcal S,\mathcal A,P,R,\gamma\rangle.
\]

在 NCAT 中：

### 状态

\[
s_t
=
\{(q_1,a_{i(1)}),\ldots,(q_{t-1},a_{i(t-1)})\}.
\tag{6}
\]

实现时通常拆成答错题序列和答对题序列，并配套 padding mask。

### 动作

\[
q_t\in\mathcal A_i^t.
\tag{7}
\]

动作是一道合法候选题。已答题、support 外题和违反硬约束的题必须被 mask。

### 状态转移

学生回答 \(q_t\) 后：

\[
s_{t+1}=s_t\cup\{(q_t,a_{i(t)})\}.
\tag{8}
\]

转移的不确定性主要来自学生对题目的答案。

### 奖励

奖励由式 (4) 给出。它在离线训练中通过 query 真值计算。

### 折扣

\[
G_t
=
r_t+\gamma r_{t+1}
+\gamma^2r_{t+2}+\cdots.
\tag{9}
\]

\(\gamma\in[0,1]\) 控制后续 reward 的权重。

## 7. 理论目标与 DQN 训练近似

式 (5) 对各步 reward 等权，对应未折扣累计回报。若 DQN 实现使用 \(\gamma<1\)，它实际逼近

\[
\mathbb E_\pi
\left[
\sum_{t=1}^{T}
\gamma^{t-1}r_t
\right],
\tag{10}
\]

从而更重视较早 reward。这是一个训练近似，也改变了权重目标。

公开 shell 示例设置 \(\gamma=0.8\)，仓库中还把有效折扣写成 epoch 相关的衰减形式。复现实验时应同时报告：

- 论文外层目标是否等权；
- 代码实际使用的 \(\gamma\)；
- 是否有额外 epoch 调度；
- 终止 transition 是否把 bootstrap 项归零。

## 8. 为什么选 Q-learning

选题动作是离散题号，且某一步的价值取决于后续还能问什么。逐步对所有离散选择路径直接反向传播十分困难。Q-learning 通过 Bellman 递推把长期优化分解为局部 TD 更新：

\[
Q^*(s_t,q_t)
=
\mathbb E
\left[
r_t+\gamma\max_{q'\in\mathcal A_{t+1}}
Q^*(s_{t+1},q')
\right].
\tag{11}
\]

下一页将逐项解释 [Q-learning、TD target、经验回放与探索](03-q-learning.md)。
