# 模型验证、样本量与证据边界

## 用 S 验证已有 Q

若现有 Q 正确、DINA 假设成立、参数估计一致，则

\[
\left\|
\boldsymbol\beta
-
T_{\widehat{\boldsymbol c},\widehat{\boldsymbol g}}(Q)
\widehat{\boldsymbol p}
\right\|_2
\xrightarrow{p}0.
\]

因此 \(\widehat S(Q)\) 很大可提示：

- Q 结构错误；
- DINA 反应函数不合适；
- 局部独立失效；
- 参数估计失败；
- 有限样本误差较大。

S 单独无法判断是哪一种来源。

## 收敛速度

若

\[
\widehat{\boldsymbol c}-\boldsymbol c
=O_p(N^{-1/2}),
\qquad
\widehat{\boldsymbol g}-\boldsymbol g
=O_p(N^{-1/2}),
\]

正确 Q 的必要表现为

\[
\widehat S(Q)=O_p(N^{-1/2}).
\]

论文指出 S 的渐近分布依赖 \((\widehat c,\widehat g)\) 的具体形式，没有给出可直接使用的临界值或 p-value。

## 样本量经验式

论文由 \(K=5\) 的结果提出：

\[
N\ge30\times2^K.
\]

\(K=5\) 时为 960，接近 \(N=1000\)，而 Table 1 的恢复率由 \(N=500\) 的 38% 升到 98%。

这是模拟启发的经验量级，适用于类别近似均匀的设计。相关属性实验已经显示，稀有模式会进一步提高所需 N。

## 没有真实数据实验

全文的 Simulation 部分只生成 DINA 数据，Discussion 也没有加入实测数据分析。因而论文没有展示：

- 内容专家怎样解释数据建议；
- 真实 Q 缺少真值时怎样评估；
- 模型错设下 S 的行为；
- 修改 Q 后学生分类的实际改善；
- 真实题库的运行时间。

## 三层输出建议

实际应用可同时报告：

1. 当前 Q 的 \(\widehat S\)；
2. 若干近优 Q 及其 \(\Delta S\)；
3. 内容专家对每次 q-vector 变化的接受或拒绝理由。

这样能保留目标平坦时的结构不确定性，也符合论文对多个近优矩阵进行实质审查的建议。
