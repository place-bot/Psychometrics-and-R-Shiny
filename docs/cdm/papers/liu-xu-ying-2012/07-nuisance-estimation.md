# 未知 \(c,g,p\) 与 DINA EM

原文说 \((\widehat{\boldsymbol c},\widehat{\boldsymbol g},\widehat{\boldsymbol p})\) 可用 EM 高效计算，但没有逐步写出更新式。下面补齐固定 Q 时的标准 DINA EM。

## E 步

对学生 \(i\) 和属性模式 \(\boldsymbol\alpha\)，后验权重

\[
\tau_{i\boldsymbol\alpha}
=
\Pr(\boldsymbol\alpha_i=\boldsymbol\alpha
\mid \boldsymbol R_i,Q,\boldsymbol c,\boldsymbol g,\boldsymbol p)
\]

满足

\[
\tau_{i\boldsymbol\alpha}
=
\frac{
p_{\boldsymbol\alpha}
\prod_j
\pi_{j\boldsymbol\alpha}^{R_i^j}
(1-\pi_{j\boldsymbol\alpha})^{1-R_i^j}
}{
\sum_{\boldsymbol\alpha'}
p_{\boldsymbol\alpha'}
\prod_j
\pi_{j\boldsymbol\alpha'}^{R_i^j}
(1-\pi_{j\boldsymbol\alpha'})^{1-R_i^j}
}.
\]

## M 步：属性分布

\[
p_{\boldsymbol\alpha}^{\text{new}}
=
\frac1N\sum_{i=1}^N\tau_{i\boldsymbol\alpha}.
\]

## M 步：掌握组答对率

令 \(\xi_{j\boldsymbol\alpha}\) 为理想反应，

\[
c_j^{\text{new}}
=
\frac{
\sum_i\sum_{\boldsymbol\alpha}
\tau_{i\boldsymbol\alpha}
\xi_{j\boldsymbol\alpha}R_i^j
}{
\sum_i\sum_{\boldsymbol\alpha}
\tau_{i\boldsymbol\alpha}
\xi_{j\boldsymbol\alpha}
}.
\]

## M 步：非掌握组答对率

\[
g_j^{\text{new}}
=
\frac{
\sum_i\sum_{\boldsymbol\alpha}
\tau_{i\boldsymbol\alpha}
(1-\xi_{j\boldsymbol\alpha})R_i^j
}{
\sum_i\sum_{\boldsymbol\alpha}
\tau_{i\boldsymbol\alpha}
(1-\xi_{j\boldsymbol\alpha})
}.
\]

## 从 EM 到 \(\widehat S(Q)\)

对每个候选 Q：

1. 构造全部 \(2^K\) 个属性模式；
2. 运行 EM 得到 \(\widehat c,\widehat g,\widehat p\)；
3. 由候选 Q 和 \(\widehat c,\widehat g\) 构造 \(T\)；
4. 计算 \(T\widehat p\)；
5. 与固定的样本 \(\boldsymbol\beta\) 求欧氏距离。

## 计算注意

- 用 log-sum-exp 计算后验，避免大量题目概率连乘下溢；
- \(p_{\boldsymbol\alpha}\) 接近 0 时要防止 \(\log0\)；
- 若 q-vector 为全零，所有模式均进入理想掌握组，该题的 \(g_j\) 无法由数据识别；
- EM 可能依赖初值，候选 Q 的公平比较需要一致的初始化与收敛规则；
- 原文没有报告这些工程设置。

本站脚本把这部分实现为 `fit_dina_em()`，并由 `profiled_objective()` 完成式 (17) 的组合。
