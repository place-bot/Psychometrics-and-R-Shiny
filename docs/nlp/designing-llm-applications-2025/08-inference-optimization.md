# 推理优化：Cache、量化、蒸馏与加速解码

## 1. Prefill 与 Decode

```text
Prefill：并行处理输入，建立 KV cache
Decode：每轮生成一个 token，反复读取 cache
```

首 token 延迟主要受排队、tokenization 和 prefill 影响；后续速度由单步 decode、内存带宽与 batching 决定。

## 2. KV Cache

缓存此前层的 keys 和 values：

\[
M_{KV}
\approx
2Lnh_{kv}d_hb,
\]

其中 \(L\) 为层数，\(n\) 为缓存 token，\(h_{kv}\) 为 KV heads，\(d_h\) 为 head dimension，\(b\) 为字节数。

长上下文和并发会放大 KV cache，即使权重已经 4-bit 量化。

## 3. 量化

\[
q=\operatorname{round}\left(\frac{w-z}{s}\right),
\qquad
\widehat w=sq+z.
\]

低位权重减少存储和内存带宽。对称量化常设零点为 0；非对称量化允许非零 \(z\)，更灵活但元数据和 kernel 更复杂。

量化质量取决于位宽、分组、校准、outlier 处理和硬件 kernel。文件更小不保证速度更快。

## 4. Knowledge Distillation

学生模型拟合教师分布：

\[
\mathcal L
=
\lambda\mathcal L_{\mathrm{hard}}
+(1-\lambda)T^2
\operatorname{KL}
\left(
p_T^{\mathrm{teacher}}
\parallel
p_T^{\mathrm{student}}
\right).
\]

也可以蒸馏生成数据、推理轨迹、工具行为或 embedding。

## 5. Speculative Decoding

小 draft model 一次提出多个 token，大 target model 并行验证：

```text
draft proposes k tokens
→ target verifies in one pass
→ accept valid prefix
→ resample first rejection
```

算法可保持 target distribution，同时减少昂贵 target forward 次数。速度取决于 draft 成本和接受率。

## 6. Parallel Decoding

尝试同时预测多个位置或用多个候选分支降低串行步数。实际收益取决于模型支持、验证机制和请求长度。

## 7. Early Exit

在中间层已经足够确定时提前输出，适合分类或专门架构。通用自回归生成较难直接使用，因为每个 token 的误差会进入后续上下文。

## 8. Serving 评价

至少报告：

- time to first token；
- inter-token latency；
- 单用户 tokens/s；
- 并发总吞吐；
- 峰值 GPU/CPU memory；
- 每请求能耗或成本；
- 量化后任务质量；
- 长上下文性能。

## 9. 与本地推理的连接

llama.cpp、Transformers、vLLM 和 TGI 的角色与差异已整理在 [LLM 软件栈专题](../llm-software-stack/index.md)。应在目标硬件、目标 batch 和目标 context 上实测。

