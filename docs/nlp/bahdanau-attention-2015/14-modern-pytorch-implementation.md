# 现代 PyTorch 实现

下面给出结构清晰的现代实现骨架。编码器使用双向 `nn.GRU`，attention 严格对应 additive score；解码器把上下文拼入 GRU 输入。该版本保持论文级信息流，框架 GRU 的内部方程与历史 GroundHog 单元可能存在约定差异。

## 1. Additive attention

```python
import torch
from torch import nn

class AdditiveAttention(nn.Module):
    def __init__(self, state_dim, annotation_dim, align_dim):
        super().__init__()
        self.state_proj = nn.Linear(state_dim, align_dim, bias=False)
        self.source_proj = nn.Linear(annotation_dim, align_dim, bias=False)
        self.energy = nn.Linear(align_dim, 1, bias=False)

    def forward(self, state, annotations, source_mask):
        # state:       [batch, state_dim]
        # annotations: [batch, source_len, annotation_dim]
        # source_mask: [batch, source_len], True = valid
        query = self.state_proj(state).unsqueeze(1)
        keys = self.source_proj(annotations)
        scores = self.energy(torch.tanh(query + keys)).squeeze(-1)
        scores = scores.masked_fill(~source_mask, float("-inf"))
        alpha = torch.softmax(scores, dim=-1)
        context = torch.bmm(alpha.unsqueeze(1), annotations).squeeze(1)
        return context, alpha
```

形状检查：

\[
[B,1,n']+[B,T_x,n']
\rightarrow[B,T_x,n']
\rightarrow[B,T_x]
\rightarrow[B,2n].
\]

## 2. 双向编码器

```python
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, pad_id):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=pad_id)
        self.gru = nn.GRU(
            embed_dim,
            hidden_dim,
            batch_first=True,
            bidirectional=True,
        )

    def forward(self, source):
        embedded = self.embedding(source)
        annotations, final = self.gru(embedded)
        # annotations: [B, Tx, 2H]
        # final: [2, B, H]
        return annotations, final
```

正式训练可配合 `pack_padded_sequence`，避免 padding 进入递归计算。

## 3. 一个解码步骤

```python
class DecoderStep(nn.Module):
    def __init__(self, vocab_size, embed_dim, state_dim,
                 annotation_dim, align_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.attention = AdditiveAttention(
            state_dim, annotation_dim, align_dim
        )
        self.gru = nn.GRUCell(
            embed_dim + annotation_dim, state_dim
        )
        self.readout = nn.Sequential(
            nn.Linear(state_dim + embed_dim + annotation_dim, state_dim),
            nn.Tanh(),
            nn.Linear(state_dim, vocab_size),
        )

    def forward(self, previous_token, previous_state,
                annotations, source_mask):
        previous_embedding = self.embedding(previous_token)
        context, alpha = self.attention(
            previous_state, annotations, source_mask
        )
        state = self.gru(
            torch.cat([previous_embedding, context], dim=-1),
            previous_state,
        )
        logits = self.readout(torch.cat(
            [state, previous_embedding, context], dim=-1
        ))
        return logits, state, alpha
```

若追求论文方程逐项复现，应自定义 GRUCell，让 \(\mathbf c_i\) 分别通过 \(\mathbf C,\mathbf C_r,\mathbf C_z\) 进入候选与两个门，并将输出层改为论文的 maxout。

## 4. 稳定性检查

```python
context, alpha = attention(state, annotations, source_mask)

assert torch.isfinite(context).all()
assert torch.allclose(
    alpha.sum(dim=-1),
    torch.ones(alpha.size(0), device=alpha.device),
    atol=1e-6,
)
assert torch.equal(alpha.masked_select(~source_mask),
                   torch.zeros_like(alpha.masked_select(~source_mask)))
```

每个样本必须至少有一个有效源 token；全被 mask 的一行会导致 softmax 产生 `NaN`。

## 5. Teacher-forcing 循环

```python
state = initial_state
loss = 0.0

for i in range(1, target.size(1)):
    logits, state, alpha = decoder_step(
        target[:, i - 1],
        state,
        annotations,
        source_mask,
    )
    loss = loss + criterion(logits, target[:, i])
```

循环清楚显示目标位置之间的状态依赖。可将 attention 内部源位置、batch 和词表运算向量化，但无法同时计算所有目标状态。

## 6. 复现清单

- 固定随机种子并报告多次运行；
- 明确 tokenizer、词表和特殊 token；
- 记录最大句长与过滤规则；
- 核对 source/target mask；
- 使用全局梯度裁剪；
- 保存开发集 NLL 与 BLEU；
- 报告 beam width 和长度惩罚；
- 分开报告论文级复现与现代化改动；
- 用小 batch 验证 attention 行和为 1；
- 检查 EOS 后的目标损失被 mask。

## 本页小结

现代实现的关键是保存论文的信息依赖与形状：旧状态查询全部源注释，masked softmax 得到上下文，上下文再进入状态与词表读出。框架自带 GRU 提供简洁实现，自定义 cell 才能逐项匹配历史方程。
