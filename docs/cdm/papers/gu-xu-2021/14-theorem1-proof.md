# Theorem 1 的证明路线

## 1. 证明起点

假设两组对象给出相同反应分布：

\[
T(Q,\boldsymbol c,\boldsymbol g)\boldsymbol p
=
T(\bar Q,\bar{\boldsymbol c},\bar{\boldsymbol g})
\bar{\boldsymbol p}.
\]

将真 Q 的前 \(K\) 行按 Condition A 排成 \(I_K\)。目标是逐步证明替代模型只能等于真模型，允许列置换。

## 2. 充分性证明的五步

补充材料把主证明分成五步。

### Step 1：限制替代矩阵的前 \(K\) 行

利用 \(Q^\star\) 的列互异性构造属性次序，并通过归纳证明：

\[
\bar Q_{1:K,\cdot}
\]

经列置换后必须是对角线全 1 的上三角型。

关键思想是选择能区分某列与此前各列的 \(Q^\star\) 行，再用 T-matrix 平移制造零项。若候选行缺少应有的 1，会与严格单调关系 \(c_j>g_j\) 冲突。

### Step 2：识别非锚题的 \(c_j\)

对

\[
j=K+1,\ldots,J,
\]

选择包含题 \(j\) 和一组辅助题的响应矩。Condition C 保证每个属性还有足够题目参与乘积。比较平移后的 T-matrix 行可得

\[
\bar c_j=c_j.
\]

### Step 3：识别锚题的 \(g_k\)

对每个单位题 \(k\)，构造避开能力潜类的矩组合，利用 Step 1 的三角结构和 Step 2 已识别的参数消元，得到

\[
\bar g_k=g_k.
\]

### Step 4：把上三角型收紧为 \(I_K\)

若 \(\bar Q_{1:K,\cdot}\) 的某个非对角位置仍为 1，可选取两道真单位题并比较特定 T 行。已经识别的 \(g\) 和 \(c\) 会迫使矛盾。

因此

\[
\bar Q_{1:K,\cdot}\sim I_K.
\]

### Step 5：恢复剩余 Q、全部参数与比例

在两边前 \(K\) 行均对齐为 \(I_K\) 后，继续比较每道非锚题的理想反应列，得到

\[
\bar Q\sim Q.
\]

已知 Q 的 DINA 参数识别结果随后给出

\[
\bar{\boldsymbol c}=\boldsymbol c,\qquad
\bar{\boldsymbol g}=\boldsymbol g,\qquad
\bar{\boldsymbol p}=\boldsymbol p.
\]

## 3. 必要性的三条路线

### A 失败

存在等价潜类，比例可重新分配；部分场景还可构造另一张 \(\bar Q\)。

### B 失败

两个属性在 \(Q^\star\) 中列码相同，可构造参数补偿，使结构不唯一。

### C 失败

某属性只出现一题或两题。已知 Q 的 DINA 参数识别必要条件已经表明严格识别失败；Theorem 2 进一步刻画两题情形。

## 4. 证明技术的核心

这套证明没有直接套用通用三路张量唯一性。它利用 DINA 每题仅有 \(c_j,g_j\) 两个概率的特殊结构，通过：

\[
\text{T-matrix 平移}
+\text{零模式构造}
+\text{偏序归纳}
+\text{逐参数消元}
\]

把一套单位阵和列编码转化为全模型唯一性。
