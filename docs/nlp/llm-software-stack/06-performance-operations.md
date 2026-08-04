# 性能、显存、并发与可观测性

## 1. Prefill 和 decode 要分开测

LLM 请求有两个阶段：

- **prefill**：一次处理输入 token，建立 KV cache；
- **decode**：每次生成一个新 token，并复用 cache。

因此常见指标包括：

| 指标 | 反映什么 |
|---|---|
| time to first token | 排队、tokenization 与 prefill 延迟 |
| inter-token latency | 单步 decode 速度 |
| output tokens/s | 用户感受到的生成速度 |
| total tokens/s | 服务对所有并发请求的吞吐 |
| peak memory | 权重、KV cache、激活与 runtime 总占用 |

只报告单用户 tokens/s 无法说明高并发服务能力。

## 2. 批处理与 continuous batching

静态 batch 等待相同大小任务一起运行；continuous batching 动态把新请求加入正在执行的调度中。推理 server 会在吞吐与单请求延迟之间折中。

llama-server 支持并行解码和多用户；Transformers 的普通 `generate()` 需要应用自行组织 batch；专门 serving 运行时通常提供更复杂的调度。选择工具时应先确定目标是交互低延迟还是离线高吞吐。

## 3. 内存由哪些部分构成

\[
M_{\text{peak}}
=
M_{\text{weights}}
+M_{KV}
+M_{\text{activations}}
+M_{\text{workspace}}
+M_{\text{runtime}}.
\]

量化主要减少 \(M_{\text{weights}}\)。增加上下文和并发主要推高 \(M_{KV}\)。某个 4-bit 模型能成功加载，只证明权重和初始 buffer 装得下，不能保证高并发长上下文运行稳定。

## 4. 缓存与状态边界

需要区分：

- 模型下载缓存；
- tokenizer 缓存；
- 单次生成的 KV cache；
- prefix / prompt cache；
- LangChain 的短期 task state；
- 跨任务长期 memory；
- RAG vector store。

它们的生命周期、隐私和失效策略不同。删除聊天记录不一定清除了向量库或 server 日志。

## 5. 可观测性

每个请求至少记录：

```text
request ID
model ID + revision + quantization
prompt template version
input/output token counts
retrieved document IDs
tool calls and statuses
latency breakdown
stop reason
error class
```

含有学生数据时，不应默认保存完整 prompt 和输出。可以记录哈希、脱敏字段或受控抽样，并设置保留期限与访问权限。

## 6. 回归测试

软件或模型升级前运行固定测试集：

1. tokenizer 结果是否改变；
2. chat template 是否改变；
3. greedy 输出是否在允许范围内；
4. 结构化输出和工具调用是否仍满足 schema；
5. RAG 引用是否仍指向正确证据；
6. 峰值显存、首 token 延迟和吞吐是否退化；
7. 超时、取消、并发和错误响应是否符合契约。

生成式模型即使设置相同 seed，也可能因硬件和 kernel 不同出现数值差异。回归标准应优先检查任务正确性与结构约束，不必要求所有采样文本逐字符相等。

