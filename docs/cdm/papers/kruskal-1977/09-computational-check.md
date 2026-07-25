# 可计算检查

## 代码边界

Kruskal (1977) 没有官方代码。本站提供

```text
tools/kruskal_1977_demo.py
```

用于复现本专题中的有限维代数检查：

1. 用有理数高斯消元计算普通矩阵秩；
2. 枚举列子集，精确计算小矩阵的 Kruskal rank；
3. 构造三重积；
4. 验证共同置换与相消缩放保持张量不变；
5. 验证第三因子列重复时的非唯一分解。

脚本没有实现一般 CP 分解算法，也不从带噪数据估计因子。

## 运行

在仓库根目录执行：

```bash
python3 tools/kruskal_1977_demo.py
```

预期关键输出包括：

```text
Full-rank R=3 example
  ordinary ranks = (3, 3, 3)
  Kruskal ranks = (3, 3, 3)
  condition: 9 >= 8 -> True
  tensor rank certified as R = 3
  max difference after permutation/scaling = 0
```

以及：

```text
Non-unique matrix-like example
  Kruskal ranks = (2, 2, 1)
  condition: 5 >= 6 -> False
  equal tensors from a non-monomial Q = True
```

## 普通秩函数

脚本使用 `fractions.Fraction` 保存有理数，通过高斯消元得到精确秩：

```python
def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    ...
```

这样示例中的零差异来自精确算术，不依赖浮点容差。

## Kruskal rank 的枚举

对每个 \(q\)，枚举全部 \(q\) 列组合：

```python
def kruskal_rank(matrix):
    column_count = len(matrix[0])
    result = 0
    for size in range(1, column_count + 1):
        if all(
            matrix_rank(select_columns(matrix, indices)) == size
            for indices in itertools.combinations(
                range(column_count),
                size,
            )
        ):
            result = size
        else:
            break
    return result
```

若某个规模 \(q\) 已经存在相关列集，更大的规模也无法满足“任意子集独立”，所以可以停止。

## 三重积

代码直接实现

\[
x_{ijk}
=
\sum_{r=1}^{R}
a_{ir}b_{jr}c_{kr}.
\]

```python
def triple_product(a, b, c):
    return [
        [
            [
                sum(
                    a[i][r] * b[j][r] * c[k][r]
                    for r in range(component_count)
                )
                for k in range(len(c))
            ]
            for j in range(len(b))
        ]
        for i in range(len(a))
    ]
```

## 置换与缩放检查

脚本按同一个 `permutation` 重排三个矩阵的列，再分别乘

```text
(2, 1/2, 1)
(3, 1, 1/3)
(1/6, 2, 3)
```

每个位置的三项乘积都是 1。随后重新计算全部张量元素并比较。

这个检查展示式

\[
[AP\Lambda,BPM,CPN]=[A,B,C].
\]

它验证的是固有等价性，没有通过数值搜索“发现”唯一分解。

## 非唯一例子的代码映射

第二个例子使用

\[
A=B=I_2,\qquad C=(1,1)
\]

和一个非对角、非置换的可逆矩阵 \(Q\)。脚本构造

\[
\bar A=AQ,\qquad
\bar B=BQ^{-\mathsf T},
\qquad
\bar C=C.
\]

由于两个第三方向列完全相同，三路问题退化成矩阵因子分解，任意 \(Q\) 都会产生同一个张量。

## 代码结果能支持到哪里

| 检查 | 可以确认 | 无法确认 |
| --- | --- | --- |
| 枚举 \(k\)-rank | 给定小矩阵的精确 \(k\)-rank | 大矩阵上的高效一般算法 |
| 检查不等式 | Kruskal 充分条件是否成立 | 条件失败后的唯一性 |
| 构造等价因子 | 置换/缩放确实保持张量 | 从未知张量稳定恢复因子 |
| 显式反例 | 某个具体分解存在额外多解 | 所有低 \(k\)-rank 情形都多解 |

若研究目标是有限样本 CDM 估计，还需要非负张量分解、潜在类似然或贝叶斯估计，以及对采样误差的分析。
