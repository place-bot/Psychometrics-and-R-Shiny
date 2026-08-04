# 复杂度、路径长度与并行化

论文用每层复杂度、最少串行操作和最大路径长度比较架构。

## 1. 原论文表 1

| 层 | 每层复杂度 | 串行操作 | 最大路径 |
|---|---:|---:|---:|
| Self-attention | \(O(n^2d)\) | \(O(1)\) | \(O(1)\) |
| Recurrent | \(O(nd^2)\) | \(O(n)\) | \(O(n)\) |
| Convolution | \(O(knd^2)\) | \(O(1)\) | \(O(\log_k n)\) |
| Restricted attention | \(O(rnd)\) | \(O(1)\) | \(O(n/r)\) |

## 2. 何时 self-attention 计算更省

比较

\[
n^2d
\quad\text{与}\quad
nd^2.
\]

当 \(n<d\) 时，self-attention 的该项更小。原论文机器翻译常见子词序列长度通常低于表示维度 512。

长上下文时 \(n^2\) 会成为主要瓶颈，这催生了稀疏、局部、低秩和线性 attention。

## 3. 路径长度

self-attention 一层内任意两位置直接相连，最长路径为常数。RNN 两端位置的信息需穿过 \(O(n)\) 次递归。这会影响长距离信号的前向与反向传播。

## 4. 训练为何并行

整层可写成几个大矩阵运算，所有 query 行一起计算。causal mask 只删除非法连接，不要求按行等待。

RNN 中 \(\mathbf h_t\) 是计算 \(\mathbf h_{t+1}\) 的输入；Transformer 中同一层的 \(\mathbf z_t\) 都只依赖上一层已知矩阵。

## 5. 推理为何仍串行

自回归概率

\[
p(\mathbf y\mid\mathbf x)
=
\prod_t p(y_t\mid y_{<t},\mathbf x)
\]

要求先选出 \(y_t\) 才知道下一步输入。模型内部位置并行与外部 token 生成顺序属于两个层面。

## 6. 实际硬件视角

理论 FLOPs 之外还受显存带宽、kernel 融合、序列长度、batch、通信和 attention 矩阵存储影响。Transformer 的优势来自将串行小计算转成硬件高效的大矩阵；极长序列则可能受二次内存和计算限制。
