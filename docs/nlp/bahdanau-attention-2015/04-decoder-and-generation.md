# 逐步解码与条件生成

## 1. 解码器每一步完成什么

目标位置 \(i\) 的解码流程包含：

1. 根据前一状态 \(\mathbf s_{i-1}\) 查询源端注释；
2. 得到权重 \(\alpha_{ij}\) 和上下文 \(\mathbf c_i\)；
3. 结合前一目标词 \(y_{i-1}\) 更新解码状态；
4. 计算词表分布；
5. 训练时读取真实 \(y_i\)，推理时选择一个生成词。

## 2. 目标端条件概率

论文把第 \(i\) 个词的概率写成：

\[
p(y_i\mid y_1,\ldots,y_{i-1},\mathbf x)
=
g(y_{i-1},\mathbf s_i,\mathbf c_i).
\tag{1}
\]

解码状态为：

\[
\mathbf s_i
=
f
(\mathbf s_{i-1},y_{i-1},\mathbf c_i).
\tag{2}
\]

这里 \(\mathbf c_i\) 在每一步变化。

## 3. 解码顺序

注意力打分使用 \(\mathbf s_{i-1}\)：

\[
e_{ij}
=
a(\mathbf s_{i-1},\mathbf h_j).
\tag{3}
\]

因此一个清晰的时间顺序是：

```text
s(i-1)
   │
   ├── 与全部 hj 打分
   ▼
αi1, ..., αiTx
   │
   ▼
ci
   │
   ├── 与 y(i-1)、s(i-1) 一起更新
   ▼
si
   │
   ▼
p(yi | y<i, x)
```

## 4. 目标词嵌入

目标词 \(y_{i-1}\) 用 one-hot 表示时：

\[
\mathbf e(y_{i-1})
=
\mathbf E_y y_{i-1}.
\tag{4}
\]

论文实验的目标词嵌入维度为：

\[
m=620.
\]

源端和目标端是不同语言，使用不同词表与嵌入矩阵。

## 5. 上下文进入三个门控通道

论文附录中的解码 gated unit 为：

\[
\widetilde{\mathbf s}_i
=
\tanh
\left(
W\mathbf e(y_{i-1})
+
U[\mathbf r_i\odot\mathbf s_{i-1}]
+
C\mathbf c_i
\right),
\tag{5}
\]

\[
\mathbf z_i
=
\sigma
\left(
W_z\mathbf e(y_{i-1})
+
U_z\mathbf s_{i-1}
+
C_z\mathbf c_i
\right),
\tag{6}
\]

\[
\mathbf r_i
=
\sigma
\left(
W_r\mathbf e(y_{i-1})
+
U_r\mathbf s_{i-1}
+
C_r\mathbf c_i
\right),
\tag{7}
\]

\[
\mathbf s_i
=
(1-\mathbf z_i)\odot\mathbf s_{i-1}
+
\mathbf z_i\odot\widetilde{\mathbf s}_i.
\tag{8}
\]

上下文分别通过 \(C\)、\(C_z\)、\(C_r\) 影响：

- 候选状态内容；
- 更新多少状态；
- 重置多少历史。

## 6. 形状检查

论文实验使用：

\[
\mathbf e(y_{i-1})\in\mathbb R^{620},
\quad
\mathbf s_{i-1}\in\mathbb R^{1000},
\quad
\mathbf c_i\in\mathbb R^{2000}.
\]

所以：

| 参数 | 形状 |
|---|---|
| \(W,W_z,W_r\) | \(1000\times620\) |
| \(U,U_z,U_r\) | \(1000\times1000\) |
| \(C,C_z,C_r\) | \(1000\times2000\) |
| \(\mathbf z_i,\mathbf r_i,\widetilde{\mathbf s}_i,\mathbf s_i\) | \(1000\) |

每一项相加前都映射到 1000 维。

## 7. 初始解码状态

附录把初始状态定义为：

\[
\mathbf s_0
=
\tanh
\left(
W_s\overleftarrow{\mathbf h}_1
\right).
\tag{9}
\]

反向编码器从句末读向句首，所以 \(\overleftarrow{\mathbf h}_1\) 已经看过整句。它为解码器提供初始全局概览。

