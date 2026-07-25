# PVAF 穷举搜索与阈值

## 第一步：计算所有非零候选

\(K\) 个属性共有

\[
2^K-1
\]

个非零 q-vector。对每道题逐一计算：

\[
\widehat{\varsigma}_j^2(\boldsymbol q).
\]

全属性向量

\[
\boldsymbol 1=(1,\ldots,1)
\]

产生最细分组，并作为样本最大值基准。

## 第二步：转换成 PVAF

\[
\operatorname{PVAF}_j(\boldsymbol q)
=
\frac{
\widehat{\varsigma}_j^2(\boldsymbol q)
}{
\widehat{\varsigma}_j^2(\boldsymbol 1)
}.
\tag{12}
\]

原文将

\[
\operatorname{PVAF}_j(\boldsymbol q)\ge\varepsilon
\]

的候选视为经验上 appropriate。模拟与真实数据都使用

\[
\varepsilon=.95.
\]

## 第三步：最简性

令候选集合为

\[
\mathcal C_j(\varepsilon)
=
\left\{
\boldsymbol q:
\operatorname{PVAF}_j(\boldsymbol q)\ge\varepsilon
\right\}.
\]

选择属性数最少的候选：

\[
\widehat K_j
=
\min_{\boldsymbol q\in\mathcal C_j}
\sum_k q_k.
\]

若同一属性数下有多个候选，再选择

\[
\widehat{\varsigma}_j^2
\]

最大的一个。

## 伪代码

```text
for item j:
    for each nonzero q in {0,1}^K:
        collapse full latent classes using q
        calculate group weights and group success probabilities
        calculate GDI(q)

    PVAF(q) = GDI(q) / GDI(11...1)
    keep q with PVAF(q) >= epsilon
    keep the smallest number of required attributes
    break a same-size tie by the largest GDI
```

## 复杂度

单题候选数随 \(K\) 指数增长：

| \(K\) | 候选数 |
| ---: | ---: |
| 5 | 31 |
| 10 | 1023 |
| 15 | 32767 |
| 20 | 1048575 |

论文实验固定 \(K=5\)，穷举很轻。大属性空间需要优先搜索、逐步搜索或结构约束。

## 阈值的含义

\(\varepsilon=.95\) 表示候选需保留饱和分组至少 95% 的组间成功率方差。

- 较小 \(\varepsilon\)：更容易接受短 q-vector，漏设风险增加；
- 较大 \(\varepsilon\)：更接近饱和分组，增设风险增加；
- 项目效应弱、样本小或属性高度相关时，敏感性更强。

这个阈值是调节最简性与信息保留的设计参数。

## 与 2008 年阈值的区别

2008 年算法比较相邻步骤：

\[
\widehat\delta^{(s)}
-\widehat\delta^{(s-1)}
>\varepsilon.
\]

2016 年算法比较候选与饱和向量：

\[
\frac{\widehat{\varsigma}^2(\boldsymbol q)}
{\widehat{\varsigma}^2(\boldsymbol1)}
\ge\varepsilon.
\]

一个是增量阈值，一个是保留比例。
