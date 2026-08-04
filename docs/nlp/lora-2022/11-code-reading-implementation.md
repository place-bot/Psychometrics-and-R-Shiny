# `loralib` 代码精读与从零实现

## 1. 官方文件

- `loralib/layers.py`：Embedding、Linear、MergedLinear、ConvLoRA；
- `loralib/utils.py`：冻结非 LoRA 参数与筛选 state dict；
- `examples/NLU`：RoBERTa/DeBERTa；
- `examples/NLG`：GPT-2。

## 2. `Linear` 核心

官方实现创建

\[
A\in\mathbb R^{r\times d_{\text{in}}},
\qquad
B\in\mathbb R^{d_{\text{out}}\times r},
\]

设置 `weight.requires_grad=False`，缩放 `lora_alpha / r`，前向加入

```python
(dropout(x) @ A.T @ B.T) * scaling
```

## 3. 从零实现

```python
import math
import torch
from torch import nn
from torch.nn import functional as F

class LoRALinear(nn.Linear):
    def __init__(self, in_features, out_features,
                 r=8, alpha=8, dropout=0.0, bias=True):
        super().__init__(in_features, out_features, bias=bias)
        self.r = r
        self.scaling = alpha / r
        self.lora_dropout = nn.Dropout(dropout)
        self.weight.requires_grad = False

        self.lora_A = nn.Parameter(torch.empty(r, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, r))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

    def forward(self, x):
        base = F.linear(x, self.weight, self.bias)
        update = F.linear(
            F.linear(self.lora_dropout(x), self.lora_A),
            self.lora_B,
        )
        return base + self.scaling * update

    @torch.no_grad()
    def merged_weight(self):
        return self.weight + self.scaling * (
            self.lora_B @ self.lora_A
        )
```

## 4. 官方 merge

`model.eval()` 将 \(sBA\) 加入 `weight.data`，`model.train()` 再减去，并用 `merged` 标记防止重复操作。对 PyTorch 的 `nn.Linear` 权重方向要注意转置约定。

## 5. 工具函数

`mark_only_lora_as_trainable` 依据参数名 `lora_` 冻结其他权重，并支持 `none`、`all`、`lora_only` 三种 bias 策略。`lora_state_dict` 用同一策略筛选 checkpoint。

## 6. 验证

```python
layer.eval()
y_unmerged = layer(x)
w = layer.merged_weight()
y_merged = F.linear(x, w, layer.bias)
torch.testing.assert_close(y_unmerged, y_merged)
```

还应检查：

- 初始 LoRA 输出为 0；
- 只有 LoRA 参数有梯度；
- merge/unmerge 循环稳定；
- fused QKV 只更新指定切片；
- checkpoint 加载到准确的基座版本；
- 分布式训练没有意外解冻基座。
