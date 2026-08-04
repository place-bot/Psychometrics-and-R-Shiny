# Benchmark 污染与 clean subset

## 1. 问题为何比 GPT-2 更严重

GPT-3 的数据和模型规模相对 GPT-2 约扩大两个数量级，Common Crawl 中可能包含公开 benchmark、题目来源网页或其近重复文本。模型不需要看到正式标签，也可能因见过背景段落而获益。

## 2. 训练前过滤

作者尝试搜索 benchmark development/test 与训练数据的 13-gram 重叠，删除碰撞片段及前后 200 字符。过短碎片被丢弃；一篇文档若被切成超过 10 段则整体删除。

后来发现一个 bug 使长文档过滤不完整。由于 175B 重训成本过高，作者没有重新训练，而是进行事后 clean subset 分析。

## 3. Clean example 定义

对每个 benchmark 选择长度 \(N\)，大致取样本词数的第 5 百分位，并限制在 8 到 13 之间；合成短任务可使用更小 n-gram。若样本任何 \(N\)-gram 与完整训练 corpus 碰撞，则标记为 dirty，否则为 clean。

简化写成：

\[
\operatorname{dirty}(x)
=
\mathbb I
\left[
\exists g\in\operatorname{NGram}_N(x):
g\in\mathcal C_{\mathrm{train}}
\right].
\]

然后比较：

\[
\Delta
=
\operatorname{Score}(\mathcal D_{\mathrm{clean}})
-
\operatorname{Score}(\mathcal D_{\mathrm{all}}).
\]

## 4. 总体结果

大多数 benchmark 在 clean subset 上变化很小，污染比例与 performance difference 没有明显相关。作者提出两种解释：

- 保守检测产生大量 false positives；
- 存在文本重叠，但对任务答案帮助有限。

## 5. 重点案例

### 5.1 阅读理解

QuAC、SQuAD2、DROP 超过 90% 样本被初筛标记，但人工检查发现训练语料主要包含 source passage，没有正式问题和答案。对这些任务，见过背景文档与记住答案需要区分。

### 5.2 PIQA

约 29% 样本被标记，clean subset accuracy 绝对下降约 3 个百分点。由于较小模型也有类似下降，作者怀疑 clean/dirty 难度分布差异，但不能严格排除污染，因而给结果加星号。

### 5.3 Winograd

约 45% 被标记；人工检查确认 132 个 schema 出现在训练集中，格式有所不同。clean subset 下降 2.6%，论文给结果加污染标记。

### 5.4 LAMBADA

存在大量真实重叠，但 clean subset 与完整集分数差异在约 0.5% 内。填空格式也阻止了最直接的整段续写记忆，不过不能消除所有影响。

### 5.5 语言建模数据集

GPT-2 用过的四个 Wikipedia LM benchmark 和 CBT 几乎全部出现在 GPT-3 训练数据中，无法构造可信 clean subset，论文因此不报告这些结果。PTB 因年代较早、污染较少，成为主要 LM benchmark。

## 6. Clean subset 也会产生选择偏差

若被互联网转载的题恰好更简单，删除 dirty examples 会留下更难分布：

\[
p(x\mid\mathrm{clean})
\ne
p(x\mid\mathrm{all}).
\]

此时 score 下降可能来自难度变化，不能全归因于记忆。反方向也同样可能。

## 7. 这套分析的价值

论文公开承认过滤 bug、标注可疑结果，并删除无法可信评价的数据集。这建立了大模型评测的重要规范：

- 训练前去重；
- 训练后污染检测；
- 区分 source overlap 与 label leakage；
- 同时报 clean 与 all；
- 对无法裁决的结果明确加注。

它仍是事后近似。开放网页规模下，语义改写、翻译、答案泄漏和训练 corpus 不公开都会限制审计完整性。
