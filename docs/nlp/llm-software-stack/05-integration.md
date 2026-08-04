# 三者怎样连接成同一个应用

## 1. 三种常见组合

### 组合 A：Transformers 直接推理

```text
Python 应用 → Transformers → PyTorch → GPU/CPU
```

适合研究、训练、读取 logits、修改模型结构和小规模批处理。没有 LangChain，也没有独立模型 server。

### 组合 B：llama.cpp 本地服务

```text
网页 / 脚本 → HTTP → llama-server → GGUF → Metal/CUDA/CPU
```

适合本地量化模型、语言无关 HTTP 客户端和简单独立部署。

### 组合 C：LangChain 编排 llama.cpp

```text
应用 → LangChain agent
          ├── retriever / database / tools
          └── OpenAI-compatible client
                         ↓
                    llama-server
                         ↓
                    GGUF model
```

LangChain 负责循环与工具，llama.cpp 负责 token 生成。Transformers 不必参与在线请求，但可用于离线微调后再转换 GGUF。

## 2. 一个本地 server 请求

启动模型：

```bash
llama-server \
  -m /absolute/path/model.Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 8080
```

用兼容客户端调用：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="local-only",
)

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "解释 CAT。"}],
)
```

在同一设备运行并不自动安全。若 server 绑定 `0.0.0.0`，局域网或外部网络可能访问端口；生产部署需要鉴权、TLS、网络限制与日志脱敏。

## 3. 离线训练到本地部署

一条完整模型生命周期可能是：

```text
Hugging Face base checkpoint
        ↓ Transformers + PEFT
领域 LoRA / merged SafeTensors
        ↓ 验证 tokenizer 与输出
转换为 GGUF
        ↓ 量化
Q4_K_M / Q5_K_M 等文件
        ↓ llama.cpp 回归测试
本地部署
```

每个箭头都可能改变输出。必须分别验证：

1. adapter 合并前后；
2. SafeTensors 到 GGUF 转换前后；
3. 浮点 GGUF 到量化 GGUF 前后；
4. 官方 chat template 与部署模板；
5. 目标上下文和生成参数。

## 4. API 抽象泄漏

即使两个 server 都提供 `/v1/chat/completions`，仍可能在以下方面不同：

- system message 支持；
- tool call schema；
- JSON constrained decoding；
- token usage 计算；
- stop sequences；
- streaming chunk 格式；
- 错误码、超时与取消；
- 多模态输入格式。

因此应为每个 backend 建立 contract tests，而非只验证“能返回一段文字”。

## 5. CAT 研究系统示例

```text
学生作答
   ↓
CAT 状态更新（IRT/CDM/策略模型）
   ↓
选择下一题 ───────────────┐
   ↓                      │
需要解释或内容检索？       │
   ↓ 是                   │
LangChain 检索题目元数据   │
   ↓                      │
本地 llama.cpp / 远程模型  │
   ↓                      │
生成受约束的解释           │
   ↓                      │
审计与界面展示 ────────────┘
```

IRT 估计和选题约束应由确定性测量代码控制；LLM 适合内容理解、检索和自然语言解释。把能力估计完全交给聊天历史会失去可校准的测量模型与误差量化。

