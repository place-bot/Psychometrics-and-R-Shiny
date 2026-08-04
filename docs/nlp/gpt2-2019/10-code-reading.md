# 官方代码精读

## 1. 仓库范围

官方仓库 [openai/gpt-2](https://github.com/openai/gpt-2) 提供：

- TensorFlow 1.x 模型前向；
- byte-level BPE encoder/decoder；
- 条件与无条件生成；
- top-k、top-p 与 temperature 采样；
- 公开检查点下载脚本。

仓库没有提供论文级 WebText 训练管线和完整 benchmark 评测代码。因此它适合验证模型结构与生成，不足以一键复现论文训练和所有表格。

## 2. `default_hparams()`

默认配置为：

```python
n_vocab = 0
n_ctx = 1024
n_embd = 768
n_head = 12
n_layer = 12
```

真正运行时从检查点目录中的 `hparams.json` 覆盖这些值。

## 3. `attention_mask()`

代码构造下三角条件：

```python
i = tf.range(nd)[:, None]
j = tf.range(ns)
m = i >= j - ns + nd
```

在没有 past cache 时，\(nd=ns=T\)，于是

\[
m_{t,s}=\mathbb I(s\le t).
\]

masked logits 被减去约 \(10^{10}\)，softmax 后未来位置概率近似为 0。

## 4. `attn()` 的张量形状

输入：

\[
\mathbf X\in\mathbb R^{B\times T\times d}.
\]

一次线性投影产生拼接 QKV：

\[
\mathbf C\in\mathbb R^{B\times T\times 3d}.
\]

拆成多头后：

\[
\mathbf Q,\mathbf K,\mathbf V
\in
\mathbb R^{B\times H\times T\times d_h}.
\]

注意力权重形状：

\[
\mathbf A
\in
\mathbb R^{B\times H\times T_{\mathrm{dst}}\times T_{\mathrm{src}}}.
\]

## 5. `block()` 验证 Pre-LN

核心逻辑为：

```python
a, present = attn(norm(x, 'ln_1'), ...)
x = x + a
m = mlp(norm(x, 'ln_2'), ...)
x = x + m
```

LayerNorm 明确发生在 attention 和 MLP 之前，残差直接加回原状态。这对应论文的 pre-normalization 描述。

## 6. embedding 与输出共享

`model()` 创建：

```python
wpe = position_embedding
wte = token_embedding
h = gather(wte, X) + gather(wpe, positions)
```

最后 logits 使用：

```python
logits = tf.matmul(h_flat, wte, transpose_b=True)
```

因此输出层复用 \(\mathbf W_E^\top\)，没有单独的 vocabulary projection matrix。

## 7. KV cache

每层把当前 key 与 value 堆成 `present`：

\[
\text{present}
\in
\mathbb R^{B\times2\times H\times T\times d_h}.
\]

下一生成步将 past K/V 与当前 K/V 沿序列维拼接。这样已经计算过的前缀无需每次从头通过所有 attention 投影。

注意：cache 降低重复计算，但自回归 token 依赖仍存在。第 \(t+1\) 个 token 必须等第 \(t\) 个 token 生成后才能确定。

## 8. 采样代码

每步先做 temperature：

\[
\mathbf z' = \frac{\mathbf z}{\tau}.
\]

`top_k_logits` 把第 \(k\) 大 logit 以下的值设为约 \(-10^{10}\)。`top_p_logits` 按概率排序并保留累计质量达到阈值附近的最小候选集合。最后用 `tf.multinomial` 抽取一个 token。

## 9. 一个实现细节：top-p 是后续加入的

论文摘要实验明确使用 top-k；当前仓库还含 nucleus sampling。阅读代码时应区分“论文当时报告的实验配置”和“仓库后续补充的推理功能”。

## 10. 参数计数修正

仓库 README 说明，早期博客和论文中的参数计数有误。公开模型卡列出 124M、355M、774M 与 1.5B。写复现实验时应同时记录：

- 使用的检查点目录名；
- `hparams.json`；
- 实际参数统计方法；
- 论文原表使用的规模标签。
