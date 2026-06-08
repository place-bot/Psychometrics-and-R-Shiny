# 规则4详解：项目属性的无偏估计

规则对比

| CTT | IRT |
| --- | --- |
| 只有在具有代表性样本的情况下，才能对项目属性进行无偏估计 | 即使样本不具代表性，也可以对项目属性进行无偏估计 |

## 1. 项目属性定义

项目属性（Item Properties）

测验中单个题目的统计特征，主要包括：

- **难度**：题目的通过率或位置参数
- **区分度**：题目区分不同能力水平的能力
- **猜测参数**：随机猜对的概率（仅在某些模型中）

## 2. CTT框架下的项目属性

### 2.1 难度指标

CTT项目难度

\[
p_i = \frac{\sum_{j=1}^n u_{ij}}{n}
\]

其中 \(u_{ij} \in \{0,1\}\) 表示被试 \(j\) 在项目 \(i\) 上的反应

### 2.2 区分度指标

点双列相关系数

\[
r_{pb} = \frac{(\bar{X}_1 - \bar{X}_0)\sqrt{p(1-p)}}{\sigma_X}
\]

推导：设 \(u \in \{0,1\}\) 为二值变量，\(X\) 为连续变量（总分）。

协方差：

\[
\operatorname{Cov}(u, X) = \mathbb{E}[uX] - \mathbb{E}[u]\mathbb{E}[X]
\]

由于：

\[
\mathbb{E}[uX] = P(u=1) \cdot \mathbb{E}[X|u=1] = p\bar{X}_1
\]

\[
\mathbb{E}[X] = p\bar{X}_1 + (1-p)\bar{X}_0
\]

代入得：

\[
\operatorname{Cov}(u, X) = p\bar{X}_1 - p[p\bar{X}_1 + (1-p)\bar{X}_0] = p(1-p)(\bar{X}_1 - \bar{X}_0)
\]

标准差：

\[
\sigma_u = \sqrt{\operatorname{Var}(u)} = \sqrt{p(1-p)}
\]

因此：

\[
r_{pb} = \frac{\operatorname{Cov}(u, X)}{\sigma_u \sigma_X} = \frac{p(1-p)(\bar{X}_1 - \bar{X}_0)}{\sqrt{p(1-p)} \cdot \sigma_X} = \frac{(\bar{X}_1 - \bar{X}_0)\sqrt{p(1-p)}}{\sigma_X}
\]

### 2.3 样本依赖性的本质

设项目 \(i\) 的真实反应函数为 \(P_i(\theta)\)，样本能力分布为 \(g(\theta)\)，则：

\[
p_i = \int_{-\infty}^{\infty} P_i(\theta) g(\theta) d\theta = \mathbb{E}_{\theta \sim g}[P_i(\theta)]
\]

不同样本有不同的 \(g(\theta)\)：

- 高能力样本：\(g_H(\theta) = \mathcal{N}(\mu_H, \sigma^2)\)，\(\mu_H > 0\)
- 低能力样本：\(g_L(\theta) = \mathcal{N}(\mu_L, \sigma^2)\)，\(\mu_L < 0\)

即使对同一题目，\(p_{i,H} \neq p_{i,L}\)。

## 3. IRT框架下的项目属性

### 3.1 Rasch模型

Rasch模型定义

\[
P(u_{ij} = 1 | \theta_j, b_i) = \frac{\exp(\theta_j - b_i)}{1 + \exp(\theta_j - b_i)}
\]

- \(\theta_j\)：被试 \(j\) 的能力参数
- \(b_i\)：项目 \(i\) 的难度参数

### 3.2 充分统计量

定理

在Rasch模型中，总分 \(r_j = \sum_{i=1}^I u_{ij}\) 是 \(\theta_j\) 的充分统计量。

**证明**：

反应向量 \(\mathbf{u}_j = (u_{1j}, ..., u_{Ij})\) 的似然函数：

\[
L(\mathbf{u}_j | \theta_j, \mathbf{b}) = \prod_{i=1}^I \left(\frac{e^{\theta_j - b_i}}{1 + e^{\theta_j - b_i}}\right)^{u_{ij}} \left(\frac{1}{1 + e^{\theta_j - b_i}}\right)^{1-u_{ij}}
\]

\[
= \prod_{i=1}^I \frac{e^{u_{ij}(\theta_j - b_i)}}{1 + e^{\theta_j - b_i}}
\]

\[
= \frac{\exp\left(\sum_{i=1}^I u_{ij}(\theta_j - b_i)\right)}{\prod_{i=1}^I (1 + e^{\theta_j - b_i})}
\]

\[
= \frac{\exp\left(\theta_j r_j - \sum_{i=1}^I u_{ij} b_i\right)}{\prod_{i=1}^I (1 + e^{\theta_j - b_i})}
\]

分解为：

\[
L(\mathbf{u}_j | \theta_j, \mathbf{b}) = \underbrace{\frac{\exp(\theta_j r_j)}{\prod_{i=1}^I (1 + e^{\theta_j - b_i})}}_{g(r_j, \theta_j)} \cdot \underbrace{\exp\left(-\sum_{i=1}^I u_{ij} b_i\right)}_{h(\mathbf{u}_j, \mathbf{b})}
\]

