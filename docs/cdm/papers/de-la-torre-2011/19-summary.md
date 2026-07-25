# 总结与后续阅读

## 论文的核心贡献

### 1. 将 DINA 推广到项目约化属性组

DINA 每题只有低、高两个成功组；G-DINA 为全部

\[
2^{K_j^*}
\]

个约化属性模式分别建模。

### 2. 用 link function 统一一般 CDM

identity、logit 和 log link 分别描述：

- 概率加法；
- log-odds 加法；
- 概率乘法。

饱和时三者拟合相同，约化以后形成不同模型。

### 3. 用 design matrix 统一参数化

\[
h(\boldsymbol P_j)
=
M_j\boldsymbol\phi_j.
\]

同一个矩阵框架可以表达饱和模型、DINA、DINO、A-CDM、LLM、G-NIDA/R-RUM 与其他分组模型。

### 4. 建立两步估计

先用 MMLE 获得

\[
\widehat{\boldsymbol P}_j,
\]

再通过矩阵变换或带权拟合得到具体模型参数。饱和模型和论文定义的特殊约化类具有明确的 MLE 保证。

### 5. 建立逐题 Wald 检验

限制矩阵把模型约化写成

\[
R_{jr}f(\boldsymbol P_j)=0,
\]

从而在不重新拟合全部反应数据的情况下检验每道题的模型结构。

## 实验结论

### 模拟

在 \(I=2000,J=30,K=5\)、每种生成模型 1,000 个数据集的条件下：

- A-CDM 为真时，Wald Type I error 接近 0.01、0.05、0.10；
- DINA/DINO 为真时，拒绝 A-CDM 的 power 为 1.0。

该结论适用于论文设置的高信号条件。

### 分数减法数据

536 名学生、12 题、4 属性的分析显示：

- 只有少数多属性题接近 DINA；
- 部分属性的单独贡献明显不对称；
- 三属性组合可能形成关键提升；
- 饱和 G-DINA 能显示 DINA 二组压缩隐藏的结构。

### 临床数据

1,210 名受试者、44 个 MCMI-III 项目的分析说明 CDM 可以迁移到临床诊断变量。例示项目的四个概率近似满足 identity-link 加法。根据同年勘误，相关受版权保护题干不应转载。

## 论文结论的强度

论文有力支持：

- 模型之间的代数关系；
- design/weight/restriction matrix 框架；
- MMLE 与饱和参数变换；
- 特定模拟条件下的 Wald 表现；
- 两个真实数据例子的可解释性。

论文仍未解决：

- 广泛条件下的 SE 与 Wald 小样本性质；
- Q 矩阵错误；
- 模式稀疏；
- 选择后推断；
- 跨项目约束；
- 分类准确率与干预效度。

## 对当前研究的直接启示

G-DINA framework 提供了一种层次清晰的建模方式：

\[
\text{先允许充分灵活的项目反应结构}
\longrightarrow
\text{再逐题检验可解释约束}.
\]

对于 CD-CAT 或生成式选题研究，它适合作为学生反应模型。实时 adaptive 行为还需要把后验更新、选题效用、内容平衡和停止规则连接到每次交互。

## 后续阅读

1. **Ma & de la Torre (2020)**：`GDINA` R package，把 2011 framework 发展成完整软件。
2. **de la Torre & Lee (2013)**：进一步评估 item-level Wald test。
3. **Henson, Templin & Willse (2009)**：LCDM 的 log-linear 统一框架。
4. **von Davier (2005/2008)**：GDM 与更一般诊断模型。
5. **de la Torre & Chiu (2016)**：G-DINA 的 Q 矩阵验证。

模型主线的直接后续是 Ma & de la Torre (2020) 的 `GDINA` R package 论文，它将转向用户接口、软件对象、模型拟合与可复现工作流。按照本站跨类别制作顺序，下一篇进入 [Xu (2017) 的二分 restricted latent class model 可识别性](../xu-2017/index.md)。
