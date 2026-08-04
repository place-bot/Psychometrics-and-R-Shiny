# Beam Search 与推理

## 1. 序列搜索目标

\[
\widehat{\mathbf y}
=
\arg\max_{\mathbf y}
\log p(\mathbf y\mid\mathbf x)
=
\arg\max_{\mathbf y}
\sum_i\log p(y_i\mid y_{<i},\mathbf x).
\]

候选空间随词表与长度指数增长，实际使用近似搜索。

## 2. Greedy 与 beam search

贪心解码每步只保留当前概率最大的词。beam search 保留 \(B\) 条前缀，对每条前缀扩展候选词，再按累计成本留下最优的 \(B\) 条：

\[
C(\mathbf y_{1:i})
=
-\sum_{t=1}^{i}
\log p(y_t\mid y_{<t},\mathbf x).
\]

遇到 \(\langle EOS\rangle\) 的路径进入完成集合。

## 3. 每条 beam 的状态

不同前缀拥有不同的

\[
\mathbf s_i,\qquad
\boldsymbol\alpha_i,\qquad
\mathbf c_i.
\]

搜索程序要同时保存 token 前缀、累计成本、解码状态和完成标记。源端注释可由所有 beam 共享。

## 4. 长度偏好

每个条件对数概率不大于 0，原始序列分数容易偏向短译文。常见处理包括长度归一化、长度惩罚、最短长度和覆盖惩罚。它们会改变解码准则，应独立报告。

## 5. 论文与代码的边界

论文说明使用 beam search，但没有明确报告 beam width。作者的 GroundHog 代码展示了维护候选、屏蔽 \([UNK]\)、可选长度归一化以及长度边界等历史实现。主结果中未报告的配置仍构成复现不确定性。

## 6. \([UNK]\) 与两组 BLEU

词表只保留各语言最频繁的 30,000 个词，其他词映射为 \([UNK]\)。论文报告：

- **All**：完整测试集；
- **No UNK**：源句和参考译文都没有未知词的子集，并禁止模型生成 \([UNK]\)。

No-UNK 结果刻画词表覆盖较充分的情形，需要与完整测试集分开解释。

## 7. Teacher forcing 与部署

训练使用 \(y_{i-1}^{\text{gold}}\)，推理使用模型生成的 \(\widehat y_{i-1}\)。早期错误会改变后续状态和 attention。beam search 同时保留多条前缀，可以缓解单次贪心决策造成的搜索错误，仍无法消除训练—推理分布偏移。

## 8. 简化算法

```python
beams = [(0.0, [BOS], initial_state)]
finished = []

for step in range(max_length):
    candidates = []
    for cost, tokens, state in beams:
        alpha, context = attend(state, annotations)
        new_state, log_probs = decoder_step(
            tokens[-1], state, context
        )
        for token in top_tokens(log_probs, beam_size):
            new_cost = cost - log_probs[token]
            if token == EOS:
                finished.append((new_cost, tokens + [token]))
            else:
                candidates.append(
                    (new_cost, tokens + [token], new_state)
                )
    beams = keep_best(candidates, beam_size)
```

工程实现通常把 beam 维度向量化，并根据父路径索引重排隐藏状态。

## 9. 主要计算

每个目标步包含 \(B\) 条路径的 decoder 更新、对 \(T_x\) 个源位置的 attention，以及 30k 词表读出。增大 beam width 会增加搜索覆盖，同时增加时间、显存与状态管理成本。

## 本页小结

attention 决定每一步读取哪些源信息，beam search 决定保留哪些目标前缀。复现要同时报告模型参数、词表策略、beam width、长度规则与 \([UNK]\) 处理。
