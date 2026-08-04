# Discriminative LR、STLR 与 Gradual Unfreezing

## 1. Discriminative fine-tuning

为每层使用不同学习率：

\[
\theta_t^\ell
=
\theta_{t-1}^\ell
-
\eta^\ell\nabla_{\theta^\ell}J.
\]

先找顶层学习率，再令

\[
\eta^{\ell-1}=\eta^\ell/2.6.
\]

底层通用语言特征改动较小，顶层任务特征改动较大。

## 2. Slanted triangular learning rate

\[
cut=\lfloor T\cdot cut_{\text{frac}}\rfloor.
\]

\[
p=
\begin{cases}
t/cut,&t<cut,\\
1-\dfrac{t-cut}{cut(1/cut_{\text{frac}}-1)},&t\ge cut.
\end{cases}
\]

\[
\eta_t
=
\eta_{\max}
\frac{1+p(ratio-1)}{ratio}.
\]

论文常用

\[
cut_{\text{frac}}=0.1,\quad ratio=32.
\]

学习率短期快速上升，再长时间线性下降：先快速适应，再细化。

## 3. 数字例子

设 \(\eta_{\max}=0.01,ratio=32\)。起点：

\[
\eta_0=0.01/32=0.0003125.
\]

到 cut：

\[
\eta_{cut}=0.01.
\]

末尾回到约 0.0003125。

## 4. Gradual unfreezing

分类器训练先只解冻最后一层；下一轮再解冻倒数第二层，逐轮向底层扩展，最后微调整体。它减少底层通用特征在早期被随机分类头大梯度破坏的风险。

## 5. 三者配合

- gradual unfreezing 控制“何时更新哪层”；
- discriminative LR 控制“各层更新多快”；
- STLR 控制“训练过程中学习率怎样变化”。

它们解决不同维度的问题。
