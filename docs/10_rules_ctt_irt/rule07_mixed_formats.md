# 规则7详解：混合项目格式

规则对比

| CTT | IRT |
| --- | --- |
| 混合项目格式导致测验总分的不平衡影响 | 混合项目格式可以产生最优测验得分 |

## 1. 项目格式的定义与类型

项目格式（Item Format）

题目的反应方式和评分标准

**常见格式**：

**二分类项目**：

- 例子：对/错、是/否题
- 评分：0分（错误）或1分（正确）
- 优点：客观、容易评分
- 缺点：信息量有限

**多选择项目**：

- 例子：ABCD四选一
- 评分：0分（答错）或1分（答对）
- 优点：减少猜测概率
- 缺点：仍然是二分信息

**Likert量表项目**：

- 例子：1-5分或1-7分评价
- 评分：连续的等级分数
- 优点：能捕捉程度差异
- 缺点：主观性较强

**开放式题目**：

- 例子：作文、解答题
- 评分：0-10分或更复杂的评分标准
- 优点：信息丰富、真实性高
- 缺点：评分主观、成本高

## 2. 为什么需要混合格式？

### 2.1 测量需求的多样性

设测量的特质为 \(\theta\)，如果只用一种格式，信息函数为：

\[
I_{\text{单一}}(\theta) = \sum_{i=1}^n I_i(\theta)
\]

如果用混合格式，信息函数为：

\[
I_{\text{混合}}(\theta) = \sum_{i=1}^{n_1} I_{i,\text{格式1}}(\theta) + \sum_{j=1}^{n_2} I_{j,\text{格式2}}(\theta) + \cdots
\]

理论上，\(I_{\text{混合}}(\theta)\) 可以在更广的 \(\theta\) 范围内提供更高的信息。

### 2.2 信息互补原理

对于二分类项目，信息函数为：

\[
I_{\text{二分}}(\theta) = P(\theta)[1-P(\theta)]
\]

最大值点：

\[
\frac{dI}{d\theta} = \frac{dP}{d\theta}[1-2P(\theta)] = 0
\]

得 \(P(\theta) = 0.5\)，最大值为 \(I_{\max} = 0.25\)

对于多分类项目（如5分制Likert），信息函数为：

\[
I_{\text{多分}}(\theta) = \sum_{k=0}^4 P_k(\theta)\left[\frac{\partial \ln P_k(\theta)}{\partial \theta}\right]^2
\]

展开对数导数：

\[
\frac{\partial \ln P_k(\theta)}{\partial \theta} = \frac{1}{P_k(\theta)} \frac{\partial P_k(\theta)}{\partial \theta}
\]

这个函数可能在多个 \(\theta\) 值处有局部最大值。

## 3. CTT中混合格式的根本问题

### 3.1 隐含权重的完整推导

CTT权重问题

CTT中总分 \(X_{\text{total}} = \sum_{i=1}^I X_i\) 看似等权重，实则不然

**方差分解**：

\[
\text{Var}(X_{\text{total}}) = \text{Var}\left(\sum_{i=1}^I X_i\right)
\]

展开得：

\[
\text{Var}(X_{\text{total}}) = \sum_{i=1}^I \text{Var}(X_i) + 2\sum_{i<j} \text{Cov}(X_i, X_j)
\]

改写为双重求和：

\[
\text{Var}(X_{\text{total}}) = \sum_{i=1}^I \sum_{j=1}^I \text{Cov}(X_i, X_j)
\]

**项目贡献的定义**：

项目 \(i\) 对总分方差的贡献为其在协方差矩阵中对应行（或列）的和：

\[
\text{贡献}_i = \sum_{j=1}^I \text{Cov}(X_i, X_j) = \text{Cov}\left(X_i, \sum_{j=1}^I X_j\right) = \text{Cov}(X_i, X_{\text{total}})
\]

**验证权重和为1**：

\[
\sum_{i=1}^I \text{贡献}_i = \sum_{i=1}^I \text{Cov}(X_i, X_{\text{total}}) = \text{Cov}\left(\sum_{i=1}^I X_i, X_{\text{total}}\right) = \text{Var}(X_{\text{total}})
\]

**实际权重公式**：

\[
w_{\text{实际},i} = \frac{\text{Cov}(X_i, X_{\text{total}})}{\text{Var}(X_{\text{total}})}
\]

利用相关系数定义：

\[
\text{Cov}(X_i, X_{\text{total}}) = r_{i,\text{total}} \cdot \sigma_i \cdot \sigma_{\text{total}}
\]

代入得：

\[
w_{\text{实际},i} = \frac{r_{i,\text{total}} \cdot \sigma_i \cdot \sigma_{\text{total}}}{\sigma_{\text{total}}^2} = \frac{r_{i,\text{total}} \cdot \sigma_i}{\sigma_{\text{total}}}
\]

