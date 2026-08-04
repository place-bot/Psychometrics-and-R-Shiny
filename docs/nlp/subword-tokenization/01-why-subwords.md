# 为什么需要子词单位

## 1. 语言是开放的，模型词表是固定的

训练好的模型通常有固定词表：

\[
\mathcal V=\{v_1,v_2,\ldots,v_{|\mathcal V|}\}.
\]

tokenizer 把字符串 \(x\) 映射为 ID 序列：

\[
T(x)=(t_1,t_2,\ldots,t_n),
\qquad t_i\in\{1,\ldots,|\mathcal V|\}.
\]

自然语言却会不断出现新姓名、拼写变化、数字、网址、术语和复合词。若词表单位只允许完整单词，训练后出现的新词无法映射到已有 ID。

## 2. 三种粒度的取舍

| 粒度 | 优势 | 代价 |
|---|---|---|
| 整词 | 序列短，常见词语义集中 | 词表巨大，长尾词与新词成为 OOV |
| 字符 / 字节 | 基础词表小，覆盖能力强 | 序列长，模型要跨更多位置组合词义 |
| 子词 | 高频片段较长、低频片段可拆 | 切分由统计和规则决定，边界未必符合语言学形态 |

子词方法的核心折中是：

\[
\text{高频字符串}\longrightarrow\text{较少 token},
\]

\[
\text{低频字符串}\longrightarrow\text{较多但可表示的 token}.
\]

例如一个词表可能把 `playing` 编码为 `play + ing`，把少见名称拆成更短片段。模型通过共享 `play` 或 `ing` 的 embedding，在相关词之间共享一部分统计强度。

## 3. OOV 的两种含义

### 词级 OOV

完整单词不在词表中。子词算法通常能把它拆成已知单位，因此避免整词 `[UNK]`。

### 基础字母表 OOV

连最小单位也不在初始 alphabet 中。字符级 BPE 或 WordPiece 仍可能遇到这种情况；byte-level 方法以 256 个字节为基础，对任意 UTF-8 字节序列都有表示路径。

“没有 OOV”只保证能编码，不保证编码高效或模型理解良好。一个少见字符可能被拆成多个字节 token，训练中又几乎没有出现，对应表示仍会很弱。

## 4. Token 数直接影响模型成本

设原文经过 tokenizer 后长度为 \(n\)。标准 self-attention 的主要矩阵规模约为：

\[
O(n^2).
\]

同一段中文、代码或数学文本在两个 tokenizer 下可能分别占 500 和 800 token。后者不仅更快用完上下文，还增加 prefill 计算与 KV cache。

## 5. 词表大小也有成本

embedding 矩阵形状通常为：

\[
E\in\mathbb R^{|\mathcal V|\times d},
\]

其中 \(d\) 是 hidden size。若输入 embedding 与输出 projection 不共享参数，词表相关参数还会出现两次。增大词表能缩短序列，却增加 embedding、输出层和 softmax 成本。

Tokenizer 设计因此同时优化两个方向：

\[
\text{序列长度}
\quad\text{与}\quad
\text{词表规模}.
\]

## 6. 子词不等于词素分析

BPE 和 WordPiece 从频率或似然目标学习字符串片段，没有显式使用词根、前缀、后缀或语法规则。`un + happy` 可能恰好符合形态学，也可能被切成 `unh + app + y`。

统计子词的直接目标是改善有限词表下的编码和模型训练，不保证产生语言学上正确的 morphemes。

