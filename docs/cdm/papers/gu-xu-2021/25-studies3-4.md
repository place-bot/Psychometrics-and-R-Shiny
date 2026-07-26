# Experiment：DINA Studies III--IV

## Study III：连局部泛识别也失败

### 1. 三张真 Q

\[
Q^{10}=
\begin{pmatrix}
0&1\\
0&1\\
0&1\\
1&0\\
0&1
\end{pmatrix}
\]

第一列只出现 1 次。

\[
Q^{21}=
\begin{pmatrix}
0&1\\
1&1\\
0&1\\
1&1\\
0&1
\end{pmatrix}
\]

不完整，缺少 \((1,0)\) 单属性行。

\[
Q^{55}=
\begin{pmatrix}
0&1\\
0&1\\
0&1\\
0&1\\
1&1
\end{pmatrix}
\]

第一列的信息高度不足，相关结构不满足泛识别条件。

### 2. 结果

三个场景中，真 Q 均未取得最大对数似然，多个错误候选具有更高似然。Figure 6 把红色真 Q 与紫色最大似然候选明显分开。

### 3. 解读

有限样本 MLE 选择错误 Q 和理论失识别方向一致。理论陈述更强：真分布本身允许局部连续等价对象。

## Study IV：完整性的必要性

### 1. 场景

作者设置：

\[
(K,J)=(3,20)
\quad\text{与}\quad
(5,20).
\]

每个场景从不完整 Q 出发，构造两张替代矩阵 \(Q'\)、\(Q''\)，并调整潜类比例。

### 2. 构造逻辑

定义理想反应矩阵

\[
\Gamma_{j,\boldsymbol\alpha}(Q)
=
I(\boldsymbol\alpha\succeq\boldsymbol q_j).
\]

替代 Q 的 \(\Gamma\) 含有更多理想反应列。对替代模型中新出现、真模型中没有的列，把相应潜类比例设为 0；再把这些质量并入与真模型同列的潜类。

题目参数保持不变。

### 3. 全分布核验

对每个模型计算全部

\[
2^{20}=1,048,576
\]

个反应模式概率。

#### \(K=3\)

\[
\max_{\boldsymbol r}
|\Pr_Q(\boldsymbol R=\boldsymbol r)
-\Pr_{Q'}(\boldsymbol R=\boldsymbol r)|
=2.17\times10^{-19},
\]

\[
\max_{\boldsymbol r}
|\Pr_Q(\boldsymbol R=\boldsymbol r)
-\Pr_{Q''}(\boldsymbol R=\boldsymbol r)|
=4.34\times10^{-19}.
\]

#### \(K=5\)

对应最大差为

\[
2.17\times10^{-19}
\quad\text{和}\quad
6.51\times10^{-19}.
\]

### 4. 结果分析

这些误差低于 MATLAB 的双精度机器误差

\[
2.22\times10^{-16}.
\]

Study IV 给出显式观测等价构造，直接验证不完整 Q 无法联合识别。

### 5. 与主文假设的关系

构造中的替代潜类比例含 0，用于展示不同 Q 的观测等价。主文真模型假设全部 \(p_\alpha>0\)；必要性证明通过更一般的参数构造处理严格正参数空间。数值 Study 的角色是直观展示 \(\Gamma\) 列合并机制。
