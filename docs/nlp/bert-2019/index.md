# BERT：深层双向 Transformer 预训练

本专题精读 Devlin et al. 的 **BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**。论文 2018 年发布预印本，正式发表于 NAACL-HLT 2019。

## 核心思想

BERT 使用 Transformer encoder，让每个 token 在每层同时读取左右上下文。为避免目标 token 直接看到自身，预训练随机遮蔽部分输入并预测原词：

\[
\mathcal L_{\text{pretrain}}
=
\mathcal L_{\text{MLM}}
+
\mathcal L_{\text{NSP}}.
\]

预训练后，用少量任务头和同一组 BERT 参数完成分类、句对推断、序列标注与抽取式问答。

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Jacob Devlin、Ming-Wei Chang、Kenton Lee、Kristina Toutanova |
| 发表 | NAACL-HLT 2019，4171–4186 |
| 正式论文 | [ACL Anthology](https://aclanthology.org/N19-1423/) |
| arXiv | [1810.04805](https://arxiv.org/abs/1810.04805) |
| 原始代码 | [google-research/bert](https://github.com/google-research/bert) |

## 阅读路线

1. [问题、创新与 encoder-only 架构](01-problem-architecture.md)
2. [WordPiece、CLS、SEP 与三种 embedding](02-input-representation.md)
3. [MLM 与 80/10/10](03-masked-language-model.md)
4. [NSP 与预训练样本构造](04-nsp-and-data-construction.md)
5. [预训练数据、配置与优化](05-pretraining-configuration.md)
6. [统一微调接口](06-finetuning-tasks.md)
7. [完整手算](07-worked-example.md)
8. [实验结果](08-experiments-results.md)
9. [消融、双向性与模型规模](09-ablations.md)
10. [Google 原始代码精读与现代实现](10-code-reading-implementation.md)
11. [局限、后续发展与结论](11-limitations-followups-conclusion.md)
12. [参考文献](references.md)

## 与前后专题的关系

- Word2Vec：每个词一个静态向量；
- Bahdanau/Transformer：序列中的 token 通过 attention 获得上下文；
- BERT：用无标注语料预训练深层双向 Transformer encoder；
- LoRA：冻结这类预训练模型，用低秩更新完成参数高效适配。
