# RLCM 数据生成过程与全部对象

## 1. 观测反应

被试的二元反应向量写作

\[
\boldsymbol R=(R_1,\ldots,R_J)^\top\in\{0,1\}^{J}.
\]

\(R_j=1\) 表示第 \(j\) 题出现正反应，在教育测验中通常对应答对。

## 2. 潜在属性模式

\[
\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_K)^\top
\in\{0,1\}^{K}.
\]

\(\alpha_k=1\) 表示掌握第 \(k\) 个属性。全部 \(2^K\) 个模式的总体比例为

\[
\boldsymbol p=
\left(p_{\boldsymbol\alpha}:
\boldsymbol\alpha\in\{0,1\}^{K}\right)^\top,
\]

并假设

\[
p_{\boldsymbol\alpha}>0,\qquad
\sum_{\boldsymbol\alpha}p_{\boldsymbol\alpha}=1.
\]

严格正比例是主定理的重要参数空间假设。

## 3. Q 矩阵

\[
Q=(q_{jk})_{J\times K}\in\{0,1\}^{J\times K}.
\]

- \(q_{jk}=1\)：题 \(j\) 需要属性 \(k\)；
- 第 \(j\) 行 \(\boldsymbol q_j\)：题 \(j\) 的完整属性要求；
- 第 \(k\) 列：哪些题测量属性 \(k\)。

定义偏序

\[
\boldsymbol\alpha\succeq\boldsymbol q_j
\quad\Longleftrightarrow\quad
\alpha_k\ge q_{jk}\ \text{对所有 }k.
\]

这表示被试掌握题 \(j\) 所需的全部属性。

## 4. 局部独立

给定 \(\boldsymbol\alpha\) 后，各题反应条件独立：

\[
\Pr(\boldsymbol R=\boldsymbol r\mid
\boldsymbol\alpha,Q,\Theta)
=
\prod_{j=1}^{J}
\theta_{j,\boldsymbol\alpha}^{r_j}
(1-\theta_{j,\boldsymbol\alpha})^{1-r_j},
\]

其中

\[
\theta_{j,\boldsymbol\alpha}
=
\Pr(R_j=1\mid\boldsymbol\alpha).
\]

混合掉潜类后，

\[
\Pr(\boldsymbol R=\boldsymbol r\mid Q,\Theta,\boldsymbol p)
=
\sum_{\boldsymbol\alpha\in\{0,1\}^{K}}
p_{\boldsymbol\alpha}
\prod_{j=1}^{J}
\theta_{j,\boldsymbol\alpha}^{r_j}
(1-\theta_{j,\boldsymbol\alpha})^{1-r_j}.
\]

## 5. Q 对参数施加的限制

本文一般 RLCM 假设单调性：

\[
\theta_{j,\boldsymbol\alpha}>
\theta_{j,\boldsymbol\alpha'}
\quad
\text{只要}\quad
\boldsymbol\alpha\succeq\boldsymbol q_j,\ 
\boldsymbol\alpha'\nsucceq\boldsymbol q_j.
\]

掌握全部所需属性的潜类具有更高正反应概率。

常见 RLCM 还满足无关属性不改变题目反应概率：

\[
\boldsymbol\alpha\odot\boldsymbol q_j
=
\boldsymbol\alpha'\odot\boldsymbol q_j
\quad\Longrightarrow\quad
\theta_{j,\boldsymbol\alpha}
=
\theta_{j,\boldsymbol\alpha'}.
\]

\(\odot\) 表示逐元素乘积。

## 6. 两步生成图

```text
潜类比例 p
    │
    └── 抽取属性模式 α
              │
              ├── Q 指定题目依赖哪些属性
              └── Θ 给出每题正反应概率
                         │
                         └── 条件独立生成 R1,...,RJ
```

联合识别要从最下方的反应分布逆推出上方的 \(Q,\Theta,\boldsymbol p\)。
