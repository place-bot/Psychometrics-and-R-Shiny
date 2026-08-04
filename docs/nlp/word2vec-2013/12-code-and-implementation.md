# 公开代码与最小实现

## 1. 代码身份

论文 v3 的 Follow-Up Work 指向 Google Code 上的多线程 C 实现。项目现保存在 [Google Code Archive](https://code.google.com/archive/p/word2vec/)。核心文件包括：

| 文件 | 功能 |
|---|---|
| `word2vec.c` | 词表、Huffman 树、CBOW、Skip-gram、HS、负采样和多线程训练 |
| `compute-accuracy.c` | 语义—句法类比准确率 |
| `distance.c` | 最近邻查询 |
| `word-analogy.c` | 交互式词类比 |
| `word2phrase.c` | 短语发现 |
| `questions-words.txt` | 19,544 个类比问题和 14 个类别标题 |

归档代码已经吸收同年后续工作的功能。阅读代码时需要区分“本文原始方法”和“后续 Word2Vec 工具”。

## 2. 核心参数数组

公开 C 代码使用：

| C 名称 | 数学含义 | 形状 |
|---|---|---|
| `syn0` | 输入词向量 \(W_{\mathrm{in}}\) | \(V\times D\) |
| `syn1` | hierarchical-softmax 内部节点向量 \(U\) | 约 \((V-1)\times D\) |
| `syn1neg` | negative-sampling 输出词向量 | \(V\times D\) |
| `neu1` | CBOW 聚合表示 \(\mathbf h\) | \(D\) |
| `neu1e` | 返回输入侧的累计误差 | \(D\) |
| `expTable` | sigmoid 查找表 | 固定长度 |

本文原始 hierarchical-softmax 复现只需要 `syn0` 和 `syn1`。

## 3. Huffman 树实现

`CreateBinaryTree()` 的主要步骤是：

1. 把词按频率排序；
2. 维护尚未合并的词节点与新建内部节点；
3. 每次取两个最小计数节点合并；
4. 保存父节点和二进制分支；
5. 为每个词生成根到叶 code 与内部节点路径。

核心不变量为：

\[
\operatorname{count}(\text{parent})
=\operatorname{count}(\text{left})
+\operatorname{count}(\text{right}).
\]

高频词在构树过程中更晚被合并，因而离根更近。

## 4. 代码中的分支标签

hierarchical-softmax 更新使用近似形式：

```c
g = (1 - code[d] - sigmoid(f)) * alpha;
```

这里代码把期望 sigmoid 输出定义为

\[
y=1-\operatorname{code}[d].
\]

若 code 为 0，则期望 \(y=1\)；若 code 为 1，则期望 \(y=0\)。这只是左右分支的编码约定。对应梯度上升更新为

\[
\eta(y-p),
\]

与最小化交叉熵时的 \(-\eta(p-y)\) 完全一致。

## 5. 动态窗口的实际代码

代码先采样

```c
b = next_random % window;
```

随后只遍历从 `b` 到 `2*window-b` 的位置。有效半径为

\[
R=\text{window}-b.
\]

因为

\[
b\in\{0,1,\ldots,C-1\},
\]

所以

\[
R\in\{1,2,\ldots,C\}
\]

均匀分布，与论文描述一致。

## 6. CBOW 代码路径

CBOW 分支执行：

1. 将窗口内 `syn0` 向量累加到 `neu1`；
2. 除以有效上下文数 `cw`；
3. 对目标词 Huffman 路径计算 sigmoid；
4. 把路径误差累计进 `neu1e`；
5. 更新 `syn1`；
6. 将 `neu1e` 加回每个上下文的 `syn0`。

这验证了正文“平均上下文向量”的实现。

## 7. Skip-gram 代码路径

Skip-gram 分支对窗口内每个 `last_word`：

1. 读取该词的 `syn0`；
2. 沿当前 `word` 的 Huffman 路径计算损失；
3. 更新 `syn1`；
4. 把误差写回 `last_word` 的 `syn0`。

变量方向与论文图 1 的表述相反：代码块表面上以窗口词预测当前词。滑动窗口会在语料中产生大量双向相邻关系，但逐样本目标方向仍有区别。需要精确重现实验时，应固定所使用源码版本并按代码执行；讲解架构时通常沿用论文定义的中心词预测附近词。

## 8. 公开代码为何不能直接代表本文

归档版本默认参数包括：

```text
negative = 5
hs = 0
sample > 0
```

并包含 `word2phrase.c`。这些功能对应同年后续论文中的：

- negative sampling；
- 高频词下采样；
- 短语学习。

若目标是贴近本文的训练机制，命令配置应明确使用：

```bash
./word2vec \
  -train corpus.txt \
  -output vectors.bin \
  -cbow 1 \
  -size 300 \
  -window 4 \
  -hs 1 \
  -negative 0 \
  -sample 0 \
  -iter 3 \
  -binary 1
```

Skip-gram 把 `-cbow 1` 改为 `-cbow 0`，论文主要实验的最大窗口为 10。命令中的具体线程、词频阈值和语料处理仍需另行记录。

## 9. 最小 Python 数据结构

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class HuffmanPath:
    nodes: np.ndarray   # [path_length]
    labels: np.ndarray  # 0/1, [path_length]

class Word2VecHS:
    def __init__(self, vocab_size, dim, paths, seed=0):
        rng = np.random.default_rng(seed)
        self.w_in = rng.uniform(
            -0.5 / dim,
            0.5 / dim,
            size=(vocab_size, dim),
        )
        self.u_node = np.zeros((vocab_size - 1, dim))
        self.paths = paths
```

树有 \(V-1\) 个内部节点，因此 `u_node` 的第一维为 `vocab_size - 1`。

## 10. 稳定 sigmoid 与路径更新

```python
def sigmoid(x):
    if x >= 0:
        z = np.exp(-x)
        return 1.0 / (1.0 + z)
    z = np.exp(x)
    return z / (1.0 + z)

def hs_update(h, path, u_node, learning_rate):
    grad_h = np.zeros_like(h)

    for node, label in zip(path.nodes, path.labels):
        u_old = u_node[node].copy()
        p = sigmoid(np.dot(u_old, h))
        delta = p - label

        grad_h += delta * u_old
        u_node[node] -= learning_rate * delta * h

    return grad_h
```

复制 `u_old` 可以保证输入梯度使用更新前的节点参数。

## 11. CBOW 单步

```python
def cbow_step(model, context_ids, target_id, learning_rate):
    context_ids = np.asarray(context_ids, dtype=np.int64)
    h = model.w_in[context_ids].mean(axis=0)

    grad_h = hs_update(
        h,
        model.paths[target_id],
        model.u_node,
        learning_rate,
    )

    grad_each = grad_h / len(context_ids)
    np.add.at(model.w_in, context_ids, -learning_rate * grad_each)
```

`np.add.at` 能正确处理上下文中重复词索引。

## 12. Skip-gram 单步

```python
def skipgram_step(model, center_id, target_ids, learning_rate):
    for target_id in target_ids:
        h = model.w_in[center_id].copy()
        grad_h = hs_update(
            h,
            model.paths[target_id],
            model.u_node,
            learning_rate,
        )
        model.w_in[center_id] -= learning_rate * grad_h
```

每个上下文目标完成一次独立的路径更新。

## 13. 类比评价实现

```python
def analogy(vectors, a, b, c):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    unit = vectors / np.maximum(norms, 1e-12)
    query = unit[b] - unit[a] + unit[c]
    scores = unit @ query
    scores[[a, b, c]] = -np.inf
    return int(np.argmax(scores))
```

大词表上可使用分块矩阵乘法或近似最近邻索引，避免一次保存全部候选分数。

## 14. 单元检查

实现应通过以下检查：

- 每个词路径最终到达唯一叶节点；
- Huffman 高频词平均路径更短；
- 单个 HS 样本更新后目标路径损失下降；
- CBOW 上下文置换不改变前向结果；
- Skip-gram 实际窗口半径在 \(1\) 到 \(C\) 之间；
- 输入矩阵和节点矩阵都得到非零梯度；
- 类比检索排除三个输入词；
- OOV 题计入 coverage，而不进入可计算准确率分母。

## 15. 论文级与工具级复现

建议维护两套配置：

| 配置 | 目的 | 关键选项 |
|---|---|---|
| paper-HS | 理解本文 | CBOW/SG + Huffman HS，无负采样 |
| later-word2vec | 使用成熟工具技巧 | 负采样、下采样、短语等 |

把两套配置分开，才能准确判断性能来自原始架构还是后续改进。
