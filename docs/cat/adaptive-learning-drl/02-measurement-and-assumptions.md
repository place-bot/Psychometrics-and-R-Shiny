# 测量模型、能力状态与假设

## 1. 能力从哪里来

论文把学生当前水平表示为 \(D\) 维潜在能力向量：

\[
\boldsymbol\theta^{(t)}
=
\left[
\theta_1^{(t)},
\ldots,
\theta_D^{(t)}
\right]^\top.
\]

潜在能力无法直接观察。系统在每轮学习后给学生测试或作业，再用 IRT/MIRT 从反应数据估计 \(\boldsymbol\theta^{(t)}\)。

完整闭环为：

```text
学习材料
   ↓
学生学习
   ↓
测试 / 作业反应
   ↓
IRT 或 MIRT 能力估计
   ↓
把估计能力交给 DQN
```

## 2. 通用 IRT 表达

论文先写出通用测量模型：

\[
\Pr(U=u\mid\boldsymbol\theta)
=
f(\boldsymbol\theta,\boldsymbol\eta,u).
\tag{1}
\]

各符号含义如下：

| 符号 | 含义 |
|---|---|
| \(U\) | 某道测试题得分的随机变量 |
| \(u\) | 一个具体得分，例如 0 或 1 |
| \(\boldsymbol\theta\) | 学生潜在能力参数 |
| \(\boldsymbol\eta\) | 题目参数 |
| \(f\) | 把能力、题目参数和得分映射为概率的反应函数 |

这个表达允许二分、等级、多项和多维模型。

## 3. M2PL 示例

论文用多维二参数逻辑模型说明：

\[
\Pr(U_{ij}=1\mid\boldsymbol\theta_i,\mathbf a_j,d_j)
=
\frac{
\exp\!\left(\mathbf a_j^\top\boldsymbol\theta_i+d_j\right)
}{
1+\exp\!\left(\mathbf a_j^\top\boldsymbol\theta_i+d_j\right)
}.
\tag{2}
\]

其中：

- \(i\) 表示学生；
- \(j\) 表示测试题；
- \(\boldsymbol\theta_i\in\mathbb R^D\) 是学生能力；
- \(\mathbf a_j\in\mathbb R^D\) 是题目对各能力维度的区分参数；
- \(d_j\) 是截距；
- \(U_{ij}=1\) 表示答对。

线性预测量

\[
\mathbf a_j^\top\boldsymbol\theta_i+d_j
\]

把多维能力压缩成该题的有效能力。若 \(\mathbf a_j\) 的分量非负，提高相关能力会提高答对概率。

## 4. 每轮测量怎样进入决策

令真实能力为 \(\boldsymbol\theta^{(t)}\)，估计值为

\[
\widehat{\boldsymbol\theta}^{(t)}
=
\boldsymbol\theta^{(t)}
+\mathbf e^{(t)}.
\]

DQN 实际接收的是估计值：

\[
a^{(t)}
=
\pi\!\left(\widehat{\boldsymbol\theta}^{(t)}\right).
\]

因此测量误差会通过两条路径影响系统：

1. 当前材料可能因状态判断偏差而选错；
2. 训练数据中的 \(s\) 与 \(s'\) 带噪，Q 网络和转移模型都会学习到受污染的映射。

论文的模拟专门加入正态能力估计误差，检查策略性能是否稳健。

## 5. 从 IRT 尺度映射到统一状态空间

IRT 能力通常定义在实数轴上。论文指出，实际估计可把第 \(d\) 维限制在

\[
[-5,h_d],
\]

其中 \(h_d\) 是该能力的目标水平。

一个自然的线性双射为：

\[
x_d
=
\frac{\theta_d+5}{h_d+5}.
\tag{3}
\]

端点满足：

\[
\theta_d=-5\Rightarrow x_d=0,
\qquad
\theta_d=h_d\Rightarrow x_d=1.
\]

逆变换为：

\[
\theta_d=(h_d+5)x_d-5.
\tag{4}
\]

所有维度变换后：

\[
\mathbf x\in[0,1]^D.
\]

!!! warning "尺度解释"

    \(x_d\) 是重标度后的能力。数值 \(0.8\) 表示它在所设区间中的相对位置；只有测量模型另有定义时，才能把它解释为“80% 掌握概率”。

## 6. 目标状态

缩放后，第 \(d\) 维达到目标对应 \(x_d=1\)。所有维度的共同目标为

\[
\mathbf 1_D
=
\begin{bmatrix}
1\\
\vdots\\
1
\end{bmatrix}.
\]

这里的 1 代表预先规定的目标水平 \(h_d\)，并不表示现实中的绝对完美。

## 7. 论文明确写出的两项假设

### 假设 A1：能力不倒退

\[
\theta_d^{(t+1)}
\ge
\theta_d^{(t)},
\qquad
d=1,\ldots,D.
\tag{5}
\]

它排除了遗忘、疲劳造成的表现下降、知识干扰和测量波动引起的真实退步。

### 假设 A2：材料数有限

\[
\mathcal A=\{1,\ldots,L\}.
\tag{6}
\]

有限离散动作使 DQN 可以一次输出全部材料的 Q 值。

## 8. 建模中还隐含的假设

完整算法还依赖以下条件：

| 假设 | 算法中的位置 | 风险 |
|---|---|---|
| 能力向量充分概括学习历史 | 马尔可夫状态 | 相同能力点估计可能对应不同先修经历 |
| 能力估计足够准确 | DQN 输入 | 测量误差可能改变选材 |
| 同一群体共享转移规律 | 统一 \(\mathcal P\) | 个体差异被平均 |
| 转移时间齐 | 使用固定 \(\mathcal P(s'\mid s,a)\) | 疲劳、学期阶段和教学变化会破坏稳定性 |
| 每份材料成本相同 | 每步统一 \(-1\) | 视频时长、负荷和金钱成本没有体现 |
| 所有维度目标都为 1 | 终止条件 | 个性化目标与选修能力难以表达 |

这些假设决定了论文结果能够推广到什么范围。

## 9. 能力点估计与 belief state

若两个学生的点估计相同：

\[
\widehat{\boldsymbol\theta}_A
=
\widehat{\boldsymbol\theta}_B,
\]

但 A 的后验分布很集中、B 的后验分布很宽，二者面对同一材料的风险可能不同。严格的部分可观测建模会使用

\[
b_t(\boldsymbol\theta)
=
\Pr(\boldsymbol\theta_t=\boldsymbol\theta\mid H_t),
\tag{7}
\]

其中 \(H_t\) 是全部已观察历史。

论文以点估计作为状态，计算更直接；作者也把 POMDP 作为未来方向。

## 10. CAT 在测量环节的作用

每轮学习后若用固定长测验，测量会占用大量时间。CAT 可以根据当前作答逐题选题，用较少题估计 \(\boldsymbol\theta^{(t)}\)。于是系统形成两层自适应：

```text
外层：根据能力选择学习材料
  └─ 内层：用 CAT 逐题选择测量项目并估计能力
```

内层 CAT 追求测量效率，外层学习策略追求能力成长效率。两层目标应分别定义和验证。
