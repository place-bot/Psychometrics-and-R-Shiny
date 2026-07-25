# EM 完整推导

## 缺失数据

把学生 \(i\) 属于属性模式 \(l\) 的指示变量记为

\[
Z_{il}
=
\mathbf 1(
\boldsymbol\alpha_i=\boldsymbol\alpha_l
).
\]

若 \(Z_{il}\) 已知，guess 和 slip 都是分组 Bernoulli 比例。EM 用

\[
w_{il}
=
E(Z_{il}\mid\boldsymbol X_i)
=
P(\boldsymbol\alpha_l\mid\boldsymbol X_i)
\]

替代未知指示变量。

## E 步

由 Bayes 公式：

\[
w_{il}
=
\frac{
\pi_l
L(\boldsymbol X_i\mid\boldsymbol\alpha_l)
}{
\sum_{h=1}^{L}
\pi_h
L(\boldsymbol X_i\mid\boldsymbol\alpha_h)
}.
\tag{7}
\]

对每个学生：

\[
\sum_{l=1}^{L}w_{il}=1.
\]

## 按理想状态聚合期望人数

对题目 \(j\) 和状态 \(z\in\{0,1\}\)，定义：

\[
I_j^{(z)}
=
\sum_{i=1}^{I}
\sum_{l:\eta_{lj}=z}
w_{il},
\tag{8}
\]

即理想状态为 \(z\) 的期望人数。

答对的期望人数为

\[
R_j^{(z)}
=
\sum_{i=1}^{I}
\sum_{l:\eta_{lj}=z}
w_{il}X_{ij}.
\tag{9}
\]

并且

\[
I_j^{(0)}+I_j^{(1)}=I.
\]

## M 步：更新 guessing

对 \(\eta=0\) 组，答对概率为 \(g_j\)。附录 Equation A10 给出：

\[
\widehat g_j
=
\frac{R_j^{(0)}}{I_j^{(0)}}.
\tag{10}
\]

它是“未掌握全部所需属性者中的期望答对比例”。

## M 步：更新 slipping

对 \(\eta=1\) 组，答错概率为 \(s_j\)。Equation A11 给出：

\[
\widehat s_j
=
\frac{
I_j^{(1)}-R_j^{(1)}
}{
I_j^{(1)}
}.
\tag{11}
\]

它是“掌握全部所需属性者中的期望答错比例”。

## 完整算法

1. 给定初始 \(g_j^{(0)},s_j^{(0)}\) 和固定模式先验 \(\pi_l\)。
2. 用当前参数计算全部 \(w_{il}\)。
3. 计算 \(I_j^{(0)},R_j^{(0)},I_j^{(1)},R_j^{(1)}\)。
4. 用式 (10)--(11) 更新全部题目参数。
5. 计算前后两轮参数的最大绝对差。
6. 未达到阈值则回到步骤 2。

论文模拟使用：

\[
\max_m
|\beta_m^{(t+1)}-\beta_m^{(t)}|
<0.0001
\]

作为收敛标准。

## 为什么 M 步有闭式解

E 步以后，每道题被拆成两个加权 Bernoulli 样本：

- \(\eta=0\) 组估计成功率 \(g_j\)；
- \(\eta=1\) 组估计失败率 \(s_j\)。

Bernoulli 极大似然就是加权成功次数除以加权总次数，因此无需数值优化器。

## 固定先验与经验 Bayes 扩展

论文的基础算法在每轮使用同一组 \(\pi_l\)。讨论部分建议更新：

\[
\widehat\pi_l
=
\frac{1}{I}
\sum_{i=1}^{I}
w_{il}.
\tag{12}
\]

这会把算法扩展为同时估计饱和属性模式比例。

本站脚本默认复现固定均匀先验；加上

```bash
--update-prior
```

才执行式 (12)，并将其标为论文讨论的扩展。

## 计算复杂度

每轮 E 步要对

\[
I\times 2^K\times J
\]

个学生—类别—题目组合计算概率，主要复杂度为

\[
O(IJ2^K).
\]

这解释了论文对较大 \(K\) 的担忧。M 步聚合期望计数也依赖同一后验矩阵，但代价通常低于 E 步的似然计算。
