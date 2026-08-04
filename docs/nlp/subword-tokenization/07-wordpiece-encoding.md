# BERT 的 WordPiece 编码

## 1. FullTokenizer 有两层

BERT 官方 `FullTokenizer` 先调用 BasicTokenizer，再对每个 basic token 调用 WordpieceTokenizer：

```text
raw text
  ↓ BasicTokenizer
basic tokens
  ↓ WordpieceTokenizer
word pieces
  ↓ vocabulary lookup
token IDs
```

只讨论 longest-match-first 会漏掉大小写、重音、标点和中文字符处理。

## 2. BasicTokenizer

原始 uncased BERT 的典型流程包括：

1. 删除无效或不需要的控制字符；
2. 统一空白；
3. 在 CJK 统一表意文字两侧加空格；
4. 小写化；
5. 通过 Unicode NFD 分解并去除 combining marks；
6. 把标点独立切出。

例如官方文档给出的思路是：

```text
John Johanson's,
→ john johanson ' s ,
→ john johan ##son ' s ,
```

cased 模型会保留大小写与重音，必须匹配相应 checkpoint 的 tokenizer 配置。

## 3. Greedy Longest-Match-First

对一个 basic token 的字符序列 \(c_1\cdots c_m\)，从位置 `start` 开始：

1. 先尝试直到词尾的最长 substring；
2. 若不在 vocabulary，逐步缩短右端；
3. 非词首候选添加 `##`；
4. 找到第一个词表项后移动 `start`；
5. 重复直到覆盖整个词。

伪代码：

```python
start = 0
pieces = []
while start < len(chars):
    end = len(chars)
    found = None
    while end > start:
        candidate = chars[start:end]
        if start > 0:
            candidate = "##" + candidate
        if candidate in vocab:
            found = candidate
            break
        end -= 1
    if found is None:
        return ["[UNK]"]
    pieces.append(found)
    start = end
```

## 4. `unaffable` 例子

若 vocabulary 含：

```text
un, ##aff, ##able
```

算法得到：

```text
unaffable
→ un | ##aff | ##able
```

第一段尝试完整词、`unaffabl`、……直到 `un`；第二段所有候选带 `##`，找到 `##aff`；最后找到 `##able`。

## 5. 为什么一个字符失败会让整词变 `[UNK]`

原始 BERT 实现若任一位置无法继续覆盖，会把整个 basic token 输出为 `[UNK]`，而不是保留已经找到的前缀再只替换剩余字符。

此外，长度超过 `max_input_chars_per_word` 的 basic token 也直接变成 `[UNK]`；官方默认上限为 200 个字符。

这与 byte-level BPE 的 fallback 不同。后者总能退回 UTF-8 字节单位。

## 6. 中文 BERT 的表现

BERT BasicTokenizer 会在每个 CJK 统一表意文字两侧加入空格，使这些汉字分别成为独立 basic token。WordPiece 不会跨越 basic-token 边界重新合并它们，因此原始 Chinese BERT 的连续汉字通常按字进入后续词表查找。

不能简单说“WordPiece 总是先做中文分词”。原始 BERT 主要是按 Unicode 范围隔开汉字，并未调用一个外部中文词法分词器。

## 7. 添加 `[CLS]` 与 `[SEP]`

句子对任务通常形成：

\[
[\mathrm{CLS}]
\;A\;
[\mathrm{SEP}]
\;B\;
[\mathrm{SEP}].
\]

这属于 post-processing，而非 WordPiece longest-match 算法。MLM 中的 `[MASK]` 也由训练样本构造加入。

## 8. 标签对齐

NER 中一个原始词可能拆成多个 pieces：

```text
Johanson → johan | ##son
```

常见策略包括：

- 只在第一个 piece 计算标签损失；
- 把标签复制到全部 pieces，并调整 BIO 规则；
- 保存 `word_ids` 或 offset mapping 做聚合。

训练与评价必须采用同一对齐规则，否则 token-level 指标无法比较。
