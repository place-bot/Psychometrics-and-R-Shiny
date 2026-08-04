# LLM 软件栈的分层地图

## 1. 模型、运行时与应用框架

一句“运行 LLM”可能包含完全不同的任务：下载模型、读取 tokenizer、把权重放进显存、执行矩阵乘法、管理对话历史、检索文档、调用工具以及把结果流式发送给网页。

可以拆成七层：

| 层 | 典型对象 | 负责内容 |
|---|---|---|
| 模型资产 | config、tokenizer、weights、chat template | 描述模型及其参数 |
| 模型库 | Transformers | 用代码实现架构并把资产实例化 |
| 推理运行时 | llama.cpp、vLLM、TGI | 高效执行 prefill 和 decode |
| 硬件后端 | PyTorch、CUDA、Metal、BLAS、Vulkan | 执行张量算子 |
| 服务层 | llama-server、TGI server、自建 FastAPI | 并发、流式响应、鉴权、健康检查 |
| 应用编排 | LangChain / LangGraph | prompt、检索、工具、状态、agent 循环 |
| 用户界面 | 网页、桌面端、命令行 | 展示消息并收集用户输入 |

同一个工具可以跨越相邻层。例如 Transformers 既能定义模型，也能直接执行推理；llama.cpp 同时提供核心库、CLI 和 HTTP server。分层的用途是判断主要职责，并不要求每个项目只能属于一个格子。

## 2. 后端一词为什么容易混淆

在 Web 开发中，backend 常指服务器端业务逻辑。在深度学习中，backend 还可能指 CUDA、Metal 或 CPU BLAS 这样的算子实现。在模型应用中，开发者又会把本地推理 server 称为模型 backend。

因此更准确的表达是：

- llama.cpp：**推理运行时 / serving backend**；
- Transformers：**模型实现与训练推理库**；
- LangChain：**LLM 应用与 agent 编排框架**。

## 3. 一次生成经历什么

给定消息 \(m)，生成过程可以写成：

\[
x_{1:n}=\operatorname{Tokenizer}(\operatorname{Template}(m)),
\]

\[
z_{n+1}=f_\theta(x_{1:n};K,V),
\]

\[
x_{n+1}\sim\operatorname{Sampler}(z_{n+1}),
\]

随后把新 token 加入序列，更新 KV cache 并重复解码。不同层的职责是：

1. LangChain 或应用代码组织 \(m\) 以及可能的检索文档和工具结果；
2. chat template 把消息角色变成模型训练时使用的控制 token；
3. tokenizer 把文本变成 token IDs；
4. Transformers 或 llama.cpp 执行 \(f_\theta\)；
5. sampler 按 temperature、top-p 等规则选出下一个 token；
6. 服务层将 token 流返回应用。

## 4. 模型格式不是架构名称

同一个 Llama 架构可以以不同文件格式保存：

| 格式 | 常见生态 | 特点 |
|---|---|---|
| SafeTensors | Transformers / Hugging Face | 安全的张量序列化，常与 config 和 tokenizer 分文件保存 |
| PyTorch checkpoint | PyTorch | 通用，但需谨慎对待 pickle 类格式的代码执行风险 |
| GGUF | llama.cpp 生态 | 单文件携带张量与元数据，适合量化和跨平台本地推理 |
| ONNX | ONNX Runtime | 静态计算图与跨平台执行 |

模型格式只描述资产怎样存储。它不自动决定训练数据、许可证、准确率或聊天能力。

## 5. GUI 是否存在不是核心差异

这些项目大多可以被无界面地嵌入服务器，也可能附带 CLI、Notebook 或 Web UI。llama-server 当前提供简单 Web UI，Transformers 常在 Notebook 中使用，LangChain 也提供前端集成。生产系统仍应把界面与模型运行层解耦，以便替换模型或运行时而不重写产品界面。

