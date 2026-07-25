# 符号表

## 数据与维度

| 符号 | 含义 |
| --- | --- |
| \(I\) | 学生/受试者数 |
| \(J\) | 项目数 |
| \(K\) | 测验总属性数 |
| \(L=2^K\) | 无结构限制时的完整属性模式数 |
| \(X_{ij}\) | 学生 \(i\) 对项目 \(j\) 的二元反应 |
| \(\boldsymbol X_i\) | 学生 \(i\) 的反应向量 |

## Q 矩阵与属性

| 符号 | 含义 |
| --- | --- |
| \(Q\) | \(J\times K\) 项目-属性矩阵 |
| \(q_{jk}\) | 项目 \(j\) 是否需要属性 \(k\) |
| \(K_j^*=\sum_k q_{jk}\) | 项目 \(j\) 所需属性数 |
| \(\boldsymbol\alpha_l\) | 第 \(l\) 个完整属性模式 |
| \(\boldsymbol\alpha^*_{lj}\) | 项目 \(j\) 对模式 \(l\) 的约化属性模式 |
| \(\boldsymbol a\preceq\boldsymbol b\) | \(\boldsymbol a\) 的每一分量均不大于 \(\boldsymbol b\) |
| \(\boldsymbol a\prec\boldsymbol b\) | 上述偏序成立且至少一处分量严格小于 |

## 成功概率与 link

| 符号 | 含义 |
| --- | --- |
| \(P(\boldsymbol\alpha^*_{lj})\) | 约化模式下回答项目 \(j\) 正确的概率 |
| \(\boldsymbol P_j\) | 项目 \(j\) 全部约化组成功概率向量 |
| \(h(P)\) | identity、logit 或 log link |
| \(\boldsymbol\delta_j\) | identity-link G-DINA 效应 |
| \(\boldsymbol\lambda_j\) | logit-link 效应 |
| \(\boldsymbol\nu_j\) | log-link 效应 |
| \(g_j,s_j\) | DINA 的 guessing 与 slipping 参数 |

## design 与约束

| 符号 | 含义 |
| --- | --- |
| \(A_j\) | 项目 \(j\) 全部约化属性组合矩阵 |
| \(M_j^{(S)}\) | 饱和 design matrix |
| \(M_j^{(r)}\) | 约化模型 \(r\) 的 design matrix |
| \(M_j^{(r-)}\) | 去掉截距列的约化 design matrix |
| \(R_{jr}\) | 项目 \(j\)、模型 \(r\) 的限制矩阵 |
| \(p\) 或 \(P\) | 约化模型自由参数数；需依上下文辨别 |

## EM 与后验计数

| 符号 | 含义 |
| --- | --- |
| \(p(\boldsymbol\alpha_l)\) | 完整属性模式先验概率 |
| \(\tau_{il}\) | 学生 \(i\) 属于完整模式 \(l\) 的后验概率 |
| \(\tau_{ij}(\boldsymbol a)\) | 学生 \(i\) 属于项目 \(j\) 约化组 \(\boldsymbol a\) 的后验概率 |
| \(I_{\boldsymbol a j}\) | 约化组 \(\boldsymbol a\) 的期望人数 |
| \(R_{\boldsymbol a j}\) | 约化组 \(\boldsymbol a\) 的期望答对人数 |
| \(W_j\) | 以 \(I_{\boldsymbol a j}\) 为对角元的权重矩阵 |

## 推断

| 符号 | 含义 |
| --- | --- |
| \(\mathcal I(\widehat{\boldsymbol P}_j)\) | 项目概率的观测信息矩阵 |
| \(\operatorname{Var}(\widehat{\boldsymbol P}_j)\) | 项目概率协方差矩阵 |
| \(G_j\) | 参数变换的 Jacobian |
| \(W\) | Wald 统计量；与权重矩阵 \(W_j\) 不同 |
| \(2^{K_j^*}-p\) | Wald 检验自由度 |

## 代码对象映射

| 论文对象 | `GDINA` R package | 本站 Python |
| --- | --- | --- |
| 完整属性模式 | `attributepattern()` | `attribute_patterns()` |
| 约化组映射 | `LC2LG()` / `reduced.LG` | `item_group_maps()` |
| \(M_j\) | `designmatrix()` | `design_matrix()` |
| \(R_{\boldsymbol a j}\) | `Rg` | `expected_correct` |
| \(I_{\boldsymbol a j}\) | `Ng` | `expected_total` |
| \(\boldsymbol P_j\) | `catprob.parm` | `probabilities` |
| Wald | `modelcomp()` | `wald_acdm()` |
