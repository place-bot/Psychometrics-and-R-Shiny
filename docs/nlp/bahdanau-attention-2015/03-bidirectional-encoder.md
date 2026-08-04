# 双向编码器与源端注释

## 1. 为什么注意力读取的是注释

注意力在源位置 \(j\) 上分配权重。若每个位置只有孤立词嵌入：

\[
\mathbf E_x x_j,
\]

模型很难仅凭该向量判断词义、短语边界和句法角色。

论文先把每个位置编码成上下文化注释：

\[
\mathbf h_j.
\]

\(\mathbf h_j\) 以 \(x_j\) 为中心，同时包含前文和后文信息。

## 2. 单向 RNN 的方向限制

正向 RNN：

\[
\overrightarrow{\mathbf h}_j
=
\overrightarrow f
\left(
\overrightarrow{\mathbf h}_{j-1},
\mathbf E_x x_j
\right).
\tag{1}
\]

\(\overrightarrow{\mathbf h}_j\) 能访问：

\[
x_1,\ldots,x_j.
\]

它在处理 \(x_j\) 时还没有读取：

\[
x_{j+1},\ldots,x_{T_x}.
\]

机器翻译中的词义和语法角色经常依赖右侧上下文，因此只用正向状态会限制每个位置的注释。

## 3. 反向 RNN

反向 RNN 从句末读向句首：

\[
\overleftarrow{\mathbf h}_j
=
\overleftarrow f
\left(
\overleftarrow{\mathbf h}_{j+1},
\mathbf E_x x_j
\right).
\tag{2}
\]

\(\overleftarrow{\mathbf h}_j\) 能访问：

\[
x_j,\ldots,x_{T_x}.
\]

论文在两个方向共享源词嵌入矩阵 \(\mathbf E_x\)，递归权重分别学习。

## 4. 拼接形成注释

第 \(j\) 个源位置的注释为：

\[
\mathbf h_j
=
\begin{bmatrix}
\overrightarrow{\mathbf h}_j\\
\overleftarrow{\mathbf h}_j
\end{bmatrix}.
\tag{3}
\]

若每个方向有 \(n\) 个隐藏单元：

\[
\overrightarrow{\mathbf h}_j,
\overleftarrow{\mathbf h}_j
\in\mathbb R^n,
\]

则：

\[
\mathbf h_j\in\mathbb R^{2n}.
\]

论文实验取：

\[
n=1000,
\]

所以每个注释维度为：

\[
2n=2000.
\]

## 5. 注释矩阵

把所有注释按源位置排列：

\[
H
=
\begin{bmatrix}
\mathbf h_1^\top\\
\mathbf h_2^\top\\
\vdots\\
\mathbf h_{T_x}^\top
\end{bmatrix}
\in
\mathbb R^{T_x\times 2n}.
\tag{4}
\]

对 batch 训练，加入 batch 维：

\[
H\in
\mathbb R^{B\times T_x\times 2n}.
\]

GroundHog/Theano 使用时间优先布局：

\[
H\in
\mathbb R^{T_x\times B\times 2n}.
\]

形状次序不同，数学内容相同。

## 6. “聚焦在第 \(j\) 个词周围”的含义

理论上，\(\mathbf h_j\) 可以包含整句信息：

- 正向状态总结 \(x_{\le j}\)；
- 反向状态总结 \(x_{\ge j}\)。

论文指出，RNN 往往更强地表示最近输入，所以 \(\mathbf h_j\) 会突出 \(x_j\) 周围区域。

这是一种归纳偏置，不要求注释只含局部窗口。实际信息范围由：

- 门控状态；
- 训练数据；
- 隐藏维度；
- 梯度传播；
- 句子长度；
- 翻译目标

共同决定。

## 7. 编码器使用 gated hidden unit

论文使用 Cho 等人提出的 gated hidden unit，即后来通常称为 GRU 的结构。

为简化记号，令源词嵌入：

\[
\mathbf e_j=\mathbf E_x x_j.
\]

以正向编码器为例。

### 7.1 更新门

\[
\overrightarrow{\mathbf z}_j
=
\sigma
\left(
\overrightarrow W_z\mathbf e_j
+
\overrightarrow U_z
\overrightarrow{\mathbf h}_{j-1}
\right).
\tag{5}
\]

### 7.2 重置门

\[
\overrightarrow{\mathbf r}_j
=
\sigma
\left(
\overrightarrow W_r\mathbf e_j
+
\overrightarrow U_r
\overrightarrow{\mathbf h}_{j-1}
\right).
\tag{6}
\]

