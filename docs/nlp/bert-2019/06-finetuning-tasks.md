# 统一微调接口

原论文为每个任务加入小输出层，并更新全部 BERT 参数。

## 1. 单句/句对分类

取 `[CLS]` 顶层表示 \(\mathbf C\)：

\[
p(y\mid x)
=
\operatorname{softmax}(
\mathbf W\mathbf C+\mathbf b).
\]

单句情感使用 A 句段；NLI、paraphrase 使用 A/B 句段。

## 2. Token classification

每个 token 的 \(\mathbf T_i\) 进入共享分类层：

\[
p(y_i\mid x)
=
\operatorname{softmax}(
\mathbf W\mathbf T_i+\mathbf b).
\]

适用于 NER 等序列标注。WordPiece 拆分后的标签对齐需由实现明确处理。

## 3. SQuAD 抽取式问答

输入：

\[
[\text{CLS}]\ \text{Question}\ [\text{SEP}]\
\text{Passage}\ [\text{SEP}].
\]

学习起点向量 \(S\) 与终点向量 \(E\)：

\[
p_i^{start}
=
\frac{\exp(S^\top T_i)}
{\sum_j\exp(S^\top T_j)},
\quad
p_j^{end}
=
\frac{\exp(E^\top T_j)}
{\sum_k\exp(E^\top T_k)}.
\]

候选 span 分数：

\[
S^\top T_i+E^\top T_j,\qquad j\ge i.
\]

SQuAD 2.0 把 `[CLS]` 位置作为 no-answer span，并在开发集选择阈值。

## 4. SWAG 多项选择

为四个候选分别构造句对，取各自 \(\mathbf C_k\)，用一个向量打分：

\[
s_k=\mathbf w^\top\mathbf C_k,
\qquad
p(k)=\operatorname{softmax}(s)_k.
\]

## 5. 统一的意义

过去系统常为 QA、NLI、NER 设计大量专用网络。BERT 把主要表示学习放进预训练 encoder，下游只需调整输入格式和浅输出层。

## 6. Fine-tuning 与 feature extraction

论文也测试冻结 BERT、抽取各层特征用于 NER。最后四层拼接达到 96.1 dev F1，接近全量微调 96.4；说明表示可以作为特征使用，但主线方法是端到端微调。
