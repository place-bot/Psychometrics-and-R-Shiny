# 正弦与余弦位置编码

self-attention 对输入行的排列具有等变性。若没有位置信息，模型无法仅凭 attention 区分词序。

## 1. 原论文公式

\[
PE_{(pos,2i)}
=
\sin\!\left(
\frac{pos}{10000^{2i/d_{\text{model}}}}
\right),
\]

\[
PE_{(pos,2i+1)}
=
\cos\!\left(
\frac{pos}{10000^{2i/d_{\text{model}}}}
\right).
\]

偶数维用正弦，奇数维用余弦。波长按几何级数从 \(2\pi\) 扩展到约 \(10000\cdot2\pi\)。

## 2. 怎样进入模型

\[
\mathbf x_{pos}
=
\sqrt{d_{\text{model}}}\,\mathbf e_{token}
+\mathbf{PE}_{pos}.
\]

位置编码与 embedding 同为 512 维，直接相加。论文还对相加结果做 dropout。

## 3. 为什么正弦能表达相对位移

利用

\[
\sin(a+b)=\sin a\cos b+\cos a\sin b,
\]

\[
\cos(a+b)=\cos a\cos b-\sin a\sin b,
\]

对固定偏移 \(k\)，频率对

\[
[\sin(\omega(pos+k)),\cos(\omega(pos+k))]
\]

可以由位置 \(pos\) 的正余弦对通过一个依赖 \(k\) 的线性旋转得到。这为学习相对位置关系提供便利。

## 4. 固定与可学习位置

论文消融中，学习位置 embedding 的开发集 BLEU 25.7，正弦版本 25.8，表现近似。作者选择正弦版本，理由是它可能外推到训练时未见的更长序列。

外推能力并非自动保证：模型其余部分、训练长度、数值频率和任务分布都会影响实际表现。

## 5. 后续位置方法

RoPE、relative position bias、ALiBi 等属于后续发展。它们不能写成 2017 原始 Transformer 的组成部分。
