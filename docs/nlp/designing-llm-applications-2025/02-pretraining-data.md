# 预训练数据：从语料规模到数据治理

## 1. 模型学习的是训练分布

自回归语言模型最小化：

\[
\mathcal L(\theta)
=
-\sum_{x\in\mathcal D}
\sum_{t=1}^{|x|}
\log p_\theta(x_t\mid x_{<t}).
\]

数据集 \(\mathcal D\) 决定模型反复看到哪些语言、领域、文体与偏差。模型规模无法弥补关键知识完全缺失，也不能自动识别训练语料中的事实错误。

## 2. 数据流水线

```text
原始来源
  ↓ extraction
可解析文档
  ↓ language / format / quality filtering
候选语料
  ↓ deduplication / PII / safety
清洗语料
  ↓ decontamination
训练语料池
  ↓ mixture weighting / curriculum
训练 batches
```

每一步都改变经验分布。

## 3. 质量过滤

质量分数可以由规则、分类器或更强模型给出：

\[
q(x)=f(
\text{语言},
\text{结构},
\text{重复},
\text{可读性},
\text{来源},
\text{安全}
).
\]

硬阈值直接删除文档；软采样以 \(q(x)\) 调整被选概率。质量模型本身可能偏爱主流语言、正式文体或与评价标准相似的内容，因此需要按领域审计误删。

## 4. 去重

### Exact duplication

用内容 hash 检测完全相同文档。

### Near duplication

通过 n-gram、MinHash 或局部敏感哈希找高度重叠文档。去重可以：

- 降低少数文档被重复记忆；
- 让 token budget 覆盖更多独立信息；
- 降低 train-test contamination；
- 改善 data mixture 的可解释性。

去重太强也可能删掉合法模板、引用或重要重复事实。

## 5. Data contamination

若评价样本或其近似版本进入训练集，测得性能包含记忆成分：

\[
\widehat R_{\mathrm{test}}
=
R_{\mathrm{generalization}}
+B_{\mathrm{contamination}}.
\]

decontamination 需要在 tokenizer、字符串 normalization 和匹配粒度上做选择。只匹配完整文档会漏掉局部题目泄漏；过宽的 n-gram 匹配会误删常见表达。

## 6. Data mixture

多个数据源 \(D_k\) 的采样概率为：

\[
p(x)
=
\sum_{k=1}^{K}
\pi_k p_k(x),
\qquad
\sum_k\pi_k=1.
\]

\(\pi_k\) 不必等于原始数据量占比。高质量书籍、代码或数学语料可以被上采样；大规模噪声网页可以被下采样。

Mixture 选择控制能力，也控制偏差和重复次数。应记录每个 source 的 token 数、epoch 数和训练阶段权重。

## 7. Synthetic data

合成数据适合：

- 补充稀缺任务格式；
- 控制难度与覆盖；
- 生成推理或工具轨迹；
- 构造负例与安全边界；
- 蒸馏强模型行为。

风险包括错误循环放大、风格单一、教师偏差和 benchmark contamination。可靠流程应包含生成、过滤、去重、事实验证和人工抽检。

## 8. PII 与数据治理

删除姓名正则远远不够。PII 可能出现在自由文本、代码、表格和组合字段中。数据治理至少包括：

- 来源授权和许可证；
- PII detection 与复核；
- 删除请求和数据 lineage；
- 高风险领域排除；
- 训练集访问权限；
- 模型记忆与抽取测试。

## 9. 与 CAT 数据的接口

学生作答数据不是普通网页语料。需要考虑：

- FERPA/隐私与机构协议；
- 学生、题目和时间切分，避免同一对象泄漏；
- 低能力群体和语言群体是否被低估；
- 题目曝光与版权；
- 作答轨迹是否保留实时顺序；
- 模拟数据与真实行为的 domain gap。

生成式 CAT 的上限会受到训练轨迹覆盖和反事实缺失共同限制。

