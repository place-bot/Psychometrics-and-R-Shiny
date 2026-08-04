# 三阶段迁移流程与 AWD-LSTM

## 1. 三阶段

### 通用语言模型预训练

在 WikiText-103 上训练 left-to-right LM：

\[
\mathcal L_{\text{LM}}
=
-\sum_t\log p(w_t\mid w_{<t}).
\]

### 目标任务 LM 微调

使用目标任务的全部文本，仍做语言建模，使通用 LM 适应领域分布。

### 目标分类器微调

在 LM 上加入分类头，使用标注训练，并逐层解冻。

## 2. 为什么中间还要目标域 LM

通用 Wikipedia 与 IMDb 评论、新闻标题或问句分布不同。无标注目标文本先调整语言模型，可缩小 domain shift，再学习标签边界。

## 3. AWD-LSTM

论文使用：

- 3 层 LSTM；
- embedding 400；
- 每层隐藏 1150；
- BPTT 70；
- embedding、输入、层间、循环权重等多类 dropout；
- weight-dropped LSTM。

方法强调可替换的通用 LM，作者预期更好的 LM 会进一步提升下游表现。

## 4. 与 Dai & Le

Dai & Le 证明 LM/autoencoder 预训练可作为 LSTM 初始化。ULMFiT 将其扩展为大通用语料 → 目标域 LM → 分类器，并专门解决微调中的遗忘和过拟合。
