# BPE 与 WordPiece 逐项比较

## 1. 核心差异表

| 维度 | Merge-based BPE | BERT-style WordPiece |
|---|---|---|
| 训练起点 | 字符或字节等基础单位 | 词首与词内字符单位 |
| 合并选择 | 通常选最高频相邻 pair | 以最大 likelihood 改善为原始思想；常见实现用归一化 pair score |
| 运行时资产 | vocabulary + ordered merge list | 主要是最终 vocabulary |
| 新文本编码 | 反复应用最低 merge rank | greedy longest-match-first |
| 词内标记 | 依实现使用 `</w>`、`Ġ`、`▁` 等 | BERT 常用 `##` 表示 continuation |
| 未知字符 | 字符版可能 OOV；byte-level 版可回退到字节 | 原始 BERT 可能把整个 basic token 变成 `[UNK]` |
| 典型模型 | GPT-2、RoBERTa 的 byte-level BPE 等 | BERT、DistilBERT、MobileBERT 等 |

## 2. 共同点

两者都：

- 从小单位建立有限 vocabulary；
- 让高频片段获得独立 token；
- 把少见词拆成较小单位；
- 在词表规模和序列长度之间折中；
- 不保证产生语言学词素；
- 需要与 normalization、pre-tokenization 和 special tokens 一起定义。

## 3. “选择哪个 pair”不同

BPE：

\[
\operatorname{score}_{\mathrm{BPE}}(a,b)=F(a,b).
\]

常见 WordPiece 近似：

\[
\operatorname{score}_{\mathrm{WP}}(a,b)
=
\frac{F(a,b)}{F(a)F(b)}.
\]

因此 BPE 偏爱绝对出现次数高的 pair；WordPiece-like score 会惩罚边际频率很高的组成部分。

## 4. “怎样编码”不同

### BPE

编码受 merge order 约束：

```text
当前相邻 pair → 查 rank → 先合并 rank 最小者
```

### WordPiece

编码只需要当前 vocabulary：

```text
当前位置 → 取词表中最长可用前缀 → 移到下一位置
```

因此即使最终 vocabulary 字符串集合相同，两种运行时算法也可能给出不同切分。

## 5. `Ġ`、`##` 与 `▁` 不应混淆

| 表面符号 | 常见来源 | 含义 |
|---|---|---|
| `Ġcat` | GPT-2 byte mapping | 底层片段通常含前导空格字节 |
| `##ing` | BERT WordPiece | token 位于同一 basic token 的非首位置 |
| `▁cat` | SentencePiece | `▁` 通常表示规范化后的空格边界 |

这些符号属于 tokenizer 的内部文本表示，不一定出现在用户原文。

## 6. 算法名和软件库是不同层次

- BPE、WordPiece、Unigram 是 subword model；
- SentencePiece 是可从 raw text 训练和解码的 tokenizer 软件，并支持 BPE 与 Unigram；
- Hugging Face Tokenizers 是组合 normalizer、pre-tokenizer、model 与 post-processor 的实现库；
- tiktoken 是面向部分 OpenAI tokenizer 的快速实现；
- Transformers 负责把 tokenizer 与具体模型 checkpoint 配套加载。

“使用 SentencePiece”不能直接推出使用 BPE；“从 Hugging Face 下载”也不能推出 tokenizer 算法。

## 7. 不能脱离 checkpoint 替换 tokenizer

模型 embedding 的第 \(i\) 行对应训练时 tokenizer 的第 \(i\) 个 token：

\[
\operatorname{Embed}(t_i)=E[i,:].
\]

若直接换一套 vocabulary，即使词表大小相同，相同 ID 的含义也会改变。除非重新训练或采用受控的 vocabulary extension 与 embedding 初始化，否则 tokenizer 必须与 checkpoint 成套使用。

