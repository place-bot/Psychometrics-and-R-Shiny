# 状态编码与双通道 attention

NCAT 的神经网络要把一个长度可变、答对答错混合的集合状态 \(s_t\) 变成固定维度向量，再输出所有候选题的 Q 值。

## 1. 为什么分两个通道

设第 \(t\) 步之前：

- 答错题集合含 \(k_0\) 道题；
- 答对题集合含 \(k_1\) 道题。

同一道题的正确反应与错误反应携带不同测量信息，因此论文使用两张独立 embedding 表：

\[
E^0\in\mathbb R^{|\mathcal J|\times d},
\qquad
E^1\in\mathbb R^{|\mathcal J|\times d}.
\]

把已答错题查表得到

\[
\mathbf E_t^0
=
[\mathbf e_{q_1}^0,\ldots,\mathbf e_{q_{k_0}}^0]^\top
\in\mathbb R^{k_0\times d},
\]

把已答对题查表得到

\[
\mathbf E_t^1
=
[\mathbf e_{q_1}^1,\ldots,\mathbf e_{q_{k_1}}^1]^\top
\in\mathbb R^{k_1\times d}.
\]

实现中的 padding 题号不能参与 attention 和 pooling。

## 2. Performance Learning：通道内建模

答对题之间、答错题之间都可能存在知识点、难度和题型关系。NCAT 分别对两个通道使用 self-attention：

\[
\mathbf S_t^z
=
\operatorname{Attention}
\left(
\mathbf E_t^zW_{1,c}^z,
\mathbf E_t^zW_{1,k}^z,
\mathbf E_t^zW_{1,v}^z
\right),
\qquad z\in\{0,1\}.
\tag{1}
\]

缩放点积 attention 定义为

\[
\operatorname{Attention}(C,K,V)
=
\operatorname{softmax}
\left(
\frac{CK^\top}{\sqrt d}
\right)V.
\tag{2}
\]

再通过逐位置前馈网络：

\[
\mathbf F_t^z
=
\operatorname{FFN}(\mathbf S_t^z)
=
\sigma(\mathbf S_t^zW^{(1)}+b^{(1)})W^{(2)}+b^{(2)}.
\tag{3}
\]

论文使用 ReLU 作为 \(\sigma\)。真实代码还包含多头投影、残差、LayerNorm 和 dropout。

### 一个两题 self-attention 小例子

假设某通道有两题、\(d=2\)，为突出机制令投影矩阵都是单位阵：

\[
\mathbf E
=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}.
\]

分数矩阵为

\[
\frac{\mathbf E\mathbf E^\top}{\sqrt2}
=
\begin{bmatrix}
1/\sqrt2&0\\
0&1/\sqrt2
\end{bmatrix}.
\]

逐行 softmax 后，对角权重较大，表示每道题更关注自身；若两题 embedding 相似，非对角权重会增加，输出便会融合另一题的信息。

## 3. Contradiction Learning：跨通道建模

单看答对集合或答错集合还不足以识别反应矛盾。例如：

- 学生答对一道高难度乘法题；
- 同时答错一道较简单、知识点相关的加法题。

这可能来自猜测、失误、题目歧义或局部知识结构。NCAT 为每个“答错题—答对题”配对计算 contradiction score：

\[
\alpha_{ij}
=
\frac{
(W_{2,c}^0\mathbf e_{q_i}^0)
(W_{2,k}^1\mathbf e_{q_j}^1)^\top
}{
\sqrt d
}.
\tag{4}
\]

所有分数组成

\[
A\in\mathbb R^{k_0\times k_1}.
\]

对 \(A\) 分别按行和按列 softmax：

\[
\widetilde A^0_{ij}
=
\frac{\exp(\alpha_{ij})}
{\sum_{j'=1}^{k_1}\exp(\alpha_{ij'})},
\qquad
\widetilde A^1_{ij}
=
\frac{\exp(\alpha_{ij})}
{\sum_{i'=1}^{k_0}\exp(\alpha_{i'j})}.
\tag{5}
\]

然后跨通道聚合 Performance Learning 的输出：

