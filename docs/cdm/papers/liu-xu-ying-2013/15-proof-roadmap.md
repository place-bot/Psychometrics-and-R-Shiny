# 全部证明的总路线

## 证明依赖图

\[
\boxed{\text{C1 + C2}}
\Longrightarrow
\boxed{T(Q)\text{ 满列秩}}
\]

\[
\boxed{\text{C1--C5 + } \boldsymbol p^*\succ0}
\Longrightarrow
\boxed{\text{真矩与错误 Q 的列空间分离}}
\]

\[
\boxed{\boldsymbol\alpha\to\boldsymbol\mu_Q}
+
\boxed{\text{有限候选空间}}
\Longrightarrow
\boxed{\widehat Q\sim Q\text{ 的概率趋近 1}}.
\]

## 两条线性代数任务

### 任务一：真 Q 内部的唯一性

要从

\[
T(Q)\boldsymbol p=\boldsymbol\mu
\]

唯一恢复 \(\boldsymbol p\)，需要 \(T(Q)\) 满列秩。

对应结果：

- Proposition 6.1：\(T(Q)\) 满列秩；
- Proposition 6.2：\(T_c(Q)\) 满列秩；
- Proposition 6.6：增广 \(\widetilde T_{c,g}(Q)\) 满列秩。

### 任务二：不同 Q 之间的可分离性

要恢复 Q，需要证明错误候选无法通过调整属性分布和项目参数复制真矩。

对应结果：

- Proposition 6.3：错误候选的前 \(k\) 行仍完整；
- Proposition 6.4：错误候选的前 \(k\) 行不完整；
- Corollary 6.5：合并两种情况；
- Proposition 6.6：加入猜测后仍分离。

## 为什么列空间是自然对象

固定候选 Q 与 \(\boldsymbol c\) 后，允许 \(\boldsymbol p\) 在实数空间中变化，所有线性组合形成

\[
\mathcal C(T_c(Q)).
\]

合法概率向量生成的矩集合只是该列空间中的一个凸子集。

如果真矩连错误 Q 的整个列空间都不属于，那么它当然也不属于错误 Q 的合法概率凸集。作者证明了这个更强的排除关系。

## 命题链

### Proposition 6.1

完整 Q 与饱和 T 允许抽出块上三角方阵，证明 \(T(Q)\) 满列秩。

### Proposition 6.2

\[
T_c(Q)=D_cT(Q).
\]

当每个 \(c_i\ne0\) 时，\(D_c\) 满秩，满列秩得到保留。

### Propositions 6.3--6.4

对任意 \(Q'\not\sim Q\) 和任意候选缩放参数 \(\boldsymbol c'\)，证明

\[
T_c(Q)\boldsymbol p^*
\notin
\mathcal C(T_{c'}(Q')).
\]

两条命题按候选 \(Q'_{1:k}\) 是否完整拆分。

### Corollary 6.5

把两种候选情况合并，并可令 \(c_i=1,g_i=0\) 得到无噪声分离。

### Lemma 6.7

若

\[
T_1\boldsymbol p\in\mathcal C(T_2),
\]

则对任意维度相容的 D，

\[
DT_1\boldsymbol p\in\mathcal C(DT_2).
\]

逆否命题允许作者在变换后的简单空间证明分离，再推回原空间。

### Proposition 6.6

构造只依赖 \(\boldsymbol g\) 的 D：

\[
D\widetilde T_{c,g}(Q)
=
(0,T_{c-g}(Q)).
\]

问题被化回无猜测情形，随后调用 Propositions 6.3--6.4。

## 从命题到三个定理

| 主定理 | 经验收敛 | 分离工具 | 唯一性工具 |
| --- | --- | --- | --- |
| Theorem 2.4 | \(\alpha=T(Q)\widehat p\to T(Q)p^*\) | Corollary 6.5 | Proposition 6.1 |
| Theorem 3.1 | \((\alpha^\top,1)^\top\to\widetilde T_{c,g}(Q)p_0^*\) | Proposition 6.6 | Proposition 6.6 |
| Theorem 4.2 | 真 Q 下剖面损失趋于 0 | Proposition 6.6 对全部 \(c'\) 一致分离 | \(p\) 结论另需 \(\widehat c\to c\) |

## 证明策略最有价值的一点

论文没有直接比较两个潜在类模型的完整似然。它先把响应分布投影成饱和联合正响应矩，再通过矩阵列空间研究：

\[
\text{结构相同}
\quad\Longleftrightarrow\quad
\text{矩表示能力相同到列置换}.
\]

这套“矩映射—列空间—一致性”的结构后来成为受限潜在类模型可识别性研究的重要语言。

[下一页：满列秩命题](16-full-rank-propositions.md)
