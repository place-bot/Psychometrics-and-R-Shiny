# T-matrix 与识别等价式

## 1. T-matrix 的维度

补充材料定义

\[
T(Q,\Theta)\in\mathbb R^{2^J\times2^K}.
\]

- 行由 \(\boldsymbol r\in\{0,1\}^{J}\) 索引；
- 列由 \(\boldsymbol\alpha\in\{0,1\}^{K}\) 索引。

## 2. 元素含义

\[
T_{\boldsymbol r,\boldsymbol\alpha}(Q,\Theta)
=
\Pr(\boldsymbol R\succeq\boldsymbol r
\mid Q,\Theta,\boldsymbol\alpha)
=
\prod_{j=1}^{J}
\theta_{j,\boldsymbol\alpha}^{r_j}.
\]

这里 \(\boldsymbol R\succeq\boldsymbol r\) 表示所有满足 \(r_j=1\) 的题都出现正反应；\(r_j=0\) 的题不加限制。

例如

\[
\boldsymbol r=(1,0,1,0)^\top
\]

对应

\[
T_{\boldsymbol r,\boldsymbol\alpha}
=
\theta_{1,\boldsymbol\alpha}
\theta_{3,\boldsymbol\alpha}.
\]

## 3. 混合潜类

右乘潜类比例得到总体可观测矩：

\[
\left[T(Q,\Theta)\boldsymbol p\right]_{\boldsymbol r}
=
\sum_{\boldsymbol\alpha}
T_{\boldsymbol r,\boldsymbol\alpha}
p_{\boldsymbol\alpha}
=
\Pr(\boldsymbol R\succeq\boldsymbol r).
\]

全部联合正反应矩与完整反应分布可经 Möbius 反演互相恢复，因此使用 \(T\boldsymbol p\) 不损失识别信息。

## 4. Lemma 1

识别等价于：

\[
T(Q,\Theta)\boldsymbol p
=
T(\bar Q,\bar\Theta)\bar{\boldsymbol p}
\]

必然推出

\[
(Q,\Theta,\boldsymbol p)
\sim
(\bar Q,\bar\Theta,\bar{\boldsymbol p}).
\]

证明中还会对 \(T\) 做可逆线性变换。对任意

\[
\boldsymbol\theta^\star=(\theta_1^\star,\ldots,\theta_J^\star)^\top,
\]

存在可逆矩阵 \(D(\boldsymbol\theta^\star)\)，使变换后的行相当于把每题概率从 \(\theta_{j,\alpha}\) 平移为

\[
\theta_{j,\alpha}-\theta_j^\star.
\]

选择恰当的 \(\boldsymbol\theta^\star\) 可以让某些潜类列或题目行归零，从而隔离目标参数。

## 5. T-matrix 在证明中的角色

```text
相同完整反应分布
        │
        ▼
T(Q,Θ)p = T(Q̄,Θ̄)p̄
        │
        ├── 选取特定行：隔离题目组合
        ├── 可逆平移：制造零元素
        ├── 比较列结构：恢复 Γ 与 Q
        └── 消元：恢复题目参数和 p
```

## 6. 与 Liu、Xu & Ying 的 T-matrix

本站前两篇 Q 学习论文也使用 T-matrix。区别在于：

- Q 学习算法把经验矩与候选 \(T(Q)\boldsymbol p\) 的距离作为目标；
- 本文把两个总体 \(T\)-映射相等作为识别证明起点；
- 一般 RLCM 的 \(T\) 使用完整 \(\Theta\)，DINA 的 \(T\) 可进一步写成 \(\boldsymbol c,\boldsymbol g\) 和理想反应矩阵 \(\Gamma(Q)\)。
