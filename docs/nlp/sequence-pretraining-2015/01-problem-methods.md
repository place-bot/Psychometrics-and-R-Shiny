# 预训练问题与两种无监督目标

## 1. 目标

监督文档分类数据有限，长序列 LSTM 又难优化。论文先用无标注序列学习 embedding 与 LSTM 权重：

\[
\theta_{\text{pre}}
=
\arg\min_\theta
\mathcal L_{\text{unsup}}(\theta),
\]

再初始化监督模型：

\[
\theta_0^{\text{sup}}=\theta_{\text{pre}}.
\]

## 2. Recurrent language model

\[
\mathcal L_{\text{LM}}
=
-\sum_t\log p(x_{t+1}\mid x_{\le t}).
\]

它训练 LSTM 保存有利于预测下一个 token 的状态，得到 LM-LSTM 初始化。

## 3. Sequence autoencoder

encoder LSTM 读完整输入 \(x_1,\ldots,x_T\) 到状态，decoder 再重构原序列：

\[
\mathcal L_{\text{SA}}
=
-\sum_t\log p(x_t\mid x_{<t},h_{\text{enc}}).
\]

得到 SA-LSTM 初始化。作者认为重构整文档迫使最终状态捕获更长程信息。

## 4. 为什么称为 semi-supervised

无标注数据训练表示与序列参数，标注数据训练分类器并继续微调全部权重：

\[
\text{unlabeled pretraining}
\rightarrow
\text{labeled fine-tuning}.
\]

## 5. 与 Word2Vec

Word2Vec 初始化只迁移词 embedding；LM/SA 预训练同时迁移 embedding 和递归组合函数。论文 IMDB 中 word2vec 初始化 error 10.00%，LM-LSTM 7.64%，SA-LSTM 7.24%。
