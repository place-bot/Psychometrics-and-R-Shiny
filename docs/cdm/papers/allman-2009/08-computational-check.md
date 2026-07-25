# 可计算复现

## 代码边界

原论文没有官方代码仓库，也没有提出参数估计算法。Kruskal 唯一性是总体分布层面的理论结论，从经验频数恢复张量因子还需要额外的数值方法。

本站提供

```text
tools/allman_2009_identifiability_demo.py
```

作为概念复现。它使用 Python 标准库完成：

1. 搜索 Theorem 4 的最佳三块划分；
2. 计算 Corollary 5 的 Bernoulli 充分变量数；
3. 构造块条件概率矩阵；
4. 通过边缘化恢复块内单题概率；
5. 枚举完整观测联合分布；
6. 验证共同类别置换不改变观测分布。

它不执行潜在类估计，也不从样本反推参数。

## 运行

在仓库根目录执行：

```bash
python3 tools/allman_2009_identifiability_demo.py
```

检查其他类别数和二分变量数：

```bash
python3 tools/allman_2009_identifiability_demo.py \
  --classes 8 \
  --binary-items 7
```

## Theorem 4 条件搜索

脚本对每个变量分配块标签 \(0,1,2\)，保留三个块都非空的分配。对每个划分计算

\[
K_a=\prod_{j\in S_a}\kappa_j
\]

和

\[
\operatorname{score}
=
\sum_{a=1}^{3}\min(r,K_a).
\]

若

\[
\operatorname{score}\ge2r+2,
\]

该划分通过 Theorem 4 的维度级充分条件。

核心函数：

```python
def tripartition_score(number_of_classes, arities, blocks):
    state_counts = tuple(
        product(arities[index] for index in block)
        for block in blocks
    )
    score = sum(
        min(number_of_classes, count)
        for count in state_counts
    )
    return score, state_counts
```

这里的 `arities[j]` 就是单变量状态数 \(\kappa_j\)。

## 块矩阵对应行张量积

对一个二分题块，脚本枚举所有 \(0/1\) 反应模式。给定一类的答对概率

\[
(\theta_1,\ldots,\theta_m),
\]

某反应模式 \(\boldsymbol x\) 的概率为

\[
P(\boldsymbol X=\boldsymbol x\mid Z=i)
=
\prod_{j=1}^{m}
\theta_j^{x_j}(1-\theta_j)^{1-x_j}.
\]

代码：

```python
def block_probability_row(item_success_probabilities):
    probabilities = []
    for pattern in itertools.product(
        (0, 1),
        repeat=len(item_success_probabilities),
    ):
        probability = product(
            theta if response else 1.0 - theta
            for response, theta in zip(
                pattern,
                item_success_probabilities,
            )
        )
        probabilities.append(float(probability))
    return probabilities
```

把每个潜在类的块反应分布按行堆叠，就得到 \(N_a\)。

## 边缘化复现 Lemma 14

从一个块行恢复块中第 \(q\) 道题的答对概率，只需对所有

\[
x_q=1
\]

的反应模式求和：

```python
def recover_item_probability(
    block_row,
    block_size,
    item_position,
):
    patterns = itertools.product(
        (0, 1),
        repeat=block_size,
    )
    return sum(
        probability
        for pattern, probability in zip(
            patterns,
            block_row,
        )
        if pattern[item_position] == 1
    )
```

这对应证明中的

\[
\sum_{\boldsymbol x_{-q}}
N_a(i;\boldsymbol x)
=
M_q(i,x_q).
\]

## 标签置换检查

脚本枚举

\[
P(\boldsymbol X=\boldsymbol x)
=
\sum_i\pi_i
\prod_j
\theta_{ij}^{x_j}(1-\theta_{ij})^{1-x_j}.
\]

随后对 \(\pi\) 和 \(\Theta\) 的行做同一个置换，再计算一次全部模式概率。两次结果的最大差异应为浮点舍入量级：

```text
max difference after class permutation = 0.000e+00
```

这个检查展示标签置换为何属于模型的结构对称性。

## 数值行秩检查能说明什么

脚本用高斯消元计算示例块矩阵的普通行秩。对

\[
r=4,\quad S_1=\{1,2\},\quad S_2=\{3,4\},\quad S_3=\{5\},
\]

前两个 \(4\times4\) 块矩阵在示例参数下满行秩，第 3 个 \(4\times2\) 矩阵普通秩为 2。

对 \(4\times4\) 满行秩矩阵，

\[
\operatorname{rank}_K=\operatorname{rank}=4.
\]

对 \(4\times2\) 矩阵，普通秩为 2 没有自动保证任意两行都独立；还需要检查每一对行。示例中的单题答对概率互异，因此任意两行

\[
(1-\theta_i,\theta_i)
\]

不成比例，Kruskal 秩为 2。

脚本的普通秩结果只能作为该数值例子的检查，不能代替一般 Kruskal 秩证明。

## 预期默认输出

默认示例应报告：

```text
Theorem 4 dimension check
  r = 4
  arities = [2, 2, 2, 2, 2]
  block state counts = (4, 4, 2)
  score = 10; threshold = 10
  sufficient dimension condition = True
  Bernoulli Corollary 5 bound = 5 items
```

随后输出三个块矩阵的形状与秩、边缘化恢复值、联合概率和标签置换误差。

## 若要真正做参数恢复

从有限样本频数表估计参数会引入新的问题：

- 经验张量含采样误差；
- CP 分解可能有局部最优和尺度问题；
- 非负与随机行约束需要显式处理；
- 接近低秩例外集时条件数可能很差；
- 类别数 \(r\) 需要选择；
- 估计出的无名字类别还要对齐到 CDM 属性模式。

这些问题属于张量估计、潜在类估计和 CDM 结构学习。Allman 等人的识别定理提供唯一性基础，没有给出这套计算流程。

