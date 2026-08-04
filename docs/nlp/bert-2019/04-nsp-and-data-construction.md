# NSP 与预训练样本构造

## 1. Next Sentence Prediction

每个样本包含片段 A 与 B：

- 50%：B 是语料中紧随 A 的片段，`IsNext`；
- 50%：B 从其他文档随机采样，`NotNext`。

`[CLS]` 顶层向量通过二分类器：

\[
p(z\mid\mathbf C)
=
\operatorname{softmax}(
\mathbf W_{\text{NSP}}\mathbf C+\mathbf b).
\]

\[
\mathcal L_{\text{NSP}}=-\log p(z^\star\mid\mathbf C).
\]

## 2. 联合目标

\[
\mathcal L
=
\mathcal L_{\text{MLM}}
+
\mathcal L_{\text{NSP}}.
\]

原代码直接相加两个平均 loss，没有额外可调权重。

## 3. 文档级语料的重要性

NSP 正例需要真实连续片段，所以论文强调使用保留文档结构的 BooksCorpus 与 Wikipedia，而非完全打乱的句子集合。

## 4. 样本构造

原始脚本将文档分成句子列表，累积片段直到接近目标长度，再决定 B 为真实后续或随机文档片段。10% 样本随机使用短于最大长度的目标长度，帮助模型适应短序列并减少只见满长样本的偏差。

## 5. NSP 学到什么

任务同时包含话题一致性、文档连续性与随机负例辨别。论文认为它有利于 QA/NLI，并在自己的消融中观察到去掉 NSP 会下降。

后续 RoBERTa 在更强训练配方下去掉 NSP 仍表现良好，说明 BERT 表 5 的结论与其训练条件绑定。NSP 的普适必要性不能只由原论文单一消融确定。

## 6. NSP 与句对任务

预训练输入形式与下游的 premise–hypothesis、question–passage 等句对形式一致。下游不直接继续做 NSP；它利用共享 encoder 和句段表示，训练自己的监督目标。
