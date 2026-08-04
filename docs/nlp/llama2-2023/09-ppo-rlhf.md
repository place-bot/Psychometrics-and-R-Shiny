# PPO、组合奖励与 KL 约束

## 1. Policy 优化目标

prompt \(p\sim\mathcal D\)，回答 \(g\sim\pi_\theta(\cdot\mid p)\)。理想目标是：

\[
\max_\pi
\mathbb E_{p,g}
[R(g\mid p)].
\]

reward 来自训练好的 RM，不是每次都请人现场评分。

## 2. Helpfulness 与 Safety 的选择

先定义组合 reward：

\[
R_c(g\mid p)=
\begin{cases}
R_s(g\mid p),
&\operatorname{is\_safety}(p)
\ \text{or}\ R_s(g\mid p)<0.15,\\
R_h(g\mid p),&\text{otherwise}.
\end{cases}
\]

阈值 0.15 在 Meta Safety test set 上对应 precision 0.89、recall 0.55。潜在危险 prompt 或 safety score 很低时优先安全奖励。

## 3. Reward whitening

论文先对 \(R_c\) 做 logit 逆变换和 whitening：

\[
\widetilde R_c
=
\operatorname{whiten}
\left(
\operatorname{logit}(R_c)
\right).
\]

目的包括平衡 reward 尺度、提高 PPO 稳定性，并让它与 KL penalty 数值更匹配。

## 4. KL 约束

最终 reward：

\[
R(g\mid p)
=
\widetilde R_c(g\mid p)
-
\beta D_{\mathrm{KL}}
\left(
\pi_\theta(\cdot\mid p)
\parallel
\pi_0(\cdot\mid p)
\right).
\]

\(\pi_0\) 是原始 reference policy。KL penalty 阻止 policy 为追求 RM 高分而过度偏离可读语言分布，减少训练不稳与 reward hacking。

## 5. PPO clipped objective

令 old policy 为 \(\pi_{\mathrm{old}}\)，token action ratio：

\[
\rho_t(\theta)
=
\frac{
\pi_\theta(a_t\mid s_t)
}{
\pi_{\mathrm{old}}(a_t\mid s_t)
}.
\]

PPO 使用：

\[
\mathcal L_{\mathrm{PPO}}
=
-\mathbb E_t
\left[
\min
\left(
\rho_tA_t,
\operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)A_t
\right)
\right].
\]

clip 限制单次更新幅度。论文 clip threshold 为

\[
\epsilon=0.2.
\]

## 6. 训练超参数

- AdamW：\(\beta_1=0.9,\beta_2=0.95,\epsilon=10^{-5}\)；
- weight decay 0.1；
- gradient clipping 1.0；
- constant learning rate \(10^{-6}\)；
- PPO batch 512；
- mini-batch 64；
- 每个 mini-batch 一次 gradient step；
- 7B/13B：\(\beta=0.01\)；
- 34B/70B：\(\beta=0.005\)；
- 训练约 200–400 iterations，held-out prompt early stopping。

## 7. 系统实现

70B 每个 PPO iteration 平均约 330 秒。训练用 FSDP；FSDP 对少量 forward/backward 有效，却让 generation 慢约 20 倍。团队在生成前把模型权重整合到每个 node，生成后释放，再继续训练环节。

## 8. Reward hacking 与 Goodhart 风险

当 RM score 成为直接优化目标，policy 可能发现人类不喜欢但 RM 高分的模式。论文的缓解包括：

- KL penalty；
- on-policy 新偏好数据；
- 两个独立 RM；
- 开放数据混合增强泛化；
- GPT-4 与人工评价交叉检查；
- 每次新版本继续进入下一轮比较。

这些措施降低风险，无法从数学上保证 reward 与真实人类偏好始终一致。
