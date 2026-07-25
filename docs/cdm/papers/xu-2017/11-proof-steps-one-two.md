# 证明步骤 1--2

## 证明目标与列顺序

假设两组允许参数满足

\[
T(Q,\Theta)\boldsymbol p
=
T(Q,\bar\Theta)\bar{\boldsymbol p}.
\tag{3.5}
\]

将潜在类列按掌握属性数排列：

\[
\boldsymbol 0,\ 
\boldsymbol e_1,\ldots,\boldsymbol e_K,\ 
\boldsymbol e_1+\boldsymbol e_2,\ldots,\ 
\boldsymbol 1.
\]

前 \(2K\) 题由 C1 分成两个 \(I_K\) 块。证明先处理 \(j>2K\) 的剩余题。

## 步骤 1 的结论

证明

\[
\theta_{j,\boldsymbol 0}
=
\bar\theta_{j,\boldsymbol 0},
\qquad j>2K.
\tag{S1}
\]

### 选择平移向量

取

\[
\boldsymbol\theta^*
=
\left(
\bar\theta_{1,\boldsymbol 1},
\ldots,
\bar\theta_{K,\boldsymbol 1},
\theta_{K+1,\boldsymbol 1},
\ldots,
\theta_{2K,\boldsymbol 1},
0,\ldots,0
\right)^\top.
\]

第一块使用带横线参数的最高概率，第二块使用无横线参数的最高概率。

对第一块第 \(k\) 题，只要
\(\boldsymbol\alpha\succeq\boldsymbol e_k\)，就有

\[
\bar\theta_{k,\boldsymbol\alpha}
-\bar\theta_{k,\boldsymbol 1}
=0.
\]

对第二块同理：

\[
\theta_{K+k,\boldsymbol\alpha}
-\theta_{K+k,\boldsymbol 1}
=0.
\]

### 把 2K 个锚定行相乘

取包含前 \(2K\) 题的 \(T\)-矩阵行。任意非零属性模式至少含一个属性 \(k\)，相应的消零因子出现，因此该行只可能在
\(\boldsymbol 0\) 列非零：

\[
T_{\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}
\left(
Q,\Theta-\boldsymbol\theta^*\boldsymbol1^\top
\right)
=
(c_0,0,\ldots,0).
\]

两个技术引理与式 (2.3) 保证

\[
c_0\ne0.
\]

### 加入一条剩余题行

再把第 \(j>2K\) 题加入同一个题目子集：

\[
T_{\boldsymbol e_j+\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}
=
\theta_{j,\boldsymbol0}
T_{\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}.
\]

对带横线参数也有对应式。将两条等式分别乘
\(\boldsymbol p\) 与 \(\bar{\boldsymbol p}\)，再利用变换后等式，两个非零标量的比值给出

\[
\theta_{j,\boldsymbol0}
=
\bar\theta_{j,\boldsymbol0}.
\]

步骤 1 的实质是先构造一个只看见零属性类的“选择行”。

## 步骤 2 的结论

证明

\[
\theta_{j,\boldsymbol e_k}
=
\bar\theta_{j,\boldsymbol e_k},
\qquad
j>2K,\quad k=1,\ldots,K.
\tag{S2}
\]

### 以单属性类 e₁ 为例

把第一块第 1 题和第二块第 1 题的平移基准由最高概率改成零属性概率，其他锚定题仍以最高概率为基准：

\[
\boldsymbol\theta^*
=
\left(
\bar\theta_{1,\boldsymbol0},
\bar\theta_{2,\boldsymbol1},
\ldots,
\bar\theta_{K,\boldsymbol1},
\theta_{K+1,\boldsymbol0},
\theta_{K+2,\boldsymbol1},
\ldots,
\theta_{2K,\boldsymbol1},
0,\ldots,0
\right)^\top.
\]

前 \(2K\) 行的 Hadamard 乘积现在只可能在
\(\boldsymbol e_1\) 列非零：

\[
T_{\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}
\left(
Q,\Theta-\boldsymbol\theta^*\boldsymbol1^\top
\right)
=
(0,c_1,0,\ldots,0),
\]

其中 \(c_1\ne0\)。

非零性需要排除跨参数相等，例如

\[
\theta_{k,\boldsymbol e_1}
=
\bar\theta_{k,\boldsymbol1},
\]

这由引理 1、引理 2 与模型严格次序共同完成。

### 再次用行比值

加入第 \(j>2K\) 题后：

\[
T_{\boldsymbol e_j+\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}
=
\theta_{j,\boldsymbol e_1}
T_{\sum_{\ell=1}^{2K}\boldsymbol e_\ell,\cdot}.
\]

在两套参数之间比较得到

\[
\theta_{j,\boldsymbol e_1}
=
\bar\theta_{j,\boldsymbol e_1}.
\]

对每个 \(h=2,\ldots,K\) 将第 \(h\) 对锚定题改用零属性基准，重复同一构造，就得到全部
\(\boldsymbol e_h\) 列。

## 前两步建立了什么

步骤 1--2 已经识别 \(Q'\) 题目中的

\[
\left\{
\theta_{j,\boldsymbol0},
\theta_{j,\boldsymbol e_1},
\ldots,
\theta_{j,\boldsymbol e_K}
\right\},
\qquad j>2K.
\]

这些剩余题上的已知对比随后通过 C2 反过来识别前两个单位块及
\(p_{\boldsymbol0},p_{\boldsymbol e_k}\)。