\[
\mathbf F_t^{1\rightarrow0}
=
\operatorname{FFN}
\left(
\widetilde A^0\mathbf F_t^1
\right)
\in\mathbb R^{k_0\times d},
\tag{6}
\]

\[
\mathbf F_t^{0\rightarrow1}
=
\operatorname{FFN}
\left(
(\widetilde A^1)^\top\mathbf F_t^0
\right)
\in\mathbb R^{k_1\times d}.
\tag{7}
\]

两次归一化回答不同问题：

- 每道答错题最应参考哪些答对题；
- 每道答对题最应参考哪些答错题。

## 4. 从四个矩阵到一个学生状态向量

论文对四个矩阵分别做平均池化：

\[
\operatorname{pool}(\mathbf X)
=
\frac{1}{m}\sum_{r=1}^{m}\mathbf X_{r,:}.
\tag{8}
\]

拼接得到

\[
\mathbf u_t
=
\operatorname{concat}
\left[
\operatorname{pool}(\mathbf F_t^0),
\operatorname{pool}(\mathbf F_t^1),
\operatorname{pool}(\mathbf F_t^{1\rightarrow0}),
\operatorname{pool}(\mathbf F_t^{0\rightarrow1})
\right]
\in\mathbb R^{4d}.
\tag{9}
\]

policy layer 输出：

\[
Q_\phi(s_t,\cdot)
=
\delta(\mathbf u_tW^{(1)}+b^{(1)})W^{(2)}+b^{(2)}
\in\mathbb R^{|\mathcal J|}.
\tag{10}
\]

其中 \(W^{(1)}\in\mathbb R^{4d\times d_p}\)，\(W^{(2)}\in\mathbb R^{d_p\times|\mathcal J|}\)。

## 5. 论文与仓库的 pooling 差异

论文式 (8) 对四路特征都做平均池化。公开仓库 `NCAT.py` 的实际 forward 是：

- 两个 contradiction 输出在序列维取 mean；
- 两个 self-attention 通道取各自“最后一个有效位置”；
- 再拼成 \(4d\) 向量。

核心代码对应：

```python
input_01, input_10 = self.contradiction(
    item_emb_0, item_emb_1, item_per_1, item_per_0
)
input_01, input_10 = input_01.mean(-2), input_10.mean(-2)

input_0 = item_per_0[torch.arange(batch_size), p_0_target]
input_1 = item_per_1[torch.arange(batch_size), p_1_target]
state_vector = torch.cat([input_0, input_1, input_01, input_10], dim=-1)
q_values = self.policy_layer(state_vector)
```

这使仓库表示对序列填充位置和“最后有效题”更敏感。论文同时假设短测期间能力稳定、反应顺序不重要，因此若目标是复现论文公式，masked mean 更一致。

## 6. 空通道怎样处理

第一步时两个通道都为空；之后也可能只有答对或只有答错。实现必须定义：

1. 专用空状态 token；
2. 或一个 padding token 加有效长度；
3. masked pooling 的分母至少为 1；
4. cross-attention 在一侧为空时返回零向量或可学习 empty vector。

一个安全的 masked mean：

```python
def masked_mean(x, mask):
    weight = mask.unsqueeze(-1).to(x.dtype)
    total = (x * weight).sum(dim=1)
    denom = weight.sum(dim=1).clamp_min(1.0)
    return total / denom
```

!!! warning "padding 泄漏会制造伪规律"

    padding embedding、非法题和空通道若处理不一致，网络可能从序列长度或填充值中学习数据划分特征。应专门测试：增加 padding 后同一真实状态的 Q 值不变。

## 7. 网络在每一步怎样保持 adaptive

学生答题后，至少三处发生变化：

1. 新题进入答对或答错通道；
2. attention 权重与跨通道 contradiction 重新计算；
3. 已答题从合法动作集中移除。

于是

\[
Q_\phi(s_{t+1},\cdot)
\neq
Q_\phi(s_t,\cdot)
\]

一般成立，下一题会根据实时答案分叉。完整训练与上线过程见[训练与真实学生部署](05-training-and-deployment.md)。
