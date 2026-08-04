# 外部工具与 Agent 系统

## 1. 三种交互范式

### Passive

应用构造输入，模型只返回内容。

### Explicit tool use

模型输出结构化工具请求，应用执行后把结果返回模型。

### Autonomous loop

模型根据状态反复决定调用工具或结束，形成 agent。

## 2. Agent 状态

\[
s_t=(x,h_t,o_t,m_t),
\]

其中 \(x\) 是目标，\(h_t\) 是对话与动作历史，\(o_t\) 是 observations，\(m_t\) 是外部 memory。

策略选择：

\[
a_t\sim\pi_\theta(a\mid s_t).
\]

若 \(a_t\) 是工具调用，执行后进入 \(s_{t+1}\)；若是 final answer，则停止。

## 3. 工具定义

一个工具至少包含：

- name；
- description；
- JSON schema；
- executable function；
- authorization policy；
- timeout 与 error semantics。

工具描述是模型的行为条件，实际权限必须由代码控制。

## 4. Guardrail 与 Verifier

```text
模型提议动作
→ schema validation
→ policy / permission check
→ optional human approval
→ execution
→ output sanitization
→ model observation
```

Prompt 里写“不要做危险操作”不能替代最小权限、沙箱与人工审批。

## 5. Stop conditions

Agent 必须有：

- 最大步数；
- token/费用预算；
- 工具超时；
- 重复动作检测；
- no-progress 判断；
- 用户取消；
- 需要人工输入时的暂停状态。

## 6. Memory

短期 state 是本任务历史；长期 memory 跨任务保存。长期记忆进入本轮上下文前仍需检索、过滤和权限判断。

## 7. Orchestration 软件

LangChain 提供较高层 agent 和工具抽象，LangGraph 更偏向 durable state 与图执行。它们不负责底层 Transformer forward。详见 [LLM 软件栈](../llm-software-stack/index.md)。

## 8. Agent 评价

| 指标 | 含义 |
|---|---|
| task success | 最终任务是否完成 |
| tool selection | 是否选择正确工具 |
| argument accuracy | 参数是否正确 |
| excess calls | 是否产生不必要调用 |
| recovery | 工具失败后能否恢复 |
| safety violation | 是否越权或泄漏数据 |
| cost/latency | 完成任务所需资源 |

## 9. CAT Agent 的边界

题目选择属于高约束决策。Agent 可以查询题库、内容标签、曝光统计和学生状态，但合法动作 mask、能力估计和停止规则应由确定性代码执行。模型不能绕过测验安全与内容蓝图。

