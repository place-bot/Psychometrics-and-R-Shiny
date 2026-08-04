# 端到端训练：翻译误差怎样更新对齐

RNNsearch 没有人工对齐标签。编码器、对齐网络、解码器和输出层共同接受翻译损失的梯度。

## 1. 训练目标与 teacher forcing

\[
p(\mathbf y\mid\mathbf x)
=
\prod_{i=1}^{T_y}
p(y_i\mid y_{<i},\mathbf x),
\qquad
\mathcal L
=
-\sum_{i=1}^{T_y}
\log p(y_i\mid y_{<i},\mathbf x).
\]

训练第 \(i\) 步读取真实前一个目标词：

\[
\mathbf s_i=f(\mathbf s_{i-1},y_{i-1},\mathbf c_i).
\]

目标句全部已知，状态递归仍要按顺序执行。推理时模型把自身生成词送回下一步，由此形成训练—推理输入分布差异。

## 2. Batch mask

设 \(m_i^{(b)}\) 表示第 \(b\) 个样本的第 \(i\) 个目标位置有效：

\[
\mathcal L_{\text{batch}}
=
-\frac{
\sum_b\sum_i m_i^{(b)}
\log p(y_i^{(b)}\mid y_{<i}^{(b)},\mathbf x^{(b)})
}{
\sum_b\sum_i m_i^{(b)}
}.
\]

按有效 token 归一化可避免 padding 方式改变损失尺度。

## 3. 从输出层反传

若 \(\mathbf p_i=\operatorname{softmax}(\mathbf o_i)\)，正确词 one-hot 向量为 \(\mathbf y_i\)，则

\[
\frac{\partial\mathcal L_i}{\partial\mathbf o_i}
=
\mathbf p_i-\mathbf y_i.
\]

误差经过 deep output、状态 \(\mathbf s_i\) 与上下文 \(\mathbf c_i\)，继续传到 attention。

## 4. 上下文对注意力分数的梯度

已知

\[
\mathbf c_i=\sum_j\alpha_{ij}\mathbf h_j,
\qquad
\boldsymbol\alpha_i=\operatorname{softmax}(\mathbf e_i),
\]

记

\[
\mathbf g_i=\frac{\partial\mathcal L}{\partial\mathbf c_i}.
\]

softmax Jacobian 为

\[
\frac{\partial \alpha_{ij}}{\partial e_{ik}}
=
\alpha_{ij}
\bigl[\mathbb I(j=k)-\alpha_{ik}\bigr].
\]

整理可得

\[
\boxed{
\frac{\partial\mathcal L}{\partial e_{ik}}
=
\alpha_{ik}\,
\mathbf g_i^\top(\mathbf h_k-\mathbf c_i)
}
\]

其中：

- \(\alpha_{ik}\) 是位置 \(k\) 的当前权重；
- \(\mathbf h_k-\mathbf c_i\) 是该注释相对平均上下文的独特方向；
- \(\mathbf g_i\) 表示怎样移动上下文可以降低损失；
- 内积衡量增加位置 \(k\) 权重是否符合有利方向。

## 5. 源注释的梯度路径

\[
\frac{\partial\mathcal L}{\partial\mathbf h_j}
=
\underbrace{
\sum_i\alpha_{ij}
\frac{\partial\mathcal L}{\partial\mathbf c_i}
}_{\text{加权和的直接路径}}
+
\underbrace{
\sum_i
\frac{\partial\mathcal L}{\partial e_{ij}}
\frac{\partial e_{ij}}{\partial\mathbf h_j}
}_{\text{对齐分数路径}}
+
\text{编码器递归路径}.
\]

一个翻译损失由此能更新输出层、解码器、对齐网络、双向编码器和两端词嵌入。

## 6. 论文的优化设置

- Adadelta，\(\rho=0.95,\epsilon=10^{-6}\)；
- mini-batch 大小 80；
- 全局梯度 \(L_2\) 范数上限 1；
- 每次取 1600 个句对，按长度排序后分为 20 个 batch；
- 训练数据开始时随机打乱一次。

若梯度上限为 \(\tau\)，裁剪写成

\[
\widetilde{\mathbf g}
=
\mathbf g
\min\!\left(1,\frac{\tau}{\|\mathbf g\|_2}\right).
\]

它限制更新幅度，有助于缓解循环网络的梯度爆炸。

## 7. 参数初始化

附录报告：

- 循环连接矩阵采用随机正交矩阵；
- \(\mathbf W_a,\mathbf U_a\) 从标准差 \(0.001\) 的高斯分布采样；
- \(\mathbf v_a\) 与 bias 初始化为 0；
- 其余权重从标准差 \(0.01\) 的高斯分布采样。

## 8. 一次训练迭代

```python
annotations = encoder(source, source_mask)
state = initialize(annotations)
loss = 0.0

for i in range(target_length):
    scores = alignment(state, annotations)
    alpha = masked_softmax(scores, source_mask)
    context = weighted_sum(alpha, annotations)
    state = decoder_gru(target[i - 1], state, context)
    logits = deep_output(state, target[i - 1], context)
    loss += masked_cross_entropy(logits, target[i])

loss.backward()
clip_global_grad_norm_(parameters, 1.0)
adadelta.step()
```

实现会把 batch、词表投影和可预计算项向量化，伪代码保留论文的信息依赖。

## 9. 训练并行化的边界

可以并行：

- batch 中不同句子；
- 同一目标步内全部源位置的 attention score；
- embedding、线性层和 softmax 的矩阵运算；
- 双向编码器的两个方向可分别运行。

必须等待：

\[
\overrightarrow{\mathbf h}_j
\leftarrow
\overrightarrow{\mathbf h}_{j-1},
\qquad
\mathbf s_i
\leftarrow
\mathbf s_{i-1}.
\]

这条关键路径限制了 GPU 同时处理全部位置的能力。后文会单独比较 RNN、Word2Vec 与 Transformer。

## 本页小结

\[
\frac{\partial\mathcal L}{\partial e_{ik}}
=
\alpha_{ik}\,
\mathbf g_i^\top(\mathbf h_k-\mathbf c_i)
\]

说明模型会比较单个源注释与当前平均上下文，并根据它能否改善翻译来调整注意力分数。
