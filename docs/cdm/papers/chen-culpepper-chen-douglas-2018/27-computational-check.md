# 本站可计算核验与代码审查发现

## 脚本

本站提供：

[`tools/chen_et_al_2018_bayesian_q_check.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/chen_et_al_2018_bayesian_q_check.py)

运行：

```bash
python3 tools/chen_et_al_2018_bayesian_q_check.py
```

它是独立教学核验，没有替代作者 Rcpp 实现。

## 核验一：三条识别限制

`is_identified(q)` 检查：

\[
\min_j\sum_kq_{jk}>0,
\]

\[
\min_k\sum_jq_{jk}\ge3,
\]

\[
\#\{j:\boldsymbol q_j=\boldsymbol e_k\}\ge2
\quad\forall k.
\]

第三式等价于行置换后含两套 \(I_K\)。

## 核验二：小规模不可约性

取

\[
K=2,\qquad J=6.
\]

每行只允许 \((10),(01),(11)\)，枚举得到 230 张满足限制的有标签 Q。

把两个合法状态间“只差一个元素翻转”定义为图边。广度优先搜索输出：

```text
Identified states for K=2, J=6: 230
States reached by one-flip graph: 230
One-flip graph connected: True
```

这验证了 Theorem 1 在一个有限小例中的结论。它不构成一般证明。

## 核验三：Table 1 聚合

脚本录入论文 Table 1 的 32 行，复算条件等权平均：

```text
K=3 mean whole-Q recovery:
MH=94.06, CGibbs=94.94, Gibbs=90.88
K=3 mean entry accuracy:
MH=98.04, CGibbs=98.36, Gibbs=95.54

K=4 mean whole-Q recovery:
MH=53.56, CGibbs=84.88, Gibbs=55.50
K=4 mean entry accuracy:
MH=88.41, CGibbs=96.02, Gibbs=89.27
```

它也核对：在全部 \(K=4,\rho>0\) 条件中，CGibbs 的整张 Q 恢复次数均最高或并列最高。

## 核验四：逐元素多数票反例

考虑三张合法 Q：

\[
Q^{(1)}=
\begin{bmatrix}
10\\10\\10\\01\\01\\01
\end{bmatrix},
\quad
Q^{(2)}=
\begin{bmatrix}
10\\10\\01\\10\\01\\01
\end{bmatrix},
\quad
Q^{(3)}=
\begin{bmatrix}
10\\10\\01\\01\\10\\01
\end{bmatrix}.
\]

三张矩阵均满足两套单位阵、每列至少三题和每行非零。

逐元素多数票得到

\[
\widehat Q_{\text{entry}}=
\begin{bmatrix}
10\\10\\01\\01\\01\\01
\end{bmatrix}.
\]

其列和为

\[
(2,4),
\]

第一属性只有两道题，因此

\[
\widehat Q_{\text{entry}}\notin\mathcal Q.
\]

脚本输出：

```text
Every one of three posterior draws is identified: True
Entry-wise majority is identified: False
Column sums of entry-wise majority: [2, 4]
```

## 对软件使用的直接建议

使用当前 `edina` 包后，至少执行：

```r
q_hat = extract_q_matrix(fit, binary = TRUE)
check_identifiability(q_hat)
```

若返回 `FALSE`，应报告逐元素包含概率并改用满足约束的整张 Q 摘要。由于 `check_identifiability()` 是包内 Rcpp 函数，用户接口能否直接调用取决于命名空间导出；也可以用 `q_matrix(q_hat)` 查看对象的 `identifiable` 属性。

## 核验范围

脚本没有：

- 重新运行 3200 个原始模拟；
- 重建缺失的真 \(s,g\) 设计；
- 复现分数减法的 30,000 次链；
- 证明一般 \(K,J\) 的不可约性；
- 评估 `edina` 包的统计校准。

它主要用于核对离散约束、表格汇总和软件摘要边界。

[下一页：局限、结论与未来工作](28-limitations-conclusion-future.md)
