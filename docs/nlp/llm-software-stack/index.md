# LLM 软件栈：Transformers、llama.cpp 与 LangChain

这组专题专门解释大型语言模型从“磁盘上的权重”变成“可被应用调用的系统”时需要哪些软件层。重点讨论 Hugging Face Transformers、llama.cpp 和 LangChain，并说明它们各自负责什么、怎样连接以及何时不需要同时使用。

!!! info "先校准原句"
    “它们都是没有 GUI、负责在设备上加载和运行 LLM 的后端软件包”只准确描述了部分情况。

    - **llama.cpp** 是面向高效本地推理的 C/C++ 运行时和工具集；核心通过 CLI、库或 HTTP server 工作，当前也附带简单 Web UI；
    - **Transformers** 是模型架构、tokenizer、权重加载、训练与推理的通用 Python 库；
    - **LangChain** 是模型、工具、检索、状态和 agent 循环的应用编排框架，通常调用另一个推理运行时或云端 API。

三者处在不同层，因此真正有用的分类标准是“它在请求链的哪一层”，而不是“有没有图形界面”。

## 一条完整请求链

```text
用户界面 / API
       ↓
应用编排：LangChain
  ├── prompt 与消息
  ├── 检索 / 工具 / memory
  └── agent 控制循环
       ↓
统一模型接口或 HTTP 请求
       ↓
推理层：Transformers 或 llama.cpp
  ├── tokenizer
  ├── 权重加载
  ├── forward pass
  ├── KV cache
  └── sampling
       ↓
PyTorch/CUDA/Metal/CPU 等计算后端
```

## 阅读路线

1. [先建立 LLM 软件栈的分层地图](01-stack-layers.md)
2. [Hugging Face Transformers：模型库、加载器与训练接口](02-transformers.md)
3. [llama.cpp：GGUF、量化与本地推理](03-llama-cpp.md)
4. [LangChain：模型、工具、检索和 agent 编排](04-langchain.md)
5. [三者怎样连接成同一个应用](05-integration.md)
6. [性能、显存、并发和可观测性](06-performance-operations.md)
7. [怎样按研究与部署目标选软件](07-selection-conclusion.md)
8. [官方文档与延伸工具](references.md)

## 版本范围

这些项目更新很快。本专题解释稳定的软件边界与核心机制，示例接口依据 2026 年 8 月 4 日的官方文档核对。实际运行时应固定依赖版本与模型 revision。

