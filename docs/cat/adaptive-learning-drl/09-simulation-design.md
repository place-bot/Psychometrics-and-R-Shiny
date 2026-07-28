# 模拟环境与实验设计

论文没有使用真实学习平台数据。两组实验共享同一个人工构造的连续状态 MDP，用来验证策略学习、测量噪声稳健性和转移模型的数据效率。

## 1. 实验问题

### Study I

1. DQN 能否学到稳定策略？
2. DQN 是否优于启发式与随机选材？
3. 能力估计误差存在时，优势是否保持？

### Study II

1. 少量真实学生能否拟合有效转移模型？
2. 用转移模型训练的 virtual DQN 是否比直接用同样数量学生的 actual DQN 更好？

## 2. 状态与动作

状态是二维能力：

\[
\boldsymbol\Theta^{(t)}
=
\begin{bmatrix}
\Theta_1^{(t)}\\
\Theta_2^{(t)}
\end{bmatrix}.
\]

动作集合：

\[
\mathcal A=\{1,2,3\}.
\]

可把两个能力理解为加法与减法：

- 材料 1 主要提高能力 1；
- 材料 2 主要提高能力 2；
- 材料 3 同时涉及两个能力，并包含跨维度依赖。

所有学生初始状态为：

\[
\boldsymbol\Theta^{(0)}=(0,0)^\top.
\tag{1}
\]

## 3. 能力增量

\[
\Delta\boldsymbol\Theta^{(t)}
=
\boldsymbol\Theta^{(t+1)}
-\boldsymbol\Theta^{(t)}
=
\begin{bmatrix}
\Delta\Theta_1^{(t)}\\
\Delta\Theta_2^{(t)}
\end{bmatrix}.
\tag{2}
\]

转移核写为：

