# Masked Language Model 与 80/10/10

## 1. 采样

每条序列随机选择 15% 的 WordPiece 位置作为预测目标。损失只在这些位置计算：

\[
\mathcal L_{\text{MLM}}
=
-\sum_{i\in\mathcal M}
\log p(x_i\mid\widetilde{\mathbf x}).
\]

\(\mathcal M\) 是被选目标集合，\(\widetilde{\mathbf x}\) 是破坏后的输入。

## 2. 80/10/10

对已选中的 15% 位置：

- 80% 替换为 `[MASK]`；
- 10% 替换为随机词；
- 10% 保持原词。

占全部 token 的期望比例约为：

\[
12\%\ [MASK],\qquad
1.5\%\ \text{随机},\qquad
1.5\%\ \text{不变且仍预测}.
\]

## 3. 为什么不全部换成 [MASK]

`[MASK]` 在下游微调输入中通常不会出现。随机词与原词分支减少预训练—微调输入差异，并迫使模型对普通 token 也保持可用表示。

保持原词的目标位置虽然能看到自身，但模型不知道哪些普通 token 被选中，且只占少量；整体任务仍需要上下文。

## 4. MLM 输出头

选中位置表示先经过 dense、GELU、LayerNorm，再与词 embedding 矩阵共享的输出权重计算词表 logits：

\[
\mathbf o_i
=
\operatorname{LN}(
\operatorname{GELU}(
\mathbf T_i\mathbf W+\mathbf b))
\mathbf E_{\text{vocab}}^\top
+\mathbf b_{\text{vocab}}.
\]

## 5. MLM 的效率代价

每个序列只有 15% 位置提供直接词预测损失，训练信号比 left-to-right LM 稀疏。论文 FAQ 也指出 MLM 收敛速度较慢；它换取了每个 token 的深层双向上下文。

## 6. 静态 mask

原始代码离线生成 TFRecord，`dupe_factor` 多次复制文档片段并随机产生不同 mask。它不是每个训练 epoch 在线无限重采样；RoBERTa 后来强调动态 masking。

## 7. 常见混淆

- 15% 是被选作预测目标的比例；
- 80/10/10 只在这 15% 内分配；
- 损失也要计算那 10% 保持原词的位置；
- 特殊 token 不参与 mask；
- 原论文按 WordPiece 独立选择，不是 whole-word mask。
