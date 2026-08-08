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

### 五篇核心文献

| 顺序 | 文献 | 与本专题的关系 | 当前进度 |
|---:|---|---|---|
| 1 | [Wise et al. (1991), *A Comparison of Self-Adapted and Computer-Adaptive Tests*](wise-et-al-1991.md) | 让受测者在每一道题前选择难度，并与标准自适应测验直接比较 | **已完成精读** |
| 2 | [Zhu and Fan (1999), *Adjusting Computer Adaptive Test Starting Points to Conserve Item Pool*](zhu-fan-1999.md) | 用自报数学课程和平均成绩预测初始能力，只据此选择起始题，随后恢复标准 CAT | **已完成精读** |
| 3 | [van der Linden (1999), *Empirical Initialization of the Trait Estimator in Adaptive Testing*](van-der-linden-1999.md) | 用测验前已知的背景变量构造个体化初始估计，为自报信息进入 CAT 提供统计框架 | **精读中：引文地图已整理** |
| 4 | [Frans et al. (2023), *Empirical Priors in Polytomous Computerized Adaptive Tests: Risks and Rewards in Clinical Settings*](https://doi.org/10.1177/01466216221124091) | 在多级计分和临床场景中研究经验先验能否缩短测验，以及错误先验会造成什么风险 | 待精读 |
| 5 | [Petersen et al. (2026), *Evaluating the Use of Prior Information to Individualise Start Item Selection for the EORTC CAT Core*](https://doi.org/10.1007/s11136-025-04101-y) | 在欧洲癌症研究与治疗组织（European Organisation for Research and Treatment of Cancer, EORTC）的 CAT 中，外部信息只决定第一题，此后使用原有选题和停止规则；机制上最接近本专题的设计 | 待精读 |

建议阅读顺序不是简单按年份排列。前两篇已经读完；目前用第 3 篇补齐初始化模型的统计理论与引文基础，接下来再读第 4、5 篇，看现代临床 CAT 中的题量收益与风险。

### 第一篇已经读到什么

[A Comparison of Self-Adapted and Computer-Adaptive Tests](wise-et-al-1991.md) 直接比较两种 20 题测验：

- Self-Adapted Testing（SA）：受测者在每题前从六个难度等级中自行选择；
- Computerized Adaptive Testing（CA）：计算机根据此前表现选择下一题；
- 两组都在每题后得到正误反馈。

论文发现 SA 组的平均能力估计更高、测后状态焦虑更低，但用时更长、能力估计误差方差更大。它证明了“受测者掌握的主观信息可能影响测验过程”值得研究，同时也暴露出效度、精度与因果解释上的难题。

### 第二篇已经读到什么

[Adjusting Computer Adaptive Test Starting Points to Conserve Item Pool](zhu-fan-1999.md) 比较共同中等难度起点、平均成绩起点，以及课程与平均成绩综合起点。辅助信息只决定第一题，此后恢复相同的 CAT。

课程与平均成绩综合起点把首题分散到更宽的难度范围，降低了中间题目的集中曝光，并在多数条件下保持与无信息起点接近的能力相关。但它没有稳定缩短可变长度 CAT；在停止标准较宽松的短测验中，平均题量反而多出约一至两题。单独使用平均成绩还因大量 4.0 自报在高难度端形成曝光尖峰，说明错误或堆积的辅助信息可能只是把曝光从题库中间转移到题库尾部。

### 第三篇的引文地图

[Empirical Initialization of the Trait Estimator in Adaptive Testing](van-der-linden-1999.md) 把测验前辅助变量建模为潜在能力的预测变量，并据此构造个体化初始点或完整经验先验。独立笔记按论点整理了它引用的理论、经验研究与算法来源，也标出了哪些结论只是本文的理论动机、二手转引或尚未经过 CAT 对照实验验证。

### 三篇补充文献

| 文献 | 为什么补充阅读 |
|---|---|
| [Revuelta (2004), *Estimating Ability and Item-Selection Strategy in Self-Adapted Testing: A Latent Class Approach*](https://doi.org/10.3102/10769986029004379) | 把受测者的选题策略本身作为潜在类别建模，提醒我们“选择了什么难度”也可能是一类需要分析的数据。 |
| [Wise et al. (2005), *An Investigation of the Effects of Self-Adapted Testing on Examinee Effort and Performance in a Low-Stakes Achievement Test*](https://files.eric.ed.gov/fulltext/ED490205.pdf) | 直接检验低风险测验中的努力与表现，帮助评估“低风险情境下受测者会认真、准确地提供自我信息”这一前提。 |
| [Arieli-Attali et al. (2019), *Understanding Test Takers' Choices in a Self-Adapted Test: A Hidden Markov Modeling of Process Data*](https://doi.org/10.3389/fpsyg.2019.00083) | 使用隐马尔可夫模型分析逐题难度选择怎样随目标条件和作答过程变化，适合为前 \(k\) 题选择数据建立过程模型。 |

三篇补充文献不负责回答“是否缩短测验”这一主问题，而是帮助理解受测者如何选择、低风险是否等于高投入，以及选择策略应不应该进入测量模型。

### 四篇已获取的延伸文献

| 文献 | 在研究路线中的位置 |
|---|---|
| [Frosini et al. (1998), *Performing Automatic Exams*](https://doi.org/10.1016/S0360-1315(98)00042-6) | 先用一段类似自我适应测验（Self-Adapted Testing, SAT）的预考确定起始难度，再进入计算机化自适应测验（Computerized Adaptive Testing, CAT）；架构上非常接近“先由用户信息启动，再交回 CAT”。 |
| [Bass et al. (2026), *Brief Reports: Impact of Informed Starting Value on Longitudinal Computer Adaptive Tests in PROMIS Assessments*](https://doi.org/10.1016/j.apro.2026.100322) | 在患者报告结局测量信息系统（Patient-Reported Outcomes Measurement Information System, PROMIS）的纵向复测中使用 informed starting value，直接考察受测负担、题量与估计误差。 |
| [Chang and Ying (1999), *a-Stratified Multistage Computerized Adaptive Testing*](https://doi.org/10.1177/01466219922031338) | 导师提到的 a-stratified 基线：早期使用低区分度题，后期保留高区分度题，主要解决题库曝光与安全，而不是利用个体信息解决冷启动。 |
| [Pitkin and Vispoel (2001), *Differences Between Self-Adapted and Computerized Adaptive Tests: A Meta-Analysis*](https://doi.org/10.1111/j.1745-3984.2001.tb01125.x) | 汇总早期 Self-Adapted Testing 与 Computerized Adaptive Testing 的比较结果，用来判断允许选择对能力估计与测后焦虑的平均影响。 |

这四篇已经取得全文。Frosini et al. (1998) 和 Bass et al. (2026) 直接补充“如何启动”的证据；Chang and Ying (1999) 是不同机制的基线；Pitkin and Vispoel (2001) 提供整体证据背景。

## 后续阅读要回答的问题

1. 自报信息究竟应当映射为一个点估计，还是一个带不确定性的先验分布？
2. 让受测者选第一题、选前 \(k\) 题，还是只报告自身水平，哪种接口更稳定？
3. 自我评价错误时，标准 CAT 需要多少题才能纠正错误起点？
4. 在相同停止规则下，平均题量、尾部题量、偏差、均方根误差（root mean square error, RMSE）和覆盖率怎样变化？
5. 效率收益是否只出现在极端能力或症状水平的受测者身上？
6. 自主感、焦虑和动机的变化，是否会改变被测构念本身的作答过程？

本专题后续将沿着“全程自主选题 - 个体化起点 - 经验先验 - 仅个体化第一题”的顺序继续整理文献，并把三篇补充文献用于解释选择过程与低风险作答行为。
