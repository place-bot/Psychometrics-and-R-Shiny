# Q 矩阵与理想反应

## Equation 1

DINA 的确定性输入层为

\[
\eta_{ij}
=
\prod_{k=1}^{K}
\alpha_{ik}^{q_{jk}}.
\tag{1}
\]

原文使用 \(Z_{ij}\)，本专题同时写作 \(\eta_{ij}\)，以便和后续 CDM 文献统一。

## 每个因子怎样工作

因为 \(q_{jk}\in\{0,1\}\)：

\[
\alpha_{ik}^{q_{jk}}
=
\begin{cases}
1,&q_{jk}=0,\\
\alpha_{ik},&q_{jk}=1.
\end{cases}
\]

不要求属性 \(k\) 时，对乘积贡献 1；要求属性 \(k\) 时，对乘积贡献学生的掌握状态。

因此

\[
\eta_{ij}=1
\]

当且仅当所有满足 \(q_{jk}=1\) 的属性都有 \(\alpha_{ik}=1\)。

## 与点积条件等价

所需属性数量为

\[
\boldsymbol q_j^\mathsf T\boldsymbol q_j
=
\sum_{k=1}^{K}q_{jk}.
\]

学生拥有的所需属性数量为

\[
\boldsymbol\alpha_i^\mathsf T\boldsymbol q_j.
\]

所以

\[
\eta_{ij}=1
\iff
\boldsymbol\alpha_i^\mathsf T\boldsymbol q_j
=
\boldsymbol q_j^\mathsf T\boldsymbol q_j.
\tag{2}
\]

若左侧小于右侧，至少缺少一个所需属性，\(\eta_{ij}=0\)。

## 分数减法例子

题目要求

\[
\boldsymbol q_j=(1,0,1,1,0).
\]

比较四名学生：

| 属性模式 \(\boldsymbol\alpha_i\) | 属性 1 | 属性 3 | 属性 4 | \(\eta_{ij}\) |
| --- | ---: | ---: | ---: | ---: |
| \((1,0,1,1,0)\) | 1 | 1 | 1 | 1 |
| \((1,1,1,0,1)\) | 1 | 1 | 0 | 0 |
| \((0,1,1,1,1)\) | 0 | 1 | 1 | 0 |
| \((1,0,1,1,1)\) | 1 | 1 | 1 | 1 |

与该题无关的属性 2 和 5 不影响理想状态。

## “AND gate” 的含义

式 (1) 是布尔 AND：

\[
\eta_{ij}
=
\alpha_{i,k_1}
\land
\alpha_{i,k_2}
\land\cdots
\land
\alpha_{i,k_m},
\]

其中 \(k_1,\ldots,k_m\) 是题目要求的属性。

任何一个所需属性为 0，乘积就为 0。这对应非补偿性：

\[
\text{一个已掌握属性不能抵消另一个所需属性的缺失}.
\]

## 论文 Figure 1 的信息流

原图可以压缩为：

\[
\boldsymbol\alpha_i,\boldsymbol q_j
\longrightarrow
\eta_{ij}
\longrightarrow
\begin{cases}
g_j,&\eta_{ij}=0,\\
1-s_j,&\eta_{ij}=1
\end{cases}
\longrightarrow
X_{ij}.
\]

前半段是确定性认知门；后半段加入随机噪声。

## Q 矩阵错误会流向哪里

若 Q 行漏掉一种真实解题策略，能够用该策略答对、却没有掌握 Q 中规定属性的学生会被置于

\[
\eta_{ij}=0.
\]

他们的系统性成功会被模型吸收到 \(g_j\)。原文特别说明，guess 在这里是广义概念，也包括 Q 矩阵没有表达的替代策略。

所以较大的 \(g_j\) 可能来自：

- 随机猜测；
- 题目线索；
- 部分知识；
- 替代策略；
- Q 矩阵错误；
- 其他模型失配。

参数名称不能单独确定心理过程。
