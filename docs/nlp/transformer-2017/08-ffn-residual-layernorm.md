# FFN、残差与 LayerNorm

attention 负责位置之间交换信息，FFN 负责每个位置内部的非线性特征变换。

## 1. Position-wise FFN

\[
\operatorname{FFN}(\mathbf x)
=
\max(0,\mathbf x\mathbf W_1+\mathbf b_1)
\mathbf W_2+\mathbf b_2.
\]

base 模型：

\[
\mathbf W_1\in\mathbb R^{512\times2048},
\qquad
\mathbf W_2\in\mathbb R^{2048\times512}.
\]

同一层的所有位置共享 \(\mathbf W_1,\mathbf W_2\)，不同层参数独立。它也可视作两个 kernel size 1 的卷积。

## 2. 残差连接

\[
\mathbf r=\mathbf x+\operatorname{Dropout}(
\operatorname{Sublayer}(\mathbf x)).
\]

残差提供恒等路径，便于信息和梯度跨层传播。所有子层输入输出保持 \(d_{\text{model}}\) 维，才能相加。

## 3. LayerNorm

对单个 token 的 \(d_{\text{model}}\) 个特征：

\[
\mu=\frac1d\sum_kx_k,\qquad
\sigma^2=\frac1d\sum_k(x_k-\mu)^2,
\]

\[
\operatorname{LN}(\mathbf x)
=
\boldsymbol\gamma\odot
\frac{\mathbf x-\mu}{\sqrt{\sigma^2+\epsilon}}
+\boldsymbol\beta.
\]

它不依赖 batch 中其他样本，适合变长序列。

## 4. 原论文是 Post-LN

\[
\operatorname{LN}(
\mathbf x+\operatorname{Sublayer}(\mathbf x)).
\]

很多现代大模型采用 Pre-LN：

\[
\mathbf x+\operatorname{Sublayer}(
\operatorname{LN}(\mathbf x)).
\]

Pre-LN 往往更易训练很深网络，但属于后续常见修改。解读原论文图 1 和复现 base/big 时应使用 Post-LN。

## 5. 激活函数

原论文 FFN 使用 ReLU。GELU、SwiGLU、GEGLU 等是后续 Transformer 变体，不能回填到 2017 配置。
