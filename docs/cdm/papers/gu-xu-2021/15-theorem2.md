# Theorem 2：只测两次时的三种结构

## 1. 标准形

假设属性 1 恰好被两道题要求。经行列置换后，

\[
Q=
\begin{pmatrix}
1&\boldsymbol0^\top\\
1&\boldsymbol v^\top\\
\boldsymbol0&Q^\star
\end{pmatrix},
\]

其中

\[
\boldsymbol v\in\{0,1\}^{K-1},
\qquad
Q^\star\in\{0,1\}^{(J-2)\times(K-1)}.
\]

第一题只测属性 1；第二题同时测属性 1 和由 \(\boldsymbol v\) 指定的其他属性；其余题不测属性 1。

## 2. 属性只出现一次

\[
\exists k:\sum_jq_{jk}=1
\]

时，DINA 不具有泛识别。该属性与唯一题目的参数可以连续互换。

## 3. Case (a)：\(\boldsymbol v=\boldsymbol1\)

第二题要求属性 1 和其余全部属性：

\[
\boldsymbol q_2=(1,1,\ldots,1).
\]

结论是模型连局部泛识别也不成立。真参数任意小邻域内都存在无穷多组等价参数。

直觉上，第二题只在全掌握潜类中进入能力状态，难以把属性 1 的独立贡献与全掌握类比例分开。

## 4. Case (b)：\(\boldsymbol v=\boldsymbol0\)

前两题都是属性 1 的单属性题。以下任一条件可保证全局泛识别：

### (b.1)

\(Q^\star\) 对其余 \(K-1\) 个属性满足 Theorem 1 的 A/B/C。

### (b.2)

\(Q^\star\) 含两套

\[
I_{K-1}.
\]

该结论覆盖四题两属性例子。此时 \(Q^\star\) 对单个剩余属性含两道单位题。

## 5. Case (c)：\(\boldsymbol v\ne\boldsymbol0,\boldsymbol1\)

第二题只联结其余属性的一个真子集。若 \(Q^\star\) 满足 A/B/C，则模型局部泛可识别。

论文只给出局部结论，因为证明需要在真参数邻域中排除额外分支，尚未建立整个参数空间的全局唯一性。

## 6. 零测集条件

Case (b) 的可识别参数要求存在两组其余属性配置，使

\[
p_{\boldsymbol\alpha^1}
p_{\boldsymbol\alpha^2+\boldsymbol e_1}
\ne
p_{\boldsymbol\alpha^2}
p_{\boldsymbol\alpha^1+\boldsymbol e_1}.
\]

等号定义不可识别代数集合。\(K=2\) 时退化为

\[
p_{00}p_{11}=p_{01}p_{10}.
\]

## 7. 如何使用 Theorem 2

```text
统计每列的 1
   │
   ├── 有列 ≤ 1：泛识别失败
   ├── 所有列 ≥ 3：转 Theorem 1
   └── 某列 = 2
          │
          ├── 重排成标准形，读取 v
          ├── v=1：局部泛识别失败
          ├── v=0：检查 (b.1)/(b.2)
          └── 其他 v：检查 Q* 的 A/B/C，得到局部结论
```
