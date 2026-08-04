# Zero-shot、One-shot、Few-shot 与 Fine-tuning

## 1. 四种设置

设任务训练集为 \(\mathcal D_{\mathrm{task}}\)，预训练参数为 \(\theta_0\)。

### 1.1 Fine-tuning

通过任务数据更新参数：

\[
\theta_{\mathrm{task}}
=
\theta_0-eta\nabla_\theta
\mathcal L_{\mathrm{task}}(\theta_0).
\]

推理使用 \(\theta_{\mathrm{task}}\)。论文不把 fine-tuning 作为 GPT-3 的主要实验设置。

### 1.2 Few-shot

上下文中放 \(K\) 个示例：

\[
c_K=[x_1,y_1;\ldots;x_K,y_K;x_*].
\]

模型预测

\[
\hat y_*
\sim p_{\theta_0}(y\mid c_K).
\]

参数保持 \(\theta_0\)。论文通常取 \(K\approx10\) 到 \(100\)，上限受 2048-token context window 限制；具体任务可能用 32 或 64 个示例。

### 1.3 One-shot

\[
K=1.
\]

一个示例同时告诉模型任务映射和答案格式。

### 1.4 Zero-shot

不给输入—答案示例，只给任务自然语言说明或调用语：

```text
Translate English to French:
cheese =>
```

模型依靠说明与预训练知识完成任务。

## 2. 梯度与激活的区别

| 设置 | 参数变化 | 上下文激活变化 | 任务数据需求 |
|---|---|---|---|
| Fine-tuning | 有 | 有 | 通常较多 |
| Few-shot | 无 | 有 | 少量示例 |
| One-shot | 无 | 有 | 1 个示例 |
| Zero-shot | 无 | 有 | 说明，不含示例 |

in-context learning 的“learning”发生在单次前向的状态中。关闭上下文后，模型不会永久保留刚才的任务示例。

## 3. 一个统一翻译例子

### Fine-tuning

使用大量英法平行句对更新模型参数，再输入新英文句子。

### Few-shot

```text
sea otter => loutre de mer
peppermint => menthe poivrée
cheese =>
```

### One-shot

```text
sea otter => loutre de mer
cheese =>
```

### Zero-shot

```text
Translate English to French:
cheese =>
```

## 4. 为什么 few-shot 仍然用了标签

上下文示例里的 \(y_i\) 就是任务标签。few-shot 的优势是：

- 不需要用这些标签反向传播；
- 不为任务保存新参数；
- 更换 prompt 即可切换任务。

它仍需要人工选取、格式化或生成示例。评价它的数据效率时，应按 prompt 中真实使用的标签数量计数。

## 5. 为什么顺序和格式会重要

自回归模型读取的是 token 序列，而不是无序集合：

\[
p(y_*\mid x_1,y_1,x_2,y_2,x_*)
\ne
p(y_*\mid x_2,y_2,x_1,y_1,x_*).
\]

换行符、标签词、选项顺序和示例顺序都可能改变输出概率。原论文随机抽取 conditioning examples，但尚未全面量化 prompt 方差。

## 6. 与传统 few-shot learning 的关系

传统元学习也追求从少量样本快速适配。区别在于适配机制：

- MAML：内层执行梯度更新；
- matching/prototypical networks：计算样本与类别表示；
- GPT-3：把示例串进上下文，由 Transformer 激活实现适配。

共同点是外层先从广泛任务或数据分布中学习，面对新任务时再利用少量信息快速改变行为。
