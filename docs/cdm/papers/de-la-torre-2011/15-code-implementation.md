# 代码实现精读

## 2011 年原始实现

论文报告：

- MMLE 程序使用 Ox 编写；
- 分数减法数据运行少于 16 秒；
- MCMI-III 数据运行少于 20 秒；
- 计算机为 3 GHz Pentium 4；
- 收敛准则为 0.001。

正文没有给出源代码下载地址、版本库或补充材料。因此无法对原始 2011 Ox 文件做逐行核验。

## 后续官方实现

当前公开实现是

[Wenchao-Ma/GDINA](https://github.com/Wenchao-Ma/GDINA)。

本站核对的是 2026-07-10 的提交

[`ac5eca223a1ee32b6c2f595cfeaef9b330451425`](https://github.com/Wenchao-Ma/GDINA/tree/ac5eca223a1ee32b6c2f595cfeaef9b330451425)，

仓库 `DESCRIPTION` 标记版本为 2.12.3。该包由 Wenchao Ma 和 Jimmy de la Torre 共同开发，属于 2011 论文之后形成的软件系统。

## 从用户接口进入

核心入口是

[`R/GDINA.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/GDINA.R)。

用户提供：

```r
fit <- GDINA(
  dat = dat,
  Q = Q,
  model = "GDINA"
)
```

同一入口支持 DINA、DINO、A-CDM、LLM、RRUM、multiple-strategy DINA 和后续扩展。

## 属性空间与约化组

[`R/ExportedFuncs.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/ExportedFuncs.R)
中的几个函数直接对应论文符号：

| 函数 | 论文对象 |
| --- | --- |
| `attributepattern()` | 全部 \(\boldsymbol\alpha_l\) |
| `LC2LG()` | 完整潜在类到项目约化组的映射 |
| `designmatrix()` | \(M_j\) |
| `att.structure()` | 结构化属性空间 |

`designmatrix()` 根据模型名产生 G-DINA、DINA、DINO、A-CDM、LLM 或 RRUM 的设计矩阵。LLM 与 RRUM 使用和 A-CDM 相同的列结构，再通过不同 link function 区分。

## 单组估计主循环

[`R/SingleGroup_Estimation.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/SingleGroup_Estimation.R)
完成：

1. 数据与 Q 矩阵检查；
2. 完整属性模式生成；
3. 各项目约化 latent group 建立；
4. 属性联合分布初始化；
5. design matrix 和约束矩阵初始化；
6. E 步 `LikNR()`；
7. M 步 `Mstep()`；
8. 属性分布更新；
9. 收敛检查；
10. 概率、效应参数、后验和拟合指标整理。

代码中 `Ng` 和 `Rg` 分别对应论文的期望组人数与期望答对人数。

## M 步

[`R/Mstep.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/Mstep.R)
区分两种路线。

### 闭式更新

identity-link G-DINA、DINA、DINO 可以直接使用：

```r
phat <- Rj / Nj
```

DINA/DINO 会先按 design matrix 合并相应约化组的 `Rj` 和 `Nj`。

### 约束优化

A-CDM、LLM、RRUM 和用户定义模型需要数值优化。代码提供：

- BFGS；
- augmented Lagrangian；
- `solnp`；
- SLSQP。

优化同时处理概率上下界与单调约束。

底层概率计算和目标函数由

[`src/Mstep.cpp`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/src/Mstep.cpp)
中的 Rcpp/Armadillo 代码加速。

## item-level model comparison

[`R/modelcomp.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/modelcomp.R)
实现：

- Wald test；
- likelihood-ratio test；
- Lagrange-multiplier test；
- DINA、DINO、A-CDM、LLM、RRUM 比较；
- Holm、Bonferroni、BH、BY 等 \(p\) 值调整；
- 按最大 \(p\) 值或模型简洁性选择模型。

Wald 分支直接读取项目成功概率和协方差矩阵，再计算

```r
t(R %*% p) %*%
  ginv(R %*% vcov %*% t(R)) %*%
  (R %*% p)
```

这与论文公式 (35) 一致。

## 模拟工具

[`R/simGDINA.R`](https://github.com/Wenchao-Ma/GDINA/blob/ac5eca223a1ee32b6c2f595cfeaef9b330451425/R/simGDINA.R)
支持：

- 多种 CDM；
- identity、logit、log link；
- uniform、categorical、higher-order 等属性分布；
- 自定义 design matrix；
- 单调约束；
- 二分与后续序列模型。

## 论文与软件的边界

现代 `GDINA` 包包含大量 2011 年以后发展的功能，例如：

- 多组估计；
- sequential G-DINA；
- polytomous attributes；
- Q 矩阵验证；
- DIF；
- 多种 item/test fit；
- bootstrap SE。

阅读代码时应把“论文原始框架”和“后续软件扩展”分开。版本 2.12.3 可以验证核心算法如何落地，却不能作为 2011 论文当时已经具备全部功能的证据。

## 本站教学实现

[`tools/de_la_torre_2011_gdina_framework.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/de_la_torre_2011_gdina_framework.py)
保留最小主线：

```text
Q + full attribute patterns
  -> item-specific reduced groups
  -> saturated G-DINA EM
  -> design-matrix transformation
  -> observed information
  -> A-CDM Wald test
```

它适合逐公式核对，不替代正式分析中的 `GDINA` R package。
