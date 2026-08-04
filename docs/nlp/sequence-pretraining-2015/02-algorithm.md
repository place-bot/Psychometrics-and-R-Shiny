# LM-LSTM、SA-LSTM 与训练流程

## 1. Sequence autoencoder

输入末尾加入结束标记。encoder 读完后，decoder 开始逐 token 重构完整文档。论文不截断输入窗口，但反向传播最多从序列末端追踪 400 时间步。

## 2. 预训练配置

- 约 500k updates；
- batch size 128；
- 分词将标点独立处理；
- 去除只出现一次的词；
- LSTM 使用 cell output 与 gradient clipping。

## 3. 迁移哪些参数

\[
\theta_{\text{transfer}}
=
\{\text{word embeddings},\text{LSTM weights}\}.
\]

监督阶段加入分类头，继续 fine-tune embedding 与 LSTM，验证误差上升时 early stopping。

## 4. 分类

最终 LSTM 状态进入小隐藏层和 softmax：

\[
p(y\mid x)
=
\operatorname{softmax}(
W_c\,g(h_T)+b_c).
\]

IMDB 配置使用 1024 memory cells、512 embedding、30 单元分类隐藏层与 dropout。

## 5. 变体

- LM-LSTM：next-token LM 初始化；
- SA-LSTM：sequence autoencoder 初始化；
- linear gain：对重构位置加权；
- joint training：监督任务与 autoencoder 同时训练。

实验中简单阶段式 SA-LSTM 优于 linear gain 和 joint training，说明联合目标并不自动更好。

## 6. 预训练为什么改善稳定性

随机初始化 LSTM 要同时学词表示、长程状态和分类边界。预训练先把参数放入能建模序列结构的区域，使监督优化起点更好。它属于经验解释，不能保证任何预训练目标都帮助任何任务。
