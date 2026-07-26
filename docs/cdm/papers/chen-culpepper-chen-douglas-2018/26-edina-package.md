# 当前 `edina` 包代码精读

## 包的定位

[`tmsalab/edina`](https://github.com/tmsalab/edina) 把本文方法封装为 R 包。当前 `DESCRIPTION` 为 0.1.2，核心入口是：

```r
fit = edina(data, k = 3, burnin = 10000, chain_length = 20000)
```

还提供：

```r
auto_edina(data, k = 2:4)
```

用于依次拟合多个属性数。

## 当前包保留了哪条原算法

`src/edina.cpp` 只导出：

```cpp
edina_Gibbs_Q(...)
check_identifiability(...)
```

当前包主估计器对应论文的**受限 Gibbs**。原始补充材料中的 MH 和无约束 Gibbs 没有成为用户接口。

## 文件结构

| 路径 | 作用 |
| --- | --- |
| `R/edina.R` | 参数检查、调用 C++、构造与打印对象 |
| `R/auto-edina.R` | 多个 \(K\) 的循环拟合 |
| `R/model-selection.R` | BIC、DIC、PPP |
| `R/q-matrix.R` | Q 对象、格式化、可识别标记 |
| `R/vis-*.R` | Q 热图与模型比较图 |
| `src/edina.cpp` | Rcpp 导出薄封装 |
| `inst/include/edina_meat.h` | 主要 C++ 算法 |

## 相对原始补充代码的改进

### 保留样本数语义更清楚

当前 C++ 使用

\[
\text{iter\_total}
=
\text{burnin}+\text{chain\_length}.
\]

`chain_length` 表示保留样本数。原始代码把它当总迭代数，再保留 `chain_length-burnin` 个样本。

### 不存整条 Q 立方体

当前实现累计

\[
\overline Q
=
\frac1M\sum_{m=1}^{M}Q^{(m)},
\]

减少 \(J\times K\times M\) 的内存。

### 增加模型诊断

每次保留迭代模拟复制数据，比较项目对的 odds ratio，形成后验预测概率；同时累计边际对数似然，用于 BIC 与 DIC。

### 增加对象和可视化

返回 `edina` 对象，包含：

- 题目参数均值与标准差；
- 潜在类比例；
- `avg_q` 与 `est_q`；
- BIC、DIC 和 PPP 所需量；
- 运行时间与数据名。

## 一个重要的汇总变化

当前代码设置：

```cpp
Qest = conv_to<mat>::from(Q_summed > .5);
```

也就是逐元素多数票。原论文和原始补充代码使用消除列置换后的**整张 Q 后验众数**。

逐元素多数票可能离开 \(\mathcal Q\)。当前 `new_edina()` 只格式化 `est_q`，没有再次强制检查；且完整 Q 样本没有保存，拟合完成后无法从对象恢复原论文的整张矩阵众数。

建议软件层面：

1. 对 `est_q` 再做 `check_identifiability()`；
2. 保留规范 Q 编码频数，或在线维护 top modes；
3. 若多数票非法，把它投影回 \(\mathcal Q\)；
4. 在输出中同时提供 Q 模式和逐元素包含概率。

## 输入边界

R 层检查 `data` 是矩阵、\(k\) 和链长为整数，但当前入口没有显式检查：

- 数据只含 0/1；
- 缺失值；
- \(J\) 足以支持给定 \(K\)；
- `burnin` 与 `chain_length` 为正；
- 可识别空间非空。

`random_Q()` 内使用无符号整数计算 \(J-2K\)。实务上应先保证至少

\[
J\ge2K+1.
\]

## 当前 0.1.2 的一个接口问题

`auto_edina()` 把准则矩阵存为：

```r
criterions
```

而 `best_model.auto_edina()` 当前读取：

```r
x$criterion[, ic]
```

字段少了末尾 `s`。按当前源码，这个辅助函数会因字段不存在而失败。直接读取 `x$criterions` 或修正字段名即可。这个结论来自当前仓库代码审查，与 2018 论文算法无关。

## 论文结果与软件扩展的边界

BIC、DIC、PPP、`auto_edina()`、Q 热图和逐元素阈值摘要都没有出现在 2018 论文的实验中。使用这些功能时应引用软件版本，并单独验证其统计与实现行为。

[下一页：本站可计算核验与代码审查发现](27-computational-check.md)
