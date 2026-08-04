# 神经机器翻译概率基础与固定向量瓶颈

## 1. 翻译是条件序列建模

给定源句

\[
\mathbf x=(x_1,\ldots,x_{T_x}),
\]

翻译系统需要寻找目标句

\[
\mathbf y=(y_1,\ldots,y_{T_y})
\]

使条件概率最大：

\[
\widehat{\mathbf y}
=
\operatorname*{arg\,max}_{\mathbf y}
p_\theta(\mathbf y\mid\mathbf x).
\]

模型参数 \(\theta\) 从平行句对中学习。

## 2. 自回归分解

联合条件概率按目标词顺序分解：

\[
p_\theta(\mathbf y\mid\mathbf x)
=
\prod_{i=1}^{T_y}
p_\theta(y_i\mid y_1,\ldots,y_{i-1},\mathbf x).
\tag{1}
\]

取对数：

\[
\log p_\theta(\mathbf y\mid\mathbf x)
=
\sum_{i=1}^{T_y}
\log p_\theta(y_i\mid y_{<i},\mathbf x).
\tag{2}
\]

这使句子级目标转成一系列词级预测，但每个词级条件仍然依赖完整源句和目标前缀。

## 3. 训练目标

设平行语料为

\[
\mathcal D
=
\{(\mathbf x^{(n)},\mathbf y^{(n)})\}_{n=1}^{N}.
\]

最大似然训练等价于最小化负对数似然：

\[
\mathcal L(\theta)
=
-\sum_{n=1}^{N}
\sum_{i=1}^{T_y^{(n)}}
\log
p_\theta
\left(
y_i^{(n)}
\mid
y_{<i}^{(n)},
\mathbf x^{(n)}
\right).
\tag{3}
\]

实际计算还需要 mask，排除 batch 中补齐出来的 padding 位置。

## 4. 训练时的目标前缀

在每个训练位置，模型读取真实的前一目标词 \(y_{i-1}\)，预测真实的当前词 \(y_i\)。这种做法后来通常称为 teacher forcing。

```text
真实目标句： <bos>  le  chat  dort  <eos>
输入前缀：   <bos>  le   chat  dort
监督目标：     le   chat  dort  <eos>
```

训练损失可以汇总多个目标位置，但 RNN 隐藏状态仍按时间递推。

推理时真实目标前缀不可用，模型必须读取自己已经生成的词。训练与推理前缀来源不同，这会带来 exposure bias。

## 5. 基础 RNN Encoder–Decoder

### 5.1 编码器

编码器按顺序读取源词：

\[
\mathbf h_t
=
f_{\mathrm{enc}}
(\mathbf h_{t-1},\mathbf E_x x_t).
\tag{4}
\]

其中 \(\mathbf E_x x_t\) 表示源词嵌入。

最后用一个固定向量概括源句：

\[
\mathbf c
=
q(\mathbf h_1,\ldots,\mathbf h_{T_x}).
\tag{5}
\]

常见选择为：

\[
\mathbf c=\mathbf h_{T_x}.
\tag{6}
\]

### 5.2 解码器

解码状态递推：

\[
\mathbf s_i
=
f_{\mathrm{dec}}
(\mathbf s_{i-1},\mathbf E_y y_{i-1},\mathbf c).
\tag{7}
\]

目标词概率为：

\[
p_\theta(y_i\mid y_{<i},\mathbf x)
=
g(y_{i-1},\mathbf s_i,\mathbf c).
\tag{8}
\]

所有目标位置共享同一个 \(\mathbf c\)。

## 6. 固定向量接口

基础模型的信息流为：

```text
x1 → x2 → ... → xTx
                  │
                  ▼
             单一向量 c
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
      y1         y2        ... yTy
```

\(\mathbf c\) 同时是：

- 编码器到解码器的唯一直接通道；
- 每个目标位置共享的源句摘要；
- 解码器恢复全部源端细节的依据。

## 7. 瓶颈为什么随句长加剧

### 7.1 信息数量增加

源句越长，需要保留的实体、关系和局部结构通常越多。

