# 实验裁剪：805 道题与两个互斥类别

## 1. 二分类数据

定义

\[
y_j=
\begin{cases}
0,&\text{题 }j\text{ 属于 Operations of integers},\\
1,&\text{题 }j\text{ 属于 Mathematical thinking}.
\end{cases}
\]

对应的两列 \(Q\) 行只有

\[
(1,0)
\quad\text{或}\quad
(0,1).
\]

预测 \(y_j\) 后就能恢复这两个可能 Q 行之一。

## 2. 类别比例

\[
\Pr(O)=\frac{666}{805}=0.8273,
\]

\[
\Pr(M)=\frac{139}{805}=0.1727.
\]

多数类约为少数类的

\[
\frac{666}{139}=4.79
\]

倍。

## 3. one-hot 假设带来的简化

一般 Q 行有

\[
2^K
\]

种二元模式；去掉全零行后仍有

\[
2^K-1
\]

种合法组合。

one-hot 约束把候选数压到 \(K\)：

\[
\{\boldsymbol e_1,\ldots,\boldsymbol e_K\}.
\]

进一步保留两个属性后，候选只剩两种。

## 4. 这一简化排除了什么

实验没有遇到下列情况：

- 一题同时需要整数运算与数学推理；
- 属性之间存在先修或层级关系；
- 题目只靠文本无法区分多种解法；
- 同一题的多个合理 Q 行；
- 某属性存在而专家没有标记。

## 5. 从二分类推广到 multi-label

若每题可对应多个属性，可为每列建立一个概率：

\[
\widehat{\boldsymbol p}_j
=
\left(
p_{j1},\ldots,p_{jK}
\right),
\qquad
p_{jk}
=
\Pr(q_{jk}=1\mid d_j).
\]

随后选阈值：

\[
\widehat q_{jk}
=
\mathbb I(p_{jk}\ge \tau_k).
\]

此时需要报告：

- micro-F1 与 macro-F1；
- 每个属性的 precision/recall；
- row exact match；
- Hamming loss；
- Q 矩阵进入 CDM 后的拟合和分类结果。

论文没有进行这一推广。

## 6. 更合适的实际定位

这项方法可以作为**候选 Q 行生成器**：

1. 对新题输出属性概率；
2. 把高置信度题送入快速复核；
3. 把低置信度或多属性冲突题送入完整专家讨论；
4. 收集学生反应后进行 CDM 校准。

这一定位既利用文本自动化，也保留测量证据链。
