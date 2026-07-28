# 转移模型估计器与虚拟学生

## 1. 为什么还要学习转移模型

DQN 被称为 model-free，因为策略学习不需要显式知道

\[
\mathcal P(s'\mid s,a).
\]

然而 model-free 不等于数据需求低。真实学生的完整学习路径耗时长，探索性材料还可能带来教育风险。论文因此增加一个辅助模型，目标是提高真实数据利用率。

## 2. 转移模型的输入输出

模型接收当前状态与动作：

\[
(s,a),
\]

输出下一状态预测：

\[
\widehat s'=\psi_v(s,a),
\tag{1}
\]

其中 \(v\) 是神经网络参数。

若 \(s\in\mathbb R^D\)，动作编号可用 one-hot：

\[
\operatorname{onehot}(a)\in\{0,1\}^L.
\]

输入向量为：

\[
\mathbf x_{\text{model}}
=
\begin{bmatrix}
s\\
\operatorname{onehot}(a)
\end{bmatrix}
\in\mathbb R^{D+L}.
\tag{2}
\]

输出层有 \(D\) 个单元。

## 3. 监督学习目标

从历史转移集合

\[
\mathcal H
=
\{(s_i,a_i,r_i,s_i')\}_{i=1}^H
\]

拟合：

\[
\min_v
\sum_{i=1}^H
\left\|
\psi_v(s_i,a_i)-s_i'
\right\|_2^2.
\tag{3}
\]

奖励可由预测的下一状态重新计算，因此训练 \(\psi_v\) 时主要使用 \((s,a,s')\)。

## 4. 论文中的转移模型结构

模拟 Study II 使用：

- 一个隐藏层；
- 32 个隐藏单元；
- 输入为当前状态与材料；
- 输出为二维下一能力。

论文没有给出公开代码仓库链接，也没有在正文中完整报告激活函数、训练 epoch、batch size 和正则化。复现时这些参数需要自行明确记录。

## 5. 从真实学生到虚拟学生

训练分两阶段。

### 阶段一：拟合环境

\[
\mathcal H_{\text{real}}
\longrightarrow
\psi_v.
\]

### 阶段二：生成虚拟 episode

\[
s_{t+1}^{\text{virtual}}
=
\psi_v(s_t^{\text{virtual}},a_t).
\]

DQN 可以在模型环境中运行很多轮：

```text
有限真实学生
   ↓
拟合 ψ_v
   ↓
反复重置虚拟学生
   ↓
DQN 选择材料
   ↓
ψ_v 产生下一能力
   ↓
生成大量虚拟 transition
```

## 6. model-free 与 model-based 的准确关系

论文的基础策略算法是 model-free DQN。加入 \(\psi_v\) 后，训练过程利用了学习到的环境模型：

- Q 更新仍使用 TD 形式；
- 训练转移可由模型生成；
- 整体系统具有 model-based data augmentation 的成分。

可将它理解为早期的 Dyna 思路：真实经验学习模型，模型再生成经验帮助价值学习。

## 7. 论文的预测评价指标

### 决定系数

\[
R^2
=
1-
\frac{
\sum_{i=1}^H
\|s_i'-\widehat s_i'\|_2^2
}{
\sum_{i=1}^H
\|s_i'-\bar s'\|_2^2
}.
\tag{4}
\]

\(\bar s'\) 是真实下一状态的均值。\(R^2=1\) 表示完全预测。

### RMSE

论文写为：

\[
\operatorname{RMSE}
=
\sqrt{
\frac1H
\sum_{i=1}^H
\|s_i'-\widehat s_i'\|_2^2
}.
\tag{5}
\]

它是每条转移的向量误差经平方平均后开方。

## 8. 论文报告的转移预测结果

| 真实学生数 | 10 | 20 | 30 | 40 | 50 | 100 | 150 | 200 | 2000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 训练 \(R^2\) | 0.96 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| 测试 \(R^2\) | 0.95 | 0.97 | 0.96 | 0.96 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| RMSE | 0.11 | 0.08 | 0.09 | 0.09 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 |

在作者构造的二维平滑转移环境中，10 名学生已经得到较高 \(R^2\)。这项结果依赖模拟函数结构、状态维数和每名学生提供的转移数。

## 9. 为什么一步预测好仍可能导致策略差

DQN 关心长轨迹。若每一步有小偏差：

\[
\widehat s_{t+1}
=
s_{t+1}+\varepsilon_t,
\]

模型随后把自己的预测再次作为输入：

\[
\widehat s_{t+2}
=
\psi_v(\widehat s_{t+1},a_{t+1}).
\]

误差会递归累积，使虚拟轨迹逐渐离开真实状态分布。这称为 compounding error。

策略还会寻找模型过度乐观的区域：

\[
\max_a Q_{\psi_v}(s,a),
\]

从而利用模型漏洞。高一步 \(R^2\) 不能单独保证策略价值准确。

## 10. 随机转移与确定性均值模型

论文写成 \(\widehat s'=\psi_v(s,a)\)，对应点预测。真实环境的转移是随机分布：

\[
s'\sim\mathcal P(\cdot\mid s,a).
\]

若 \(\psi_v\) 只预测条件均值：

\[
\psi_v(s,a)
\approx
\mathbb E[S'\mid s,a],
\]

它会丢失方差、尾部风险和多峰结果。更完整的模型可输出：

\[
\widehat{\mathcal P}_v(s'\mid s,a),
\tag{6}
\]

例如：

- 高斯均值与协方差；
- Beta 分布参数；
- mixture density network；
- ensemble 或 Bayesian neural network。

## 11. 单调性约束

论文假设能力不退步。模型可通过输出增量来编码：

\[
\widehat{\Delta s}
=
\operatorname{softplus}(f_v(s,a)),
\]

\[
\widehat s'
=
\min\!\left(
\mathbf1_D,
s+\widehat{\Delta s}
\right).
\tag{7}
\]

这样每个预测分量满足：

\[
\widehat s_d'\ge s_d.
\]

若研究现实遗忘，应取消该限制并显式建模时间。

## 12. 更稳妥的模型使用方式

可采用混合 replay：

\[
\mathcal M
=
\mathcal M_{\text{real}}
\cup
\mathcal M_{\text{model}}.
\]

同时控制：

- 虚拟样本比例；
- 模型 rollout 长度；
- ensemble 不确定性阈值；
- 与真实数据支持区域的距离。

模型不确定时只做短 rollout，或直接回退到真实数据支持的保守动作。

## 13. 这部分真正解决的问题

转移模型估计器解决的是**数据复用**：

\[
\text{少量真实交互}
\longrightarrow
\text{可重复训练的近似环境}.
\]

它不会自动解决：

- 真实学生的因果异质性；
- 日志策略选择偏差；
- 能力估计误差；
- 模型外推风险；
- 奖励与教育价值的错位。
