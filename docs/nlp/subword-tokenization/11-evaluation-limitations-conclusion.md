# 评价、局限与结论

## 1. Tokenizer 评价指标

### Fertility

每个原始词平均产生多少 token：

\[
\operatorname{fertility}
=
\frac{\text{subword token 数}}
{\text{原始词数}}.
\]

越低通常意味着序列更短，但不能单独代表模型质量。

### 字符或字节覆盖率

测量 `[UNK]` rate、byte fallback rate，以及不同语言能否稳定 round-trip。

### Compression ratio

\[
R
=
\frac{\text{原始字符数或字节数}}
{\text{token 数}}.
\]

必须说明分子使用 Unicode code points、grapheme clusters 还是 UTF-8 bytes，否则跨语言比较不公平。

### 下游质量

最终还要比较 language-model loss、任务准确率、生成质量、训练速度和服务成本。token 数少并不保证表示更有用。

## 2. 多语言公平性

以英语主导语料训练的 tokenizer 往往为英语分配很多长 token，而低资源语言被切得更碎。后果包括：

- 相同含义占用更多上下文；
- 每个句子推理成本更高；
- 长距离依赖跨越更多 token；
- 低资源文字更多依赖字符或字节 fallback；
- 某些语言更早触及最大序列长度。

应按语言分别报告 fertility、bytes-per-token、UNK、延迟和任务质量。

## 3. 数字、代码与空白

Tokenizer 可能把数字按单个 digit、数位片段或整段切分。代码对空格、缩进、运算符和大小写高度敏感。选择 tokenizer 时要覆盖真实领域数据：

```text
1,000.25
student_id_0042
θ_i^(t)
缩进代码
URL 与邮箱
```

只在新闻英文上测得的压缩率不能代表数学、编程或教育题库内容。

## 4. 边界错误与 tokenization attack

不可见 Unicode、零宽字符、同形异码字符、异常空白和组合重音可能造成：

- 肉眼相同文本得到不同 IDs；
- moderation 规则与模型输入不一致；
- 关键词匹配被绕过；
- offset 和高亮错位；
- prompt 长度突然膨胀。

安全系统应在明确 normalization 后检查文本，并把实际送入模型的 token 序列纳入审计。

## 5. Vocabulary 越大并非越好

大 vocabulary 可以缩短序列，却会：

- 增加 embedding 和 output projection 参数；
- 让罕见长 token 的训练次数减少；
- 降低相似词之间的子词共享；
- 增加 tokenizer 训练和 softmax 成本。

最优词表规模依赖语料量、语言数量、模型大小、上下文和任务。

## 6. BPE 与 WordPiece 的局限

- 都是贪心或局部构造方法，不保证全局最优切分；
- 统计片段不保证符合词素和语义；
- 结果强烈依赖训练语料与 pre-tokenization；
- 确定性单一切分可能降低对拼写变化的稳健性；
- tokenizer 固化后，新领域词汇只能被旧单位拆分；
- 子词边界会影响 NER、抽取式问答和字符级评价。

Unigram language model、subword regularization、BPE dropout、byte fallback 和 vocabulary adaptation 分别尝试缓解其中一部分问题。

## 7. 对 CAT 与教育文本的启发

在题目生成、开放作答评分或教育对话系统中，应额外检查：

- 数学公式和 LaTeX 的 token 开销；
- 中英文混排、单位、题号与选项符号；
- 学生拼写错误和口语缩写；
- 专业术语、变量名和代码；
- 不同语言学生的上下文预算是否相近；
- token offset 能否准确回到学生原答案。

Tokenizer 会改变模型看到的序列，却不能取代测量模型、评分 rubric 或内容效度分析。

## 8. 最终结论

可以把两条路线压缩成：

```text
BPE
训练：合并高频 pair
编码：按 merge rank 重放合并

WordPiece
训练思想：选择能改善训练语料 likelihood 的单位
编码：在最终 vocabulary 上做最长匹配
```

GPT-2 在 BPE 前加入可逆 UTF-8 字节映射，形成 byte-level BPE；BERT 在 WordPiece 前加入 BasicTokenizer，并以 `##` 标记词内 continuation。

真正可复现的 tokenizer 从来不只是一个算法名，而是 normalization、pre-tokenization、subword model、vocabulary、special tokens 和 post-processing 的完整组合。

