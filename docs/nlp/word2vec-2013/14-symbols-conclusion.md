# 符号表、结论与阅读地图

## 1. 符号表

| 符号 | 含义 |
|---|---|
| \(\mathcal V\) | 词表 |
| \(V\) | 词表大小 |
| \(D\) | 词向量维度 |
| \(T\) | 训练语料词元数 |
| \(E\) | epoch 数 |
| \(Q\) | 单训练位置的近似计算量 |
| \(N\) | CBOW / NNLM 使用的上下文词数 |
| \(C\) | Skip-gram 最大窗口距离 |
| \(R\) | 随机采样的实际窗口半径 |
| \(H\) | NNLM / RNNLM 隐藏层维度 |
| \(w_t\) | 序列位置 \(t\) 的词 |
| \(\mathbf e_w\) | 词 \(w\) 的 one-hot 向量 |
| \(\mathbf v_w\) | 词 \(w\) 的输入向量 |
| \(W_{\mathrm{in}}\) | 输入词向量矩阵 |
| \(\mathbf h\) | 送入输出层的表示 |
| \(\mathbf u_n\) | Huffman 内部节点 \(n\) 的输出向量 |
| \(U\) | 全部内部节点向量矩阵 |
| \(L_w\) | 词 \(w\) 的 Huffman 路径长度 |
| \(n_{w,j}\) | 词 \(w\) 路径上的第 \(j\) 个内部节点 |
| \(y_{w,j}\) | 第 \(j\) 个二分类的目标标签 |
| \(p_j\) | 第 \(j\) 个路径分支的预测概率 |
| \(\eta\) | 学习率 |
| \(\sigma\) | sigmoid 函数 |

## 2. 四种模型的复杂度

总训练复杂度：

\[
O=E\times T\times Q.
\]

前馈 NNLM：

\[
Q=ND+NDH+HV.
\]

RNNLM：

\[
Q=H^2+HV.
\]

CBOW + hierarchical softmax：

\[
Q=ND+D\log_2V.
\]

Skip-gram + hierarchical softmax：

\[
Q=C(D+D\log_2V).
\]

## 3. 两个核心目标

CBOW：

\[
\max_\Theta
\sum_{t=1}^{T}
\log P(w_t\mid\mathcal C_t).
\]

Skip-gram：

\[
\max_\Theta
\sum_{t=1}^{T}
\sum_{\substack{-c\le j\le c\\j\neq0}}
\log P(w_{t+j}\mid w_t).
\]

## 4. Hierarchical-softmax 概率

\[
P(w\mid\mathbf h)
=\prod_{j=1}^{L_w}
p_j^{y_{w,j}}(1-p_j)^{1-y_{w,j}},
\]

\[
p_j
=\sigma(\mathbf u_{n_{w,j}}^\top\mathbf h).
\]

单路径节点误差：

\[
\delta_j=p_j-y_{w,j}.
\]

输入表示梯度：

\[
\frac{\partial\mathcal L}{\partial\mathbf h}
=\sum_j\delta_j\mathbf u_{n_{w,j}}.
\]

节点向量梯度：

\[
\frac{\partial\mathcal L}{\partial\mathbf u_{n_{w,j}}}
=\delta_j\mathbf h.
\]

## 5. CBOW 与 Skip-gram 的最短区分

```text
CBOW
上下文词向量 ──平均──► h ──HS──► 中心词

Skip-gram
中心词向量 ─────────► h ──HS──► 每个附近词
```

CBOW 每个中心位置聚合一次；Skip-gram 把中心位置展开为多个预测对。

## 6. 类比评价

给定

\[
a:b::c:d,
\]

查询：

\[
\mathbf q
=\mathbf v_b-\mathbf v_a+\mathbf v_c.
\]

输出：

\[
\widehat d
=\arg\max_{w\notin\{a,b,c\}}
\operatorname{cos}(\mathbf v_w,\mathbf q).
\]

公开数据包含 19,544 题：8,869 题语义类比与 10,675 题句法类比。

## 7. 论文的核心实验事实

1. Table 2：更多数据和更高维度共同增加时，准确率最高。
2. Table 3：固定 320M 数据与 640 维后，Skip-gram 语义准确率最高，CBOW 句法准确率最高。
3. Table 4：300 维 Skip-gram 在综合类比上达到 53.3%。
4. Table 5：看 1.6B 新 token 一个 epoch，可达到或超过在 783M token 上重复三个 epoch。
5. Table 6：6B 数据、1,000 维 Skip-gram 达到 65.6%，约 2.5 天 × 125 CPU 核。
6. Table 7：Skip-gram 单独句子补全为 48.0%，与 RNNLM 组合达到 58.9%。

## 8. 论文贡献的层次

### 模型层

提出 CBOW 与 Continuous Skip-gram 两种对数线性架构。

### 计算层

去除昂贵隐藏层，配合 Huffman hierarchical softmax 和分布式训练。

### 数据层

把训练扩展到十亿级 token、百万级词表和千维表示。

### 评价层

建立语义—句法类比测试，用向量差值和 top-1 检索量化线性关系。

### 应用层

证明词向量得分能与 RNNLM 互补，并讨论检索、翻译、问答和知识库等应用。

## 9. 三个常见混淆

### 9.1 Word2Vec 与单一模型

Word2Vec 通常指一组训练词向量的架构和工具，至少包含 CBOW 与 Skip-gram 两种方向。

### 9.2 本文与 negative sampling

本文的输出机制主要是 hierarchical softmax。Negative Sampling、频繁词下采样和短语学习由同年后续 NIPS 论文系统提出。

### 9.3 类比与完整语言理解

向量类比测量稳定线性关系。完整语言理解还需要上下文消歧、词序、组合、事实与推理能力。

## 10. 对现代 NLP 的启发

这篇论文留下的思想包括：

- 用自监督局部预测学习可迁移表示；
- 通过参数共享把稀疏符号映射到连续空间；
- 让单步训练足够便宜，再扩大数据和维度；
- 用近似输出目标处理巨大类别空间；
- 用探测任务分析表示中保留的结构；
- 把预训练表示导出并复用于下游任务。

现代预训练语言模型扩大了上下文、模型深度和训练目标，但这些基本设计原则仍然清晰可见。

## 11. 最终结论

论文最重要的结果可以写成一条计算预算链：

\[
\text{删除昂贵隐藏层}
\Longrightarrow
Q\downarrow
\Longrightarrow
T,D,V\uparrow
\Longrightarrow
\text{词向量关系质量提高}.
\]

CBOW 和 Skip-gram 的影响来自这条完整链路。架构简洁、训练规模和评价方法共同构成了 Word2Vec 的历史突破。

## 12. 后续阅读地图

建议按问题继续：

| 问题 | 后续论文方向 |
|---|---|
| 怎样进一步降低输出训练成本？ | SGNS、NCE |
| 怎样解释 Word2Vec 与共现矩阵的关系？ | SGNS 隐式矩阵分解 |
| 怎样使用全局共现统计？ | GloVe |
| 怎样加入字符和形态？ | fastText |
| 怎样处理一词多义？ | 多原型嵌入、ELMo |
| 怎样学习深层双向上下文？ | BERT |
| 怎样统一理解大规模自监督表示？ | Transformer 语言模型 |

参考入口见[参考文献与资料](references.md)。