由Neyman-Fisher因子分解定理，\(r_j\) 是 \(\theta_j\) 的充分统计量。\(\square\)

## 4. 条件最大似然估计

### 4.1 条件概率推导

给定总分 \(r_j\) 的条件下，反应模式的概率：

\[
P(\mathbf{u}_j | r_j, \mathbf{b}) = \frac{P(\mathbf{u}_j | \theta_j, \mathbf{b})}{P(r_j | \theta_j, \mathbf{b})}
\]

分母为所有总分为 \(r_j\) 的反应模式的概率和：

\[
P(r_j | \theta_j, \mathbf{b}) = \sum_{\mathbf{u}': \sum u'_i = r_j} P(\mathbf{u}' | \theta_j, \mathbf{b})
\]

\[
= \sum_{\mathbf{u}': \sum u'_i = r_j} \frac{\exp\left(\theta_j r_j - \sum_{i=1}^I u'_i b_i\right)}{\prod_{i=1}^I (1 + e^{\theta_j - b_i})}
\]

\[
= \frac{\exp(\theta_j r_j)}{\prod_{i=1}^I (1 + e^{\theta_j - b_i})} \sum_{\mathbf{u}': \sum u'_i = r_j} \exp\left(-\sum_{i=1}^I u'_i b_i\right)
\]

代入条件概率：

\[
P(\mathbf{u}_j | r_j, \mathbf{b}) = \frac{\exp\left(-\sum_{i=1}^I u_{ij} b_i\right)}{\sum_{\mathbf{u}': \sum u'_i = r_j} \exp\left(-\sum_{i=1}^I u'_i b_i\right)}
\]

关键结果

条件概率不依赖于 \(\theta_j\)，只依赖于项目参数 \(\mathbf{b}\)

### 4.2 条件似然函数

对所有被试：

\[
L_{CML}(\mathbf{b}) = \prod_{j=1}^J P(\mathbf{u}_j | r_j, \mathbf{b})
\]

对数似然：

\[
\ell_{CML}(\mathbf{b}) = \sum_{j=1}^J \left[-\sum_{i=1}^I u_{ij} b_i - \ln\left(\sum_{\mathbf{u}': \sum u'_i = r_j} \exp\left(-\sum_{i=1}^I u'_i b_i\right)\right)\right]
\]

## 5. 估计方法比较

### 5.1 联合最大似然（JMLE）

\[
(\hat{\mathbf{\theta}}, \hat{\mathbf{b}}) = \arg\max_{\mathbf{\theta}, \mathbf{b}} \sum_{j=1}^J \sum_{i=1}^I [u_{ij} \ln P_i(\theta_j) + (1-u_{ij}) \ln(1-P_i(\theta_j))]
\]

问题：参数数量随样本增加而增加，导致不一致性。

### 5.2 边际最大似然（MML）

假设 \(\theta \sim \mathcal{N}(0, 1)\)：

\[
L_{MML}(\mathbf{b}) = \prod_{j=1}^J \int_{-\infty}^{\infty} \left[\prod_{i=1}^I P_i(\theta)^{u_{ij}} (1-P_i(\theta))^{1-u_{ij}}\right] \phi(\theta) d\theta
\]

其中 \(\phi(\theta)\) 是标准正态密度函数。

### 5.3 条件最大似然（CML）

见4.2节。

方法特性比较

| 特性 | JMLE | MML | CML |
| --- | --- | --- | --- |
| 一致性 | 否 | 是 | 是 |
| 需要分布假设 | 否 | 是 | 否 |
| 计算复杂度 | 低 | 高 | 中 |
| 适用模型 | 所有IRT | 所有IRT | Rasch |

## 6. 样本不变性的本质

### 6.1 CTT中的样本依赖

设两个样本的能力分布为 \(g_1(\theta)\) 和 \(g_2(\theta)\)：

\[
p_{i,1} = \int P_i(\theta) g_1(\theta) d\theta
\]

\[
p_{i,2} = \int P_i(\theta) g_2(\theta) d\theta
\]

一般情况下，\(p_{i,1} \neq p_{i,2}\)。

### 6.2 IRT中的样本不变性

在CML估计下：

\[
\hat{b}_i^{(1)} = \arg\max_{b_i} L_{CML}^{(1)}(b_i)
\]

\[
\hat{b}_i^{(2)} = \arg\max_{b_i} L_{CML}^{(2)}(b_i)
\]

理论上，\(\hat{b}_i^{(1)} = \hat{b}_i^{(2)}\)（忽略抽样误差）。

## 7. 实际意义

IRT的优势

**题库建设**：项目参数在不同样本中保持稳定

\[
b_i^{\text{pilot}} \approx b_i^{\text{operational}}
\]

**测验等值**：不同测验形式直接在共同量表上比较

\[
\theta_{\text{Form A}} = \theta_{\text{Form B}}
\]

**自适应测验**：基于稳定的项目参数选择最优题目

\[
i_{next} = \arg\max_i I_i(\hat{\theta}_{current})
\]
