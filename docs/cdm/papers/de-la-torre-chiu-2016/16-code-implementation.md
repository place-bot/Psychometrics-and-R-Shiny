# 原文 Ox 与 `GDINA::Qval()` 代码精读

## 原文代码状态

论文说明：

- 两阶段估计与搜索由 Ox 编写；
- 实现引用 Doornik (2007)；
- 感兴趣的读者可联系第一作者。

文章没有给出仓库、下载地址、版本号或随机种子。因此原始 Ox 实现无法逐行审计。

## 当前公开实现

本页核对：

- [`Wenchao-Ma/GDINA`](https://github.com/Wenchao-Ma/GDINA)；
- CRAN `GDINA` 2.9.12；
- `R/GDI.R`；
- `src/varsigma.cpp`；
- `Qval()` 文档。

该包由 Wenchao Ma 与 Jimmy de la Torre 等维护，当前接口为：

```r
fit <- GDINA(dat = Y, Q = Q0, model = "GDINA")
out <- Qval(
  fit,
  method = "PVAF",
  iter = "none",
  eps = 0.95
)
```

## `Qval()` 的入口检查

R 层先检查：

- 输入对象属于 `GDINA`；
- `eps` 位于 \([0,1]\) 或等于 `-1`；
- 单组模型；
- 二分属性；
- 属性没有预设结构；
- `iter` 属于 `none/test/test.att/item`。

这些限制明确了当前函数的适用范围。

## 从拟合对象取后验

核心对象：

```r
w <- extract(GDINA.obj, "posterior.prob")
logpost <- extract(GDINA.obj, "logposterior.i")
```

其中：

- `w` 对应 \(\widehat w_l\)；
- `exp(logpost)` 对应每个学生的 \(\tau_{il}\)。

代码计算后验期望答对数：

```r
rc <- apply(YY, 2, function(x) {
  colSums(x * exp(logpost))
})
```

以及后验期望作答人数：

```r
rn <- apply(1 * (!is.na(Y)), 2, function(x) {
  colSums(x * exp(logpost))
})
```

完整模式成功率：

```r
est.p <- (rc + 1e-10) / (rn + 2e-10)
```

这对应

\[
\widehat p_{jl}
=
\frac{\sum_i\tau_{il}Y_{ij}+10^{-10}}
{\sum_i\tau_{il}+2\times10^{-10}}.
\]

极小平滑项防止空类别产生除零。

## 候选分组

```r
patt <- attributepattern(K)[-1, ]
loc <- eta(patt)
```

`patt` 包含 \(2^K-1\) 个非零候选，`eta()` 返回每个候选对 \(2^K\) 个完整模式的分组编号。

## C++ 的 `varsigma()`

`src/varsigma.cpp` 对每题、每个候选执行：

```cpp
arma::vec wp = mP.col(j) % vw;
reducedw(l) = arma::accu(vw.elem(q1));
reducedp(l) = arma::accu(wp.elem(q1)) / reducedw(l);
double pbar = arma::accu(reducedp % reducedw);
double Sbar = arma::accu(reducedp % reducedp % reducedw);
varsig(j,q) = Sbar - pbar * pbar;
```

逐行映射：

| C++ | 公式 |
| --- | --- |
| `wp` | \(w_lp_{jl}\) |
| `reducedw` | 折叠组权重 |
| `reducedp` | 折叠组加权成功率 |
| `pbar` | \(\bar p_j\) |
| `Sbar` | \(\sum_r w_rp_r^2\) |
| `Sbar-pbar*pbar` | \(\varsigma_j^2\) |

## PVAF 与建议向量

R 层：

```r
vsg <- varsigma(t(loc), est.p, w)
PVAF <- vsg / vsg[, L - 1]
```

最后一列是全属性候选。随后按所需属性数分组：

1. 每个属性数内取最高 PVAF；
2. 判断最高值是否大于 `eps`；
3. 取第一个通过阈值的属性数；
4. 返回对应 q-vector。

当前代码使用严格比较：

```r
max(x) > eps
```

论文文字使用

\[
\operatorname{PVAF}\ge\varepsilon.
\]

只有 PVAF 恰好等于阈值时两者才产生差异。

## 后续扩展

当前 `GDINA::Qval()` 已加入原文没有的功能：

| 选项 | 含义 |
| --- | --- |
| `eps=-1` | 用后续研究的预测公式产生阈值 |
| `iter="test"` | 每轮更新全部建议题后重拟合 |
| `iter="test.att"` | 每轮每题只改变一个属性数 |
| `iter="item"` | 每轮优先修改一题 |
| `method="wald"` | 使用 stepwise Wald 验证 |
| mesa plot | 检查属性数与 PVAF 路径 |

迭代实现回应了“初始 Q 污染后验”的问题，但仍可能循环或停在错误平衡点。代码显式记录：

- 收敛；
- 检测到循环；
- 产生空属性列；
- 达到最大迭代数。

## 独立 `Qval` 包

CRAN 的 [`Qval`](https://cran.r-project.org/package=Qval) 进一步整合：

- GDI；
- Wald；
- Hull；
- MLR-B；
- 多种搜索与迭代方式。

它是后续通用框架，不能反向当作 2016 年原始 Ox 程序。

## 应用建议

当前 `GDINA` 文档建议在默认 PVAF 产生过多修改时：

- 检查 mesa plots；
- 尝试 stepwise Wald；
- 尝试迭代实现；
- 使用预测阈值；
- 结合内容审核。

这比单次 `.95` 阈值更接近稳健分析流程。