### 7.2 递归距离增加

早期源词对最后状态的影响需要穿过更多次递归更新，梯度也要沿更长路径返回。

### 7.3 解码需求随时间改变

生成目标词 \(y_i\) 和 \(y_{i+k}\) 需要关注的源信息不同。固定 \(\mathbf c\) 无法显式改变读取位置。

### 7.4 训练长度分布限制

超过训练长度的句子要求模型把更多信息压入相同维度，并保持更长时间。

## 8. 维度固定与信息固定

“固定长度”描述向量维度不随源句长度变化：

\[
\mathbf c\in\mathbb R^d
\quad
\text{对任意 }T_x.
\]

一个实数向量在数学上可以编码很多信息，因此瓶颈并非简单的信息论不可能性结论。论文关注可学习性：

- 有限精度；
- 有限参数；
- 有限训练数据；
- RNN 的梯度传播；
- 可泛化的连续表示；
- 下游解码器能否稳定取回细节。

## 9. RNNsearch 的概率改写

RNNsearch 为每个目标位置引入 \(\mathbf c_i\)：

\[
p_\theta
(y_i\mid y_{<i},\mathbf x)
=
g(y_{i-1},\mathbf s_i,\mathbf c_i),
\tag{9}
\]

\[
\mathbf s_i
=
f_{\mathrm{dec}}
(\mathbf s_{i-1},y_{i-1},\mathbf c_i).
\tag{10}
\]

条件概率仍然保持式 (1) 的自回归分解。改变的是源端信息接口：

\[
\mathbf c
\quad\longrightarrow\quad
\mathbf c_1,\ldots,\mathbf c_{T_y}.
\]

## 10. 从压缩到可寻址读取

RNNsearch 的编码器输出：

\[
H
=
(\mathbf h_1,\ldots,\mathbf h_{T_x}).
\]

解码器第 \(i\) 步通过注意力读取：

\[
\operatorname{Read}(\mathbf s_{i-1},H)
=
\mathbf c_i.
\]

这可以理解为一个可微的内容寻址过程：

1. 用 \(\mathbf s_{i-1}\) 表示当前翻译进度；
2. 与每个 \(\mathbf h_j\) 计算兼容性；
3. 对源位置归一化；
4. 聚合需要的信息。

## 11. 动态上下文仍是固定维度

每个 \(\mathbf c_i\) 的维度仍然固定：

\[
\mathbf c_i\in\mathbb R^{d_h}.
\]

关键差异在于 \(\mathbf c_i\) 可以随 \(i\) 改变。模型无需让一个向量永久保存全部信息，只需在当前步骤形成合适摘要。

## 12. 两种模型的结构对照

| 维度 | RNNencdec | RNNsearch |
|---|---|---|
| 源端输出 | 单一向量 | 注释序列 |
| 源句方向 | 单向 RNN | 双向 RNN |
| 目标端上下文 | 所有步骤相同 | 每一步重新计算 |
| 对齐 | 无显式机制 | 可微软对齐 |
| 训练监督 | 目标词 | 目标词 |
| 长句信息路径 | 全部经过最终编码状态 | 可从任意源位置直接读取 |
| 每步额外成本 | 低 | 遍历全部源位置打分 |

## 13. 似然与 BLEU 的关系

训练直接优化式 (3) 的 token-level log-likelihood。实验用 BLEU 评价生成译文。

两者目标不同：

- 似然奖励真实目标序列中每个词的条件概率；
- BLEU 比较生成句与参考句的 n-gram 重合并含长度惩罚；
- beam search 近似寻找高概率序列；
- 更高似然通常有助于翻译，但不保证 BLEU 单调提高。

论文训练期间报告 NLL，最终比较报告 BLEU。

## 14. 这一章的主结论

RNNsearch 没有改变神经机器翻译的自回归概率定义。它重新设计了条件概率中“怎样访问源句”的机制：

\[
\boxed{
\text{单一固定摘要}
\;\longrightarrow\;
\text{由解码状态控制的逐步软读取}
}
\]

下一章具体说明可被读取的源端注释怎样由双向编码器产生。
