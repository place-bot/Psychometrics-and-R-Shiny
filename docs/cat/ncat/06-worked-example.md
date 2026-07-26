# 完整手算示例

下面用四道题、二维 embedding 走完一次 NCAT 前向计算和一次 TD 更新。为使每一步可手算，attention 投影矩阵取单位矩阵，FFN 暂按恒等映射处理。真实网络中的这些矩阵由训练学习。

## 1. 当前状态

题库为

\[
\mathcal J=\{q_1,q_2,q_3,q_4\},
\qquad d=2.
\]

学生已经：

- 答对 \(q_1,q_3\)；
- 答错 \(q_2\)；
- 尚未回答 \(q_4\)。

答对 embedding 设为

\[
\mathbf e_{q_1}^1=[1,0],
\qquad
\mathbf e_{q_3}^1=[0,1],
\]

答错 embedding 设为

\[
\mathbf e_{q_2}^0=[0.8,0.2].
\]

## 2. 答对通道 self-attention

答对题矩阵是

\[
\mathbf E_t^1
=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}.
\]

缩放点积分数：

\[
\frac{\mathbf E_t^1(\mathbf E_t^1)^\top}{\sqrt2}
=
\begin{bmatrix}
0.707&0\\
0&0.707
\end{bmatrix}.
\]

逐行 softmax：

\[
W_{\mathrm{att}}^1
\approx
\begin{bmatrix}
0.67&0.33\\
0.33&0.67
\end{bmatrix}.
\]

乘以 value 后：

\[
\mathbf F_t^1
\approx
\begin{bmatrix}
0.67&0.33\\
0.33&0.67
\end{bmatrix}.
\]

第一行表示 \(q_1\) 的表示仍主要来自自己，同时吸收了 \(q_3\) 的信息；第二行同理。

## 3. 答错通道 self-attention

答错通道只有 \(q_2\)，其 attention 权重只能是 1：

\[
\mathbf F_t^0=[0.8,0.2].
\]

## 4. 从答对通道汇总到答错位置

\(q_2\) 与两个答对题的缩放点积为

\[
A
=
\begin{bmatrix}
\dfrac{[0.8,0.2][1,0]^\top}{\sqrt2}
&
\dfrac{[0.8,0.2][0,1]^\top}{\sqrt2}
\end{bmatrix}
\approx
\begin{bmatrix}
0.566&0.141
\end{bmatrix}.
\]

按行 softmax：

\[
\widetilde A^0
\approx
[0.605,0.395].
\]

因此答错题 \(q_2\) 从答对通道获得的跨通道特征是

\[
\mathbf F_t^{1\rightarrow0}
=
[0.605,0.395]
\begin{bmatrix}
0.67&0.33\\
0.33&0.67
\end{bmatrix}
\approx
[0.536,0.464].
\]

该结果更偏向 \(q_1\) 的方向，因为 \(q_2\) 与 \(q_1\) 的点积更大。

## 5. 从答错通道汇总到答对位置

答错通道只有一题。对每个答对题按另一个维度归一化后，唯一答错题的权重都是 1：

\[
\mathbf F_t^{0\rightarrow1}
=
\begin{bmatrix}
0.8&0.2\\
0.8&0.2
\end{bmatrix}.
\]

平均池化得到

\[
\overline{\mathbf f}_t^{0\rightarrow1}
=[0.8,0.2].
\]

## 6. 四路池化与拼接

四个固定维度向量分别是

\[
\overline{\mathbf f}_t^0=[0.8,0.2],
\]

\[
\overline{\mathbf f}_t^1
=
\frac12
\left(
[0.67,0.33]+[0.33,0.67]
\right)
=[0.5,0.5],
\]

\[
\overline{\mathbf f}_t^{1\rightarrow0}
=[0.536,0.464],
\]

\[
\overline{\mathbf f}_t^{0\rightarrow1}
=[0.8,0.2].
\]

按照论文的四路顺序拼接：

\[
\mathbf u_t
=
[0.8,0.2,\,
0.5,0.5,\,
0.536,0.464,\,
0.8,0.2]
\in\mathbb R^8.
\]

具体实现只要训练和推理保持同一顺序即可。

## 7. policy layer 与动作 mask

假设第一层把八维向量映射成

\[
\mathbf h=[0.9,0.4],
\]

最后一层输出

\[
Q_\phi(s_t,\cdot)
=
[0.30,0.10,0.45,0.70].
\]

题 \(q_1,q_2,q_3\) 已经作答，mask 后：

\[
\widetilde Q_\phi(s_t,\cdot)
=
[-\infty,-\infty,-\infty,0.70].
\]

因此本步选择

\[
q_t=q_4.
\]

这个前向过程的输出是每道离散题的长期选题价值。学生参数由旁边的响应模型根据累计作答估计。

## 8. 读取答案并更新学生

离线日志显示学生对 \(q_4\) 的答案为 0。状态更新为

\[
s_{t+1}
=
\{
(q_1,1),(q_2,0),(q_3,1),(q_4,0)
\}.
\]

响应模型用这四条作答重新估计学生参数。假设更新后的参数在 query 集上的 BCE 为

\[
\mathcal L_M
\left(
\mathcal D_i^u,\widehat\theta_i^{\,t}
\right)
=0.25.
\]

于是

\[
r_t=-0.25.
\]

## 9. 终止 transition 的 TD 更新

若 \(q_4\) 是最后一步，则 \(d_t=1\)：

\[
y_t=r_t=-0.25.
\]

网络此前给出

\[
Q_\phi(s_t,q_4)=0.70.
\]

单样本 TD MSE 为

\[
\mathcal L_{\mathrm{TD}}
=
\left(
0.70-(-0.25)
\right)^2
=
0.9025.
\]

梯度下降会把该状态下 \(q_4\) 的预测向 \(-0.25\) 调整。

## 10. 非终止 transition 的 TD 更新

若仍有合法题，且下一状态的最大 target Q 值为

\[
\max_{q'}Q_{\bar\phi}(s_{t+1},q')=-0.10,
\qquad
\gamma=0.8,
\]

则

\[
y_t
=
-0.25+0.8(-0.10)
=
-0.33.
\]

该目标同时包含当前 query 损失和未来选题的预计损失。Q-learning 只需比较价值大小：

\[
-0.20>-0.70,
\]

所以累计损失较小的动作会得到更大、也就是更接近 0 的 Q 值。

## 11. 两种 reward 的目标差异

原论文使用

\[
r_t=-L_t.
\]

一种可研究的替代设计是损失改善量：

\[
r_t^\Delta=L_{t-1}-L_t.
\]

它的未折扣和会发生 telescoping：

\[
\sum_{t=1}^{T}
\left(
L_{t-1}-L_t
\right)
=
L_0-L_T,
\]

主要强调最终改善。原定义

\[
\sum_{t=1}^{T}-L_t
\]

持续奖励每个中间步都保持较低 query 损失，因此更贴合“测验可能在任意步停止”的外层目标。

下一页用原论文的所有数值检查方法效果：[实验设计、完整结果与结果分析](07-experiments.md)。
