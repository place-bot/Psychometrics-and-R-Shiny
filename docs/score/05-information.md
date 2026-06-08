# 5. 项目和测验信息

## 5.1 信息的概念

### 5.1.1 Fisher信息的定义

信息的定义

**Fisher信息（Fisher Information）** 是统计学中衡量一个观测样本中关于参数的不确定性的指标。

\[
I(\theta) = E\left[\left(\frac{\partial \log L}{\partial \theta}\right)^2\right] = -E\left[\frac{\partial^2 \log L}{\partial \theta^2}\right]
\]

- 第一种形式解释：期望平方导数越大，说明小的参数变化导致较大的对数似然变动，因此样本中包含的"信息量"更大。
- 第二种形式解释：对数似然函数的二阶导数的期望（负号是因为通常为负值）也代表了对数似然的“弯曲程度”——越陡峭，估计越精准。

**直观理解**：

- 信息量大，说明我们能较准确地估计参数；
- 信息量小，估计会有更大的不确定性；
- 它与标准误之间关系为：

\[
SE(\theta) = \frac{1}{\sqrt{I(\theta)}}
\]

即信息越大，标准误越小。

---

## 5.2 项目信息函数

### 5.2.1 二分项目的信息公式

项目信息的定义与推导

**一、基本定义：**

设第 \(i\) 个项目的反应 \(u_i\) 是一个二元随机变量（0 或 1），满足伯努利分布：

\[
u_i \sim \text{Bernoulli}(P_i(\theta))
\]

则其**对数似然函数**为：

\[
\log L_i(\theta) = u_i \log P_i(\theta) + (1 - u_i) \log [1 - P_i(\theta)]
\]

对其关于 \(\theta\) 求导数：

