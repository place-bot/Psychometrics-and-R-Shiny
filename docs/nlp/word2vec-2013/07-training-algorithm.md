# SGD、反向传播与完整算法

## 1. 训练系统的组成

复现本文的 hierarchical-softmax 版本，需要以下对象：

1. 训练 token 序列；
2. 词频表与词到整数索引的映射；
3. Huffman 二叉树；
4. 输入词向量矩阵 \(W_{\mathrm{in}}\)；
5. 内部节点向量矩阵 \(U\)；
6. 上下文窗口采样器；
7. SGD 或并行优化器。

## 2. 预处理

### 2.1 词表

统计语料中的词频：

\[
f(w)=\sum_{t=1}^{T}\mathbb I(w_t=w).
\]

论文实验按最常见词限制词表：小规模比较使用 30K 词表，大规模 Google News 实验使用最多 1M 高频词。词表外 token 无法参与类比评价。

### 2.2 Huffman 树

初始化每个词的权重为 \(f(w)\)，反复合并当前频率最低的两个节点，直到只剩根节点。记录每个词：

- 根到叶的二进制 code；
- 路径经过的内部节点索引；
- 路径长度 \(L_w\)。

### 2.3 参数初始化

可用小范围均匀分布初始化输入向量：

\[
W_{\mathrm{in},ij}
\sim\operatorname{Uniform}
\left(-\frac{1}{2D},\frac{1}{2D}\right).
\]

公开 C 实现按这一量级初始化 `syn0`，把 hierarchical-softmax 节点向量 `syn1` 初始化为 0。论文正文没有详细规定初始化分布。

## 3. 学习率

Table 2 和 Table 4 对应实验使用：

\[
\eta_0=0.025,
\]

并在 3 个 epoch 内线性下降，使训练结束时接近 0。若已处理的训练位置比例为 \(\rho\in[0,1]\)，可以写为

\[
\eta(\rho)
=\eta_0(1-\rho).
\]

实现通常设置很小的下界，避免浮点数和异步计数造成负学习率。

分布式 DistBelief 实验使用 mini-batch 异步梯度和 AdaGrad，属于另一套优化配置。

## 4. Hierarchical-softmax 核心更新

输入表示为 \(\mathbf h\)，目标词为 \(o\)。对其路径上的每个节点 \(n_r\)：

1. 计算

    \[
    p_r=\sigma(\mathbf u_{n_r}^\top\mathbf h);
    \]

2. 计算误差

    \[
    \delta_r=p_r-y_r;
    \]

3. 累积输入梯度

    \[
    \mathbf g_h\mathrel{+}=\delta_r\mathbf u_{n_r};
    \]

4. 更新节点向量

    \[
    \mathbf u_{n_r}
    \leftarrow
    \mathbf u_{n_r}-\eta\delta_r\mathbf h.
    \]

遍历完路径后，用累计的 \(\mathbf g_h\) 更新输入表示的来源参数。

## 5. CBOW 完整伪代码

```text
for epoch in 1..E:
    for position t in corpus:
        context = valid words around t
        h = average(W_in[word] for word in context)
        target = w_t

        grad_h = 0
        for (node, branch_label) in huffman_path[target]:
            p = sigmoid(U[node] dot h)
            delta = p - branch_label
            grad_h += delta * U[node]          # 使用更新前参数
            U[node] -= learning_rate * delta * h

        for word in context:
            W_in[word] -= learning_rate * grad_h / len(context)
```

一个实现细节是：若上下文词重复出现，可按出现次数多次加梯度；若用唯一索引批量写回，需要显式累加重复位置。

## 6. Skip-gram 完整伪代码

```text
for epoch in 1..E:
    for position t in corpus:
        radius = UniformInteger(1, C)
        center = w_t

        for j in positions within radius around t, j != t:
            target = w_j
            h = W_in[center]
            grad_h = 0

            for (node, branch_label) in huffman_path[target]:
                p = sigmoid(U[node] dot h)
                delta = p - branch_label
                grad_h += delta * U[node]
                U[node] -= learning_rate * delta * h

            W_in[center] -= learning_rate * grad_h
```

若希望严格匹配某个历史公开版本，应进一步核对其中心词和窗口词在 `syn0`、目标路径中的实际方向。

## 7. 一次更新的形状检查

| 对象 | 形状 |
|---|---|
| \(W_{\mathrm{in}}\) | \(V\times D\) |
| \(U\) | \((V-1)\times D\) |
| \(\mathbf h\) | \(D\) |
| \(\mathbf u_n\) | \(D\) |
| \(p_r,delta_r\) | 标量 |
| \(\mathbf g_h\) | \(D\) |

点积 \(\mathbf u_n^\top\mathbf h\) 输出标量，节点梯度与输入梯度都保持 \(D\) 维。

## 8. 复杂度检查

若目标词路径长度为 \(L_o\)，一次 hierarchical-softmax 目标更新需约 \(L_o\) 个 \(D\) 维点积和向量更新：

\[
O(DL_o).
\]

平衡树下 \(L_o\approx\log_2V\)，Huffman 树下应使用按 token 频率加权的平均路径长度。

CBOW 额外读取 \(N\) 个上下文向量；Skip-gram 每个中心位置执行多次目标更新。这与论文式 (4)、式 (5) 一致。

## 9. 单机与分布式训练

### 9.1 单机 SGD

每读到一个位置就更新参数，数据顺序和线程调度会影响具体结果。多线程公开实现采用近似无锁更新，允许不同线程同时修改共享向量。

### 9.2 DistBelief

论文的并行版本包含：

- 多个模型 replica；
- 参数服务器；
- mini-batch 异步梯度；
- AdaGrad；
- 50–100 个 replica。

异步更新会引入陈旧梯度，但显著提高吞吐量。论文用最终类比准确率验证训练仍然有效。

## 10. epoch、数据量和维度

Table 5 比较了三种扩大训练量的方法：

- 同一 783M 语料训练 3 epoch；
- 1.6B 语料训练 1 epoch；
- 783M 语料、扩大向量维度、训练 1 epoch。

作者发现：看更多不同 token 的一个 epoch 可以达到或超过在较小语料上重复 3 次的结果。这支持“扩大数据覆盖”这一设计取向。

## 11. 数值稳定性

实现 sigmoid 时应避免直接计算极端 \(e^{-x}\)。常见做法包括：

- 对 logit 截断；
- 使用稳定的 `logsigmoid`；
- 用查表近似 sigmoid；
- 对概率损失使用 `softplus` 表达。

原始 C 代码构造 `expTable` 加速 sigmoid，并对超出区间的分数采用边界处理。

## 12. 训练完成后导出什么

最终词表示通常取

\[
W_{\mathrm{in}}.
\]

hierarchical-softmax 的 \(U\) 对应树内部节点，没有一行一词的直接对齐。导出后常对每个词向量做 \(L_2\) 归一化，以便快速计算余弦近邻和类比。

## 13. 可复现性记录

至少应保存：

- 语料版本、清洗与分词规则；
- 词表大小与截断方式；
- \(D\)、最大窗口 \(C\)、epoch 数；
- CBOW 或 Skip-gram；
- hierarchical softmax 的树构造与分支编码；
- 初始学习率和衰减；
- 随机种子；
- 线程数和并行更新方式；
- 类比评价时的 OOV 处理与排除规则。

这些因素会改变最终准确率，论文中的历史硬件时间无法直接作为现代复现的速度基线。
