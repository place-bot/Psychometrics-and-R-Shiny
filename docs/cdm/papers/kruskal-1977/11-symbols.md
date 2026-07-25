# 符号表

## 三路数组与秩

| 符号 | 维度或类型 | 含义 |
| --- | --- | --- |
| \(\mathbb F\) | 数域 | 原文主要为实数；现代证明可覆盖更一般的域 |
| \(I,J,K\) | 正整数 | 三个数组方向的大小 |
| \(\mathcal X=(x_{ijk})\) | \(I\times J\times K\) | 三路数组或三阶张量 |
| \(i,j,k\) | 指标 | 三个方向的位置 |
| \(\boldsymbol a,\boldsymbol b,\boldsymbol c\) | 向量 | 一个 triad 的三个因子 |
| \(\boldsymbol a\otimes\boldsymbol b\otimes\boldsymbol c\) | 三路数组 | 秩一张量，即原文的 triad |
| \(\operatorname{rank}(\mathcal X)\) | 整数 | 表示 \(\mathcal X\) 所需的最少 triad 数 |
| \(X_{i::}\) | \(J\times K\) | 固定第一个指标的 slab |
| \(\dim_\ell(\mathcal X)\) | 整数 | 第 \(\ell\) 方向 slabs 张成空间的维数 |
| \(X_{(\ell)}\) | 矩阵 | 第 \(\ell\) 个模式展开 |

## 三重积分解

| 符号 | 维度 | 含义 |
| --- | ---: | --- |
| \(R\) | 正整数 | 分解中的成分数 |
| \(A\) | \(I\times R\) | 第一个因子矩阵 |
| \(B\) | \(J\times R\) | 第二个因子矩阵 |
| \(C\) | \(K\times R\) | 第三个因子矩阵 |
| \(\boldsymbol a_r\) | \(I\) | \(A\) 的第 \(r\) 列 |
| \(\boldsymbol b_r\) | \(J\) | \(B\) 的第 \(r\) 列 |
| \(\boldsymbol c_r\) | \(K\) | \(C\) 的第 \(r\) 列 |
| \([A,B,C]\) | \(I\times J\times K\) | \(\sum_r\boldsymbol a_r\otimes\boldsymbol b_r\otimes\boldsymbol c_r\) |
| \(\odot\) | 运算 | 按列 Khatri--Rao 积 |

## 唯一性

| 符号 | 含义 |
| --- | --- |
| \(k_A,k_B,k_C\) | 三个因子矩阵的列 Kruskal rank |
| \(P\) | \(R\times R\) 共同置换矩阵 |
| \(\Lambda,M,N\) | 可逆对角缩放矩阵 |
| \(\lambda_r,\mu_r,\nu_r\) | 第 \(r\) 个成分在三个方向上的缩放 |
| \(\lambda_r\mu_r\nu_r=1\) | 缩放相互抵消条件 |
| \(a_i=R-k_{M_i}\) | Rhodes 证明中的 \(k\)-rank 缺陷量 |
| \(\Pi_i\) | 在第 \(i\) 个方向消去指定列空间的投影 |
| \(S_i\) | 固定第三方向坐标得到的矩阵切片 |

## CDM 接口

| 符号 | 含义 |
| --- | --- |
| \(\mathcal A\) | 允许的潜在属性模式集合 |
| \(R=|\mathcal A|\) | 潜在成分或属性模式数 |
| \(\boldsymbol\alpha_r\) | 第 \(r\) 个属性模式 |
| \(\pi_r\) | 第 \(r\) 个属性模式的总体比例 |
| \(\mathcal J_t\) | 第 \(t\) 个项目块，\(t=1,2,3\) |
| \(M_t\) | 第 \(t\) 个块的类条件反应模式概率矩阵 |
| \(\mathcal P\) | 三块反应模式的总体联合概率数组 |
| \(Q\) | 项目—属性关系矩阵；负责把潜在成分连接到认知标签 |

## 记号方向检查

本文专题遵循 CP 文献，把成分放在因子矩阵的列中：

\[
A\in\mathbb F^{I\times R}.
\]

Allman (2009) 的潜在类笔记把类别放在行中：

\[
M\in\mathbb R^{R\times\kappa}.
\]

二者通过转置对应。若后续文章写

\[
\operatorname{rank}_K(M),
\]

需要先查看作者定义的是行 Kruskal rank 还是列 Kruskal rank。
