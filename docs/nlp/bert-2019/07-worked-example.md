# 完整手算：MLM 与 NSP

## 1. 原始句对

\[
[\text{CLS}],\ \text{my},\ \text{dog},\ \text{is},\
\text{cute},\ [\text{SEP}],\
\text{he},\ \text{likes},\ \text{playing},\ [\text{SEP}].
\]

WordPiece 可能把 playing 拆为 `play`、`##ing`。

## 2. 三种 embedding

以 `dog` 位置 \(i=2\) 为例：

\[
e_2=e_{\text{dog}}^{token}
+e_A^{segment}
+e_2^{position}.
\]

第二片段的 `he` 使用 \(e_B^{segment}\)，位置仍按整条序列连续编号。

## 3. MLM

假设 `dog` 被选中并走 80% 分支，输入变成 `[MASK]`，标签仍为 dog。顶层 mask 表示产生三个简化 logits：

\[
o=(1.2,\;2.0,\;-0.5)
\]

分别对应 cat、dog、book。

\[
\operatorname{softmax}(o)
\approx(0.294,\;0.654,\;0.052).
\]

MLM 损失：

\[
L_{\text{MLM}}=-\log0.654\approx0.425.
\]

未被选中的普通位置不进入 MLM loss。

## 4. NSP

若第二片段确为真实后续，标签 `IsNext`。设 logits：

\[
u=(1.5,\;0.2)
\]

对应 IsNext、NotNext：

\[
p(\text{IsNext})\approx0.786.
\]

\[
L_{\text{NSP}}=-\log0.786\approx0.241.
\]

总损失：

\[
L\approx0.425+0.241=0.666.
\]

## 5. 梯度传播

MLM 梯度从被选位置传播到全部能通过 self-attention 影响它的 token；NSP 梯度从 `[CLS]` 传播到整句表示。二者共同更新 embedding 与 12/24 层 encoder。

## 6. Fine-tuning

做情感分类时不再遮蔽 token，不再计算 MLM/NSP。加入分类层并用标注交叉熵更新：

\[
L_{\text{task}}
=
-\log p(y^\star\mid\mathbf C).
\]

这清楚区分预训练目标与下游目标。
