# CTT vs IRT 十大规则总览

关于本章

本章系统比较经典测量理论（CTT）与项目反应理论（IRT）的十个核心差异。每个规则都包含完整的推导过程和实例分析。

## 规则概览表

| 规则 | CTT 观点 | IRT 观点 | 核心公式 |
| --- | --- | --- | --- |
| [规则1](10_rules_ctt_irt/rule01_measurement_error.md) | 标准误恒定 | 标准误因人而异 | \(SE_{CTT} = \sigma\sqrt{1-r_{tt}}\) vs \(SE_{IRT}(\theta) = \frac{1}{\sqrt{I(\theta)}}\) |
| [规则2](10_rules_ctt_irt/rule02_test_length.md) | 越长越好 | 质量胜于数量 | Spearman-Brown: \(r_{nn} = \frac{nr_{tt}}{1+(n-1)r_{tt}}\) |
| [规则3](10_rules_ctt_irt/rule03_test_forms.md) | 需要平行测验 | 个性化最优 | 平行条件 vs 自适应算法 |
| [规则4](10_rules_ctt_irt/rule04_item_properties.md) | 样本依赖 | 样本无关 | \(p = \int P(\theta)g(\theta)d\theta\) vs \(P(\theta) = \frac{e^{\theta-b}}{1+e^{\theta-b}}\) |
| [规则5](10_rules_ctt_irt/rule05_score_meaning.md) | 常模参照 | 项目参照 | 百分位数 vs 能力-项目距离 |
| [规则6](10_rules_ctt_irt/rule06_interval_scale.md) | 通过正态化 | 通过模型 | 非线性变换 vs logit线性性 |
| [规则7](10_rules_ctt_irt/rule07_mixed_formats.md) | 权重不平衡 | 最优组合 | 隐含权重 vs GPCM |
| [规则8](10_rules_ctt_irt/rule08_change_scores.md) | 初值依赖 | 可比较 | \(r_{DD} = f(r_{12})\) vs MRMLC |
| [规则9](10_rules_ctt_irt/rule09_factor_analysis.md) | Phi相关问题 | 全信息方法 | \(\phi_{max} < 1\) vs M2PL |
| [规则10](10_rules_ctt_irt/rule10_item_features.md) | 特征不重要 | 特征可建模 | 黑箱 vs LLTM |

## 理论框架

### CTT 基础

CTT 核心模型

\[X = T + E\]

**关键假设**：
1. \(E(E) = 0\)
2. \(\text{Cov}(T,E) = 0\)
3. 误差对所有人相同

### IRT 基础

IRT 核心模型（Rasch）

\[P(\theta) = \frac{e^{\theta-b}}{1+e^{\theta-b}}\]

**关键特征**：
1. 概率化建模
2. 个体化精度
3. 参数分离

## 快速导航

### 🎯 如果你关心测量精度

- [规则1：测量标准误](10_rules_ctt_irt/rule01_measurement_error.md)
- [规则2：测验长度与信度](10_rules_ctt_irt/rule02_test_length.md)

### 📊 如果你关心测验开发

- [规则3：可互换的测验形式](10_rules_ctt_irt/rule03_test_forms.md)
- [规则4：项目属性估计](10_rules_ctt_irt/rule04_item_properties.md)
- [规则10：项目刺激特征](10_rules_ctt_irt/rule10_item_features.md)

### 📈 如果你关心分数解释

- [规则5：得分的意义](10_rules_ctt_irt/rule05_score_meaning.md)
- [规则6：区间量表属性](10_rules_ctt_irt/rule06_interval_scale.md)
- [规则8：变化得分](10_rules_ctt_irt/rule08_change_scores.md)

### 🔬 如果你关心高级分析

- [规则7：混合项目格式](10_rules_ctt_irt/rule07_mixed_formats.md)
- [规则9：二元项目因素分析](10_rules_ctt_irt/rule09_factor_analysis.md)

## 符号约定

| 符号 | 含义 |
| --- | --- |
| \(X\) | 观察分数 |
| \(T\) | 真分数 |
| \(E\) | 测量误差 |
| \(\theta\) | IRT能力参数 |
| \(b\) | IRT难度参数 |
| \(P(\theta)\) | 反应概率函数 |
| \(I(\theta)\) | 信息函数 |
| \(r_{tt}\) | 信度系数 |
| \(SE\) | 标准误 |

## 参考文献

核心文献

- Gulliksen, H. (1950). *Theory of mental tests*
- Lord, F. M., & Novick, M. R. (1968). *Statistical theories of mental test scores*
- Rasch, G. (1960). *Probabilistic models for some intelligence and attainment tests*
- Embretson, S. E., & Reise, S. P. (2000). *Item response theory for psychologists*

## 学习建议

如何使用本章

1. **顺序学习**：按规则1-10的顺序，理解CTT到IRT的演进
2. **对比学习**：每个规则都对比CTT和IRT的方法
3. **推导为主**：重点理解每个公式的推导过程
4. **实例验证**：通过数值例子加深理解

**适合读者**：

- 有基本统计学基础
- 熟悉概率论基本概念
- 对心理测量感兴趣的研究者

---

本章内容基于 Embretson & Reise (2000) 第二章整理
