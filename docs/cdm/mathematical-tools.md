# 数学工具

这一页整理证明工具。它们不都是 CDM 论文，但会反复出现在潜在类模型（latent class models）、受限潜在类模型（restricted latent class models, RLCM）和可识别性（identifiability）证明中。

## 核心工具

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 精读 | Kruskal (1977). Three-way arrays: Rank and uniqueness of trilinear decompositions, with application to arithmetic complexity and statistics. | `cdm/papers/kruskal-1977-three-way-arrays.md` | Allman, Matias & Rhodes (2009) 的底层唯一性工具。重点读 Kruskal rank 和三路张量分解唯一性。 |
| 背景 | Kruskal (1976). More factors than subjects, tests and treatments. | `cdm/papers/kruskal-1976-indeterminacy.md` | 可选。帮助理解分解不唯一和不可识别现象。 |
| 主读 | Lauritzen (1996). Graphical Models. | `cdm/papers/lauritzen-1996-graphical-models.md` | 图模型（graphical models）、条件独立（conditional independence）和潜变量结构的通用语言。 |

## 怎么读

这些文献不适合按章节硬读。更有效的方式是围绕后续证明问题做摘录：

- Kruskal 条件到底要求哪些矩阵列秩或 Kruskal rank。
- 张量分解唯一性如何转化成 latent class model 的参数唯一性。
- 图模型语言如何表达条件独立和潜变量结构。
