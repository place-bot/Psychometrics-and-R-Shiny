# BPE：从数据压缩到子词词表

## 1. 原始 BPE 的目标

Philip Gage 在 1994 年介绍 BPE 时讨论的是无损数据压缩。算法寻找最频繁的相邻字节对，用一个未使用的字节替换它，并保存替换表：

```text
原序列：A A A B A A A B
高频对：A A
新符号：X := A A
替换后：X A B X A B
```

解压时按替换表递归展开 \(X\)。这个版本受限于可用字节，并以压缩后文件大小为目的。

## 2. NLP BPE 改了什么

Sennrich、Haddow 和 Birch 将这种“反复合并高频相邻符号”的思想用于神经机器翻译：

- 初始符号通常是字符，而非必须是真实字节；
- 新合并得到的是可增长的子词词表条目；
- 不需要把合并结果塞进一个未使用字节；
- 目标是固定词表下处理 rare words，而非直接输出压缩文件；
- merge operations 作为编码新词的模型保存。

## 3. 从带频数的词表开始

先对训练语料做预分词，得到词及频数：

\[
\mathcal C=\{(w_i,f_i)\}_{i=1}^{M}.
\]

每个词拆成初始字符序列。经典 subword-nmt 例子还会加入词尾标记 `</w>`，用来区分词内片段和词尾片段：

```text
low   → l o w </w>
lower → l o w e r </w>
```

不同现代实现对边界的表示并不相同，不能把 `</w>` 当成所有 BPE 的必需规则。

## 4. 统计相邻对

设当前切分 \(s(w_i)=(u_{i1},\ldots,u_{im_i})\)。相邻对 \((a,b)\) 的加权频数为：

\[
F(a,b)
=
\sum_{i=1}^{M} f_i
\sum_{j=1}^{m_i-1}
\mathbb I(u_{ij}=a,\ u_{i,j+1}=b).
\]

每轮选择频数最大的 pair：

\[
(a^*,b^*)=\arg\max_{(a,b)}F(a,b),
\]

并把所有相邻的 \(a^*,b^*\) 合并成新符号 \(a^*b^*\)。

## 5. 保存 merge rank

假设前三轮学到：

```text
u g
u n
h ug
```

顺序本身就是模型的一部分：

\[
r(u,g)=0,\quad r(u,n)=1,\quad r(h,ug)=2.
\]

rank 越小，优先级越高。只保存最终出现过的字符串集合，会丢失某些 BPE 编码所需的合并顺序。

## 6. 停止条件

常见停止方式：

- 执行固定数量的 merge operations；
- 达到目标词表规模；
- 最高 pair 频数低于阈值；
- 新增 token 不再带来足够收益。

若初始 alphabet 大小为 \(|\mathcal A|\)，特殊 token 数为 \(S\)，执行 \(K\) 次有效合并，理想化词表规模约为：

\[
|\mathcal V|\approx |\mathcal A|+S+K.
\]

实际实现还会受最小频数、重复 token、reserved token 和 alphabet coverage 影响。

## 7. 训练伪代码

```python
splits = initialize_as_characters(word_frequencies)
merges = []

while vocabulary_not_large_enough():
    pair_freq = count_weighted_adjacent_pairs(splits)
    best = argmax(pair_freq)
    splits = merge_every_occurrence(splits, best)
    merges.append(best)
```

朴素实现每轮扫描整个语料，成本很高。实际 trainer 会缓存 pair counts，并只更新受本次合并影响的邻接关系。

## 8. 合并频率不是最终模型概率

BPE 训练用频率决定合并，但下游语言模型仍学习：

\[
p_\theta(t_i\mid t_{<i}).
\]

tokenizer 的 merge frequency 不会直接成为 Transformer 的 token probability。它只决定离散序列怎样构造。

