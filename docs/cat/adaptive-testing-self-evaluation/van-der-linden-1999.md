# van der Linden（1999）：个体化经验初始化完整精读笔记

## 文献身份

> van der Linden, W. J. (1999). Empirical initialization of the trait (θ) estimator in adaptive testing. *Applied Psychological Measurement, 23*(1), 21–29. [https://doi.org/10.1177/01466219922031149](https://doi.org/10.1177/01466219922031149)

- 研究类型：统计方法论文，附一个实际数据示例
- 核心问题：如何把测验前已经掌握的背景信息转化为 CAT 的个体化初始点或经验先验
- 核心模型：潜在回归（latent regression）加经验贝叶斯初始化
- 实例中的辅助信息：前一项测验的总作答时间，而不是受测者自评

!!! abstract "这篇论文到底完成了什么"
    van der Linden（1999）提出了一套从“测验前辅助变量 + 已校准题目的逐题作答”直接估计个体化初始能力分布的方法。本页依次整理研究动机、引文证据、潜在回归、EM 估计、实际数据示例、CAT 中的两种用法及证据边界，并说明它对自评信息进入 CAT 的直接启示。

!!! important "全篇最关键的观点：点估计可忽略，不等于误差可忽略"
    Mislevy and Wu（1988）区分了两个问题。对于一次已经完成的 CAT，如果只关心这名受测者实际得到的最大似然（maximum likelihood, ML）能力点估计，在满足可忽略性条件时，可以不把“系统为何选择这些题”的概率另外乘入似然：

    \[
    \widehat\theta_{\mathrm{ML}}
    =
    \arg\max_\theta
    \prod_{t=1}^{T}
    P(U_t=u_t\mid\theta,J_t).
    \]

    这里绝对不能忽略实际施测的题目 \(J_t\) 及其题目参数；能够忽略的是选题机制本身的概率，例如 \(P(J_t\mid J_{1:t-1},U_{1:t-1})\)。选到难题往往只是先前答对的算法结果，并不是独立于先前作答的第二份能力证据。

    但是，如果关心 \(\widehat\theta\) 在重复施测中的抽样分布——包括标准误、偏差、方差、均方根误差与置信区间覆盖率——就不能忽略选题与停止机制。因为不同的早期作答会产生不同题目路径、信息量和测验长度。

    **对本专题的直接含义：**如果自评只决定第一题、最终采用 ML 计分，自评不必作为一个额外加分项进入最终分数；如果自评被构造成 \(p(\theta\mid X)\) 并用于 Bayesian 更新，它就已经正式进入能力推断，不能再援引这条 ML 结论说“自评被忽略”。

## 1. 先分清：哪些是本文贡献，哪些是前人证据

### van der Linden（1999）自己的主要贡献

论文假设背景变量向量为 \(X=(X_1,\ldots,X_P)\)，并建立潜在回归模型：

\[
\theta
=
\beta_0+\beta_1X_1+\cdots+\beta_PX_P+\varepsilon,
\qquad
\varepsilon\sim N(0,\sigma^2).
\]

因此，对于背景信息为 \(X=x\) 的受测者：

\[
\theta\mid X=x
\sim
N(x^\top\beta,\sigma^2).
\]

这一区分直接对应两种 CAT 初始化方式：

1. **只需要初始点时**，令 \(\widehat\theta^{(0)}=x^\top\widehat\beta\)，据此选择第一题；
2. **使用 Bayesian CAT 时**，把完整的 \(N(x^\top\widehat\beta,\widehat\sigma^2)\) 作为个体化经验先验，背景信息会通过后验更新持续影响后续估计与选题。

论文进一步把 Rigdon and Tsutakawa（1983）的 EM 思路改写到已校准二参数 Logistic 模型（two-parameter logistic model, 2PLM）与稀疏 CAT 作答数据中，直接估计 \(\beta\) 和 \(\sigma^2\)。这样可以避免先估计每个人的 \(\widehat\theta\)，再对带测量误差的 \(\widehat\theta\) 做普通回归。

### 不是本文直接检验的结论

本文没有设置标准 CAT 对照条件，也没有模拟或实测比较题量、均方根误差、覆盖率与曝光率。因此它**没有直接证明**：

- 个体化初始化必然缩短 CAT；
- 自报信息能够准确预测 \(\theta\)；
- 个体化先验一定优于标准正态先验；
- 相同起点造成的曝光问题已经被本文的实例解决；
- 使用背景信息在所有测验情境中都公平。

这些是论文提出的理论理由、统计方法或后续需要检验的研究假设，不能写成本文已经获得的效果结论。

## 2. 一页式引文证据地图

| van der Linden（1999）使用的观点 | 主要引文 | 引文实际承担的作用 | 后续引用强度 |
|---|---|---|---|
| 传统线性测验可在预期能力区间优化测验信息 | Birnbaum（1968） | 项目反应理论（Item Response Theory, IRT）信息函数与测验组卷基础 | 背景理论 |
| CAT 根据当前能力估计逐题匹配题目 | Wainer（1990）；Thissen and Mislevy（1990） | CAT 的最大信息量与 Bayesian 选题框架 | 背景理论 |
| 最大似然与 Bayesian 估计在一定条件下可收敛到真实能力 | Chang and Ying（1996）；Gelman et al.（1995） | 支撑渐近收敛，而不是保证短测验中快速或单调收敛 | 有条件的理论支持 |
| 实际 CAT 中可能存在大量内容与题目依赖约束 | van der Linden and Reese（1998） | 说明约束 CAT 的现实规模；其 LSAT 示例包含大量约束 | 直接方法与实例支持 |
| 短的自适应分测验可借用早期分测验信息改善后续初始化 | Brown and Weiss（1977）；Gialluca and Weiss（1979） | 与“用已有个体信息预测后续起点”最接近的早期应用 | 直接前驱证据 |
| 从共同初始值出发会使起点附近题目承受集中曝光 | van der Linden（1999）的理论论证；Sympson and Hetter（1985）提供控制方法 | 本文给出机制推论，但没有在实例中直接比较曝光；经验检验可另引 Zhu and Fan（1999） | 本文可引作理论动机，不宜写成其经验结果 |
| 直接曝光控制可能牺牲统计信息 | Thomasson（1995），经 van der Linden（1999）转引 | 报告特定模拟中的约 15% 与最高约 40% 信息损失 | 二手、情境依赖证据 |
| 辅助信息可进入 IRT 参数与群体分布估计 | Mislevy（1988）；Mislevy and Sheehan（1989）；Sheehan and Mislevy（1990）；Mislevy et al.（1992） | 证明 collateral information 在 IRT 中已有统计传统 | 相邻问题的方法基础 |
| 自适应选题机制在特定目标下可以忽略 | Little and Rubin（1987）；Mislevy and Wu（1988） | 区分点估计的 realized value 与抽样分布、标准误 | 技术性、有边界的支持 |
| 可用显变量预测潜在能力 | Zwinderman（1991, 1997） | manifest predictors 潜在回归模型；当 \(a_i=1\) 时对应广义 Rasch 模型 | 本文模型的直接统计基础 |
| 可用 EM 从潜在特质模型直接估计参数 | Rigdon and Tsutakawa（1983） | 本文 EM 推导的算法来源 | 直接计算基础 |
| 转换变量、非线性项仍可保持参数线性 | Neter et al.（1990） | 回归建模与变量变换依据 | 通用统计背景 |
| 数值积分可采用 Gauss–Hermite quadrature | Ralston and Rabinowitz（1983） | 本文计算积分的方法来源 | 数值计算背景 |
| 前一测验反应时可能预测后一测验语言能力 | Schoonman（1989） | 提供本文 \(N=306\) 的实例数据与朴素回归比较 | 本文实例的数据来源 |
| Bayesian CAT 可采用不同的选题目标 | van der Linden（1998） | 比较最大后验信息、最小期望后验方差等选题标准 | 直接方法扩展 |

## 3. CAT 选题与收敛：这些引文到底说明了什么

### Birnbaum（1968）：为什么题目可以匹配能力位置

Birnbaum 的章节是题目信息函数的经典来源。它支撑的基本思想是：不同题目在 \(\theta\) 尺度上的信息峰值不同，传统线性测验可以选择一组题，使测验信息在目标人群预计出现的能力区间内较高。

可用于论证：**题目参数分离以后，可以依据受测者预计所处的能力区域选择题目。**

它不直接讨论个体化先验，也不检验背景变量能否预测能力。

### Wainer（1990）与 Thissen and Mislevy（1990）：CAT 如何逐题运行

Wainer 编辑的 *Computerized Adaptive Testing: A Primer* 提供 CAT 的总体框架；其中 Thissen and Mislevy 的 “Testing Algorithms” 章节讨论最大似然与 Bayesian 测验算法。van der Linden 用它们支撑两条标准路径：

- 用当前 \(\widehat\theta\) 选择信息量最大的题；
- 用当前后验分布选择能够优化后验的题。

这组引文适合定义“传统 CAT 基线”，但不能用来证明个体化起点更有效。

### Chang and Ying（1996）与 Gelman et al.（1995）：收敛论证需要加限定词

van der Linden 引用这两项工作说明，在一般正则条件下，最大似然估计或 Bayesian 后验估计可以随着信息积累接近真实 \(\theta\)。由此，论文进一步提出：初始点或初始分布离真实能力越远，算法通常越慢进入合适区域。

安全的写法是：

> 在适当正则条件下，CAT 中的能力估计可随作答信息积累而收敛；初始化主要影响有限测验前期的路径与效率（van der Linden, 1999；参见 Chang & Ying, 1996）。

不要把它写成“起点距离与有限题量下的收敛速度存在已被证明的单调函数关系”。原文中的 “generally” 是方法动机，不是本文提供的有限样本定理。

!!! note "Chang and Ying（1996）的版本"
    van der Linden 的参考文献列的是 1996 年 Psychometric Society 年会论文 *Building a Statistical Foundation for Computerized Adaptive Testing*。同年发表的相关期刊论文 [*A Global Information Approach to Computerized Adaptive Testing*](https://doi.org/10.1177/014662169602000303) 不是同一个书目条目，引用时不应直接互换。

## 4. 短测验、内容约束与经验起点

### van der Linden and Reese（1998）：真实 CAT 不只追求信息最大

[A Model for Optimal Constrained Adaptive Testing](https://doi.org/10.1177/01466216980223006) 说明，实际选题还要同时满足内容、认知层级、题面属性、敌对题和题组等约束。van der Linden（1999）借此强调：当约束很多时，CAT 早期未必能始终选择统计上最理想的题，因此更准确的初始化可能更有价值。

这里需要保持准确：van der Linden and Reese（1998）直接支持“约束可以很多且需要统一建模”，但它并不等价于“任何内容约束必然降低最终测量效率”。后者仍取决于题库、测验长度和约束强度。

### Brown and Weiss（1977）：短的自适应分测验

[An Adaptive Testing Strategy for Achievement Test Batteries](https://files.eric.ed.gov/fulltext/ED150165.pdf) 研究由多个分测验组成的自适应测验电池。它的重要性不只在于“CAT 可以缩短测验”，还在于前面分测验得到的信息能够帮助后面分测验更合理地开始。

### Gialluca and Weiss（1979）：跨分测验分支

*Efficiency of an Adaptive Inter-Subtest Branching Strategy in the Measurement of Classroom Achievement* 进一步研究用早期分测验表现安排后续分测验起点。van der Linden（1999）把 Brown and Weiss（1977）与 Gialluca and Weiss（1979）称为经验起始值的早期实例：他们把后续分测验的能力估计回归到早期分测验的估计上。

这两篇最适合支持：

> 在由多个短分测验组成的测验电池中，先前分测验的表现可作为后续分测验初始化的辅助信息。

它们并不直接支持“单次自报可以形成准确先验”，因为辅助信息来自先前的实际作答。

## 5. 曝光控制：15% 和 40% 应该怎样引用

### Sympson and Hetter（1985）：控制题目实际施测概率

Sympson–Hetter 方法在 CAT 选出题目后，再根据题目特异的接受概率决定是否真正施测。本站另有一页[完整方法笔记](sympson-hetter-1985.md)。

van der Linden（1999）的逻辑是：

1. 所有人从同一能力值出发，起点附近的题目容易被反复选中；
2. 直接曝光控制会拒绝一部分当前最优题，因此可能损失信息；
3. 如果个体化初始化本身就把受测者分散到不同 \(b\) 区域，可能减少对强制拒绝机制的依赖。

其中第 1 和第 3 点在本文中是机制论证，不是曝光模拟的结果。若需要经验数据，应同时引用 [Zhu and Fan（1999）](zhu-fan-1999.md)：他们直接比较了共同起点与个体化起始题的题目使用分布。

### Thomasson（1995）：这是二手且情境依赖的数字

van der Linden 转述 Thomasson（1995）的会议论文：Sympson–Hetter 控制在能力分布中心附近造成约 15% 的信息损失，更保守的方法在整个能力范围内最高可达到约 40%。

引用时最好写成：

> 在 Thomasson（1995）的模拟条件下，曝光控制伴随了明显的信息损失；van der Linden（1999）转述 Sympson–Hetter 方法在能力分布中心附近约损失 15% 的信息，而更保守方法在部分条件下达到约 40%。

不要写成“Sympson–Hetter 方法固定损失 15%，其他方法固定损失 40%”。原因有三点：

- 数字来自未正式出版的会议论文；
- 当前获得的是 van der Linden 的二手转述；
- 信息损失会随题库、能力分布、最高曝光率与选题约束变化。

## 6. collateral information、可忽略性与公平

### Mislevy 系列：辅助信息进入 IRT 并不是新思想

van der Linden 用四组工作说明，IRT 已经在其他统计目标中使用辅助信息：

| 文献 | 辅助信息用于什么目标 | 与本文的关系 |
|---|---|---|
| [Mislevy（1988）](https://doi.org/10.1177/014662168801200306) | 借用题目辅助信息估计 Rasch 题目难度 | 证明辅助信息可进入题目参数估计 |
| [Mislevy and Sheehan（1989）](https://doi.org/10.1007/BF02296402) | 用受测者辅助信息改善题目参数估计 | 更直接连接 examinee collateral information 与 IRT |
| Sheehan and Mislevy（1990） | 整合认知与心理测量模型测量文献素养 | 展示结构化外部信息如何进入测量模型 |
| [Mislevy et al.（1992）](https://doi.org/10.1111/j.1745-3984.1992.tb00371.x) | 从稀疏矩阵抽样的作答中估计群体特征 | 连接辅助变量、稀疏数据与群体推断 |

这些文献为方法思想提供先例，但研究目标主要是题目参数或群体分布，不是为单个受测者初始化 CAT。因此，个体层面的初始化仍是 van der Linden（1999）要补上的环节。

### Little and Rubin（1987）：为什么作者讨论 missingness

CAT 中每个人只作答题库的一小部分，其余题目是按自适应规则没有施测。Little and Rubin 的缺失数据框架为“选择机制能否忽略”提供正式语言。

### Mislevy and Wu（1988）：可忽略不等于任何推断都不受影响

[Inferring Examinee Ability When Some Items Are Missing](https://doi.org/10.1002/j.2330-8516.1988.tb00304.x) 是 van der Linden 公平论证中最关键的技术来源。原文给出的限定是：如果关注最大似然能力估计已经实现的数值，而不是它的抽样分布或标准误，那么自适应选题机制可以被忽略。

这意味着：利用背景信息选题，并不会自动要求把背景变量直接加到最终分数公式里；作答仍由 IRT 似然提供证据。但它**不意味着**：

- 背景信息对题目路径、测量精度与停止时间没有影响；
- 条件标准误可以无条件忽略选题机制；
- 使用敏感背景变量不存在公平或政策问题。

van der Linden 的结论是“是否用先验信息选题属于政策选择，没有普遍的技术性禁止”，而不是“公平性已经得到证明”。

## 7. 真正的方法差别：先计分再回归，还是对潜在能力积分

!!! important "一句话概括"
    Schoonman 把 \(\widehat\theta_j\) 当作已经观察到的回归因变量；van der Linden 把 \(\theta_j\) 保留为潜变量，使用完整逐题作答对它的不确定性进行积分。两者的差别不是“做不做回归”，而是 **plug-in point estimate** 与 **integrating over latent-trait uncertainty** 的差别。

### 两条估计路径

Schoonman 的两步法是：

\[
\mathbf u_j
\longrightarrow
\widehat\theta_j
\longrightarrow
\widehat\theta_j\sim x_j.
\]

它先把每个人的 Vocabulary 逐题作答 \(\mathbf u_j\) 压缩成一个能力点估计 \(\widehat\theta_j\)，再使用普通最小二乘回归：

\[
\widehat\theta_j
=
\beta_0+\beta_1x_j+e_j.
\]

van der Linden 则按照下列方向建立联合生成模型：

\[
x_j
\longrightarrow
\theta_j
\longrightarrow
\mathbf u_j,
\]

\[
\theta_j\mid x_j
\sim
N(\beta_0+\beta_1x_j,\sigma^2),
\qquad
U_{ij}\mid\theta_j
\sim
\operatorname{Bernoulli}\{P_i(\theta_j)\}.
\]

这个模型问的是：哪一组 \(\beta_0,\beta_1,\sigma^2\) 最有可能生成当前观察到的全部逐题作答？

### 两步回归为什么会污染 prior variance

假设真实的潜在回归为：

\[
\theta_j
=
\beta_0+\beta_1x_j+\varepsilon_j,
\qquad
\operatorname{Var}(\varepsilon_j)=\sigma^2.
\]

但能力点估计本身带有误差：

\[
\widehat\theta_j
=
\theta_j+\delta_j.
\]

因此，两步回归实际拟合的是：

\[
\widehat\theta_j
=
\beta_0+\beta_1x_j
+
\underbrace{\varepsilon_j}_{\text{真实预测残差}}
+
\underbrace{\delta_j}_{\text{能力估计误差}}.
\]

如果两种误差独立，普通回归看到的残差方差大约是：

\[
\operatorname{Var}(e_j)
=
\sigma^2+\operatorname{Var}(\delta_j).
\]

但个体化 prior 需要的是真实条件异质性：

\[
\sigma^2
=
\operatorname{Var}(\theta_j\mid x_j),
\]

而不应把短测验本身对 \(\theta_j\) 计分不准的部分也塞进 prior variance。

!!! example "一个假想的数值例子"
    如果真实的 \(\sigma^2=0.8\)，而 \(\widehat\theta\) 的平均估计误差方差为 \(0.3\)，那么两步回归可能看到 \(0.8+0.3=1.1\) 的残差方差。由此构造的 \(N(\widehat\beta_0+\widehat\beta_1x,1.1)\) 比真正的 \(N(\beta_0+\beta_1x,0.8)\) 更宽，因而会低估辅助信息的预测价值。这些数字只是解释机制的假想例子，不是论文的估计结果。

### 一个必须加上的统计限定

如果能力估计误差满足 \(E(\delta_j\mid x_j)=0\)，且与 \(x_j\) 无关，那么“因变量含有经典测量误差”并不必然使 OLS 斜率 \(\widehat\beta_1\) 衰减：

\[
\frac{\operatorname{Cov}(x,\widehat\theta)}{\operatorname{Var}(x)}
=
\frac{\operatorname{Cov}(x,\theta+\delta)}{\operatorname{Var}(x)}
=
\frac{\operatorname{Cov}(x,\theta)}{\operatorname{Var}(x)}.
\]

所以 van der Linden 的原文只说：两步法可能仍然给出令人满意的 \(\beta\) 估计，但无法给出良好的 prior variance \(\sigma^2\) 估计。更明确会受到影响的是残差方差、回归不确定性以及相关系数。在经典独立误差下，相关的衰减可表示为：

\[
\operatorname{Cor}(\widehat\theta,x)
=
\operatorname{Cor}(\theta,x)
\sqrt{
\frac{\operatorname{Var}(\theta)}
{\operatorname{Var}(\theta)+\operatorname{Var}(\delta)}
}.
\]

### van der Linden 如何保留每个人的能力不确定性

已校准的 2PLM 给出：

\[
P(U_{ij}=1\mid\theta_j)
=
\frac{\exp[a_i(\theta_j-b_i)]}
{1+\exp[a_i(\theta_j-b_i)]}.
\]

不再先生成一个固定的 \(\widehat\theta_j\) 后，回归参数的边际似然可写为：

\[
L(\beta_0,\beta_1,\sigma^2)
=
\prod_{j=1}^{N}
\int
\left[
\prod_{i=1}^{I}
P_i(\theta)^{u_{ij}}
\{1-P_i(\theta)\}^{1-u_{ij}}
\right]
\phi\left(
\theta;
\beta_0+\beta_1x_j,
\sigma^2
\right)
\,d\theta.
\]

对每个人，这个式子不假定能力就是某个无误差的点，而是遍历所有可能的 \(\theta\)，根据逐题作答判断各个位置有多合理，再对它们积分。因此，两名同样得到 \(\widehat\theta=0.5\) 的受测者不再被当成同样精确：20 道高区分度题给出的 \(0.5\) 会比 4 道低区分度题给出的 \(0.5\) 更紧，对回归参数提供更多信息。

### EM 算法实际在做什么

对于每名受测者，未观察的残差为：

\[
\varepsilon_j
=
\theta_j-(\beta_0+\beta_1x_j).
\]

van der Linden 借用 Rigdon and Tsutakawa（1983）的思路，把 \(\varepsilon_j\) 当作 missing data：

- **E 步：**根据当前 \(\beta_0,\beta_1,\sigma^2\)，结合个人的 \(x_j\) 和全部逐题作答 \(\mathbf u_j\)，计算 \(p(\varepsilon_j\mid\mathbf u_j,x_j,\beta_0,\beta_1,\sigma)\)。直观上是问：这个人的真实能力比回归预测值高多少或低多少？
- **M 步：**根据上述后验分布重新更新 \(\beta_0,\beta_1,\sigma^2\)。残差方差的更新本质上是

    \[
    \widehat\sigma^2
    =
    \frac{1}{N}
    \sum_{j=1}^{N}
    E\left(
    \varepsilon_j^2
    \mid
    \mathbf u_j,x_j
    \right).
    \]

两步反复执行直到收敛。实例用 Gauss–Hermite quadrature 计算积分，并用 Newton’s method 更新 \(\beta_0\) 和 \(\beta_1\)。这里“直接估计真实 \(\theta\) 的回归”并不是说作者观察到了真实能力，而是说他把 \(\theta\) 作为潜变量，不把第一阶段的 \(\widehat\theta\) 冒充成无误差观测值。

!!! note "方法的引文来源"
    Zwinderman（1991, 1997）提供 manifest predictors 进入潜在特质模型的基础；Rigdon and Tsutakawa（1983）提供 EM 思路；Neter et al.（1990）支撑回归与变量变换；Ralston and Rabinowitz（1983）是 Gauss–Hermite quadrature 的数值计算来源。未施测题目不进入该受测者的似然乘积，因此同一思路也可用于实际 CAT 的稀疏作答数据。

## 8. Empirical Example：从前测反应时到后测个体化 prior

!!! abstract "这个实例的核心"
    van der Linden 用前一个测验的反应时间，给后一个词汇测验建立个体化能力先验；并且不是先估计每个人的 \(\widehat\theta\) 再做普通回归，而是把回归模型和 IRT 作答模型联合估计，以避免 \(\widehat\theta\) 的测量误差被误当成先验不确定性。

### 数据与预测关系

论文使用荷兰一般能力倾向测验组的数据，样本量为：

\[
N=306.
\]

每个人依次完成两个测验：

1. **Name Comparison test：**记录完成该测验的总反应时间 \(T_j\)，并使用对数时间 \(x_j=\log T_j\)。
2. **Vocabulary test：**测量语言使用能力 \(\theta_j\)，研究者使用每名受测者的实际逐题作答 \(u_{ij}\in\{0,1\}\)。题库已经用 2PLM 标定，所以题目难度 \(b_i\) 和区分度 \(a_i\) 当作已知。

两个测验都涉及简单的词语使用，因此作者预期语言能力越高者完成 Name Comparison 越快：

\[
\operatorname{Cor}(\theta,x)<0.
\]

Schoonman（1989）使用前述两步法，得到 \(\operatorname{Cor}(\widehat\theta,x)=-0.46\)。van der Linden 在潜变量层面联合估计后，报告真实 \(\theta\) 与对数反应时的估计相关为 \(-0.59\)，并把绝对值的差异解释为先估计 \(\widehat\theta\) 造成的信息损失。这是相关的测量误差衰减，不应被改写为“OLS 斜率必然从 \(-0.46\) 修正到 \(-0.59\)”。

### 最终估计出的 prior

多组起始值都收敛到：

\[
\widehat\beta_0=5.833,
\qquad
\widehat\beta_1=-1.279,
\qquad
\widehat\sigma^2=0.986.
\]

因此，新受测者只要提供 Name Comparison 的对数总反应时间 \(x\)，就可以得到：

\[
\theta\mid x
\sim
N(5.833-1.279x,0.986).
\]

负斜率表示反应越慢，预测的 Vocabulary 潜在能力越低。

### 在新 CAT 中的两种使用方式

**只作为初始点：**

\[
\widehat\theta^{(0)}
=
5.833-1.279x_{\mathrm{new}}.
\]

然后在这个位置选择信息量最大的第一道 Vocabulary 题：

\[
j_1
=
\arg\max_j I_j(\widehat\theta^{(0)}).
\]

这时前一测验的反应时只负责把新 CAT 送到较合适的起点。

**作为完整的 Bayesian prior：**

\[
p_0(\theta\mid x_{\mathrm{new}})
=
N(5.833-1.279x_{\mathrm{new}},0.986).
\]

每作答一题就使用贝叶斯定理更新：

\[
p_t(\theta)
\propto
p_0(\theta\mid x_{\mathrm{new}})
\prod_{s=1}^{t}
P(U_{i_s}=u_{i_s}\mid\theta).
\]

这时辅助信息会持续影响中间能力估计、后续题目选择、最终估计和后验标准误。后续可以在 EAP 位置使用最大信息量选题，也可以使用最小期望后验方差等 Bayesian 准则。

### 这个实例证明了什么，又没有证明什么

它证明的是：可以从“测前辅助变量 + 逐题作答”中直接估计个体化 prior 的均值与方差，并避免把能力计分误差误当成背景变量的预测失败。

它没有重新运行一组个体化 prior CAT 与标准 CAT 对照，因此没有直接比较：

- 平均测验长度和相同 stopping rule 下的停止时间；
- bias、均方根误差和区间覆盖率；
- 实际题目路径和题目曝光；
- 错误先验是否导致偏差或错误提前停止。

!!! warning "它是先验构造示例，不是 CAT 效率实验"
    本例的证据上限是“该联合模型可以被估计并得到个体化先验”，不是“该先验已被证明能缩短 CAT”。

### 对自评 CAT 的直接启示

如果将反应时 \(x_j\) 换成用户自评 \(s_j\)，最简单的训练方式是对 \(\widehat\theta_j\) 做普通回归。如果用来估计 \(\theta_j\) 的校准测验很长，\(\widehat\theta_j\) 足够精确，这种两步法可能够用。

但如果校准测验本来就很短，更合理的做法是直接建立：

\[
\theta_j\mid s_j
\sim
N(\beta_0+\beta_1s_j,\sigma^2),
\qquad
U_{ij}\mid\theta_j
\sim
\operatorname{Bernoulli}\{P_i(\theta_j)\},
\]

再从逐题作答中联合估计 \(\beta_0,\beta_1,\sigma^2\)。这样才能把“用户自评预测不准”与“短测验对能力计分不准”分开。

## 9. 可以直接改写进论文的引用句

下面是安全的中文转述模板，不是原文逐字翻译。

### 个体化经验先验

> 测验前可得的个体辅助变量可以通过潜在回归映射为条件能力分布 \(\theta\mid X=x\sim N(x^\top\beta,\sigma^2)\)，其条件均值可用于选择起始题，完整条件分布则可作为 Bayesian CAT 的个体化经验先验（van der Linden, 1999）。

### 初始点与完整 prior 的区别

> 仅使用条件均值初始化点估计时，辅助信息可以只决定第一道题；若将条件分布作为 prior，辅助信息会通过逐题后验更新影响整个自适应测验过程（van der Linden, 1999）。

### 不应对带误差的能力估计做朴素回归

> 将带测量误差的能力估计作为普通回归因变量，会把能力估计误差与真实预测残差混合，因而难以正确估计先验方差；更合适的做法是从题目作答数据直接估计潜在回归参数（van der Linden, 1999）。

### 早期跨分测验初始化

> 在自适应测验电池中，先前分测验的表现曾被用于预测并初始化后续短分测验的能力位置（Brown & Weiss, 1977; Gialluca & Weiss, 1979; van der Linden, 1999）。

### 共同起点与题库曝光

> 共同初始能力值会使起点附近的题目承受较高曝光压力；个体化起始位置有可能将首题使用分散到更宽的难度范围（van der Linden, 1999）。这一机制的直接模拟证据可另见 Zhu and Fan（1999）。

### 公平与可忽略性

> 在特定最大似然推断目标下，自适应选题机制对已实现的能力点估计可以是可忽略的，但这一结果不自动扩展到估计量的抽样分布、标准误或公平性判断（Mislevy & Wu, 1988; van der Linden, 1999）。

## 10. 最容易引用过头的六个地方

| 不建议的写法 | 问题 | 更准确的写法 |
|---|---|---|
| “van der Linden（1999）证明个体化 prior 会缩短 CAT。” | 没有 CAT 对照实验 | “提出个体化经验先验的估计与初始化框架。” |
| “本文证明自评可以准确预测能力。” | 实例用的是前测反应时，不是自评 | “框架原则上允许使用与能力相关的测前变量；自评效度需另行验证。” |
| “个体化信息只改变第一题。” | 只有使用条件均值作初始点时才成立 | “点初始化可只影响首题；完整 prior 会影响后续后验路径。” |
| “Sympson–Hetter 固定损失 15% 信息。” | 数字是二手、特定模拟结果 | “van der Linden 转述 Thomasson（1995）在特定条件下观察到约 15% 的中心信息损失。” |
| “选题机制可以忽略，所以背景变量不会造成公平问题。” | 混淆统计可忽略性与规范性公平 | “可忽略性只在特定推断目标和模型条件下成立；公平仍是政策与实证问题。” |
| “更接近真实值的 prior 可以立即停止。” | 单次作答具有随机性，停止仍需足够后验精度 | “更合适的 prior 可能改善早期路径，但仍须用作答证据达到既定停止标准。” |

## 11. 为本专题最值得继续追的七项来源

按与“自评信息进入 CAT”研究的接近程度排序：

1. **Zwinderman（1991）**：理解 \(X\rightarrow\theta\) 的潜在回归模型；
2. **Rigdon and Tsutakawa（1983）**：理解为什么要从题目反应直接估计 \(\beta\) 和 \(\sigma^2\)；
3. **Mislevy and Wu（1988）**：厘清自适应选题、缺失机制与最终能力推断；
4. **Brown and Weiss（1977）与 Gialluca and Weiss（1979）**：寻找“已有个体信息初始化后续短测验”的早期直接先例；
5. **van der Linden and Reese（1998）**：理解真实 CAT 中的信息量与内容约束怎样共同决定选题；
6. **van der Linden（1998）**：比较最大信息量与最小期望后验方差等 Bayesian 选题准则；
7. **Thomasson（1995）**：如能取得原始会议论文，再核查 15%/40% 信息损失的模拟条件。

## 12. 参考文献中的一个书目问题

正文引用的是 Lord（1970），但论文参考文献页印成 Lord（1990），并列出的书名是 W. H. Holtzman 主编的 *Computer-Assisted Instruction, Testing, and Guidance*。该书及 Lord 的章节实际对应 1970 年出版信息。后续写作不要同时出现 “Lord, 1970” 和参考文献中的 “Lord, 1990”；应先按原始出版物核对后统一为正确年份。

## 13. 对本专题实验设计的直接启示

van der Linden（1999）把导师提出的两个动作明确分开了：

| 设计动作 | 数学实现 | 它改变什么 |
|---|---|---|
| 只改变第一题 | 用 \(\mu_c=x_c^\top\widehat\beta\) 初始化并选择首题 | 首题难度位置与首题曝光 |
| 改变个体化 prior | 使用 \(N(\mu_c,\tau_c^2)\) 逐题更新 | 初始位置、不确定性、后验路径、后续选题与停止时间 |

因此后续消融至少需要分别比较：

1. 标准先验 \(N(0,1)\) 与标准首题；
2. 标准先验与自评匹配首题；
3. 个体化先验与常规 Bayesian 选题；
4. 个体化先验与自评匹配首题。

而 van der Linden（1999）提供的是第 3、4 类方法的统计入口，不是这四组之间的效果答案。

## 14. 按引用角色重排的参考文献

### CAT、IRT 与收敛基础

- Birnbaum, A. (1968). Some latent trait models and their use in inferring an examinee’s ability. In F. M. Lord and M. R. Novick, *Statistical Theories of Mental Test Scores*. Addison-Wesley.
- Chang, H.-H., and Ying, Z. (1996, June). *Building a Statistical Foundation for Computerized Adaptive Testing*. Paper presented at the annual meeting of the Psychometric Society, Banff, Alberta, Canada.
- Gelman, A., Carlin, J. B., Stern, H. S., and Rubin, D. B. (1995). *Bayesian Data Analysis*. Chapman and Hall.
- Thissen, D., and Mislevy, R. J. (1990). Testing algorithms. In H. Wainer (Ed.), *Computerized Adaptive Testing: A Primer*. Erlbaum.
- Wainer, H. (Ed.). (1990). *Computerized Adaptive Testing: A Primer*. Erlbaum.

### 经验初始化、短分测验与约束

- Brown, J. M., and Weiss, D. J. (1977). *An Adaptive Testing Strategy for Achievement Test Batteries* (Research Report 77-6). University of Minnesota. [ERIC 全文](https://files.eric.ed.gov/fulltext/ED150165.pdf)
- Gialluca, K. A., and Weiss, D. J. (1979). *Efficiency of an Adaptive Inter-Subtest Branching Strategy in the Measurement of Classroom Achievement* (Research Report 79-6). University of Minnesota.
- Lord, F. M. (1970). Some test theory for tailored testing. In W. H. Holtzman (Ed.), *Computer-Assisted Instruction, Testing, and Guidance* (pp. 139–183). Harper and Row. 原论文参考文献页误印为 1990。
- van der Linden, W. J., and Reese, L. M. (1998). A model for optimal constrained adaptive testing. *Applied Psychological Measurement, 22*, 259–270. [DOI](https://doi.org/10.1177/01466216980223006)

### 曝光控制

- Sympson, J. B., and Hetter, R. D. (1985, October). *Controlling Exposure Rates in Computerized Adaptive Testing*. Paper presented at the 27th annual meeting of the Military Testing Association, San Diego, California.
- Thomasson, G. L. (1995, June). *New Item Exposure Control Algorithms for Computerized Adaptive Testing*. Paper presented at the annual meeting of the Psychometric Society, Minneapolis, Minnesota.

### 辅助信息、缺失数据与可忽略性

- Little, R. J. A., and Rubin, D. B. (1987). *Statistical Analysis with Missing Data*. Wiley.
- Mislevy, R. J. (1988). Exploiting auxiliary information about items in the estimation of Rasch item difficulty parameters. *Applied Psychological Measurement, 12*, 281–296. [DOI](https://doi.org/10.1177/014662168801200306)
- Mislevy, R. J., Beaton, A. E., Kaplan, B., and Sheehan, K. M. (1992). Estimating population characteristics from sparse matrix samples of item responses. *Journal of Educational Measurement, 29*, 133–161. [DOI](https://doi.org/10.1111/j.1745-3984.1992.tb00371.x)
- Mislevy, R. J., and Sheehan, K. M. (1989). The role of collateral information about examinees in item parameter estimation. *Psychometrika, 54*, 661–679. [DOI](https://doi.org/10.1007/BF02296402)
- Mislevy, R. J., and Wu, P.-K. (1988). *Inferring Examinee Ability When Some Items Are Missing* (Research Report 88-48). Educational Testing Service. [DOI](https://doi.org/10.1002/j.2330-8516.1988.tb00304.x)
- Sheehan, K. M., and Mislevy, R. J. (1990). Integrating cognitive and psychometric models to measure document literacy. *Journal of Educational Measurement, 27*, 255–272.

### 潜在回归、EM 与数值计算

- Neter, J., Wasserman, W., and Kutner, M. H. (1990). *Applied Linear Statistical Models* (3rd ed.). Irwin.
- Ralston, A., and Rabinowitz, P. (1983). *A First Course in Numerical Analysis*. McGraw-Hill.
- Rigdon, S. E., and Tsutakawa, R. K. (1983). Parameter estimation in latent trait models. *Psychometrika, 48*, 567–574. [DOI](https://doi.org/10.1007/BF02293880)
- Zwinderman, A. H. (1991). A generalized Rasch model for manifest predictors. *Psychometrika, 56*, 589–600. [DOI](https://doi.org/10.1007/BF02294492)
- Zwinderman, A. H. (1997). Response models with manifest predictors. In W. J. van der Linden and R. K. Hambleton (Eds.), *Handbook of Modern Item Response Theory* (pp. 245–256). Springer. [DOI](https://doi.org/10.1007/978-1-4757-2691-6_14)

### 本文实例与 Bayesian 选题扩展

- Schoonman, W. (1989). *An Applied Study on Computerized Adaptive Testing*. Swets and Zeitlinger.
- van der Linden, W. J. (1998). Bayesian item selection criteria for adaptive testing. *Psychometrika, 63*, 201–216. [DOI](https://doi.org/10.1007/BF02294775)

---

**专题导航：**[返回阅读清单](index.md) · [第二篇：Zhu and Fan（1999）](zhu-fan-1999.md) · [Sympson–Hetter 方法](sympson-hetter-1985.md)
