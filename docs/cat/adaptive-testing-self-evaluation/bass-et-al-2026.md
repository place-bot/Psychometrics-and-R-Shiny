# Bass 等人（2026）：纵向 PROMIS CAT 能否沿用上一次分数作为 prior

## 文献身份

> Bass, M., Morris, S., & Lam, T. (2026). Brief reports: Impact of informed starting value on longitudinal computer adaptive tests in PROMIS assessments. *Advances in Patient-Reported Outcomes, 2*, 100322. [DOI](https://doi.org/10.1016/j.apro.2026.100322)

- 研究类型：两时间点 test-retest CAT 模拟
- 应用工具：患者报告结局测量信息系统（Patient-Reported Outcomes Measurement Information System, PROMIS）成人与儿童题库
- 辅助信息：第一次 CAT 的最终 \(\widehat\theta_1\)
- 第二次 CAT：以 \(\widehat\theta_1\) 为 prior 均值，并改变 prior 标准差
- 估计方法：期望后验估计（Expected A Posteriori, EAP）
- 停止规则：至少 4 题、\(SE<0.3\)、最多 8 题
- 主要结论：适度加权旧分数在健康状态变化较小时可能略微缩短测验并降低 RMSE；过窄 prior 会把第二次估计锁在旧分数附近，形成更短但更不准确的测验

!!! abstract "一句话结论"
    上一次 CAT 分数可以作为纵向复测的个体化 prior，但收益取决于两次测量之间可能变化多少以及题库是否覆盖患者位置。小变化时 \(SD=0.5\) 通常表现较好；大变化时更宽的 \(SD=0.75\) 或 \(1.0\) 更安全，\(SD=0.25\) 则常把真实变化误当成噪声。

!!! danger "最容易把这篇读错的地方"
    标题使用 informed starting value，但作者改变的是第二次 CAT 的完整 prior 分布。它不仅决定开头位置，还持续进入 EAP 能力估计、逐题选题、最终分数和停止判断。因此它不是 Petersen 等人（2026）那种“只改变第一题”的研究。

## 1. 研究问题：复测为什么不直接从上一次分数开始

纵向 CAT 已经拥有同一患者上一次测量的分数。最自然的想法是：

\[
\mu_{2,p}
=
\widehat\theta_{1,p}.
\]

如果患者状态变化不大，这比每次都从总体均值 0 开始更个性化。

问题在于，上一次分数并不等于这一次真实状态：

\[
\theta_{2,p}
=
\theta_{1,p}
+
\delta_p,
\]

其中 \(\delta_p\) 是两次评估之间的真实变化。此外，\(\widehat\theta_{1,p}\) 自身还带有测量误差。

若系统只使用上次测量的最终标准误作为 prior 不确定性，就隐含假设：

\[
\delta_p=0.
\]

在真正需要监测疗效、病情恶化或恢复的情境中，这个假设恰恰可能不成立。过度相信旧分数会将第二次估计向旧状态收缩，从而降低检测变化的能力。

## 2. 纵向 prior 的方差应当包含两种不确定性

作者用一个简单近似表示第二次状态相对于第一次估计的不确定性：

\[
SD(\theta_2\mid\widehat\theta_1)
=
\sqrt{
SE(\widehat\theta_1)^2
+
SD(\delta)^2
}.
\]

这里包含：

1. 上一次 CAT 的计分误差 \(SE(\widehat\theta_1)\)；
2. 两次测量之间真实变化的个体差异 \(SD(\delta)\)。

这条公式对我们很有价值，因为它说明个体化 prior 的方差不能只由“自评本身看起来多精确”决定。若辅助信息与当前目标状态之间存在时间间隔、情境变化或构念漂移，还必须加入状态变化的不确定性。

### 一个直观数值例子

PROMIS 第一次测量的最终标准误约为 \(0.25\)，如果两次之间的小变化标准差约为 \(0.30\)：

\[
\sqrt{0.25^2+0.30^2}
\approx
0.39.
\]

模拟候选值中最接近的是 prior \(SD=0.5\)。

若变化标准差为 \(0.80\)：

\[
\sqrt{0.25^2+0.80^2}
\approx
0.84.
\]

此时 \(SD=0.75\) 或 \(1.0\) 更合理。论文结果也大致呈现这一模式：小变化时 \(0.5\) 往往最好，大变化时 \(0.75\) 或 \(1.0\) 更安全。

作者也提出，如果拥有合适人群的大样本纵向数据，可以直接估计变化方差；若没有，则可依据既有研究、复测间隔与专家判断设定，再通过模拟调参。

## 3. 必须区分 prior 标准差和 prior 方差

Bass 等人操纵的是：

\[
SD_{\mathrm{prior}}
\in
\{1.00,0.75,0.50,0.25\}.
\]

对应方差为：

\[
\operatorname{Var}_{\mathrm{prior}}
\in
\{1.00,0.5625,0.25,0.0625\}.
\]

这与 Frans 等人（2023）操纵的 prior 方差：

\[
\{1.00,0.50,0.25\}
\]

不是同一组强度。

| Bass：prior SD | Bass：prior variance | 大致对应含义 |
|---:|---:|---|
| 1.00 | 1.0000 | 几乎不信任旧分数 |
| 0.75 | 0.5625 | 轻度信任 |
| 0.50 | 0.2500 | 中等信任 |
| 0.25 | 0.0625 | 极强信任 |

!!! warning "与我们的 \(\tau^2\) 实验直接相关"
    如果我们说“prior variance 从 0.1 到 1”，Bass 的 \(SD=0.25\) 不是方差 0.25，而是方差 0.0625；\(SD=0.5\) 才对应方差 0.25。跨论文比较时必须统一到 variance 或 precision，不能直接比较表面数字。

## 4. 模拟使用哪些 PROMIS 题库

### 七个成人领域

1. Physical Function；
2. Fatigue；
3. Pain Interference；
4. Sleep Disturbance；
5. Depression；
6. Anxiety；
7. Ability to Participate in Social Roles and Activities。

### 六个儿童领域

1. Mobility；
2. Fatigue；
3. Pain Interference；
4. Depressive Symptoms；
5. Anxiety；
6. Peer Relationships。

论文的一个现实优势是使用官方 PROMIS 题库与实际运行软件，而不是只按照大致参数生成虚构题库。成人与儿童题库在题数、覆盖范围和 ceiling/floor effects 上不同，可以检验 prior 收益是否受题库特征限制。

## 5. 两时间点数据怎样生成

### 5.1 Time 1 的真实状态

第一次测量的真实能力位于九个网格点：

\[
\theta_{1,p}
\in
\{-2,-1.5,-1,-0.5,0,0.5,1,1.5,2\}.
\]

每个网格点模拟 100 次，所以每个 PROMIS 领域有：

\[
900
\]

组评估。

### 5.2 Time 2 的真实变化

作者模拟两种变化尺度：

#### 小变化

\[
\delta_p\sim N(0,0.3),
\]

#### 大变化

\[
\delta_p\sim N(0,0.8).
\]

正文把 \(0.3\) 和 \(0.8\) 当作变化的标准差/效应量尺度来讨论，尽管 \(N(0,\cdot)\) 的第二参数没有在符号上明确写成方差还是标准差。本页依照作者的文字解释，将其记作 \(SD(\delta)=0.3\) 或 \(0.8\)。

于是：

\[
\theta_{2,p}
=
\theta_{1,p}
+
\delta_p.
\]

论文同时允许改善和恶化，因为变化分布以 0 为中心。

## 6. 两次 CAT 的 prior、估计和停止规则

### Time 1

\[
\theta_{1,p}
\sim
N(0,1).
\]

### Time 2

prior 均值设为第一次 CAT 的最终 EAP：

\[
\mu_{2,p}
=
\widehat\theta_{1,p}.
\]

再依次使用：

\[
\theta_{2,p}
\sim
N(
\widehat\theta_{1,p},
\sigma_{\mathrm{prior}}^2
),
\]

其中：

\[
\sigma_{\mathrm{prior}}
\in
\{1.00,0.75,0.50,0.25\}.
\]

每个领域单独实施 CAT，题目反应由该领域相应的 IRT 模型生成，能力估计使用 EAP。prior 会持续参与第二次 CAT 的后验：

\[
p(\theta_{2,p}\mid\mathbf u_{2,p})
\propto
p(\mathbf u_{2,p}\mid\theta_{2,p})
\phi(
\theta_{2,p};
\widehat\theta_{1,p},
\sigma_{\mathrm{prior}}^2
).
\]

因此 prior 会影响：

\[
\text{初始位置}
\rightarrow
\text{第一题}
\rightarrow
\text{后续 EAP}
\rightarrow
\text{后续选题}
\rightarrow
\text{最终估计与停止}.
\]

共同停止规则为：

\[
n\geq4,
\qquad
SE(\widehat\theta)<0.3,
\qquad
n\leq8.
\]

评价指标为：

- 平均题量；
- 最终估计的均方根误差（root mean squared error, RMSE）：

\[
\operatorname{RMSE}
=
\sqrt{
\frac{1}{N}
\sum_{p=1}^{N}
(\widehat\theta_{2,p}-\theta_{2,p})^2
}.
\]

## 7. 为什么 \(SD=0.25\) 会把 CAT 变成四题测验

最窄 prior 的方差为：

\[
0.25^2
=
0.0625.
\]

其初始标准差 \(0.25\) 已经小于停止阈值 \(0.3\)。如果没有最少题数约束，系统可能在施测前就认为精度足够。

由于论文强制至少施测四题，\(SD=0.25\) 条件几乎全部在第四题立即停止。作者明确说，这实际上把 CAT 变成了固定长度四题测验。

所以该条件“题量大幅下降到 4”不能被解释为题目证据高效完成了测量。更准确的解释是：

\[
\text{强 prior 已满足精度要求}
\quad+\quad
\text{最少四题约束}
\quad\Rightarrow\quad
n=4.
\]

作者也说明 \(SD=0.25\) 不是现实中建议的默认实现，而是用于显示不同题库在当前停止规则下可能达到的题量下限。

## 8. 题库 well-targeted 和 poorly targeted 是什么

PROMIS 题库通常在有一定症状或功能受损的位置提供较高信息，而在无症状或 ceiling/floor 区域信息较低。

作者按照 Time 2 的真实 \(\theta_{2,p}\) 与完整题库信息函数的匹配程度，把模拟评估分成：

- well-targeted：真实位置处完整题库信息 \(TI>22\)；
- poorly targeted：真实位置处完整题库信息不超过 22。

因为：

\[
SE
\approx
\frac{1}{\sqrt{TI}},
\]

\[
TI=22
\Rightarrow
SE\approx0.21.
\]

论文选择 22，而不是刚好满足 \(SE=0.3\) 所需的约 11，是为了识别能够较稳定地在耗尽题库前达到停止条件的区域。

### 成人题库中 well-targeted 的比例

| 领域 | 比例 |
|---|---:|
| Physical Function | 83% |
| Fatigue | 82% |
| Ability to Participate Social | 74% |
| Sleep Disturbance | 72% |
| Anxiety | 60% |
| Depression | 60% |
| Pain Interference | 60% |

### 儿童题库中 well-targeted 的比例

| 领域 | 比例 |
|---|---:|
| Peer Relationships | 61% |
| Anxiety | 49% |
| Depressive Symptoms | 49% |
| Fatigue | 49% |
| Pain Interference | 39% |
| Mobility | 18% |

!!! note "这个分层不能直接用于真实施测决策"
    well-targeted/poorly targeted 是根据模拟中的真实 \(\theta_2\) 事后划分的。实际 CAT 开始前并不知道真实位置，因此它是解释结果异质性的分析工具，不是可以直接部署的 routing rule。

## 9. 小变化下的成人 CAT：题量减少多少

当 \(SD(\delta)=0.3\) 时，仅把 Time 2 prior 均值改成上一次分数、但仍保留 \(SD=1\)，题量与不使用旧信息的标准 \(N(0,1)\) prior 很接近。作者报告成人领域平均变化不足 0.1 题。

这再次说明：

> 移动 prior 均值本身不一定缩短固定精度 CAT；真正显著改变题量的是缩小 prior SD、让旧分数贡献更多精度。

### well-targeted 组

从 prior \(SD=1\) 缩小到 \(0.25\)，平均题量跨领域下降约 0.44 题，范围从：

- Depression：下降 0.13 题；
- Sleep Disturbance：下降 1.00 题。

收益有限，因为许多 well-targeted 受测者本来就只做最低的 4 题，存在明显 floor effect。

更有实际意义的是 \(SD=0.5\)：

| 领域 | \(SD=1\) 题量 | \(SD=0.5\) 题量 |
|---|---:|---:|
| Ability to Participate Social | 4.43 | 4.17 |
| Anxiety | 4.16 | 4.01 |
| Depression | 4.13 | 4.02 |
| Fatigue | 4.17 | 4.02 |
| Pain Interference | 4.49 | 4.31 |
| Physical Function | 4.76 | 4.25 |
| Sleep Disturbance | 5.00 | 4.16 |

### poorly targeted 组

从 \(SD=1\) 缩小到 \(0.25\)，所有成人领域平均减少超过 3 题，但原因是 CAT 被强制压到 4 题。

在更合理的 \(SD=0.5\) 条件下：

| 领域 | \(SD=1\) 题量 | \(SD=0.5\) 题量 |
|---|---:|---:|
| Ability to Participate Social | 7.72 | 7.34 |
| Anxiety | 7.65 | 7.29 |
| Depression | 7.58 | 7.17 |
| Fatigue | 7.13 | 6.16 |
| Pain Interference | 7.97 | 7.92 |
| Physical Function | 7.97 | 7.27 |
| Sleep Disturbance | 7.34 | 6.05 |

题量收益主要出现在原本接近最大 8 题、题库对真实位置提供较少信息的情况；但这些人也最容易受到错误 prior 的影响，因此不能只看题量。

## 10. 小变化下的成人 CAT：RMSE 怎样变化

### well-targeted 组

作者报告，相对 \(SD=1\)，使用 informed prior 的平均 RMSE 改善约：

\[
0.025,
\]

不同领域约为 \(0.015\) 至 \(0.051\)。多数领域在 \(SD=0.5\) 时得到最低 RMSE。

例如：

| 领域 | \(SD=1\) RMSE | \(SD=0.5\) RMSE | \(SD=0.25\) RMSE |
|---|---:|---:|---:|
| Pain Interference | 0.253 | 0.202 | 0.225 |
| Physical Function | 0.244 | 0.217 | 0.237 |
| Sleep Disturbance | 0.275 | 0.251 | 0.283 |

\(SD=0.25\) 虽然都只做 4 题，却已经开始比 \(SD=0.5\) 更差。

### poorly targeted 组

作者报告跨领域平均 RMSE 改善约：

\[
0.059.
\]

Fatigue 在 \(SD=0.5\) 时改善最大，约 \(0.097\)：

\[
0.407
\rightarrow
0.310.
\]

但 Pain Interference 是明显反例：

| prior SD | 题量 | RMSE |
|---:|---:|---:|
| 1.00 | 7.97 | 0.526 |
| 0.75 | 7.94 | 0.529 |
| 0.50 | 7.92 | 0.573 |
| 0.25 | 4.00 | 0.639 |

prior 越强，题量越短或基本不变，RMSE 却持续变差。这说明即使真实变化总体较小，个别题库和位置仍不适合复用旧分数。

## 11. 大变化时，旧分数迅速失去价值

当 \(SD(\delta)=0.8\) 时，Time 1 分数与 Time 2 真实状态的差异更大。

### 成人 well-targeted

正文称只有 Pain Interference 和 Physical Function 在 \(SD=0.75\) 时略有改善：

- Pain Interference：RMSE \(0.276\rightarrow0.254\)；
- Physical Function：RMSE \(0.239\rightarrow0.233\)。

其余领域的最低 RMSE一般出现在 \(SD=1\)，即几乎不对旧分数增加额外权重。

### 成人 poorly targeted

正文称没有领域因加强 prior 而提高准确性。表 3 中 Ability to Participate Social 从：

\[
0.594
\rightarrow
0.587
\]

在 \(SD=0.75\) 时有极小的数值下降，因此“没有领域改善”应理解为没有清晰或有意义的改善，而不是每个表格数值都严格单调变差。

最窄的 \(SD=0.25\) 把所有测验压到 4 题，并产生严重 RMSE：

| 领域 | \(SD=1\) RMSE | \(SD=0.25\) RMSE |
|---|---:|---:|
| Ability to Participate Social | 0.594 | 0.814 |
| Anxiety | 0.516 | 0.775 |
| Depression | 0.518 | 0.761 |
| Fatigue | 0.382 | 0.821 |
| Pain Interference | 0.679 | 0.914 |
| Physical Function | 0.447 | 0.900 |
| Sleep Disturbance | 0.369 | 0.719 |

这正是纵向测量中最危险的情况：

\[
\text{测验更短}
\quad\text{但}\quad
\text{真实变化被 prior 压回旧状态}.
\]

## 12. 儿童题库的结果

论文只模拟儿童领域的小变化 \(SD(\delta)=0.3\)。

### well-targeted

平均 RMSE 改善约 \(0.013\)，小于成人领域。多数领域在 \(SD=0.5\) 最好，Mobility 则在 \(SD=0.75\) 略好。

### poorly targeted

只有三个领域在 \(SD=0.75\) 出现较低 RMSE：

- Peer Relationships；
- Anxiety；
- Depressive Symptoms。

Fatigue 基本不变，Pain Interference 与 Mobility 则在 \(SD=1\) 最好。儿童题库更小、ceiling/floor effects 更明显，使 prior 的表现更依赖领域。

这表明不能从某个 PROMIS 领域得到“最佳 prior SD”后直接推广到其他领域或年龄组。

## 13. 表格与正文中需要注意的标记问题

### 13.1 表 2 至表 4 把 prior SD 行标成了 SE

表格第一列写成：

\[
SE=1,\ 0.75,\ 0.5,\ 0.25.
\]

但方法、图 1 至图 6 和正文都说明被操纵的是 prior standard deviation。因此这些行应按：

\[
SD_{\mathrm{prior}}
=
1,\ 0.75,\ 0.5,\ 0.25
\]

解释，不能把它们读成 CAT 最终标准误。

### 13.2 \(N(0,0.3)\) 的第二参数写法不够明确

统计学中有的作者用 \(N(\mu,\sigma^2)\)，有的用 \(N(\mu,\sigma)\)。本文把 0.3 称为 change magnitude/effect size，并用 \(SD(\delta)\) 推导 prior，因此更合理的阅读是变化标准差为 0.3，而不是变化方差为 0.3。

### 13.3 没有报告 Monte Carlo 不确定性或显著性检验

表中的题量和 RMSE 是描述性模拟结果，没有置信区间、Monte Carlo standard error 或模型比较检验。“improved”主要指数值更低，不应自动解释为稳定、显著或具有临床意义。

## 14. 与 Petersen 和 Frans 的关系

| 研究 | 辅助信息来源 | prior 是否持续进入估计 | 是否只改第一题 | 主要问题 |
|---|---|---:|---:|---|
| Petersen 等人（2026） | 另一个 HRQoL 领域 | 否 | 是 | 个体化首题的局部收益 |
| Frans 等人（2023） | oracle 偏差或临床 global score | 是 | 否 | 错误强 prior 的风险 |
| Bass 等人（2026） | 同一领域上一次 CAT 分数 | 是 | 否 | 时间变化下如何设 prior SD |

Bass 等人不是“外部信息只决定第一题”的新证据，而是 Frans 等人的纵向版本：旧分数既改变初始位置，也持续改变后验精度与停止时间。

它的独特贡献是把 prior variance 拆成：

\[
\text{上一次计分误差}
+
\text{真实状态变化方差}.
\]

## 15. 证据边界与限制

### 15.1 这是模拟，不是真实 longitudinal PROMIS 数据

第一次与第二次作答都由 IRT 模型生成。论文没有使用真实患者的重复测量检验：

- 变化分布是否真为正态；
- 不同人变化方差是否相同；
- prior 是否影响真实患者的作答行为；
- 实际临床中题量节省是否可感知。

### 15.2 prior 均值来自上一次 CAT，不是用户自评

这篇证明的是：

> prior assessment information 可以进入下一次 CAT。

它没有证明用户显式自评具备相同的误差结构或稳定性。

### 15.3 well-targeted 分层使用真实 \(\theta_2\)

真实部署时无法预先知道患者属于哪组。论文没有给出一个可观察的规则来决定：

\[
\text{该患者应使用 }SD=0.5
\quad\text{还是}\quad
SD=1.
\]

### 15.4 没有独立拆分“首题路径”和“持续 prior”

所有 Time 2 条件都让 prior 持续进入 EAP。论文没有比较：

- 只用旧分数选择第一题；
- 旧分数只用于初始 EAP，第一题后丢弃；
- 旧分数持续进入完整后验。

### 15.5 没有覆盖率、变化检测和曝光指标

论文报告题量与 RMSE，但没有直接报告：

- bias；
- 后验区间覆盖率；
- minimally important change 的检出率；
- 假阴性变化率；
- 题目总体与条件曝光；
- test overlap。

尤其在纵向测量中，仅看 RMSE 会掩盖一个关键临床问题：强 prior 是否系统性把真实改善或恶化缩向 0。

### 15.6 最少四题制造明显的 floor

well-targeted 组本来就经常只做 4 题，因此 informed prior 即使有用也无法继续缩短。由此得到的“边际收益很小”既可能说明 prior 没用，也可能只是现有最少题数规则限制了可观察收益。

## 16. 对我们研究设计的直接启示

### 16.1 prior 方差要从信号误差和状态变化共同标定

如果自评与 CAT 同时发生，状态变化项可能很小；如果自评来自数天前、历史记录或上次测量，则应使用：

\[
\tau_{\mathrm{current}}^2
=
\tau_{\mathrm{signal}}^2
+
\tau_{\mathrm{change}}^2.
\]

不能把历史分数当作对当前状态同样精确的观测。

### 16.2 统一用 variance 报告实验条件

建议主实验写：

\[
\tau^2
\in
\{1.00,0.50,0.25,0.10\},
\]

并同时列出：

\[
\tau
\in
\{1.00,0.707,0.500,0.316\}.
\]

这样可以与 Frans 的 variance 条件直接比较，也能避免把 Bass 的 \(SD=0.5\) 错读成 variance 0.5。

### 16.3 检查 prior 是否在施测前已满足停止规则

对每个 \(\tau^2\)，先比较：

\[
\tau
\quad\text{与}\quad
\varepsilon_{\mathrm{stop}}.
\]

若：

\[
\tau\leq\varepsilon_{\mathrm{stop}},
\]

则必须显式说明：

- 是否允许 0 题停止；
- 是否强制最少题数；
- 最少题数以后立即停止是否被视为成功；
- 精度有多少来自 prior，而不是正式题目。

### 16.4 对“真实变化”做方向敏感评价

除了 RMSE，纵向模拟应报告：

\[
\operatorname{Bias}(
\widehat\Delta
),
\qquad
\widehat\Delta
=
\widehat\theta_2-\widehat\theta_1,
\]

以及：

- 真改善被判断为无变化的比例；
- 真恶化被判断为无变化的比例；
- 变化方向判断准确率；
- minimally important change 的 sensitivity 和 specificity。

### 16.5 增加 prior tempering 或动态冲突机制

若早期作答与旧分数或自评冲突，可以扩大 prior 方差：

\[
\tau_t^2
=
h(
\text{prior-response conflict}
),
\]

或逐步降低 prior 权重：

\[
p_t(\theta)
\propto
p_0(\theta)^{\lambda_t}
\prod_{s=1}^{t}
p(u_s\mid\theta),
\qquad
0\leq\lambda_t\leq1.
\]

Bass 的 \(SD=0.25\) 失败说明，固定强 prior 缺少“承认自己错了”的机制。

### 16.6 完整消融应包含纵向条件

| 条件 | Time 2 首题 | Time 2 估计 | 目的 |
|---|---|---|---|
| A 标准复测 | \(0\) 附近 | \(N(0,1)\) | 基线 |
| B 只改首题 | \(\widehat\theta_1\) 附近 | 第一题后恢复 \(N(0,1)\) | 首题路径 |
| C 历史 prior | 当前 EAP 处 | \(N(\widehat\theta_1,\tau^2)\) | 持续 prior |
| D 稳健历史 prior | 当前 EAP 处 | 冲突时扩大 \(\tau^2\) | 动态保护 |

再与当次用户自评结合，可以检验：

\[
\text{历史分数}
\quad\text{和}\quad
\text{当前自评}
\]

在预测当前状态时谁更可靠，以及两者冲突时怎样处理。

## 17. 可以安全引用的中文转述

### 支持“复测 prior 的方差应包含变化不确定性”

> Bass 等人（2026）指出，纵向 CAT 不能仅以第一次测量的最终标准误作为第二次 prior 的不确定性；合理的 prior 方差还应包含两次测量之间真实变化的个体差异，否则旧分数会被赋予过高权重。

### 支持“小变化时中等强度 prior 可能最好”

> 在官方 PROMIS 题库的 test-retest 模拟中，当健康状态变化的标准差为 0.3 时，prior \(SD=0.5\) 通常以相同或更少题量获得较低 RMSE；仅移动 prior 均值而保持 \(SD=1\) 的收益很小。

### 支持“窄 prior 会妨碍变化检测”

> 当 prior \(SD=0.25\) 时，最少四题规则使许多 CAT 在第四题立即停止；健康状态发生变化时，旧分数对后验的强收缩导致 RMSE 上升，形成更短但更不准确的复测。

### 支持“题库覆盖决定 prior 的边际作用”

> 对位于题库高信息区域的患者，标准 PROMIS CAT 往往已经在最少四题处停止，个体化 prior 的额外收益很小；对题库覆盖不足的患者，prior 对题量和最终估计影响更大，同时风险也更高。

### 不能这样引用

- 不能写成“Bass 等人只利用上次分数选择第一题”；
- 不能把 \(SD=0.25\) 写成 prior variance \(0.25\)；
- 不能把四题停止解释为完全由四道新题获得足够信息；
- 不能声称真实患者 longitudinal CAT 已经验证了题量下降；
- 不能写成 informed prior 在所有 PROMIS 领域都提高准确性；
- 不能把小变化条件的结果推广到可能发生大幅改善或恶化的患者。

## 18. 关键参考文献及其作用

- **van der Linden（1999）**：经验初始化 CAT 能力估计。
- **Frans 等人（2023）**：临床多级计分 CAT 中经验 prior 的题量收益与错误 prior 风险。
- **Petersen 等人（2025）**：在 EORTC CAT Core 身体功能领域使用跨领域信息选择个体化首题。
- **Wang、Berger 与 Burdick（2013）**：动态 IRT 中真实轨迹变化与测量误差的 Bayesian 建模背景。
- **Terwee 等人（2021）**：PROMIS minimally important change 的概念与经验范围。
- **Choi 等人（2010）**：PROMIS 静态短表与 CAT 效率背景。
- **Morris 等人（2017）与 Bass 等人（2025）**：PROMIS 多变量 CAT 与停止规则效率研究。

## 19. 精读结论

Bass 等人把经验 prior 的问题从“辅助信息准不准”推进到“辅助信息会不会过时”：

\[
\text{旧分数的不确定性}
\neq
\text{当前状态的不确定性}.
\]

纵向 prior 的适当强度取决于：

\[
\underbrace{SE(\widehat\theta_1)^2}_{\text{上次测量误差}}
+
\underbrace{SD(\delta)^2}_{\text{真实变化差异}}.
\]

这篇论文对我们最重要的警告是：**强 prior 可以轻易制造更短的 CAT，但如果它让系统失去检测当前变化的能力，这种“效率”没有测量价值。** 因而方法贡献不应只是把 prior 设得更窄，而应当让 prior 强度与信号可靠性、时间间隔和早期作答冲突共同变化。
