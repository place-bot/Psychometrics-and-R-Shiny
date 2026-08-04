# Tokenizer 的完整流水线

## 1. 只说“使用 BPE”还不够

两个 tokenizer 即使都采用 BPE，也可能因为大小写、Unicode、空格和 pre-tokenization 不同而输出完全不同的 ID。完整 tokenizer 可以写成函数复合：

\[
T
=
P_{\mathrm{post}}
\circ L_{\mathrm{id}}
\circ S_{\mathrm{subword}}
\circ P_{\mathrm{pre}}
\circ N,
\]

其中：

| 符号 | 阶段 | 作用 |
|---|---|---|
| \(N\) | Normalizer | Unicode 规范化、大小写、重音和空白处理 |
| \(P_{\mathrm{pre}}\) | Pre-tokenizer | 决定空格、标点或正则边界 |
| \(S_{\mathrm{subword}}\) | Subword model | BPE、WordPiece 或 Unigram 切分 |
| \(L_{\mathrm{id}}\) | Vocabulary lookup | token 字符串映射到整数 ID |
| \(P_{\mathrm{post}}\) | Post-processor | 加 `[CLS]`、`[SEP]`、BOS、EOS 等 |

## 2. Normalization

Normalization 可能执行：

- Unicode NFC、NFD、NFKC 或 NFKD；
- 大写转小写；
- 去除组合重音符；
- 控制字符过滤；
- 多种空白统一；
- 全角与兼容字符转换。

规范化可能不是可逆的。例如 uncased BERT 把 `Café` 小写并去重音后可能得到 `cafe`，token IDs 无法恢复原始大小写和重音。

## 3. Pre-tokenization

Pre-tokenizer 决定 subword model 可以在哪些边界内合并。常见做法包括：

- 按空格分词；
- 把标点独立出来；
- 对中文字符两侧加空格；
- 用正则区分字母、数字、缩写和标点；
- 把空格绑定到后一个片段。

GPT-2 的 byte-level BPE 并非直接让所有字节在整篇文档中任意合并。它先用正则找到局部 token，再对每个局部片段应用字节映射与 BPE。

## 4. Subword model

这一阶段决定局部片段怎样分解为词表单位：

```text
BPE：按照训练得到的 merge rank 反复合并
WordPiece：从当前位置寻找词表中的最长可用片段
Unigram：在候选子词概率模型下搜索高概率切分
```

训练 tokenizer 和使用 tokenizer 是两种不同算法。训练阶段学习词表或合并规则；编码阶段固定这些资产，不再重新统计输入文本。

## 5. Special tokens

特殊 token 由模型训练目标定义，不应靠字符串猜测：

| 模型路线 | 常见特殊 token |
|---|---|
| BERT | `[PAD]`、`[UNK]`、`[CLS]`、`[SEP]`、`[MASK]` |
| GPT-2 | `<|endoftext|>`；原始 GPT-2 也把它用于文档边界 |
| 现代 chat model | BOS、EOS、system/user/assistant、tool call 边界等 |

特殊 token 的文本形式、ID 和是否自动添加都属于 tokenizer 配置。

## 6. Offset mapping

序列标注、抽取式问答和高亮需要把 token 映射回原文字符区间：

\[
(t_i)\longleftrightarrow [a_i,b_i).
\]

Normalization 会改变字符，byte-level token 又以 UTF-8 字节为基础，因此 offset 不能仅靠 token 字符串长度重建。现代 fast tokenizer 会在流水线中追踪对齐关系。

## 7. Round-trip 的两种标准

### 字节可逆

\[
\operatorname{decode}(\operatorname{encode}(x))=x.
\]

GPT-2 byte-level BPE 的字节映射支持这种目标。

### 规范化后可逆

\[
\operatorname{decode}(\operatorname{encode}(x))=N(x).
\]

若 tokenizer 主动 lowercasing 或去重音，只能要求恢复规范化后的文本。测试 tokenizer 时应明确采用哪一种标准。

