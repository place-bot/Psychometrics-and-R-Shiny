# 问题、创新与 Encoder-Only 架构

## 1. 2018 年的两条预训练路线

### Feature-based

ELMo 等模型生成上下文化特征，再交给任务专用网络。

### Fine-tuning

OpenAI GPT 先预训练 Transformer，再用少量任务头微调整体参数。它使用 left-to-right causal attention。

BERT希望保留统一微调接口，同时让每一层 token 表示都联合利用左右上下文。

## 2. 为什么普通双向语言模型会泄漏

若目标仍是预测当前位置 \(x_i\)，又允许表示直接读取包含 \(x_i\) 的完整输入，网络可以复制答案。BERT 先破坏选中的 token，再让模型从剩余上下文恢复原词。

## 3. 架构

BERT 是多层 Transformer encoder：

\[
\mathbf H^{(L)}
=
\operatorname{TransformerEncoder}^{(L)}
(\mathbf E).
\]

没有 decoder cross-attention，也没有目标端 causal mask。每个有效位置可以关注整条输入序列。

## 4. Base 与 Large

| 模型 | 层 \(L\) | 隐藏 \(H\) | 头 \(A\) | FFN | 参数 |
|---|---:|---:|---:|---:|---:|
| BERT Base | 12 | 768 | 12 | 3072 | 110M |
| BERT Large | 24 | 1024 | 16 | 4096 | 340M |

Base 特意与 OpenAI GPT 保持相近模型规模，便于比较预训练方向与输入形式。

## 5. 深层双向

BERT 每层 self-attention 都允许左右交互。ELMo 将独立训练的左向 LM 与右向 LM 在输出处拼接，两个方向在深层内部没有联合条件化。论文用“deeply bidirectional”强调这一差别。

## 6. 两阶段范式

### Pre-training

使用无标注 BooksCorpus 与 Wikipedia，训练 MLM 与 NSP。

### Fine-tuning

同一预训练 checkpoint 为每个任务初始化独立模型，加入小任务头，并更新全部参数。原论文的“少量任务特定参数”不表示冻结 BERT。

## 7. 贡献

- MLM 支持深层双向预训练；
- NSP 为句对关系提供预训练信号；
- 统一输入表示覆盖单句与句对；
- 极少任务架构修改即可处理 11 个任务；
- 系统消融双向性、NSP、规模和 feature-based 用法。
