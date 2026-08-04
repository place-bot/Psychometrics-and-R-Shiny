# 帮助性、安全性实验与评测边界

## 1. 帮助性人工评价

作者在 4000 多个 single-turn 与 multi-turn prompts 上比较 Llama 2-Chat 与 Falcon、MPT、Vicuna、ChatGPT、PaLM-chat。每个比较由三名评审打分。

主要结果：

- 7B 对 MPT-7B-chat，约 60% prompts 获胜；
- 34B 对 Vicuna-33B 与 Falcon-40B，总 win rate 超过 75%；
- 70B 对 ChatGPT：win 36%，tie 31.5%；
- 70B 在该 prompt 集上明显优于 PaLM-bison chat。

把 tie 一半计入可得到近似 preference score：

\[
36+\frac{31.5}{2}=51.75.
\]

这解释了论文说 70B 与 ChatGPT competitive，但不代表显著全面优于。

## 2. Inter-rater reliability

帮助性使用 7-point Likert scale，Gwet’s AC2 约 0.37–0.55。模型越接近，评审越难一致；生成评价本身具有明显主观性。

## 3. 人工帮助性评价的限制

论文明确列出：

- 约 4K prompt 不能覆盖真实使用；
- prompt 不含 coding/reasoning；
- 多轮对话只评最后一次 generation；
- 不同 evaluator instructions 会改变结果；
- ChatGPT 固定为 `gpt-3.5-turbo-0301`，模型版本具有时间性。

## 4. 安全人工评价

收集约 2000 个 adversarial prompts：

- 1351 single-turn；
- 623 multi-turn。

每个回答按 1–5 分：1–2 视为 safety violation，3–5 不计违规。三名评审 majority vote。安全 Gwet’s AC2 在不同批次约 0.70–0.95，Llama 2-Chat 平均约 0.92。

## 5. 多轮更危险

论文观察到大多数模型在 multi-turn prompt 上 violation rate 更高。攻击者可以逐步建立语境、隐藏意图或让模型在前后轮之间失去安全约束。

Falcon 单轮违规率较低，但回答很短、帮助性也低；只看 violation percentage 会奖励“什么都少说”的策略，因此还要结合平均帮助性与安全评分。

## 6. 自动安全 benchmark

| Fine-tuned model | TruthfulQA ↑ | ToxiGen ↓ |
|---|---:|---:|
| ChatGPT | 78.46 | 0.20 |
| Falcon-instruct 7B | 28.03 | 7.89 |
| MPT-instruct 7B | 29.99 | 16.33 |
| Llama 2-Chat 7B | 57.04 | 0.00 |
| Llama 2-Chat 13B | 62.18 | 0.00 |
| Llama 2-Chat 34B | **67.20** | 0.02 |
| Llama 2-Chat 70B | 64.14 | 0.01 |

70B base 到 chat：

\[
\text{TruthfulQA}:50.18\to64.14,
\]

\[
\text{ToxiGen}:24.60\to0.01.
\]

## 7. 自动指标的局限

- toxicity classifier 可能有 subgroup bias；
- 模板化拒绝可降低 toxicity，却降低帮助性；
- TruthfulQA 只覆盖特定 misconception；
- BOLD sentiment 不能完整代表公平性；
- 指标与真实伤害之间存在产品和社会中介。

## 8. Reward-model evaluation 的循环性

用自家 RM 选模型，又用同一 RM 评模型，会偏向 Llama 2-Chat。论文因此还用 GPT-4 judge 与人工评价交叉验证。GPT-4 judge 也有偏差、提示敏感和闭源版本问题。

最可靠的阅读方式是看多种评测是否给出一致方向，同时保留 prompt 集与评审范围的边界。
