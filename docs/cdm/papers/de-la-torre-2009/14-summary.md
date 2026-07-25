# 总结与后续阅读

## 这篇论文完成了什么

de la Torre (2009) 把 DINA 模型组织成一条可执行流程：

1. 用 Q 矩阵声明每道题要求的属性；
2. 用 AND gate 计算理想反应；
3. 用 \(g_j,s_j\) 描述观测噪声；
4. 把 \(2^K\) 个属性模式写成受限潜在类；
5. 用边际似然避免 JML 的 incidental parameter 问题；
6. 用 EM 的期望计数闭式更新项目参数；
7. 用观测信息矩阵计算标准误；
8. 用模拟和真实数据展示算法表现；
9. 用 HO-DINA 展示属性分布降维路线。

## 最核心的四条公式

### 理想反应

\[
\eta_{ij}
=
\prod_{k=1}^{K}
\alpha_{ik}^{q_{jk}}.
\]

### 反应函数

\[
P(X_{ij}=1\mid\boldsymbol\alpha_i)
=
g_j^{1-\eta_{ij}}
(1-s_j)^{\eta_{ij}}.
\]

### E 步

\[
w_{il}
=
\frac{
\pi_lL(\boldsymbol X_i\mid\boldsymbol\alpha_l)
}{
\sum_h
\pi_hL(\boldsymbol X_i\mid\boldsymbol\alpha_h)
}.
\]

### M 步

\[
\widehat g_j
=
\frac{R_j^{(0)}}{I_j^{(0)}},
\qquad
\widehat s_j
=
\frac{I_j^{(1)}-R_j^{(1)}}{I_j^{(1)}}.
\]

## 实验证据

模拟研究在

\[
I=2000,\ J=30,\ K=5
\]

和 \(g_j=s_j=.20\) 下进行 100 次重复：

- 几乎所有平均估计四舍五入后恢复为 .20；
- 只有 \(\overline{\widehat s}_{25}=.21\)；
- 模型标准误与经验标准差接近；
- 模型 SE 平均约保守 2%。

真实分数减法数据中，DINA-EM 与 HO-DINA-MCMC 的项目参数大多相同或相差 .01，主要差异集中在 Item 5 的 guessing 和少数边界标准误。

## 论文贡献的准确定位

它提供了：

- DINA 的清晰教学定义；
- 可执行的 EM 推导；
- 标准误公式；
- 一个模拟可行性检查；
- 一个真实数据示范；
- HO-DINA 的计算动机。

它没有完成：

- Q 矩阵估计与验证；
- DINA 可识别性条件；
- 系统分类准确率研究；
- 多条件大规模模拟；
- 公开代码仓库；
- G-DINA 等一般模型比较。

## 与前两篇专题的连接

\[
\text{Kruskal / Allman}
\quad\Rightarrow\quad
\text{潜在类参数何时可由总体分布恢复},
\]

\[
\text{de la Torre (2009)}
\quad\Rightarrow\quad
\text{DINA 的受限类概率怎样定义和估计}.
\]

识别理论与 EM 算法回答不同问题：

- 唯一性理论关心总体映射；
- EM 关心给定模型下怎样寻找似然解；
- 一个算法收敛并不能替代识别证明。

## 下一篇

下一篇按主线进入：

> de la Torre, J. (2011). The Generalized DINA Model Framework.

重点将从两状态 DINA 反应函数扩展到：

- 属性主效应；
- 高阶交互；
- 饱和项目反应函数；
- DINA、DINO、A-CDM、LLM 等约束子模型；
- 模型选择与相对拟合。

它会直接回答本篇留下的核心模型限制：同一题上，不同部分掌握模式能否拥有不同答对概率。
