# BPE 编码：按 Merge Rank 合并

## 1. 训练完成后哪些东西固定了

一个 merge-based BPE tokenizer 至少需要：

- normalization 与 pre-tokenization 规则；
- 初始 alphabet；
- 有顺序的 merge list；
- token 到 ID 的 vocabulary；
- special-token 配置。

对新文本编码时不再重新计算 pair frequency，而是查训练得到的 merge rank。

## 2. 编码算法

假设预切分片段已经变成初始符号序列 \(s=(s_1,\ldots,s_m)\)。每轮：

1. 枚举当前所有相邻 pair；
2. 查找各 pair 的 rank；
3. 选择 rank 最小的可合并 pair；
4. 合并它的所有非重叠出现；
5. 没有 pair 出现在 merge table 时停止。

\[
(a^*,b^*)
=
\arg\min_{(a,b)\in\operatorname{Pairs}(s)}r(a,b).
\]

## 3. 一个简单例子

merge list 为：

```text
rank 0: u + g  → ug
rank 1: h + ug → hug
rank 2: hug + s → hugs
```

输入 `hugs`：

```text
h u g s
→ h ug s       # rank 0
→ hug s        # rank 1
→ hugs         # rank 2
```

如果 `hug + s` 不在 merge list，编码会停在 `hug | s`。

## 4. 为什么不能只做最长匹配

设 vocabulary 同时包含：

```text
a, b, c, ab, bc
```

最长前缀算法从 `abc` 开始会取 `ab | c`。BPE 若 merge rank 规定 `b+c` 早于 `a+b`，则可能得到 `a | bc`。

BPE 编码由 merge history 约束；WordPiece 的经典编码则直接根据最终词表做 longest-match-first。这是二者在推理阶段的重要差异。

## 5. Tie-breaking 必须稳定

训练时若多个 pair 频数相同，选择哪一个会改变后续 merge history。实现可能按首次出现、词典序、内部 heap 顺序或显式规则打破平局。

复现 tokenizer 不能只保存：

```text
vocab size = 30,000
algorithm = BPE
```

还需要训练语料顺序、normalizer、pre-tokenizer、最小频数、特殊 token、alphabet 和 trainer 版本。

## 6. Cache

自然语料中相同预切分片段会反复出现。GPT-2 官方 encoder 对片段的 BPE 结果使用 cache：

\[
\text{piece string}\longrightarrow\text{BPE segmentation}.
\]

这只复用确定性编码结果，不改变 tokenization。

## 7. 解码

普通字符 BPE 解码通常执行：

1. ID 映射回 token string；
2. 拼接 token；
3. 还原词尾或空格标记；
4. 逆 normalization 若可能。

如果 normalization 丢失了大小写或重音，最后一步无法恢复原文。BPE merge 本身是字符串拼接，通常可逆；不可逆性多来自前后处理。

