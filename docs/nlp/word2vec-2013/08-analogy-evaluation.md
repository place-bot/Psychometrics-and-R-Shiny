# 类比评测与向量运算

## 1. 从近邻展示到关系测试

早期词向量论文常展示一个词的若干最近邻。这种展示容易挑选有利例子，也难以比较模型。本文建立批量类比测试，把关系保持能力转成可重复计算的 top-1 准确率。

给定两个词对

\[
(a,b),\qquad(c,d),
\]

假设二者表达相同关系：

\[
a:b::c:d.
\]

模型构造查询向量

\[
\mathbf q
=\mathbf v_b-\mathbf v_a+\mathbf v_c,
\]

再寻找余弦相似度最大的词：

\[
\widehat d
=\arg\max_{w\in\mathcal V\setminus\{a,b,c\}}
\operatorname{cos}(\mathbf v_w,\mathbf q).
\]

若 \(\widehat d=d\)，该题记为命中。

## 2. 例子

### 2.1 最高级

\[
\mathbf q
=\mathbf v_{\text{biggest}}
-\mathbf v_{\text{big}}
+\mathbf v_{\text{small}}.
\]

若最近词为 `smallest`，说明

\[
\mathbf v_{\text{biggest}}-\mathbf v_{\text{big}}
\approx
\mathbf v_{\text{smallest}}-\mathbf v_{\text{small}}.
\]

### 2.2 国家—首都

\[
\mathbf q
=\mathbf v_{\text{Paris}}
-\mathbf v_{\text{France}}
+\mathbf v_{\text{Italy}},
\]

最近词若为 `Rome`，则国家到首都的差值在这两个词对上近似平行。

## 3. 为什么排除三个输入词

查询向量通常与 \(a\)、\(b\)、\(c\) 本身高度相似。若不排除它们，最近邻可能直接返回某个输入词，无法测量关系迁移。因此候选集合去掉前三个词。

## 4. 14 类关系

论文 Table 1 包含 5 类语义关系和 9 类句法关系：

| 组别 | 关系类别 | 词对示例 1 | 词对示例 2 |
|---|---|---|---|
| 语义 | common capital city | Athens–Greece | Oslo–Norway |
| 语义 | all capital cities | Astana–Kazakhstan | Harare–Zimbabwe |
| 语义 | currency | Angola–kwanza | Iran–rial |
| 语义 | city-in-state | Chicago–Illinois | Stockton–California |
| 语义 | man–woman | brother–sister | grandson–granddaughter |
| 句法 | adjective to adverb | apparent–apparently | rapid–rapidly |
| 句法 | opposite | possibly–impossibly | ethical–unethical |
| 句法 | comparative | great–greater | tough–tougher |
| 句法 | superlative | easy–easiest | lucky–luckiest |
| 句法 | present participle | think–thinking | read–reading |
| 句法 | nationality adjective | Switzerland–Swiss | Cambodia–Cambodian |
| 句法 | past tense | walking–walked | swimming–swam |
| 句法 | plural nouns | mouse–mice | dollar–dollars |
| 句法 | plural verbs | work–works | speak–speaks |

类别标签中的“语义”和“句法”是论文的分组。某些类别同时涉及世界知识、命名实体和形态变化，边界并非纯粹语言学划分。

## 5. 问题怎样生成

每个类别先人工建立关系一致的词对列表，再组合两个不同词对形成问题。

若一个类别有 \(m\) 个有向词对，理论上可以形成约

\[
m(m-1)
\]

个有向组合。论文以 68 个美国城市及其州为例，组合后约产生 2.5K 个问题。

公开 `questions-words.txt` 中共有：

\[
8{,}869\ \text{个语义问题}
+10{,}675\ \text{个句法问题}
=19{,}544\ \text{个问题}.
\]

## 6. 严格 top-1 准确率

总准确率为

\[
\operatorname{Accuracy}
=\frac{1}{M}
\sum_{m=1}^{M}
\mathbb I(\widehat d_m=d_m).
\]

论文采用严格字符串匹配：

- 只有最近词与目标词完全相同才计为命中；
- 同义词也会被计为错误；
- 多词实体没有纳入，因为测试集只保留单 token；
- 当前模型没有显式词形结构，因此达到 100% 很困难。

## 7. OOV 与分母

若 \(a,b,c,d\) 任一词不在模型词表中，该问题无法计算。公开 `compute-accuracy.c` 会跳过这些问题，并同时报告：

```text
Questions seen / total
```

因此复现实验时应同时记录：

\[
\text{coverage}
=\frac{\text{可计算问题数}}{\text{全部问题数}},
\]

以及在可计算问题上的准确率。只报告准确率可能掩盖小词表带来的覆盖损失。

Table 2 明确只使用四个词都位于 30K 高频词表的问题；后续表使用完整模型词表。

## 8. 归一化与检索

公开评价代码先归一化每个词向量：

\[
\widetilde{\mathbf v}_w
=\frac{\mathbf v_w}{\lVert\mathbf v_w\rVert_2}.
\]

查询向量为

\[
\mathbf q
=\widetilde{\mathbf v}_b
-\widetilde{\mathbf v}_a
+\widetilde{\mathbf v}_c.
\]

然后计算 \(\mathbf q^\top\widetilde{\mathbf v}_w\)。查询向量是否再归一化不改变候选排序，因为它对所有候选只提供同一个正比例因子。

## 9. 一个手算例子

设归一化后的二维向量为

\[
\mathbf v_a=(0.8,0.6),\quad
\mathbf v_b=(0.6,0.8),\quad
\mathbf v_c=(1,0).
\]

查询向量为

\[
\mathbf q
=(0.6,0.8)-(0.8,0.6)+(1,0)
=(0.8,0.2).
\]

两个候选为

\[
\mathbf v_d=(0.97,0.24),
\qquad
\mathbf v_e=(0.3,0.95).
\]

点积分数为

\[
\mathbf q^\top\mathbf v_d
=0.824,
\qquad
\mathbf q^\top\mathbf v_e
=0.430.
\]

模型选择 \(d\)。这个计算只比较方向相似性，没有要求 \(\mathbf q\) 本身恰好等于某个词向量。

## 10. 多示例关系向量

单个词对的差值可能含噪。若有 \(K\) 个示例关系，可平均：

\[
\mathbf r
=\frac{1}{K}
\sum_{k=1}^{K}
(\mathbf v_{b_k}-\mathbf v_{a_k}).
\]

新查询为

\[
\mathbf q=\mathbf v_c+\mathbf r.
\]

论文报告使用 10 个示例形成关系向量后，最佳模型在语义—句法测试上的准确率绝对提高约 10 个百分点。这表明关系方向的平均可以降低单一词对噪声。

## 11. 评价能说明什么

该任务直接测量以下性质：

- 词向量差值能否在多个词对间保持一致；
- 目标词能否成为全词表中的 top-1 最近邻；
- 语义与句法类别的关系迁移能力。

它无法单独证明：

- 向量适合所有下游任务；
- 模型理解了完整词义；
- 线性关系覆盖所有语言现象；
- 高准确率与人类语言理解等价。

论文把它作为可量化的表示质量代理，并在 Microsoft Sentence Completion Challenge 上补充任务级证据。
