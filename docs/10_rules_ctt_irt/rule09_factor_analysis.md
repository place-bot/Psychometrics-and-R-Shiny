# 规则9详解：二元项目的因素分析

规则对比

| CTT | IRT |
| --- | --- |
| 二元项目的因素分析产生假象而非因素 | 原始项目数据的因素分析产生完全信息因素分析 |

## 1. 二元项目因素分析的重要性

二元项目与因素分析

**为什么需要因素分析？**

因素分析是验证测验结构效度的核心方法，帮助我们理解：

- 测验是否真的测量了预期的构念
- 有多少个潜在维度
- 各个项目如何反映这些维度

**二元项目的普遍性**：

- **能力测验**：对/错、答对/答错
- **诊断量表**：是/否、有/无症状
- **行为观察**：出现/未出现
- **态度测验**：同意/不同意（二分化处理）

### 1.1 二元项目的特殊性质

**特殊性1：有限的变异范围**

二元项目只能取0或1，变异范围受到严格限制。

**特殊性2：非正态分布**

二元项目遵循伯努利分布：

\[
P(X = x) = p^x(1-p)^{1-x}, \quad x \in \{0,1\}
\]

**特殊性3：方差与均值的依赖关系**

\[
\text{Var}(X) = p(1-p)
\]

方差完全由均值决定，这导致了独特的统计性质。

**特殊性4：相关系数的限制**

两个二元项目间的相关系数受到边际分布的严重限制。

## 2. CTT中Phi相关的根本问题

### 2.1 Phi相关系数的推导

Phi相关系数

**联合分布表**：

设两个二元变量 \(X\) 和 \(Y\)，取值为0或1

|  | \(Y=1\) | \(Y=0\) | 总计 |
| --- | --- | --- | --- |
| \(X=1\) | \(p_{11}\) | \(p_{10}\) | \(p_1\) |
| \(X=0\) | \(p_{01}\) | \(p_{00}\) | \(1-p_1\) |
| 总计 | \(p_2\) | \(1-p_2\) | 1 |

**推导步骤**：

**步骤1：计算协方差**

\[
\text{Cov}(X,Y) = E[XY] - E[X]E[Y]
\]

由于：

\[
E[XY] = 1 \cdot 1 \cdot p_{11} + 1 \cdot 0 \cdot p_{10} + 0 \cdot 1 \cdot p_{01} + 0 \cdot 0 \cdot p_{00} = p_{11}
\]

\[
E[X] = p_1, \quad E[Y] = p_2
\]

因此：

\[
\text{Cov}(X,Y) = p_{11} - p_1 p_2
\]

**步骤2：计算标准差**

\[
\text{Var}(X) = p_1(1-p_1), \quad \sigma_X = \sqrt{p_1(1-p_1)}
\]

\[
\text{Var}(Y) = p_2(1-p_2), \quad \sigma_Y = \sqrt{p_2(1-p_2)}
\]

**步骤3：Phi相关公式**

\[
\phi = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y} = \frac{p_{11} - p_1 p_2}{\sqrt{p_1(1-p_1)p_2(1-p_2)}}
\]

### 2.2 Phi相关上界的推导

**问题**：求 \(\phi\) 的最大可能值

**约束条件**：

\[
\begin{align}
p_{11} + p_{10} &= p_1 \
p_{11} + p_{01} &= p_2 \
p_{11}, p_{10}, p_{01}, p_{00} &\geq 0 \
p_{11} + p_{10} + p_{01} + p_{00} &= 1
\end{align}
\]

**最大化 \(p_{11}\)**：

由约束条件：

\[
p_{11} \leq \min(p_1, p_2)
\]

当 \(p_{11} = \min(p_1, p_2)\) 时，\(\phi\) 达到最大值。

**情况1**：\(p_1 \leq p_2\)

\[
p_{11,\max} = p_1
\]

\[
\phi_{\max} = \frac{p_1 - p_1p_2}{\sqrt{p_1(1-p_1)p_2(1-p_2)}} = \frac{p_1(1-p_2)}{\sqrt{p_1(1-p_1)p_2(1-p_2)}}
\]

