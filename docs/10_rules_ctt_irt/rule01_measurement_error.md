# 规则1：测量标准误

规则对比

| CTT | IRT |
| --- | --- |
| 测量误差的标准误适用于特定群体内的所有得分 | 测量误差的标准误随得分变化，但可推广至多个群体 |

## 1. CTT 标准误推导

### 1.1 基本模型

CTT 基本假设

\[X = T + E\]

- \(X\) = 观察分数
- \(T\) = 真分数
- \(E\) = 测量误差

**三个核心假设**：
1. \(E(E) = 0\)
2. \(\rho(T,E) = 0\)
3. \(\rho(E_1,E_2) = 0\)

### 1.2 标准误公式推导

**步骤1：方差分解**

\[\sigma_X^2 = \text{Var}(X) = \text{Var}(T + E) = \sigma_T^2 + \sigma_E^2 + 2\text{Cov}(T,E)\]

由于 \(\text{Cov}(T,E) = 0\)：

\[\sigma_X^2 = \sigma_T^2 + \sigma_E^2\]

**步骤2：信度定义**

\[r_{tt} = \frac{\sigma_T^2}{\sigma_X^2} = \frac{\sigma_T^2}{\sigma_T^2 + \sigma_E^2}\]

**步骤3：求解误差方差**

\[\sigma_E^2 = \sigma_X^2 - \sigma_T^2 = \sigma_X^2\left(1 - \frac{\sigma_T^2}{\sigma_X^2}\right) = \sigma_X^2(1 - r_{tt})\]

CTT 标准误公式

\[SE_{\text{msmt}} = \sigma_E = \sigma_X\sqrt{1 - r_{tt}}\]

**特点**：对所有被试都相同，不区分能力水平

### 1.3 数值例子

给定：\(\sigma = 15\)，\(r_{tt} = 0.84\)

\[SE_{\text{msmt}} = 15\sqrt{1 - 0.84} = 15\sqrt{0.16} = 15 \times 0.4 = 6\]

**含义**：无论考80分还是40分，测量误差都是6分。

## 2. IRT 标准误推导

### 2.1 信息函数

核心概念：信息函数

\[SE(\theta) = \frac{1}{\sqrt{I(\theta)}}\]

标准误与信息函数成反比关系

### 2.2 信息函数推导（Rasch模型）

**步骤1：对数似然函数**

对于单个项目的反应 \(u_i \in \{0,1\}\)：

\[\ln L_i = u_i \ln P_i(\theta) + (1-u_i) \ln(1-P_i(\theta))\]

其中：

\[P_i(\theta) = \frac{e^{\theta - b_i}}{1 + e^{\theta - b_i}}\]

**步骤2：一阶导数**

\[\frac{\partial \ln L_i}{\partial \theta} = u_i - P_i(\theta)\]

**步骤3：二阶导数**

\[\frac{\partial^2 \ln L_i}{\partial \theta^2} = -P_i(\theta)[1-P_i(\theta)]\]

**步骤4：Fisher信息**

项目信息函数

\[I_i(\theta) = -E\left[\frac{\partial^2 \ln L_i}{\partial \theta^2}\right] = P_i(\theta)[1-P_i(\theta)]\]

**最大信息点**：当 \(P_i(\theta) = 0.5\) 时，\(I_i(\theta) = 0.25\)

### 2.3 信息函数性质分析

| \(P_i(\theta)\) | \(I_i(\theta)\) | 测量精度 |
| --- | --- | --- |
| 0.5 | 0.25 | 最高 |
| 0.9 | 0.09 | 较低 |
| 0.1 | 0.09 | 较低 |
| 0.99 | 0.0099 | 很低 |

**核心洞察**：当题目难度与能力匹配（\(\theta = b_i\)）时，测量最精确。

## 3. IRT 复合信度

### 3.1 平均标准误的平方

\[\sigma_\theta^2 = \frac{1}{N}\sum_{j=1}^N [SE(\theta_j)]^2 = \frac{1}{N}\sum_{j=1}^N \frac{1}{I(\theta_j)}\]

### 3.2 特质方差

\[\sigma^2 = \frac{1}{N}\sum_{j=1}^N (\theta_j - \bar{\theta})^2\]

### 3.3 复合信度公式

IRT 复合信度

\[r'_{tt} = 1 - \frac{\sigma_\theta^2}{\sigma^2}\]

**解释**：

- \(\sigma^2\) = 总变异（被试间能力差异）
- \(\sigma_\theta^2\) = 测量误差导致的变异
- \(r'_{tt}\) = 能够解释的真实能力变异比例

### 3.4 数值计算示例

设5个被试：\(\theta = [-2, -1, 0, 1, 2]\)，信息函数：\(I(\theta) = [1.0, 1.2, 1.5, 1.2, 1.0]\)

**计算 \(\sigma_\theta^2\)**：

| \(\theta_j\) | \(I(\theta_j)\) | \(SE(\theta_j)\) | \([SE(\theta_j)]^2\) |
| --- | --- | --- | --- |
| -2 | 1.0 | 1.000 | 1.000 |
| -1 | 1.2 | 0.913 | 0.834 |
| 0 | 1.5 | 0.816 | 0.666 |
| 1 | 1.2 | 0.913 | 0.834 |
| 2 | 1.0 | 1.000 | 1.000 |

\[\sigma_\theta^2 = \frac{1}{5}(1.000 + 0.834 + 0.666 + 0.834 + 1.000) = 0.867\]

**计算 \(\sigma^2\)**：

\[\bar{\theta} = 0, \quad \sigma^2 = \frac{1}{5}(4 + 1 + 0 + 1 + 4) = 2\]

**复合信度**：

\[r'_{tt} = 1 - \frac{0.867}{2} = 0.567\]

## 4. CTT vs IRT 对比总结

关键差异

**CTT 局限性**：

- 单一标准误，忽视能力差异
- 依赖特定样本
- 无法区分不同能力水平的测量精度

**IRT 优势**：

- 个体化标准误
- 样本无关
- 精确定位最佳测量区间
