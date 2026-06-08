# 规则10详解：项目刺激特征的重要性

规则对比

| CTT | IRT |
| --- | --- |
| 与心理测量属性相比，项目刺激特征不重要 | 项目刺激特征可以直接与心理测量属性相关 |

## 1. 项目刺激特征的定义与分类

项目刺激特征（Item Stimulus Features）

**定义**：题目中可能影响个体反应的各种具体特征

**特征的层次结构**：

1. **表面特征**：可直接观察的物理属性
2. **结构特征**：题目的逻辑或认知结构
3. **内容特征**：涉及的知识领域或主题
4. **过程特征**：解题所需的认知过程

### 1.1 认知能力测验中的特征体系

**表面特征**：

- 呈现模态：视觉vs听觉、文字vs图形vs符号
- 元素数量：题目中包含的信息单元数量
- 时间压力：有限时间vs无限时间
- 反应格式：选择vs构造、单选vs多选

**结构特征**：

- 逻辑关系：类比、分类、序列、矩阵
- 变换规律：旋转、翻转、大小变化、颜色变化
- 干扰因素：无关信息的数量和类型
- 抽象程度：具体图形vs抽象符号

**认知过程特征**：

- 工作记忆负荷：需要同时保持的信息量
- 注意控制：需要抑制的干扰信息量
- 流体推理：需要发现的模式复杂度
- 处理速度：完成所需的基本操作数量

## 2. CTT框架下项目特征的边缘化

### 2.1 传统测验开发的"黑箱"模式

CTT测验开发的典型流程

**阶段1：内容规范**
- 做法：制定宽泛的内容描述
- 问题：规范过于抽象，缺乏操作性

**阶段2：项目编写**
- 做法：依靠编写者的主观经验
- 问题：缺乏科学指导，质量不稳定

**阶段3：试测筛选**
- 做法：用统计指标筛选项目
- 问题：只关注统计性能，忽视特征-性能关系

**阶段4：最终选择**
- 做法：基于统计指标和内容平衡
- 问题：无法预测或控制项目性能

### 2.2 特征空间的高维性问题

设项目特征空间为 \(\mathcal{F} = \mathbb{R}^n\)（\(n\) 很大），而规范只能描述 \(k\) 个维度（\(k \ll n\)），则：

\[
\text{规范覆盖度} = \frac{k}{n} \to 0
\]

项目性能往往由特征的复杂交互决定：

\[
\text{性能} = f(x_1, x_2, \ldots, x_n) + \sum_{i<j} g_{ij}(x_i, x_j) + \sum_{i<j<k} h_{ijk}(x_i, x_j, x_k) + \cdots
\]

## 3. IRT中项目特征建模：线性Logistic测验模型（LLTM）

### 3.1 LLTM的基本框架

线性Logistic测验模型（LLTM）

**核心思想**：将项目难度分解为基本认知操作的线性组合

**基本模型**：

\[
P_i(\theta) = \frac{\exp(\theta - \sum_{k=1}^K q_{ik}\eta_k)}{1 + \exp(\theta - \sum_{k=1}^K q_{ik}\eta_k)}
\]

**难度分解**：

\[
b_i = \sum_{k=1}^K q_{ik}\eta_k
\]

### 3.2 参数估计的详细推导

**似然函数**：

对于个体 \(j\) 在项目 \(i\) 上的反应 \(u_{ij}\)：

\[
L_{ij} = P_i(\theta_j)^{u_{ij}}[1-P_i(\theta_j)]^{1-u_{ij}}
\]

**对数似然**：

\[
\ln L = \sum_{i=1}^I \sum_{j=1}^J \left[u_{ij}\ln P_i(\theta_j) + (1-u_{ij})\ln(1-P_i(\theta_j))\right]
\]

**LLTM约束下的对数似然**：

将 \(b_i = \sum_{k=1}^K q_{ik}\eta_k\) 代入：

