# Rejection Sampling 迭代微调

## 1. 基本算法

对每个 prompt \(p\)，从当前 policy \(\pi\) 采样 \(K\) 个回答：

\[
y^{(1)},\ldots,y^{(K)}
\sim
\pi(\cdot\mid p).
\]

reward model 打分：

\[
s_k=r(p,y^{(k)}).
\]

选择最高分回答：

\[
y^*
=
\arg\max_{1\le k\le K}s_k.
\]

把 \((p,y^*)\) 当作新 gold data，再执行类似 SFT 的梯度更新。

## 2. 它为何有效

若每次采样产生好回答的概率为 \(q\)，至少出现一个好回答的概率为：

\[
1-(1-q)^K.
\]

当 \(K\) 墅大，探索到高质量轨迹的机会增加。论文 Figure 7 显示最大 reward 随样本数上升，而中位数基本稳定；两条曲线差距就是 reranking 的潜在收益。

## 3. Temperature 与探索

采样分布为：

\[
p_\tau(y_t\mid c)
=
\operatorname{softmax}
\left(\frac{z_t}{\tau}\right).
\]

较高温度扩大多样性，让 \(K\) 个回答覆盖更多候选；过高温度会降低单个回答质量。论文发现最优 temperature 会随 RLHF 版本变化；后期模型在 \(K=10\) 到 100 时常以 \(1.2\)–\(1.3\) 获得较高最大 reward。

## 4. 只用 70B 执行 rejection sampling

论文只让最大 70B 生成并筛选 rejection-sampling 数据。较小 7B/13B 模型在 70B 选出的数据上微调，相当于把较大模型的能力蒸馏到小模型。

## 5. Breadth 与 depth

### Rejection sampling 的 breadth

同一个 policy 对每个 prompt 一次性探索 \(K\) 个回答，之后统一训练。

### PPO 的 depth

每次梯度更新后 policy 改变，下一轮 sample 来自更新后的模型，形成连续 trajectory optimization。

论文进行多轮 rejection-sampling 更新，使两者的实践差异小于一次性算法对比。

## 6. 遗忘问题

早期 RLHF-V3 只使用上一版本生成的新数据，出现押韵写诗能力回退。后续迭代把所有历史版本的高分样本一起加入：

\[
\mathcal D_t
=
\bigcup_{j=1}^{t}
\mathcal D_{\mathrm{best}}^{(j)}.
\]

历史 replay 缓解训练分布变窄与能力遗忘。

## 7. 算法伪代码

```text
输入：当前 policy π_t，reward model r_t，prompt 集 P
best_set = 历史高分样本

for p in P:
    samples = 从 π_t(·|p) 采样 K 个回答
    y_star = reward 最高的回答
    best_set 加入 (p, y_star)

π_{t+1} = 在 best_set 上执行 answer-only SFT
```

## 8. 风险

- RM 偏差会被放大；
- 采样越多，越容易找到 exploit RM 的文本；
- top-1 丢弃其他候选的信息；
- 高计算成本集中在生成与打分；
- 只从 70B 蒸馏可能传递其偏差；
- 新数据过度替代旧数据会遗忘。

论文用持续更新 RM、历史 replay、人工复核与后续 PPO 减轻这些问题。
