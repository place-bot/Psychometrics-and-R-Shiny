# He 等人（2019）：自我叙事怎样变成 PTSD 测量的个体化先验

## 文献身份

> He, Q., Veldkamp, B. P., Glas, C. A. W., & van den Berg, S. M. (2019). Combining text mining of long constructed responses and item-based measures: A hybrid test design to screen for posttraumatic stress disorder (PTSD). *Frontiers in Psychology, 10*, 2358. [DOI](https://doi.org/10.3389/fpsyg.2019.02358)

- 研究类型：真实数据方法研究
- 测量目标：创伤后应激障碍（posttraumatic stress disorder, PTSD）潜在严重程度与筛查分类
- 辅助信息：受测者自己撰写的创伤经历与症状叙事
- 核心模型：文本分类分数 \(\rightarrow\) 个体化正态 prior \(\rightarrow\) 二参数 Logistic IRT 后验
- 关键结果：21 题分类准确率由 0.94 提高到 0.97；平均后验标准误曲线显示 17 题加文本 prior 与 21 题不加 prior 接近

!!! abstract "一句话结论"
    这篇论文证明了“受测者自己产生的非结构化文本可以被转换为心理测量 prior”已有直接先例；但它的题目顺序是在统一诊断切点处预先排好的，对所有人完全相同，因此不是文本 prior 驱动的个性化 CAT 选题。

!!! warning "最容易读错的地方"
    作者把按题目信息量逐题加入称为 adaptive，但这里的信息量始终计算在共同诊断切点 \(\theta_c=-0.15\)，而不是每个人当前的后验位置。所有受测者接受相同的题目顺序。真正个体化的是能力 prior 与后验估计，不是题目选择。

## 1. 研究想解决什么问题

研究者希望把两类信息放进同一 PTSD 筛查流程：

1. **非结构化信息：**受测者自由书写的创伤经历与相关症状；
2. **结构化信息：**21 道 PTSD 症状二分题。

他们提出两个问题：

- 文本与题目反应结合后，能否比单独使用问卷更准确地区分 PTSD 与非 PTSD？
- 文本能否充当一种 routing information，使较短的题目序列达到完整问卷相近的估计精度？

因此，这不是传统意义上“先问一句你有多焦虑”的自评，而是：

\[
\text{受测者自我叙事}
\longrightarrow
\text{机器学习文本分数}
\longrightarrow
p(\theta\mid\text{文本})
\longrightarrow
\text{IRT 后验}.
\]

## 2. 样本、参考诊断与两类作答

最初从一个面向心理健康问题人群的网络论坛招募 105 名创伤幸存者。排除 2 名未经历列出的创伤事件者与 4 名缺少叙事者后，最终样本为：

\[
N=99,
\]

其中：

- PTSD：34 人；
- 非 PTSD：65 人；
- 年龄范围：19 至 63 岁，平均 30.06 岁，标准差 11.30；
- 女性占 78.4%；
- 超过 90% 具有大学或更高教育背景。

受测者先报告自己是否曾由精神科医生通过结构化访谈诊断为 PTSD，论文随后把这一标签当作分类比较的 true standard。需要注意：本研究没有重新对 99 人实施一场独立的临床诊断；参考标签来自受测者对既往专业诊断的报告。

### 自我叙事

受测者被要求描述创伤事件及其症状，建议长度超过 150 词。

### 21 道结构化题目

题目来自美国国家共病调查复测（National Comorbidity Survey Replication, NCS-R）的 PTSD 筛查部分，与《精神障碍诊断与统计手册》第四版（Diagnostic and Statistical Manual of Mental Disorders, Fourth Edition, DSM-IV）的症状标准对应，采用“是/否”二分作答。

题目参数并非在当前 99 人上重新标定，而是来自先前 NCS-R 样本：

\[
N_{\mathrm{calibration}}=880.
\]

这一点是设计的优点：当前混合模型使用外部标定的固定题目参数，没有用同一小样本同时重标题目。

## 3. Approach 1：只有 IRT 问卷

作者此前比较过 Rasch 模型、单维二参数 Logistic 模型（two-parameter logistic model, 2PLM）和三维模型。似然比检验更偏向三维模型，但 item-oriented Lagrange multiplier 检验显示单维 2PLM 与多维模型均没有显著题目失配，而且效应量相近。出于简约性，最终采用单维 2PLM。

对题目 \(i\) 与受测者 \(n\)：

\[
P(X_{ni}=1\mid\theta_n)
=
\frac{
\exp\{\alpha_i(\theta_n-\beta_i)\}
}{
1+\exp\{\alpha_i(\theta_n-\beta_i)\}
}.
\]

其中 \(\theta_n\) 表示 PTSD 潜在严重程度，\(\alpha_i\) 是区分度，\(\beta_i\) 是症状严重程度位置。

21 道题的外部标定参数范围为：

- \(\alpha_i\in[0.78,1.86]\)，平均约 1.32；
- \(\beta_i\in[-4.45,1.22]\)，平均约 \(-0.99\)。

IRT-only 条件使用期望后验估计（expected a posteriori, EAP），并假定标准正态能力分布。

## 4. Approach 2：只有文本分类

### 文本模型不是在当前 99 人上从头训练的

论文沿用 He 等人早期研究建立的 product score model（PSM）。原始训练材料包括 300 篇自我叙事，其中 PTSD 与非 PTSD 各 150 篇。当前研究使用此前筛选出的 1,000 个 unigram 特征及已经确定的文本处理流程。

预处理包括：

- 去除数字、标点、停用词和常见缩写；
- 使用 Porter stemming 归一化词形；
- 计算输入叙事中的 unigram 特征。

### Product score model 怎样计分

设 \(C_1\) 为 PTSD 文本语料，\(C_2\) 为非 PTSD 语料。对输入文本中出现的关键词，PSM 分别计算：

\[
S_1
=
P(C_1)
\prod_{w=1}^{k}
\frac{u_w+a}{\operatorname{len}(C_1)},
\]

\[
S_2
=
P(C_2)
\prod_{w=1}^{k}
\frac{v_w+a}{\operatorname{len}(C_2)},
\]

其中 \(u_w\) 与 \(v_w\) 是关键词 \(w\) 在两个语料中的频数，平滑常数设为 \(a=0.5\)。

个人文本分数定义为：

\[
y_n
=
\log\frac{S_1}{S_2}.
\]

当 \(y_n>0\) 时，文本模型分类为 PTSD；否则分类为非 PTSD。为了与 IRT 的标准正态尺度衔接，当前样本的文本分数再被标准化。

!!! note "这是什么意义上的‘自我信息’"
    信息确实由受测者本人产生，但最终进入模型的不是其显式自我评价，而是监督学习算法从叙事用词中提取的风险分数。因此它证明的是“self-generated data 可以形成 prior”，而不是“受测者能够准确选择自己的能力或症状等级”。

## 5. Approach 3：文本分数变成个体化 prior

作者建立潜在回归：

\[
\theta_n
=
b_0+b_1y_n+\varepsilon_n,
\qquad
\varepsilon_n\sim N(0,\sigma^2).
\]

于是：

\[
\theta_n\mid y_n
\sim
N(b_0+b_1y_n,\sigma^2).
\]

它作为 IRT 的个体化 prior：

\[
p(\theta_n\mid\mathbf x_n,y_n)
\propto
p(\mathbf x_n\mid\theta_n,\alpha,\beta)
g(\theta_n\mid y_n).
\]

在当前 99 人数据中，估计得到：

\[
\widehat b_0=-0.41,
\qquad
\widehat b_1=1.44,
\qquad
\widehat\sigma^2=3.57.
\]

因此：

\[
\theta_n\mid y_n
\sim
N(-0.41+1.44y_n,3.57).
\]

先验标准差约为：

\[
\sqrt{3.57}\approx1.89,
\]

所以它并不是特别狭窄的强先验。文本主要移动个人先验中心，同时保留相当大的不确定性。

后验通过 WinBUGS 估计，每人运行 5,000 次 Markov chain Monte Carlo（MCMC）迭代，前 1,000 次作为 burn-in。论文没有报告多链收敛诊断、\(\widehat R\) 或有效样本量。

## 6. 所谓 adaptive item administration 到底是什么

作者采用此前在 \(N=880\) 的 NCS-R 样本上确定的诊断切点：

\[
\theta_c=-0.15.
\]

然后对每道题计算该共同切点处的信息量：

\[
I_i(\theta_c)
=
\alpha_i^2
P_i(\theta_c)
\{1-P_i(\theta_c)\},
\]

再把 21 道题按 \(I_i(\theta_c)\) 从高到低排成一个固定序列。第一题为 C6，随后是 B5、C4、B3 等，直到全部 21 题。

研究比较：

\[
\text{前 }k\text{ 道固定排序题},
\qquad
k=1,\ldots,21,
\]

在“有文本 prior”与“无文本 prior”两种估计方式下的平均后验标准误。

### 为什么这不是个性化 CAT

| 真正的个性化 CAT | He 等人（2019） |
|---|---|
| 在个人当前 \(\widehat\theta_{n,k}\) 或后验上计算选题目标 | 始终在共同切点 \(-0.15\) 计算信息量 |
| 不同人的早期反应可能产生不同下一题 | 所有人使用同一预排序 |
| prior 可以改变实际题目序列 | prior 只改变后验估计，不改变题目顺序 |
| 每一步重新选择剩余最优题 | 只是在固定序列上逐渐增加前缀长度 |

它更准确的名称是：**由诊断切点优化的固定短表序列 + 个体化文本 prior**。

## 7. 三种方法的分类结果

论文比较：

1. IRT-only：21 道题；
2. Text-only：PSM 文本分类；
3. Hybrid：文本 prior + 21 道题的 IRT 后验。

### 三类分数之间的相关

| 两种分数 | 相关 |
|---|---:|
| IRT 与 Text | 0.56 |
| IRT 与 Hybrid | 0.99 |
| Text 与 Hybrid | 0.62 |

Hybrid 与 IRT 的相关高达 0.99，说明使用完整 21 题时，混合分数仍主要由结构化题目决定；文本提供的是小幅但可能有用的修正。

### 分类表现

| 方法 | Accuracy | Sensitivity | Specificity | PPV | NPV |
|---|---:|---:|---:|---:|---:|
| IRT-only | 0.94 | 1.00 | 0.92 | 0.87 | 1.00 |
| Text-only | 0.84 | 1.00 | 0.77 | 0.69 | 1.00 |
| Hybrid | 0.97 | 1.00 | 0.95 | 0.92 | 1.00 |

其中 PPV 与 NPV 分别是阳性预测值（positive predictive value）与阴性预测值（negative predictive value）。

样本中：

- IRT-only 错分 6 人；
- Hybrid 错分 3 人。

因此作者把误分类人数下降解释为 50% reduction。这个相对百分比听起来很大，但绝对差异只有 3 人，且总样本只有 99 人，不能把它当作稳定的外部效度结论。

## 8. “少 4 题”的证据是怎样得到的

随着固定序列逐题增加，论文报告平均后验标准误：

- 无文本 prior：约从第 1 题的 1.6 降到第 21 题的 0.68；
- 有文本 prior：约从第 1 题的 1.4 降到第 21 题的 0.65。

两条曲线差异从约 0.20 缩小到约 0.03，符合“题目越多，prior 相对影响越弱”的规律。

作者画出无 prior、21 题条件的平均标准误水平，并发现它与“有 prior”曲线大约在 17 题相交。因此提出：

\[
17\text{ 题 + text prior}
\approx
21\text{ 题 + no text prior}
\]

可以少 4 题而维持相近精度。

!!! warning "这里的‘相同精度’只是平均后验标准误相近"
    论文没有报告 17 题 Hybrid 的 accuracy、sensitivity、specificity、PPV 或 NPV，也没有比较 bias、RMSE、区间覆盖率或个体层面的停止结果。因此“少 4 题且不损失准确率”比原始证据更强；更严谨的说法是“17 题 Hybrid 的平均后验标准误接近 21 题 IRT-only”。

## 9. 哪些证据比较扎实，哪些需要保留

### 比较扎实的部分

- 题目参数来自独立的 \(N=880\) 样本；
- 文本分类器的关键词体系来自更早的独立语料，而非在当前 99 人上从零训练；
- 同一批 99 人同时提供叙事与题目反应，使两种数据能够在个体层面结合；
- 论文明确给出 prior 回归、分类指标和逐题平均标准误曲线。

### 需要保留的部分

1. **样本很小且不具代表性。**只有 99 人，多数为女性且教育程度很高，来自心理健康网络论坛。
2. **参考标签不是本研究重新实施的临床诊断。**受测者报告其既往精神科诊断，论文再把它作为 true standard。
3. **Hybrid mapping 与效果评估使用同一 99 人。**文本分类器来自外部研究，但 \(b_0,b_1,\sigma^2\) 在当前样本估计，分类与标准误也在同一样本报告，没有交叉验证或独立验证集。
4. **加入 prior 后后验标准误下降具有模型内成分。**额外信息必然增加模型中的精度；真正关键的是该 prior 在新样本中是否校准正确，论文没有报告覆盖率。
5. **没有错误 prior 实验。**文本误判、语言风格差异、教育差异或刻意隐瞒会造成什么后果，没有被检验。
6. **省题不等于省总负担。**受测者还要撰写至少约 150 词的敏感叙事；作者自己也承认需要把写作时间纳入成本效益。
7. **没有题目曝光分析。**所有人使用同一排序，反而可能使最前面的几道题高度曝光。

## 10. 论文真正证明了什么

它直接支持：

1. 受测者自产生的长文本能够通过监督文本模型转成个人分数；
2. 该分数可以通过潜在回归构造成 IRT 能力的个体化经验 prior；
3. 在当前 99 人样本中，文本 prior 与完整问卷结合后，误分类人数由 6 人降到 3 人；
4. 文本 prior 对平均后验标准误的影响在题目较少时更明显；
5. 17 题 Hybrid 的平均后验标准误与 21 题 IRT-only 接近。

它没有直接证明：

- 自报一个症状等级也能达到同样效果；
- 文本 prior 能够驱动个性化 CAT 选题；
- 17 题 Hybrid 的分类准确率与完整 21 题相同；
- 新受测者或其他语言、教育和性别人群中仍有相同收益；
- 错误或过强的文本 prior 不会造成漏诊；
- 该方法减少总完成时间或总心理负担；
- 该方法已经解决题目曝光问题。

## 11. 对我们研究新颖性的影响

这篇论文使下列新颖性主张不成立：

> 首次把受测者自己产生的信息转换成心理测量中的个体化 prior。

因为它已经完成：

\[
\text{self-narrative}
\longrightarrow
y_n
\longrightarrow
N(b_0+b_1y_n,\sigma^2)
\longrightarrow
p(\theta_n\mid\mathbf x_n,y_n).
\]

但它并没有完成：

\[
p(\theta_n\mid\mathbf x_{n,1:k},y_n)
\longrightarrow
\text{下一题的个性化选择}.
\]

因此仍可研究：

- 用户显式自评或难度选择，而不是 NLP 风险分数；
- prior 同时驱动真正的逐人选题；
- 不同 prior variance 下的收益与风险；
- prior 与低 \(a\) 起步、\(b\)-matching 和首题随机化怎样组合；
- 同一精度停止规则下的真实题量分布；
- 错误 prior、漏诊风险、覆盖率与条件曝光。

!!! important "最准确的新颖性表述"
    可能的贡献不再是“把 self-generated information 放进 prior”，而是“把受测者的自评信号、可校准的先验强度、真正个性化的早期选题和曝光保护放进一个可消融、可检验错误先验的 CAT 框架”。

## 12. 对实验设计的直接启示

### 训练映射必须与效果评估分开

如果我们用自评 \(s_i\) 构造：

\[
\theta_i\mid s_i
\sim
N(\mu(s_i),\tau^2(s_i)),
\]

就不能在同一批人上既拟合 \(\mu(\cdot),\tau^2(\cdot)\)，又把 CAT 收益当作外部表现。至少应采用：

- 独立训练集与测试集；或
- cross-fitting / nested cross-validation；或
- 在独立样本上固定 prior mapping 后再做 CAT 模拟。

### “省题”必须使用真正的 stopping rule

不能只比较平均后验标准误曲线的交点。应逐人运行：

\[
\operatorname{Var}(\theta_i\mid\mathcal D_{i,t})
\leq
\varepsilon,
\]

并报告平均题量、95% 分位题量、错误提前停止率、bias、RMSE 与覆盖率。

### 选题个性化要单独证明

应明确比较：

1. 所有人按同一诊断切点排序；
2. 在个人当前后验位置最大信息量选题；
3. 在与个人后验匹配的 \(b\) 区域内随机选择；
4. 加入 \(a\)-stratified 或后验方差门控。

这样才能区分：收益来自 prior 本身、固定短表排序，还是真正的个性化题目路径。

### 总负担不应只数题目

如果自评或叙事需要额外时间，总负担应写成：

\[
T_{\mathrm{total}}
=
T_{\mathrm{self\ info}}
+
T_{\mathrm{items}}.
\]

减少 4 道题并不自动意味着总体更快、更轻松。

## 13. 可以安全写进论文的中文转述

### 受测者自产信息进入 prior

> He 等人（2019）将受测者的创伤自我叙事转换为文本分数，再通过潜在回归构造 PTSD 潜在特质的个体化正态先验，并与 IRT 问卷似然结合。

### 分类表现

> 在该研究的 99 人样本中，完整 21 题问卷的分类准确率为 0.94，加入文本 prior 后为 0.97；由于差异对应 6 人与 3 人被误分类，仍需在独立大样本中验证。

### 题量结果

> 文本 prior 加 17 道预排序题的平均后验标准误，约等于无文本 prior 时完整 21 题的平均后验标准误；论文没有报告 17 题条件下的分类准确率或覆盖率（He et al., 2019）。

### 选题边界

> 该研究按共同诊断切点处的信息量为所有人预先确定同一题目顺序，文本 prior 并未参与个体化实时选题，因此不属于 prior-driven CAT item selection（He et al., 2019）。

## 14. 精读后的结论

He 等人（2019）是“受测者自产生信息 \(\rightarrow\) 个体化 prior”的直接先例，也是本专题必须承认的邻近工作。但它把个性化限制在估计层面：题目仍然按照全体共用的诊断切点统一排序。

对我们最重要的启发是：**外部信号进入 prior、prior 改善短测验精度、prior 驱动个性化选题，是三个不同层次的主张，必须分别设置消融条件验证。**

---

**专题导航：**[返回阅读清单](index.md) · [上一篇：Matteucci 与 Veldkamp（2009）](matteucci-veldkamp-2009.md)
