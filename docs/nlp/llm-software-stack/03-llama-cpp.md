# llama.cpp：GGUF、量化与本地推理

## 1. 项目目标

llama.cpp 用 C/C++ 实现 LLM 推理，强调较少依赖、跨平台和消费级硬件运行。它最初围绕 LLaMA 发展，随后支持许多模型架构与多种硬件后端，包括 CPU BLAS、Apple Metal、NVIDIA CUDA、AMD HIP 和 Vulkan 等。

它提供三种常见入口：

| 入口 | 用途 |
|---|---|
| `llama-cli` | 命令行对话、补全与快速实验 |
| `llama-server` | HTTP 服务、并发、流式响应和 OpenAI-compatible endpoints |
| `libllama` | 作为库嵌入 C/C++ 或语言绑定 |

## 2. GGUF 保存了什么

GGUF 是 llama.cpp 常用的模型文件格式。它在同一容器中保存：

- 权重张量；
- 张量形状和数据类型；
- 架构元数据；
- tokenizer 与特殊 token 信息；
- 量化类型；
- 上下文与 RoPE 等配置。

Transformers 仓库往往由多个配置和权重分片组成，GGUF 更强调一个自描述文件方便传输和加载。转换必须准确保留 tensor name、tokenizer 和 chat template 元数据。

## 3. 量化原理

把浮点权重块 \(w\) 映射到较低位整数 \(q\)，最简单形式是：

\[
q=\operatorname{round}\left(\frac{w-z}{s}\right),
\qquad
\widehat w=sq+z,
\]

其中 \(s\) 是尺度，\(z\) 是零点。llama.cpp 的 K-quants 等格式对权重块使用更细致的元数据和分组策略，以在文件大小、速度和误差之间折中。

模型名称中的 `Q4_K_M`、`Q5_K_M` 等表示具体量化方案，不是模型参数规模。不同量化器、校准方法和源权重可能让两个同名量化产生不同结果，应保留文件哈希和来源。

## 4. CPU/GPU 混合卸载

本地设备显存不足时，可以把部分层放到 GPU，其余留在系统内存和 CPU 上。粗略过程是：

```text
token IDs
  ↓
CPU embedding / 部分层
  ↓ PCIe 或统一内存传输
GPU layers
  ↓
logits 与 sampling
```

Apple Silicon 使用统一内存，CPU 和 GPU 共享内存池，但带宽和可用容量仍有限。离散 GPU 混合卸载可能受 PCIe 传输限制。最优 `n_gpu_layers` 需要根据模型、量化和设备实测。

## 5. KV cache 与上下文

自回归解码缓存此前 token 的 keys 和 values，避免每一步重算全部历史。缓存量近似为：

\[
M_{KV}
\approx
2Lnh_{kv}d_hb,
\]

其中 2 对应 K 和 V，\(L\) 为层数，\(n\) 为上下文 token 数，\(h_{kv}\) 为 KV heads，\(d_h\) 为每头维度，\(b\) 为每元素字节数。

增加 context size 或 parallel slots 会明显增加缓存，即使权重已经量化。llama-server 的总 context 可以在并发 slot 之间分配，所以必须同时规划上下文和并发。

## 6. 基本命令

```bash
# 直接运行本地 GGUF
llama-cli -m /absolute/path/model.gguf

# 从兼容仓库取得 GGUF 并运行
llama-cli -hf organization/model-GGUF:Q4_K_M

# 启动本地服务
llama-server -m /absolute/path/model.gguf --port 8080
```

服务启动后，应用可调用：

```text
POST http://127.0.0.1:8080/v1/chat/completions
```

OpenAI-compatible 表示常用请求形状兼容，不保证所有字段、错误语义与供应商 API 完全一致。集成前应以 llama-server 当前文档和自动化测试为准。

## 7. 聊天模板与约束生成

llama.cpp 可读取 GGUF 中的聊天模板，也支持显式指定模板。工具调用和多轮对话依赖模板准确性。项目还支持 GBNF grammar 或 JSON schema 约束输出，适合生成结构化数据。

结构约束保证输出满足语法，不能保证字段值真实。例如 JSON 中的日期格式正确，仍可能是模型编造的日期。

## 8. 适用与限制

llama.cpp 很适合个人电脑、本地离线、低依赖应用、GGUF 量化评测和嵌入式服务。它并非每个场景的最高吞吐方案：大 GPU 集群、高并发 continuous batching 或训练任务可能更适合 vLLM、TGI、TensorRT-LLM 或 PyTorch/Transformers。模型转换和量化还会引入额外版本管理责任。

