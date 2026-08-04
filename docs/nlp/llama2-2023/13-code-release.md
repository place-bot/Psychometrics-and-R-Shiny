# 官方代码、聊天模板与开放边界

## 1. 仓库提供什么

官方 [meta-llama/llama](https://github.com/meta-llama/llama) 仓库是最小推理实现，包含：

- PyTorch Transformer forward；
- RMSNorm、RoPE、SwiGLU、GQA；
- FairScale tensor model parallel layers；
- SentencePiece tokenizer wrapper；
- KV cache 与 top-p generation；
- text/chat completion 例子；
- 模型卡、许可证与 Responsible Use Guide。

仓库当前已标记 deprecated，并指向后续 Llama 工具链；精读本专题仍以其中的 Llama 2 最小实现为准。

## 2. `RMSNorm`

代码：

```python
x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps)
```

之后乘可学习 `weight`。计算临时转为 float，再转回原 dtype，提升归一化数值稳定性。

## 3. `FeedForward`

```python
w2(F.silu(w1(x)) * w3(x))
```

直接对应 SwiGLU。三组无 bias 线性层通过 Column/RowParallelLinear 切到 tensor-parallel devices。

## 4. RoPE

`precompute_freqs_cis()` 构造复数极坐标：

\[
e^{it\omega_j}.
\]

`apply_rotary_emb()` 把 Q/K 最后维两两组合成复数，与位置相位相乘，再转回实数。

## 5. GQA

```python
n_rep = n_local_heads // n_local_kv_heads
keys = repeat_kv(keys, n_rep)
values = repeat_kv(values, n_rep)
```

K/V cache 只存较少的 `n_kv_heads`，attention 前再逻辑展开到 query heads 数量。

## 6. KV cache

每层预分配：

\[
\text{cache shape}
=
[B_{\max},T_{\max},H_{KV},d_h].
\]

因此 README 提醒 `max_seq_len` 和 `max_batch_size` 会直接影响显存预分配。生成一步只把新 K/V 写入 `start_pos:start_pos+seqlen`。

## 7. Chat template

官方代码定义：

```text
[INST] ... [/INST]
<<SYS>>
system message
<</SYS>>
```

system message 被合并进第一条 user content。历史每轮以 BOS 开头、EOS 结束，最后 user turn 以 `[INST] ... [/INST]` 结束，等待 assistant generation。

模型对模板很敏感。缺失 BOS/EOS、空格、换行或 role 顺序都可能改变行为。

## 8. 模板注入检查

官方 `chat_completion()` 拒绝用户消息中直接出现特殊模板 tags，避免用户伪造 system/assistant 边界。它只是一层字符串检查，不能覆盖所有语义 prompt injection。

## 9. 采样

temperature 大于 0 时：

\[
p=\operatorname{softmax}(z/\tau),
\]

再使用 top-p 选取累计概率质量内的 token。temperature 为 0 时直接 argmax。代码在不同 prompt 长度组成 batch 时，用 mask 保持仍处于 prompt 区的 token 不被生成覆盖。

## 10. 发布范围

官方提供模型权重访问与推理代码，但论文级内容仍未全部发布：

- 2T-token 完整语料；
- 预训练和 RLHF 全部代码；
- 27,540 条 SFT 数据；
- Meta preference data；
- reward model weights；
- rejection sampling/PPO 生产管线。

因此外部可以运行、微调和研究 checkpoint，却不能精确复现完整 Llama 2-Chat 训练。

## 11. 许可证边界

Llama 2 使用自定义 Community License，包含署名、acceptable use、特定再分发要求、超大月活产品的额外商业条款以及不得用材料改进其他大模型等限制。使用时应直接阅读官方 `LICENSE` 与 `USE_POLICY`。

“权重可下载”和“OSI 意义上的开源软件”涉及不同标准。本专题使用“开放权重”描述其科学与工程可获得性。
