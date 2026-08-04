# GRU、状态初始化与 Deep Output

论文附录给出了 RNNsearch 的门控状态更新与输出层。这里沿着 \(\mathbf c_i\) 进入解码器的路径逐式解释。

## 1. 解码器状态

\[
\mathbf s_i
=
(1-\mathbf z_i)\odot\mathbf s_{i-1}
+
\mathbf z_i\odot\widetilde{\mathbf s}_i.
\]

\[
\begin{aligned}
\mathbf z_i
&=\sigma(
\mathbf W_z\mathbf E_y[y_{i-1}]
+\mathbf U_z\mathbf s_{i-1}
+\mathbf C_z\mathbf c_i),\\
\mathbf r_i
&=\sigma(
\mathbf W_r\mathbf E_y[y_{i-1}]
+\mathbf U_r\mathbf s_{i-1}
+\mathbf C_r\mathbf c_i),\\
\widetilde{\mathbf s}_i
&=\tanh\!\left(
\mathbf W\mathbf E_y[y_{i-1}]
+\mathbf U[\mathbf r_i\odot\mathbf s_{i-1}]
+\mathbf C\mathbf c_i
\right).
\end{aligned}
\]

| 输入 | 信息 |
|---|---|
| \(\mathbf s_{i-1}\) | 已生成目标前缀的状态 |
| \(\mathbf E_y[y_{i-1}]\) | 前一个目标词 embedding |
| \(\mathbf c_i\) | 当前从源句动态读取的内容 |

update gate 决定旧状态与候选状态的插值，reset gate 决定旧状态有多少进入候选计算。上下文同时影响两个门和候选状态。

## 2. 与现代 GRU API 的差异

论文、框架之间可能交换 update gate 的插值方向，改变 reset gate 在线性变换前后的次序，或将上下文与输入拼接。复现时要核对完整方程与张量形状，单看 “GRU” 名称不足以保证逐项一致。

## 3. 双向编码器

源端两个方向也采用门控单元：

\[
\mathbf h_j
=
\begin{bmatrix}
\overrightarrow{\mathbf h}_j\\
\overleftarrow{\mathbf h}_j
\end{bmatrix}.
\]

正向状态读取左侧历史，反向状态读取右侧历史，拼接后每个源位置都拥有全句语境。

## 4. 解码器初始化

\[
\mathbf s_0
=
\tanh(
\mathbf W_s\overleftarrow{\mathbf h}_1).
\]

\(\overleftarrow{\mathbf h}_1\) 已从句尾递归到句首，用作全局起点；后续每一步再通过 attention 获取动态上下文。

## 5. Deep output 与 maxout

输出层先融合三个来源：

\[
\widetilde{\mathbf t}_i
=
\mathbf U_o\mathbf s_i
+
\mathbf V_o\mathbf E_y[y_{i-1}]
+
\mathbf C_o\mathbf c_i.
\]

随后相邻两维做 maxout：

\[
t_{i,k}
=
\max(
\widetilde t_{i,2k-1},
\widetilde t_{i,2k}).
\]

最终

\[
\mathbf o_i=\mathbf W_o\mathbf t_i,
\qquad
p(y_i=w\mid\cdots)
=
\frac{\exp(o_{i,w})}
{\sum_{v\in\mathcal V_y}\exp(o_{i,v})}.
\]

上下文既进入 GRU，也通过 \(\mathbf C_o\mathbf c_i\) 直接进入目标词读出，提供一条更短的信息与梯度路径。

## 6. 主要维度

| 量 | 论文配置 |
|---|---:|
| 编码器单方向隐藏维度 \(n\) | 1000 |
| 解码器状态维度 | 1000 |
| 双向注释维度 | 2000 |
| 词 embedding 维度 \(m\) | 620 |
| 对齐隐藏维度 \(n'\) | 1000 |
| maxout 输出维度 \(l\) | 500 |
| 两端词表 | 各 30,000 |

若 maxout 输出为 500 维，则它之前的 \(\widetilde{\mathbf t}_i\) 为 1000 维。

## 7. 状态下标

正文概率式使用当前状态 \(\mathbf s_i\)，附录与 GroundHog 读出代码存在一步下标平移。稳定的数据流是：

1. 旧状态计算当前 attention；
2. attention 得到 \(\mathbf c_i\)；
3. 前一目标词、旧状态和上下文更新状态；
4. 输出当前目标词分布。

实现时采用一套一致下标即可。

## 本页小结

\[
\boxed{
\text{目标前缀状态}
+
\text{前一目标词}
+
\text{当前源上下文}
\longrightarrow
\text{新状态与目标词概率}
}
\]

attention 的上下文同时控制门控更新并直接参与词表预测。
