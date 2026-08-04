# Google 原始代码精读与现代实现

## 1. 文件地图

| 文件 | 职责 |
|---|---|
| `modeling.py` | BertConfig、embedding、Transformer encoder |
| `create_pretraining_data.py` | 文档切片、NSP、15% mask、TFRecord |
| `run_pretraining.py` | MLM/NSP heads 与联合 loss |
| `optimization.py` | AdamW、warmup、线性衰减 |
| `run_classifier.py` | GLUE 类分类 |
| `run_squad.py` | span 起止预测 |
| `tokenization.py` | BasicTokenizer 与 WordPiece |

仓库已归档，代码基于 TensorFlow 1.x。

## 2. 数据生成

默认参数包括：

```text
dupe_factor = 10
masked_lm_prob = 0.15
short_seq_prob = 0.1
```

`create_masked_lm_predictions` 排除特殊 token，打乱候选位置，按 80/10/10 产生输入与原始标签。

## 3. 模型输入

`BertModel` 接收：

- `input_ids [B,T]`；
- `input_mask [B,T]`；
- `token_type_ids [B,T]`。

embedding postprocessor 相加 token-type 与 position embedding，随后 LayerNorm 和 dropout。

## 4. 预训练头

`get_masked_lm_output` 只 gather 被选位置，执行 dense + GELU + LayerNorm，并共享输入 embedding 权重。`get_next_sentence_output` 对 pooled `[CLS]` 做 2 类分类。总 loss 直接相加。

## 5. 现代 MLM collator 伪代码

```python
selected = random_uniform(tokens.shape) < 0.15
selected &= ~special_token_mask
labels = tokens.clone()
labels[~selected] = -100

branch = random_uniform(tokens.shape)
tokens[selected & (branch < 0.80)] = mask_id
tokens[selected & (branch >= 0.80) & (branch < 0.90)] = random_ids
# 最后 10% 保持原 token，labels 仍保留
```

## 6. 最小微调

```python
class BertClassifier(nn.Module):
    def __init__(self, bert, hidden, classes):
        super().__init__()
        self.bert = bert
        self.classifier = nn.Linear(hidden, classes)

    def forward(self, input_ids, attention_mask, token_type_ids):
        output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )
        cls = output.last_hidden_state[:, 0]
        return self.classifier(cls)
```

## 7. 验证清单

- tokenizer/cased 配置与 checkpoint 匹配；
- `[CLS]/[SEP]` 与 segment id 正确；
- padding 未进入 attention 与 loss；
- MLM labels 保留原 token；
- 只在 15% 位置计算 MLM；
- 80/10/10 的 10% 保持项仍有标签；
- 长序列没有超过 position embedding；
- SQuAD offset 从 WordPiece 映射回原文本；
- 微调学习率、seed 和重启策略有记录。
