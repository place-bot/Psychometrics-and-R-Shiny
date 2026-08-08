# Adaptive Testing with Self-Evaluation

传统的计算机化自适应测验（Computerized Adaptive Testing, CAT）在选择第一道题时很尴尬：系统还没有观察到任何作答，却必须先给出一道题。常见做法是先给受测者一个相同的初始能力值，再选择在该位置最有信息的题。本专题研究另一条路线：**在测验开始时利用受测者对自身状态的判断，为 CAT 提供少量但可能有用的个体信息。**

这里的 self-evaluation 是一个宽泛概念，可以是自报能力或症状水平，也可以是主动选择题目难度。它并不预设受测者一定能够准确评价自己；真正的问题是，这个信号在什么条件下有用，以及用错时会付出什么代价。

## 三类相邻但不同的方法

| 方法 | 受测者提供什么 | 系统怎样使用 | 控制权持续多久 |
|---|---|---|---|
| Self-adapted testing | 每次选择下一题的难度等级 | 按所选等级发题 | 通常贯穿整场测验 |
| Self-informed starting point | 自报水平，或选择开始难度 | 设定初始能力值或第一题 | 只影响开头 |
| Informative prior | 问卷、历史分数或其他辅助变量 | 构造个体化先验分布 | 随作答证据逐渐被更新 |

这三类方法共享一个直觉：受测者或外部资料可能掌握标准 CAT 尚未观察到的信息。但它们不是同一个设计。尤其要区分：**让人选择每一道题**，和**只让人的判断帮助 CAT 起步，随后完全交回标准算法**。

## 本专题的研究主线

我们重点考虑的是第二类及其与第三类的接口：在低风险的心理测量或自适应学习场景中，让受测者在第一题或前 \(k\) 题提供自我评价，然后回到原有 CAT 的能力更新、选题规则和停止规则。

一个最小版本可以写成：

\[
s_i
\longrightarrow
\widehat{\theta}_i^{(0)}
\longrightarrow
\text{前 }k\text{ 题}
\longrightarrow
\text{标准 CAT 更新与选题}
\longrightarrow
SE(\widehat{\theta}_i)\le \varepsilon.
\]

其中，\(s_i\) 表示受测者的自报结果或难度选择，\(\widehat{\theta}_i^{(0)}\) 表示由此得到的初始能力估计，\(SE\) 表示标准误（standard error），\(\varepsilon\) 表示原有的精度停止阈值。核心假设是：如果 \(s_i\) 包含与真实水平有关的信息，CAT 就能更快进入适合该受测者的题目区域，从而以更少的题目达到同等估计精度。

!!! warning "尚未被第一篇论文检验的部分"
    “题量会缩短”是本专题准备检验的假设，不是下面第一篇论文已经得到的结论。Wise et al. (1991) 使用固定 20 题，无法比较停止时间或测验长度。

## 阅读清单

### 方法专题

| 方法 | 独立笔记 | 为什么需要单独掌握 |
|---|---|---|
| Sympson–Hetter（1985）题目曝光控制 | [完整方法笔记：接受概率、模拟标定、信息损失与条件曝光](sympson-hetter-1985.md) | Zhu and Fan（1999）使用的核心曝光控制机制，也是比较“自评起点能否分散题库使用”时必须固定或单独消融的基线。 |

### 八篇核心文献

