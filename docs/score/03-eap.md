# 3. 期望后验概率（EAP）评分

## 3.1 EAP方法的基本思想

### 3.1.1 从众数到均值

三种估计的区别

**ML**：找似然函数的最大值（众数）

**MAP**：找后验分布的最大值（众数）

**EAP**：计算后验分布的期望值（均值）

\[\hat{\theta}_{EAP} = E[\theta|\mathbf{u}] = \int_{-\infty}^{\infty} \theta \cdot P(\theta|\mathbf{u}) d\theta\]

### 3.1.2 数值积分方法

前置：贝叶斯定理（连续型参数空间）

根据贝叶斯定理：

\[
P(\theta \mid \mathbf{u}) = \frac{L(\mathbf{u} \mid \theta) \cdot P(\theta)}{\int_{-\infty}^{\infty} L(\mathbf{u} \mid \theta') \cdot P(\theta') \, d\theta'}
\]

- 分子是联合密度，代表在能力为 \(\theta\) 且观测到 \(\mathbf{u}\) 的情况下的联合概率；
- 分母是归一化常数，确保后验分布 \(P(\theta \mid \mathbf{u})\) 的积分为 1；
- 在计算 MAP 或 EAP 时，常使用比例形式：

\[
P(\theta \mid \mathbf{u}) \propto L(\mathbf{u} \mid \theta) \cdot P(\theta)
\]

数值积分的原理与公式

**EAP（Expected A Posteriori）估计** 是贝叶斯估计中的一种，目标是求解后验分布的期望值：

\[
\hat{\theta}_{EAP} = \mathbb{E}[\theta \mid \mathbf{u}] = \int_{-\infty}^{\infty} \theta \cdot P(\theta \mid \mathbf{u}) \, d\theta
\]

一、从贝叶斯公式出发

根据贝叶斯定理：

\[
P(\theta \mid \mathbf{u}) = \frac{L(\mathbf{u} \mid \theta) \cdot P(\theta)}{\int L(\mathbf{u} \mid \theta') \cdot P(\theta') \, d\theta'}
\]

二、代入 EAP 估计公式：

\[
\hat{\theta}_{EAP} = \frac{ \int \theta \cdot L(\mathbf{u} \mid \theta) \cdot P(\theta) \, d\theta }{ \int L(\mathbf{u} \mid \theta) \cdot P(\theta) \, d\theta }
\]

三、为什么需要数值积分？

通常 \(L(\mathbf{u} \mid \theta)\) 是如下形式的乘积：

\[
L(\mathbf{u} \mid \theta) = \prod_{i=1}^I P_i(\theta)^{u_i} (1 - P_i(\theta))^{1 - u_i}
\]

其中：

\[
P_i(\theta) = \frac{1}{1 + \exp(-\alpha_i(\theta - \beta_i))}
\]

因为 \(L(\mathbf{u} \mid \theta)\) 是多个非线性 sigmoid 函数的乘积，其与先验 \(P(\theta)\) 的乘积在多数情况下**无法求出解析积分**：

\[
\int_{-\infty}^{\infty} L(\mathbf{u} \mid \theta) \cdot P(\theta) \, d\theta \quad \text{没有封闭形式}
\]

因此，我们只能通过 **数值积分**（如 Gauss-Hermite 或简单求和近似）来逼近后验分布的归一化常数和期望。

四、数值逼近（离散积分）：

将区间 \([-3, 3]\) 离散为 \(R\) 个点，计算近似值：

\[
\hat{\theta}_{EAP} \approx \frac{\sum_{r=1}^{R} \theta_r \cdot L(\mathbf{u}|\theta_r) \cdot P(\theta_r)}{\sum_{r=1}^{R} L(\mathbf{u}|\theta_r) \cdot P(\theta_r)}
\]

五、每一项的解释：

- \(\theta_r\)：第 \(r\) 个能力点（如从 \(-3\) 到 \(3\)，步长 \(0.1\)）
- \(L(\mathbf{u}|\theta_r)\)：在该点上的似然值
- \(P(\theta_r)\)：先验分布在该点的密度

六、直觉解释：

> “在各个 \(\theta_r\) 上，以其后验概率为权重，求其加权平均。”

七、实践建议：

- 常用 \(R=61\)（\([-3,3]\)）
- 更高精度可用 Gauss-Hermite 求积
- 与 MAP 相比，EAP 更稳定但计算更慢

## 3.2 EAP算法的实现

EAP数值积分的具体步骤

在前面我们已经知道，EAP估计是后验分布的期望：

\[
\hat{\theta}_{EAP} = \frac{ \int \theta \cdot L(\mathbf{u} \mid \theta) \cdot P(\theta) \, d\theta }{ \int L(\mathbf{u} \mid \theta) \cdot P(\theta) \, d\theta }
\]

回顾它的近似值：

\[
\hat{\theta}_{EAP} \approx \frac{\sum_{r=1}^{R} \theta_r \cdot L(\mathbf{u}|\theta_r) \cdot P(\theta_r)}{\sum_{r=1}^{R} L(\mathbf{u}|\theta_r) \cdot P(\theta_r)}
\]

下面我们采用 **离散求和逼近** 这个积分，分为五步：

**第一步：设置求积点**

- 在区间 \(\theta \in [-3, 3]\) 上，选取 \(R=61\) 个等距点
- 例如：\(\theta_r \in \{-3.0, -2.9, ..., 2.9, 3.0\}\)
- 步长为 \(0.1\)，共 \(R=61\) 个点

**第二步：计算先验密度 \(P(\theta_r)\)**

- 若使用标准正态先验：\(P(\theta_r) = \phi(\theta_r) = \frac{1}{\sqrt{2\pi}} e^{-\theta_r^2/2}\)
- 可选归一化版本：\(W_r = \frac{\phi(\theta_r)}{\sum_{s=1}^R \phi(\theta_s)}\) （使权重和为 1）

**第三步：计算似然函数 \(L(\mathbf{u} \mid \theta_r)\)**

- 在每个 \(\theta_r\) 处计算：

\[
L(\mathbf{u} \mid \theta_r) = \prod_{i=1}^I P_i(\theta_r)^{u_i} \cdot (1 - P_i(\theta_r))^{1 - u_i}
\]

- 其中 \(P_i(\theta_r) = \frac{1}{1 + \exp(-\alpha_i(\theta_r - \beta_i))}\) 是第 \(i\) 个项目的2PL模型成功概率

**第四步：计算非归一化的后验权重**

\[
W_r^* = L(\mathbf{u} \mid \theta_r) \cdot P(\theta_r)
\]

> 后验密度 ∝ 似然 × 先验，因此这个就是比例项

**第五步：归一化并求加权平均**

- 归一化：

\[
\tilde{W}_r = \frac{W_r^*}{\sum_{s=1}^R W_s^*}
\]

- 最终得到 EAP 估计：

\[
\hat{\theta}_{EAP} = \sum_{r=1}^R \theta_r \cdot \tilde{W}_r
\]

**结论理解：**

> 本质上就是“加权平均所有 \(\theta_r\)”，其中权重是每点的**后验概率密度**，因此能反映出后验的中心趋势。

## 3.3 标准误的计算

EAP标准误的定义与计算

为了衡量 EAP 估计的不确定性，我们希望计算后验分布的标准差作为估计误差：

一、基本定义

后验标准差的定义是后验分布关于其期望值的标准差：

\[
SE_{EAP} = \sqrt{ \text{Var}[\theta \mid \mathbf{u}] }
= \sqrt{ \mathbb{E}[(\theta - \hat{\theta}_{EAP})^2 \mid \mathbf{u}] }
\]

这表示在后验分布下，\(\theta\) 围绕其均值（即 \(\hat{\theta}_{EAP}\)）的波动程度。

二、代入后验分布

将期望展开为积分形式：

\[
SE_{EAP}
= \sqrt{ \int_{-\infty}^{\infty} (\theta - \hat{\theta}_{EAP})^2 \cdot P(\theta \mid \mathbf{u}) \, d\theta }
\]

注意：这与频率学派中基于采样分布的标准误不同，这里是对**后验分布**进行积分。

三、离散求和逼近

因为积分无法解析计算，我们使用数值积分将其逼近：

\[
SE_{EAP}
\approx \sqrt{ \sum_{r=1}^R (\theta_r - \hat{\theta}_{EAP})^2 \cdot \tilde{W}_r }
\]

其中：

- \(\theta_r\) 是离散化的能力点（如 \([-3, 3]\) 区间等距划分）
- \(\tilde{W}_r\) 是归一化的后验概率：

\[
\tilde{W}_r = \frac{L(\mathbf{u} \mid \theta_r) \cdot P(\theta_r)}{\sum_{s=1}^R L(\mathbf{u} \mid \theta_s) \cdot P(\theta_s)}
\]

也就是在每个 \(\theta_r\) 点上，“发生该能力水平的后验概率”

四、总结含义

- 这个标准差量化了 \(\theta\) 在后验分布下的 **不确定性**；
- 如果 \(\tilde{W}_r\) 很集中（说明我们很确定 \(\theta\) 的位置），那么 \(SE_{EAP}\) 会很小；
- 如果 \(\tilde{W}_r\) 分布广泛（说明我们很不确定），那么 \(SE_{EAP}\) 会很大；
- 不依赖样本量信息，也不使用 Fisher 信息，是**贝叶斯推断特有的标准误形式**。

> 与 MAP 或 MLE 的标准误不同，EAP 的标准误考虑了整个后验分布，而不仅仅是一个点附近的曲率。

## 3.4 EAP评分实例

表7.4展示了EAP评分结果：

| 考生 | 反应模式 | MAP |  | EAP |  |
| --- | --- | --- | --- | --- | --- |
|  |  | \(\hat{\theta}\) | \(SE\) | \(\hat{\theta}\) | \(SE\) |
| 1 | \(1111100000\) | \(0.00\) | \(0.47\) | \(0.00\) | \(0.48\) |
| 15 | \(0000000000\) | \(-1.48\) | \(0.53\) | \(-1.52\) | \(0.54\) |
| 23 | \(1111111110\) | \(1.48\) | \(0.53\) | \(1.52\) | \(0.54\) |

EAP vs MAP的比较

**相似性**：

- 两者都使用先验信息
- 估计值通常很接近
- 都能处理极端反应

**差异**：

- EAP是均值，MAP是众数
- EAP计算不需要迭代
- EAP更容易推广到复杂模型

## 3.5 三种方法的综合比较

评分方法选择指南

**使用ML当**：

- 测验较长（>30题）
- 不担心极端反应
- 需要无偏估计

**使用MAP当**：

- 测验较短
- 需要处理所有反应模式
- 愿意接受轻微偏差

**使用EAP当**：

- 需要快速计算
- 使用复杂IRT模型
- 重视均方误差最小
