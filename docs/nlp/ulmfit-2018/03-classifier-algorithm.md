# Concat Pooling 与分类算法

## 1. 为什么只用最后状态不够

长文档的判别词可能出现在任意位置。只读 \(h_T\) 可能丢失早期强信号。

## 2. Concat pooling

对隐藏状态

\[
H=\{h_1,\ldots,h_T\},
\]

拼接

\[
h_c
=
[h_T;\operatorname{maxpool}(H);
\operatorname{meanpool}(H)].
\]

它同时保留：

- 最终顺序状态；
- 每维最强激活；
- 全文平均激活。

## 3. 分类头

\(h_c\) 进入两个 linear blocks，中间使用 batch norm、dropout、ReLU，最后 softmax。

## 4. BPT3C

长文档按固定长度 batch 分段，下一段用上一段最终状态初始化；系统持续累计 mean/max pooling，梯度按段反传。这样可处理超出显存的文档。

## 5. 完整流程

```text
WikiText-103 LM pretraining
  → target-text LM fine-tuning (Discr + STLR)
  → add concat-pooling classifier
  → train head
  → gradual unfreezing
  → all unfrozen with layer-wise LR + STLR
```

## 6. 与 BERT [CLS]

ULMFiT 显式拼接 last/max/mean；BERT 通常用 `[CLS]` 经 self-attention 汇总，也可做 token pooling。两者都是把变长序列转换为固定分类表示，机制不同。
