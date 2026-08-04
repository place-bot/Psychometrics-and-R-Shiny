# 训练过程、并行化与计算成本

## 1. 优化器

所有模型使用 Adam：

\[
\beta_1=0.9,
\qquad
\beta_2=0.95,
\qquad
\epsilon=10^{-8}.
\]

全局梯度范数裁剪为

\[
\|g\|_2\le1.0,
\]

weight decay 为 0.1。

## 2. 学习率调度

前 3.75 亿 token 线性 warmup。随后采用 cosine decay，在前 2600 亿 token 内下降到初始值的 10%；最后约 400 亿 token 保持在初始学习率的 10%。

简化写成：

\[
\eta(s)=
\begin{cases}
\eta_0\dfrac{s}{S_{\mathrm{warm}}},
&s<S_{\mathrm{warm}},\\[6pt]
\eta_0\left[0.1+0.9\dfrac{1+\cos(\pi q)}{2}\right],
&S_{\mathrm{warm}}\le s\le260\mathrm B,\\[6pt]
0.1\eta_0,&s>260\mathrm B,
\end{cases}
\]

其中 \(q\) 是 decay 区间归一化进度。

## 3. Batch size warmup

训练开始时 batch 约 32K token，再在前 40–120 亿训练 token 内线性增大到完整 batch。不同模型完整 batch 为 0.5M 到 3.2M token。

作者使用 gradient noise scale 指导 batch 选择：更大模型通常可有效利用更大 batch，同时需要更小学习率。

## 4. 序列 packing

所有训练序列长度固定为 2048。较短文档被打包进同一序列，中间用 end-of-text token 分隔：

```text
document A <|endoftext|> document B <|endoftext|> ...
```

不同文档之间没有额外 attention mask。模型可以看到边界 token，并学习边界两侧不具备常规语义连续性。

## 5. 数据采样

在到达某个数据集 epoch 边界之前，样本以 without-replacement 方式抽取，降低短期重复和过拟合。由于混合权重不同，小型高质量语料仍会跨 epoch 重复多次。

## 6. 训练计算

论文 broader impacts 估计 GPT-3 175B 预训练消耗数千 PF-days。官方图表给出的训练计算量约为

\[
3.14\times10^{23}\ \text{FLOPs},
\]

折合约 3640 PF-days。这个数描述最终训练 run，不含搜索、失败实验、小模型和系统开发的全部成本。

## 7. 计算的近似来源

对 dense Transformer，一种常用训练 FLOPs 粗略估计是：

\[
C\approx6NT,
\]

其中 \(N\) 是非 embedding 参数量，\(T\) 是训练 token 数；系数 6 粗略涵盖前向与反向矩阵乘。带 sparse attention 和具体系统优化时，精确值需要实际算子统计。

## 8. 能耗与推理

论文指出大型训练能耗高；同一模型训练完成后，单次样本的增量推理成本可能远低于重新训练任务模型。这个比较仍取决于：

- 服务请求量；
- prompt 长度与输出长度；
- KV cache；
- batch 与硬件利用率；
- 模型是否长期常驻；
- 每个任务替代了多少微调模型。

## 9. 可复现性

论文说明模型在 Microsoft 提供的高带宽 V100 cluster 上训练，并采用层内与层间模型并行。官方未发布训练代码、并行拓扑、检查点或完整硬件日程，175B 实验也超出大多数研究团队预算。

因此论文结果可被科学审查，但完整计算复现受代码、数据、模型权重与成本共同限制。
