# 官方代码精读与现代实现

## 1. GPT-2 `encoder.py`

OpenAI 官方实现的关键对象包括：

| 对象 | 作用 |
|---|---|
| `bytes_to_unicode()` | 建立 256 个字节到可打印 Unicode 符号的可逆表 |
| regex pattern | 把输入切成缩写、字母、数字、符号和空白片段 |
| `bpe_ranks` | 把有序 merge list 映射为 rank |
| `bpe()` | 每轮合并当前 rank 最小的相邻 pair |
| `encoder` / `decoder` | token string 与 ID 双向映射 |
| cache | 复用相同片段的确定性 BPE 结果 |

编码调用链可概括为：

```python
for piece in regex_pretokenize(text):
    byte_symbols = reversible_byte_map(piece.encode("utf-8"))
    subtokens = apply_ranked_bpe(byte_symbols, merge_ranks)
    ids.extend(vocab[token] for token in subtokens)
```

解码则反向拼接、逆 byte map，再做 UTF-8 decode。

## 2. BERT `tokenization.py`

Google 官方实现分三层：

| 类 | 职责 |
|---|---|
| `BasicTokenizer` | 清洗、CJK 间隔、lowercase、去重音、标点切分 |
| `WordpieceTokenizer` | 对每个 basic token 做 greedy longest-match-first |
| `FullTokenizer` | 串联两层并完成 token/ID 映射 |

WordpieceTokenizer 的关键控制逻辑是：

```python
while start < len(chars):
    end = len(chars)
    while end > start:
        candidate = make_candidate(chars[start:end], is_continuation=start > 0)
        if candidate in vocab:
            break
        end -= 1
```

若这一位置没有任何候选匹配，整段 basic token 输出 `[UNK]`。

## 3. 一个最小 BPE 编码器

下面的教学实现假设输入已经是字符序列：

```python
def adjacent_pairs(symbols):
    return set(zip(symbols, symbols[1:]))

def encode_bpe(text, merge_ranks):
    symbols = tuple(text)
    while len(symbols) > 1:
        candidates = adjacent_pairs(symbols)
        ranked = [p for p in candidates if p in merge_ranks]
        if not ranked:
            break
        best = min(ranked, key=merge_ranks.get)

        merged = []
        i = 0
        while i < len(symbols):
            if i + 1 < len(symbols) and symbols[i:i+2] == best:
                merged.append(best[0] + best[1])
                i += 2
            else:
                merged.append(symbols[i])
                i += 1
        symbols = tuple(merged)
    return list(symbols)
```

真实实现还需要 pre-tokenization、字节映射、cache、特殊 token、错误处理和 ID 映射。

## 4. 一个最小 WordPiece 编码器

```python
def encode_wordpiece(word, vocab, prefix="##", unk="[UNK]"):
    pieces = []
    start = 0
    while start < len(word):
        match = None
        for end in range(len(word), start, -1):
            candidate = word[start:end]
            if start > 0:
                candidate = prefix + candidate
            if candidate in vocab:
                match = candidate
                start = end
                pieces.append(candidate)
                break
        if match is None:
            return [unk]
    return pieces
```

它展示的是 BERT-style runtime segmentation，不是 WordPiece vocabulary trainer。

## 5. Hugging Face Tokenizers 组件化实现

现代 `tokenizers` 库把流水线拆成可组合组件：

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
trainer = BpeTrainer(
    vocab_size=30_000,
    special_tokens=["[UNK]", "[PAD]"],
)
tokenizer.train(["corpus.txt"], trainer)
```

若要复现 GPT-2 或 BERT，应优先加载原 checkpoint 的 tokenizer，而不是仅选择同名 model class。默认参数、normalizer 和 pre-tokenizer 不同就可能产生另一套 tokenizer。

## 6. 必须保存的复现资产

```text
tokenizer.json 或等价组件配置
vocabulary
ordered BPE merges（若需要）
normalization 配置
pre-tokenization 配置
special token IDs
post-processing / chat template
library version 与文件 hash
```

只保存 `vocab.txt` 对原始 BERT runtime 通常足够重建 WordPiece vocabulary lookup，但仍需同时记录 cased/uncased 与 BasicTokenizer 行为。

## 7. 安全与正确性检查

- 不从不可信仓库执行自定义 tokenizer 代码；
- 固定 model 和 tokenizer revision；
- 检查 special token 是否被普通 normalization 改写；
- 对空字符串、超长词、控制字符、emoji、组合字符和无效 UTF-8 做测试；
- 保存 offset mapping 并验证 span 对齐；
- 模型部署前比较 slow 与 fast tokenizer 的输出一致性。

