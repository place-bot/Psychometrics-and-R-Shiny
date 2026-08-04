# 子词分词专题：BPE、Byte-level BPE 与 WordPiece

神经网络不能直接读取字符串。文本必须先经过 tokenizer，变成有限词表中的整数 ID。BPE 和 WordPiece 都在“整词”与“单字符”之间寻找子词单位，使常见片段可以合并成较长 token，同时让少见词仍能被拆开处理。

!!! info "先把常见表述说准确"
    “BPE 广泛用于 GPT，WordPiece 用于 BERT”适合作为入门索引，但需要补充两个限定：

    - GPT-2 使用的是 **byte-level BPE**：先把 UTF-8 字节可逆地映射成可处理符号，再应用 BPE 合并；后续 GPT tokenizer 沿用了字节级、merge-based 的总体路线，但具体正则、词表和特殊 token 会变化。
    - BERT 使用 **BasicTokenizer + WordPieceTokenizer**：规范化、大小写和标点切分先发生，WordPiece 再对每个预切分词做 greedy longest-match-first。

## 一张总图

```text
原始文本
   ↓ normalization
规范化文本
   ↓ pre-tokenization
局部片段 / 单词边界
   ↓ subword model
子词 token
   ↓ vocabulary lookup
token IDs
   ↓ special-token post-processing
模型输入
```

BPE 与 WordPiece 主要描述中间的 **subword model**。它们的实际输出还受到 normalization、pre-tokenization、空格表示和特殊 token 规则影响。

## 阅读路线

1. [为什么需要子词：整词、字符与固定词表的矛盾](01-why-subwords.md)
2. [Tokenizer 的完整流水线与每层职责](02-tokenizer-pipeline.md)
3. [BPE 从数据压缩到 NLP 词表学习](03-bpe-training.md)
4. [BPE 编码：怎样按 merge rank 切分新文本](04-bpe-encoding.md)
5. [GPT-2 Byte-level BPE：字节、正则与可逆编码](05-byte-level-bpe.md)
6. [WordPiece 词表训练：最大似然思想与公开证据边界](06-wordpiece-training.md)
7. [BERT WordPiece 编码：BasicTokenizer 与最长匹配](07-wordpiece-encoding.md)
8. [BPE 与 WordPiece 的逐项比较](08-bpe-wordpiece-comparison.md)
9. [完整手算：同一小语料怎样产生不同合并](09-worked-example.md)
10. [官方代码精读与现代实现](10-code-implementation.md)
11. [怎样评价 tokenizer、局限与结论](11-evaluation-limitations-conclusion.md)
12. [论文、官方代码与参考资料](references.md)

## 学完后要能回答的问题

- 子词方法为什么能缓解 OOV，却不能自动理解词法结构？
- 原始 BPE、NLP BPE 和 byte-level BPE 有什么关系？
- WordPiece 的词表训练与分词阶段为什么要分开说？
- GPT-2 中的 `Ġ` 和 BERT 中的 `##` 分别表示什么？
- 为什么换 tokenizer 会改变上下文容量、速度和模型参数？
- 为什么同一字符串在不同 normalization 和 pre-tokenization 下会得到不同 ID？