\[
\mathcal P(\boldsymbol\theta'\mid\boldsymbol\theta,a)
=
\Pr\!\left(
\Delta\boldsymbol\Theta^{(t)}
=
\Delta\boldsymbol\theta
\mid
\boldsymbol\Theta^{(t)}
=
\boldsymbol\theta,
A^{(t)}=a
\right).
\tag{3}
\]

论文假设能力不倒退，因此：

\[
\Delta\theta_d\in[0,1-\theta_d].
\tag{4}
\]

## 4. Beta 增量分布

对材料 1 或 3：

\[
\Delta\theta_1
\sim
\operatorname{Beta}
\left(
1,
g_1(\boldsymbol\theta,a)
\right).
\tag{5}
\]

对材料 2 或 3：

\[
\Delta\theta_2
\sim
\operatorname{Beta}
\left(
1,
g_2(\Delta\theta_1,\boldsymbol\theta,a)
\right).
\tag{6}
\]

特殊情形：

\[
\Delta\theta_2=0
\quad\text{当 }a=1,
\]

\[
\Delta\theta_1=0
\quad\text{当 }a=2.
\]

## 5. 第一维的参数函数

\[
g_1(\boldsymbol\theta,a)
=
\begin{cases}
3+8\theta_1-0.2\theta_2,
&
a=1,
\\
15+15\theta_1-0.4\theta_2,
&
a=3.
\end{cases}
\tag{7}
\]

在 \(\operatorname{Beta}(1,b)\) 中，\(b\) 越大，质量越集中在 0 附近，典型增量越小。因此：

- \(\theta_1\) 越高，继续提高能力 1 越难；
- \(\theta_2\) 对能力 1 存在轻微正向迁移，因为其系数为负。

## 6. 第二维的参数函数

\[
g_2(\Delta\theta_1,\boldsymbol\theta,a)
=
\begin{cases}
10-\theta_1+5\theta_2,
&
a=2,
\\
\displaystyle
20
-28\theta_1
\exp\!\left[
-\frac{(\theta_1-0.6)^2}{0.3}
\right]
+30\theta_2
-0.3\Delta\theta_1,
&
a=3.
\end{cases}
\tag{8}
\]

式 (8) 表达：

- \(\theta_2\) 越高，继续提高能力 2 越难；
- 能力 1 对能力 2 有迁移；
- 材料 3 对中高能力 1 的学习者更有利；
- 本轮 \(\Delta\theta_1\) 较大时，\(\Delta\theta_2\) 也更可能较大。

## 7. 一个复现时必须补全的细节

标准 Beta 分布取值在 \([0,1]\)，论文同时声明：

\[
\Delta\theta_d\in[0,1-\theta_d].
\]

正文没有明确写出抽样后如何满足剩余空间约束。可选实现包括：

\[
\Delta\theta_d
=
(1-\theta_d)Z_d,
\qquad
Z_d\sim\operatorname{Beta}(1,g_d),
\tag{9}
\]

或对更新后的状态做截断：

\[
\theta_d'
=
\min(1,\theta_d+\Delta\theta_d).
\tag{10}
\]

两种实现的转移分布不同。复现报告应明确采用哪一种。

## 8. 能力估计误差

观测状态为：

\[
\widehat{\boldsymbol\theta}
=
\boldsymbol\theta+\mathbf e,
\]

\[
e_1,e_2
\overset{\text{iid}}{\sim}
\mathcal N(0,\sigma^2).
\tag{11}
\]

正态分布下约 99.7% 的误差落在：

\[
(-3\sigma,3\sigma).
\]

图 8 的横轴使用 \(\sigma\)：

\[
0\%,0.5\%,1\%,2\%,3\%,3.3\%,4\%,5\%.
\]

当 \(\sigma=5\%\) 时，约 99.7% 的单维误差位于 \(\pm15\%\)，因此正文所说的 “1% 到 15% 误差”主要对应三倍标准差范围。

## 9. Study I 训练条件

| 项目 | 设置 |
|---|---:|
| 训练学生数 | 2000 |
| 测试学生数 | 200 |
| DQN 隐藏层 | 64、32 |
| 折扣 \(\gamma\) | 0.9 |
| 学习率 \(\alpha\) | \(6\times10^{-4}\) |
| 初始探索率 | 1.0 |
| 最终探索率 | 0.1 |
| 探索衰减步数 | 2000 |
| mini-batch | 256 |
| 优化器 | Adam |
| 曲线平滑窗口 | 20 episodes |

## 10. Study I 比较策略

### DQN

根据当前连续能力输出三份材料的长期 Q 值。

### 启发式

选择能够提高尚未完全掌握能力的材料。正文没有给出足以独立复刻全部 tie-breaking 的伪代码。

### 随机

从三份材料中随机选择。

## 11. Study II 设计

转移模型结构：

- 输入：当前二维状态与动作；
- 隐藏层：1 层、32 单元；
- 输出：下一二维状态。

真实学生数量依次为：

\[
10,20,30,40,50,100,150,200,2000.
\]

对每个样本规模比较两条路线。

### Actual DQN

直接用这批真实学生产生的 episode 训练 DQN。

### Virtual DQN

先用同一批真实学生拟合转移模型，再让 DQN 在估计模型上训练 2000 个虚拟 episode。

两者使用相同真实学生预算，差别在于数据复用方式。

## 12. 评价指标

### 策略 reward

episode reward 越接近 0，达到目标所需的非终止步数越少。

### 转移模型

- 训练 \(R^2\)；
- 测试 \(R^2\)；
- 下一状态 RMSE。

### 稳健性

比较不同 \(\sigma\) 下 DQN 与启发式策略的平均 episode reward。

## 13. 实验设计能支持的结论

它能验证：

- 在已知模拟规律下，DQN 是否能从转移样本学习；
- 非线性跨能力依赖是否可能让长期策略超过局部启发式；
- 学习到的转移模型能否提高样本复用；
- 对加性高斯测量误差是否稳健。

它无法直接验证：

- 真实学生会按这些 Beta 函数学习；
- 策略能提高真实课程成绩；
- 材料对不同群体的因果效应相同；
- 虚拟学生模型在分布外动作上可信。
