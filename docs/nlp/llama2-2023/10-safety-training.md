# 安全微调、Context Distillation 与红队

## 1. 三层安全训练

### 1.1 Safety SFT

标注者设计 adversarial prompts，并编写安全、解释充分、尽可能有帮助的回答，和一般 SFT 数据一起训练。

### 1.2 Safety RLHF

收集更难的攻击 prompt，让标注者比较多个回答的安全性，训练 Safety RM，再用于 rejection sampling 和 PPO。

### 1.3 Safety Context Distillation

先给模型加安全 preprompt：

```text
You are a safe and responsible assistant ...
```

生成更安全回答 \(y^+\)，再用原始用户 prompt 与 \(y^+\) 微调，不保留 preprompt：

\[
(c_{\mathrm{safety}},p)
\xrightarrow{\pi}
y^+,
\]

\[
(p,y^+)
\xrightarrow{\mathrm{SFT}}
\theta'.
\]

安全上下文产生的行为被蒸馏进参数。

## 2. 风险类别

论文主要划分：

- illicit and criminal activities；
- hateful and harmful activities；
- unqualified advice，如医疗、金融、法律建议。

攻击向量包括心理操纵、错误前提、拼写变形、隐喻、角色扮演、非英语和长对话。

## 3. 安全回答指南

目标回答通常依次：

1. 处理立即安全风险；
2. 解释为什么请求可能有风险；
3. 在可能时提供安全替代、背景知识或求助渠道；
4. 避免无意义说教与过度拒绝。

安全与帮助性的张力体现在：拒绝危险细节后，仍应尽量回应用户的正当目的。

## 4. Safety data scaling

论文保持约 0.9M helpfulness samples 不变，把 safety data 从 0% 增加到 100%，总量约 0.1M，训练多个变体。

Safety RM score 随安全数据增加明显改善，helpfulness score 在足够帮助性数据支撑下没有明显下降。但 false refusal rate 会增加，说明安全调优过强会损害正常请求。

## 5. 为什么只做几千条 Safety SFT 就转向 RLHF

模型从少量安全示范中很快学会写详细拒绝和替代建议；继续人工写长答案的边际价值下降。偏好比较更适合区分：

- 简短拒绝与有帮助的安全回答；
- 表面安全但仍泄露危险细节的回答；
- 过度拒绝与合理回答；
- 多轮诱导下的细微违规。

## 6. Context distillation 的副作用

论文附录展示它可能：

- 给无害问题添加多余安全警告；
- 误判语境并拒绝；
- 让回答模板化；
- 把 preprompt 的偏差固化进参数。

作者让 Safety RM 决定每个 sample 是否使用 context distillation，避免对全部 prompt 无差别施加。

## 7. 红队

红队超过 350 人，包括网络安全、选举虚假信息、法律、政策、公民权利、伦理、软件工程、ML、Responsible AI 和创意写作专家，也覆盖不同人口背景。

测试范围包括犯罪计划、人口贩运、受管制物质、露骨内容、无资质建议、隐私、武器与 cyber 等，并尝试角色扮演、创作任务、积极包装、拼写变形和长对话等攻击。

## 8. 红队闭环

每轮发现被用于：

- fine-tuning data；
- model feedback training；
- safety model training；
- 下一轮候选 release 复测。

论文用每人每小时发现违规 prompt 数衡量红队难度。7B 的一个示例从 1.8 降至 0.45；新模型对上一轮违规 prompt 平均拒绝率约 90%。

## 9. 评测边界

红队覆盖广但不穷尽所有语言、文化、攻击者和未来组合攻击。训练进红队发现还可能造成 benchmark 熟悉。安全需要持续监控、部署层过滤、访问控制和场景化测试，不能只由模型参数承担。
