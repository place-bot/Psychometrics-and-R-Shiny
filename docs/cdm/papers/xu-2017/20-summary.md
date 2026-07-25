# 总结与后续阅读

## 核心贡献

### 1. 定义统一的 Q-restricted latent class model

论文以

\[
\Theta=(\theta_{j,\boldsymbol\alpha}),
\qquad
\boldsymbol p=(p_{\boldsymbol\alpha})
\]

描述二分诊断模型，并用 Q 矩阵的等值与单调限制覆盖 DINA、DINO、G-DINA、logit-CDM 和 reduced RUM 等模型。

### 2. 把观测分布转成 T 矩阵边际

\[
T_{\boldsymbol r,\cdot}(Q,\Theta)\boldsymbol p
=
P(\boldsymbol R\succeq\boldsymbol r).
\]

全部 subset-success marginals 与完整反应模式分布一一对应，所以识别问题可以完全在 \(T\)-矩阵上处理。

### 3. 给出可执行的充分设计条件

\[
Q=
\begin{pmatrix}
I_K\\I_K\\Q'
\end{pmatrix},
\]

并且 \(Q'\) 能对每个 \(\boldsymbol e_k\) 与
\(\boldsymbol0\) 提供概率区分，则

\[
(\Theta,\boldsymbol p)
\]

严格可识别。三个 \(I_K\) 是仅凭 Q 结构即可保证 C1、C2 的安全设计。

### 4. 证明 C1 单独不够

两个单位块可能仍留下连续等价参数族。本站的 \(K=1\) 精确例子展示了两套不同项目概率与类比例产生完全相同的二题反应分布。

### 5. 建立新的证明技术

\[
T(Q,\Theta-\boldsymbol\theta^*\boldsymbol1^\top)
=
D(\boldsymbol\theta^*)T(Q,\Theta)
\]

把参数平移写成可逆行变换。通过选择平移量消零，证明按

\[
\boldsymbol0
\to
\boldsymbol e_k
\to
\text{二属性模式}
\to
\cdots
\to
\boldsymbol1
\]

逐层识别 \(\Theta\) 与 \(\boldsymbol p\)。

## 证据强度

论文有力建立：

- C1、C2 下的 strict identifiability；
- C1 单独不充分；
- \(T\)-矩阵变换的代数正确性；
- 在常规条件下通向 MLE 一致性的逻辑。

论文没有提供：

- 真实数据或模拟结果；
- 一般 RLCM 的必要充分条件；
- Q 未知时的联合识别；
- 结构零属性空间；
- 弱识别的有限样本误差；
- CAT 数据收集机制下的结论。

## 对 CDM 研究的直接意义

估计之前先问

\[
\text{Q 与反应限制是否让总体参数唯一？}
\]

如果答案为否，增加被试数、改变优化器或加入更多随机初值都不会创造缺失的总体信息。若答案为是，仍要继续检查条件数、边界、类稀疏和模型错设。

## 对 CAT 与生成式选题的意义

这篇论文讨论反应模型的群体识别，尚未讨论动态选题。它提示 CAT 研究至少需要同时处理两层条件：

1. **题库结构层**：Q 与项目反应模型能否识别；
2. **交互采样层**：adaptive policy 是否让关键题型获得足够曝光。

闭环 CAT 的序列形式为

\[
q_{t+1}
\sim
\pi\!\left(
\cdot\mid
q_{1:t},R_{1:t}
\right).
\]

每次作答 \(R_t\) 都改变下一题分布。若模型一次生成整套固定题序列，后续位置没有条件于学生新反应，它便没有实现 CAT 的逐步适应。可以预先生成候选计划，但执行时仍需在每次反馈后重规划或采用 autoregressive policy。

Xu (2017) 没有解决这个动态问题；它提供的是让底层认知状态模型具有明确统计含义的设计基础。

## 后续阅读

1. **Xu & Zhang (2016)**：DINA 模型的专门识别理论。
2. **Xu & Shang (2018)**：从给定 Q 限制推进到 latent structure 的识别与估计。
3. **Gu & Xu (2020)**：strict 与 partial identifiability 的一般框架。
4. **Culpepper (2023)**：弱化二分 RLCM 的设计条件。
5. **Lin & Xu (2024)**：多项反应 DINA。
6. **Liu & Culpepper (2024)**：名义反应 RLCM。

按照本站制作顺序，下一组进入 Q 矩阵验证、学习与识别论文，先读 de la Torre (2008) 的 DINA Q-matrix validation。
