# 估计、正则化与计算

这一页放估计方法（estimation）、正则化（regularization）、联合最大似然（joint maximum likelihood estimation, joint MLE）、高维属性结构（high-dimensional attribute structures）和计算实现。

## 阅读目标

- 理解 CDM 估计不只是 EM，还包括 regularized likelihood、joint MLE、Bayesian estimation、variational inference 和结构学习。
- 区分把属性 \(A\) 当作随机潜变量和固定未知参数的两种估计哲学。
- 为后续 R Shiny 示例和 `GDINA` 包实践建立方法背景。
- 为 continuous-Q 或 exploratory-Q 的算法设计准备比较对象。

## 正则化与 Q 矩阵估计

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Chen, Liu, Xu & Ying (2015). Statistical analysis of Q-matrix based diagnostic classification models. | `cdm/papers/chen-liu-xu-ying-2015-q-matrix-dcm.md` | regularized maximum likelihood 和 Q 矩阵结构学习的重要参考。 |
| 精读 | Chen, Li, Liu & Ying (2017). Regularized latent class analysis with application in cognitive diagnosis. | `cdm/papers/chen-li-liu-ying-2017-regularized-lca.md` | 正则化潜在类分析（regularized latent class analysis）与 CDM 应用。 |
| 主读 | Chen, Culpepper & Liang (2020). A sparse latent class model for cognitive diagnosis. | `cdm/papers/chen-culpepper-liang-2020-sparse-latent-class.md` | 稀疏潜在类模型（sparse latent class model, SLCM）和 exploratory CDM。 |

## 高维属性与联合 MLE

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Gu & Xu (2019). Learning attribute patterns in high-dimensional structured latent attribute models. | `cdm/papers/gu-xu-2019-high-dimensional-attribute-patterns.md` | 高维 SLAM 中 significant attribute patterns 的选择一致性。 |
| 精读 | Gu & Xu (2023). A joint MLE approach to large-scale structured latent attribute analysis. | `cdm/papers/gu-xu-2023-joint-mle-slam.md` | 把 latent attributes 当 fixed unknown parameters 的核心文献。 |
| 精读 | Ma & Xu. Learning latent and hierarchical structures in cognitive diagnosis models. | `cdm/papers/ma-xu-latent-hierarchical-structures.md` | 同时学习 latent structure 和 hierarchy，后续需要补完整发表信息。 |

## 软件、贝叶斯与可扩展计算

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Ma & de la Torre (2020). GDINA: An R package for cognitive diagnosis modeling. | `cdm/papers/ma-de-la-torre-2020-gdina-package.md` | R 实现和 Shiny 示例的主要入口。 |
| 主读 | Chen, Culpepper, Chen & Douglas (2018). Bayesian estimation of the DINA Q-matrix. | `cdm/papers/chen-culpepper-chen-douglas-2018-bayesian-q.md` | Bayesian Q-matrix estimation 的比较对象。 |
| 主读 | Liu, Andersson & Skrondal (2020). A constrained Metropolis-Hastings Robbins-Monro algorithm for Q matrix estimation in DINA models. | `cdm/papers/liu-andersson-skrondal-2020-mhrm-q.md` | 约束采样与 Robbins-Monro 更新。 |
| 主读 | Li, Ma & Xu (2022). Learning large Q-matrix by restricted Boltzmann machines. | `cdm/papers/li-ma-xu-2022-rbm-q-matrix.md` | 深度学习式大规模 Q 矩阵估计。 |
| 主读 | Oka & Okada (2023). Scalable Bayesian approach for the DINA Q-matrix estimation combining stochastic optimization and variational inference. | `cdm/papers/oka-okada-2023-scalable-bayesian-q.md` | stochastic optimization 与 variational inference 的可扩展路线。 |
| 主读 | Balamuta & Culpepper (2022). Exploratory restricted latent class models with monotonicity requirements under Pólya-Gamma data augmentation. | `cdm/papers/balamuta-culpepper-2022-exploratory-rlcm-monotonicity.md` | Bayesian computation、monotonicity 和 exploratory latent structure 的交叉。 |

## 推荐顺序

1. Chen, Liu, Xu & Ying (2015)
2. Chen, Li, Liu & Ying (2017)
3. Gu & Xu (2019)
4. Gu & Xu (2023)
5. Ma & Xu 的结构学习论文
6. Ma & de la Torre (2020)
7. Bayesian、RBM、variational 和 Pólya-Gamma 扩展
