# Vocabulary 与 Tokenization

## 1. 这正是推荐语句指向的章节

该书 Chapter 3 专门讨论 Vocabulary and Tokenization，目录覆盖：

```text
Vocabulary
→ Tokenizer
→ Normalization
→ Pre-tokenization
→ BPE / WordPiece
→ Special Tokens
```

它的价值在于把 BPE 和 WordPiece 放回完整输入流水线，而不只讲一个 pair-merge 算法。

## 2. Vocabulary 是模型参数的一部分

若词表大小为 \(V\)，hidden size 为 \(d\)，embedding 参数规模为：

\[
P_{\mathrm{embed}}=Vd.
\]

大词表可以缩短序列，但增加 embedding 与输出层；小词表降低参数，却会增加 token 数和 attention 成本。

## 3. Tokenizer 是函数组合

\[
T=P_{\mathrm{post}}
\circ L_{\mathrm{id}}
\circ S_{\mathrm{subword}}
\circ P_{\mathrm{pre}}
\circ N.
\]

其中 normalization、pre-tokenization、subword model、ID lookup 和 special-token post-processing 都影响最终输入。

## 4. BPE 与 WordPiece 的书中位置

BPE 训练通常选择最高频相邻 pair：

\[
(a^*,b^*)=\arg\max_{a,b}F(a,b).
\]

WordPiece 的原始思想是选择能够最大改善语料 likelihood 的新单位；BERT runtime 则对最终 vocabulary 做 longest-match-first。

详细推导、GPT-2 byte mapping、`Ġ`、BERT `##` 和完整手算已放在 [子词分词专题](../subword-tokenization/index.md)。

## 5. Special token 连接模型目标与应用协议

特殊 token 可能表示：

- 文档开始与结束；
- padding；
- BERT classification 和 sentence separation；
- masked prediction；
- system/user/assistant 角色；
- tool call 与 observation 边界。

它们不是普通字符串装饰。模型必须在训练中学过对应 ID 的行为，推理模板也必须准确复现。

## 6. Tokenizer 对应用行为的影响

| 行为 | Tokenizer 影响 |
|---|---|
| 上下文容量 | 相同原文产生多少 token |
| 延迟与费用 | prefill 长度与 API token 计费 |
| 多语言公平性 | 不同语言 fertility 是否失衡 |
| 数字与代码 | 数位、缩进、符号怎样切分 |
| Span 任务 | token offset 能否准确回到原文 |
| 安全 | Unicode 和空白变体是否绕过检查 |
| 继续训练 | 新领域术语是否被过度碎片化 |

## 7. 为什么不能给已有模型随便换 tokenizer

embedding 第 \(i\) 行绑定训练时 token ID \(i\)：

\[
e_i=E[i,:].
\]

新 tokenizer 即使 vocabulary size 相同，也会重新定义 ID 语义。直接替换相当于把输入送到错误的 embedding 行。

安全做法包括保持原 tokenizer、受控增加新 token 并初始化 embedding，或重新训练/继续预训练模型。

## 8. CAT 场景检查

教育文本要单独测试公式、选项编号、代码、单位、中英文混排、拼写错误和学生口语。Tokenizer efficiency 可能影响不同语言学生能使用的有效上下文，因此属于系统公平性的一部分。