\[
\ln L = \sum_{i=1}^I \sum_{j=1}^J \left[u_{ij}(\theta_j - \sum_{k=1}^K q_{ik}\eta_k) - \ln(1 + \exp(\theta_j - \sum_{k=1}^K q_{ik}\eta_k))\right]
\]

**对 \(\eta_k\) 的导数**：

\[
\frac{\partial \ln L}{\partial \eta_k} = -\sum_{i=1}^I \sum_{j=1}^J q_{ik}\left[u_{ij} - P_i(\theta_j)\right]
\]

**对 \(\theta_j\) 的导数**：

\[
\frac{\partial \ln L}{\partial \theta_j} = \sum_{i=1}^I \left[u_{ij} - P_i(\theta_j)\right]
\]

### 3.3 Newton-Raphson迭代

**Hessian矩阵元素**：

\[
\frac{\partial^2 \ln L}{\partial \eta_k \partial \eta_l} = -\sum_{i=1}^I \sum_{j=1}^J q_{ik}q_{il}P_i(\theta_j)[1-P_i(\theta_j)]
\]

\[
\frac{\partial^2 \ln L}{\partial \theta_j \partial \theta_m} = -\delta_{jm}\sum_{i=1}^I P_i(\theta_j)[1-P_i(\theta_j)]
\]

\[
\frac{\partial^2 \ln L}{\partial \eta_k \partial \theta_j} = -\sum_{i=1}^I q_{ik}P_i(\theta_j)[1-P_i(\theta_j)]
\]

**更新公式**：

\[
\begin{pmatrix}
\mathbf{\eta}^{(t+1)} \
\mathbf{\theta}^{(t+1)}
\end{pmatrix} =
\begin{pmatrix}
\mathbf{\eta}^{(t)} \
\mathbf{\theta}^{(t)}
\end{pmatrix} - \mathbf{H}^{-1}\mathbf{g}
\]

其中 \(\mathbf{H}\) 是Hessian矩阵，\(\mathbf{g}\) 是梯度向量。

### 3.4 模型拟合检验

**似然比检验**：

比较LLTM与标准Rasch模型：

\[
\chi^2 = 2[\ln L_{\text{Rasch}} - \ln L_{\text{LLTM}}]
\]

自由度：

\[
df = (I-1) - K
\]

其中 \(I\) 是项目数，\(K\) 是特征数。

**条件是**：\(K < I-1\)，否则LLTM会过度参数化。

## 4. 认知诊断模型

### 4.1 基本框架

认知诊断模型（CDMs）

**个体属性向量**：

\[
\mathbf{\alpha}_j = (\alpha_{j1}, \alpha_{j2}, \ldots, \alpha_{jK})'
\]

其中 \(\alpha_{jk} \in \{0, 1\}\) 表示个体 \(j\) 是否掌握属性 \(k\)

**Q矩阵**：

\[
Q = (q_{ik})_{I \times K}
\]

其中 \(q_{ik} \in \{0, 1\}\) 表示项目 \(i\) 是否需要属性 \(k\)

### 4.2 DINA模型的详细分析

**DINA（Deterministic Input, Noisy And gate）模型**：

**理想反应**：

\[
\eta_{ij} = \prod_{k=1}^K \alpha_{jk}^{q_{ik}}
\]

当且仅当个体掌握项目所需的所有属性时，\(\eta_{ij} = 1\)。

**反应概率**：

\[
P(u_{ij} = 1 | \mathbf{\alpha}_j) = (1-s_i)^{\eta_{ij}} g_i^{1-\eta_{ij}}
\]

其中：

- \(s_i\)：失误参数（slip parameter）- 掌握所有技能但答错的概率
- \(g_i\)：猜测参数（guessing parameter）- 未掌握所有技能但答对的概率

**参数约束**：

\[
0 < g_i < 1-s_i < 1
\]

### 4.3 DINA模型的似然函数

**个体似然**：

\[
L_j = \prod_{i=1}^I P(u_{ij}|\mathbf{\alpha}_j)
\]

**边际似然**：

