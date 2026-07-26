# Q 矩阵验证与学习

Q 矩阵（Q-matrix）定义项目和属性之间的依赖关系，是 CDM 里最容易出问题、也最值得单独成线读的部分。本页把验证（validation）、数据驱动学习（data-driven learning）、贝叶斯估计（Bayesian estimation）、机器学习辅助（machine learning-assisted）和 AI 辅助（AI-assisted）方法分开。

## 阅读目标

- 理解专家给定 Q 矩阵为什么可能错，以及错了以后会影响哪些参数和分类。
- 区分 Q 矩阵验证（Q-matrix validation）和 Q 矩阵学习（Q-matrix learning）。
- 理解从 response data、文本信息和 AI 工具中学习 Q 矩阵的不同统计含义。
- 为 continuous-Q 或 exploratory-Q 研究准备比较对象。

## 经验验证与经典方法

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | de la Torre (2008). An empirically based method of Q-matrix validation for the DINA model: Development and applications. | [完整专题](papers/de-la-torre-2008/index.md) | DINA 下经验 Q 矩阵验证的经典入口。 |
| 精读 | de la Torre & Chiu (2016). A general method of empirical Q-matrix validation. | [完整专题](papers/de-la-torre-chiu-2016/index.md) | 用 GDI/PVAF 把经验验证推广到 G-DINA 家族。 |
| 精读 | Chen, Liu, Xu & Ying (2015). Statistical analysis of Q-matrix based diagnostic classification models. | `cdm/papers/chen-liu-xu-ying-2015-q-matrix-dcm.md` | 同时属于 Q 矩阵、可识别性和正则化估计。必须精读。 |

## 数据驱动与理论学习

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Liu, Xu & Ying (2012). Data-driven learning of Q-matrix. | [完整专题](papers/liu-xu-ying-2012/index.md) | 用 \(T\)-matrix 和联合反应矩从 response data 学习 Q。 |
| 精读 | Liu, Xu & Ying (2013). Theory of self-learning Q-matrix. | [完整专题](papers/liu-xu-ying-2013/index.md) | 给出 C1--C5、列空间分离以及无噪声、已知 \(c,g\)、未知 \(c\) 三层一致性理论。 |
| 主读 | Li, Ma & Xu (2022). Learning large Q-matrix by restricted Boltzmann machines. | `cdm/papers/li-ma-xu-2022-rbm-q-matrix.md` | 大规模 Q 矩阵学习，连接受限玻尔兹曼机（restricted Boltzmann machines, RBM）。 |
| 主读 | Chen, Liu, Culpepper & Chen (2021). Inferring the number of attributes for the exploratory DINA model. | `cdm/papers/chen-liu-culpepper-chen-2021-number-attributes.md` | exploratory DINA 中属性数量（number of attributes）的推断。 |

## 贝叶斯与部分已知 Q 矩阵

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Chen, Culpepper, Chen & Douglas (2018). Bayesian estimation of the DINA Q-matrix. | [完整专题](papers/chen-culpepper-chen-douglas-2018/index.md) | 受限 MH 与 Gibbs 在可识别 Q 空间中进行探索性贝叶斯估计。 |
| 主读 | Liu, Andersson & Skrondal (2020). A constrained Metropolis-Hastings Robbins-Monro algorithm for Q matrix estimation in DINA models. | `cdm/papers/liu-andersson-skrondal-2020-mhrm-q.md` | 带识别约束的 MCMC/Robbins-Monro Q 矩阵估计。 |
| 主读 | Oka & Okada (2023). Scalable Bayesian approach for the DINA Q-matrix estimation combining stochastic optimization and variational inference. | `cdm/papers/oka-okada-2023-scalable-bayesian-q.md` | 大规模 Bayesian Q estimation，重点读 stochastic optimization 和 variational inference。 |
| 主读 | Yamaguchi (2025). Bayesian diagnostic classification models for a partially known Q-matrix. | `cdm/papers/yamaguchi-2025-partially-known-q.md` | 介于 confirmatory 和 exploratory 之间的 partially known Q-matrix。 |

## 文本、机器学习和 AI 辅助

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Zhao & Huang (2019). Automated Q-matrix identification using text classification techniques. | `cdm/papers/zhao-huang-2019-text-classification-q.md` | 用文本分类（text classification）辅助 Q 矩阵识别。 |
| 主读 | Qin & Guo (2024). Using machine learning to improve Q-matrix validation. | `cdm/papers/qin-guo-2024-ml-q-validation.md` | 机器学习用于 Q 矩阵验证。 |
| 主读 | Fan, Bialo & Li (2026). The use of AI tools to develop and validate Q-matrices. | `cdm/papers/fan-bialo-li-2026-ai-q-matrices.md` | AI 工具辅助 Q 矩阵开发与验证。当前先作为新近方向，后续需要补完整版本信息。 |

## 和可识别性直接相连的 Q 矩阵论文

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Gu & Xu (2021). The sufficient and necessary condition for the identifiability of the Q-matrix. | `cdm/papers/gu-xu-2021-q-matrix-identifiability.md` | Q 矩阵可识别性的必要充分条件，和 Q-matrix validation 必须一起读。 |

## 推荐顺序

1. de la Torre (2008)
2. de la Torre & Chiu (2016)
3. Liu, Xu & Ying (2012, 2013)
4. Chen, Liu, Xu & Ying (2015)
5. Chen, Culpepper, Chen & Douglas (2018)
6. Gu & Xu (2021)
7. 大规模、Bayesian、ML 和 AI 方向
