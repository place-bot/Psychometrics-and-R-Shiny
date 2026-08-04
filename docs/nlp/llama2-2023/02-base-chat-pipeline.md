# 基础模型与 Chat 模型的完整流水线

## 1. 五个阶段

### 阶段 A：预训练

在 2T token 上学习：

\[
\mathcal L_{\mathrm{PT}}(\theta)
=
-\sum_t\log p_\theta(x_t\mid x_{<t}).
\]

输出 Llama 2 base checkpoints。

### 阶段 B：Supervised Fine-Tuning

输入人工编写的 prompt—answer 对，只在 assistant answer token 上计算 loss：

\[
\mathcal L_{\mathrm{SFT}}(\theta)
=
-\sum_{t\in\mathcal A}
\log p_\theta(y_t\mid p,y_{<t}),
\]

其中 \(\mathcal A\) 是回答 token 位置集合。

### 阶段 C：Reward Modeling

对同一 prompt 生成两个回答，由标注者选择 preferred response。reward model 学习标量：

\[
r_\phi(p,y)\in\mathbb R.
\]

### 阶段 D：RLHF 迭代

两条路线并用：

- rejection sampling：每个 prompt 采样多个回答，reward model 选最好者，再做监督式更新；
- PPO：把聊天模型视为 policy，用 reward 和 KL 约束直接优化生成策略。

### 阶段 E：安全专项训练

把 adversarial prompts、安全示范、安全偏好、context distillation 与 red-teaming 发现持续加入迭代。

## 2. 数据闭环

论文强调 reward data 必须随模型更新：

```text
当前 Chat 模型
   ↓ 对新 prompt 生成回答对
人类比较回答
   ↓
更新 reward model
   ↓
训练下一版 Chat 模型
   ↓ 分布发生变化
再收集新一轮偏好
```

若 reward model 只见过旧模型的回答，新 policy 可能离开其训练分布，评分精度下降或出现 reward hacking。

## 3. 三种监督信号的密度

| 信号 | 人类提供什么 | 模型学到什么 |
|---|---|---|
| SFT | 完整理想答案 | token 级模仿 |
| Preference | 两个答案哪个更好 | 序列级排序 |
| Safety label | safe/unsafe 与风险类别 | 安全识别和拒绝策略 |

SFT 的 token 信号密集，但要求标注者亲自写高质量长答案；偏好比较信号较稀疏，却允许模型探索出人类未必能快速写出的好答案。

## 4. 为什么需要两个 reward models

“尽可能满足请求”和“避免危险输出”有时冲突。一个回答可能很详细、直接、技术上有用，却违反安全规范。

论文训练：

\[
r_h(p,y)=\text{helpfulness score},
\]

\[
r_s(p,y)=\text{safety score}.
\]

PPO 阶段再根据 prompt 与安全阈值选择使用哪一个奖励，减少单模型同时学习两套冲突判断的难度。

## 5. 迭代版本

作者训练 RLHF-V1 到 RLHF-V5。V4 以前主要使用 rejection sampling；后期在 rejection-sampling checkpoint 上加入 PPO，再继续采样下一轮数据。

这条流程不是一次静态训练，而是模型、偏好数据和 reward model 共同演进。
