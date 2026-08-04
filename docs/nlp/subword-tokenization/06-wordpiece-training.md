# WordPiece 训练：思想与证据边界

## 1. 历史目标

WordPiece 最早用于日语和韩语语音搜索。核心思想是从基础单位出发，逐步加入子词，使训练数据在语言模型下的 likelihood 得到最大改善。

若当前词表为 \(\mathcal V\)，候选新 piece 为 \(z\)，原始表述可以概括为选择：

\[
z^*
=
\arg\max_z
\left[
\log p(\mathcal C\mid\mathcal V\cup\{z\})
-
\log p(\mathcal C\mid\mathcal V)
\right].
\]

它与 BPE 直接选择最高频 pair 的动机不同：WordPiece 更关心新增单位对模型化训练语料的收益。

## 2. BERT 公布了什么

BERT 论文和官方仓库明确说明使用 30,000 个 WordPiece token。官方仓库公开了：

- `vocab.txt`；
- BasicTokenizer；
- WordpieceTokenizer；
- token 到 ID 的映射；
- longest-match-first 编码。

官方仓库也明确说明，当年学习新 WordPiece vocabulary 的 C++ 代码依赖 Google 内部库，没有随 BERT 开源。

因此下面必须区分：

1. WordPiece 文献中的 likelihood 思想；
2. 社区根据公开资料实现的 trainer；
3. BERT 推理代码中可直接核查的 greedy segmentation。

## 3. 常见的 Pair Score 近似

许多现代教学和实现用下式说明 WordPiece 的 merge preference：

\[
\operatorname{score}(a,b)
=
\frac{F(a,b)}{F(a)F(b)}.
\]

与 BPE 的 \(F(a,b)\) 相比，分母会降低那些“两个部分各自都很常见”的 pair 优先级，偏向结合性更强的 pair。

这个式子适合解释 BPE 与 WordPiece 的统计差异，但不应写成“BERT 内部 trainer 的已公开精确源码”。Google 没有发布该 trainer，具体平滑、likelihood 模型和 tie-breaking 无法从 BERT 仓库完全还原。

## 4. `##` 前缀的含义

BERT 英文 vocabulary 通常把非词首 piece 写为：

```text
play ##ing
```

其中 `##ing` 表示它只能接在一个词内部的当前位置，不能作为该预切分词的首 token。于是初始 alphabet 区分：

```text
词首字符：p
词内字符：##l, ##a, ##y
```

`##` 是 vocabulary 约定，不是原文字符。其他 WordPiece 实现可以配置不同 continuing-subword prefix。

## 5. 训练过程的概念伪代码

```python
splits = initialize_with_word_start_and_continuation_symbols(corpus)
vocab = special_tokens + initial_alphabet

while len(vocab) < target_size:
    pair_statistics = collect_statistics(splits)
    best_pair = choose_largest_likelihood_gain(pair_statistics)
    new_piece = merge(best_pair)
    vocab.add(new_piece)
    update_splits(new_piece)
```

这里的 `choose_largest_likelihood_gain` 是方法核心。不同开源库可能用可计算的 score 近似，不应假设它们一定复现 BERT 内部 trainer 的所有细节。

## 6. 为什么频率归一化有意义

假设 pair \((a,b)\) 出现 100 次，但 \(a\) 与 \(b\) 各自出现 10,000 次，二者结合并不专一。另一 pair 出现 30 次，而两个部分几乎只彼此相邻，则新增合并可能更有效地表达稳定片段。

频率比值近似衡量：

\[
\text{共同出现强度}
\approx
\frac{\text{pair frequency}}
{\text{marginal frequencies}}.
\]

这与 PMI 的归一化直觉相近，但具体公式、计数口径和概率模型不必完全等同于 PMI。

## 7. 最终保存什么

BERT 的运行时主要读取最终 `vocab.txt`。WordPiece 编码直接对该词表做最长匹配，并不需要重放训练 merge list。

这与经典 merge-based BPE 的资产结构形成鲜明对比：

```text
BPE runtime：vocabulary + ordered merges
WordPiece runtime：vocabulary + continuation-prefix convention
```

