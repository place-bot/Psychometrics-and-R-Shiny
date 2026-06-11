# Psychometrics and R Shiny Notes

本站整理心理测量、经典测量理论（CTT）、项目反应理论（IRT）、认知诊断模型（CDM）与 R Shiny 入门实践笔记。

内容按主题拆分，适合课堂复习、概念查阅和后续继续校对。站点使用 **MkDocs + Material** 构建，支持数学公式、代码块、全文搜索和结构化导航。

## 快速入口

- [心理测量基础](psychometrics/index.md)
- [IRT 模型](irt-models/index.md)
- [IRT 估计与评估](irt-estimation/index.md)
- [CTT/IRT 应用规则](10_rules_ctt_irt/index.md)
- [认知诊断模型（CDM）](cdm/index.md)
- [R Shiny](shiny/index.md)
- [质量与维护](quality/index.md)

## 记号示例

二参数逻辑模型（2PL）的常见形式为：

\[
P(X_{ij}=1 \mid \theta_j)
=
\frac{1}{1+\exp[-a_i(\theta_j-b_i)]}
\]

其中 \(\theta_j\) 表示被试 \(j\) 的潜在特质水平，\(a_i\) 表示项目 \(i\) 的区分度，\(b_i\) 表示项目难度。
