# LoRA：大语言模型的低秩适配

本专题精读 Hu et al. 的 **LoRA: Low-Rank Adaptation of Large Language Models**，正式发表于 ICLR 2022。

## 核心公式

对预训练权重

\[
\mathbf W_0\in\mathbb R^{d\times k},
\]

冻结 \(\mathbf W_0\)，把任务更新写成

\[
\Delta\mathbf W=\mathbf B\mathbf A,
\qquad
\mathbf B\in\mathbb R^{d\times r},
\quad
\mathbf A\in\mathbb R^{r\times k},
\quad
r\ll\min(d,k).
\]

前向传播：

\[
\mathbf h
=
\mathbf W_0\mathbf x
+
\frac{\alpha}{r}
\mathbf B\mathbf A\mathbf x.
\]

## 文献身份

| 项目 | 信息 |
|---|---|
| 作者 | Edward J. Hu、Yelong Shen 等 |
| 发表 | ICLR 2022 |
| 正式页面 | [OpenReview](https://openreview.net/forum?id=nZeVKeeFYf9) |
| arXiv | [2106.09685](https://arxiv.org/abs/2106.09685) |
| 官方代码 | [microsoft/LoRA](https://github.com/microsoft/LoRA) |

## 阅读路线

1. [全量微调的问题与 LoRA 创新](01-problem-and-contributions.md)
2. [低秩更新的线性代数](02-low-rank-math.md)
3. [参数量、显存与训练成本](03-parameter-memory-compute.md)
4. [Transformer 中改哪些矩阵](04-target-modules.md)
5. [初始化、缩放与 rank](05-initialization-scaling-rank.md)
6. [训练、保存、合并与任务切换](06-training-merge-deployment.md)
7. [完整手算](07-worked-example.md)
8. [与 FT、Adapter、Prefix、BitFit 比较](08-method-comparison.md)
9. [实验设计与结果](09-experiments-results.md)
10. [低秩更新分析](10-rank-analysis.md)
11. [`loralib` 代码精读与从零实现](11-code-reading-implementation.md)
12. [局限、现代扩展与结论](12-limitations-extensions-conclusion.md)
13. [参考文献](references.md)

LoRA 的理解重点是：它约束任务造成的**权重变化**具有低秩结构，没有把预训练权重本身近似成低秩矩阵。
