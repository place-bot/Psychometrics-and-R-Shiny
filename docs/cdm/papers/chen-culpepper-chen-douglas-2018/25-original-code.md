# 原始补充材料代码精读

## 文件组成

原作者随文发布：

| 文件 | 作用 |
| --- | --- |
| `Q_Dina_all.cpp` | 三种 MCMC、数据生成、编码和辅助函数 |
| `fraction_subtraction.R` | 读取数据、编译 C++、拟合三种方法、提取结果 |
| `README.txt` | 函数入口、参数与返回对象说明 |

C++ 通过 `RcppArmadillo` 编译，R 端使用：

```r
Rcpp::sourceCpp("Q_Dina_all.cpp")
```

## 论文对象到代码函数

| 论文对象 | 代码 |
| --- | --- |
| 二进制向量整数编码 | `bijectionvector()` |
| 整数还原属性/q-vector | `inv_bijectionvector()` |
| 理想反应矩阵 | `ETAmat()` |
| 合法初始 Q | `random_Q()` |
| 三条可识别限制 | `identify_check()` |
| 学生属性、\(\pi,s,g\) 更新 | `parm_update_nomiss()` / `update_alpha()` / `update_sg()` |
| 受限逐元素 Q 更新 | `updateQ_DINA_new()` |
| DS2 + MH | `updateQ_MH()` |
| 受限 Gibbs 主链 | `dina_Gibbs_Q()` |
| 受限 MH 主链 | `DINA_MH_Q()` |
| 无约束 Gibbs 主链 | `DINA_Gibbs_Q_unconst()` |
| DINA 模拟 | `sim_Y_dina()` |

## `identify_check()` 怎样检查三条条件

代码计算：

```cpp
c_sum = sum(Q, 0);
r_sum = sum(Q, 1);
```

分别检查

\[
\min_k c_k>2,
\qquad
\min_j r_j>0.
\]

随后通过矩阵运算统计每种单位行 \(\boldsymbol e_k\) 的出现数 `n_ek`，要求

\[
\min_k n_{e_k}>1.
\]

三个布尔值都为真时返回合法。

## 理想反应的实现

`ETAmat(K,J,Q)` 枚举 \(2^K\) 个属性模式。对题目 \(j\) 和类别 \(c\)：

```cpp
compare = qj * alpha_c - qj * qj.t();
ETA(j, cc) = (compare >= 0);
```

这正对应

\[
\eta_{cj}
=
I(\boldsymbol q_j^{\mathsf T}\boldsymbol a_c
\ge
\boldsymbol q_j^{\mathsf T}\boldsymbol q_j).
\]

对二元向量，左侧不可能超过右侧，所以 `>= 0` 等价于相等。

## 受限 Gibbs 的快速条件更新

`ETAmat_nok_one_m_ac(K)` 预计算每个属性 \(k\)、其余 q-vector 配置和属性类下的

\[
\eta_{-k}(1-\alpha_k).
\]

`abcounts()` 再把受影响学生按 \(Y_{ij}=0,1\) 计数。这样每次更新 \(q_{jk}\) 无需为全部 Q 重新生成完整 ETA。

条件抽样使用：

```cpp
qjk = 1.0 * (
    log(1-u) - log(u)
    > a0*log(s/(1-g)) + a1*log((1-s)/g)
);
```

与前页推导一致。

## MH 的局部似然比

`updateQ_MH()`：

1. 从某列抽 \(B\) 个行位置；
2. 按 DS2 固定必要的 0/1；
3. 枚举自由位的合法配置编号；
4. 只对被选中的题目行计算新旧似然比；
5. 用 `min(1, ratio)` 接受。

原实现逐次相乘概率比。大数据复现宜改为对数似然差，减少浮点下溢。

## Q 众数的实现

每个 Q 样本先计算

\[
Q^{\mathsf T}\boldsymbol v,
\]

再降序排列列编码。`Qcount` 或 `Qveccount` 的最后一行存出现次数。R 脚本取：

```r
modeindex = which.max(out$Qcount[K+1, ])
modeQ = inv_bijectionmat(J, out$Qcount[1:K, modeindex])
```

这实现了论文 Section 2.7 的整张矩阵众数和列标签对齐。

## 返回值

三种主函数均返回：

- `QS`：burn-in 后的 Q 样本；
- `PIs`：潜在类比例样本；
- `SS`、`GS`：题目参数样本；
- `Qcount` 或 `Qveccount`：规范 Q 编码及频数。

MH 版本另返回学生类别样本 `CLASSES`。

## 原始代码的范围

它完整实现论文比较的三条算法。公开 R 文件只给分数减法应用，模拟 Table 1 的 3200 个数据集驱动脚本、真题目参数和随机种子没有随文发布。

## 逐行审查发现的三个复现问题

这些问题来自公开补充文件的当前静态版本，均属于实现与复现层面。

### 1. R 脚本含一个未定义对象

脚本在调用任何估计器之前执行：

```r
vj = bijectionvector(J)
Qvj = t(Q) %*% vj
```

此时脚本没有创建 `Q`，`Qvj` 在后文也没有使用。全新 R 会话中，第二行会报 `object 'Q' not found`。复现时可删除这两行；后续众数恢复已经另行创建 `vv`。

### 2. MH 初值第一轮可能违反单调性

`DINA_MH_Q()` 独立生成：

```cpp
ss = randu(J);
gs = randu(J);
```

因此第一轮属性更新时可能出现

\[
g_j\ge1-s_j.
\]

随后的 `update_sg()` 会恢复截断限制，且长 burn-in 会削弱初始影响。更清楚的初始化是原代码在受限 Gibbs 中采用的写法：

```cpp
ss = randu(J);
gs = (ones(J) - ss) % randu(J);
```

### 3. DS2 自由位恰好全需为 1 的边界

`updateQ_MH()` 只在

```cpp
Bmax > Bmin
```

时给自由位置赋 0/1 配置。若 `Bmax == Bmin > 0`，唯一合法配置是所有自由位均为 1，但原数组会保留初始化哨兵值 2。稳健实现应让这一相等边界也进入 `validvector()`，或显式把所有自由位设为 1。

这些审查发现不改写论文 Table 1 的已报告数字；若重新编译补充代码做新实验，建议先修正并记录补丁。

[下一页：当前 edina 包代码精读](26-edina-package.md)
