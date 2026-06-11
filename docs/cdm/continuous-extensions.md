# 连续化与扩展模型

这一页整理连续化（continuous generalization）和更灵活的 CDM 扩展。这里要特别区分三件事：连续属性掌握（continuous attribute mastery）、连续反应数据（continuous response data）和广义反应类型（general response types）。

## 阅读目标

- 理解传统 CDM 的二元掌握（binary mastery）如何扩展为部分掌握（partial mastery）。
- 区分连续化学生属性 \(A\) 和连续化项目需求 \(Q\)。
- 理解连续反应、混合型潜变量和 general-response CDM 的适用场景。
- 为后续 continuous-Q 研究找到合适定位：别人连续化什么，我们连续化什么。

## 部分掌握与连续属性

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Shang, Erosheva & Xu (2021). Partial-mastery cognitive diagnosis models. | `cdm/papers/shang-erosheva-xu-2021-partial-mastery.md` | partial mastery 主线。重点读连续属性如何替代 binary mastery。 |
| 主读 | Shu et al. (2023). An explicit form with continuous attribute profile of the partial mastery model. | `cdm/papers/shu-et-al-2023-cap-dina.md` | CAP-DINA 或 continuous attribute profile 方向，后续核对完整作者。 |
| 主读 | Cárdenas-Hurtado, Chen & Moustaki (2025). A generalized additive partial-mastery cognitive diagnosis model. | `cdm/papers/cardenas-hurtado-chen-moustaki-2025-gapm-cdm.md` | generalized additive PM-CDM，用非参数单调函数放松 item response function。 |
| 背景 | A partial mastery, higher-order latent structural model for polytomous attributes (2020). | `cdm/papers/partial-mastery-higher-order-lsm-2020.md` | 高阶潜在结构（higher-order latent structure）和多级属性（polytomous attributes）背景。 |

## 概率输入、连续反应与混合型潜变量

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Zhan, Wang, Jiao & Bian (2018). Probabilistic-input, noisy conjunctive models for cognitive diagnosis. | `cdm/papers/zhan-wang-jiao-bian-2018-pinc.md` | probabilistic input 与 noisy conjunctive 模型，是 continuous/flexible CDM 的重要接口。 |
| 主读 | Hong, Wang, Lim & Douglas (2015). Efficient models for cognitive diagnosis with continuous and mixed-type latent variables. | `cdm/papers/hong-wang-lim-douglas-2015-continuous-mixed-latent.md` | 连续和混合型潜变量（continuous and mixed-type latent variables）。 |
| 主读 | Minchen, de la Torre & Liu (2017). A cognitive diagnosis model for continuous response. | `cdm/papers/minchen-de-la-torre-liu-2017-continuous-response.md` | 连续反应数据（continuous response data）的 CDM。 |
| 背景 | Stout (2007). Skills diagnosis using IRT-based continuous latent trait models. | `cdm/papers/stout-2007-skills-diagnosis-continuous-trait.md` | 用 IRT 连续潜在特质做 skills diagnosis 的背景。 |

## 广义反应与更一般数据类型

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Lee & Gu (2024). New paradigm of identifiable general-response cognitive diagnostic models: Beyond categorical data. | `cdm/papers/lee-gu-2024-general-response-cdm.md` | general-response CDM 的核心新近文献，适合和 continuous response、nominal response 对照。 |
| 主读 | Liu & Culpepper (2024). Restricted latent class models for nominal response data: Identifiability and estimation. | `cdm/papers/liu-culpepper-2024-nominal-rlcm.md` | nominal response data 下 RLCM 的识别和估计。 |
| 主读 | Lin & Xu (2024). Sufficient and necessary conditions for the identifiability of DINA models with polytomous responses. | `cdm/papers/lin-xu-2024-polytomous-dina-identifiability.md` | 多项反应 DINA 的识别条件。 |

## 推荐顺序

1. Shang, Erosheva & Xu (2021)
2. Zhan, Wang, Jiao & Bian (2018)
3. Hong, Wang, Lim & Douglas (2015)
4. Minchen, de la Torre & Liu (2017)
5. Lee & Gu (2024)
6. Cárdenas-Hurtado, Chen & Moustaki (2025)