之后每一步再通过注意力取得位置相关信息。

## 8. 结束符

目标序列包含结束符 `<eos>`。生成过程在模型输出该符号时停止。

训练目标包括预测结束符：

\[
p(y_{T_y}=\texttt{<eos>}
\mid
y_{<T_y},\mathbf x).
\]

结束符使不同长度的目标句都能用同一个自回归模型表示。

## 9. 训练阶段

训练时第 \(i\) 步通常读取真实前词：

\[
\mathbf e(y_{i-1}^{\text{gold}}).
\]

当前词损失为：

\[
\ell_i
=
-\log
p_\theta
\left(
y_i^{\text{gold}}
\mid
y_{<i}^{\text{gold}},
\mathbf x
\right).
\tag{10}
\]

全句损失为各有效位置之和。

## 10. 推理阶段

推理时模型从起始符开始：

\[
y_0=\texttt{<bos>}.
\]

随后递归：

\[
\widehat y_i
\sim
p_\theta
(y_i\mid\widehat y_{<i},\mathbf x)
\]

或用 beam search 保留多个高概率前缀。

预测词会影响下一步：

- 目标词嵌入；
- 解码状态；
- 注意力查询；
- 后续上下文；
- 后续词分布。

一个早期错误可能沿整个剩余序列传播。

## 11. 输出层并非单层 softmax

论文使用 deep output：

\[
\widetilde{\mathbf t}_i
=
U_o\mathbf s_{\text{read}}
+
V_o\mathbf e(y_{i-1})
+
C_o\mathbf c_i,
\tag{11}
\]

再把相邻单元两两做 maxout：

\[
t_{i,j}
=
\max
\left(
\widetilde t_{i,2j-1},
\widetilde t_{i,2j}
\right).
\tag{12}
\]

最后：

\[
p(y_i=k\mid\cdot)
=
\frac{
\exp(\mathbf w_k^\top\mathbf t_i)
}{
\sum_{k'=1}^{K_y}
\exp(\mathbf w_{k'}^\top\mathbf t_i)
}.
\tag{13}
\]

论文附录和实现采用特定时间索引，输出读取状态在公式中写作 \(\mathbf s_{i-1}\)。现代讲解常用更新后的 \(\mathbf s_i\)。两种记号的关键是输入、状态、上下文与监督目标必须整体错位一致。

## 12. 词表规模

目标词表保留 30,000 个高频词，其他词映射为 `[UNK]`。

因此式 (13) 的 softmax 规模约为：

\[
K_y\approx30{,}000.
\]

论文没有使用 subword 分词。稀有词问题在全测试集 BLEU 中非常明显。

## 13. 一步解码的依赖图

\[
\mathbf s_{i-1}
\longrightarrow
\alpha_i
\longrightarrow
\mathbf c_i
\longrightarrow
\mathbf s_i
\longrightarrow
p(y_i).
\]

同时：

\[
y_{i-1}
\longrightarrow
\mathbf s_i
\quad\text{和}\quad
p(y_i).
\]

这说明注意力处在递归动力学内部：

- \(\mathbf s_{i-1}\) 决定当前读取；
- 当前读取影响 \(\mathbf s_i\)；
- \(\mathbf s_i\) 决定下一次读取。

## 14. 覆盖信息来自哪里

模型没有显式 coverage 向量记录哪些源词已经翻译。历史信息主要隐含在：

\[
\mathbf s_{i-1}.
\]

如果解码状态能够总结过去的输出和过去读取的上下文，对齐网络可以据此移动关注位置。

这种隐式覆盖可能造成：

- 重复翻译；
- 漏译；
- 过早结束；
- 注意力反复停在同一位置。

后续 NMT 工作专门引入 coverage 机制缓解这些问题。

## 15. 逐步生成的核心

RNNsearch 的解码器可以概括为：

\[
\boxed{
\text{前缀状态}
\rightarrow
\text{读取源句}
\rightarrow
\text{更新状态}
\rightarrow
\text{预测目标词}
}
\]

下一章进入读取源句的核心：additive attention 的打分、归一化、上下文与形状。
