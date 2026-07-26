# Metropolis-within-Gibbs 完整算法

## 初始化

随机初始化：

\[
\boldsymbol\alpha^{(0)},\quad
\boldsymbol\pi^{(0)},\quad
Q^{(0)}\in\mathcal Q,\quad
\boldsymbol g^{(0)},\quad
\boldsymbol s^{(0)}.
\]

题目参数需满足

\[
0\le g_j^{(0)}<1-s_j^{(0)}\le1.
\]

原始代码的 `random_Q(J,K)` 先放入两套 \(I_K\)，构造非零的剩余行与列，再随机打乱行。

## 一轮迭代

### Step A：更新猜测率

\[
\boldsymbol g^{(t)}
\sim
p(\boldsymbol g\mid
\boldsymbol Y,\boldsymbol s^{(t-1)},
\boldsymbol\alpha^{(t-1)},Q^{(t-1)}).
\]

逐题使用截断 Beta 条件分布。

### Step B：更新失误率

\[
\boldsymbol s^{(t)}
\sim
p(\boldsymbol s\mid
\boldsymbol Y,\boldsymbol g^{(t)},
\boldsymbol\alpha^{(t-1)},Q^{(t-1)}).
\]

### Step C：更新学生属性

\[
\boldsymbol\alpha_i^{(t)}
\sim
\operatorname{Categorical}
\left(
\frac{w_{i1}}{\sum_cw_{ic}},\ldots,
\frac{w_{iC}}{\sum_cw_{ic}}
\right).
\]

### Step D：更新潜在类比例

\[
\boldsymbol\pi^{(t)}
\sim
\operatorname{Dirichlet}
(\boldsymbol\delta_0+\boldsymbol n^{(t)}).
\]

### Step E：更新 Q

1. 用 DS2 产生 \(Q^\star\in\mathcal Q\)；
2. 计算条件似然比；
3. 按 MH 规则接受或拒绝。

## 伪代码

```text
initialize alpha, pi, s, g, Q in identified space
for t = 1, ..., T:
    draw g from its truncated-Beta conditionals
    draw s from its truncated-Beta conditionals
    draw every alpha_i from 2^K class probabilities
    draw pi from its Dirichlet conditional
    choose one Q column and B item positions
    construct an identified DS2 proposal Q*
    accept Q* with min(1, likelihood(Q*) / likelihood(Q))
    after burn-in, save Q, s, g, pi, alpha
```

## 论文实验设置

MH 方法使用：

\[
B=2K,
\qquad
T=30{,}000,
\qquad
\text{burn-in}=15{,}000.
\]

预实验中 DS2 接受率在 18%--25% 之间。

## 每轮主要计算

粗略看：

- 属性更新需要 \(O(NJ2^K)\)；
- 题目参数更新需要 \(O(NJ)\)；
- Q 的候选构造需要检查局部结构；
- MH 比值对 \(N\times B\) 个受影响作答计算。

属性更新中的 \(2^K\) 是属性数扩展的主要障碍之一。

## 补充代码中的实现顺序

公开 `DINA_MH_Q()` 的实际顺序是：

1. `update_alpha()` 同时更新 \(\boldsymbol\alpha,\boldsymbol\pi\)；
2. `update_sg()` 更新 \(\boldsymbol s,\boldsymbol g\)；
3. `updateQ_MH()` 提出并更新 Q。

Gibbs 分块次序不同仍可以以同一联合后验为平稳分布，只要每一步使用相应条件分布。

[下一页：受限 Gibbs 完整算法](16-constrained-gibbs.md)
