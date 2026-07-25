# 代码库实现精读

## 原文代码状态

论文三处实验都说明算法由作者用 Ox 实现，引用 Doornik (2003)。正文与参考文献没有提供：

- 下载地址；
- 附录代码；
- 软件包；
- 可执行文件；
- 随机种子。

因此无法对原 Ox 程序逐行复核。原文给出的公式、算法说明和表格是复现的主要依据。

## 后续公开实现

CRAN [`CDM`](https://cran.r-project.org/package=CDM) 提供：

```r
din.validate.qmatrix(object, IDI_diff = .02, print = TRUE)
```

本站核对了 CDM 8.3-14 的：

- [`R/din.validate.qmatrix.R`](https://github.com/alexanderrobitzsch/CDM/blob/master/R/din.validate.qmatrix.R)
- [`src/cdm_rcpp_din_validate.cpp`](https://github.com/alexanderrobitzsch/CDM/blob/master/src/cdm_rcpp_din_validate.cpp)
- `man/din.validate.qmatrix.Rd`

该函数引用 de la Torre (2008)，但搜索和阈值逻辑与原文 sequential \(\delta\)-method 有重要差异。

## R 层输入

函数接受一个已经由 `CDM::din()` 拟合的对象，读取：

| 对象字段 | 含义 |
| --- | --- |
| `object$q.matrix` | 当前 Q |
| `object$rule` | 每题 DINA 或 DINO 规则 |
| `object$guess[,1]` | 当前 guessing |
| `object$slip[,1]` | 当前 slipping |
| `object$I.lj` | 模式与题目的期望人数 |
| `object$R.lj` | 模式与题目的期望答对人数 |
| `object$attribute.patt.splitted` | \(2^K\) 个属性模式 |

代码先计算：

```r
IDI <- 1 - slip - guess
```

这与原文的 \(\widehat\delta\) 相同。

## 候选生成

R 代码用 `expand.grid()` 生成全部二分向量，并删除全零行：

```r
q.matrix.poss <- q.matrix.poss[
    !(rowMeans(q.matrix.poss) %in% 0),
]
```

候选数为：

\[
2^K-1.
\]

因此该实现执行穷举搜索。它没有沿用原文“单属性开始、每轮只加一个属性”的二次级顺序搜索。

## C++ 核心怎样分组

对每个候选 `qvec`、题目 `ii` 和属性模式 `ll`，C++ 计算：

```cpp
ness_ii += qvec[kk];
latresp += qvec[kk] * attr_patt(ll,kk);
```

若

```cpp
latresp < ness_ii
```

则该模式进入 DINA 的 \(\eta=0\) 组；否则进入 \(\eta=1\) 组。

这与

\[
\eta_l(\boldsymbol q)
=
\prod_k\alpha_{lk}^{q_k}
\]

等价。

期望计数聚合为：

```cpp
Ij0[ii] += Ilj(ii,ll);
Rj0[ii] += Rlj(ii,ll);
Ij1[ii] += Ilj(ii,ll);
Rj1[ii] += Rlj(ii,ll);
```

候选参数：

```cpp
guess[ii] = Rj0[ii] / Ij0[ii];
slip[ii] = (Ij1[ii] - Rj1[ii]) / Ij1[ii];
```

完全对应原文 EM-based solution。

## R 层怎样选行

C++ 返回所有“题目 × 候选 q-vector”的 \(g,s\)。R 层计算：

```r
coef.modified$IDI <-
    1 - coef.modified$slip - coef.modified$guess
```

再计算：

```r
delta.IDI <- IDI(candidate) - IDI(original)
```

只保留：

```r
IDI(candidate) - IDI(original) > IDI_diff
```

对每题按 IDI 降序取第一行作为建议 q-vector。

## 两种阈值含义的差别

| 原文 \(\varepsilon\) | `CDM::IDI_diff` |
| --- | --- |
| 比较相邻搜索步 \(\delta^{(s)}-\delta^{(s-1)}\) | 比较候选与原 Q 的 `IDI(candidate)-IDI(original)` |
| 决定是否继续加入一个属性 | 决定候选是否足以超过原行 |
| 路径依赖的 forward search | 全候选穷举后过滤 |
| 候选数最多 \(K(K+1)/2\) | 候选数 \(2^K-1\) |

所以 `IDI_diff=.02` 不能直接解释成原文 \(\varepsilon=.02\) 的同一算法。

## 返回对象

| 字段 | 内容 |
| --- | --- |
| `coef.modified` | 全部题目与全部候选的参数、IDI 和改善 |
| `coef.modified.short` | 超过 `IDI_diff` 的候选 |
| `q.matrix.prop` | 每题取最高 IDI 后的建议 Q |
| `time_diff` | 函数耗时 |

## 代码层面的三个注意点

1. 函数使用当前 `din` 对象中的后验期望计数，初始 Q 错误仍会进入候选评分。
2. 函数返回建议 Q，但没有自动在建议 Q 下完成原文所说的多阈值追加 EM 与内容审核。
3. 穷举复杂度随 \(K\) 指数增长，属性数较大时需评估内存和运行时间。

## 官方示例

`CDM` 文档模拟 12 题、3 属性、4000 人，将题 1 与题 10 的 Q 行写错。`din.validate.qmatrix()` 给出的建议 Q 恢复：

\[
\boldsymbol q_1=100,\qquad
\boldsymbol q_{10}=110.
\]

这个示例验证包内流程可运行；它属于后续软件示例，不能替代原文的 30 题模拟与两项真实数据分析。

