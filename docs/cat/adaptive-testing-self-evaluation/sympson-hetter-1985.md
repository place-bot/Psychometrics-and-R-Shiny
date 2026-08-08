# Sympson–Hetter（1985）：CAT 题目曝光控制方法

## 方法身份

> Sympson, J. B., & Hetter, R. D. (1985, October). *Controlling item-exposure rates in computerized adaptive testing*. In *Proceedings of the 27th Annual Meeting of the Military Testing Association* (pp. 973–977). San Diego, CA: Navy Personnel Research and Development Center.

- 方法类型：计算机化自适应测验（Computerized Adaptive Testing, CAT）的概率式最大曝光控制
- 控制对象：每道题在总体受测者中被实际施测的比例
- 核心工具：题目特异的接受概率与离线 Monte Carlo 模拟
- 清晰的开放全文说明：[Stocking（1993），*Controlling Item Exposure Rates in a Realistic Adaptive Testing Paradigm*](https://files.eric.ed.gov/fulltext/ED384663.pdf)

!!! abstract "一句话结论"
    Sympson–Hetter 方法先让 CAT 按原有规则选出最优题，再用该题自己的曝光参数决定是否真正施测。它能够压低热门题的总体曝光率，但会拒绝一部分最优题、损失测验信息，而且不能自动保护特定能力或自评群体内部的条件曝光。

## 1. 为什么 CAT 需要曝光控制

如果 CAT 每一步都选择当前信息量最大的题：

\[
j_t
=
\arg\max_{j\in\mathcal R_t}
I_j(\widehat\theta_{t-1}),
\]

相似能力、相似作答路径的受测者就会反复遇到相同题目。第一题尤其危险：如果所有人的初始能力都设为 \(0\)，大量受测者会从同一批中等难度、高区分度题开始。

题目曝光率可以写成：

\[
\widehat P_i(A)
=
\frac{\text{题目 }i\text{ 被实际施测的人数}}
{\text{受测者总人数}}.
\]

这里的 \(A_i\) 表示 item \(i\) was administered，即题目 \(i\) 被真正呈现给受测者。曝光率过高会带来：

1. 题目被记忆、传播或泄露的风险；
2. 少数优质题快速消耗，题库维护成本上升；
3. 不同受测者获得高度重叠的测验；
4. 大量已经开发和校准的题目几乎从不使用。

Sympson–Hetter 方法主要解决第一类问题：**限制任何单道题的最高总体曝光率。**

## 2. 最关键的区分：被选中不等于被施测

该方法区分两个事件：

- \(S_i\)：题目 \(i\) 被 CAT 选题算法选中；
- \(A_i\)：题目 \(i\) 最终被实际施测。

只有先被选中，题目才可能被施测，因此：

\[
A_i\subseteq S_i.
\]

题目 \(i\) 的实际曝光率可以分解为：

\[
P_i(A)
=
P_i(A\mid S)P_i(S).
\]

令

\[
K_i=P_i(A\mid S),
\]

其中 \(K_i\in[0,1]\) 是题目 \(i\) 的 **exposure control parameter**，即曝光控制参数。于是：

\[
P_i(A)=K_iP_i(S).
\]

这三个概率分别回答：

| 符号 | 含义 | 由什么决定 |
|---|---|---|
| \(P_i(S)\) | 题目被选题算法选中的概率 | 题库、能力分布、初始值、选题规则、内容约束和停止规则 |
| \(K_i=P_i(A\mid S)\) | 被选中以后允许施测的概率 | Sympson–Hetter 标定得到的题目参数 |
| \(P_i(A)\) | 最终实际曝光率 | 前两者共同决定 |

!!! note "它控制的不是选题概率"
    热门题仍然可能经常被最大信息量规则选中。Sympson–Hetter 方法不改变它为何成为最优题，而是在它被选中以后增加一道接受或拒绝关卡。

## 3. 实际施测时怎样运行

假设当前 CAT 根据能力估计、内容约束等条件选出了题目 \(i\)：

1. 从均匀分布生成随机数 \(U\sim\operatorname{Uniform}(0,1)\)；
2. 如果 \(U\le K_i\)，实际施测题目 \(i\)；
3. 如果 \(U>K_i\)，不向受测者展示题目 \(i\)，并将它从该受测者本次可用题目中暂时移出；
4. 从剩余题目中选择下一道最优题，再做一次接受或拒绝判断；
5. 直到找到一题可以实际施测。

> CAT 选出当前最优题 \(i\) → 抽取 \(U\sim\operatorname{Uniform}(0,1)\) → 若 \(U\le K_i\) 则施测；否则本次跳过题目 \(i\)，转向下一道最优题。

被拒绝的题不会显示给受测者，也不会被记作一道作答题。算法只是退而选择信息量或约束适配程度稍低的候选题。

!!! note "怎样保证最后一定有题可用"
    对固定长度为 \(n\) 的测验，经典实现会确保题库中至少有 \(n\) 道题的 \(K_i=1\)；否则极端情况下可能连续拒绝所有剩余候选题，无法完成测验。含内容区块的 CAT 还要在每个必须抽题的区块中保留足够多 \(K_i=1\) 的题。现代实现也可以设置明确的后备选题规则。

## 4. 一个具体数值例子

假设目标最大曝光率为：

\[
r_{\max}=0.20.
\]

模拟发现，若没有接受或拒绝关卡，题目 \(i\) 会被 \(50\%\) 的受测者选中：

\[
P_i(S)=0.50.
\]

若把它的接受概率设为：

\[
K_i
=
\frac{r_{\max}}{P_i(S)}
=
\frac{0.20}{0.50}
=
0.40,
\]

那么它的预期实际曝光率就是：

\[
P_i(A)
=
K_iP_i(S)
=
0.40\times0.50
=
0.20.
\]

也就是说，这道题虽然经常成为算法的第一选择，但平均只有 \(40\%\) 的入选会变成实际施测。

如果另一道题只有：

\[
P_j(S)=0.08<r_{\max},
\]

便可以设 \(K_j=1\)。它每次被选中都可以施测，因为即使完全接受，预期曝光率也不会超过 \(0.20\)。

## 5. 为什么不能直接算一次 \(K_i\)

看起来可以直接使用：

\[
K_i
=
\min\left(1,\frac{r_{\max}}{P_i(S)}\right).
\]

问题是 \(P_i(S)\) 不是一个预先固定的题目属性。它会受到整个 CAT 系统的影响：

- 题库中其他题目的参数；
- 受测者能力分布；
- 初始能力估计或先验；
- 选题准则；
- 内容平衡与敌对题约束；
- 固定长度或可变长度停止规则；
- 其他题目的 \(K_j\)。

当热门题 \(i\) 被拒绝以后，下一道候选题 \(j\) 会更频繁地被选中；于是 \(P_j(S)\) 上升，它原来的 \(K_j\) 可能也不再足够。拒绝会产生连锁反应，因此所有 \(K_i\) 必须联合标定。

## 6. 离线 Monte Carlo 标定

经典实现使用反复模拟来得到每道题的 \(K_i\)：

1. 固定完整的 CAT 设计，包括题库、能力估计、选题、内容约束、曝光目标和停止规则；
2. 从预计的真实能力分布中生成大量模拟受测者；
3. 初始化所有题目 \(K_i^{(0)}=1\)，即第一轮不进行曝光限制；
4. 模拟完整 CAT，记录每道题的选择率 \(\widehat P_i(S)\) 和实际曝光率 \(\widehat P_i(A)\)；
5. 更新曝光参数：

\[
K_i^{\text{new}}
=
\begin{cases}
r_{\max}/\widehat P_i(S),&
\widehat P_i(S)>r_{\max},\\[4pt]
1,&
\widehat P_i(S)\le r_{\max};
\end{cases}
\]

6. 用新的 \(K_i\) 重新模拟；
7. 重复更新，直到最高观察曝光率稳定在目标值附近；
8. 将最后一轮的 \(K_i\) 用于正式 CAT。

!!! warning "目标值不是每一批数据中的硬上限"
    \(r_{\max}\) 控制的是模型和模拟条件下的预期曝光。有限样本的随机波动、真实能力分布与模拟分布不一致、题目参数误差或系统规则改变，都可能使正式施测中的观察曝光率超过目标。

Stocking（1993）的示例从全部 \(K_i=1\) 开始，经过多轮模拟才使最大曝光率趋于稳定。这也说明 \(K_i\) 不是题目的永久属性，而是“这道题在当前整套 CAT 系统中应被接受多少次”的系统参数。

## 7. 为什么它会损失信息量

没有曝光控制时，算法可以施测最优题 \(i^*\)：

\[
i^*
=
\arg\max_i I_i(\widehat\theta).
\]

如果 \(i^*\) 被曝光关卡拒绝，系统只能改用次优题 \(j\)，通常有：

\[
I_j(\widehat\theta)
<
I_{i^*}(\widehat\theta).
\]

因此，曝光控制与单题测量效率之间存在直接权衡：

\[
\text{更强的题库保护}
\quad\Longleftrightarrow\quad
\text{更多次拒绝最优题}
\quad\Longleftrightarrow\quad
\text{更低的累计信息}.
\]

在固定长度 CAT 中，这可能表现为更大的标准误或均方根误差；在以精度为停止标准的可变长度 CAT 中，则可能表现为需要更多题才能达到同一个停止阈值。

van der Linden（1999）转述 Thomasson（1995）的结果称，Sympson–Hetter 方法在 \(\theta\) 分布中间区域约损失 \(15\%\) 的信息，更严格的方法在整个 \(\theta\) 范围内最高可损失 \(40\%\)。这组数字应当理解为特定研究条件下的结果，不是该方法在所有题库中的固定损失率；而且这里是 van der Linden 对一篇会议论文的二手引用，不是 Sympson and Hetter（1985）原文的结论。

## 8. 为什么中间能力者可能损失更多

若真实能力分布在 \(0\) 附近最密集，中等能力受测者数量最多。适合这一群体的中等难度、高信息题最容易被频繁选中，因此往往得到较小的 \(K_i\)。

极端能力受测者较少，适合题库两端的题即使对该群体非常热门，在总体中的选择率也可能不高，因此其 \(K_i\) 常接近 \(1\)。

结果可能是：

| 能力区域 | 人数 | 最优题的总体选择率 | 常见 \(K_i\) | 信息损失 |
|---|---:|---:|---:|---:|
| 中间 | 多 | 高 | 较小 | 较明显 |
| 两端 | 少 | 低 | 接近 \(1\) | 较小 |

这解释了为什么 Stocking（1993）观察到：Sympson–Hetter 控制下，中间分数区域的条件测量标准误比尾部增加得更多。

## 9. 最大局限：总体曝光安全不等于群体内部安全

经典 Sympson–Hetter 控制的是总体边际曝光率：

\[
P_i(A).
\]

它不自动控制特定能力位置上的条件曝光率：

\[
P_i(A\mid\theta),
\]

也不自动控制特定自评档次内的曝光率：

\[
P_i(A\mid C=c).
\]

例如，高能力者只占总体的 \(5\%\)。某道极难题被几乎所有高能力者看到、其他人完全看不到，那么：

\[
P_i(A)\approx0.05,
\]

低于 \(r_{\max}=0.10\)，总体指标看起来很安全；但：

\[
P_i(A\mid\theta\text{ 很高})\approx1.
\]

这道题对高能力群体几乎完全暴露。Stocking（1993）明确指出，题目的总体曝光率可能很低，但它仍可能被某个能力水平的几乎所有受测者看到。

条件版 Sympson–Hetter 可以在若干 \(\theta\) 区间内分别标定 \(K_i(\theta)\)，但需要更大的模拟样本、更复杂的参数标定，也会面对早期 \(\widehat\theta\) 不稳定的问题。

## 10. 它还不能自动解决什么

### 不能保证题库利用均匀

经典方法主要压低最高曝光率，不会主动提高从未被选中的低质量或不匹配题目的使用率。于是可能同时出现：

- 少数题仍接近 \(r_{\max}\)；
- 大量题曝光率接近 \(0\)。

后来的两阶段 Sympson–Hetter 等方法才进一步尝试同时控制最低和最高曝光率。

### 不能直接控制 test overlap

单题最大曝光下降通常会降低两名受测者之间的题目重叠，但两者不是同一个约束。固定长度为 \(L\) 时，平均成对重叠率可以写为：

\[
\overline O
=
\frac{\sum_i n_i(n_i-1)}
{N(N-1)L},
\]

其中 \(n_i\) 是题目 \(i\) 的施测人数，\(N\) 是受测者总数。研究仍应直接报告 test overlap，而不能只报告 \(\max_i\widehat P_i(A)\)。

### 不能永久沿用同一组参数

只要改变以下任何部分，选择率 \(P_i(S)\) 就可能改变：

- 增删题目；
- 改变能力分布；
- 改变起始值或先验；
- 改变选题规则；
- 改变内容约束；
- 改变测验长度或停止规则。

因此通常需要重新标定 \(K_i\)。van der Linden 后来还指出，经典离线迭代耗时，并不总能平稳得到满足目标的参数；这推动了 on-the-fly 和 item-eligibility 等在线替代方法。

## 11. 与随机选前几名题有什么区别

| 方法 | 怎样引入随机性 | 直接控制什么 | 主要问题 |
|---|---|---|---|
| Randomesque | 从信息量最高的前若干题中随机抽一题 | 候选集内的选择分散 | 很难事先知道最终最大曝光率 |
| Sympson–Hetter | 先选最优题，再按该题 \(K_i\) 接受或拒绝 | 每道题的预期总体曝光率 | 需要反复模拟标定 |
| Hard cap / restricted | 达到上限后直接禁用题目 | 观察曝光率硬上限 | 上限附近可能突然改变选题行为 |
| \(a\)-stratified | 早期用低 \(a\) 层，后期开放高 \(a\) 层 | 高区分度题的使用时机 | 不直接给每道题一个曝光上限 |

这些方法可以组合。例如，先按 \(a\) 层与内容约束形成候选集，再用 Sympson–Hetter 控制候选题的实际施测概率。

## 12. 它与自评起点方法是怎样的关系

两类方法分别作用在概率分解的不同部分：

\[
\underbrace{P_i(A)}_{\text{最终曝光}}
=
\underbrace{P_i(A\mid S)}_{\text{Sympson–Hetter 控制}}
\times
\underbrace{P_i(S)}_{\text{自评起点与选题规则影响}}.
\]

自评起点把不同受测者送往不同的 \(b\) 区域，主要改变 \(P_i(S)\)：减少所有人从共同中点出发造成的选择集中。

Sympson–Hetter 则控制 \(P_i(A\mid S)\)：即使某道题仍经常成为最优候选，也只允许其中一部分选择变成实际施测。

因此两者不是竞争关系，而是可以互补：

> 自评或背景信息 → 个体化先验或初始位置 → 形成与 \(b\) 匹配的候选区域 → 按信息量、\(a\) 层和内容约束选出候选题 → Sympson–Hetter 接受或拒绝 → 实际施测

但必须注意：自评起点改变了 \(P_i(S)\)，所以不能直接沿用标准起点条件下标定的 \(K_i\)。每一种起点方法都应单独重新标定曝光参数，否则比较并不公平。

## 13. 对本专题最直接的实验设计

可以先做一个清晰的 \(2\times2\) 消融：

| 起点 | 曝光控制 | 回答的问题 |
|---|---|---|
| 共同起点 | 无 | 标准最大信息量 CAT 的精度与曝光基线 |
| 共同起点 | Sympson–Hetter | 直接曝光控制单独能做什么 |
| 自评起点 | 无 | 分散 \(P_i(S)\) 本身能做什么 |
| 自评起点 | Sympson–Hetter | 两种机制结合后是否互补 |

四组使用相同题库、能力估计器、内容约束和停止规则。对于两个使用 Sympson–Hetter 的条件，应分别标定各自的 \(K_i\)。

至少同时报告：

1. 偏差、均方根误差（root mean square error, RMSE）与覆盖率；
2. 达到同一精度所需的平均题量及尾部题量；
3. 最大总体曝光率 \(\max_i\widehat P_i(A)\)；
4. 题库曝光率分布与有效使用题数；
5. 按真实 \(\theta\) 分组的条件曝光率；
6. 按自评档次 \(C\) 分组的条件曝光率；
7. 第一题曝光率与第一题有效题库规模；
8. test overlap。

!!! tip "你们方法可能呈现的真正贡献"
    如果自评起点使 \(P_i(S)\) 本身更加分散，就可能在达到相同最大曝光目标时需要较少的拒绝，从而保留更多测验信息。最有意义的结果不是单独证明“曝光更低”，而是证明在相同曝光安全水平下，题量更短或估计更精确。

## 14. 阅读 Zhu and Fan（1999）时怎样理解 \(0.90\) 和 \(0.10\)

Zhu and Fan 把 Sympson–Hetter 的目标曝光水平设置为 \(0.90\) 或 \(0.10\)：

- \(r_{\max}=0.90\)：控制很宽松，热门题大多仍可施测；
- \(r_{\max}=0.10\)：控制很严格，热门题会频繁被拒绝，更多替代题进入测验。

所以 \(0.10\) 不是“每道被选中的题只有 \(10\%\) 的概率施测”。每道题有自己的 \(K_i\)：

- 热门题的 \(K_i\) 可能很小；
- 本来就不热门的题可能有 \(K_i=1\)；
- 最终目标是 \(P_i(A)\le0.10\)，不是要求所有 \(K_i=0.10\)。

这也解释了 Zhu and Fan 的结果：严格控制使 No-Info 方法不得不使用更多中等难度替代题，整体题目使用看起来更分散；但它没有消除共同中间起点造成的选择压力。

## 参考文献

- Chao, H.-Y., & Chen, J.-H. (2023). Controlling the minimum item exposure rate in computerized adaptive testing: A two-stage Sympson–Hetter procedure. *Applied Psychological Measurement, 47*(7–8), 460–477. [开放全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10664747/) · [DOI](https://doi.org/10.1177/01466216231209756)
- Stocking, M. L. (1993). *Controlling item exposure rates in a realistic adaptive testing paradigm* (ETS Research Report RR-93-02). Educational Testing Service. [ERIC 全文 PDF](https://files.eric.ed.gov/fulltext/ED384663.pdf) · [DOI](https://doi.org/10.1002/j.2333-8504.1993.tb01513.x)
- Sympson, J. B., & Hetter, R. D. (1985). Controlling item-exposure rates in computerized adaptive testing. In *Proceedings of the 27th Annual Meeting of the Military Testing Association* (pp. 973–977).
- van der Linden, W. J. (1999). Empirical initialization of the trait estimator in adaptive testing. *Applied Psychological Measurement, 23*(1), 21–29. [DOI](https://doi.org/10.1177/01466219922031149)
- van der Linden, W. J. (2006). *A formal characterization of and some alternatives to Sympson–Hetter item-exposure control in computerized adaptive testing* (LSAC Computerized Testing Report 02-05). Law School Admission Council. [出版信息与全文入口](https://research.utwente.nl/en/publications/a-formal-characterization-of-and-some-alternatives-to-sympson-het/)
