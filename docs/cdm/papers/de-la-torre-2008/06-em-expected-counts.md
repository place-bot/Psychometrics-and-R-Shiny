# EM 后验期望计数

## 直接重估为什么昂贵

最直接的方案是：

1. 换一行 q-vector；
2. 在整套数据上重新拟合 DINA；
3. 得到新的 \(g_j,s_j,\delta_j\)；
4. 对下一候选重复。

即使使用顺序搜索，若每题每个候选都完整重估，最坏仍需大量 EM 拟合。本文的关键计算简化来自 E-step 的后验权重。

## 一次 DINA 拟合

在当前 Q 矩阵下，E-step 计算

\[
\widehat p_{il}
=
\widehat P(\boldsymbol\alpha_l\mid\boldsymbol X_i),
\]

其中 \(l=0,\ldots,2^K-1\)。

对题目 \(j\) 和属性模式 \(l\)，定义：

\[
N_{jl}
=
\sum_{i=1}^{N}\widehat p_{il},
\]

\[
R_{jl}
=
\sum_{i=1}^{N}X_{ij}\widehat p_{il}.
\]

\(N_{jl}\) 是该模式下的后验期望人数，\(R_{jl}\) 是后验期望答对人数。原文用 \(N_j^{(\eta)}\) 和 \(R_j^{(\eta)}\) 表示聚合到理想反应组后的计数。

## 候选 q-vector 只改变聚合方式

给定候选 \(\boldsymbol q_{jl'}\)，对每个模式计算

\[
\eta_{ll'}=\prod_{k=1}^{K}\alpha_{lk}^{q_{jl'k}}.
\]

然后把模式级期望计数聚合为：

\[
N_{jl'}^{(h)}
=
\sum_{l:\eta_{ll'}=h}N_{jl},
\qquad h\in\{0,1\},
\]

\[
R_{jl'}^{(h)}
=
\sum_{l:\eta_{ll'}=h}R_{jl}.
\]

候选参数可直接计算：

\[
\widehat g_{jl'}
=
\frac{R_{jl'}^{(0)}}{N_{jl'}^{(0)}},
\]

\[
\widehat s_{jl'}
=
\frac{N_{jl'}^{(1)}-R_{jl'}^{(1)}}{N_{jl'}^{(1)}},
\]

\[
\widehat\delta_{jl'}
=
1-\widehat s_{jl'}-\widehat g_{jl'}.
\]

整个候选比较过程只需加总已经存在的期望计数。

## 一个四模式小例子

设 \(K=2\)，某题的后验期望计数为：

| 模式 | \(N_{jl}\) | \(R_{jl}\) |
| :---: | ---: | ---: |
| 00 | 20 | 4 |
| 01 | 30 | 9 |
| 10 | 25 | 10 |
| 11 | 25 | 20 |

候选 \(q=11\) 时，只有模式 11 进入 \(\eta=1\)：

\[
\widehat g
=\frac{4+9+10}{20+30+25}
=\frac{23}{75}
=.307,
\]

\[
\widehat s
=\frac{25-20}{25}
=.20,
\]

\[
\widehat\delta=.493.
\]

候选 \(q=10\) 时，10 和 11 都进入 \(\eta=1\)：

\[
\widehat g
=\frac{4+9}{20+30}
=.26,
\]

\[
\widehat s
=\frac{(25+25)-(10+20)}{50}
=.40,
\]

\[
\widehat\delta=.34.
\]

第二个候选漏掉属性 2，mastery 组混入模式 10，slip 上升。

## 近似从哪里来

候选计算沿用当前 Q 拟合得到的

\[
\widehat P(\boldsymbol\alpha_l\mid\boldsymbol X_i),
\]

没有为每个新 q-vector 立即重算后验。若初始 Q 错误较多，项目参数与后验本身可能偏差明显，候选 \(\widehat\delta\) 也会受影响。

论文的处理是：

- 先用快速重分组生成候选 Q；
- 再在候选 Q 下运行少量追加 EM 循环；
- 用更新后的全测验指标比较不同 \(\varepsilon\) 解。

