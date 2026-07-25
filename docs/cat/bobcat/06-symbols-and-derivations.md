# BOBCAT 符号表与必要推导

## 符号回查表

这一章只用于读完正文后的查阅。相同字母在不同文献中可能有不同含义，下面严格按本讲义
和 BOBCAT 原论文的语境整理。

### 数据与索引

| 符号 | 类型 | 含义 |
| --- | --- | --- |
| \(N\) | 正整数 | 历史训练响应数据中的学生数 |
| \(Q\) | 正整数 | 题库题目总数 |
| \(i\) | 学生索引 | \(i=1,\ldots,N\) |
| \(j,r\) | 题目索引 | 题库中的题号；\(r\) 常作求和临时索引 |
| \(t,\tau\) | 选题步索引 | \(t=1,\ldots,n\)；上标 \((t)\) 表示步骤 |
| \(k\) | 内层 GD 步索引 | \(k=0,\ldots,K-1\) |
| \(n\) | 正整数 | 每名学生短测中选择的题数 |
| \(K\) | 正整数 | 每次学生特定适应的梯度下降步数 |
| \(Y_{i,j}\) | \(0/1\) | 学生 \(i\) 对题 \(j\) 的历史或实时作答 |
| \(\mathcal O_i\) | 题目集合 | 数据中学生 \(i\) 有已观测答案的题 |
| \(\Omega_i^{(t)}\) | 题目集合 | 第 \(t\) 步学生 \(i\) 尚可选择的 training 候选题 |
| \(\Gamma_i\) | 题目集合 | 学生 \(i\) 的 held-out meta 题 |
| \(S_i^{(t)}\) | 题目集合 | 截至第 \(t\) 步已选题集合 |
| \(j_i^{(t)}\) | 题号 | 第 \(t\) 步为学生 \(i\) 选择的题 |
| \(j_i^{(1:n)}\) | 题号序列 | 学生 \(i\) 的整条长度 \(n\) 选题轨迹 |
| \(\mathcal B\) | 学生集合 | 当前 mini-batch |

### 模型与状态

| 符号 | 类型 | 含义 |
| --- | --- | --- |
| \(x_i^{(t)}\) | \(Q\) 维向量 | 第 \(t\) 步选题前的作答状态，分量取 \(-1,0,1\) |
| \(g(j;\theta_i)\) | 概率函数 | 响应模型对学生 \(i\) 答对题 \(j\) 的预测 |
| \(\theta_i\) | 标量或向量 | 学生 \(i\) 的局部响应参数 |
| \(\theta_i^*\) | 标量或向量 | 理想内层最优解；实现中由 \(\theta_i^{(K)}\) 近似 |
| \(\theta_i^{(k)}\) | 标量或向量 | 内层第 \(k\) 步后的局部参数 |
| \(\gamma\) | 参数集合 | 全局响应模型参数 |
| \(\psi\) | 参数集合 | 本讲义拆出的共享响应参数，例如题目难度或网络权重 |
| \(\mu\) | 标量或向量 | 本讲义拆出的局部参数全局初始化或先验中心 |
| \(\Pi(\cdot;\phi)\) | 策略 | 题目选择算法 |
| \(\phi\) | 参数向量 | 选题器神经网络参数 |
| \(z_{i,j}^{(t)}\) | 实数 | 选题网络给候选题 \(j\) 的 logit |
| \(b_j\) | 实数 | 1PL IRT 中题 \(j\) 的难度 |
| \(p_{i,j}\) | \(0\) 到 \(1\) | 预测答对概率 |

### 损失、优化与梯度