### 3.2 能量唤醒量表实例分析

设原始第10项得分为 \(Y\)，分数范围1-4，修改后为 \(2Y\)，分数范围2-8。

**均值变化**：

\[
E[X_{\text{修改}}] = E[X_{\text{原始}} - Y + 2Y] = E[X_{\text{原始}}] + E[Y]
\]

如果 \(E[Y] = 2.29\)，则：

\[
E[X_{\text{修改}}] = 22.33 + 2.29 = 24.62
\]

**方差变化**：

\[
\text{Var}(X_{\text{修改}}) = \text{Var}(X_{\text{原始}} - Y + 2Y) = \text{Var}(X_{\text{原始}} + Y)
\]

由于 \(Y\) 包含在 \(X_{\text{原始}}\) 中：

\[
\text{Var}(X_{\text{原始}} + Y) = \text{Var}(X_{\text{原始}}) + \text{Var}(Y) + 2\text{Cov}(X_{\text{原始}} - Y, Y)
\]

设 \(S = X_{\text{原始}} - Y\)（前9项之和），则：

\[
\text{Cov}(S, Y) = \text{Cov}(X_{\text{原始}} - Y, Y) = \text{Cov}(X_{\text{原始}}, Y) - \text{Var}(Y)
\]

### 3.3 个体差异的定量分析

对于原始总分相同的两个个体 A 和 B：

\[
X_{\text{原始},A} = X_{\text{原始},B} = 30
\]

但反应模式不同：

- A: 前9项得27分，第10项得3分
- B: 前9项得29分，第10项得1分

修改后的差异：

\[
\Delta = X_{\text{修改},A} - X_{\text{修改},B} = (27 + 6) - (29 + 2) = 2
\]

一般化：如果第 \(i\) 项得分差异为 \(\delta_i\)，类别数乘数为 \(m\)，则：

\[
\Delta_{\text{总分}} = \delta_i \times (m-1)
\]

## 4. CTT处理混合格式的传统方法

### 4.1 标准化处理

标准化方法的问题

将每个项目转换为标准分数：

\[
Z_{ij} = \frac{X_{ij} - \mu_i}{\sigma_i}
\]

**问题1：样本依赖性**

在样本1中：

\[
Z_i^{(1)} = \frac{X_i - \mu_i^{(1)}}{\sigma_i^{(1)}}
\]

在样本2中：

\[
Z_i^{(2)} = \frac{X_i - \mu_i^{(2)}}{\sigma_i^{(2)}}
\]

一般情况下，\(Z_i^{(1)} \neq Z_i^{(2)}\)

**问题2：相关结构的改变**

原始协方差：

\[
\text{Cov}(X_i, X_j) = E[(X_i - \mu_i)(X_j - \mu_j)]
\]

标准化后协方差：

\[
\text{Cov}(Z_i, Z_j) = E\left[\frac{(X_i - \mu_i)}{\sigma_i} \cdot \frac{(X_j - \mu_j)}{\sigma_j}\right] = \frac{\text{Cov}(X_i, X_j)}{\sigma_i \sigma_j} = r_{ij}
\]

### 4.2 除以常数方法

设原始最大分数为 \(M_i\)，标准化到共同最大分数 \(M\)：

\[
X_i' = \frac{M}{M_i} \cdot X_i
\]

**反应函数的非线性**：

假设个体的真实态度为 \(\theta\)，反应函数：

- 4分制：\(f_4(\theta)\)
- 8分制：\(f_8(\theta)\)

线性假设要求：

\[
f_8(\theta) = 2 \cdot f_4(\theta)
\]

但实际上这个关系通常不成立。

## 5. IRT中混合格式的解决方案

### 5.1 广义部分信用模型（GPCM）

GPCM模型

\[
P_{ik}(\theta) = \frac{\exp\left[\sum_{j=0}^k a_i(\theta - b_{ij})\right]}{\sum_{h=0}^{m_i} \exp\left[\sum_{j=0}^h a_i(\theta - b_{ij})\right]}
\]

其中：
- \(P_{ik}(\theta)\)：能力为 \(\theta\) 的个体在项目 \(i\) 上选择类别 \(k\) 的概率
- \(a_i\)：项目 \(i\) 的区分度参数
- \(b_{ij}\)：项目 \(i\) 的第 \(j\) 个阈值参数
- \(m_i\)：项目 \(i\) 的最高类别编号

**累积概率函数**：

定义累积函数：

\[
\Psi_{ik}(\theta) = \sum_{j=0}^k a_i(\theta - b_{ij})
\]

则：

\[
P_{ik}(\theta) = \frac{\exp[\Psi_{ik}(\theta)]}{\sum_{h=0}^{m_i} \exp[\Psi_{ih}(\theta)]}
\]

