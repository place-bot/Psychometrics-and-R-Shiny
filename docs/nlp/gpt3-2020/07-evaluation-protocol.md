# Prompt 构造与评测协议

## 1. Few-shot 示例抽样

对每个 evaluation example，论文通常从该任务 training set 随机抽取 \(K\) 个示例作为 conditioning，并用一至两个换行分隔。LAMBADA 与 StoryCloze 没有标准监督训练集，示例从 development set 抽取，最终在 test set 评价。

## 2. Prompt 的组成

一个完整 prompt 可能含：

\[
c=
[\text{instruction};
\text{demo}_1;\ldots;\text{demo}_K;
\text{query}].
\]

不同任务会：

- 添加自然语言任务说明；
- 调整答案格式；
- 把 classification 写成 completion；
- 使用候选答案比较；
- 限制生成到换行或分隔符。

## 3. Test 与 development

公开 test server 可用时报告 test 结果。部分 private test server 无法容纳模型，论文改报 development 结果。比较表中的数字必须核对 split；论文 Figure 1.1 的 GPT-3 SuperGLUE 曲线使用 dev，而参考虚线来自 test，正文明确提醒不能直接等同比较。

## 4. 自由生成

自由形式 completion 使用 beam search：

\[
\text{beam width}=4,
\qquad
\alpha=0.6
\]

的 length penalty。其他任务会采用特定 scoring 或 sampling。评测行为因此不是统一 greedy decoding。

## 5. 多 token 标签与长度偏差

若候选答案长度不同，原始联合概率天然偏向较短序列，因为每个 token 概率都小于等于 1：

\[
p(y\mid c)=\prod_{r=1}^{|y|}p(y_r\mid c,y_{<r}).
\]

可用平均 log-probability：

\[
S_{\mathrm{avg}}(y;c)
=
\frac{1}{|y|}
\sum_{r=1}^{|y|}\log p(y_r\mid c,y_{<r}),
\]

但是否归一化应遵循具体 benchmark 规则。论文附录为不同任务给出具体格式。

## 6. SuperGLUE 的示例设置

few-shot SuperGLUE 对每个任务使用 32 个示例。除 WSC 与 MultiRC 外，每道 evaluation problem 重新随机采样 conditioning examples；WSC 和 MultiRC 为所有问题复用同一组随机示例。

因此结果同时反映：

- 模型规模；
- prompt 设计；
- 32 个示例的具体抽样；
- 答案评分与 split。

## 7. Prompt 选择也是一种研究者自由度

同一任务可写成多种自然语言模板。论文报告 WiC 尝试了多种措辞仍没有强结果，这说明 prompt engineering 可以排除某些表面失败，但也引入选择偏差：如果只报告最优模板，benchmark 会吸收额外调参。

严谨复现需要保存：

- 完整 prompt 字符串；
- 示例 ID 与顺序；
- 随机种子；
- tokenizer 与截断规则；
- decoding/scoring 参数；
- exact evaluation script。

## 8. “没有训练”与“没有调参”要分开

GPT-3 下游没有梯度更新，但研究仍可能在 prompt、格式、\(K\)、分隔符和 decoding 上作选择。参数学习成本被移除，任务接口设计成本仍然存在。
