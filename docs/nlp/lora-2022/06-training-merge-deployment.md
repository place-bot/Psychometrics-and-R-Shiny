# 训练、保存、合并与任务切换

## 1. 训练

冻结 \(W_0\)，只让 `lora_A`、`lora_B` 与可选 bias 获得梯度。前向：

\[
y=xW_0^\top
+s\,xA^\top B^\top.
\]

## 2. 保存

checkpoint 只需保存 LoRA 参数和必要配置：

- target module；
- rank \(r\)；
- \(\alpha\)；
- dropout；
- bias 策略；
- 基座模型身份与版本。

只有 \(A,B\) 而缺少基座版本，无法恢复完整任务模型。

## 3. 合并

部署前计算

\[
W_{\text{merged}}
=
W_0+sBA.
\]

推理恢复普通线性层：

\[
y=W_{\text{merged}}x.
\]

因此不会增加 adapter 那样的额外串行层。

## 4. 取消合并与切换

\[
W_0
=
W_{\text{merged}}-sBA.
\]

再加入另一任务的 \(s'B'A'\)。实际系统需避免重复 merge、低精度累计误差和多线程并发修改共享权重。

## 5. 合并与动态路由的权衡

- 合并：单任务推理路径最简、无低秩分支 latency；
- 未合并：同一基座可按样本动态选择 adapter，但每次前向多算低秩分支；
- 一个 batch 混合不同已合并 LoRA 很困难，因为共享 \(W\) 无法同时代表多个任务。

## 6. 官方 `loralib` 行为

默认 `model.eval()` 会合并，`model.train()` 会取消合并；可设置 `merge_weights=False` 禁用。加载时先加载基座，再以 `strict=False` 加载 LoRA state dict。

## 7. 验证合并正确性

\[
\max|f_{\text{unmerged}}(x)-f_{\text{merged}}(x)|
\]

应仅有浮点误差。还要测试 train/eval 多次切换不会重复加减。
