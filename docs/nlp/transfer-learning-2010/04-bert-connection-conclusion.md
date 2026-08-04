# 与 BERT 的关系与结论

## 1. 把 BERT 放进定义

源 domain：

\[
\mathcal D_S=\text{BooksCorpus + Wikipedia}.
\]

源 task：

\[
\mathcal T_S=\text{MLM + NSP}.
\]

目标 domain/task 可以是 SQuAD QA、GLUE 分类或目标领域文本。BERT 将 encoder 参数和表示转移到目标任务，属于 inductive transfer learning。

## 2. Pretraining、fine-tuning 与 transfer 的层级

- transfer learning：整体问题设定；
- pretraining：在源数据/目标上学习可复用参数；
- fine-tuning：用目标数据调整参数；
- language modeling：常用的预训练任务之一。

这四个词处在不同抽象层级，不能互作同义词。

## 3. 现代问题

现代模型需要继续回答：

- 源语料与目标域相似度怎样量化；
- 哪层、哪类参数最值得迁移；
- 全量微调还是 LoRA；
- 何时冻结；
- 多源迁移如何组合；
- 怎样检测负迁移、遗忘与捷径。

## 4. 结论

Pan 与 Yang 的框架用 domain、task、transfer object 三个坐标拆解迁移学习。BERT 的预训练—微调是其中极成功的一种参数/表示迁移实现，而非迁移学习的全部。
