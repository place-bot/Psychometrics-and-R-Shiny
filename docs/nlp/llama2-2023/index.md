# Llama 2：开放权重基础模型与对话对齐

本专题精读 Touvron et al. 的 **Llama 2: Open Foundation and Fine-Tuned Chat Models**。论文于 2023 年发布，包含两类模型：经过 2 万亿 token 预训练的 Llama 2 基础模型，以及在此基础上通过 SFT 与 RLHF 得到的 Llama 2-Chat。

## 一句话抓住论文

先训练 7B、13B、34B、70B 的通用自回归基础模型；再用少量高质量对话示范建立 SFT 模型，持续收集人类偏好比较，训练帮助性与安全性 reward models，并交替使用 rejection sampling 与 PPO 把模型对齐为聊天助手。

## 完整训练路线

```text
公开可获得的在线语料
        ↓ 2T token 自回归预训练
Llama 2 基础模型
        ↓ 27,540 条高质量 SFT 标注
Llama 2-Chat-SFT
        ↓ 偏好比较 → Helpfulness RM + Safety RM
        ↓ Rejection Sampling + PPO，多轮迭代
        ↓ Safety SFT / Safety RLHF / Context Distillation / Red Teaming
Llama 2-Chat
```

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Hugo Touvron 等 68 位作者 |
| 发布 | arXiv:2307.09288，2023 |
| 原文 | [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288) |
| 官方仓库 | [meta-llama/llama](https://github.com/meta-llama/llama) |
| 官方模型卡 | [Llama 2 model card](https://github.com/meta-llama/llama-models/blob/main/models/llama2/MODEL_CARD.md) |
| 模型规模 | 7B、13B、34B、70B；公开发布时重点提供 7B、13B、70B |
| 上下文 | 4096 token |

## 阅读路线

1. [论文问题、贡献与模型家族](01-question-contributions.md)
2. [基础模型与 Chat 模型的完整流水线](02-base-chat-pipeline.md)
3. [预训练数据、tokenizer 与优化](03-pretraining-data-tokenizer.md)
4. [RMSNorm、SwiGLU、RoPE 与 GQA](04-architecture.md)
5. [基础模型实验与证据分析](05-base-experiments.md)
6. [监督微调：为什么少量高质量数据有效](06-supervised-finetuning.md)
7. [偏好数据与双 Reward Model](07-preference-reward-model.md)
8. [Rejection Sampling 迭代微调](08-rejection-sampling.md)
9. [PPO、组合奖励与 KL 约束](09-ppo-rlhf.md)
10. [安全微调、Context Distillation 与红队](10-safety-training.md)
11. [Ghost Attention 与多轮一致性](11-ghost-attention.md)
12. [帮助性、安全性实验与评测边界](12-chat-evaluation.md)
13. [官方代码、聊天模板与开放边界](13-code-release.md)
14. [局限、结论与方法演进](14-limitations-conclusion.md)
15. [参考文献与一手资料](references.md)

## 这篇论文在学习路线中的位置

GPT-3 主要研究固定参数下的 in-context learning。Llama 2 的重点转向：怎样把预训练基础模型持续训练成更符合人类偏好、适合对话部署的模型，同时发布权重和推理代码供外部研究与开发。

两者的关键差别可以先记成：

\[
\text{GPT-3 few-shot}
=
\text{上下文改变行为},
\]

\[
\text{Llama 2-Chat alignment}
=
\text{SFT/RLHF 永久改变参数}.
\]
