# 理论背景：潜在结构与混合模型

这一页放在 CDM 分区最前面。原因是 CDM 的很多问题本质上不是先从 DINA 公式开始，而是从潜在结构模型（latent structure models）、有限混合模型（finite mixture models）和可识别性（identifiability）开始。

## 阅读目标

- 理解从观测反应分布 \(P(Y)\) 到潜在类反应轮廓（latent class response profiles）的识别逻辑。
- 理解有限混合模型何时可识别，哪些条件只是充分条件，哪些条件接近必要条件。
- 学会区分模型参数可识别（parameter identifiability）、潜在结构可识别（latent structure identifiability）和标签置换（label switching）。
- 为后面读受限潜在类模型（restricted latent class models, RLCM）和 Q 矩阵（Q-matrix）识别做准备。

## 潜在结构与一般可识别性

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Allman, Matias & Rhodes (2009). Identifiability of parameters in latent structure models with many observed variables. | `cdm/papers/allman-matias-rhodes-2009-latent-structure-identifiability.md` | CDM 识别理论的上游。重点读 three-block 分解、Kruskal 条件和 generic identifiability 的表达方式。 |
| 背景 | Allman & Rhodes (2006/2009). Tree topology and covarion identifiability papers. | `cdm/papers/allman-rhodes-phylogenetic-identifiability.md` | 不作为 CDM 主证明，但能帮助理解 mixture/covarion 模型里如何写 identifiability。 |
| 背景 | Koopmans & Reiersøl (1950). The identification of structural characteristics. | `cdm/papers/koopmans-reiersol-1950-identification.md` | 一般识别问题的经典统计背景，作为术语和思想来源。 |
| 背景 | Koopmans (1950). Statistical Inference in Dynamic Economic Models. | `cdm/papers/koopmans-1950-dynamic-economic-models.md` | 只读 identification 相关背景，不进入 CDM 主线。 |
| 背景 | Rothenberg (1971). Identification in parametric models. | `cdm/papers/rothenberg-1971-parametric-identification.md` | 用来补 parametric identifiability 的一般语言。 |

## 有限混合模型与潜在类模型

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Teicher (1967). Identifiability of mixtures of product measures. | `cdm/papers/teicher-1967-product-mixtures.md` | 有限乘积分布混合（mixtures of product measures）的基础识别结果。 |
| 精读 | Yakowitz & Spragins (1968). On the identifiability of finite mixtures. | `cdm/papers/yakowitz-spragins-1968-finite-mixtures.md` | 有限混合模型可识别性的经典结果，适合和 Teicher 对照。 |
| 主读 | Goodman (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. | `cdm/papers/goodman-1974-latent-structure.md` | 早期潜在结构分析（latent structure analysis）文本，适合理解 exploratory 视角。 |
| 主读 | Lindsay (1995). Mixture Models: Theory, Geometry and Applications. | `cdm/papers/lindsay-1995-mixture-models.md` | 混合模型几何（mixture geometry）和理论背景。 |
| 主读 | McLachlan & Peel (2000). Finite Mixture Models. | `cdm/papers/mclachlan-peel-2000-finite-mixture-models.md` | EM、模型选择、有限混合模型写作口径。 |
| 主读 | Carreira-Perpiñán & Renals (2000). Practical identifiability of finite mixtures of multivariate Bernoulli distributions. | `cdm/papers/carreira-perpinan-renals-2000-bernoulli-mixtures.md` | 和 CDM 的二元反应数据很接近，重点看 Bernoulli mixture 的 practical identifiability。 |
| 背景 | Gyllenberg, Koski, Reilink & Verlaan (1994). Nonuniqueness in probabilistic numerical identification of bacteria. | `cdm/papers/gyllenberg-koski-reilink-verlaan-1994-nonuniqueness.md` | 作为不可识别（nonuniqueness）的反例背景。 |

## 非参数混合与重复测量

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Hettmansperger & Thomas (2000). Almost nonparametric inference for repeated measures in mixture models. | `cdm/papers/hettmansperger-thomas-2000-repeated-measures-mixtures.md` | repeated measures 下的 mixture 识别和估计背景。 |
| 主读 | Hall & Zhou (2003). Nonparametric estimation of component distributions in a multivariate mixture. | `cdm/papers/hall-zhou-2003-nonparametric-mixtures.md` | 多变量混合的非参数估计（nonparametric estimation）。 |
| 主读 | Elmore, Hettmansperger & Thomas (2004). Estimating component cumulative distribution functions in finite mixture models. | `cdm/papers/elmore-hettmansperger-thomas-2004-component-cdf.md` | component distribution 的估计方法，和非参数 mixture 线相连。 |
| 主读 | Hall, Neeman, Pakyari & Elmore (2005). Nonparametric inference in multivariate mixtures. | `cdm/papers/hall-neeman-pakyari-elmore-2005-multivariate-mixtures.md` | 多变量非参数 mixture 的推断框架。 |
| 主读 | Elmore, Hall & Neeman (2005). An application of classical invariant theory to identifiability in nonparametric mixtures. | `cdm/papers/elmore-hall-neeman-2005-invariant-theory.md` | 非参数 mixture 的识别证明工具，和数学工具页交叉。 |
| 主读 | Cruz-Medina, Hettmansperger & Thomas (2004). Semiparametric mixture models and repeated measures: The multinomial cut point model. | `cdm/papers/cruz-medina-hettmansperger-thomas-2004-cut-point.md` | repeated measures 与半参数 mixture 的具体模型。 |
| 背景 | Benaglia, Chauveau & Hunter (2009). An EM-like algorithm for semi and nonparametric estimation in multivariate mixtures. | `cdm/papers/benaglia-chauveau-hunter-2009-em-like-mixtures.md` | 读算法思路即可，后续可和 CDM 的 EM、MML、变分方法对照。 |

## 暂时读法

这一组不要求一开始全部细节吃透。优先顺序是：

1. Allman, Matias & Rhodes (2009)
2. Kruskal (1977)，见数学工具页
3. Teicher (1967) 与 Yakowitz & Spragins (1968)
4. Goodman (1974)、Lindsay (1995)、McLachlan & Peel (2000)
5. 非参数 mixture 和 repeated-measures 文献
