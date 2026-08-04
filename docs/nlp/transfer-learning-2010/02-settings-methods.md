# 三种设置与四类迁移方法

## 1. Inductive transfer

\[
\mathcal T_S\ne\mathcal T_T.
\]

目标域有少量标注，用于学习目标函数。预训练语言模型到情感分类、QA 或 NLI 属于这一大类。

## 2. Transductive transfer

\[
\mathcal T_S=\mathcal T_T,
\qquad
\mathcal D_S\ne\mathcal D_T.
\]

源域有标注、目标域通常无标注。典型情况是 domain adaptation 或 covariate shift。

## 3. Unsupervised transfer

源、目标任务相关但不同，目标任务是聚类、降维或密度估计等无监督任务，双方训练时没有标签。

## 4. 四类“转移什么”

| 类别 | 转移对象 | 典型机制 |
|---|---|---|
| Instance-based | 源样本 | 重加权/选择有用源样本 |
| Feature-representation | 表示 | 学习跨域共享特征 |
| Parameter-transfer | 参数/先验 | 共享或初始化模型参数 |
| Relational-knowledge | 实体关系 | 迁移关系结构 |

BERT 同时体现表示迁移与参数迁移：预训练 encoder 产生通用表示，下游模型由预训练参数初始化并继续更新。

## 5. 三个核心问题

- What to transfer：哪些知识可共享；
- How to transfer：怎样编码和优化；
- When to transfer：什么时候会改善或伤害目标任务。

LoRA 改变的是 how：它用低秩参数承载目标更新；BERT 预训练主要提供 what：上下文化语言表示与参数。