| 顺序 | 文献 | 与本专题的关系 | 当前进度 |
|---:|---|---|---|
| 1 | [Wise et al. (1991), *A Comparison of Self-Adapted and Computer-Adaptive Tests*](wise-et-al-1991.md) | 让受测者在每一道题前选择难度，并与标准自适应测验直接比较 | **已完成精读** |
| 2 | [Zhu and Fan (1999), *Adjusting Computer Adaptive Test Starting Points to Conserve Item Pool*](zhu-fan-1999.md) | 用自报数学课程和平均成绩预测初始能力，只据此选择起始题，随后恢复标准 CAT | **已完成精读** |
| 3 | [van der Linden (1999), *Empirical Initialization of the Trait Estimator in Adaptive Testing*](https://place-bot.github.io/Psychometrics-and-R-Shiny/cat/adaptive-testing-self-evaluation/van-der-linden-1999/) | 用测验前已知的背景变量构造个体化初始估计，为自报信息进入 CAT 提供统计框架 | **已完成精读** |
| 4 | [Matteucci and Veldkamp (2009), *Computer Adaptive Testing with Empirical Prior Information: A Gibbs Sampler Approach for Ability Estimation*](matteucci-veldkamp-2009.md) | 背景变量构造的个体化经验先验同时进入能力初始化与逐题/最终能力估计；虽然仍用经典最大信息量准则，却已经通过改变当前能力估计改变实际选题路径 | **已完成精读** |
| 5 | [He et al. (2019), *Combining Text Mining of Long Constructed Responses and Item-Based Measures: A Hybrid Test Design to Screen for Posttraumatic Stress Disorder (PTSD)*](he-et-al-2019.md) | 将受测者的创伤与症状 self-narrative 通过文本挖掘转换为个体化先验，再与 PTSD 问卷的 IRT 似然结合；题目却是按固定诊断切点的信息量排成全员相同的顺序，并非个体化实时选题 | **已完成精读** |
| 6 | [Frans et al. (2023), *Empirical Priors in Polytomous Computerized Adaptive Tests: Risks and Rewards in Clinical Settings*](frans-et-al-2023.md) | 在多级计分临床 CAT 中正交操纵先验均值偏差与先验方差，揭示窄 prior 缩短测验的同时也可能造成严重偏差、过早停止或题库耗尽 | **已完成精读** |
| 7 | [Petersen et al. (2026), *Evaluating the Use of Prior Information to Individualise Start Item Selection for the EORTC CAT Core*](petersen-et-al-2026.md) | 用已经完成的另一个生活质量领域预测目标领域位置，只据此选择第一题；第一题后恢复原有 CAT，直接检验轻量个性化首题的效果边界 | **已完成精读** |
| 8 | [Bass et al. (2026), *Brief Reports: Impact of Informed Starting Value on Longitudinal Computer Adaptive Tests in PROMIS Assessments*](bass-et-al-2026.md) | 以第一次 PROMIS CAT 的最终分数构造第二次测量的个体化 prior，并系统改变 prior 标准差，检验小变化、大变化与题库覆盖如何共同决定题量和 RMSE | **已完成精读** |

八篇核心文献已经全部完成精读：第 3 篇补齐初始化模型的统计理论，第 4 篇说明经验先验怎样进入整个逐题估计过程，第 5 篇把辅助信息扩展到心理健康 self-narrative，第 6 篇揭示固定精度 CAT 中先验精度同时制造效率收益与错误先验风险，第 7 篇直接检验只个性化第一题的轻量方案，第 8 篇则说明纵向复测还必须把真实状态变化的不确定性放进 prior。补充文献目前完成 1 篇，下一篇将检验低风险 SAT 中的努力与表现。

### 第一篇已经读到什么

[A Comparison of Self-Adapted and Computer-Adaptive Tests](wise-et-al-1991.md) 直接比较两种 20 题测验：

- Self-Adapted Testing（SA）：受测者在每题前从六个难度等级中自行选择；
- Computerized Adaptive Testing（CA）：计算机根据此前表现选择下一题；
- 两组都在每题后得到正误反馈。

论文发现 SA 组的平均能力估计更高、测后状态焦虑更低，但用时更长、能力估计误差方差更大。它证明了“受测者掌握的主观信息可能影响测验过程”值得研究，同时也暴露出效度、精度与因果解释上的难题。

### 第二篇已经读到什么

[Adjusting Computer Adaptive Test Starting Points to Conserve Item Pool](zhu-fan-1999.md) 比较共同中等难度起点、平均成绩起点，以及课程与平均成绩综合起点。辅助信息只决定第一题，此后恢复相同的 CAT。

课程与平均成绩综合起点把首题分散到更宽的难度范围，降低了中间题目的集中曝光，并在多数条件下保持与无信息起点接近的能力相关。但它没有稳定缩短可变长度 CAT；在停止标准较宽松的短测验中，平均题量反而多出约一至两题。单独使用平均成绩还因大量 4.0 自报在高难度端形成曝光尖峰，说明错误或堆积的辅助信息可能只是把曝光从题库中间转移到题库尾部。

### 第三篇已经读到什么

[Empirical Initialization of the Trait Estimator in Adaptive Testing](van-der-linden-1999.md) 把测验前辅助变量建模为潜在能力的预测变量，并据此构造个体化初始点或完整经验先验。论文不是先估计每个人的 \(\widehat\theta\) 再做普通回归，而是把能力保留为潜变量，从完整逐题作答中联合估计回归系数与先验方差。实际数据示例使用前一测验的对数反应时预测后一词汇测验的能力，但没有重新比较标准 CAT 与个体化 prior CAT 的题量、精度或曝光，因此它是先验构造与估计方法论文，不是 CAT 效率实验。

### 第四篇已经读到什么

[Computer Adaptive Testing with Empirical Prior Information: A Gibbs Sampler Approach for Ability Estimation](matteucci-veldkamp-2009.md) 把背景变量构造的经验先验同时放入 CAT 的初始化和中间/最终能力估计，并在每次更新后继续使用最大信息量选题。因此，“不改选题公式”不等于“不改实际选题路径”。在正确指定的模拟先验下，完整经验先验主要改善了 5 题短测验及极端能力处的估计；只改变起点的半经验条件总体较弱。随着题量增加，优势缩小，而且原表并不支持经验方法在每个能力点的 RMSE 都更低。论文采用固定题长，没有检验同一停止精度下能否减少题量，也没有模拟错误自评、不同先验方差或题目曝光。

### 第五篇已经读到什么

[Combining Text Mining of Long Constructed Responses and Item-Based Measures](he-et-al-2019.md) 让受测者写下创伤经历与症状，通过既有文本分类器得到个人分数，再建立 \(\theta_n\mid y_n\) 的正态先验并与 IRT 问卷似然结合。在 99 人样本中，完整 21 题的分类准确率从 IRT-only 的 0.94 提高到 Hybrid 的 0.97；文本 prior 加 17 道题的平均后验标准误约等于无文本 prior 的完整 21 题。可是 21 道题是在共同诊断切点 \(-0.15\) 处按信息量预先排成同一顺序，prior 没有驱动个性化实时选题；论文也没有报告 17 题条件的分类准确率、覆盖率或错误 prior 风险。

### 第六篇已经读到什么

[Empirical Priors in Polytomous Computerized Adaptive Tests](frans-et-al-2023.md) 使用五级计分临床题库、最大后验估计、最大 Fisher 信息量选题和共同的固定精度停止规则，分别操纵个体化 prior 的均值偏差与方差。仅把无偏 prior 的中心移到真实能力而维持方差为 1，并未明显缩短 CAT；效率收益主要来自更小的先验方差。可是窄而错误的 prior 可能把 CAT 送入题库低信息区，造成长测验或题库耗尽；也可能在高信息区迅速达到标准误阈值，形成“题量很短但估计严重偏”的隐蔽失败。

第二项较现实的模拟用临床医生预先给出的 global score 构造个体化 prior。在 5,000 名模拟受测者中，经验 prior 使 68% 的人题量缩短，中位减少 20%（1 题），但没有带来明显的总体偏差改善。强制最少题数或放宽 prior 可以降低风险，却也会削弱题量收益。这篇因此直接支持我们把 prior 均值误差、先验方差与最少题数分开消融，并同时报告偏差、覆盖率、错误提前停止和题库耗尽，而不能只比较平均题量。

### 第七篇已经读到什么

[Evaluating the Use of Prior Information to Individualise Start Item Selection](petersen-et-al-2026.md) 是目前机制上最接近“只改变第一题”的研究。作者先在 10,084 次癌症患者评估中，用一个已经完成的生活质量领域简单回归预测另一个领域；随后只在预测位置选择目标 CAT 的第一题，第一题以后恢复原有流程。对每个目标领域挑选最佳单一预测领域时，预测-观察相关为 0.31 至 0.72，72% 至 89% 的预测位于观察分数 1 个标准差以内；若跨全部预测领域平均，表现明显较低，不能把摘要中的最佳结果推广到任意领域组合。

CAT 模拟显示，个体化首题的收益主要集中在 1 至 3 题以及远离总体均值的患者；低分区跨领域平均可靠性提高 0.11，达到 4 至 5 题后多数差异消失。固定精度模拟中只有低身体功能条件最多平均减少 1.4 题，其余条件不超过 0.7 题。还要注意，模拟使用的是“真实分数、真实分数正负 5 或 10 分”的受控起点，并没有把实证回归的逐人预测误差端到端送入 CAT。因此它很好地证明首题路由的局部效果，却没有证明真实辅助信息能够普遍大幅缩短测验。

### 第八篇已经读到什么

[Impact of Informed Starting Value on Longitudinal Computer Adaptive Tests in PROMIS Assessments](bass-et-al-2026.md) 使用官方 PROMIS 成人与儿童题库模拟两次纵向 CAT。第一次使用标准 \(N(0,1)\) prior；第二次把第一次最终 EAP 设为 prior 均值，并将 prior 标准差设为 1、0.75、0.5 或 0.25。这里改变的是完整 prior 而不只是第一题，而且数值是标准差：\(SD=0.5\) 对应方差 0.25，\(SD=0.25\) 对应方差 0.0625。

状态变化较小时，\(SD=0.5\) 往往以相同或更少的题量得到最低 RMSE，但总体改善较小且依赖题库覆盖。状态变化较大时，多数成人领域在 \(SD=1\) 最准确；最窄 prior 会把第二次估计强烈拉回旧分数。由于 \(SD=0.25\) 已小于 \(SE<0.3\) 的停止阈值，最少四题规则使 CAT 几乎全部在第四题停止，形成“更短但更不准确”的测验。论文最重要的方法启示是：纵向 prior 方差应同时包含上次计分误差与真实状态变化方差，不能把历史分数的精度直接当作当前状态的不确定性。

### 三篇补充文献

| 文献 | 为什么补充阅读 | 当前进度 |
|---|---|---|
| [Revuelta (2004), *Estimating Ability and Item-Selection Strategy in Self-Adapted Testing: A Latent Class Approach*](revuelta-2004.md) | 把受测者的选题策略本身作为潜在类别建模，提醒我们“选择了什么难度”也可能是一类需要分析的数据。 | **已完成精读** |
| [Wise et al. (2005), *An Investigation of the Effects of Self-Adapted Testing on Examinee Effort and Performance in a Low-Stakes Achievement Test*](https://files.eric.ed.gov/fulltext/ED490205.pdf) | 直接检验低风险测验中的努力与表现，帮助评估“低风险情境下受测者会认真、准确地提供自我信息”这一前提。 | 待精读 |
| [Arieli-Attali et al. (2019), *Understanding Test Takers' Choices in a Self-Adapted Test: A Hidden Markov Modeling of Process Data*](https://doi.org/10.3389/fpsyg.2019.00083) | 使用隐马尔可夫模型分析逐题难度选择怎样随目标条件和作答过程变化，适合为前 \(k\) 题选择数据建立过程模型。 | 待精读 |

三篇补充文献不负责回答“是否缩短测验”这一主问题，而是帮助理解受测者如何选择、低风险是否等于高投入，以及选择策略应不应该进入测量模型。

### 补充文献第一篇已经读到什么

[Estimating Ability and Item-Selection Strategy in Self-Adapted Testing](revuelta-2004.md) 区分了两个经常被混淆的命题。在作者的序贯模型下，未呈现题目的潜在反应满足随机缺失；但若难度选择策略与能力相关，策略参数和能力参数便不可分离，选择机制仍必须进入联合似然。只有在两者独立时，能力才能只根据实际作答的 IRT 似然估计。

72 名高中生完成固定 20 题英语词汇 SAT 的实例显示，受测者存在保持难度、随反馈调节以及容忍失败等不同选择模式，而且前半场改变难度比后半场频繁。把前后半场分开拟合使 AIC 从约 5468 降到 5228，反对“整场策略不变”的假设。论文还发现固定题目路径的渐近标准误约为完整 Bootstrap 标准误的四成，提示验证自评驱动 CAT 时必须重演整条选题与停止过程。它没有检验题量缩短或个体化 prior 的效果。

### 三篇已获取的延伸文献

| 文献 | 在研究路线中的位置 |
|---|---|
| [Frosini et al. (1998), *Performing Automatic Exams*](https://doi.org/10.1016/S0360-1315(98)00042-6) | 先用一段类似自我适应测验（Self-Adapted Testing, SAT）的预考确定起始难度，再进入计算机化自适应测验（Computerized Adaptive Testing, CAT）；架构上非常接近“先由用户信息启动，再交回 CAT”。 |
| [Chang and Ying (1999), *a-Stratified Multistage Computerized Adaptive Testing*](https://doi.org/10.1177/01466219922031338) | 导师提到的 a-stratified 基线：早期使用低区分度题，后期保留高区分度题，主要解决题库曝光与安全，而不是利用个体信息解决冷启动。 |
| [Pitkin and Vispoel (2001), *Differences Between Self-Adapted and Computerized Adaptive Tests: A Meta-Analysis*](https://doi.org/10.1111/j.1745-3984.2001.tb01125.x) | 汇总早期 Self-Adapted Testing 与 Computerized Adaptive Testing 的比较结果，用来判断允许选择对能力估计与测后焦虑的平均影响。 |

这三篇已经取得全文。Frosini et al. (1998) 直接补充“如何启动”的证据；Chang and Ying (1999) 是不同机制的基线；Pitkin and Vispoel (2001) 提供整体证据背景。Bass et al. (2026) 因为直接检验纵向 CAT 的 informed starting value，已经移入核心文献。

## 后续阅读要回答的问题

1. 自报信息究竟应当映射为一个点估计，还是一个带不确定性的先验分布？
2. 让受测者选第一题、选前 \(k\) 题，还是只报告自身水平，哪种接口更稳定？
3. 自我评价错误时，标准 CAT 需要多少题才能纠正错误起点？
4. 在相同停止规则下，平均题量、尾部题量、偏差、均方根误差（root mean square error, RMSE）和覆盖率怎样变化？
5. 效率收益是否只出现在极端能力或症状水平的受测者身上？
6. 自主感、焦虑和动机的变化，是否会改变被测构念本身的作答过程？

本专题后续将继续沿着“全程自主选题 - 个体化起点 - 经验先验 - 仅个体化第一题”的顺序整理文献。Revuelta（2004）已经补上选择过程的潜在类别模型；下一步用 Wise 等人（2005）检验低风险是否真的带来足够努力，再用 Arieli-Attali 等人（2019）的动态模型解释策略怎样随题序改变。