\[
= \sqrt{\frac{p_1(1-p_2)}{(1-p_1)p_2}}
\]

**一般公式**：

\[
\phi_{\max} = \sqrt{\frac{\min(p_1, p_2) \cdot \min(1-p_1, 1-p_2)}{\max(p_1, p_2) \cdot \max(1-p_1, 1-p_2)}}
\]

### 2.3 难度因素的产生机制

假设有4个项目，真实的因素结构是：

- 项目1和2：测量因素A，难度分别为0.2和0.8
- 项目3和4：测量因素B，难度分别为0.2和0.8

**理想的相关矩阵**（如果没有难度效应）：

\[
R_{\text{理想}} = \begin{pmatrix}
1 & 0.8 & 0 & 0 \
0.8 & 1 & 0 & 0 \
0 & 0 & 1 & 0.8 \
0 & 0 & 0.8 & 1
\end{pmatrix}
\]

**实际的Phi相关矩阵**：

由于难度限制，相关被压缩。根据前面的公式，当 \(p_1 = 0.2, p_2 = 0.8\) 时：

\[
\phi_{\max} = \sqrt{\frac{0.2 \times 0.2}{0.8 \times 0.8}} = 0.25
\]

因此，即使真实相关为0.8，观察到的相关最多只能是 \(0.8 \times 0.25 = 0.2\)。

## 3. 四分相关的改进尝试

### 3.1 四分相关的理论基础

四分相关（Tetrachoric Correlation）

**核心假设**：每个二元项目背后都有一个潜在的连续正态变量

**模型**：
设潜在变量 \(Z_1 \sim N(0,1)\) 和 \(Z_2 \sim N(0,1)\)，阈值为 \(\tau_1\) 和 \(\tau_2\)：

\[
X = \begin{cases}
1 & \text{如果} Z_1 > \tau_1 \
0 & \text{如果} Z_1 \leq \tau_1
\end{cases}
\]

\[
Y = \begin{cases}
1 & \text{如果} Z_2 > \tau_2 \
0 & \text{如果} Z_2 \leq \tau_2
\end{cases}
\]

**目标**：估计 \(\rho = \text{Cor}(Z_1, Z_2)\)

### 3.2 四分相关的计算

**步骤1：从边际概率推断阈值**

\[
p_1 = P(X=1) = P(Z_1 > \tau_1) = 1 - \Phi(\tau_1)
\]

因此：

\[
\tau_1 = \Phi^{-1}(1-p_1) = -\Phi^{-1}(p_1)
\]

同理：

\[
\tau_2 = -\Phi^{-1}(p_2)
\]

**步骤2：利用联合概率**

\[
p_{11} = P(X=1, Y=1) = P(Z_1 > \tau_1, Z_2 > \tau_2)
\]

这是一个双变量正态分布的积分：

\[
p_{11} = \int_{\tau_1}^{\infty} \int_{\tau_2}^{\infty} \frac{1}{2\pi\sqrt{1-\rho^2}} \exp\left(-\frac{z_1^2 - 2\rho z_1 z_2 + z_2^2}{2(1-\rho^2)}\right) dz_2 dz_1
\]

**步骤3：数值求解**

定义函数：

\[
L(\rho, \tau_1, \tau_2) = \int_{\tau_1}^{\infty} \int_{\tau_2}^{\infty} \phi_2(z_1, z_2; \rho) dz_2 dz_1
\]

需要解方程：

\[
L(\rho, \tau_1, \tau_2) = p_{11}
\]

### 3.3 四分相关的问题分析

**问题1：计算不稳定性**

当 \(p\) 接近0或1时，阈值趋向无穷：

\[
\lim_{p \to 0} \Phi^{-1}(p) = -\infty, \quad \lim_{p \to 1} \Phi^{-1}(p) = +\infty
\]

这导致数值积分极不稳定。

**问题2：非正定矩阵问题**

