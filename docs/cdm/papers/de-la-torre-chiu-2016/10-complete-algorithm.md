# 完整估计与验证算法

## 输入

- \(N\times J\) 二分反应矩阵 \(Y\)；
- \(J\times K\) 初始 Q 矩阵 \(Q_0\)；
- G-DINA 模型；
- PVAF 阈值 \(\varepsilon\)。

## 阶段 1：在初始 Q 下拟合模型

用 empirical Bayes EM 估计：

- 项目参数；
- 属性模式总体概率；
- 每个学生的完整属性模式后验。

\[
\tau_{il}
=
P(\boldsymbol\alpha_i=\boldsymbol\alpha_l
\mid\boldsymbol Y_i,Q_0,\widehat\Theta).
\]

## 阶段 2：构造完整模式统计量

模式权重：

\[
\widehat w_l
=
\frac{1}{N}\sum_i\tau_{il}.
\tag{13}
\]

题目 \(j\) 在完整模式 \(l\) 下的成功概率：

\[
\widehat p_{jl}
=
\frac{\sum_i\tau_{il}Y_{ij}}
{\sum_i\tau_{il}}.
\tag{14}
\]

论文正文只概括两阶段过程；Liu (2017) 根据与作者的沟通明确给出式 (14)。

## 阶段 3：逐题穷举候选

对每个 \(\boldsymbol q\ne\boldsymbol0\)：

1. 按候选要求的属性把 \(2^K\) 个完整模式分组；
2. 对每组求 \(\widehat w\)；
3. 以 \(\widehat w\) 对 \(\widehat p_{jl}\) 加权求组成功率；
4. 计算 \(\widehat{\varsigma}_j^2(\boldsymbol q)\)；
5. 除以全属性向量 GDI，得到 PVAF。

## 阶段 4：产生建议 Q

每题执行：

\[
\operatorname{PVAF}\ge\varepsilon
\rightarrow
\text{最少属性}
\rightarrow
\text{同规模最大 GDI}.
\]

把所有建议行组合为

\[
\widehat Q.
\]

## 阶段 5：内容审核

论文真实数据分析显示，统计建议可能在相似题目之间产生内容上难以解释的差异。完整应用需要：

1. 检查建议新增或删除的属性是否符合解题步骤；
2. 重新拟合建议 Q；
3. 比较项目拟合、整体拟合和分类稳定性；
4. 对接近阈值的多个候选保留不确定性；
5. 由学科专家确认最终 Q。

## 算法中的三种“概率”

| 对象 | 公式 | 角色 |
| --- | --- | --- |
| 学生后验 | \(\tau_{il}\) | 把每个人软分配到完整属性模式 |
| 模式权重 | \(\widehat w_l=N^{-1}\sum_i\tau_{il}\) | GDI 的加权分布 |
| 成功概率 | \(\widehat p_{jl}\) | 描述题目在完整模式下的反应结构 |

## 原文实现边界

论文说明两步分析由 Ox 程序完成，并邀请读者联系第一作者获取代码。文章、补充材料和参考文献均没有公开仓库链接，所以目前无法逐行核对原 Ox 实现。
