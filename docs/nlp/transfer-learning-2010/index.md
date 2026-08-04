# 迁移学习：Pan & Yang (2010)

**A Survey on Transfer Learning** 是迁移学习的经典综述。迁移思想早于该文；这里选择它，是因为论文给出统一的 domain/task 定义与分类框架，适合回答“BERT 为什么属于迁移学习”。

## 核心定义

一个 domain：

\[
\mathcal D=\{\mathcal X,P(X)\}.
\]

一个 learning task：

\[
\mathcal T=\{\mathcal Y,P(Y\mid X)\}.
\]

迁移学习利用源 \((\mathcal D_S,\mathcal T_S)\) 的知识改善目标预测 \(f_T\)，条件是

\[
\mathcal D_S\ne\mathcal D_T
\quad\text{或}\quad
\mathcal T_S\ne\mathcal T_T.
\]

## 阅读路线

1. [Domain、Task 与迁移定义](01-definitions-taxonomy.md)
2. [三种设置与四类迁移方法](02-settings-methods.md)
3. [负迁移与一个重加权手算](03-negative-transfer-worked-example.md)
4. [与 BERT 预训练—微调的关系](04-bert-connection-conclusion.md)
5. [参考文献](references.md)
