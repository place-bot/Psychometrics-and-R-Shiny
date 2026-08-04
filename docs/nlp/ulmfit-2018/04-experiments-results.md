# 实验、消融与低样本结果

## 1. 六个分类数据集

| 数据集 | ULMFiT test error |
|---|---:|
| IMDb | 4.6% |
| TREC-6 | 3.6% |
| AG | 5.01% |
| DBpedia | 0.80% |
| Yelp binary | 2.16% |
| Yelp full | 29.98% |

论文在多数数据集相对此前 SOTA 降低约 18–24% 相对 error。

## 2. 低样本

IMDb 与 AG 只有 100 个标签时，监督 ULMFiT 可匹配从头训练使用 10×/20× 标签；再使用目标域无标注文本，可匹配 100×/50× 标签量的从头训练。

## 3. 预训练消融

| 设置 | IMDb | TREC-6 | AG |
|---|---:|---:|---:|
| 无通用预训练 | 5.63 | 10.67 | 5.52 |
| WikiText-103 预训练 | 5.00 | 5.69 | 5.38 |

小型 TREC-6 获益尤其明显。

## 4. 目标 LM 微调

IMDb：

- 不做 target LM fine-tuning：6.99；
- 普通 full fine-tuning：5.86；
- + discriminative LR：5.55；
- + Discr + STLR：5.00。

## 5. 分类器微调

IMDb：

- 从头训练分类器：9.93；
- full：6.87；
- full + discriminative：4.57；
- gradual + discriminative + STLR：5.00。

不同数据集的最佳局部变体略有差异；完整 ULMFiT 跨任务最稳定，论文据此强调 universal。

## 6. 证据边界

- 主模型是单向 AWD-LSTM，任务集中于文本分类；
- 超参数主要在 IMDb 调整；
- 部分小测试集差异不显著；
- “100×”指特定低样本曲线匹配，不表示所有任务固定节省 100 倍标签。
