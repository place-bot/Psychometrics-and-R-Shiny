# 完整验证流程

## 输入与输出

输入：

- 二分反应矩阵 \(\boldsymbol X\)；
- 初始 Q 矩阵 \(Q^{(0)}\)；
- 固定的 \(K\) 个属性及其含义；
- 一组阈值 \(\mathcal E\)；
- DINA 估计设置。

输出：

- 每个 \(\varepsilon\) 下的候选 Q；
- 改动过的 q-vector；
- 更新后的 \(g,s,\delta\)；
- 测验级 \(\bar g+\bar s\)；
- 交由内容专家复核的题目清单。

## 阶段一：拟合当前模型

在 \(Q^{(0)}\) 下拟合 DINA，得到：

\[
\widehat{\boldsymbol g}^{(0)},\quad
\widehat{\boldsymbol s}^{(0)},\quad
\widehat P(\boldsymbol\alpha_l\mid\boldsymbol X_i).
\]

同时记录原始测验级指标：

\[
C(Q^{(0)})
=
\overline{\widehat g}^{(0)}
+
\overline{\widehat s}^{(0)}.
\]

## 阶段二：建立后验期望计数

对所有 \(j,l\) 计算：

\[
N_{jl}=\sum_i\widehat p_{il},
\qquad
R_{jl}=\sum_iX_{ij}\widehat p_{il}.
\]

这一步只做一次。

## 阶段三：逐题顺序搜索

对每道题 \(j\) 和每个 \(\varepsilon\)：

```text
selected = empty
previous_delta = undefined

for s = 1,...,K:
    candidates = selected plus each remaining attribute
    compute g, s, delta for every candidate
    best = candidate with largest delta

    if this is the first step:
        accept best
    else if best.delta - previous_delta > epsilon:
        accept best
    else:
        stop and retain the previous candidate
```

得到该题在阈值 \(\varepsilon\) 下的建议行

\[
\widehat{\boldsymbol q}_j(\varepsilon).
\]

## 阶段四：拼成候选 Q

\[
\widehat Q(\varepsilon)
=
\begin{bmatrix}
\widehat{\boldsymbol q}_1(\varepsilon)\\
\vdots\\
\widehat{\boldsymbol q}_J(\varepsilon)
\end{bmatrix}.
\]

较小 \(\varepsilon\) 更容易接受新增属性，候选 Q 往往更密；较大 \(\varepsilon\) 要求每次新增带来更明显的区分度提升，候选 Q 往往更稀。

## 阶段五：追加 EM

论文在每套候选 Q 下追加若干 EM 循环，更新：

\[
\widehat{\boldsymbol g}(\varepsilon),\quad
\widehat{\boldsymbol s}(\varepsilon),\quad
\widehat p_{il}(\varepsilon).
\]

模拟中追加 5 个 EM cycles；分数减法中追加 100 个；NAEP 中追加 10 个。

## 阶段六：全测验比较

计算

\[
C\{\widehat Q(\varepsilon)\}
=
\overline{\widehat g}(\varepsilon)
+
\overline{\widehat s}(\varepsilon).
\]

并同时比较：

- 与原 Q 相同的格子比例；
- 与原 Q 相同的整行比例；
- 改动集中在哪些题；
- 每题 \(\delta\) 的改善或恶化；
- 修改后的属性解释能否成立。

## 阶段七：实质审核

建议把每道被改动题整理成：

| 内容 | 问题 |
| --- | --- |
| 原 q-vector | 专家最初为何要求这些属性？ |
| 推荐 q-vector | 新增或删除了哪些属性？ |
| 参数变化 | \(g,s,\delta\) 改善多少？ |
| 题目文本 | 替代策略、线索和语言负荷是什么？ |
| 作答证据 | 口语报告或过程数据支持哪个解释？ |
| 最终决策 | 保留、修改、删除题目或重构属性？ |

算法产生统计建议，最终 Q 应当记录统计与内容证据的联合理由。

