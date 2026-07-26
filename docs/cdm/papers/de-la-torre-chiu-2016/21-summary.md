# 总结与后续阅读

## 一条主线

\[
Y,Q_0
\longrightarrow
\widehat P(\boldsymbol\alpha_i\mid\boldsymbol Y_i)
\longrightarrow
\widehat w_l,\widehat p_{jl}
\longrightarrow
\widehat{\varsigma}_j^2(\boldsymbol q)
\longrightarrow
\operatorname{PVAF}
\longrightarrow
\text{最简建议 q-vector}.
\]

## 五个核心公式

### 完整模式成功概率

\[
\widehat p_{jl}
=
\frac{\sum_i\tau_{il}Y_{ij}}
{\sum_i\tau_{il}}.
\]

### 折叠成功概率

\[
p_j(G)
=
\frac{\sum_{\boldsymbol\alpha\in G}
w(\boldsymbol\alpha)p_j(\boldsymbol\alpha)}
{\sum_{\boldsymbol\alpha\in G}w(\boldsymbol\alpha)}.
\]

### GDI

\[
\varsigma_j^2(\boldsymbol q)
=
\sum_Gw(G)[p_j(G)-\bar p_j]^2.
\]

### 主定理

\[
\varsigma_j^2(\boldsymbol q)
\le
\varsigma_j^2(\boldsymbol q^*).
\]

### PVAF

\[
\operatorname{PVAF}_j(\boldsymbol q)
=
\frac{\widehat{\varsigma}_j^2(\boldsymbol q)}
{\widehat{\varsigma}_j^2(\boldsymbol1)}.
\]

## 最重要的逻辑

遗漏有效属性会合并成功概率不同的类别：

\[
\frac{w_0w_1}{w_0+w_1}(p_0-p_1)^2
\]

这部分组间方差随折叠消失。

加入无关属性只会细分同质组，GDI 保持不变。由此形成：

\[
\text{最大 GDI}
+
\text{最少属性}.
\]

## 原文证据

| 证据 | 结论 |
| --- | --- |
| Table 1 | 正确向量与增设向量并列，漏设向量 GDI 较小 |
| Study 1 | 五种约化模型下正确 Q 高保留，多数错误被纠正 |
| Study 2 | 无约束 G-DINA 下恢复更困难 |
| 分数减法 | 8/11 保留，3/11 建议删除化简属性 |
| 2017 评论与回应 | 初始 Q、固定阈值和相合性仍需额外理论 |

## 2008 与 2016 的位置

| 论文 | 主要对象 | 关键指标 |
| --- | --- | --- |
| de la Torre (2008) | DINA Q 验证 | \(\delta=1-s-g\) |
| de la Torre & Chiu (2016) | G-DINA 家族 Q 验证 | \(\varsigma^2\) 与 PVAF |

2016 年方法保留了“用学生后验期望计数重评候选 Q”的思想，并把两组区分推广为多组方差。

## 实践使用清单

1. 说明 provisional Q 的来源；
2. 拟合饱和 G-DINA；
3. 检查后验类别稀疏性；
4. 报告 GDI/PVAF path；
5. 做 \(\varepsilon\) 敏感性；
6. 比较单次与迭代建议；
7. 对建议 Q 重新拟合；
8. 检查模型拟合和分类稳定性；
9. 由领域专家逐题审核；
10. 把不确定候选保留下来。

## 下一篇

[Liu, Xu & Ying (2012)：Data-driven Learning of Q-matrix](../liu-xu-ying-2012/index.md)

阅读重点：

- 从“验证一个大体可信的 Q”走向“数据驱动学习 Q”；
- 目标函数怎样定义；
- 搜索和更新怎样进行；
- 对初值、可识别性和一致性提供哪些保证；
- 与 GDI/PVAF 的候选评价有何差异。

## 与 CAT 的接口

Q 验证解决题库属性标签质量。CAT 再利用该结构实时更新学生状态并选下一题：

\[
\text{validated Q}
\rightarrow
\text{posterior update}
\rightarrow
\text{item utility}
\rightarrow
\text{next item}.
\]

这条链说明 Q 错误会一路传播到 adaptive decision。
