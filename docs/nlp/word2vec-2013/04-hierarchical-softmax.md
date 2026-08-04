# Huffman Hierarchical Softmax

## 1. 大词表 softmax 的成本

给定隐藏表示 \(\mathbf h\in\mathbb R^D\)，完整 softmax 为每个词计算分数

\[
z_w=\mathbf u_w^\top\mathbf h,
\]

并归一化：

\[
P(w\mid\mathbf h)
=\frac{\exp(z_w)}
{\sum_{w'\in\mathcal V}\exp(z_{w'})}.
\]

分母需要遍历 \(V\) 个词，每个分数包含 \(D\) 维点积，因此一次预测约为 \(O(VD)\)。百万词表下，这会主导训练成本。

## 2. 把多分类改写为树上决策

Hierarchical softmax 把每个词放在二叉树叶节点。预测一个词等价于从根节点出发，依次选择左或右，最终到达该词。

若词 \(w\) 的路径经过内部节点

\[
n_{w,1},n_{w,2},\ldots,n_{w,L_w},
\]

对应分支标签为

\[
y_{w,1},y_{w,2},\ldots,y_{w,L_w},
\qquad y_{w,j}\in\{0,1\},
\]

则只需计算 \(L_w\) 次二分类。

树中每个内部节点 \(n\) 有输出向量

\[
\mathbf u_n\in\mathbb R^D.
\]

在节点 \(n\) 选择标签 1 的概率定义为

\[
p_n(1\mid\mathbf h)
=\sigma(\mathbf u_n^\top\mathbf h),
\qquad
\sigma(x)=\frac{1}{1+e^{-x}}.
\]

选择标签 0 的概率为 \(1-p_n\)。

## 3. 一个词的概率

词 \(w\) 的条件概率是整条路径上分支概率的乘积：

\[
P(w\mid\mathbf h)
=\prod_{j=1}^{L_w}
p_{n_{w,j}}^{\,y_{w,j}}
(1-p_{n_{w,j}})^{1-y_{w,j}}.
\]

这里乘号的每个因子应理解为

\[
p_{n_{w,j}}^{\,y_{w,j}}
(1-p_{n_{w,j}})^{1-y_{w,j}}
=
\begin{cases}
p_{n_{w,j}}, & y_{w,j}=1,\\
1-p_{n_{w,j}}, & y_{w,j}=0.
\end{cases}
\]

由于每个叶节点对应唯一根到叶路径，所有叶词的概率总和为 1。模型仍然给出规范化词分布。

## 4. Huffman 树为什么更快

平衡二叉树的路径长度约为

\[
\log_2V.
\]

Huffman 编码根据词频构树：

- 高频词获得较短编码；
- 低频词允许较长编码；
- 平均路径长度接近该频率分布的编码下界。

训练样本本身也按词频出现，所以高频目标词被频繁访问，而它们恰好拥有短路径。原文用“约 \(\log_2(\text{unigram perplexity})\)”描述平均输出数量，并报告百万词表相对平衡树可约快两倍。

## 5. 单个目标词的损失

对目标词 \(w\)，负对数似然为

\[
\mathcal L(w,\mathbf h)
=-\log P(w\mid\mathbf h).
\]

展开得到沿路径的二元交叉熵：

\[
\mathcal L(w,\mathbf h)
=-\sum_{j=1}^{L_w}
\left[
y_{w,j}\log p_j
+(1-y_{w,j})\log(1-p_j)
\right],
\]

其中

\[
p_j=\sigma(\mathbf u_{n_{w,j}}^\top\mathbf h).
\]

因此一次词预测只训练目标路径上的 \(L_w\) 个二分类器。

## 6. 梯度

记

\[
z_j=\mathbf u_{n_{w,j}}^\top\mathbf h.
\]

逻辑回归交叉熵对 logit 的导数为

\[
\frac{\partial\mathcal L}{\partial z_j}
=p_j-y_{w,j}.
\]

于是内部节点向量的梯度为

\[
\frac{\partial\mathcal L}
{\partial\mathbf u_{n_{w,j}}}
=(p_j-y_{w,j})\mathbf h,
\]

输入表示的梯度为

\[
\frac{\partial\mathcal L}{\partial\mathbf h}
=\sum_{j=1}^{L_w}
(p_j-y_{w,j})\mathbf u_{n_{w,j}}.
\]

学习率为 \(\eta\) 时，SGD 更新为

\[
\mathbf u_{n_{w,j}}
\leftarrow
\mathbf u_{n_{w,j}}
-\eta(p_j-y_{w,j})\mathbf h,
\]

\[
\mathbf h
\leftarrow
\mathbf h
-\eta\sum_j(p_j-y_{w,j})\mathbf u_{n_{w,j}}.
\]

实现中应先用更新前的节点向量累积 \(\partial\mathcal L/\partial\mathbf h\)，再写回输入向量，避免顺序更新改变同一个样本的梯度。

## 7. 三层路径的数值例子

设某词的路径标签为

\[
(y_1,y_2,y_3)=(1,0,1),
\]

模型得到

\[
(p_1,p_2,p_3)=(0.8,0.3,0.6).
\]

目标词概率为

\[
P(w\mid\mathbf h)
=0.8\times(1-0.3)\times0.6
=0.336.
\]

损失为

\[
\mathcal L=-\log(0.336)\approx1.0906.
\]

三个 logit 梯度分别是

\[
(p_1-y_1,p_2-y_2,p_3-y_3)
=(-0.2,0.3,-0.4).
\]

第一个和第三个节点需要提高标签 1 的概率，第二个节点需要降低标签 1 的概率。

## 8. 参数规模

含 \(V\) 个叶节点的满二叉树有 \(V-1\) 个内部节点。输出参数约为

\[
(V-1)D,
\]

与完整 softmax 的 \(VD\) 同阶。hierarchical softmax 主要节省每个样本参与计算的输出向量数量，而非显著减少总参数。

## 9. 与 negative sampling 的边界

本文实验主要使用 Huffman hierarchical softmax。Negative Sampling 在同年后续论文 **Distributed Representations of Words and Phrases and their Compositionality** 中提出，它用一个真实词和若干噪声词构造二分类目标。

两者的差别包括：

| 维度 | Hierarchical softmax | Negative sampling |
|---|---|---|
| 输出结构 | Huffman 树内部节点 | 词表中的输出词向量 |
| 每样本成本 | 目标路径长度 | \(1+k\) 个正负样本 |
| 是否形成规范化全词分布 | 是 | 训练目标本身不直接给出完整归一化分布 |
| 在本文中的地位 | 核心输出机制 | 尚未提出 |

后来的公开 `word2vec.c` 同时支持 `-hs` 和 `-negative`，其功能范围已经超过本文原始实验。

## 10. 阅读 hierarchical softmax 的关键

它完成三次替换：

1. \(V\) 类 softmax 被替换为树路径；
2. 一次巨大归一化被替换为若干 sigmoid；
3. 每步更新 \(V\) 个输出向量被替换为更新目标路径上的内部节点。

CBOW 与 Skip-gram 的差别决定 \(\mathbf h\) 从哪里来；hierarchical softmax 负责把这个 \(\mathbf h\) 转成目标词概率。
