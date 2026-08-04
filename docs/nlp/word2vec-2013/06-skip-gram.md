# Skip-gram：从中心词预测上下文

## 1. 任务方向

Skip-gram 以中心词 \(w_t\) 为输入，预测附近的每个词：

\[
P(w_{t+j}\mid w_t),
\qquad -c\le j\le c,\quad j\neq0.
\]

它把一个中心位置展开成多个训练对：

\[
(w_t,w_{t-c}),\ldots,(w_t,w_{t-1}),
(w_t,w_{t+1}),\ldots,(w_t,w_{t+c}).
\]

## 2. 语料目标

固定窗口半径 \(c\) 时，常见写法为

\[
\max_\Theta
\sum_{t=1}^{T}
\sum_{\substack{-c\le j\le c\\j\neq0}}
\log P(w_{t+j}\mid w_t).
\]

使用 hierarchical softmax 时，输入表示就是中心词向量：

\[
\mathbf h_t=\mathbf v_{w_t}.
\]

每个上下文目标 \(o=w_{t+j}\) 的概率为

\[
P(o\mid w_t)
=\prod_{r=1}^{L_o}
p_r^{y_r}(1-p_r)^{1-y_r},
\]

\[
p_r
=\sigma(\mathbf u_{n_{o,r}}^\top\mathbf v_{w_t}).
\]

## 3. 单个中心—上下文对的梯度

对训练对 \((i,o)\)，其中 \(i\) 是输入中心词、\(o\) 是输出上下文词：

\[
\mathcal L(i,o)
=-\sum_{r=1}^{L_o}
\left[y_r\log p_r+(1-y_r)\log(1-p_r)\right].
\]

输入中心词向量的梯度为

\[
\frac{\partial\mathcal L(i,o)}{\partial\mathbf v_i}
=\sum_{r=1}^{L_o}
(p_r-y_r)\mathbf u_{n_{o,r}}.
\]

输出路径节点的梯度为

\[
\frac{\partial\mathcal L(i,o)}
{\partial\mathbf u_{n_{o,r}}}
=(p_r-y_r)\mathbf v_i.
\]

一个中心词会对多个上下文目标累计更新，其总梯度为各训练对梯度之和。

## 4. 动态窗口

论文设最大距离为 \(C\)。对每个中心词，随机抽取

\[
R\sim\operatorname{Uniform}\{1,2,\ldots,C\},
\]

再使用左右各 \(R\) 个词。

距离中心为 \(d\) 的词被纳入窗口，当且仅当 \(R\ge d\)。因此

\[
P(\text{纳入距离 }d)
=P(R\ge d)
=\frac{C-d+1}{C}.
\]

近处词出现频率更高。例如 \(C=5\)：

| 距离 \(d\) | 纳入概率 |
|---:|---:|
| 1 | \(1\) |
| 2 | \(4/5\) |
| 3 | \(3/5\) |
| 4 | \(2/5\) |
| 5 | \(1/5\) |

每个中心词的期望预测数为

\[
2\mathbb E[R]
=2\cdot\frac{C+1}{2}
=C+1.
\]

论文复杂度用 \(C\) 表示这一线性增长，忽略常数差异。

## 5. 为什么大窗口更偏向语义

较近上下文常包含局部句法约束，例如限定词、时态和词形；较远上下文更容易反映主题和语义场。扩大窗口会增加较远共现信号，也会混入更多噪声。

论文报告随着范围扩大，向量质量提高，但计算量同步增加。实验使用 \(C=10\)。这个结论依赖其类比测试与新闻语料，不能直接推出所有任务都应选择大窗口。

## 6. CBOW 与 Skip-gram 的结构对照

| 维度 | CBOW | Skip-gram |
|---|---|---|
| 输入 | 多个上下文词 | 一个中心词 |
| 聚合 | 求和或平均 | 无上下文聚合 |
| 输出 | 一个中心词 | 多个附近词 |
| 单中心位置训练项 | 约 1 个 | 约 \(C+1\) 个 |
| 原文复杂度 | \(ND+D\log_2V\) | \(C(D+D\log_2V)\) |
| Table 3 优势 | 句法 | 语义 |

两者使用同一语料窗口，预测方向和样本分解方式不同。

## 7. 一个中心词的完整更新

设中心词 `bank` 的实际窗口包含四个目标：

\[
\{\text{river},\text{near},\text{loan},\text{approved}\}.
\]

Skip-gram 形成四项损失：

\[
\mathcal L_t
=\mathcal L(\text{bank},\text{river})
+\mathcal L(\text{bank},\text{near})
+\mathcal L(\text{bank},\text{loan})
+\mathcal L(\text{bank},\text{approved}).
\]

`bank` 的单一输入向量接收四项梯度。多义词的不同语境因此被压进同一静态向量，最终形成混合表示。

## 8. 复杂度

论文式 (5) 为

\[
Q_{\mathrm{SG}}
=C\left(D+D\log_2V\right).
\]

其中：

- 每个预测需访问输入向量，记为 \(D\)；
- Huffman 路径约需 \(D\log_2V\)；
- 一个中心位置产生与窗口宽度成正比的预测。

Skip-gram 比 CBOW 慢，但每个词—上下文对获得独立训练信号。论文 Table 5 中，300 维、783M 词、3 epoch 的 CBOW 用约 1 天，Skip-gram 用约 3 天。

## 9. 训练方向与表示方向

模型训练 \(P(\text{context}\mid\text{center})\)。最终使用的是中心词输入向量 \(\mathbf v_w\)。一个词的向量要能够让其常见上下文在各自 Huffman 路径上获得高概率。

公开 C 代码中的变量命名和循环方向容易让读者困惑：代码对窗口内的 `last_word` 使用 `syn0`，并沿当前 `word` 的输出路径更新。由于滑动语料会反复产生相邻词对，整体仍学习双向共现结构；精确复刻时应以代码实际的输入—输出方向为准，理论讲解则按论文图 1 的“中心词预测周围词”定义。

## 10. Skip-gram 的信息流

```text
中心词索引
   │ 查 W_in
   ▼
中心词向量 v_i
   │ 对每个采样到的上下文目标重复
   ▼
目标词 Huffman 路径
   │ 多个 sigmoid
   ▼
路径交叉熵
   │
   ├── 更新目标路径节点向量
   └── 更新中心词输入向量
```

这个结构把序列学习问题转成大量共享参数的局部预测问题。
