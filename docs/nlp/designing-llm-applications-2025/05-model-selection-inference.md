# 模型选型、加载与解码

## 1. 先定义任务，再看排行榜

模型选择是约束优化：

\[
m^*
=
\arg\max_m Q(m)
\quad
\text{s.t.}
\quad
C(m)\le B,
\ L(m)\le L_{\max},
\ G(m)=1.
\]

其中 \(Q\) 为业务质量，\(C\) 为成本，\(L\) 为延迟，\(G\) 为许可证和治理可行性。

## 2. Model flavor

| 类型 | 使用方式 |
|---|---|
| Base | 继续预训练、研究和自定义对齐 |
| Instruct / Chat | 直接任务遵循与对话 |
| Code | 代码补全、生成和软件工程 |
| Embedding | 向量检索、聚类和 reranking 前置 |
| Reasoning | 高难推理与较多 inference-time compute |
| Multimodal | 文本与图像、音频等联合输入 |

选择后必须使用对应 chat template、tokenizer 和 generation config。

## 3. 开放权重与 API

需要分别评估：

- 权重是否可下载；
- 商用与再分发条款；
- 数据是否必须离开本地；
- 模型版本是否稳定；
- 本地硬件与运维成本；
- API 的价格、速率与日志政策。

详细模型家族比较见 [开放权重模型家族](../open-weight-model-families/index.md)。

## 4. 解码

Temperature：

\[
p_i(T)=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)}.
\]

Top-k 只保留概率最高的 \(k\) 个 token；top-p 保留累计概率达到 \(p\) 的最小集合。Greedy decoding 每步取最大 logit，beam search 保留多个序列候选。

解码策略改变输出分布，不改变模型参数。结构化抽取常采用低 temperature 或 constrained decoding；创意生成可增加采样多样性。

## 5. Structured output

仅在 prompt 里要求 JSON 不保证语法正确。更稳健的层次包括：

```text
自然语言要求
→ JSON mode
→ JSON Schema constrained decoding
→ 应用层 validation
→ retry / repair / human review
```

语法有效也不保证字段值真实。

## 6. 统一评价协议

每个候选模型使用：

- 相同业务样本；
- 各自正确聊天模板；
- 固定检索结果与工具 schema；
- 相同或明确记录的生成参数；
- 目标部署精度与量化版本；
- 盲评与自动指标结合；
- 失败类型而非只报平均分。

## 7. 加载层与应用层

Transformers、llama.cpp 与 LangChain 处在不同层。完整区分见 [LLM 软件栈](../llm-software-stack/index.md)。模型加载成功只说明权重能执行，不说明 prompt、工具、memory 和生产并发已经设计完成。

