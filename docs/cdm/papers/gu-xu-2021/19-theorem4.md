# Theorem 4：D/E 泛识别条件

## 1. 分块形式

经行置换后写成

\[
Q=
\begin{pmatrix}
Q_1\\
Q_2\\
Q^\star
\end{pmatrix},
\]

其中 \(Q_1,Q_2\) 均为 \(K\times K\)。

## 2. Condition D

\(Q_1\) 和 \(Q_2\) 互不重叠，且都泛完整。

每块都能把 \(K\) 个属性匹配到 \(K\) 道不同题。

## 3. Condition E

剩余矩阵 \(Q^\star\) 的每一列至少有一个 1：

\[
\sum_{j\in Q^\star}q_{jk}\ge1,
\qquad k=1,\ldots,K.
\]

D 和 E 合起来自动保证每个属性至少出现三次：

- 在 \(Q_1\) 的匹配中一次；
- 在 \(Q_2\) 的匹配中一次；
- 在 \(Q^\star\) 中至少一次。

## 4. Theorem 4

一般 RLCM 中，若 D 和 E 成立，则

\[
(Q,\Theta,\boldsymbol p)
\]

联合泛可识别。

## 5. 可识别参数子集

Remark 3 把可识别区域写为：

\[
\det T(Q_1,\Theta_{Q_1})\ne0,
\]

\[
\det T(Q_2,\Theta_{Q_2})\ne0,
\]

并且

\[
T(Q^\star,\Theta_{Q^\star})
\operatorname{Diag}(\boldsymbol p)
\]

的列向量两两不同。

这些行列式或列差为 0 的参数集合由多项式方程定义，在完整参数空间中具有零测度。

## 6. 三块信息的作用

```text
Q1：第一套潜类坐标
Q2：第二套独立坐标
Q*：区分并标记潜类列
          │
          ▼
恢复受 Q 约束的 Θ、p 和 Q 的结构
```

两块泛完整矩阵使相应 T 子矩阵在一般参数点上满秩。第三块通过不同列码消除潜类列配对歧义。

## 7. 与已知 Q 结果的差别

相同 D/E 结构也曾用于已知 Q 时的一般 RLCM 参数泛识别。未知 Q 会增加替代结构 \(\bar Q\)，因此 Condition C 重新成为必要条件。

已知 Q 场景中，某属性有时只需两题；本文 Theorem 3 说明未知 Q 时该放松失效。

## 8. 题数要求

D/E 至少需要

\[
J\ge2K+1.
\]

所以一般 RLCM 的泛识别充分设计仍接近三块结构。DINA 的两参数约束才能把严格识别题数进一步降到

\[
K+\lceil\log_2K\rceil+1.
\]
