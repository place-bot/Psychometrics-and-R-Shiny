# GPT-2 架构与 GPT-1 的差别

## 1. Decoder-only Transformer

输入 token ID \(x_t\) 先查 token embedding 与位置 embedding：

\[
\mathbf h_t^{(0)}
=
\mathbf W_E[x_t]
+
\mathbf W_P[t].
\]

之后经过 \(L\) 个 causal Transformer block。每个位置只允许读取自己和左侧位置：

\[
M_{t,s}=
\begin{cases}
0,&s\le t,\\
-\infty,&s>t.
\end{cases}
\]

## 2. 一个 Pre-LN block

GPT-2 将 LayerNorm 移到每个子层输入端。第 \(\ell\) 层可写为：

\[
\widetilde{\mathbf H}^{(\ell)}
=
\mathbf H^{(\ell-1)}
+
\operatorname{MHA}
\left(
\operatorname{LN}(\mathbf H^{(\ell-1)})
\right),
\]

\[
\mathbf H^{(\ell)}
=
\widetilde{\mathbf H}^{(\ell)}
+
\operatorname{MLP}
\left(
\operatorname{LN}(\widetilde{\mathbf H}^{(\ell)})
\right).
\]

堆叠结束后再加最终 LayerNorm：

\[
\mathbf H^{\mathrm{final}}
=
\operatorname{LN}(\mathbf H^{(L)}).
\]

## 3. Multi-head causal self-attention

对某一层输入 \(\mathbf X\)：

\[
\mathbf Q=\mathbf X\mathbf W_Q,
\quad
\mathbf K=\mathbf X\mathbf W_K,
\quad
\mathbf V=\mathbf X\mathbf W_V.
\]

单头注意力为

\[
\operatorname{Attn}(\mathbf Q,\mathbf K,\mathbf V)
=
\operatorname{softmax}
\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_h}}+\mathbf M
\right)\mathbf V.
\]

causal mask \(\mathbf M\) 让训练时所有位置可并行计算，同时避免当前位置看到未来 token。

## 4. MLP 与 GELU

每个位置独立通过两层前馈网络：

\[
\operatorname{MLP}(\mathbf h)
=
\mathbf W_2\operatorname{GELU}(\mathbf W_1\mathbf h+\mathbf b_1)
+\mathbf b_2.
\]

中间宽度为 \(4d_{\mathrm{model}}\)。官方 TensorFlow 代码使用近似 GELU：

\[
\operatorname{GELU}(x)
\approx
\frac{x}{2}
\left[
1+\tanh\left(
\sqrt{\frac{2}{\pi}}(x+0.044715x^3)
\right)
\right].
\]

## 5. 输出层与权重共享

最终隐藏状态投影到词表 logits。官方实现直接使用 token embedding 矩阵的转置：

\[
\mathbf z_t
=
\mathbf h_t^{\mathrm{final}}\mathbf W_E^\top,
\qquad
p(x_{t+1}\mid x_{\le t})
=
\operatorname{softmax}(\mathbf z_t).
\]

输入 embedding 与输出权重共享可以减少参数并把输入、输出 token 放在同一表示空间。

## 6. 四种模型规模

报告原表如下：

| 报告参数量 | 层数 | \(d_{\mathrm{model}}\) |
|---:|---:|---:|
| 117M | 12 | 768 |
| 345M | 24 | 1024 |
| 762M | 36 | 1280 |
| 1542M | 48 | 1600 |

所有模型使用 1024 token 上下文，词表扩展到 50,257，训练 batch size 为 512。官方仓库后来修正参数计数，公开检查点常称为 124M、355M、774M 与 1558M/1.5B。

## 7. 相对 GPT-1 的主要变化

论文列出：

- LayerNorm 从子层输出侧移到输入侧，即 pre-normalization；
- 最后一个 self-attention block 后增加 LayerNorm；
- 残差层初始化按深度缩放，权重乘约 \(1/\sqrt{N}\)；
- 上下文长度从 512 增到 1024；
- batch size 增到 512；
- byte-level BPE 词表为 50,257。

这些变化共同服务于更深、更大的稳定训练，实验没有逐项消融每个改动的独立贡献。