| 符号 | 类型 | 含义 |
| --- | --- | --- |
| \(\ell(y,p)\) | 标量函数 | 一道题的二元交叉熵 |
| \(\mathcal L(\theta_i,\Gamma_i)\) | 标量 | 学生 \(i\) 的 meta 题总损失 |
| \(\mathcal L_i'(\theta_i)\) | 标量 | 学生 \(i\) 的内层训练目标 |
| \(\mathcal J(\gamma,\phi)\) | 标量 | 全体学生平均外层目标 |
| \(R(\gamma,\theta_i)\) | 标量 | 把局部参数约束在全局值附近的正则项 |
| \(\alpha\) | 正实数 | 内层局部参数学习率 |
| \(\eta_1\) | 正实数 | 全局响应参数外层学习率 |
| \(\eta_2\) | 正实数 | 选题器参数外层学习率 |
| \(\nabla_\theta f\) | 向量 | \(f\) 对 \(\theta\) 的梯度 |
| \(\nabla_\theta^2f\) | 矩阵 | \(f\) 对 \(\theta\) 的 Hessian |
| \(H\) | 矩阵 | Hessian 的简写 |
| \(b_i\) | 标量 | 式（8）中降低方差的 baseline/control variate |
| \(w_j\) | \(0/1\) 或松弛权重 | 第 \(t\) 步题 \(j\) 是否进入内层损失 |
| \(\mathcal I_i(j)\) | 标量 | 题 \(j\) 对学生 \(i\) 的影响函数分数 |
| \(\lambda,\delta\) | 非负实数 | 正则强度或 Hessian 阻尼 |

### 运算符

| 符号 | 含义 |
| --- | --- |
| \(\operatorname*{arg\,min}_x f(x)\) | 返回让 \(f(x)\) 最小的 \(x\)；最小函数值记为 \(\min_x f(x)\) |
| \(\mathbb{E}[\cdot]\) | 对随机变量取期望 |
| \(\Pr(\cdot)\) | 概率 |
| \(\sim\) | 从某个分布抽样 |
| \(\lvert S\rvert\) | 集合元素个数；用于标量时也可表示绝对值，需看上下文 |
| \(\setminus\) | 集合差 |
| \(\mathbb{I}(A)\) | 事件 \(A\) 成立时为 1，否则为 0 |
| \(\operatorname{stopgrad}\) | 前向保留数值、反向梯度设为 0 |
| \((\cdot)^\mathsf{T}\) | 向量或矩阵转置 |
| \(\equiv\) 或 \(:=\) | 定义一个缩写或恒等表示 |

## 必要微积分推导

### sigmoid 导数

\[
\sigma(z)=\frac{1}{1+e^{-z}}.
\]
求导：

\[
\begin{aligned}
\sigma'(z)
&=-(1+e^{-z})^{-2}(-e^{-z})\\
&=\frac{e^{-z}}{(1+e^{-z})^2}\\
&=\frac{1}{1+e^{-z}}
\left(1-\frac{1}{1+e^{-z}}\right)\\
&=\sigma(z)(1-\sigma(z)).
\end{aligned}
\]

### 二元交叉熵对 logit 的导数

令 \(p=\sigma(z)\)，
\[
\ell(y,p)=-y\log p-(1-y)\log(1-p).
\]
先对 \(p\) 求导：
\[
\frac{\partial\ell}{\partial p}
=-\frac{y}{p}+\frac{1-y}{1-p}.
\]
再乘
\[
\frac{\partial p}{\partial z}=p(1-p).
\]
得到

\[
\begin{aligned}
\frac{\partial\ell}{\partial z}
&=
\left(-\frac{y}{p}+\frac{1-y}{1-p}\right)p(1-p)\\
&=-y(1-p)+(1-y)p\\
&=p-y.
\end{aligned}
\]

1PL 中 \(z=\theta-b\)，所以 \(\partial z/\partial\theta=1\)，从而
\(\partial\ell/\partial\theta=p-y\)。

### softmax 与 log-softmax 导数

令
\[
\pi_a=\frac{e^{z_a}}{\sum_s e^{z_s}}.
\]
对 \(z_r\) 求导：
\[
\frac{\partial\pi_a}{\partial z_r}
=\pi_a\left(\mathbb{I}(a=r)-\pi_r\right).
\]
再除以 \(\pi_a\)：
\[
\frac{\partial\log\pi_a}{\partial z_r}
=\mathbb{I}(a=r)-\pi_r.
\]
这说明提高被选动作 log 概率的梯度同时压低其他动作概率。

### score-function 恒等式

对离散 \(X\)：

\[
\begin{aligned}
\nabla_\phi\mathbb{E}_{X\sim p_\phi}[f(X)]
&=\nabla_\phi\sum_x p_\phi(x)f(x)\\
&=\sum_x \nabla_\phi p_\phi(x)f(x)\\
&=\sum_x p_\phi(x)
\frac{\nabla_\phi p_\phi(x)}{p_\phi(x)}
f(x)\\
&=\sum_x p_\phi(x)f(x)\nabla_\phi\log p_\phi(x)\\
&=\mathbb{E}[f(X)\nabla_\phi\log p_\phi(X)].
\end{aligned}
\]

若 \(f\) 还直接依赖 \(\phi\)，应增加
\(\mathbb{E}[\nabla_\phi f(X,\phi)]\)。BOBCAT 在把离散轨迹固定后，主要用 score-function
处理动作分布依赖。

### baseline 不改变期望

只要 \(b\) 不依赖当前抽样动作，

\[
\begin{aligned}
\mathbb{E}[b\nabla_\phi\log p_\phi(X)]
&=b\sum_xp_\phi(x)\nabla_\phi\log p_\phi(x)\\
&=b\sum_x\nabla_\phi p_\phi(x)\\
&=b\nabla_\phi\sum_xp_\phi(x)\\
&=b\nabla_\phi 1=0.
\end{aligned}
\]

### 隐式函数定理得到影响函数

定义加权内层目标
\[
F(\theta,w)
=F_0(\theta)+\sum_jw_j\ell_j(\theta).
\]
最优点满足
\[
G(\theta^*(w),w)
:=\nabla_\theta F(\theta^*(w),w)=0.
\]
对 \(w_j\) 求导：
\[
\frac{\partial G}{\partial\theta}
\frac{\mathrm d\theta^*}{\mathrm dw_j}
+
\frac{\partial G}{\partial w_j}
=0.
\]
其中
\[
\frac{\partial G}{\partial\theta}
=\nabla_\theta^2F=H,
\qquad
\frac{\partial G}{\partial w_j}
=\nabla_\theta\ell_j.
\]
所以
\[
\frac{\mathrm d\theta^*}{\mathrm dw_j}
=-H^{-1}\nabla_\theta\ell_j.
\]
若外层损失为 \(L(\theta^*)\)，继续链式法则：
\[
\frac{\mathrm dL}{\mathrm dw_j}
=
\nabla_\theta L^\mathsf{T}
\frac{\mathrm d\theta^*}{\mathrm dw_j}
=
-\nabla_\theta L^\mathsf{T}
H^{-1}
\nabla_\theta\ell_j.
\]

### 为什么不应显式求逆 Hessian

式子写 \(H^{-1}g_j\)，数值实现通常解线性方程
\[
Hv=g_j
\]
得到 \(v\)，再算 \(-g_{\mathrm{meta}}^\mathsf{T} v\)。显式构造 \(H^{-1}\) 更慢、更耗内存，
也更不稳定。共轭梯度、LiSSA 或自动微分 Hessian-vector product 都可避免完整逆矩阵。
