# 偏好数据与双 Reward Model

## 1. 数据怎样采集

标注者先写一个 prompt，系统从不同模型版本和不同 temperature 采样两个回答。标注者必须选择较好者，并标注偏好强度：

- significantly better；
- better；
- slightly better；
- negligibly better / unsure。

帮助性与安全性使用不同指南。安全数据还标注：

1. preferred safe、另一条 unsafe；
2. 两条都 safe；
3. 两条都 unsafe。

论文不保留“preferred unsafe、另一条 safe”的配对，因为安全回答按指南应被偏好。

## 2. 数据规模

Meta 自采 safety + helpfulness preference comparisons 共：

\[
1{,}418{,}091.
\]

再混合 Anthropic Helpful/Harmless、OpenAI Summarize/WebGPT、StackExchange、Stanford SHP 与 Synthetic GPT-J 等公开数据，总比较数为：

\[
2{,}919{,}326.
\]

一条 comparison 含共享 prompt、chosen response 与 rejected response。

## 3. Reward model 架构

从 pretrained chat checkpoint 初始化，与语言模型主体架构相同；去掉 next-token vocabulary head，换成输出一个标量的 regression head：

\[
r_\phi(p,y)\in\mathbb R.
\]

初始化自 chat model 让 RM 继承语言和事实知识，降低 reward model 因知识不足而偏好 hallucination 的风险。

## 4. Pairwise ranking loss

对 preferred \(y_c\) 与 rejected \(y_r\)：

\[
\mathcal L_{\mathrm{rank}}
=
-\log\sigma
\left(
r_\phi(p,y_c)-r_\phi(p,y_r)
\right).
\]

优化会增大 chosen 与 rejected 的 reward gap。

## 5. Preference margin

论文利用偏好强度加入 margin：

\[
\mathcal L_{\mathrm{rank}}
=
-\log\sigma
\left(
r_\phi(p,y_c)-r_\phi(p,y_r)-m(q)
\right),
\]

其中 \(q\) 是偏好等级。差异明显的回答使用更大 margin；接近或不确定的比较使用更小 margin。

## 6. 两个 RM 的训练混合

### Helpfulness RM

使用全部 Meta helpfulness，再从 Meta safety 与公开数据中均匀抽取相等部分。

### Safety RM

使用全部 Meta safety 与 Anthropic Harmless，再以 90/10 方式混入 safety 主数据和 helpfulness 数据。少量 helpfulness 对“两条都 safe”的细粒度比较有帮助。

## 7. 训练配置

- 1 epoch，继续训练会过拟合；
- 与 base model 相同 optimizer 参数；
- 70B max learning rate \(5\times10^{-6}\)；
- 其余规模 \(1\times10^{-5}\)；
- cosine decay 到最大值 10%；
- warmup 约总 steps 的 3%，至少 5 steps；
- effective batch 512 pairs，即 1024 rows。

## 8. Reward model 结果

| RM | Meta Helpful | Meta Safety | 平均 |
|---|---:|---:|---:|
| Safety RM | 56.2 | **64.5** | 64.3 |
| Helpfulness RM | **63.2** | 62.8 | **70.6** |

Helpfulness RM 在自身域更强，Safety RM 在安全域更强。偏好越明显，准确率越高；对 negligibly better / unsure 的配对，两者都接近中低 50%，反映任务主观性和噪声。

## 9. On-policy 分布问题

偏好批次每周收集。新 Chat 模型生成分布持续改变，因此 RM 要看到最新模型回答。否则

\[
p_{\mathrm{new\ policy}}(y\mid p)
\ne
p_{\mathrm{RM\ train}}(y\mid p),
\]

RM accuracy 会下降，policy 也更容易利用评分盲点。
