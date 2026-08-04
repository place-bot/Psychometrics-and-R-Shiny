# 监督微调：为什么少量高质量数据有效

## 1. SFT 的作用

预训练模型会预测自然续写。SFT 用明确 prompt—answer 对教它：

- 区分 user request 与 assistant response；
- 直接回答指令；
- 使用对话风格；
- 在初始阶段遵循安全规范；
- 输出预期长度与结构。

## 2. 数据来源与筛选

作者先用公开 instruction-tuning data 启动，再发现很多第三方数据缺乏多样性或对话质量。随后集中采集 vendor-based 高质量样本。

实验结论是质量比盲目堆数量更关键：放弃数百万条较弱第三方样本后，使用数万条自采高质量标注反而改善结果。最终在

\[
27{,}540
\]

条 SFT annotation 时停止继续采集。

论文明确说明没有使用 Meta 用户数据。

## 3. 标注内容

标注者同时编写 prompt 与理想 answer，分为帮助性和安全性场景。安全样本包含可能诱发不当内容的 prompt 以及符合指南的安全回答。

作者抽查 180 个例子，把人工答案与 SFT 模型采样对比，发现模型输出经常已能与人工 SFT 数据竞争，于是把后续标注资源更多投入偏好比较。

## 4. Loss mask

一条样本序列为：

\[
s=[p_1,\ldots,p_m,y_1,\ldots,y_n].
\]

模型前向仍读取 prompt；loss 只在 answer token 上计算：

\[
\mathcal L_{\mathrm{SFT}}
=
-\sum_{t=1}^{n}
\log p_\theta(y_t\mid p,y_{<t}).
\]

prompt token 的 loss 被置零，避免训练目标浪费在复述用户输入。

## 5. 训练配置

- 初始 learning rate：\(2\times10^{-5}\)；
- cosine schedule；
- weight decay：0.1；
- batch size：64；
- sequence length：4096；
- 训练 2 epochs。

作者把多个 prompt 和 answer 拼接以填满序列，并用 special token 分隔字段。

## 6. 为什么 SFT 后仍需要 RLHF

SFT 受限于人工答案的写作分布：

- 标注者风格差异会被整体模仿；
- 低质量尾部答案也进入 token loss；
- 写一个理想长答案比比较两个答案昂贵；
- 模型可能探索出比标注者更好的表达，但 SFT 不会主动选择它。

偏好数据允许人类只判断“哪个更好”。reward model 再把这种序列级判断扩展到大量模型采样。

## 7. “少量”需要放在上下文里理解

27,540 相对数百万 instruction 样本较少，但它建立在：

- 2T-token 预训练；
- 公开 instruction data bootstrap；
- 后续 140 万以上 Meta preference comparisons；
- 多轮 rejection sampling 与 PPO；
- 安全专项数据。

因此论文支持“高质量 SFT seed 可以较小”，不支持“整个对话对齐只需两万多样本”。
