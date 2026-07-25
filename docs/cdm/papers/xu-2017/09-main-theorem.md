# 主定理与测验设计含义

## 定理 1

在论文第 2.1 节的模型设定与限制式 (2.2)--(2.3) 下，若 C1 和 C2 成立，则

\[
(\Theta,\boldsymbol p)
\]

可识别。

完整量词是：

\[
T(Q,\Theta)\boldsymbol p
=
T(Q,\bar\Theta)\bar{\boldsymbol p}
\Longrightarrow
\Theta=\bar\Theta,\quad
\boldsymbol p=\bar{\boldsymbol p}.
\]

结论覆盖所有满足假设的允许参数点，因而是 strict identifiability。

## 定理覆盖什么

在相应参数限制成立时，它为下列模型提供统一识别保证：

- DINA；
- DINO；
- G-DINA；
- linear logistic / logit-CDM；
- reduced RUM / log-CDM；
- 论文限制族中的其他二分诊断模型。

定理直接识别 \(\Theta\) 和 \(\boldsymbol p\)。具体模型的低维参数还要求其参数化到 \(\Theta\) 的映射一对一。

## 设计含义

若可以编制单属性题，论文建议：

1. 至少准备两个完整的单属性题块，保证 C1；
2. 检查剩余题目能否对每个 \(\boldsymbol e_k\) 与 \(\boldsymbol 0\) 提供区分；
3. 若需要完全由 Q 结构保证，可准备三个 \(I_K\) 块。

当现有测试的参数估计异常且 Q 不满足条件时，可以增补题目，使设计进入定理覆盖范围。

## 与 Allman et al. (2009) 的比较

Allman 等对含 \(2^K\) 个潜在类的 Bernoulli mixture 给出 generic identifiability 结果，其中一个数量型充分条件为

\[
J\ge 2K+1.
\]

Xu 的 C1、C2 也蕴含 \(J\ge2K+1\)，但两套理论的结论与条件性质不同：

| 方面 | Allman et al. | Xu |
| --- | --- | --- |
| 模型 | 一般 latent class model | Q-restricted latent class model |
| 结论 | generic，通常允许 label swapping | strict，属性标签固定 |
| 条件 | 分块后的秩/类别数条件 | Q 单位块与概率区分 |
| 技术 | Kruskal 三路张量分解 | 边际 \(T\)-矩阵变换 |

题目数量条件不能代替 Q 结构条件，generic 结果也不能自动覆盖受约束参数空间的全部点。

## 定理能保证的层次

\[
\text{C1+C2}
\Longrightarrow
\text{总体分布中的参数唯一}
\Longrightarrow
\text{在附加正则条件下支持一致估计}.
\]

它不直接给出：

- 某个有限样本所需的 \(N\)；
- 参数估计误差界；
- 属性分类准确率；
- 题目区分度的最低数值阈值；
- Q 错设时的稳健性；
- 最短可用测验长度；
- CAT 下一题选择规则。

## 一个 K = 2 的安全设计

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&0\\
0&1\\
1&0\\
0&1
\end{pmatrix}
=
\begin{pmatrix}
I_2\\I_2\\I_2
\end{pmatrix}.
\]

前四题满足 C1，最后两题由式 (2.3) 分别保证

\[
\theta_{5,(1,0)}>\theta_{5,(0,0)},
\qquad
\theta_{6,(0,1)}>\theta_{6,(0,0)}.
\]

所以 C2 成立，主定理适用。

若只保留前四题，C1 仍成立，C2 没有剩余题可以提供区分；命题 2 说明此类设计确实可能不可识别。
