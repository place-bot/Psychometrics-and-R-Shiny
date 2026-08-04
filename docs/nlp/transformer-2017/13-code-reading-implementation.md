# Tensor2Tensor 与现代 PyTorch 实现

## 1. 原始代码位置

论文指向 [TensorFlow Tensor2Tensor](https://github.com/tensorflow/tensor2tensor)。关键模块包括：

- `tensor2tensor/models/transformer.py`：encoder、decoder 与 hparams；
- `tensor2tensor/layers/common_attention.py`：dot-product 与 multi-head attention；
- `tensor2tensor/layers/common_layers.py`：pre/postprocess、LayerNorm；
- 数据生成器：subword vocabulary、length bucket 与 batch。

仓库后来持续演化，最新代码包含 Pre-LN 等后续配置。读取时需将 `transformer_base_v1`/论文配置与现代默认项分开。

## 2. 最小 attention

```python
import math
import torch
from torch import nn

def scaled_attention(q, k, v, mask=None):
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.size(-1))
    if mask is not None:
        scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    output = weights @ v
    return output, weights
```

## 3. 多头 reshape

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, heads=8):
        super().__init__()
        assert d_model % heads == 0
        self.heads = heads
        self.d_head = d_model // heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch, length, width = x.shape
        qkv = self.qkv(x).view(
            batch, length, 3, self.heads, self.d_head
        )
        q, k, v = qkv.unbind(dim=2)
        q, k, v = [
            t.transpose(1, 2) for t in (q, k, v)
        ]
        y, weights = scaled_attention(q, k, v, mask)
        y = y.transpose(1, 2).contiguous().view(
            batch, length, width
        )
        return self.out(y), weights
```

cross-attention 需要分别对 decoder query 与 encoder key/value 投影，不能复用只接收一个 `x` 的简化接口。

## 4. Causal mask

```python
def causal_mask(length, device):
    return torch.ones(
        length, length, dtype=torch.bool, device=device
    ).tril()[None, None, :, :]
```

与 padding mask 合并时要广播成 \([B,1,T_q,T_k]\)。

## 5. 原论文 Post-LN block

```python
class PostNormBlock(nn.Module):
    def __init__(self, d_model, sublayer, dropout=0.1):
        super().__init__()
        self.sublayer = sublayer
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, **kwargs):
        y = self.sublayer(x, **kwargs)
        if isinstance(y, tuple):
            y = y[0]
        return self.norm(x + self.dropout(y))
```

## 6. 测试清单

- 每个 attention 行权重和为 1；
- padding 与未来位置权重为 0；
- QK 缩放使用 \(d_k\)，不能误用 \(d_{\text{model}}\)；
- head reshape 后 token 次序不变；
- residual 两端维度一致；
- 目标 embedding 确实右移；
- loss 忽略 target padding；
- 训练与推理位置编号一致；
- beam/KV cache 正确重排。

## 7. 与 LoRA 的代码接口

QKV 与输出投影都是 `nn.Linear`。LoRA 会把

\[
\mathbf x\mathbf W^\top
\]

改为

\[
\mathbf x\mathbf W_0^\top
+
\frac{\alpha}{r}\mathbf x\mathbf A^\top\mathbf B^\top,
\]

并冻结 \(\mathbf W_0\)。下一专题将逐行实现。
