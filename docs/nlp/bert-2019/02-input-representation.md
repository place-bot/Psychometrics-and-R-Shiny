# WordPiece、[CLS]、[SEP] 与三种 Embedding

## 1. 序列格式

单句：

\[
[\text{CLS}],\;A,\;[\text{SEP}].
\]

句对：

\[
[\text{CLS}],\;A,\;[\text{SEP}],\;B,\;[\text{SEP}].
\]

论文中的 “sentence” 可以是连续文本片段，不要求严格语言学句子。

## 2. WordPiece

词表约 30,000。低频词可拆成子词，例如

\[
\text{playing}\rightarrow
\text{play},\;\text{\#\#ing}.
\]

“##”标记该片段延续前一个词。MLM 原论文按 WordPiece token 位置采样，不是后来发布的 whole-word masking。

## 3. [CLS]

每条序列首位加入 `[CLS]`，顶层向量

\[
\mathbf C\in\mathbb R^H
\]

用于 NSP 与下游分类。它通过 self-attention 汇总全序列信息。未经任务微调的 \(\mathbf C\) 不必天然成为通用句向量；论文脚注明确提醒 NSP 训练的 C 需要微调。

## 4. [SEP]

`[SEP]` 标记句段边界。句对结尾也有一个 `[SEP]`。

## 5. 三种 embedding 相加

第 \(i\) 个输入向量：

\[
\mathbf e_i
=
\mathbf e_i^{\text{token}}
+
\mathbf e_i^{\text{segment}}
+
\mathbf e_i^{\text{position}}.
\]

- token embedding：WordPiece 身份；
- segment embedding：句段 A 或 B；
- position embedding：绝对位置。

BERT 原始位置 embedding 是可学习参数，最大长度 512；这与原 Transformer 的固定正弦位置不同。

## 6. Attention mask 与 segment id

attention mask 屏蔽 padding；segment id 区分 A/B。segment id 本身不会禁止跨句 attention。句对被拼成一条序列后，所有有效 token 可以相互关注，这为 NLI 和 QA 提供双向 cross-attention。

## 7. 输出

顶层 token 表示记为

\[
\mathbf T_i\in\mathbb R^H.
\]

分类通常读取 \(\mathbf C\)，序列标注与问答读取各 \(\mathbf T_i\)。
