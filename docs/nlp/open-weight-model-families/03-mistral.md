# Mistral：dense、MoE 与多分支家族

## 1. 为什么 Mistral 7B 引人注意

Mistral 7B 把较小参数规模和高效注意力结合起来。它采用 grouped-query attention（GQA）降低推理时 key/value cache 成本，并在早期版本中使用 sliding-window attention（SWA）限制每层直接处理的局部窗口。

标准 causal self-attention 对长度 \(n\) 的序列形成 \(n\times n\) 的注意力矩阵，主要计算量随 \(n^2\) 增长。若每个位置只直接关注最近 \(w\) 个位置，稀疏连接数约为：

\[
O(nw),\qquad w\ll n.
\]

多层堆叠后信息仍可逐层跨越更长距离。这里的收益是降低长序列成本，代价是单层不能直接比较任意两个远距离 token。

## 2. GQA 降低了什么成本

普通 multi-head attention 为每个 query head 分别保存 key 和 value。GQA 让多组 query heads 共享较少的 key/value heads。设 query head 数为 \(h_q\)，key/value head 数为 \(h_{kv}\)，则 KV cache 的头维成本比例大致从 \(h_q\) 降到 \(h_{kv}\)：

\[
\text{KV reduction}\approx \frac{h_{kv}}{h_q}.
\]

它主要改善自回归解码时的显存带宽和缓存占用，不等同于减少整个模型的参数量。

## 3. 从 dense 到 sparse MoE

Mixtral 8x7B 把每层前馈网络替换成专家集合。路由器对 token 表示 \(x_t\) 计算专家分数，并选 top-\(k\) 专家：

\[
g_t=\operatorname{softmax}(W_gx_t),
\]

\[
\operatorname{MoE}(x_t)
=
\sum_{e\in\operatorname{TopK}(g_t)}g_{t,e}E_e(x_t).
\]

Mixtral 8x7B 拥有约 47B 总参数，但每个 token 只激活约 13B 参数。于是出现三个不同的规模概念：

| 概念 | 决定什么 |
|---|---|
| 总参数 | 权重存储、跨设备通信与装载成本 |
| 激活参数 | 每个 token 前向计算的大致成本 |
| KV cache | 长上下文和并发解码的显存成本 |

“激活参数接近 13B”不能理解成它在任何硬件上都像普通 13B dense 模型一样容易部署，因为全部专家权重仍需驻留或跨设备读取。

## 4. 家族演进

Mistral 后续形成多条分支：

- **小型或中型 dense 模型**：强调低延迟与本地部署；
- **Mixtral**：用稀疏 MoE 提高总容量与单位 token 计算效率；
- **Codestral / Devstral**：针对代码生成和软件工程 agent；
- **Pixtral**：加入视觉输入；
- **Ministral**：面向较小部署规模；
- **Mistral Large / Medium / Small**：面向不同服务质量与成本层级。

这些名称表达的是一家公司逐渐扩展出的产品与研究矩阵，而非一套完全相同的架构或许可。

## 5. tokenizer 与聊天模板也会演进

Mistral 官方文档区分多个 tokenizer 版本。早期 Mistral 7B 和 Mixtral 主要使用 SentencePiece 系列模板，后续模型还采用 Tekken 等 tokenizer。聊天模型依赖准确的控制 token 和消息边界：

```text
<s>[INST] 用户消息 [/INST] 助手回答</s>
```

如果直接把一段文本送入错误模板，模型可能仍能生成语言，却会损失工具调用、轮次区分或指令遵循能力。模型 ID、tokenizer 和 chat template 必须作为一个版本整体保存。

## 6. 许可证不能按品牌推断

Mistral 7B 与 Mixtral 8x7B 的官方模型卡列出 Apache 2.0 权重；家族内其他版本可能采用不同条款。部署时应逐项核对：

```text
精确 model ID
→ 官方模型卡
→ 权重链接对应的 LICENSE
→ 是否允许商用、再分发与模型衍生
```

Mistral 的方法价值在于展示了高效 dense、GQA、局部注意力与稀疏 MoE 可以组合成一条从本地模型到大规模服务的技术路线。品牌本身不提供许可证结论。

