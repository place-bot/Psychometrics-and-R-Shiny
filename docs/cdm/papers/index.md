# CDM 单篇论文精读总进度

CDM 论文库目前收录 **86 篇**。每篇都按 BOBCAT 专题的深度制作成多页面笔记，并在导航中采用四层结构：

```text
CDM
└── 单篇论文精读
    └── 论文类别
        └── 作者与年份
            ├── 阅读导引
            ├── 问题与基础
            ├── 模型与符号
            ├── 公式、定理或算法
            ├── 证明或手算示例
            ├── 实验与结果
            ├── 代码实现
            ├── 总结
            └── 参考文献
```

页面名称会随论文类型调整：

- 理论论文：重点展开定理、证明、反例、证据边界和可计算复现；
- 方法论文：重点展开目标函数、估计算法、实验、消融与官方代码；
- 软件论文：重点展开接口、对象结构、计算流程、示例和实现映射；
- 书籍：按与 CDM 有关的章节拆分，并明确本专题实际覆盖的章节。

## 当前进度

| 类别 | 数量 | 已完成 | 当前状态 |
| --- | ---: | ---: | --- |
| [潜在结构与混合模型](categories/latent-structure-mixtures.md) | 18 | 1 | Allman et al. (2009) 已完成首版 |
| [数学工具](categories/mathematical-tools.md) | 3 | 1 | Kruskal (1977) 已完成首版 |
| [HMM、网络与机器学习](categories/hmm-network-ml.md) | 15 | 0 | 待逐篇制作 |
| [CDM 核心模型](categories/core-models.md) | 10 | 2 | de la Torre (2009, 2011) 已完成首版 |
| [Q 矩阵验证与学习](categories/q-matrix.md) | 14 | 6 | de la Torre (2008)、de la Torre & Chiu (2016)、Liu et al. (2012, 2013)、Chen et al. (2018)、Gu & Xu (2021) 已完成首版 |
| [可识别性理论](categories/identifiability.md) | 9 | 1 | Xu (2017) 已完成首版 |
| [估计、正则化与计算](categories/estimation-computation.md) | 5 | 0 | 待逐篇制作 |
| [连续化与扩展模型](categories/continuous-extensions.md) | 8 | 0 | 待逐篇制作 |
| **合计** | **86** | **11** | 持续更新 |

## 制作顺序

制作顺序同时考虑依赖关系和 CDM 主线：

1. Allman、Matias 与 Rhodes (2009)：三块张量识别总入口；
2. Kruskal (1977)：三路分解唯一性的数学核心；
3. de la Torre (2009)：DINA 模型与估计；
4. de la Torre (2011)：G-DINA 框架；
5. Xu (2017)：二分 RLCM 可识别性（已完成）；
6. de la Torre (2008)：DINA 的经验 Q 矩阵验证（已完成）；
7. de la Torre and Chiu (2016)：一般经验 Q 矩阵验证（已完成）；
8. Liu, Xu and Ying (2012)：数据驱动 Q 矩阵学习（已完成）；
9. Liu, Xu and Ying (2013)：自学习 Q 矩阵理论（已完成）；
10. Chen, Culpepper, Chen and Douglas (2018)：Bayesian DINA Q 矩阵估计（已完成）；
11. Gu and Xu (2021)：Q 矩阵可识别的必要充分条件（已完成）；
12. Zhao and Huang (2019)：文本分类自动识别 Q 矩阵（下一篇）；
13. 高维估计、正则化和结构学习；
14. partial mastery、continuous-Q 和 general-response 扩展；
15. HMM、随机图与机器学习背景；
16. 其余混合模型和识别理论来源。

同一类别中的详细清单保留原索引顺序。完整书目信息见[论文总索引](../paper-index.md)。

## 完成标准

一篇论文只有同时满足以下条件才标记“已完成”：

1. 核对原始 PDF，而非只读摘要；
2. 逐符号解释核心模型；
3. 把关键公式连接成算法或证明链；
4. 覆盖全部主要定理或实验表；
5. 区分论文结论、本站推导和推测；
6. 有官方代码时完成论文公式到代码对象的映射；
7. 无官方代码时明确说明，并提供合适的可计算检查；
8. 说明与 CDM 主线的接口和不能推出的结论；
9. 通过 MkDocs 严格构建和页面渲染检查。
