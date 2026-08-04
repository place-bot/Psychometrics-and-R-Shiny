# CBOW：从上下文预测中心词

## 1. 任务定义

给定词序列

\[
w_1,w_2,\ldots,w_T,
\]

CBOW 在位置 \(t\) 收集中心词两侧的上下文：

\[
\mathcal C_t
=\{w_{t-c},\ldots,w_{t-1},w_{t+1},\ldots,w_{t+c}\}.
\]

训练任务是根据 \(\mathcal C_t\) 预测 \(w_t\)：

\[
P(w_t\mid\mathcal C_t).
\]

原文报告其最佳设置使用 4 个历史词和 4 个未来词，即最多 8 个上下文词。

## 2. Continuous Bag-of-Words 的含义

“Bag-of-Words”表示聚合时忽略上下文顺序；“Continuous”表示被聚合的是学习得到的连续向量。

设实际有效上下文词数为 \(m_t\)，输入嵌入为 \(\mathbf v_w\in\mathbb R^D\)。投影表示可写为平均：

\[
\mathbf h_t
=\frac{1}{m_t}
\sum_{w\in\mathcal C_t}\mathbf v_w.
\]

论文图中标记为 `SUM`，正文说明向量被平均。二者只差一个与上下文长度有关的缩放；公开实现使用平均。

## 3. 预测概率

配合 hierarchical softmax：

\[
P(w_t\mid\mathcal C_t)
=P(w_t\mid\mathbf h_t)
=\prod_{j=1}^{L_{w_t}}
p_j^{y_j}(1-p_j)^{1-y_j},
\]

其中

\[
p_j
=\sigma(\mathbf u_{n_j}^\top\mathbf h_t).
\]

整个语料的最大似然目标可写为

\[
\max_\Theta
\sum_{t=1}^{T}
\log P(w_t\mid\mathcal C_t),
\]

其中 \(\Theta\) 包含输入词向量和 Huffman 内部节点向量。

论文没有用这一形式完整列出目标；它由模型描述和 hierarchical softmax 直接展开。

## 4. 单样本损失

对位置 \(t\)：

\[
\mathcal L_t
=-\sum_{j=1}^{L_{w_t}}
\left[
y_j\log p_j+(1-y_j)\log(1-p_j)
\right].
\]

对投影表示的梯度为

\[
\mathbf g_h
=\frac{\partial\mathcal L_t}{\partial\mathbf h_t}
=\sum_{j=1}^{L_{w_t}}
(p_j-y_j)\mathbf u_{n_j}.
\]

由于 \(\mathbf h_t\) 是上下文向量的平均，每个上下文词收到

\[
\frac{\partial\mathcal L_t}{\partial\mathbf v_w}
=\frac{1}{m_t}\mathbf g_h,
\qquad w\in\mathcal C_t.
\]

同一个样本中的上下文词因此共享同一方向的误差信号。

## 5. 逐步数值例子

设上下文只有两个词，其二维向量为

\[
\mathbf v_a=(0.2,0.6)^\top,
\qquad
\mathbf v_b=(0.4,0.2)^\top.
\]

CBOW 投影为

\[
\mathbf h
=\frac{\mathbf v_a+\mathbf v_b}{2}
=(0.3,0.4)^\top.
\]

目标词的 Huffman 路径经过两个节点：

\[
\mathbf u_1=(1,-0.5)^\top,
\qquad y_1=1,
\]

\[
\mathbf u_2=(-0.2,0.8)^\top,
\qquad y_2=0.
\]

两个 logit 为

\[
z_1=\mathbf u_1^\top\mathbf h=0.1,
\qquad
z_2=\mathbf u_2^\top\mathbf h=0.26.
\]

对应概率近似为

\[
p_1=\sigma(0.1)\approx0.5250,
\qquad
p_2=\sigma(0.26)\approx0.5646.
\]

目标路径概率为

\[
P(w\mid\mathcal C)
=p_1(1-p_2)
\approx0.2286.
\]

损失为

\[
\mathcal L
=-\log(0.2286)
\approx1.476.
\]

投影梯度为

\[
\begin{aligned}
\mathbf g_h
&=(p_1-1)\mathbf u_1+(p_2-0)\mathbf u_2\\
&\approx(-0.588,0.689)^{\top}.
\end{aligned}
\]

两个上下文词各自收到一半：

\[
\frac{\partial\mathcal L}{\partial\mathbf v_a}
=\frac{\partial\mathcal L}{\partial\mathbf v_b}
\approx(-0.294,0.345)^{\top}.
\]

梯度下降会把两个上下文向量都朝降低目标路径损失的方向移动。

## 6. 为什么速度快

论文给出的复杂度是

\[
Q_{\mathrm{CBOW}}
=ND+D\log_2V.
\]

- \(ND\)：读取并聚合上下文向量；
- \(D\log_2V\)：计算并更新 Huffman 路径。

模型没有投影到非线性隐藏层的 \(NDH\) 计算。

## 7. CBOW 学到什么

一个训练样本要求上下文组合能够区分中心词。频繁出现的局部搭配会反复更新：

- 上下文词的输入向量；
- 目标词 Huffman 路径的内部节点向量。

由于多个上下文词被平均，CBOW 倾向于形成平滑、稳定的上下文表示。论文 Table 3 中，CBOW 的句法准确率为 64%，高于 Skip-gram 的 59%；其语义准确率为 24%，低于 Skip-gram 的 55%。这是一组特定语料、维度和训练设置下的结果。

## 8. 顺序信息的损失

若两个上下文包含相同词袋，则

\[
\operatorname{CBOW}(a,b,c)
=\operatorname{CBOW}(c,b,a).
\]

模型无法区分上下文词的排列，也无法为不同位置设置独立变换。它仍可通过词的共现分布学习句法相关规律，但没有显式顺序编码。

## 9. 边界位置与重复词

句首、句尾处有效上下文少于 \(2c\)，应按实际词数 \(m_t\) 求平均。若同一个词在窗口内出现两次，它在求和中贡献两次，并接收两份梯度贡献。

## 10. CBOW 的完整数据流

```text
上下文词索引
   │ 查 W_in
   ▼
多个 D 维向量
   │ 求平均
   ▼
h_t
   │ 沿目标词 Huffman 路径
   ▼
若干 sigmoid 与路径损失
   │ 反向传播
   ├── 更新路径内部节点向量
   └── 把聚合梯度均分给上下文输入向量
```

部署时通常只保留训练后的输入词向量；CBOW 的中心词预测器主要是生成表示的训练工具。
