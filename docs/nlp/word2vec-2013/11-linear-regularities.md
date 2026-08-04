# 线性规律的含义与边界

## 1. 关系作为位移向量

若词对 \((a,b)\) 表达某种关系，可以用差值表示：

\[
\mathbf r_{a\rightarrow b}
=\mathbf v_b-\mathbf v_a.
\]

两个词对关系相似时，期望

\[
\mathbf v_b-\mathbf v_a
\approx
\mathbf v_d-\mathbf v_c.
\]

移项得到类比查询：

\[
\mathbf v_d
\approx
\mathbf v_b-\mathbf v_a+\mathbf v_c.
\]

几何上，这要求两个差值向量大致平行且长度相近。

## 2. 论文 Table 8 的关系

Table 8 使用 300 维、783M 训练词的 Skip-gram 向量展示：

| 关系示例 | 推出的对应词 |
|---|---|
| France → Paris | Italy → Rome；Japan → Tokyo；Florida → Tallahassee |
| big → bigger | small → larger；cold → colder；quick → quicker |
| Miami → Florida | Baltimore → Maryland；Dallas → Texas；Kona → Hawaii |
| Einstein → scientist | Messi → midfielder；Mozart → violinist；Picasso → painter |
| Sarkozy → France | Berlusconi → Italy；Merkel → Germany；Koizumi → Japan |
| copper → Cu | zinc → Zn；gold → Au；uranium → plutonium |
| Berlusconi → Silvio | Sarkozy → Nicolas；Putin → Medvedev；Obama → Barack |
| Microsoft → Windows | Google → Android；IBM → Linux；Apple → iPhone |
| Microsoft → Ballmer | Google → Yahoo；IBM → McNealy；Apple → Jobs |
| Japan → sushi | Germany → bratwurst；France → tapas；USA → pizza |

表中同时包含清晰对应、近似相关和明显偏离目标的结果。作者指出，若使用类比集的严格精确匹配规则，这些展示例子约只有 60% 会得分。

## 3. 为什么线性结构可能出现

本文没有给出线性规律的形式化定理。可以从训练目标得到三个直觉。

### 3.1 共享输出决策面

Skip-gram 中，每个输入词向量都要对大量输出节点产生正确分数。拥有相似上下文分布的词，需要在许多共享决策面上给出相似结果，因此向量趋于接近。

### 3.2 系统性上下文变化

若从单数到复数会系统性改变上下文分布，多个词对可能接收结构相近的梯度变化，形成近似共同方向。

### 3.3 低维压缩

大量共现模式被压缩进 \(D\) 维空间。最稳定、重复最多的变化因素容易形成可重用方向。

这些解释给出机制直觉，没有保证每类语言关系都对应唯一线性方向。

## 4. 关系方向的平均

单个词对差值包含个体语义。例如

\[
\mathbf v_{\text{Paris}}-\mathbf v_{\text{France}}
\]

同时包含首都关系、地理主题、新闻频率等因素。对多个示例求平均：

\[
\overline{\mathbf r}
=\frac{1}{K}\sum_{k=1}^{K}
(\mathbf v_{b_k}-\mathbf v_{a_k}),
\]

可以削弱词对特有噪声，保留共同关系。论文报告 \(K=10\) 时准确率绝对提高约 10 个百分点。

## 5. 坐标轴没有固定语义

若对所有向量施加同一个正交变换 \(R\)：

\[
\mathbf v'_w=R\mathbf v_w,
\qquad R^\top R=I,
\]

则点积、余弦和欧氏距离保持：

\[
(R\mathbf a)^\top(R\mathbf b)
=\mathbf a^\top\mathbf b.
\]

类比差值也整体旋转：

\[
R(\mathbf v_b-\mathbf v_a+\mathbf v_c).
\]

因此，模型可以在不改变几何关系的情况下旋转坐标。把第 17 维命名为“性别维”、第 42 维命名为“国家维”通常缺乏唯一性；子空间和方向比较更稳妥。

## 6. 关系不一定是单一方向

同一标签可能包含多个子关系：

- 不规则过去式与规则过去式；
- 国家首都与州首府；
- 生物性别、社会角色与语法性别；
- 公司创始人、CEO、产品和竞争者。

一个全局差值方向可能只近似覆盖其中一部分。Table 8 中 `uranium → plutonium`、`Google → Yahoo` 等输出就反映了相关性与精确关系之间的偏差。

## 7. 余弦近邻的密度问题

类比评价依赖全词表最近邻。高频词、向量空间各向异性和“hubness”会使少数词成为许多查询的近邻。即使关系向量合理，最近邻搜索也可能被局部密度影响。

常见后续处理包括：

- 均值中心化；
- 去除高方差主成分；
- 使用 3CosMul 等替代类比分数；
- 局部密度校正；
- 对输入和输出向量进行组合。

这些方法都不属于本文原始实验。

## 8. 线性类比与语言理解

类比命中说明训练语料中的某些统计关系在向量空间中形成了稳定几何结构。它没有直接证明模型掌握：

- 事实真伪；
- 组合语义；
- 事件因果；
- 语境中的具体词义；
- 新句子的完整语法。

Table 7 中 Skip-gram 单独句子补全准确率为 48.0%，低于 RNNLM 的 55.4%，恰好说明强词关系与强序列模型是不同能力。

## 9. 语料偏差会进入几何空间

词向量学习语料中的共现结构。社会刻板印象、历史不平等、新闻报道偏向和领域分布都会写入近邻与关系方向。向量算术可以放大这些规律。

因此，部署词向量时应评估：

- 不同群体词的近邻；
- 职业、情感和能力词的关联差异；
- 语料来源与时间；
- 下游模型对这些方向的敏感性；
- 去偏方法造成的信息损失。

本文发表于 2013 年，没有进行系统公平性审计。

## 10. “代数”一词的准确用法

论文展示的是向量空间中的加减运算和近邻检索。关系满足近似平行性，而非建立了词义的封闭代数系统。更准确的表述是：

> 某些语义和句法关系在所学嵌入空间中表现为近似一致的线性位移。

这已经是非常重要的发现，也保留了证据本身的范围。
