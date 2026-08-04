# 负迁移与重加权手算

## 1. 负迁移

若使用源知识后的目标性能低于不迁移：

\[
R_T(f_{\text{transfer}})
>
R_T(f_{\text{target-only}}),
\]

就发生 negative transfer。源/目标关系太弱、标签含义不同或分布偏差都可能导致它。

## 2. Covariate shift 下的重加权

若

\[
P_S(Y\mid X)=P_T(Y\mid X),
\qquad
P_S(X)\ne P_T(X),
\]

目标风险可写成

\[
\begin{aligned}
R_T(f)
&=\mathbb E_{(X,Y)\sim P_T}[\ell(f(X),Y)]\\
&=\mathbb E_{(X,Y)\sim P_S}
\left[
\frac{P_T(X)}{P_S(X)}
\ell(f(X),Y)
\right].
\end{aligned}
\]

权重

\[
w(x)=P_T(x)/P_S(x)
\]

让更像目标域的源样本贡献更大。

## 3. 数字例子

源域两类输入频率：

\[
P_S(a)=0.8,\quad P_S(b)=0.2.
\]

目标域：

\[
P_T(a)=0.2,\quad P_T(b)=0.8.
\]

权重：

\[
w(a)=0.25,\qquad w(b)=4.
\]

普通源训练会被 \(a\) 主导；重加权后 \(b\) 样本贡献放大，更接近目标分布。

## 4. 对预训练模型的启示

- 通用语料规模大不保证与教育、医疗等目标域匹配；
- 领域继续预训练可缩小 \(P(X)\) 差异；
- 下游验证集用于判断 transfer 是否有效；
- 不能只比较源任务 loss；
- 数据和标签定义改变时要检查负迁移。

## 5. Survey 的边界

该文是分类与方法综述，没有提出 BERT 式算法，也没有覆盖 foundation model、prompting 或 PEFT。它提供的是概念坐标系。
