# CDM 论文学习路线

认知诊断模型（Cognitive Diagnosis Models, CDM）分区按论文学习组织。当前论文库包含 86 篇，
分为八类；每篇都将建立 BOBCAT 级别的多页面精读专题。导航采用“论文类别 → 单篇论文 →
导引/模型/公式/证明或算法/实验/代码/总结”的层级，完成情况见
[单篇论文精读总进度](papers/index.md)。

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
| 10 | [单篇论文精读总进度](papers/index.md) | 八类、86 篇论文的完成状态与制作顺序 |

## 单篇论文模板

每篇论文采用多页面结构，并根据理论、方法、软件或书籍类型调整页面名称：

```text
论文类别/
└── 作者年份/
    ├── 阅读导引
    ├── 问题与理论基础
    ├── 模型设定与符号
    ├── 关键公式、定理或算法
    ├── 证明细节或手算示例
    ├── 实验、结果与证据边界
    ├── 官方代码精读或可计算复现
    ├── 与 CDM 主线的关系
    ├── 总结
    └── 参考文献
```

理论论文没有经验实验、官方代码时，对应页面会明确记录这个事实，并用定理证据和可计算检查
替代，不补写原文不存在的结果。
