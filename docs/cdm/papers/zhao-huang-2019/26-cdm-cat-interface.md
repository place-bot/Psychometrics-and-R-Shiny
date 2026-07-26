# 与 CDM、CAT 和 RecCAT 的接口

## 1. 论文位于题库准备层

```text
题目内容
   │
   ▼
语义模型产生 Q 候选       ← Zhao & Huang
   │
   ▼
专家/反应数据校准
   │
   ▼
可用题库参数
   │
   ▼
CAT 根据学生实时反应选下一题
```

论文没有定义 CAT 策略。它可以向 CAT 提供题目属性元数据。

## 2. CAT 的逐题更新

设第 \(t\) 题为 \(j_t\)，学生反应为 \(Y_t\)。观察后更新学生状态：

\[
\pi_t(\boldsymbol\alpha)
\propto
p
\left(
Y_t
\mid
\boldsymbol\alpha,
\boldsymbol q_{j_t},
\boldsymbol\theta_{j_t}
\right)
\pi_{t-1}(\boldsymbol\alpha).
\]

下一题根据更新后的 \(\pi_t\) 选择：

\[
j_{t+1}
=
\arg\max_{j\in\Omega_t}
U
\left(
j;\pi_t,Q,\Theta
\right).
\]

所以每收到一次反应，下一题都可以改变。

## 3. 文本 Q 模型怎样进入选题

对没有稳定 Q 的新题，文本模型给：

\[
p_\psi(\boldsymbol q_j\mid d_j).
\]

选题效用可以对 Q 不确定性积分：

\[
\widetilde U_t(j)
=
\mathbb E_{
\boldsymbol q_j
\sim
p_\psi(\cdot\mid d_j)
}
\left[
U(j;\pi_t,\boldsymbol q_j,\boldsymbol\theta_j)
\right].
\]

也可加入风险惩罚：

\[
\operatorname{Score}_t(j)
=
\widetilde U_t(j)
-
\lambda
H
\left[
p_\psi(\boldsymbol q_j\mid d_j)
\right].
\]

Q 语义越不确定，惩罚越大。

## 4. 内容平衡

若 CAT 需要覆盖多个内容领域，可维护已测计数

\[
\boldsymbol c_t=(c_{t1},\ldots,c_{tK}).
\]

选题时加入目标缺口：

\[
B_t(j)
=
\sum_{k=1}^{K}
w_k
\left(
r_{tk}-c_{tk}
\right)_+
p_\psi(q_{jk}=1\mid d_j).
\]

最终：

\[
j_{t+1}
=
\arg\max_{j\in\Omega_t}
\left\{
U_t(j)
+\gamma B_t(j)
-\lambda R_j
\right\}.
\]

这里 \(R_j\) 可表示 Q 不确定性、曝光或其他风险。

## 5. 与固定序列生成的关系

一开始可以生成一个候选计划：

\[
(j_1,\ldots,j_T).
\]

真正执行时采用 receding-horizon：

1. 只执行当前第一题；
2. 收到学生反应；
3. 更新学生后验和内容状态；
4. 重新规划剩余题；
5. 再执行下一题。

这样保留生成式规划能力，也保留 CAT 的实时自适应。

## 6. 论文能提供什么

- 新题的冷启动内容标签；
- 内容平衡所需的属性概率；
- 题库搜索空间的语义筛选；
- 低置信度题的复核优先级。

## 7. 论文不能单独提供什么

- 学生能力或属性后验；
- 逐题信息量；
- 停止规则；
- 曝光控制；
- 测试安全；
- 实时选题策略；
- 长期学习收益。

## 8. 对 RecCAT 的直接启发

可以把系统拆成两个模型：

\[
\underbrace{
p_\psi(Q\mid\text{item content})
}_{\text{题目语义模型}}
\quad+\quad
\underbrace{
\pi_\phi(\text{next item}\mid
\text{history},Q,\text{constraints})
}_{\text{自适应策略}}.
\]

Zhao 与 Huang 覆盖前一个模块的早期形式。你的生成式 CAT 研究重点会落在第二个模块及二者的联合训练。
