# 符号表、结论与阅读地图

## 1. 核心符号

| 符号 | 含义 |
|---|---|
| \(\mathbf x=(x_1,\ldots,x_{T_x})\) | 源句 |
| \(\mathbf y=(y_1,\ldots,y_{T_y})\) | 目标句 |
| \(\overrightarrow{\mathbf h}_j\) | 正向编码状态 |
| \(\overleftarrow{\mathbf h}_j\) | 反向编码状态 |
| \(\mathbf h_j\) | 双向源注释 |
| \(\mathbf s_i\) | 第 \(i\) 个目标步骤的解码状态 |
| \(e_{ij}\) | 未归一化对齐分数 |
| \(\alpha_{ij}\) | 源位置 \(j\) 的归一化权重 |
| \(\mathbf c_i\) | 当前动态上下文 |
| \(\mathbf z_i,\mathbf r_i\) | update/reset gate |
| \(\mathbf E_y[y]\) | 目标词 embedding |
| \(\mathbf o_i\) | 词表 logits |
| \(\mathcal L\) | 负对数似然 |

## 2. 五个核心公式

\[
p(\mathbf y\mid\mathbf x)
=
\prod_i p(y_i\mid y_{<i},\mathbf x)
\]

\[
\mathbf h_j
=
[\overrightarrow{\mathbf h}_j;
\overleftarrow{\mathbf h}_j]
\]

\[
e_{ij}
=
\mathbf v_a^\top
\tanh(\mathbf W_a\mathbf s_{i-1}+\mathbf U_a\mathbf h_j)
\]

\[
\alpha_{ij}
=
\frac{\exp(e_{ij})}{\sum_k\exp(e_{ik})}
\]

\[
\mathbf c_i
=
\sum_j\alpha_{ij}\mathbf h_j
\]

## 3. 算法全景

1. 双向 GRU 将源句编码为一列上下文化注释；
2. 解码器旧状态与每个注释计算 additive score；
3. masked softmax 得到源位置分布；
4. 加权和形成当前上下文；
5. 前一目标词、旧状态和上下文更新 GRU；
6. deep output 与 maxout 产生词表概率；
7. 训练用参考目标词交叉熵端到端更新；
8. 推理用 beam search近似寻找高概率序列。

## 4. 论文的核心证据

- 相同长度条件下，RNNsearch 比固定向量基线高约 7–9 BLEU；
- 长度分组曲线显示 RNNsearch 对长句更稳健；
- RNNsearch-30 可超过 RNNencdec-50，说明增加训练长度没有消除固定向量瓶颈；
- 对齐热图呈现词序相近、重排和多对一模式；
- No-UNK 与完整测试集差距揭示词级封闭词表的限制。

## 5. 一句话结论

Bahdanau、Cho 与 Bengio 把神经机器翻译从“整句一次压缩”推进到“每生成一个词都动态读取源句”，并让读取规则直接接受翻译损失训练。

## 6. 与下一篇论文的接口

RNNsearch 已经拥有 query、源表示、归一化权重和加权读取，但 query 来自递归状态。Vaswani et al. (2017) 的 **Attention Is All You Need** 会进一步：

- 用 self-attention 构造序列表示；
- 用 scaled dot-product 取代 additive score；
- 用 multi-head 并行学习不同关系；
- 用位置编码补回顺序；
- 移除训练中的 RNN 时间步依赖。

因此，下一篇应重点观察“动态读取”如何演化成完整的序列建模骨架。

## 7. 回查入口

- 数学机制：[Additive Attention](05-additive-attention.md)
- 梯度：[端到端训练](06-end-to-end-training.md)
- 手算：[逐步手算](09-worked-example.md)
- 实验：[实验设计](10-experiment-design.md)与[BLEU 结果](11-results-and-length-analysis.md)
- 代码：[GroundHog 精读](13-groundhog-code-reading.md)
- 并行化：[复杂度与并行化](15-attention-interpretation-and-complexity.md)
- 文献：[参考文献](references.md)
