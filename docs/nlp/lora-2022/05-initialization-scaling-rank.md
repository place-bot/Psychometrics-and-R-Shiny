# 初始化、缩放与 Rank

## 1. 零初始增量

论文使用：

\[
\mathbf A\sim\mathcal N(0,\sigma^2),
\qquad
\mathbf B=\mathbf 0.
\]

所以开始时

\[
\Delta W=BA=0,
\]

模型输出与预训练基座完全一致。

## 2. 第一步谁先更新

设损失对 \(\Delta W\) 的梯度为 \(G\)。忽略缩放：

\[
\frac{\partial\mathcal L}{\partial B}
=
G A^\top,
\qquad
\frac{\partial\mathcal L}{\partial A}
=
B^\top G.
\]

初始 \(B=0\)，所以第一步 \(A\) 梯度为 0，\(B\) 先获得更新。之后 \(B\neq0\)，两者共同学习。

## 3. 缩放

\[
s=\frac{\alpha}{r},
\qquad
\Delta h=sBAx.
\]

论文把 \(\alpha\) 设为首次尝试的 rank，并不系统调参。缩放帮助 rank 改变时控制更新幅度；\(\alpha\) 与学习率仍有交互。

## 4. Rank 怎样选

原论文 GPT-3 表 6 中，Q/V 同时适配时 \(r=1,2,4,8,64\) 的结果十分接近。WikiSQL 为 73.4、73.3、73.7、73.8、73.5；MultiNLI 为 91.3、91.4、91.3、91.6、91.4。

这说明这些任务下低 rank 足够，没有证明 rank 1 对所有任务都足够。领域差异、数据量、模块数量和任务复杂度都可能改变需求。

## 5. Rank 与模块覆盖

固定预算时：

\[
\text{更多模块}\times\text{较小 rank}
\]

与

\[
\text{较少模块}\times\text{较大 rank}
\]

需要联合选择。原论文结果倾向前者，但现代模型应通过验证集和资源约束决定。

## 6. LoRA dropout

官方库支持在低秩分支输入上使用 dropout。它是实现层正则化选项，不属于核心三号公式的必要组成；训练和部署时行为需遵循 PyTorch train/eval 语义。
