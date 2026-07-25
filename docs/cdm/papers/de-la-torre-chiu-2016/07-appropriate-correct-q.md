# appropriate 与 correct q-vector

## appropriate q-vector

论文定义：若候选 q-vector 产生的每个潜在组内部具有同质成功概率，则该候选是 appropriate。

设候选分组为 \(G_r\)。同质性要求：

\[
p_j(\boldsymbol\alpha)
=
p_j(\boldsymbol\alpha')
\quad
\text{对所有 }
\boldsymbol\alpha,\boldsymbol\alpha'\in G_r.
\]

## correct q-vector

在全部 appropriate q-vector 中，含有最少属性者定义为 correct q-vector。

这个定义包含两个目标：

1. 分组足以解释题目成功概率结构；
2. 删除对成功概率没有贡献的属性。

## 为什么会有多个 appropriate 向量

若正确向量为 \(1110\)，那么：

- \(1110\) 产生同质组；
- \(1111\) 把同质组进一步细分，子组仍同质。

所以二者都 appropriate。correct 定义用最少属性打破平局。

## 为什么弱效应会带来困难

总体定义要求精确同质。样本中只能得到

\[
\widehat p_j(\boldsymbol\alpha).
\]

只要有抽样噪声，增设无关属性后子组估计值通常不会完全相等；漏掉一个效应很弱的真实属性时，GDI 损失也可能极小。实践算法因此使用近似规则：

\[
\operatorname{PVAF}\ge\varepsilon.
\]

阈值越低，模型越简；阈值越高，保留属性越多。

## 统计定义与内容定义

这里的 correct 由成功概率的条件同质性和最简性定义。它仍需与认知任务分析对照：

- 某属性可能在当前样本中效应很弱；
- 属性之间高度相关时，一个属性可能预测另一个；
- 已定义属性集可能遗漏了真正过程；
- 同一个观测成功率结构可能有不同内容解释。

因此论文把输出称为 suggested q-vector，并要求领域专家参与最终判断。
