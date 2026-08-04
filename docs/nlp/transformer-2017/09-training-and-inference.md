# 训练、优化器与自回归推理

## 1. 目标函数

\[
\mathcal L
=
-\sum_t\log
p(y_t\mid y_{<t},\mathbf x).
\]

目标右移与 causal mask 让所有位置的 logits 一次计算，同时保持条件概率约束。

## 2. 数据

- WMT14 英德：约 450 万句对，共享约 37k BPE 词表；
- WMT14 英法：约 3600 万句对，约 32k word-piece 词表；
- batch 按近似长度分组；
- 每 batch 约 25k source tokens 和 25k target tokens。

## 3. Adam 与 Noam schedule

\[
\operatorname{lr}
=
d_{\text{model}}^{-1/2}
\min(
\operatorname{step}^{-1/2},
\operatorname{step}\cdot
\operatorname{warmup}^{-3/2}).
\]

论文采用

\[
\beta_1=0.9,\quad
\beta_2=0.98,\quad
\epsilon=10^{-9},\quad
\operatorname{warmup}=4000.
\]

学习率前 4000 步线性上升，之后按步数平方根倒数下降。

## 4. 正则化

- residual dropout；
- embedding 与位置编码之和的 dropout；
- base dropout 0.1；
- label smoothing \(\epsilon_{ls}=0.1\)。

label smoothing 会让模型对正确类的目标概率小于 1，可能提高交叉熵/perplexity，却改善准确率和 BLEU。

## 5. 训练规模

一台机器、8 块 P100：

- base：100k steps，约 12 小时，每步约 0.4 秒；
- big：300k steps，约 3.5 天，每步约 1.0 秒。

## 6. 解码

论文使用 beam size 4、长度惩罚 \(\alpha=0.6\)，最大输出长度为输入长度加 50。base 平均最后 5 个 checkpoint，big 平均最后 20 个。

## 7. KV cache

现代自回归推理会缓存先前层的 K/V，避免每次重算整个前缀。新 token 仍需等待上一个 token 确定，因此 cache 降低每步重复计算，没有消除 token 级串行生成。
