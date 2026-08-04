# 注意力解释、复杂度与并行化

这一页集中回答一个常见但容易说得含混的问题：

> 基于注意力的 RNN 能在生成译文时读取整句上下文，为什么它的序列特性仍然不利于训练并行化？

## 1. 先校准一句话

限制并行化的关键来自 **RNN 的递归状态依赖**。文本具有顺序并不会自动导致串行计算；Transformer 同样处理序列，却能在训练时同时计算很多位置。

对于生成 “Ik hou van lama's” 的例子，attention 可以记录每个荷兰语目标词主要从哪些源词读取信息。它改善了源端表示与动态上下文，却保留了编码器和解码器的循环依赖。

## 2. 编码器为什么要按位置等待

正向 RNN：

\[
\overrightarrow{\mathbf h}_j
=
f(\mathbf x_j,\overrightarrow{\mathbf h}_{j-1}).
\]

计算 \(\overrightarrow{\mathbf h}_5\) 前必须得到 \(\overrightarrow{\mathbf h}_4\)，而 \(\overrightarrow{\mathbf h}_4\) 又等待 \(\overrightarrow{\mathbf h}_3\)：

\[
\overrightarrow{\mathbf h}_1
\rightarrow
\overrightarrow{\mathbf h}_2
\rightarrow\cdots\rightarrow
\overrightarrow{\mathbf h}_{T_x}.
\]

反向 RNN 从另一端形成一条同样的链：

\[
\overleftarrow{\mathbf h}_{T_x}
\rightarrow\cdots\rightarrow
\overleftarrow{\mathbf h}_1.
\]

两个方向可以彼此同时运行；每个方向内部的位置仍需依次推进。编码器关键路径约有 \(T_x\) 个递归步骤。

## 3. 解码器为什么也要等待

Bahdanau 解码器第 \(i\) 步先用旧状态计算 attention：

\[
e_{ij}=a(\mathbf s_{i-1},\mathbf h_j),
\qquad
\mathbf c_i=\sum_j\alpha_{ij}\mathbf h_j,
\]

再更新

\[
\mathbf s_i
=
f(\mathbf s_{i-1},y_{i-1},\mathbf c_i).
\]

第 \(i+1\) 步的 query 需要 \(\mathbf s_i\)，所以目标位置形成

\[
\mathbf s_0
\rightarrow
\mathbf c_1,\mathbf s_1
\rightarrow
\mathbf c_2,\mathbf s_2
\rightarrow\cdots.
\]

即使 teacher forcing 已经一次给出全部真实目标词，全部 \(\mathbf s_i\) 仍不能同时算出。目标词已知没有消除状态依赖。

## 4. Attention 中哪些部分可以并行

固定一个目标步 \(i\) 后，

\[
e_{i1},e_{i2},\ldots,e_{iT_x}
\]

可以作为矩阵运算同时计算；softmax、加权和、batch 中不同句子、线性层内部也都能并行。

因此模型处于“局部高度并行、时间步全局串行”的状态。GPU 可以加速每一步的大矩阵乘法，却要等前一步状态完成后再启动下一时间步。

## 5. 与 Word2Vec 的差异

Word2Vec 把语料转换成大量中心词—上下文词训练样本。给定抽样结果后，不同词对的损失大体独立：

\[
\mathcal L
=
\sum_{(w,c)\in\mathcal D}\mathcal L(w,c).
\]

多个词对可组成大 batch，并行查 embedding、计算内积和更新。它没有“第 8 个词对必须等待第 7 个词对的隐藏状态”这条依赖链。

Word2Vec 通过局部共现学习静态词向量，无法为同一个词在不同句子、不同位置生成上下文化表示。RNNsearch 获得了逐句、逐位置的动态表示，代价之一就是递归关键路径。

## 6. 与 Transformer 的差异

Transformer 训练时把所有位置堆成矩阵，统一计算

\[
\mathbf Q=\mathbf X\mathbf W_Q,\qquad
\mathbf K=\mathbf X\mathbf W_K,\qquad
\mathbf V=\mathbf X\mathbf W_V,
\]

\[
\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)
=
\operatorname{softmax}\!\left(
\frac{\mathbf Q\mathbf K^\top}{\sqrt{d_k}}
\right)\mathbf V.
\]

目标端训练使用 causal mask 阻止位置读取未来 token，但 mask 只是把相应分数设为 \(-\infty\)。全部目标位置的矩阵仍可在同一次前向计算中得到。

### 训练与生成必须分开

Transformer 的训练可以跨位置并行。自回归生成时，第 \(i+1\) 个 token 仍要等待第 \(i\) 个 token 被选出：

\[
\widehat y_1
\rightarrow
\widehat y_2
\rightarrow\cdots.
\]

KV cache 减少重复计算，没有消除输出 token 之间的因果等待。

## 7. 四种计算的对比

| 模型/阶段 | 同一句的位置能否并行 | 顺序依赖来自哪里 |
|---|---|---|
| Word2Vec 词对训练 | 大量词对可并行 | 抽样与共享参数更新，无逐位置隐藏状态链 |
| Bahdanau RNN 编码器 | 单方向内部串行 | \(\mathbf h_j\) 依赖 \(\mathbf h_{j-1}\) |
| Bahdanau RNN 解码器训练 | 目标步串行 | \(\mathbf s_i,\mathbf c_i\) 依赖 \(\mathbf s_{i-1}\) |
| Transformer 训练 | 各位置矩阵化并行 | causal mask 限制可见性，不形成递归状态链 |
| 自回归推理 | RNN 与 Transformer 都逐 token | 下一个输入 token 尚未生成 |

## 8. 为什么 GPU 尤其在意关键路径

GPU 擅长一次处理大的规则矩阵。RNN 把整句工作拆成 \(T\) 次依次启动的较小计算：

\[
\text{总延迟}
\approx
\sum_{t=1}^{T}
\text{第 }t\text{ 步延迟}.
\]

时间步之间需要同步，长序列会增加 kernel 启动、内存访问和不可重叠等待。Transformer 把位置维度合入矩阵，使单层的关键路径与序列长度无关，代价是 self-attention 的分数矩阵需要 \(O(T^2)\) 计算和内存。

## 9. Bahdanau attention 的复杂度

| 部分 | 主要规模 |
|---|---|
| 双向 RNN 编码 | \(O(T_x)\) 个串行递归步 |
| RNN 解码 | \(O(T_y)\) 个串行递归步 |
| 全部 cross-attention score | \(O(T_xT_y n')\) |
| attention 权重存储 | \(O(T_xT_y)\) |

预计算 \(\mathbf U_a\mathbf h_j\) 会减少常数项；递归关键路径仍约为 \(T_x+T_y\)。

## 10. 注意力权重的解释范围

\(\alpha_{ij}\) 是上下文加权和中的真实系数，适合观察模型每一步的读取模式。它不是完整因果贡献证明，因为：

- \(\mathbf h_j\) 已混合左右语境；
- 信息也通过解码器旧状态流动；
- 改变权重可能把输入送到训练分布之外；
- 参数之间存在非线性交互。

稳健分析可结合 attention heatmap、梯度、输入扰动、遮蔽实验、人工对齐和翻译评价。

## 11. 最准确的结论

“这种序列特性不利于并行化”可以更精确地表述为：

> Bahdanau 模型使用递归状态表示序列。每个 RNN 位置依赖前一位置，训练时无法同时计算同一序列的全部隐藏状态；单个时间步内的源位置 attention、batch 与矩阵运算仍然可以并行。

这个区分也是从 RNN attention 走向 Transformer 的核心线索。
