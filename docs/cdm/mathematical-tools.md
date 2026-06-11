# 数学工具

这一页整理证明工具。它们不都是 CDM 论文，但会反复出现在潜在类模型（latent class models）、受限潜在类模型（restricted latent class models, RLCM）和可识别性（identifiability）证明中。

## 核心工具

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Kruskal (1977). Three-way arrays: Rank and uniqueness of trilinear decompositions, with application to arithmetic complexity and statistics. | `cdm/papers/kruskal-1977-three-way-arrays.md` | Allman, Matias & Rhodes (2009) 的底层唯一性工具。重点读 Kruskal rank 和三路张量分解唯一性。 |
| 背景 | Kruskal (1976). More factors than subjects, tests and treatments. | `cdm/papers/kruskal-1976-indeterminacy.md` | 可选。帮助理解分解不唯一和不可识别现象。 |
| 主读 | Lauritzen (1996). Graphical Models. | `cdm/papers/lauritzen-1996-graphical-models.md` | 图模型（graphical models）、条件独立（conditional independence）和潜变量结构的通用语言。 |
| 主读 | Cox, Little & O'Shea (1997). Ideals, Varieties, and Algorithms. | `cdm/papers/cox-little-oshea-1997-ideals-varieties-algorithms.md` | 代数几何入门工具书，只读 ideals、varieties 和消元思想。 |
| 主读 | Pachter & Sturmfels (2005). Algebraic Statistics for Computational Biology. | `cdm/papers/pachter-sturmfels-2005-algebraic-statistics.md` | 代数统计（algebraic statistics）背景，帮助理解统计模型的代数表示。 |

## Segre 簇与张量几何

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Abo, Ottaviani & Peterson (2009). Induction for secant varieties of Segre varieties. | `cdm/papers/abo-ottaviani-peterson-2009-segre.md` | Segre 割线簇（secant varieties of Segre varieties）和张量秩（tensor rank）背景。 |
| 主读 | Catalisano, Geramita & Gimigliano (2002). Ranks of tensors, secant varieties of Segre varieties and fat points. | `cdm/papers/catalisano-geramita-gimigliano-2002-tensor-ranks.md` | 张量秩和 secant variety 的几何语言。 |
| 主读 | Catalisano, Geramita & Gimigliano (2005). Higher secant varieties of the Segre varieties \(P^1 \times \cdots \times P^1\). | `cdm/papers/catalisano-geramita-gimigliano-2005-higher-secant.md` | 二元变量场景下的 Segre 几何背景。 |
| 可选 | Drton (2006). Algebraic techniques for Gaussian models. | `cdm/papers/drton-2006-gaussian-algebraic-techniques.md` | 和 CDM 不直接相连，只作为 algebraic statistics 的旁支背景。 |
| 暂缓 | Garcia, Stillman & Sturmfels (2005). Algebraic geometry of Bayesian networks. | `cdm/papers/garcia-stillman-sturmfels-2005-bayesian-networks.md` | 先不作为主读。保留在索引里，避免后续忘记这条工具线。 |

## 怎么读

这些文献不适合按章节硬读。更有效的方式是围绕后续证明问题做摘录：

- Kruskal 条件到底要求哪些矩阵列秩或 Kruskal rank。
- 张量分解唯一性如何转化成 latent class model 的参数唯一性。
- 代数几何语言里，generic identifiability 为什么允许排除低维例外集合。
- 图模型语言如何表达条件独立和潜变量结构。
