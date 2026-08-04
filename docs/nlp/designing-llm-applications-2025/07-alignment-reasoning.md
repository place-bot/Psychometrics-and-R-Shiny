# Alignment、幻觉与推理

## 1. Alignment 训练改变什么

预训练学习广泛文本分布；alignment 让输出更符合帮助性、安全性和任务偏好。典型流程：

```text
Base model
  ↓ SFT demonstrations
Instruction model
  ↓ preference comparisons
Reward / preference model
  ↓ RLHF、DPO 或其他优化
Aligned model
```

## 2. 偏好数据

对 prompt \(x\)，标注者比较 \(y^+\) 与 \(y^-\)。Reward model 常用：

\[
\mathcal L_{RM}
=
-\log\sigma\left(r_\phi(x,y^+)-r_\phi(x,y^-)\right).
\]

偏好标签包含标注规范和人群价值，并非客观真理。

## 3. RLHF 中的 KL 约束

\[
R'(x,y)
=
r_\phi(x,y)
-\beta
\log\frac{\pi_\theta(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}.
\]

KL penalty 限制策略远离 reference model，缓解 reward hacking 与语言退化。

Llama 2 的完整流程见 [Llama 2 对齐专题](../llama2-2023/index.md)。

## 4. 幻觉的多个来源

| 来源 | 例子 | 主要缓解 |
|---|---|---|
| 参数知识错误 | 记住过时事实 | RAG、更新数据 |
| 上下文缺失 | prompt 没有证据 | 检索、澄清 |
| 无关上下文 | 被干扰文档带偏 | rerank、context filtering |
| 解码随机性 | 采样产生不实细节 | 低温、验证 |
| 对齐压力 | 总想给答案 | 训练拒答与不确定性 |
| 推理错误 | 中间步骤失效 | verifier、搜索、工具 |

没有单一“去幻觉开关”。

## 5. Self-consistency

采样多条推理路径 \(z_1,\ldots,z_K\)，对答案聚合：

\[
\hat y
=
\arg\max_y
\sum_{k=1}^{K}
\mathbb I(g(z_k)=y).
\]

它可提高某些可验证推理任务的稳定性，但成倍增加推理成本，多数错误路径一致时仍会失败。

## 6. Verifier

生成器提出候选，verifier 评价步骤或最终结果：

```text
Generate candidates
→ Check constraints / execute tests / score evidence
→ Select or revise
```

数学可用计算器，代码可运行测试，RAG 可核对引用。能够使用外部真值时，verifier 比模型自我确信更可靠。

## 7. Inference-time computation

通过更多采样、搜索、反思或工具调用提升单题质量。其决策可写成：

\[
\max_{c} Q(c)
\quad\text{s.t.}\quad
\operatorname{Cost}(c)\le B.
\]

不同难度请求应使用不同计算预算，而非全部请求固定最大推理长度。

## 8. CAT 中的 Alignment

教育反馈需同时满足正确、适龄、不中断测量和不泄露答案。Reward 或 preference 目标应拆成多个指标，保留人工审核与内容政策。模型的“友好”不能压过测量效度。

