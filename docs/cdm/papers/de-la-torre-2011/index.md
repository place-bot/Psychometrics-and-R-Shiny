# de la Torre (2011) 阅读导引

## 原文信息

| 项目 | 内容 |
| --- | --- |
| 论文 | Jimmy de la Torre. *The Generalized DINA Model Framework*. |
| 期刊 | *Psychometrika*, 76(2), 179--199, 2011 |
| DOI | [10.1007/s11336-011-9207-7](https://doi.org/10.1007/s11336-011-9207-7) |
| 出版商页面 | [Springer Nature](https://link.springer.com/article/10.1007/s11336-011-9207-7) |
| 原文 PDF | [Springer PDF](https://link.springer.com/content/pdf/10.1007/s11336-011-9207-7.pdf) |
| 勘误 | [10.1007/s11336-011-9214-8](https://doi.org/10.1007/s11336-011-9214-8) |
| 论文代码 | 作者使用 Ox 实现 MMLE；正文没有给出公开代码地址 |
| 后续软件 | [Wenchao-Ma/GDINA](https://github.com/Wenchao-Ma/GDINA)，由 Wenchao Ma 和 Jimmy de la Torre 开发 |

## 这篇论文解决的三个问题

2011 年论文把 G-DINA 从一个反应函数扩展成了完整框架：

1. **统一表示**：用 link function 和 design matrix 表示 G-DINA、DINA、DINO、A-CDM、LLM、G-NIDA 与 R-RUM。
2. **统一估计**：先用 MMLE 估计每个项目、每个约化属性模式的答对概率，再变换到不同模型的参数。
3. **逐题比较**：用 Wald 检验判断某道多属性题能否从饱和模型约化成更简洁的 CDM。

框架的计算主线可以写成

\[
\boldsymbol X,Q
\longrightarrow
\widehat{\boldsymbol P}_j
\longrightarrow
\widehat{\boldsymbol\phi}_j
\longrightarrow
R_{jr}\widehat{\boldsymbol\phi}_j
\longrightarrow
\text{item-level model decision}.
\]

其中 \(\widehat{\boldsymbol P}_j\) 是项目 \(j\) 在全部约化属性模式下的成功概率；\(\boldsymbol\phi_j\) 可以是 identity、logit 或 log 标度上的效应参数。

## 推荐阅读顺序

1. [问题与框架全貌](01-question-and-framework.md)
2. [约化属性模式与偏序](02-reduced-patterns.md)
3. [三个 link function](03-link-functions.md)
4. [identity-link G-DINA](04-identity-gdina.md)
5. [DINA、DINO 与 A-CDM](05-special-cases.md)
6. [LLM、G-NIDA 与 R-RUM](06-logit-log-families.md)
7. [MMLE 与 EM](07-mmle.md)
8. [design matrix](08-design-matrix.md)
9. [约化模型与权重矩阵](09-reduced-model-estimation.md)
10. [MLE、不变性与标准误](10-standard-errors.md)
11. [逐题 Wald 检验](11-wald-test.md)
12. [模拟实验](12-simulation.md)
13. [分数减法数据](13-fraction-subtraction.md)
14. [临床数据与勘误](14-clinical-data-and-erratum.md)
15. [代码实现精读](15-code-implementation.md)
16. [两属性项目数值拆解](16-numerical-walkthrough.md)
17. [局限与未来工作](17-limitations-and-future.md)
18. [符号表](18-symbols.md)
19. [总结与后续阅读](19-summary.md)
20. [参考文献](references.md)

## 阅读时要分清的三层

| 层 | 对象 | 作用 |
| --- | --- | --- |
| 概率层 | \(\boldsymbol P_j=\{P(\boldsymbol\alpha^*_{lj})\}\) | 直接描述各约化属性组的成功率 |
| 参数层 | \(\boldsymbol\delta_j,\boldsymbol\lambda_j,\boldsymbol\nu_j\) | 分解主效应和交互效应 |
| 约束层 | \(M_j,R_{jr}\) | 定义具体模型并进行 Wald 检验 |

论文最重要的观念是：同一组成功概率可以换不同坐标表示；模型约化则是在这些坐标或概率之间施加可检验的限制。
