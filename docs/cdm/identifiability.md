# 可识别性理论

可识别性（identifiability）是 CDM 里必须精读的一条主线。这里按从通用潜在结构到 CDM/RLCM，再到 DINA、Q 矩阵和扩展数据类型的顺序组织。

## 阅读目标

- 明确可识别（identifiable）、泛可识别（generically identifiable）和可估计（estimable）的差异。
- 理解 Kruskal 定理如何进入 latent class model 和 RLCM 证明。
- 理解 Q 矩阵结构、属性分布和项目参数如何共同决定可识别性。
- 为 continuous-Q、general-response 或 exploratory CDM 写作准备术语。

## 通用底座

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Kruskal (1977). Three-way arrays: Rank and uniqueness of trilinear decompositions. | `cdm/papers/kruskal-1977-three-way-arrays.md` | 证明工具，不必读应用外细节，但要掌握唯一性定理的使用方式。 |
| 精读 | Allman, Matias & Rhodes (2009). Identifiability of parameters in latent structure models with many observed variables. | `cdm/papers/allman-matias-rhodes-2009-latent-structure-identifiability.md` | 从观测分布识别 latent class response profiles 的关键理论来源。 |

## RLCM 与 CDM 参数识别

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Xu (2017). Identifiability of restricted latent class models with binary responses. | `cdm/papers/xu-2017-rlcm-binary-identifiability.md` | CDM 作为 RLCM 的核心识别理论。 |
| 精读 | Xu & Shang (2018). Identifying latent structures in restricted latent class models. | `cdm/papers/xu-shang-2018-latent-structures-rlcm.md` | 从给定 restriction 到学习 latent structure 的桥梁。 |
| 精读 | Fang, Liu & Ying (2019). On the identifiability of diagnostic classification models. | `cdm/papers/fang-liu-ying-2019-dcm-identifiability.md` | 更一般 DCM 可识别性口径。 |
| 精读 | Culpepper (2023). A note on weaker conditions for identifying restricted latent class models for binary responses. | `cdm/papers/culpepper-2023-weaker-rlcm-identification.md` | 弱化条件，重点读 dyad-completeness 和 Kruskal 的使用。 |
| 精读 | Balamuta & Culpepper (2022). Exploratory restricted latent class models with monotonicity requirements under Pólya-Gamma data augmentation. | `cdm/papers/balamuta-culpepper-2022-exploratory-rlcm-monotonicity.md` | 同时属于 exploratory RLCM、Bayesian computation 和 identifiability。 |

## DINA 与 Q 矩阵识别

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Gu & Xu. Sufficient and necessary conditions for the identifiability and estimability of the DINA model. | `cdm/papers/gu-xu-dina-identifiability-estimability.md` | DINA 模型必要充分条件的核心写法。后续需要补完整年份和发表信息。 |
| 精读 | Gu & Xu (2021). The sufficient and necessary condition for the identifiability of the Q-matrix. | `cdm/papers/gu-xu-2021-q-matrix-identifiability.md` | Q 矩阵自身识别的核心文献。 |
| 精读 | Chen, Liu, Xu & Ying (2015). Statistical analysis of Q-matrix based diagnostic classification models. | `cdm/papers/chen-liu-xu-ying-2015-q-matrix-dcm.md` | Q 矩阵、估计和可识别性的交叉核心文献。 |
| 精读 | Gu (2022/2023). Generic identifiability of the DINA model and blessing of latent dependence. | `cdm/papers/gu-2023-generic-identifiability-dina.md` | anchor-free/generic 语言的重要参考。年份在文献页中用发表版本核对。 |

## 扩展响应类型

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Lin & Xu (2024). Sufficient and necessary conditions for the identifiability of DINA models with polytomous responses. | `cdm/papers/lin-xu-2024-polytomous-dina-identifiability.md` | 多项反应（polytomous responses）下 DINA 识别。 |
| 主读 | Liu & Culpepper (2024). Restricted latent class models for nominal response data: Identifiability and estimation. | `cdm/papers/liu-culpepper-2024-nominal-rlcm.md` | 名义反应（nominal response data）下的 RLCM 识别和估计，可作为 general-response 的背景。 |

## 推荐顺序

1. Kruskal (1977)
2. Allman, Matias & Rhodes (2009)
3. Xu (2017)
4. Gu & Xu 的 DINA 识别论文
5. Chen, Liu, Xu & Ying (2015)
6. Gu & Xu (2021)
7. Gu (2022/2023)
8. Fang, Liu & Ying (2019)、Xu & Shang (2018)、Culpepper (2023) 和扩展响应类型论文
