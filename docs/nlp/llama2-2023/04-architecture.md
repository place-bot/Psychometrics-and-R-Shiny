# RMSNorm、SwiGLU、RoPE 与 GQA

## 1. 一个 Llama 2 block

对输入 \(\mathbf X\)，使用 Pre-Norm 残差：

\[
\mathbf H
=
\mathbf X
+
\operatorname{Attention}
\left(\operatorname{RMSNorm}(\mathbf X)\right),
\]

\[
\mathbf Y
=
\mathbf H
+
\operatorname{SwiGLU}
\left(\operatorname{RMSNorm}(\mathbf H)\right).
\]

## 2. RMSNorm

对向量 \(\mathbf x\in\mathbb R^d\)：

\[
\operatorname{RMS}(\mathbf x)
=
\sqrt{\frac{1}{d}\sum_{i=1}^{d}x_i^2+\epsilon},
\]

\[
\operatorname{RMSNorm}(\mathbf x)
=
\mathbf g\odot
\frac{\mathbf x}{\operatorname{RMS}(\mathbf x)}.
\]

它不减均值，只按 root mean square 缩放，再乘可学习权重 \(\mathbf g\)。官方代码先转 float 计算，之后转回原 dtype。

## 3. SwiGLU

官方实现为：

\[
\operatorname{FFN}(\mathbf x)
=
\mathbf W_2
\left[
\operatorname{SiLU}(\mathbf W_1\mathbf x)
\odot
(\mathbf W_3\mathbf x)
\right].
\]

其中

\[
\operatorname{SiLU}(z)=z\sigma(z).
\]

一条分支作为门，另一条分支传递内容，逐元素相乘后再投影回模型维度。

## 4. RoPE

Rotary Position Embedding 对 query 与 key 的二维坐标对执行与位置相关的旋转。将两个实数维度看成复数：

\[
q_{t,j}^{\mathbb C}
\longmapsto
q_{t,j}^{\mathbb C}e^{it\omega_j},
\]

\[
k_{s,j}^{\mathbb C}
\longmapsto
k_{s,j}^{\mathbb C}e^{is\omega_j}.
\]

旋转后内积依赖相对位移 \(t-s\)，把位置信息注入 attention，而无需单独学习绝对位置 embedding。

## 5. MHA、MQA 与 GQA

### Multi-Head Attention

每个 query head 都有自己的 K/V head：

\[
H_Q=H_K=H_V.
\]

### Multi-Query Attention

所有 query heads 共享一个 K/V head：

\[
H_K=H_V=1.
\]

### Grouped-Query Attention

多个 query heads 组成一组，共享一个 K/V head：

\[
1<H_{KV}<H_Q.
\]

若

\[
n_{\mathrm{rep}}=rac{H_Q}{H_{KV}},
\]

推理时可以逻辑重复 K/V 以配合每个 query head，但 cache 只需保存 \(H_{KV}\) 份。

## 6. GQA 为什么减少 KV cache

每层 cache 元素数大致为：

\[
2BT H_{KV}d_h,
\]

其中 2 代表 K 与 V。MHA 使用 \(H_{KV}=H_Q\)，GQA 使用更少 K/V heads，因此长上下文、大 batch 解码时显存与带宽压力更小。

论文在 34B 与 70B 使用 GQA。附录消融显示 GQA 在接近 MHA 质量的同时提高大 batch 推理吞吐。

## 7. Causal attention 与 cache

模型仍使用因果 mask：

\[
\operatorname{softmax}
\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_h}}
+\mathbf M_{\mathrm{causal}}
\right)
\mathbf V.
\]

训练可并行计算所有位置；生成仍逐 token。KV cache 避免重复计算历史 K/V，GQA进一步降低 cache 大小。

## 8. 4K context 的效果

相对 Llama 1 的 2K，Llama 2 训练到 4K。附录长上下文消融显示 4K 模型在 long-context tasks 上更强，普通任务总体没有明显损害。上下文长度翻倍会显著增加 dense attention 计算，GQA主要缓解生成 cache，不会把训练 attention 的 \(T^2\) 成本完全消除。
