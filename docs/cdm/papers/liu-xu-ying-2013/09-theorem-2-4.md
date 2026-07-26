# Theorem 2.4：无噪声一致性

## 定理陈述

假设 C1--C5 成立，并且第 \(r\) 位学生对第 \(i\) 题的反应满足

\[
R_r^i
=\xi_r^i
=
\prod_{j=1}^k(A_r^j)^{Q_{ij}}.
\]

令 \(\widehat Q\) 为式（2.7）中对全部 \(m\times k\) 二元候选矩阵最小化 \(S(Q')\) 的解，则

\[
\lim_{N\to\infty}
\Pr(\widehat Q\sim Q)=1.
\tag{2.14}
\]

再定义

\[
\widetilde{\boldsymbol p}
=
\arg\inf_{\boldsymbol p}
\left\|
T(\widehat Q)\boldsymbol p-\boldsymbol\alpha
\right\|_2^2.
\tag{2.15}
\]

适当重排 \(\widehat Q\) 的列后，对任意 \(\varepsilon>0\)，

\[
\lim_{N\to\infty}
\Pr\!\left(
\|\widetilde{\boldsymbol p}-\boldsymbol p^*\|_2
\le\varepsilon
\right)=1.
\]

## 第一部分在说什么

随着学生人数增加：

- 估计 Q 落入真 Q 等价类的概率趋近 1；
- 属性列的名称仍有交换自由；
- 任何结构上不等价的 Q 最终都会被矩距离排除。

这是一致性结论。它不承诺某个有限 \(N\) 下一定恢复，也没有给出达到某一恢复率所需的样本量。

## 第二部分在说什么

一旦 Q 的列结构恢复正确，\(T(Q)\) 的满列秩使属性分布有唯一解。于是

\[
\widetilde{\boldsymbol p}
\overset{p}{\longrightarrow}
\boldsymbol p^*.
\]

这里必须先对齐属性列。若估计 Q 交换了两列，\(\widetilde{\boldsymbol p}\) 中相应的属性模式概率也会交换。

## 证明的四个台阶

### 台阶一：经验属性比例收敛

C3 给出独立同分布样本，因此

\[
\widehat{\boldsymbol p}
\overset{\text{a.s.}}{\longrightarrow}
\boldsymbol p^*.
\]

### 台阶二：真 Q 的样本损失恒为 0

\[
\boldsymbol\alpha
=T(Q)\widehat{\boldsymbol p},
\]

所以

\[
S(Q)=0.
\]

### 台阶三：错误 Q 与总体矩保持正距离

Propositions 6.3--6.4 与 Corollary 6.5 给出：

\[
Q'\not\sim Q
\quad\Longrightarrow\quad
T(Q)\boldsymbol p^*
\notin\mathcal C(T(Q')).
\]

列空间是有限维闭集，因此存在 \(\delta_{Q'}>0\)，使错误候选与真总体矩的距离至少为 \(\delta_{Q'}\)。

### 台阶四：候选 Q 有限

\(m,k\) 固定时二元 Q 只有有限多个。对所有错误候选取最小间隔：

\[
\delta
=
\min_{Q'\not\sim Q}\delta_{Q'}
>0.
\]

经验矩足够接近总体矩后，所有错误候选的损失都大于某个正数，而真 Q 的损失为 0。因此全局最小化者只能来自真等价类。

## 属性分布一致性为何需要满列秩

当 \(\widehat Q=Q\) 时，

\[
T(Q)\widetilde{\boldsymbol p}
=
\boldsymbol\alpha
=
T(Q)\widehat{\boldsymbol p}.
\]

Proposition 6.1 证明 \(T(Q)\) 满列秩，所以

\[
\widetilde{\boldsymbol p}
=
\widehat{\boldsymbol p}.
\]

再结合 \(\widehat{\boldsymbol p}\to\boldsymbol p^*\)，得到结论。

## 这一定理没有覆盖的误差

无噪声模型假设能力指示完全决定作答。真实测验中的会做但答错、不会但猜对都会破坏

\[
T(Q)\widehat{\boldsymbol p}
=\boldsymbol\alpha
\]

的逐样本精确恒等式。第 3 节把 0/1 B-vector 替换为条件答对概率，使等式转为总体层面的概率匹配。

[下一页：已知失误与猜测参数的 DINA](10-known-cg-dina.md)