### 7.3 候选状态

\[
\widetilde{\overrightarrow{\mathbf h}}_j
=
\tanh
\left(
\overrightarrow W\mathbf e_j
+
\overrightarrow U
\left[
\overrightarrow{\mathbf r}_j
\odot
\overrightarrow{\mathbf h}_{j-1}
\right]
\right).
\tag{7}
\]

### 7.4 新状态

\[
\overrightarrow{\mathbf h}_j
=
(1-\overrightarrow{\mathbf z}_j)
\odot
\overrightarrow{\mathbf h}_{j-1}
+
\overrightarrow{\mathbf z}_j
\odot
\widetilde{\overrightarrow{\mathbf h}}_j.
\tag{8}
\]

反向编码器使用独立参数，以相反顺序应用同样公式。

## 8. 更新门的记号提醒

式 (8) 中：

- \(z\) 接近 0：更多保留旧状态；
- \(z\) 接近 1：更多采用候选状态。

不同库可能把更新门的两项写成：

\[
z\odot h_{\text{old}}
+
(1-z)\odot\widetilde h.
\]

这只是门的定义方向不同。复现论文时应以论文和对应代码的约定为准。

## 9. 重置门的位置

论文候选状态使用：

\[
U(r\odot h_{\text{old}}).
\]

某些现代库的 GRU 实现把重置门放在隐藏线性变换之后：

\[
r\odot(Uh_{\text{old}}).
\]

一般情况下：

\[
U(r\odot h)
\neq
r\odot(Uh).
\]

因此，直接替换成框架自带 `GRUCell` 可以保持总体架构，却未必逐项匹配论文单元。

## 10. 初始状态与句界

正向状态通常从零开始：

\[
\overrightarrow{\mathbf h}_0=\mathbf 0.
\]

反向状态从句末边界开始：

\[
\overleftarrow{\mathbf h}_{T_x+1}=\mathbf 0.
\]

实现会在序列中加入结束符，并使用 mask 区分真实 token 与 padding。

## 11. Mask 怎样进入双向编码

一个 batch 中句长不同。设：

\[
m_{bj}
\in
\{0,1\}
\]

表示 batch 中第 \(b\) 个句子的第 \(j\) 个位置是否有效。

常用 masked update：

\[
\mathbf h_{bj}
\leftarrow
m_{bj}\mathbf h_{bj}^{\text{new}}
+
(1-m_{bj})\mathbf h_{b,j-1}.
\]

注意力阶段还要用同一个源端 mask，避免给 padding 位置分配概率。

## 12. 为什么拼接

拼接保留两个方向的独立坐标：

\[
[\overrightarrow h_j;\overleftarrow h_j].
\]

求和要求两套状态维度相同，并在进入注意力之前强制混合。拼接允许对齐网络的 \(U_a\) 自行学习怎样组合两种方向。

代价是注释维度从 \(n\) 变成 \(2n\)。

## 13. 与基础 RNNencdec 的编码差别

作者公开配置清楚地区分两者。

### RNNencdec

```text
last_forward = True
forward      = False
backward     = False
search       = False
```

基础模型复制正向编码器最后状态，作为所有目标位置的固定上下文。

### RNNsearch

```text
last_forward = False
forward      = True
backward     = True
search       = True
```

新模型保留每个位置的正向与反向状态，并启用动态搜索。

## 14. 编码器输出的三个层次

| 对象 | 形状 | 信息 |
|---|---|---|
| 源词嵌入 \(\mathbf e_j\) | \(m\) | 当前词类型 |
| 单向状态 \(\overrightarrow{\mathbf h}_j\) | \(n\) | 左侧到当前位置 |
| 单向状态 \(\overleftarrow{\mathbf h}_j\) | \(n\) | 右侧到当前位置 |
| 双向注释 \(\mathbf h_j\) | \(2n\) | 以当前位置为中心的双向语境 |
| 注释序列 \(H\) | \(T_x\times2n\) | 可被注意力读取的源端记忆 |

## 15. 从编码器到注意力

编码器只负责产生 \(H\)。它没有提前决定每个目标词对齐到哪里。

到目标位置 \(i\) 时，对齐网络读取：

\[
\mathbf s_{i-1}
\quad\text{和}\quad
\mathbf h_1,\ldots,\mathbf h_{T_x},
\]

再计算当前步骤的分布。源端注释一次编码、多次读取。

这正是后续 encoder memory 与 decoder cross-attention 的早期形式。
