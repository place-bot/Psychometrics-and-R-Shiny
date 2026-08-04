# 论文问题、贡献与模型家族

## 1. 研究问题

2023 年已有许多公开基础模型，但高质量聊天系统往往来自闭源产品。基础模型会续写文本，却未必稳定遵循指令、拒绝危险请求或维持多轮对话。对话对齐需要大量标注、reward modeling、RLHF 和安全工程，而这些步骤通常缺乏透明描述。

论文同时解决两个问题：

1. 如何训练有竞争力、可获得权重的基础模型；
2. 如何把基础模型系统地对齐为帮助性与安全性较强的聊天模型。

## 2. 两类模型必须分开

### Llama 2

通用基础语言模型，只接受自回归预训练。它适合 completion、研究和后续微调，不以聊天助手行为为默认目标。

### Llama 2-Chat

从 Llama 2 初始化，依次接受 SFT、reward modeling、rejection sampling、PPO 和安全微调。它使用专门聊天模板并针对 dialogue use case 优化。

同一个参数规模下：

\[
\theta_{\mathrm{Chat}}
\ne
\theta_{\mathrm{Base}}.
\]

## 3. 模型家族

| 模型 | 预训练 token | context | GQA | 峰值学习率 |
|---|---:|---:|---|---:|
| Llama 2 7B | 2.0T | 4K | 否 | \(3.0\times10^{-4}\) |
| Llama 2 13B | 2.0T | 4K | 否 | \(3.0\times10^{-4}\) |
| Llama 2 34B | 2.0T | 4K | 是 | \(1.5\times10^{-4}\) |
| Llama 2 70B | 2.0T | 4K | 是 | \(1.5\times10^{-4}\) |

所有模型使用全局 batch size 4M token。论文研究了 34B，但模型家族的主要公开下载规模为 7B、13B 与 70B。

## 4. 主要贡献

### 4.1 更强的基础模型

相对 Llama 1，训练 token 增加约 40%，上下文从 2K 增至 4K，更新数据混合与清洗，并在大模型使用 GQA 改善推理扩展性。

### 4.2 详细对齐流水线

论文公开描述：

- 27,540 条高质量 SFT 标注；
- 超过 140 万条 Meta 人类偏好比较；
- help/safety 两个独立 reward models；
- preference margin ranking loss；
- rejection sampling 与 PPO 的交替迭代；
- KL penalty 与 reward whitening；
- 多轮一致性的 Ghost Attention。

### 4.3 安全训练与评测

包括安全 SFT、安全 RLHF、context distillation、350 多人红队和约 2000 个对抗 prompt 的人工安全评价。

### 4.4 权重与推理代码发布

Meta 通过自定义 Llama 2 Community License 提供模型权重和最小推理代码，允许许多研究与商业用途，同时附带使用限制。准确称呼是“开放权重”或“可获得权重”；许可证并非无条件开源许可证。

## 5. 论文核心证据

- 基础 Llama 2 在论文汇总 benchmark 上普遍优于同规模 Llama 1、MPT 与 Falcon；
- SFT 到多轮 RLHF 版本的 reward 与人工偏好持续改善；
- Llama 2-Chat 在作者的人类评价 prompt 集上显著优于当时开源聊天 baseline；
- 70B 对 ChatGPT 的 win rate 为 36%、tie rate 为 31.5%；
- safety tuning 后，70B 的 ToxiGen 指标从 24.60 降至 0.01，TruthfulQA 从 50.18 升至 64.14。

这些结果依赖作者选定的 prompt、评审规范、模型版本与解码设置，不能直接外推到所有部署场景。
