# CDM 论文学习路线

认知诊断模型（Cognitive Diagnosis Models, CDM）分区先按论文学习来组织。这里暂时不把每篇论文都拆成独立页面，而是先建立细分专题、阅读顺序和论文索引；后续可以按 `cdm/papers/作者-年份-关键词.md` 的方式逐篇扩展。

写作语言以中文为主，第一次出现的重要术语保留英文括注，例如 Q 矩阵（Q-matrix）、可识别性（identifiability）、潜在类模型（latent class model）、受限潜在类模型（restricted latent class model, RLCM）、部分掌握（partial mastery）和张量分解（tensor decomposition）。

## 阅读顺序

1. 先读理论背景：潜在结构模型（latent structure models）、有限混合模型（finite mixture models）、非参数混合模型（nonparametric mixture models）和一般可识别性语言。
2. 再读数学工具：Kruskal 三路数组唯一性（three-way array uniqueness）和图模型（graphical models）。
3. 补 HMM、网络和机器学习背景：这些不是 CDM 主线，但能帮助理解隐藏状态（hidden states）、块模型（block models）和 EM 式学习（EM-like learning）。
4. 进入 CDM 主线：DINA、DINO、G-DINA、LCDM、GDM、Fusion Model 和 GDINA 软件框架。
5. 精读 Q 矩阵、可识别性、估计与正则化：这是后续写 continuous-Q 或 exploratory CDM 时最关键的理论与算法支撑。
6. 最后读连续化与扩展模型：部分掌握（partial mastery）、连续属性（continuous attributes）、连续反应（continuous responses）和广义反应（general-response）模型。

## 专题页

| 顺序 | 专题 | 当前用途 |
| --- | --- | --- |
| 1 | [潜在结构与混合模型](theoretical-background.md) | 建立可识别性和混合模型的理论底座 |
| 2 | [数学工具](mathematical-tools.md) | 汇总证明工具和几何语言 |
| 3 | [HMM、网络与机器学习背景](hmm-network-ml.md) | 放置辅助背景，不混进 CDM 主线 |
| 4 | [核心模型](core-models.md) | DINA、DINO、G-DINA、LCDM、GDM、Fusion Model |
| 5 | [Q 矩阵验证与学习](q-matrix.md) | Q 矩阵验证、学习、部分已知 Q 矩阵和 AI 辅助方法 |
| 6 | [可识别性理论](identifiability.md) | CDM 与 RLCM 的识别定理、必要充分条件和 generic identifiability |
| 7 | [估计、正则化与计算](estimation-computation.md) | 正则化、联合 MLE、高维属性模式、结构学习 |
| 8 | [连续化与扩展模型](continuous-extensions.md) | partial mastery、continuous response、general-response CDM |
| 9 | [论文索引](paper-index.md) | 所有纳入阅读计划的论文总表 |

## 后续单篇论文模板

每篇论文后续单独成页时建议统一结构：

```text
# 作者年份：短标题

## 为什么读
## 论文问题
## 模型设定
## 关键定理或算法
## 和 CDM 主线的关系
## 我自己的问题
## 可引用句子和符号
```

先把专题骨架稳定下来，再逐篇填充，可以避免导航栏太早变得不可维护。
