# Transformer 中改哪些矩阵

## 1. 候选矩阵

每层 attention 通常有

\[
W_q,\quad W_k,\quad W_v,\quad W_o,
\]

FFN 有

\[
W_{\text{up}},\quad W_{\text{down}}.
\]

LoRA 原理可用于任意 dense layer。原论文实验为控制变量，主要研究 self-attention 投影，很多设置只适配 \(W_q,W_v\)。

## 2. 同一预算下的 GPT-3 实验

参数预算约 18M：

| 适配矩阵 | rank | WikiSQL | MultiNLI |
|---|---:|---:|---:|
| \(W_q\) | 8 | 70.4 | 91.0 |
| \(W_k\) | 8 | 70.0 | 90.8 |
| \(W_v\) | 8 | 73.0 | 91.0 |
| \(W_o\) | 8 | 73.2 | 91.3 |
| \(W_q,W_k\) | 4 | 71.4 | 91.3 |
| \(W_q,W_v\) | 4 | 73.7 | 91.3 |
| Q/K/V/O | 2 | 73.7 | 91.7 |

分散到更多矩阵的小 rank 可优于把预算集中到单一矩阵的大 rank。

## 3. Q 与 V 的角色

- \(W_q\) 改变当前位置如何提出检索需求；
- \(W_v\) 改变被读取后传递什么内容；
- \(W_k\) 改变候选如何被匹配；
- \(W_o\) 改变各头输出怎样混合。

原论文的 Q/V 选择是经验结果，不构成所有模型和任务的通用最优定理。

## 4. Fused QKV

有些实现把 QKV 合并为一块线性层。官方 `loralib.MergedLinear` 允许通过 `enable_lora` 只为其中某些切片启用 LoRA，例如 Q 和 V 开启、K 关闭。

## 5. 现代配置

现代 decoder-only 模型还可能有 GQA/MQA、SwiGLU 与不同模块名。选择 target modules 时要检查实际模型结构、权重形状与命名，不能机械复制 `q_proj,v_proj`。