\[
L_j = \sum_{\mathbf{\alpha} \in \{0,1\}^K} \left[\prod_{i=1}^I P(u_{ij}|\mathbf{\alpha})\right] P(\mathbf{\alpha})
\]

其中 \(P(\mathbf{\alpha})\) 是属性模式的先验分布。

**对数似然**：

\[
\ln L = \sum_{j=1}^J \ln\left[\sum_{\mathbf{\alpha} \in \{0,1\}^K} \left[\prod_{i=1}^I P(u_{ij}|\mathbf{\alpha})\right] P(\mathbf{\alpha})\right]
\]

### 4.4 EM算法估计

**E步**：计算属性模式的后验概率

\[
P(\mathbf{\alpha}_c|\mathbf{u}_j) = \frac{\prod_{i=1}^I P(u_{ij}|\mathbf{\alpha}_c) P(\mathbf{\alpha}_c)}{\sum_{\mathbf{\alpha} \in \{0,1\}^K} \prod_{i=1}^I P(u_{ij}|\mathbf{\alpha}) P(\mathbf{\alpha})}
\]

**M步**：更新参数

失误参数：

\[
\hat{s}_i = \frac{\sum_{j:u_{ij}=0} P(\eta_{ij}=1|\mathbf{u}_j)}{\sum_{j=1}^J P(\eta_{ij}=1|\mathbf{u}_j)}
\]

猜测参数：

\[
\hat{g}_i = \frac{\sum_{j:u_{ij}=1} P(\eta_{ij}=0|\mathbf{u}_j)}{\sum_{j=1}^J P(\eta_{ij}=0|\mathbf{u}_j)}
\]

### 4.5 扩展模型

**DINO模型**（Deterministic Input, Noisy Or gate）：

\[
\eta_{ij} = 1 - \prod_{k=1}^K (1-\alpha_{jk})^{q_{ik}}
\]

掌握任一所需属性即可。

**G-DINA模型**（Generalized DINA）：

\[
P(u_{ij}=1|\mathbf{\alpha}_j^*) = \delta_{i0} + \sum_{k=1}^{K_i^*} \delta_{ik}\alpha_{jk}^* + \sum_{k<l} \delta_{ikl}\alpha_{jk}^*\alpha_{jl}^* + \cdots
\]

允许主效应和交互效应。

## 5. 实际应用示例

### 5.1 实际问题解决的特征分析

考虑一个分数加法问题：\(\frac{2}{3} + \frac{3}{4} = ?\)

**认知属性**：

1. 识别分母（\(\alpha_1\)）
2. 找最小公倍数（\(\alpha_2\)）
3. 通分（\(\alpha_3\)）
4. 分子相加（\(\alpha_4\)）
5. 化简（\(\alpha_5\)）

**Q矩阵构建**：

| 项目 | \(\alpha_1\) | \(\alpha_2\) | \(\alpha_3\) | \(\alpha_4\) | \(\alpha_5\) |
| --- | --- | --- | --- | --- | --- |
| \(\frac{1}{2}+\frac{1}{2}\) | 1 | 0 | 0 | 1 | 0 |
| \(\frac{1}{2}+\frac{1}{3}\) | 1 | 1 | 1 | 1 | 0 |
| \(\frac{2}{3}+\frac{3}{4}\) | 1 | 1 | 1 | 1 | 0 |
| \(\frac{2}{4}+\frac{3}{6}\) | 1 | 0 | 0 | 1 | 1 |

### 5.2 模型比较

**信息准则**：

\[
\text{AIC} = -2\ln L + 2p
\]

\[
\text{BIC} = -2\ln L + p\ln N
\]

其中：

- LLTM: \(p = K + J\)
- DINA: \(p = 2I + 2^K - 1\)
- Rasch: \(p = I + J - 1\)

选择建议

**使用LLTM当**：

- 特征效应可假设为线性
- 需要预测新项目难度
- 项目数量远大于特征数量

**使用CDMs当**：

- 需要诊断具体技能掌握
- 属性是离散的（掌握/未掌握）
- 关注个体的认知剖面
