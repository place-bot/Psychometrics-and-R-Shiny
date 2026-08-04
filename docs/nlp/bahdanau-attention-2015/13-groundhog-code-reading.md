# GroundHog 原始代码精读

作者公开的 [GroundHog](https://github.com/lisa-groundhog/GroundHog/tree/master/experiments/nmt) 是 Theano/Python 2 时代实现。它适合核对论文机制与历史配置，不适合作为现代环境的直接依赖。

## 1. 文件地图

| 文件 | 职责 |
|---|---|
| `experiments/nmt/state.py` | 模型、数据、优化器与长度配置 |
| `experiments/nmt/encdec.py` | 编码器、RNNsearch 解码层、成本图 |
| `experiments/nmt/sample.py` | 采样与 beam search |
| `groundhog/trainer/SGD_adadelta.py` | Adadelta 与梯度裁剪 |
| 数据迭代器 | padding、mask、OOV 映射与长度排序 |

README 明确说明该目录包含论文使用的实现，默认 search prototype 对应 RNNsearch-50。

## 2. 配置怎样区分两个模型

固定向量配置的关键开关包括

```python
search = False
last_forward = True
forward = False
backward = False
```

RNNsearch 配置则使用

```python
search = True
last_forward = False
forward = True
backward = True
dec_rec_layer = "RecurrentLayerWithSearch"
seqlen = 50
sort_k_batches = 20
```

这些开关把单一末端向量替换为双向注释序列，并启用逐步 search/attention。

## 3. `RecurrentLayerWithSearch` 的前向路径

代码先对全部源注释预计算投影：

\[
\mathbf U_a\mathbf h_j.
\]

每个目标步再计算状态投影，广播到所有源位置，与预计算项相加，经过 \(\tanh\) 和向量投影得到 energy。随后：

1. 应用源端 mask；
2. 对源位置归一化；
3. 对注释求加权和；
4. 将上下文加入候选状态、reset gate 与 update gate；
5. 可选返回整张 alignment。

这与论文公式一一对应。

## 4. 双向注释

代码分别构造正向层和对反转序列运行的反向层，再将对应位置的分量拼接。源 mask 同时用于递归和 attention，确保 padding 既不污染隐藏状态，也不获得注意力。

## 5. 数值稳定性

历史代码直接对 energy 取 `exp` 再除以总和。现代实现通常使用数值稳定的 `softmax`：

\[
\operatorname{softmax}(\mathbf e)
=
\frac{\exp(\mathbf e-\max\mathbf e)}
{\sum_j\exp(e_j-\max\mathbf e)}.
\]

减去最大值不改变概率，却能避免较大正数指数溢出。

## 6. 优化器

`SGD_adadelta.py` 先汇总全部梯度范数，按上限 1 缩放，再执行 Adadelta 累积更新。配置中的 \(\rho=0.95,\epsilon=10^{-6}\) 与附录一致。

## 7. 数据批次

迭代器负责：

- 把词映射到整数 id；
- OOV 映射为 \([UNK]\)；
- 对源端与目标端 padding；
- 生成有效位置 mask；
- 按长度分桶减少空算；
- 对反向编码器提供反转序列。

这些数据层细节是复现 attention mask 与训练速度的必要条件。

## 8. Beam search

`sample.py` 同时维护：

- 活跃假设 token；
- 累计负对数概率；
- 每条假设的隐藏状态；
- 已完成假设；
- 可选 \([UNK]\) 屏蔽和长度归一化。

脚本的最大循环长度与源句长度相关，并包含最短长度逻辑。论文没有报告 beam width，因此代码默认值不能自动视为论文所有结果的唯一设置。

## 9. 从旧实现迁移时

需要显式处理：

- Python 2 与旧 Theano API；
- 现代 GRU 方程约定；
- 稳定 masked softmax；
- batch-first/time-first 维度；
- EOS、BOS 与 \([UNK]\) id；
- beam 父路径状态重排；
- 论文与代码的状态下标平移。

## 本页小结

GroundHog 代码验证了论文的关键工程思想：源投影预计算、逐步状态查询、源 mask、上下文进入三条 GRU 通道，以及独立维护每条 beam 的状态。现代复现应保留这些信息路径，同时更新数值稳定性和软件栈。
