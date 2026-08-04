# 怎样选择与组合

## 1. 按目标选择

| 目标 | 优先工具 | 原因 |
|---|---|---|
| 阅读和修改模型结构 | Transformers | 架构实现与 PyTorch 张量可直接检查 |
| 训练、微调与 LoRA | Transformers + PEFT | 梯度、optimizer 与 checkpoint 流水线完整 |
| Mac/CPU/消费级 GPU 本地推理 | llama.cpp | GGUF、量化和多硬件后端成熟 |
| 暴露轻量本地 HTTP API | llama-server | 可独立运行并提供兼容接口 |
| 简单单次生成 | Transformers 或 llama.cpp 直接调用 | 无需额外编排层 |
| RAG、工具和多步 agent | LangChain / LangGraph + 任一模型 backend | 管理检索、工具、状态与控制循环 |
| 大 GPU 高并发服务 | 同时评估 vLLM、TGI 等 | 专门的 batching 与显存管理可能更合适 |

## 2. 三个常见误区

### 安装 LangChain 后还需要模型

LangChain 不自带一个通用 LLM 权重。它需要连接本地运行时或模型服务。

### 从 Hugging Face 下载不等于使用 Transformers 推理

Hugging Face Hub 是模型资产托管平台。GGUF 可以从 Hub 下载后交给 llama.cpp；SafeTensors 可以由 Transformers、vLLM 或其他运行时加载。

### 量化文件更小不保证更快

速度还取决于 kernel、内存带宽、CPU/GPU 分工、batch、上下文和量化格式是否有硬件优化。

## 3. 最小依赖原则

从最短链路起步：

```text
一次生成
→ 直接模型调用

需要共享服务
→ 增加推理 server

需要检索或工具
→ 增加明确的编排代码

需要长期、可恢复 agent
→ 增加状态图、持久化和可观测性
```

每增加一层都应解决一个已经存在的问题，并为它增加测试。这样发生错误时能判断是模型、模板、检索、工具、运行时还是应用状态造成的。

## 4. 结论

Transformers、llama.cpp 与 LangChain 可以组成同一个系统，也可以独立使用：

- Transformers 把论文架构与模型资产变成可训练、可推理的 Python 对象；
- llama.cpp 把 GGUF 权重高效映射到本地硬件并提供 CLI、库和 server；
- LangChain 把模型调用嵌入检索、工具和有状态 agent 流程。

理解它们的层级后，GUI 是否存在已经不再是关键问题。真正需要决定的是：权重在哪里运行、谁负责 token 生成、谁管理应用状态、哪些调用可以采取外部行动，以及每一层怎样测试和审计。

