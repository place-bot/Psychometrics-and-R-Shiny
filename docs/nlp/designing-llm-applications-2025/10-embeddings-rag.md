# Embedding、Chunking 与 RAG

## 1. Embedding

编码器把文本映射到向量：

\[
e(x)\in\mathbb R^d.
\]

常用 cosine similarity：

\[
\operatorname{cos}(q,d)
=
\frac{e(q)^\top e(d)}
{\|e(q)\|\|e(d)\|}.
\]

语义相似不等于事实支持。Embedding 用于候选召回，仍需 reranking 和生成验证。

## 2. Embedding fine-tuning

对 query、positive、negative 训练对比目标：

\[
\mathcal L_i
=
-\log
\frac{\exp(s(q_i,d_i^+)/\tau)}
{\exp(s(q_i,d_i^+)/\tau)+
\sum_j\exp(s(q_i,d_{ij}^-)/\tau)}.
\]

Hard negatives 对领域检索尤其重要。

## 3. Chunking

| 方法 | 优势 | 风险 |
|---|---|---|
| Fixed window | 简单、稳定 | 截断语义单位 |
| Sliding window | 保留边界信息 | 重复与索引膨胀 |
| Metadata-aware | 保留章节/题号 | 依赖文档结构 |
| Layout-aware | 处理表格与 PDF | 解析复杂 |
| Semantic | 更符合主题 | 成本高、边界不稳定 |
| Late chunking | 利用长上下文表征后再切 | 模型与实现要求更高 |

## 4. RAG 六阶段

```text
Rewrite
→ Retrieve
→ Rerank
→ Refine
→ Insert
→ Generate
```

每阶段都有独立误差：查询改写偏离、召回缺失、排序错误、文档污染、context 过长和生成不忠实。

## 5. 检索指标

\[
\operatorname{Recall@k}
=
\frac{\text{top-k 中相关文档数}}
{\text{全部相关文档数}}.
\]

生成阶段还要评价引用 precision、claim support、拒答和答案完整性。

## 6. RAG、Long Context 与 Fine-tuning

| 方法 | 更适合解决 |
|---|---|
| RAG | 外部、可更新、需引用的知识 |
| Long context | 本次请求已有的大量材料 |
| Fine-tuning | 稳定行为、格式、风格与领域决策 |

三者可以组合。RAG 负责取证，long context 负责综合，fine-tuning 负责行为。

## 7. Memory 与 RAG

对话记忆可视为私人检索库：

```text
历史交互
→ 结构化 / embedding
→ 权限与时间过滤
→ 检索相关 memory
→ 放入本轮 context
```

长期记忆需有用户可见的删除和纠错机制。

## 8. CAT 题库 RAG

检索对象可以包含题干、知识点、项目参数、曝光、敌题关系和解题依据。向量相似度只负责语义候选，最终选题还要满足测量信息、内容蓝图、可用题库和曝光约束。

