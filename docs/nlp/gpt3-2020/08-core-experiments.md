# 语言建模、问答、翻译与 SuperGLUE

## 1. Cloze 与 completion

| 设置 | LAMBADA Acc | LAMBADA PPL | StoryCloze Acc | HellaSwag Acc |
|---|---:|---:|---:|---:|
| 当时 SOTA | 68.0 | 8.63 | 91.8 | 85.6 |
| GPT-3 zero-shot | 76.2 | 3.00 | 83.2 | 78.9 |
| GPT-3 one-shot | 72.5 | 3.35 | 84.7 | 78.1 |
| GPT-3 few-shot | **86.4** | **1.92** | 87.7 | 79.3 |

LAMBADA few-shot 使用 fill-in-the-blank 格式，让模型只补一个词。one-shot 反而低于 zero-shot，作者推测一个示例不足以让模型稳定识别填空格式。

GPT-3 在 LAMBADA 很强，但 StoryCloze 与 HellaSwag 仍低于 fine-tuned SOTA，说明规模效应具有任务差异。

## 2. 闭卷问答

| 方法 | Natural Questions | WebQuestions | TriviaQA |
|---|---:|---:|---:|
| RAG，fine-tuned + retrieval | 44.5 | 45.5 | 68.0 |
| T5-11B+SSM，closed-book | 36.6 | 44.7 | 60.5 |
| GPT-3 zero-shot | 14.6 | 14.4 | 64.3 |
| GPT-3 one-shot | 23.0 | 25.3 | 68.0 |
| GPT-3 few-shot | 29.9 | 41.5 | **71.2** |

TriviaQA few-shot 很强；Natural Questions 仍明显落后于 fine-tuned T5 与检索系统。NQ 更偏向细粒度 Wikipedia 知识，参数记忆和广泛预训练分布未能替代精确检索。

## 3. 阅读理解与科学问答

| 设置 | ARC Easy | ARC Challenge | CoQA F1 | DROP F1 |
|---|---:|---:|---:|---:|
| Fine-tuned SOTA | 92.0 | 78.5 | 90.7 | 89.1 |
| GPT-3 zero-shot | 68.8 | 51.4 | 81.5 | 23.6 |
| GPT-3 one-shot | 71.2 | 53.2 | 84.0 | 34.3 |
| GPT-3 few-shot | 70.1 | 51.5 | 85.0 | 36.5 |

CoQA 接近人类 baseline；DROP 需要数值与离散推理，few-shot 虽高于原论文 BERT baseline，仍远低于带符号模块的系统与人类表现。

## 4. 翻译

| 设置 | En→Fr | Fr→En | En→De | De→En | En→Ro | Ro→En |
|---|---:|---:|---:|---:|---:|---:|
| GPT-3 zero-shot | 25.2 | 21.2 | 24.6 | 27.2 | 14.1 | 19.9 |
| GPT-3 one-shot | 28.3 | 33.7 | 26.2 | 30.4 | 20.6 | 38.6 |
| GPT-3 few-shot | 32.6 | **39.2** | 29.7 | **40.6** | 21.0 | **39.5** |

翻译到英语明显强于从英语翻到其他语言，符合 93% 英语训练分布与英语中心 tokenizer。few-shot 使用成对翻译示例，因此与完全无平行数据的 unsupervised MT 不能严格等价比较。

## 5. SuperGLUE

| 模型 | 平均 | BoolQ | CB Acc | COPA | RTE | WiC | WSC | MultiRC F1a | ReCoRD F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fine-tuned SOTA | 89.0 | 91.0 | 93.9 | 94.8 | 92.5 | 76.1 | 93.8 | 88.2 | 93.3 |
| Fine-tuned BERT-Large | 69.0 | 77.4 | 75.7 | 70.6 | 71.7 | 69.6 | 64.6 | 70.0 | 72.0 |
| GPT-3 few-shot | **71.8** | 76.4 | 52.0 | 92.0 | 69.0 | 49.4 | 80.1 | 75.4 | 91.1 |

GPT-3 few-shot 平均超过 fine-tuned BERT-Large，但仍低于整体 SOTA。任务间差异极大：

- COPA、ReCoRD 接近 SOTA；
- WSC、BoolQ、MultiRC、RTE 接近或超过 BERT-Large 部分指标；
- WiC 接近随机水平；
- CB 表现不稳定。

作者认为模型在需要比较两个句子或片段的任务上尤其薄弱，这与单向自回归目标和 prompt 形式有关。

## 6. 结果怎样概括

GPT-3 few-shot 已能在部分任务接近 fine-tuned 系统，但不存在统一领先：

\[
\text{收益大小}
=
f(\text{任务结构},\text{数据覆盖},\text{prompt},K,N).
\]

论文的中心证据是广泛的规模趋势和快速任务切换，而非一张全面压倒监督方法的排行榜。
