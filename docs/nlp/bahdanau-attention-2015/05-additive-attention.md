# Additive Attention：从对齐分数到动态上下文

Bahdanau attention 在生成第 \(i\) 个目标词以前，依据当前翻译进度为每个源位置 \(j\) 计算相关性，再把全部源端注释汇总为当前上下文：

\[
(\mathbf s_{i-1},\mathbf h_j)
\longrightarrow e_{ij}
\longrightarrow \alpha_{ij}
\longrightarrow \mathbf c_i.
\]

## 1. 每个下标表示什么

| 符号 | 含义 |
|---|---|
| \(i\) | 当前准备生成的目标位置 |
| \(j\) | 被考察的源位置 |
| \(T_x\) | 源句长度 |
| \(\mathbf s_{i-1}\in\mathbb R^n\) | 生成当前词之前的解码器状态 |
| \(\mathbf h_j\in\mathbb R^{2n}\) | 第 \(j\) 个源位置的双向注释 |
| \(e_{ij}\in\mathbb R\) | 目标位置 \(i\) 与源位置 \(j\) 的未归一化匹配分数 |
| \(\alpha_{ij}\in(0,1)\) | 在第 \(i\) 步分配给源位置 \(j\) 的注意力权重 |
| \(\mathbf c_i\in\mathbb R^{2n}\) | 第 \(i\) 步使用的源端上下文 |

同一个 \(\mathbf h_j\) 会参与多个目标步骤；同一个目标步骤也会比较全部源位置。

## 2. 对齐网络

论文将对齐模型写成

\[
e_{ij}=a(\mathbf s_{i-1},\mathbf h_j).
\]

附录给出的具体形式是单隐藏层前馈网络：

\[
e_{ij}
=
\mathbf v_a^\top
\tanh\!\left(
\mathbf W_a\mathbf s_{i-1}
+
\mathbf U_a\mathbf h_j
\right).
\]

令对齐隐藏层维度为 \(n'\)，则

\[
\begin{aligned}
\mathbf W_a&\in\mathbb R^{n'\times n},&
\mathbf U_a&\in\mathbb R^{n'\times 2n},&
\mathbf v_a&\in\mathbb R^{n'},\\
\mathbf W_a\mathbf s_{i-1}
+\mathbf U_a\mathbf h_j&\in\mathbb R^{n'},&
e_{ij}&\in\mathbb R.
\end{aligned}
\]

论文采用 \(n=n'=1000\)。双向注释维度为 2000，所以 \(\mathbf U_a\) 将 2000 维源注释投影到 1000 维对齐空间。

### 为什么称为 additive attention

状态投影与注释投影先相加，再经过 \(\tanh\) 和向量 \(\mathbf v_a\) 打分。后来的 dot-product attention 直接计算查询与键的内积；两者采用不同的兼容函数。

## 3. 在源位置上做 softmax

\[
\alpha_{ij}
=
\frac{\exp(e_{ij})}
{\sum_{k=1}^{T_x}\exp(e_{ik})}.
\]

于是

\[
\alpha_{ij}>0,
\qquad
\sum_{j=1}^{T_x}\alpha_{ij}=1.
\]

softmax 的归一化范围是当前句子的源位置 \(j\)，不能跨目标步或跨 batch 中的句子归一化。

### Padding mask

令 \(m_j=1\) 表示真实 token，\(m_j=0\) 表示 padding。稳定实现先将 padding logit 设为 \(-\infty\)：

\[
\widetilde e_{ij}
=
\begin{cases}
e_{ij},&m_j=1,\\
-\infty,&m_j=0,
\end{cases}
\qquad
\boldsymbol\alpha_i
=
\operatorname{softmax}(\widetilde{\mathbf e}_i).
\]

这样 padding 权重严格为 0。

## 4. 动态上下文

\[
\mathbf c_i
=
\sum_{j=1}^{T_x}
\alpha_{ij}\mathbf h_j
=
\mathbb E_{J\sim\boldsymbol\alpha_i}[\mathbf h_J].
\]

\(\mathbf c_i\) 是注意力分布下的期望注释。模型没有离散地挑出唯一源词，而是保留连续的软分布，因此整个计算图可微。

## 5. 一次目标步骤的矩阵形式

把源注释按列排列：

\[
\mathbf H=[\mathbf h_1,\ldots,\mathbf h_{T_x}]
\in\mathbb R^{2n\times T_x}.
\]

源端投影可以在解码开始前一次算好：

\[
\mathbf K_a=\mathbf U_a\mathbf H
\in\mathbb R^{n'\times T_x}.
\]

第 \(i\) 步计算

\[
\begin{aligned}
\mathbf q_i&=\mathbf W_a\mathbf s_{i-1}\in\mathbb R^{n'},\\
\mathbf E_i&=\mathbf v_a^\top\tanh(
\mathbf q_i\mathbf 1^\top+\mathbf K_a)
\in\mathbb R^{1\times T_x},\\
\boldsymbol\alpha_i&=\operatorname{softmax}(\mathbf E_i)
\in\mathbb R^{T_x},\\
\mathbf c_i&=\mathbf H\boldsymbol\alpha_i
\in\mathbb R^{2n}.
\end{aligned}
\]

同一个目标步骤内，全部源位置的打分可以并行完成。目标步骤之间仍受解码器递归关系约束。

## 6. 对齐如何从翻译目标中学出

训练数据只有源句与目标句，没有逐词对齐标签。模型最小化

\[
\mathcal L
=
-\sum_{i=1}^{T_y}
\log p(y_i\mid y_{<i},\mathbf x).
\]

翻译误差的梯度穿过上下文、softmax、对齐网络与双向编码器，更新

\[
\mathbf W_a,\quad \mathbf U_a,\quad \mathbf v_a
\]

以及其余翻译参数。对齐是翻译任务内部形成的潜在结构。

## 7. Soft attention 与 hard attention

当前论文对全部源位置求加权和，计算确定且可直接反向传播。若采样离散位置

\[
J_i\sim\operatorname{Categorical}(\boldsymbol\alpha_i),
\qquad
\mathbf c_i=\mathbf h_{J_i},
\]

采样会切断普通路径导数，通常需要策略梯度或其他估计方法。软注意力让训练保持端到端。

## 8. 计算量

每个目标位置都要与全部源位置计算兼容分数，核心打分约为

\[
O(T_xT_y n').
\]

预计算 \(\mathbf U_a\mathbf H\) 可以避免重复源端投影，但仍需处理全部目标—源位置组合。

## 9. 理解边界

- 权重来自翻译监督，未接受人工词对齐监督；短语、功能词和重排序可能产生分散权重。
- \(\mathbf h_j\) 已包含左右语境，所以读取的是上下文化注释。
- 动态读取缩短了信息路径；编码器容量、词表、搜索误差与递归计算仍会限制模型。

## 本页小结

\[
\boxed{
e_{ij}=a(\mathbf s_{i-1},\mathbf h_j),\quad
\alpha_{ij}=\operatorname{softmax}_j(e_{ij}),\quad
\mathbf c_i=\sum_j\alpha_{ij}\mathbf h_j
}
\]

兼容函数、源位置 softmax 与加权和共同构成随目标位置变化的动态检索。
