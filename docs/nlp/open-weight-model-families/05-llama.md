# Llama：从研究发布到开放权重生态

## 1. 代际主线

Llama 的影响不仅来自模型本身，还来自围绕权重形成的微调、量化、推理和数据生态。

| 代际 | 代表规模与上下文 | 主要变化 |
|---|---|---|
| LLaMA 1 | 7B、13B、33B、65B | 证明较小模型配合更多 token 可以获得很强基础能力；最初面向研究使用 |
| Llama 2 | 7B、13B、70B，4K | 增加公开可用训练数据、GQA（70B）以及 SFT + RLHF 的 Chat 版本 |
| Llama 3 | 8B、70B，8K | 更大 tokenizer、改进数据与训练规模 |
| Llama 3.1 | 8B、70B、405B，128K | 长上下文、多语言与 405B 模型 |
| Llama 3.2 / 3.3 | 1B、3B、视觉版本与 70B 更新 | 端侧尺寸、视觉输入和能力更新 |
| Llama 4 | Scout、Maverick 等 MoE 版本 | 稀疏专家、多模态和更长上下文 |

表格用于解释方法演进。每一代都包含 base、instruct 或多模态等不同检查点，不能用代际名称代替精确模型 ID。

## 2. Llama 2 奠定了什么

Llama 2 把一条完整的开放权重对话模型路线写得很清楚：

```text
2T token 自回归预训练
  ↓
高质量监督微调
  ↓
帮助性 / 安全性偏好数据
  ↓
Reward Models
  ↓
Rejection Sampling + PPO
  ↓
Llama 2-Chat
```

本站已在 [Llama 2 论文精读](../llama2-2023/index.md) 中逐步讲解这条流水线。家族专题更关注它怎样演化成多尺寸、多模态和长上下文生态。

## 3. tokenizer 扩展为什么重要

Llama 3 将词表扩展到约 128K token，并采用基于 tiktoken 的 tokenizer。更大的词表可能用更少 token 表示常见词和多语言片段，从而改变：

- 相同文本占用的上下文长度；
- embedding 与输出层参数量；
- 多语言和代码的切分粒度；
- 旧版微调数据与模板的兼容性。

因此，Llama 2 adapter 不能因架构名称相近就直接装到 Llama 3 上，tokenizer、词表大小和权重形状都可能不一致。

## 4. 长上下文的工程含义

Llama 3.1 把上下文扩展到 128K。长上下文带来更多原始材料，同时增加 prefill 计算与 KV cache：

\[
\text{KV cache}
\propto
L\times n\times h_{kv}\times d_h,
\]

其中 \(L\) 为层数，\(n\) 为缓存 token 数，\(h_{kv}\) 为 key/value heads 数，\(d_h\) 为 head dimension。GQA 通过减少 \(h_{kv}\) 控制这部分成本。

模型声明支持 128K 不代表它在所有任务上能同等有效地利用 128K。长文档问答仍需测量关键信息位置、干扰文档、引用正确率和首 token 延迟。

## 5. Llama 4 的 MoE 方向

Llama 4 的 Scout 和 Maverick 采用 mixture-of-experts。与 Mixtral 类似，模型拥有较大总参数容量，但每个 token 只激活部分专家。MoE 的优势主要来自提高单位前向计算所能调用的模型容量，工程代价则包括权重装载、专家并行和跨设备通信。

## 6. 为什么 Llama 生态很大

开放权重使社区能够：

- 进行 LoRA 或全参数领域微调；
- 制作 8-bit、4-bit 或更低精度量化；
- 在 llama.cpp、vLLM、Transformers 等运行时部署；
- 研究蒸馏、合成数据与模型合并；
- 对同一权重进行独立安全评测。

生态兼容仍以版本为边界。聊天模板、特殊 token、RoPE 配置、GQA 头数和许可证都应随模型保存。

## 7. Llama 的许可证边界

Meta 使用各代 Llama Community License 发布权重。以 Llama 4 为例，许可证规定归属、再分发、可接受使用以及针对超大规模月活产品的附加商业条款。这类自定义条款与 Apache 2.0 或 MIT 不同。

因此，Llama 最准确的技术分类是**开放权重模型家族**。代码仓库中的某些工具可以采用标准开源许可证，但不能据此把权重许可证也描述成 MIT 或 Apache 2.0。