**边际概率的推导**：

对于二分类的特殊情况（\(m_i = 1\)）：

\[
P_{i1}(\theta) = \frac{\exp[a_i(\theta - b_{i1})]}{\exp(0) + \exp[a_i(\theta - b_{i1})]} = \frac{1}{1 + \exp[-a_i(\theta - b_{i1})]}
\]

这正是2PL模型。

### 5.2 阈值参数的性质

阈值定义

阈值 \(b_{ij}\) 是相邻类别概率相等的能力点：

\[
P_{i,j-1}(b_{ij}) = P_{ij}(b_{ij})
\]

**阈值方程的推导**：

在 \(\theta = b_{ij}\) 处：

\[
\frac{\exp[\Psi_{i,j-1}(b_{ij})]}{\sum_h \exp[\Psi_{ih}(b_{ij})]} = \frac{\exp[\Psi_{ij}(b_{ij})]}{\sum_h \exp[\Psi_{ih}(b_{ij})]}
\]

简化得：

\[
\exp[\Psi_{i,j-1}(b_{ij})] = \exp[\Psi_{ij}(b_{ij})]
\]

\[
\Psi_{i,j-1}(b_{ij}) = \Psi_{ij}(b_{ij})
\]

这是不可能的，因为 \(\Psi_{ij} > \Psi_{i,j-1}\)。

**正确的阈值定义**：

阈值实际上是累积概率函数的交叉点，需要通过数值方法求解。

### 5.3 信息函数的完整推导

**期望得分**：

\[
E[X_i|\theta] = \sum_{k=0}^{m_i} k \cdot P_{ik}(\theta)
\]

**得分函数（一阶导数）**：

\[
\frac{\partial E[X_i|\theta]}{\partial \theta} = \sum_{k=0}^{m_i} k \cdot \frac{\partial P_{ik}(\theta)}{\partial \theta}
\]

利用多项式logit模型的导数公式：

\[
\frac{\partial P_{ik}(\theta)}{\partial \theta} = a_i P_{ik}(\theta) \left[k - E[X_i|\theta]\right]
\]

代入得：

\[
\frac{\partial E[X_i|\theta]}{\partial \theta} = a_i \sum_{k=0}^{m_i} k \cdot P_{ik}(\theta) \left[k - E[X_i|\theta]\right]
\]

\[
= a_i \left[\sum_{k=0}^{m_i} k^2 P_{ik}(\theta) - E[X_i|\theta]^2\right]
\]

\[
= a_i \cdot \text{Var}[X_i|\theta]
\]

**信息函数（二阶导数的负值）**：

\[
I_i(\theta) = -\frac{\partial^2 \ln L}{\partial \theta^2} = \left[\frac{\partial E[X_i|\theta]}{\partial \theta}\right]^2 \cdot \frac{1}{\text{Var}[X_i|\theta]}
\]

代入得：

\[
I_i(\theta) = a_i^2 \cdot \text{Var}[X_i|\theta]
\]

### 5.4 混合格式的最优组合

**总信息函数**：

\[
I_{\text{total}}(\theta) = \sum_{i=1}^I I_i(\theta) = \sum_{i=1}^I a_i^2 \cdot \text{Var}[X_i|\theta]
\]

**优化目标**：

选择项目集合 \(S\) 和参数 \(\{a_i, b_{ij}\}\) 使得：

\[
\min_{\theta \in [\theta_{\min}, \theta_{\max}]} I_{\text{total}}(\theta) \geq I_{\text{target}}
\]

这保证了在目标能力范围内都有足够的测量精度。

## 6. 实践应用指导

混合格式设计原则

**测量目标导向**：

- 确定每个项目要测量的能力范围
- 选择最适合该范围的项目格式

**信息函数互补**：

- 分析不同格式的信息函数形状
- 确保总信息函数覆盖目标能力范围

**阈值合理性验证**：

- 检查阈值的单调性：\(b_{i1} < b_{i2} < \cdots < b_{i,m_i}\)
- 分析阈值间距：\(\Delta_{ij} = b_{i,j+1} - b_{ij}\)

**区分度平衡**：

- 监控区分度分布：\(\text{CV}(a) = \frac{\sigma_a}{\mu_a}\)
- 必要时调整项目权重

**具体操作步骤**：

预测每种格式的信息贡献：

\[
I_{\text{格式}}(\theta) = \sum_{i \in \text{格式}} I_i(\theta)
\]

计算测量误差：

\[
\text{SE}(\theta) = \frac{1}{\sqrt{I_{\text{total}}(\theta)}}
\]

评估可靠性：

\[
\rho(\theta) = \frac{I_{\text{total}}(\theta)}{I_{\text{total}}(\theta) + 1}
\]
