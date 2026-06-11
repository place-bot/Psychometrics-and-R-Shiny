# CDM 核心模型

这一页整理认知诊断模型（Cognitive Diagnosis Models, CDM）的主线模型。先读模型结构，再进入 Q 矩阵、可识别性和估计。

## 阅读目标

- 区分 DINA、DINO、G-DINA、LCDM、GDM 和 Fusion Model 的建模假设。
- 明确 Q 矩阵（Q-matrix）如何把项目（items）和属性（attributes）连接起来。
- 追踪从强假设模型到一般框架的路线：conjunctive/disjunctive models 到 saturated/general models。
- 为后面读 GDINA 软件和扩展模型建立统一符号。

## 基础与早期框架

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Junker & Sijtsma (2001). Cognitive assessment models with few assumptions, and connections with nonparametric item response theory. | `cdm/papers/junker-sijtsma-2001-few-assumptions.md` | CDM 与非参数 IRT（nonparametric IRT）的连接。重点读少假设模型和诊断解释。 |
| 精读 | de la Torre (2009). DINA model and parameter estimation: A didactic. | `cdm/papers/de-la-torre-2009-dina-didactic.md` | DINA 的入门核心文献。重点读 slip、guessing、likelihood 和 EM 估计。 |
| 精读 | Templin & Henson (2006). Measurement of psychological disorders using cognitive diagnosis models. | `cdm/papers/templin-henson-2006-dino.md` | DINO 模型（Deterministic Input, Noisy Or gate）的代表文献，适合和 DINA 对照。 |

## 一般化模型与统一框架

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | de la Torre (2011). The generalized DINA model framework. | `cdm/papers/de-la-torre-2011-gdina.md` | G-DINA 是后续很多模型比较的中心。重点读 saturated item response function 和子模型约束。 |
| 主读 | Henson, Templin & Willse (2009). Defining a Family of Cognitive Diagnosis Models Using Log-Linear Models with Latent Variables. | `cdm/papers/henson-templin-willse-2009-lcdm.md` | LCDM 用 log-linear 语言统一一组 CDM，和 G-DINA、GDM 对照。 |
| 主读 | von Davier (2005/2008). A general diagnostic model applied to language testing data. | `cdm/papers/von-davier-2008-general-diagnostic-model.md` | 一般诊断模型（general diagnostic model, GDM）路线。重点看离散潜变量与项目参数化方式。 |
| 主读 | Roussos, DiBello, Stout, Hartz, Henson & Templin (2007). The Fusion Model Skills Diagnosis System. | `cdm/papers/roussos-dibello-stout-hartz-henson-templin-2007-fusion.md` | Fusion Model 的系统化诊断框架，适合理解技能诊断系统设计。 |
| 主读 | Rupp, Templin & Henson (2010). Diagnostic Measurement: Theory, Methods, and Applications. | `cdm/papers/rupp-templin-henson-2010-diagnostic-measurement.md` | 作为模型族和应用写作的书本背景。 |

## 软件与扩展入口

| 阅读级别 | 论文 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Ma & de la Torre (2020). GDINA: An R package for cognitive diagnosis modeling. | `cdm/papers/ma-de-la-torre-2020-gdina-package.md` | 网站后续要接 R Shiny，所以这篇是实现入口。重点读 `GDINA` 包能拟合哪些模型。 |
| 主读 | Zhan, Wang, Jiao & Bian (2018). Probabilistic-input, noisy conjunctive models for cognitive diagnosis. | `cdm/papers/zhan-wang-jiao-bian-2018-pinc.md` | PINC 模型把输入掌握状态概率化。后续和 continuous-Q、partial mastery 线连接。 |

## 推荐顺序

1. Junker & Sijtsma (2001)
2. de la Torre (2009)
3. Templin & Henson (2006)
4. de la Torre (2011)
5. Henson, Templin & Willse (2009)
6. Ma & de la Torre (2020)
7. Zhan, Wang, Jiao & Bian (2018)