\[
\frac{\partial \log L_i(\theta)}{\partial \theta} = \frac{u_i P'_i(\theta)}{P_i(\theta)} - \frac{(1 - u_i) P'_i(\theta)}{1 - P_i(\theta)} = \frac{P'_i(\theta)}{P_i(\theta)[1 - P_i(\theta)]} \cdot (u_i - P_i(\theta))
\]

**Fisher 信息的定义**是该导数平方的期望：

\[
I_i(\theta) = E \left[ \left( \frac{\partial \log L_i(\theta)}{\partial \theta} \right)^2 \right]
\]

把上面的导数带入得到：

\[
I_i(\theta) = \left( \frac{P'_i(\theta)}{P_i(\theta)[1 - P_i(\theta)]} \right)^2 \cdot E\left[(u_i - P_i(\theta))^2\right]
\]

注意期望项是方差：

\[
E[(u_i - P_i(\theta))^2] = \text{Var}(u_i) = P_i(\theta)[1 - P_i(\theta)]
\]

所以最终得到：

\[
I_i(\theta) = \frac{[P'_i(\theta)]^2}{P_i(\theta)[1 - P_i(\theta)]}
\]

1PL / Rasch 模型

**反应函数**：

\[
P_i(\theta) = \frac{1}{1 + \exp[-(\theta - \beta_i)]}
\]

设 \(\eta_i = \theta - \beta_i\)，则：

\[
P_i(\theta) = \frac{e^{\eta_i}}{1 + e^{\eta_i}}, \quad \Rightarrow \quad P'_i(\theta) = \frac{d}{d\theta} P_i(\theta) = P_i(\theta)[1 - P_i(\theta)]
\]

带入一般公式：

\[
I_i(\theta) = \frac{[P_i(\theta)(1 - P_i(\theta))]^2}{P_i(\theta)[1 - P_i(\theta)]} = P_i(\theta)[1 - P_i(\theta)]
\]

2PL 模型

**反应函数**：

\[
P_i(\theta) = \frac{1}{1 + \exp[-\alpha_i(\theta - \beta_i)]}
\]

令 \(\eta_i = \alpha_i(\theta - \beta_i)\)，计算导数：

\[
P'_i(\theta) = \alpha_i \cdot P_i(\theta)[1 - P_i(\theta)]
\]

所以代入信息函数：

\[
I_i(\theta) = \frac{[\alpha_i \cdot P_i(\theta)[1 - P_i(\theta)]]^2}{P_i(\theta)[1 - P_i(\theta)]} = \alpha_i^2 \cdot P_i(\theta)[1 - P_i(\theta)]
\]

3PL 模型

**反应函数**：

\[
P_i(\theta) = c_i + (1 - c_i) \cdot \frac{1}{1 + \exp[-\alpha_i(\theta - \beta_i)]}
\]

设：

\[
Q_i(\theta) = \frac{1}{1 + \exp[-\alpha_i(\theta - \beta_i)]}
\]

则：

\[
P_i(\theta) = c_i + (1 - c_i) Q_i(\theta)
\]

导数：

\[
P'_i(\theta) = (1 - c_i) \cdot Q'_i(\theta) = (1 - c_i) \cdot \alpha_i \cdot Q_i(\theta)[1 - Q_i(\theta)]
\]

记住：

\[
Q_i(\theta) = \frac{P_i(\theta) - c_i}{1 - c_i}
\]

整理代入：

\[
P'_i(\theta) = \alpha_i \cdot \frac{P_i(\theta) - c_i}{1 - c_i} \left(1 - \frac{P_i(\theta) - c_i}{1 - c_i}\right) = \alpha_i \cdot \frac{(P_i - c_i)(1 - P_i)}{(1 - c_i)^2}
\]

所以信息函数为：

\[
I_i(\theta) = \frac{[P'_i(\theta)]^2}{P_i(\theta)[1 - P_i(\theta)]} = \alpha_i^2 \cdot \frac{(P_i - c_i)^2 (1 - P_i)}{(1 - c_i)^4 P_i}
\]

最终常用整理版本为：

\[
I_i(\theta) = \alpha_i^2 \cdot \frac{[P_i(\theta) - c_i]^2}{(1 - c_i)^2} \cdot \frac{1 - P_i(\theta)}{P_i(\theta)}
\]

### 5.2.2 信息函数的特征

关键规律

**1. 位置规律**：

- 对于 1PL 和 2PL 模型，信息函数在 \(\theta = \beta\) 时达到最大值。
- 对于 3PL 模型，由于猜测参数的影响，最大值偏向略高于 \(\beta\) 的位置。

**2. 高度规律**：

- 区分度 \(\alpha\) 越大，反应曲线越陡，信息也就越大。
- 猜测参数 \(c\) 越大，会抬高底部概率，使信息量减少。

**3. 形状规律**：

- 高区分度的题目信息曲线呈尖峰状（高度集中）；
- 低区分度的题目信息曲线较平缓，作用范围更广但精度低。

信息函数的性质推导

**1. 位置规律：信息函数最大值的位置**

我们以 2PL 模型为例，其信息函数为：

\[
I_i(\theta) = \alpha_i^2 P_i(\theta)[1 - P_i(\theta)]
\]

因为 \(P_i(\theta)\) 是 S 型函数，关于 \(\theta = \beta_i\) 对称，其值在 \([0, 1]\) 之间。

当 \(P_i(\theta) = 0.5\) 时，\(1 - P_i(\theta) = 0.5\)，此时信息函数为：

\[
I_i(\theta) = \alpha_i^2 \cdot 0.5 \cdot 0.5 = \frac{\alpha_i^2}{4}
\]

因此，信息在以下位置达到最大：

\[
\boxed{\theta = \beta_i}
\]

对于 1PL 模型（即 \(\alpha_i = 1\)），结论同样成立。

对于 3PL 模型，信息函数变为：

\[
I_i(\theta) = \alpha_i^2 \cdot \frac{[P_i(\theta) - c_i]^2}{(1 - c_i)^2} \cdot \frac{1 - P_i(\theta)}{P_i(\theta)}
\]

由于 \(P_i(\theta)\) 的下界为 \(c_i\)，信息峰值不再出现在 \(\theta = \beta_i\)，而是略微向右偏移，即：

\[
\boxed{\theta^\star > \beta_i}
\]

**2. 高度规律：信息峰值的大小**

继续以 2PL 模型为例，代入 \(\theta = \beta_i\) 得：

\[
I_i(\beta_i) = \alpha_i^2 \cdot 0.5 \cdot 0.5 = \frac{\alpha_i^2}{4}
\]

由此可见，信息峰值与区分度平方成正比。

进一步解释如下：

- 若区分度 \(\alpha_i\) 越大，斜率越陡，峰值越高；
- 若猜测参数 \(c_i\) 越大，会抬高低能力者的答对概率，使 \(P_i(\theta)\) 更平缓，减小 \([P_i(\theta) - c_i]^2\)，从而降低信息量。

**3. 形状规律：信息曲线的陡峭和平坦**

由公式：

\[
I_i(\theta) = \alpha_i^2 P_i(\theta)[1 - P_i(\theta)]
\]

可以推知信息函数的形状受区分度 \(\alpha_i\) 控制。

- 如果 \(\alpha_i\) 较大：

  - \(P_i(\theta)\) 上升更快；
  - 信息函数在 \(\theta = \beta_i\) 附近集中；
  - 曲线呈现尖峰状（narrow peak）。
- 如果 \(\alpha_i\) 较小：

  - \(P_i(\theta)\) 上升更慢；
  - 信息函数分布范围较广；
  - 曲线更平缓（broad curve）。

**总结：**

- 区分度 \(\alpha_i\) 决定信息函数的“集中度”；
- 较高的 \(\alpha_i\) 意味着测量更精准但范围较窄；
- 较低的 \(\alpha_i\) 意味着测量范围更广但精度较低。

## 5.3 测验信息函数

### 5.3.1 信息的可加性

测验信息的计算

**基本原理**：若题目独立，信息函数具有可加性。

\[
TI(\theta) = \sum_{i=1}^I I_i(\theta)
\]

**含义说明**：

- 测验整体的信息量由所有题目的信息函数叠加而成；
- 每道题对能力水平的精准度有贡献；
- 这是测验设计与自适应测验的基础。

### 5.3.2 信息与标准误

实用公式

**标准误与总信息之间的关系**：

\[
SE(\theta) = \frac{1}{\sqrt{TI(\theta)}}
\]

**示例说明**：

- \(TI(\theta) = 4\)：\(SE = 0.50\)
- \(TI(\theta) = 25\)：\(SE = 0.20\)
- \(TI(\theta) = 100\)：\(SE = 0.10\)

> 这意味着，要提高精度（降低 SE），我们可以设计更有效的题目来提高信息量。

---

## 5.4 多分类项目的信息

### 5.4.1 多类别模型的推广

扩展到多分类

对于有多个选项的项目（如GRM、NRM模型），其信息函数推广如下：

\[
I_i(\theta) = \sum_{k=0}^{m_i} \frac{[P'_{ik}(\theta)]^2}{P_{ik}(\theta)}
\]

- \(P_{ik}(\theta)\) 表示在能力为 \(\theta\) 时选中类别 \(k\) 的概率；
- \(P'_{ik}(\theta)\) 是该概率关于 \(\theta\) 的导数；
- 样条和Logistic模型都可代入该通式。

**理解**：该公式衡量的是“概率曲线变化剧烈处提供的信息更丰富”。

- 如果一个选项的选择概率随着能力剧烈变化，那么我们能据此区分高低能力的受试者，因此该题在该点提供的信息多。

多分类信息函数通常在每一类别之间的转折点（category boundary）附近最大。

> 这对构造多层级评分项目（如Likert量表）尤其重要。