考虑3个项目的情况，即使每对项目的四分相关都合理，整个矩阵可能非正定。

**例子**：

\[
R = \begin{pmatrix}
1 & 0.9 & 0.9 \
0.9 & 1 & -0.8 \
0.9 & -0.8 & 1
\end{pmatrix}
\]

计算特征值：

\[
\det(R - \lambda I) = 0
\]

得到：\(\lambda_1 = 2.62\), \(\lambda_2 = 0.38\), \(\lambda_3 = -0.00\)

负特征值使得因素分析无法进行。

## 4. IRT中全信息因素分析

### 4.1 多维IRT模型

全信息因素分析（Full Information Factor Analysis, FIFA）

**核心思想**：直接对原始反应数据建模，不需要计算相关矩阵

**二维2参数逻辑模型（M2PL）**：

\[
P_i(\mathbf{\theta}) = \frac{\exp(\mathbf{a}_i' \mathbf{\theta} + d_i)}{1 + \exp(\mathbf{a}_i' \mathbf{\theta} + d_i)}
\]

其中：
- \(\mathbf{\theta} = (\theta_1, \theta_2, \ldots, \theta_m)'\)：个体在 \(m\) 个因素上的得分向量
- \(\mathbf{a}_i = (a_{i1}, a_{i2}, \ldots, a_{im})'\)：项目 \(i\) 在各因素上的载荷向量
- \(d_i\)：项目 \(i\) 的截距参数

### 4.2 线性化表示

对数几率形式：

\[
\text{logit}(P_i(\mathbf{\theta})) = \ln\left(\frac{P_i(\mathbf{\theta})}{1-P_i(\mathbf{\theta})}\right) = \mathbf{a}_i' \mathbf{\theta} + d_i
\]

展开为：

\[
\text{logit}(P_i(\mathbf{\theta})) = \sum_{k=1}^m a_{ik} \theta_k + d_i
\]

这是 \(\mathbf{\theta}\) 的线性函数，类似于线性因素分析。

### 4.3 参数估计：边际最大似然

**个体似然**：

对于个体 \(j\) 的反应向量 \(\mathbf{u}_j = (u_{1j}, u_{2j}, \ldots, u_{Ij})'\)：

\[
L_j(\mathbf{\theta}) = \prod_{i=1}^I P_i(\mathbf{\theta})^{u_{ij}} [1-P_i(\mathbf{\theta})]^{1-u_{ij}}
\]

**边际似然**：

\[
L_j = \int L_j(\mathbf{\theta}) g(\mathbf{\theta}) d\mathbf{\theta}
\]

其中 \(g(\mathbf{\theta})\) 通常假设为多元正态分布：

\[
g(\mathbf{\theta}) = \frac{1}{(2\pi)^{m/2}|\mathbf{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}\mathbf{\theta}'\mathbf{\Sigma}^{-1}\mathbf{\theta}\right)
\]

**对数似然**：

\[
\ln L = \sum_{j=1}^J \ln L_j = \sum_{j=1}^J \ln \left[\int L_j(\mathbf{\theta}) g(\mathbf{\theta}) d\mathbf{\theta}\right]
\]

### 4.4 EM算法详细推导

**E步（期望步）**：

计算完全数据对数似然的期望：

\[
Q(\mathbf{\Psi}|\mathbf{\Psi}^{(t)}) = \sum_{j=1}^J \int \ln[L_j(\mathbf{\theta})g(\mathbf{\theta})] h_j(\mathbf{\theta}|\mathbf{\Psi}^{(t)}) d\mathbf{\theta}
\]

其中后验分布：

\[
h_j(\mathbf{\theta}|\mathbf{\Psi}^{(t)}) = \frac{L_j(\mathbf{\theta}|\mathbf{\Psi}^{(t)}) g(\mathbf{\theta})}{\int L_j(\mathbf{\theta}|\mathbf{\Psi}^{(t)}) g(\mathbf{\theta}) d\mathbf{\theta}}
\]

计算后验矩：

\[
\mathbf{\mu}_j = E[\mathbf{\theta}_j|\mathbf{u}_j] = \int \mathbf{\theta} h_j(\mathbf{\theta}) d\mathbf{\theta}
\]

\[
\mathbf{\Sigma}_j = E[\mathbf{\theta}_j\mathbf{\theta}_j'|\mathbf{u}_j] = \int \mathbf{\theta}\mathbf{\theta}' h_j(\mathbf{\theta}) d\mathbf{\theta}
\]

**M步（最大化步）**：

对于项目 \(i\)，最大化：

\[
Q_i = \sum_{j=1}^J E_{\mathbf{\theta}_j|\mathbf{u}_j}\left[u_{ij} \ln P_i(\mathbf{\theta}_j) + (1-u_{ij}) \ln(1-P_i(\mathbf{\theta}_j))\right]
\]

使用Newton-Raphson：

梯度：

\[
\frac{\partial Q_i}{\partial a_{ik}} = \sum_{j=1}^J E\left[\theta_{kj}(u_{ij} - P_i(\mathbf{\theta}_j))\right]
\]

Hessian矩阵：

\[
\frac{\partial^2 Q_i}{\partial a_{ik} \partial a_{il}} = -\sum_{j=1}^J E\left[\theta_{kj}\theta_{lj}P_i(\mathbf{\theta}_j)(1-P_i(\mathbf{\theta}_j))\right]
\]

### 4.5 信息函数与测量精度

**项目信息函数**：

\[
I_i(\mathbf{\theta}) = \frac{[\nabla P_i(\mathbf{\theta})][\nabla P_i(\mathbf{\theta})]'}{P_i(\mathbf{\theta})[1-P_i(\mathbf{\theta})]}
\]

其中：

\[
\nabla P_i(\mathbf{\theta}) = \frac{\partial P_i(\mathbf{\theta})}{\partial \mathbf{\theta}} = P_i(\mathbf{\theta})[1-P_i(\mathbf{\theta})]\mathbf{a}_i
\]

因此：

\[
I_i(\mathbf{\theta}) = P_i(\mathbf{\theta})[1-P_i(\mathbf{\theta})]\mathbf{a}_i\mathbf{a}_i'
\]

**总信息矩阵**：

\[
\mathbf{I}(\mathbf{\theta}) = \sum_{i=1}^I I_i(\mathbf{\theta}) = \sum_{i=1}^I P_i(\mathbf{\theta})[1-P_i(\mathbf{\theta})]\mathbf{a}_i\mathbf{a}_i'
\]

**标准误矩阵**：

\[
\text{SE}(\hat{\mathbf{\theta}}) = \mathbf{I}(\mathbf{\theta})^{-1/2}
\]

## 5. 模型选择与应用

### 5.1 因素数量的确定

**信息准则**：

\[
\text{AIC} = -2\ln L + 2p
\]

\[
\text{BIC} = -2\ln L + p\ln N
\]

其中 \(p\) 是参数数量：

\[
p = I \times (m + 1) + \frac{m(m-1)}{2}
\]

- \(I \times m\)：载荷参数
- \(I\)：截距参数
- \(\frac{m(m-1)}{2}\)：因素相关参数

### 5.2 实际应用示例

**载荷矩阵的解释**：

\[
\text{总区分度} = ||\mathbf{a}_i|| = \sqrt{\sum_{k=1}^m a_{ik}^2}
\]

**因素贡献比例**：

\[
\text{贡献}_{ik} = \frac{a_{ik}^2}{\sum_{l=1}^m a_{il}^2}
\]

**共同度**：

\[
h_i^2 = \frac{\sum_{k=1}^m a_{ik}^2}{1 + \sum_{k=1}^m a_{ik}^2}
\]

实践建议

**数据准备**

- 检查数据质量（缺失值、异常反应）
- 编码二元反应为0/1
- 检查项目的基本统计量

**模型拟合**

- 从单因素模型开始
- 逐步增加因素数量
- 比较不同模型的拟合指标

**结果解释**

- 分析载荷模式
- 计算因素相关
- 评估项目质量
