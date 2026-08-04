# 全量微调的问题与 LoRA 创新

## 1. 多任务部署成本

全量微调从 \(\Phi_0\) 出发，为每个任务学习同维更新 \(\Delta\Phi_t\)：

\[
\Phi_t=\Phi_0+\Delta\Phi_t.
\]

若基座有 175B 参数，每个任务保存一份完整模型会迅速扩大存储、加载和服务成本；Adam 还要为可训练参数维护梯度与两个动量状态。

## 2. 参数高效目标

论文希望用小参数集 \(\Theta_t\) 编码任务更新：

\[
\Delta\Phi_t=\Delta\Phi(\Theta_t),
\qquad
|\Theta_t|\ll|\Phi_0|.
\]

训练只优化 \(\Theta_t\)：

\[
\max_{\Theta}
\sum_{(x,y)\in\mathcal Z}\sum_t
\log p_{\Phi_0+\Delta\Phi(\Theta)}
(y_t\mid x,y_{<t}).
\]

## 3. 低内在秩假设

论文受到“微调具有低内在维度”研究启发，提出下游适配所需的矩阵更新 \(\Delta W\) 可能集中在低维子空间。于是用 \(\Delta W=BA\) 直接限制其秩。

## 4. 贡献

- 冻结预训练权重，训练并行低秩分支；
- 参数和 optimizer state 大幅减少；
- 部署时可将 \(BA\) 合并进 \(W_0\)，无额外网络深度；
- 在 RoBERTa、DeBERTa、GPT-2、GPT-3 上与全量微调相当或更优；
- 比较 Q/K/V/O 投影与不同 rank；
- 用奇异子空间分析解释低秩更新。

## 5. 原论文规模结论

GPT-3 175B 设置中，论文报告：

- 可训练参数最多降低约 10,000 倍；
- 训练显存从约 1.2TB 降到约 350GB；
- rank 4、只适配 Q/V 时任务 checkpoint 约 35MB；
- 训练吞吐从每 V100 32.5 tokens/s 提升到 43.1 tokens/s；
- 合并权重后不增加推理 latency。

这些数字依赖特定模型、精度、分片与优化器设置，不能直接套用于任意现代训练栈。
