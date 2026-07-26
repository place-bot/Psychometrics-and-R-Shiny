# 受限 Gibbs 完整算法

## 从 \(B=1\) 得到逐元素更新

Theorem 1 说明 DS2 的单元素移动足以连通 \(\mathcal Q\)。作者据此把 Q 更新改写为逐个 \(q_{jk}\) 的 Gibbs 抽样。

每轮先按前述完整条件分布更新

\[
\boldsymbol s,\quad
\boldsymbol g,\quad
\boldsymbol\alpha,\quad
\boldsymbol\pi.
\]

随后按固定顺序遍历

\[
j=1,\ldots,J,
\qquad
k=1,\ldots,K.
\]

## 三类不能翻转的位置

若当前 \(q_{jk}\) 属于以下情况之一，就保持原值。

### 情况一：单位行中的 1

若

\[
\boldsymbol q_j=\boldsymbol e_k,
\]

把 \(q_{jk}=1\) 改成 0 会产生全零行。

### 情况二：列和为 3 时的 1

若

\[
\sum_jq_{jk}=3
\]

且当前位置为 1，删除它会让该属性只剩两题。

### 情况三：只有两份单位行时的关键 0

若 \(\boldsymbol q_j=\boldsymbol e_i\)、\(i\ne k\)，且当前 Q 中只有两行等于 \(\boldsymbol e_i\)，把 \(q_{jk}=0\) 改成 1 会破坏第二套单位阵要求。

## 可翻转位置

若 0 和 1 都能维持 \(Q\in\mathcal Q\)，按

\[
P(q_{jk}=x\mid-)
\propto
p(\boldsymbol Y\mid
\boldsymbol s,\boldsymbol g,\boldsymbol\alpha,
Q_{jk\leftarrow x}),
\qquad x\in\{0,1\}
\]

抽样。

## 顺序更新

更新 \(q_{jk}\) 时：

- 已经遍历过的元素使用本轮新值；
- 尚未遍历的元素使用上一轮值。

原文用 \(Q_{\text{new}}^{(t)}\) 和 \(Q_{\text{old}}^{(t-1)}\) 表达这类 systematic-scan Gibbs。

## 伪代码

```text
draw s, g, alpha, pi
for j in 1, ..., J:
    for k in 1, ..., K:
        make Q_flip by changing q[j,k]
        if Q_flip violates identification:
            keep q[j,k]
        else:
            compute conditional probabilities for 0 and 1
            sample q[j,k]
```

## 与 MH 的差别

| 方面 | MH + DS2 | 受限 Gibbs |
| --- | --- | --- |
| 一次 Q 移动 | 一列中的 \(B\) 个位置 | 一个位置 |
| 候选 | 在合法块配置中抽取 | 0/1 两个值 |
| 接受/拒绝 | 有 | 条件抽样本身完成更新 |
| 论文设置 | \(B=2K\) | \(B=1\) 的逐元素扫描 |
| 模拟表现 | \(K=3\) 很好 | \(K=4\) 明显更稳定 |

## 为什么逐元素也可能混合慢

若两个高后验 Q 相差多个彼此协调的元素，中间单元素状态的似然可能很低。受限 Gibbs 必须逐格通过这些中间状态。MH 的块移动有机会直接跨越。

论文 Table 1 中受限 Gibbs 在 \(N=4000\) 的若干条件下恢复率反而下降，也提示固定链长下的混合与后验集中可能发生交互。

[下一页：单个 q 的条件概率推导](17-q-full-conditional.md)
