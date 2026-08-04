# 系统架构、Router 与 CAT 接口

## 1. 为什么使用多个模型

单一大模型可能成本高、延迟大，并且不擅长所有任务。Multi-LLM 系统把请求分配给专门组件。

## 2. Cascade

先调用便宜模型，置信度不足再升级：

```text
request
→ small model
→ confidence / verifier
   ├── pass → return
   └── fail → large model
```

期望成本：

\[
\mathbb E[C]
=
C_s
+P(\text{escalate})C_l.
\]

关键是定义可靠升级条件。

## 3. Router

\[
r^*(x)=\arg\max_r
\left[Q(r,x)-\lambda C(r,x)\right].
\]

Router 可以依据任务类型、语言、风险、长度和难度选择模型。Router 自身也要评价误路由率。

## 4. Task-specialized models

一个系统可分别使用：

- embedding model；
- reranker；
- generator；
- moderation model；
- reward/verifier；
- OCR 或 vision model；
- 小型结构化抽取器。

专门模型往往比让一个 chat model 完成全部阶段更可测试。

## 5. Programmatic LLM systems

DSPy 等框架把 prompt 和示例视为可优化程序组件；LMQL 等语言提供生成约束和控制结构。价值在于让 LLM pipeline 更接近显式程序，而非散落字符串。

## 6. 一个面向 CAT 的系统架构

```text
学生作答
   ↓
响应记录与实时状态
   ↓
测量层：IRT / CDM / 学生模型
   ↓
合法动作层：已答题、内容、曝光、敌题、题库可用性
   ↓
选题策略：传统信息量 / RL / learned policy
   ↓
题目呈现
   ↓
下一次学生反馈
```

LLM 可以接入：

```text
题目内容 embedding
知识点与题型抽取
开放作答解析
题目检索与依据说明
自然语言反馈
生成候选题与人工审核
```

## 7. 保证 Adaptive 的关键

每次交互后必须更新状态：

\[
s_{t+1}=U(s_t,j_t,y_t),
\]

再选择：

\[
j_{t+1}\sim\pi(\cdot\mid s_{t+1},\Omega_{t+1}).
\]

LLM 若一次生成整套固定序列，就无法利用中间作答 \(y_t\)。更合理的生成式接口是逐步决策、滚动重规划或生成 contingent policy。

## 8. LLM 与测量层分工

| 层 | 更适合的技术 |
|---|---|
| 能力与误差估计 | IRT、CDM、Bayesian student model |
| 语义与内容表示 | Transformer、embedding、LLM |
| 序列长期价值 | RL、planning、learned policy |
| 硬约束 | mask、shadow test、组合优化 |
| 解释与反馈 | LLM + evidence + template |

## 9. 评价矩阵

不能只看准确率：

- 测量误差与测试长度；
- content balance；
- 曝光与题库利用；
- 个体实时适应；
- 公平性；
- 延迟；
- 解释忠实性；
- 安全与隐私。

书中的系统视角恰好支持这种多层评价。

