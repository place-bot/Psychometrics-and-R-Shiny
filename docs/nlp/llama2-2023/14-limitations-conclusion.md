# 局限、结论与方法演进

## 1. 模型局限

论文承认：

- 预训练结束后知识不再自动更新；
- 会 hallucinate、给出不准确或无资质建议；
- 主要针对英语，其他语言表现脆弱；
- 可能生成有害、冒犯或带偏见内容；
- 安全微调有时过度，导致 false refusal；
- 对话模型可能被用于虚假信息、网络犯罪等恶意用途；
- base model 缺少足够安全对齐，部署风险更高。

## 2. 方法证据局限

### 2.1 数据不透明

语料只按“公开可获得来源混合”描述，无法完整复现数据选择、版权状态、污染与群体代表性。

### 2.2 对齐数据不公开

核心 SFT、Meta preference 与 reward models 未发布，外部难以复现论文最有价值的 chat alignment 管线。

### 2.3 人工评价范围

帮助性约 4K prompts，不含 coding/reasoning；安全约 2K adversarial prompts。版本、说明和评审群体都会影响结论。

### 2.4 RM 优化偏差

reward model 是人类偏好的近似。PPO 与 best-of-N 会主动搜索其盲点，KL、人工复核和持续新数据只能缓解，不能消除。

### 2.5 安全与帮助性动态冲突

安全数据增加会减少危险输出，也可能增加正常请求拒绝。单一 violation metric 会奖励过短、过度保守的回答。

## 3. 有趣但初步的观察

论文报告：

- RLHF 让事实 prompt 的输出随 temperature 变化仍更稳定，而创意 prompt 保持多样性；
- 仅 1000 条带日期 SFT 数据就出现一定时间组织能力；
- 未专门标注工具调用时，模型在 prompt 中仍能理解 calculator/API 语义并组合调用。

这些观察来自有限手工测试或特定实验，需要更严格复现与机制研究，不能视为普遍保证。

## 4. 从 GPT-3 到 Llama 2

| 维度 | GPT-3 | Llama 2 |
|---|---|---|
| 主要问题 | 规模如何增强 in-context learning | 怎样发布强 base model 并训练安全 chat model |
| 参数更新 | 下游主实验不更新 | SFT/RLHF 持续更新 |
| 最大模型 | 175B | 70B |
| 训练 token | 300B | 2T |
| context | 2K | 4K |
| 对齐 | 论文重点不在 RLHF | SFT + dual RM + RS + PPO + safety |
| 发布 | 无权重 | 自定义许可证下提供权重 |

Llama 2 参数更少，却用更多 token 训练，并把大量研究资源投入 post-training。这体现范式变化：模型能力由预训练与对齐共同决定。

## 5. 论文最重要的方法启示

### 5.1 Base 与 assistant 分层

语言能力、任务知识与部署行为需要分别评估。基础模型 benchmark 强不代表聊天安全；聊天拒绝多也不代表基础知识弱。

### 5.2 高质量 SFT 负责启动

数万条精心设计示范可建立对话格式和初始行为，但完整对齐仍依赖大规模偏好反馈。

### 5.3 Preference pipeline 必须 on-distribution

policy 改变后要持续采集新回答比较，让 RM 跟上生成分布。

### 5.4 安全是迭代系统

安全 SFT、RM、RLHF、context distillation、红队、部署过滤和监控需要形成闭环。

### 5.5 推理效率进入模型设计

GQA 直接针对 KV cache 与吞吐，说明开放部署成本已经成为架构选择的一部分。

## 6. 结论

Llama 2 的贡献不只是一组可下载模型。论文把现代 chat model 的训练拆成可讨论的模块：预训练、SFT、偏好数据、双 RM、rejection sampling、PPO、KL、安全微调、多轮一致性与红队。

它同时留下关键开放问题：训练数据与对齐数据如何透明发布，reward model 怎样避免被利用，安全如何跨语言和场景泛化，以及开放权重模型如何兼顾可研究性、许可和部署责任。
