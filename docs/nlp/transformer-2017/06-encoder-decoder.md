# Encoder、Decoder 与三种 Attention

## 1. Encoder 层

输入

\[
\mathbf X^{(0)}
=
\sqrt{d_{\text{model}}}\,\operatorname{Embed}(\mathbf x)
+\mathbf{PE}.
\]

第 \(\ell\) 层：

\[
\begin{aligned}
\widetilde{\mathbf X}^{(\ell)}
&=
\operatorname{LayerNorm}\!\left(
\mathbf X^{(\ell-1)}
+\operatorname{Dropout}(
\operatorname{MHA}_{\text{self}}(\mathbf X^{(\ell-1)}))
\right),\\
\mathbf X^{(\ell)}
&=
\operatorname{LayerNorm}\!\left(
\widetilde{\mathbf X}^{(\ell)}
+\operatorname{Dropout}(
\operatorname{FFN}(\widetilde{\mathbf X}^{(\ell)}))
\right).
\end{aligned}
\]

encoder self-attention 的 Q、K、V 都来自同一层输入。

## 2. Decoder 层

第 \(\ell\) 层依次执行：

\[
\begin{aligned}
\mathbf U&=\operatorname{AddNorm}(
\mathbf Y,\operatorname{MaskedMHA}(\mathbf Y)),\\
\mathbf V&=\operatorname{AddNorm}(
\mathbf U,\operatorname{CrossMHA}(\mathbf U,\mathbf Z,\mathbf Z)),\\
\mathbf Y'&=\operatorname{AddNorm}(
\mathbf V,\operatorname{FFN}(\mathbf V)).
\end{aligned}
\]

\(\mathbf Z\) 是顶层 encoder 输出。cross-attention 中 query 来自 decoder，key/value 来自 encoder。

## 3. 三种 attention 的职责

- encoder self-attention：构造上下文化源表示；
- masked decoder self-attention：汇总已经可见的目标前缀；
- cross-attention：依据当前目标表示读取源句。

Bahdanau 模型只把 attention 用在第三类连接；Transformer 把第一、第二类序列建模也交给 attention。

## 4. 层与位置的信息流

同一层中所有位置并行，但层之间仍串行：

\[
\mathbf X^{(0)}
\rightarrow\mathbf X^{(1)}
\rightarrow\cdots\rightarrow\mathbf X^{(6)}.
\]

因此“无递归”指没有长度为 \(n\) 的时间步状态链，并不表示所有网络层都能同时计算。

## 5. 自回归输出

顶层 decoder 表示经共享词表权重线性变换与 softmax，得到每个位置的下一个 token 分布。训练可以一次产生全部位置 logits；生成时一次只确定一个新 token。
