# BOBCAT Framework：式（3）至式（11）与 Algorithm 1

## 先建立一次模拟短测

### 固定长度 n

论文研究固定长度 CAT。对学生 \(i\)，选题器总共选 \(n\) 道题：

\[
\{j_i^{(1)},j_i^{(2)},\ldots,j_i^{(n)}\}.
\]

这里 \(n\) 是短测长度，满足

\[
n\leq |\Omega_i^{(1)}|.
\]

竖线 \(|S|\) 表示集合 \(S\) 中元素的数量。因此右侧是学生 \(i\) 一开始可用的候选题数。

每选完一道题，就把它从候选集中删除：

\[
\Omega_i^{(t+1)}
=\Omega_i^{(t)}\setminus\{j_i^{(t)}\}.
\]

反斜杠表示集合差。这个更新保证同一学生不会重复收到同一道题。

### 状态向量第一次正式出现

第 \(t\) 步选题以前，BOBCAT 把学生到目前为止的作答编码成

\[
x_i^{(t)}\in\{-1,0,1\}^{Q}.
\]

粗体没有写出，但它是一个长度为 \(Q\) 的向量。第 \(j\) 个分量定义为

\[
x_{i,j}^{(t)}
=
\begin{cases}
1, & \text{题 \(j\) 此前已选且学生答对},\\
-1, & \text{题 \(j\) 此前已选且学生答错},\\
0, & \text{题 \(j\) 尚未被选择}.
\end{cases}
\]

!!! example "小例子：五题题库中的状态"
    题库有 \(Q=5\) 道题。学生先答对第 2 题，又答错第 5 题，则下一步状态为

    \[
    x_i^{(3)}=(0,1,0,0,-1).
    \]

    上标是 3，因为现在要做第 3 次选择。向量不仅保存答案，也通过零元素保存哪些题还没问。

### 为什么状态没有显式记录时间顺序

论文假定学生真实能力在一次短测期间静态。若先答第 2 题再答第 5 题，与先答第 5 题再答
第 2 题，当前已知信息相同。因此状态只记录“题号和答案”，不记录作答发生的先后时刻。
选题网络被设计为对历史题目顺序不敏感。

若测试期间有明显学习、疲劳、速度变化或提示效应，这个静态假设会失败。那时状态应加入
时间、作答时长或序列编码，响应模型也可能需要动态能力。这个扩展已经超出原论文。

### 从 logits 到可用动作分布

选题网络读取 \(x_i^{(t)}\)，对题库中每道题输出一个 logit。logit 是未归一化实数分数。
对已选题或没有历史答案的题加一个近似负无穷的 mask，然后用 softmax：

\[
\Pi(j\mid x_i^{(t)},\Omega_i^{(t)};\phi)
=
\frac{\exp(z_{i,j}^{(t)})}
{\sum_{r\in\Omega_i^{(t)}}\exp(z_{i,r}^{(t)})},
\qquad j\in\Omega_i^{(t)}.
\]

这里 \(z_{i,j}^{(t)}\) 是网络给题 \(j\) 的 logit，字母 \(r\) 只是分母中遍历候选题的
临时索引。softmax 后，所有可选题概率非负且总和为 1。

### 采样与贪心选择

概率策略可以抽样：

\[
j_i^{(t)}
\sim
\Pi(x_i^{(t)},\Omega_i^{(t)};\phi).
\]

符号 \(\sim\) 表示“从右侧分布中抽取”。也可以在部署时取最大概率题：

\[
j_i^{(t)}
=\operatorname*{arg\,max}_{j\in\Omega_i^{(t)}}
\Pi(j\mid x_i^{(t)};\phi).
\]

训练时保留随机性有助于探索和策略梯度；Approx 代码前向采用 hard argmax，反向把它近似
成 softmax。

## 响应模型中的 global 和 local

### 先把全局响应参数看成一个参数容器

论文用 \(\gamma\) 表示 global response model parameters。它可以容纳一组参数，维度
也可以与 \(\theta_i\) 不同。为了避免抽象混乱，我们把它拆成

\[
\gamma=(\psi,\mu).
\]

\(\psi\) 表示跨学生共享且内层固定的部分，例如所有题目难度或神经网络权重；
\(\mu\) 表示学生特定参数的全局初始化或先验中心。对学生 \(i\) 适应的是
\(\theta_i\)，初始值设为

\[
\theta_i^{(0)}=\mu.
\]

外层同时学习 \(\psi\) 和 \(\mu\) 时，二者都属于 \(\gamma\)。

### IRT 实例

在 1PL IRT 中，可以写

\[
g(j;\theta_i,\psi)
=\sigma(\theta_i-b_j),
\qquad
\psi=(b_1,\ldots,b_Q).
\]

题目难度 \(b_j\) 跨学生共享。内层只根据少量作答更新学生能力 \(\theta_i\)，不更新题目
难度。全局学生能力均值 \(\mu\) 作为每名新学生的初始能力。

论文为简化记号写 \(g(j;\theta_i)\)，把固定的全局题目参数隐含在 \(g\) 中。阅读时不能
因此误以为响应模型完全没有题目参数。

### 神经网络实例

神经响应模型可以接受学生嵌入 \(h_i\)，经共享网络产生对所有题的 logits：

\[
o_i=W_2\,\rho(W_1 h_i+c_1)+c_2.
\]

这里 \(h_i\) 对应局部参数，\(W_1,W_2,c_1,c_2\) 是全局共享权重与偏置，
\(\rho\) 是 ReLU 等非线性函数。第 \(j\) 个输出经 sigmoid 后给出

\[
g(j;h_i)=\sigma(o_{i,j}).
\]

内层可以只更新 \(h_i\)，共享网络固定。官方实验中的 BiNN 使用 256 维学生特定向量，
响应网络含一层 256 节点隐藏层、ReLU、dropout 和 sigmoid 输出。

### 全局与局部参数之间的正则项

少量作答不足以稳定估计高维局部参数，因此理想内层目标加入

\[
R(\gamma,\theta_i).
\]

例如一维 IRT 可用

\[
R(\gamma,\theta_i)
=\frac{\lambda}{2}(\theta_i-\mu)^2,
\]

其中 \(\lambda\geq0\) 控制局部能力偏离全局中心 \(\mu\) 的惩罚。若从概率角度看，这对应
\(\theta_i\sim N(\mu,\lambda^{-1})\) 的高斯先验负对数部分。

论文实际的 \(K\) 步 GD 版本省略显式正则项，把从全局初始化开始、只走少量步的
early stopping 视为一种隐式正则。理想式（4）给出目标定义，式（6）给出截断实现。

### model-agnostic 到底保证了什么

BOBCAT 只要求响应模型能根据题目和局部学生参数输出概率，并且内层适应与外层损失可以
求梯度。它不保证任意黑箱模型都能无修改使用。离散、不可微或计算极重的响应模型仍需要
额外估计器。model-agnostic 更准确的含义是框架不绑定某一个 IRT 方程。

## 原论文式（3）：外层到底最小化什么

### 先看一个学生

学生 \(i\) 有一个 meta 题集合 \(\Gamma_i\)。在短测选完并完成内层适应后，得到学生特定
参数 \(\theta_i^*\)。这个学生的 meta 损失定义为

\[
\mathcal L(\theta_i^*,\Gamma_i)
=
\sum_{j\in\Gamma_i}
\ell\!\left(Y_{i,j},g(j;\theta_i^*)\right).
\]

这里的 \(j\) 只是遍历 meta 集中的题。它与第 \(t\) 步选中的
\(j_i^{(t)}\) 角色不同。

若 \(\mathcal L\) 小，说明仅用少量选中题适应出的 \(\theta_i^*\) 能预测该学生更多未用于
适应的作答。

### 再对全部学生平均

BOBCAT 的外层目标是

\[
\min_{\gamma,\phi}
\frac{1}{N}\sum_{i=1}^{N}
\sum_{j\in\Gamma_i}
\ell\!\left(Y_{i,j},g(j;\theta_i^*)\right)
\equiv
\min_{\gamma,\phi}
\frac{1}{N}\sum_{i=1}^{N}
\mathcal L(\theta_i^*,\Gamma_i).
\tag{3}
\]

冒号等价符 \(\equiv\) 这里表示右侧只是把左侧内层求和缩写成
\(\mathcal L(\theta_i^*,\Gamma_i)\)。论文使用 \(:=\) 定义该缩写。

### 为什么目标里看不到被选题的训练损失

选中题的损失用于内层适应，不直接充当外层成绩。若外层也只奖励模型拟合选中题，选题器
可能挑最容易被当前模型拟合的重复题，却不能帮助预测其余题。meta 损失要求选中题带来的
学生表示具有外推价值。

### 全局响应模型和选题器如何进入式（3）

式（3）表面只写了 \(\theta_i^*\)，但应在脑中展开为

\[
\theta_i^*=\theta_i^*(\gamma,\phi).
\]

\(\gamma\) 决定全局初始化、共享响应模型与正则中心；\(\phi\) 决定选中哪些训练题。
所以更完整地写：

\[
\mathcal J(\gamma,\phi)
=\frac1N\sum_i
\mathcal L\!\left(\theta_i^*(\gamma,\phi),\Gamma_i;\gamma\right).
\]

这里 \(\mathcal J\) 是我们为整套外层目标新取的名字。最后的分号 \(\gamma\) 提醒读者：
共享题目参数等也可能直接参与 meta 预测。

### 式（3）优化的是期望还是一次抽样

若选题器是随机策略，严格的外层目标应当对可能的选题轨迹取期望：

\[
\mathcal J(\gamma,\phi)
=\frac1N\sum_i
\mathbb{E}_{j_i^{(1:n)}\sim\Pi_\phi}
\left[
\mathcal L\!\left(
\theta_i^*(\gamma,j_i^{(1:n)}),\Gamma_i
\right)
\right].
\]

论文在式（7）才把这个期望显式写出。式（3）可以看成紧凑的双层目标，随机策略的期望
依赖被留到梯度推导时展开。

## 原论文式（4）与式（5）：内层和选题

### 理想内层问题

对学生 \(i\)，短测选出 \(n\) 道题。理想的局部参数由

\[
\theta_i^*
=
\operatorname*{arg\,min}_{\theta_i}
\left[
\sum_{t=1}^{n}
\ell\!\left(
Y_{i,j_i^{(t)}},
g(j_i^{(t)};\theta_i)
\right)
+
R(\gamma,\theta_i)
\right]
\equiv
\operatorname*{arg\,min}_{\theta_i}\mathcal L_i'(\theta_i).
\tag{4}
\]

式末新定义的 \(\mathcal L_i'(\theta_i)\) 是学生 \(i\) 的内层目标。撇号用于与 meta 损失
\(\mathcal L(\theta_i^*,\Gamma_i)\) 区分。

### 逐层读求和

求和下标 \(t=1,\ldots,n\) 遍历**选题时刻**。在第 \(t\) 个时刻，实际题号是
\(j_i^{(t)}\)，从数据中读取的答案是 \(Y_{i,j_i^{(t)}}\)。响应模型对此题的预测是
\(g(j_i^{(t)};\theta_i)\)。每个已选题产生一个交叉熵，最后再加正则项。

不能把 \(t\) 与 \(j\) 互换。\(t\) 是短测中的位置，\(j\) 是题库编号。例如第 2 步可能
选到题库第 137 题，此时 \(t=2\)，\(j_i^{(2)}=137\)。

### 式（5）规定这些题从哪里来

第 \(t\) 道题由选题器根据此前作答选择：

\[
j_i^{(t)}
\sim
\Pi\!\left(
Y_{i,j_i^{(1)}},\ldots,Y_{i,j_i^{(t-1)}};\phi
\right),
\qquad
j_i^{(t)}\in\Omega_i^{(t)}.
\tag{5}
\]

论文随后用状态向量 \(x_i^{(t)}\) 实现同样信息，因此也可写成

\[
j_i^{(t)}
\sim
\Pi(x_i^{(t)},\Omega_i^{(t)};\phi).
\]

### 三个集合随流程怎样变化

对学生 \(i\)，整个 episode 中有三种题目角色。

- \(\Gamma_i\)：meta 题，整个内层过程都不允许选择。
- \(\Omega_i^{(t)}\)：第 \(t\) 步仍可选择的 training 候选题。
- \(S_i^{(t)}=\{j_i^{(1)},\ldots,j_i^{(t)}\}\)：截至第 \(t\) 步已选题。

它们满足

\[
S_i^{(t)}\subseteq\Omega_i^{(1)},\qquad
S_i^{(t)}\cap\Omega_i^{(t+1)}=\varnothing,\qquad
\Gamma_i\cap\Omega_i^{(1)}=\varnothing.
\]

### 双层依赖现在已经完整

式（5）用 \(\phi\) 产生题号；题号进入式（4）决定 \(\theta_i^*\)；\(\theta_i^*\) 进入
式（3）产生 meta 损失。用函数组合写成

\[
\phi
\xrightarrow{\Pi}
j_i^{(1:n)}
\xrightarrow{\text{inner argmin}}
\theta_i^*
\xrightarrow{\text{meta prediction}}
\mathcal L_i.
\]

!!! warning "容易误解"
    在训练数据里，\(Y_{i,j}\) 已经存在；选题器选择的是“揭示哪个已有历史答案给内层”。
    在部署时，\(Y_{i,j_i^{(t)}}\) 要等学生实际作答后才得到。训练和部署的计算接口相同，
    但答案来源不同。

## 原论文式（6）：内层真正怎样算

### 从理想最优解换成 K 步更新

算法不为每个学生把式（4）精确优化到收敛。它把可适应局部参数初始化为
全局值，然后走 \(K\) 步梯度下降。一次更新写成

\[
\theta_i
\leftarrow
\theta_i
-\alpha
\left.
\nabla_{\theta}
\sum_{\tau=1}^{t}
\ell\!\left(
Y_{i,j_i^{(\tau)}},
g(j_i^{(\tau)};\theta)
\right)
\right|_{\theta=\theta_i}.
\tag{6}
\]

为了与论文算法的序贯过程一致，这里把上限写成当前已观察的 \(t\)。论文正文展示式（6）
时用 \(n\) 表示已经用于适应的选题总数；Algorithm 1 第 7 行明确在每个选题步使用
\(\{Y_{i,j_i^{(1:t)}}\}\)。两种写法分别对应整段短测后的适应和逐步训练实现。

### 竖线右侧表示在哪里计算梯度

\[
\left.\nabla_\theta f(\theta)\right|_{\theta=\theta_i}
\]

读作：先把 \(f\) 看成关于临时变量 \(\theta\) 的函数并求梯度，再在当前
\(\theta_i\) 处取值。它不表示条件概率。

### 初始化和步数

在每个学生的适应开始时，

\[
\theta_i^{(0)}=\mu,
\]

其中 \(\mu\) 属于全局参数 \(\gamma\)。连续走 \(K\) 步：

\[
\theta_i^{(k+1)}
=U\!\left(\theta_i^{(k)};S_i^{(t)},\alpha\right),
\qquad k=0,\ldots,K-1,
\]

其中 \(U\) 只是我们给一次 GD 更新取的函数名。最终

\[
\theta_i^{(K)}
=U_K(\mu;S_i^{(t)},\alpha).
\]

实际实现中，这个 \(\theta_i^{(K)}\) 扮演理想符号 \(\theta_i^*\) 的角色。

### 为什么少走几步会像正则化

如果只有一道答对题，毫无约束地优化 1PL 能力会不断把 \(\theta_i\) 推向正无穷，使该题
答对概率趋近 1。少量 GD 步让参数仍停留在全局初始化附近。步数 \(K\) 越少、学习率
\(\alpha\) 越小，局部参数越难远离全局值。因此 early stopping 产生类似 shrinkage 的
效果。

early stopping 与显式二次正则在一般非线性模型中具有不同的数学形式。论文引用
Rajeswaran 等人的隐式梯度元学习观点，把少步适应作为计算和正则化上的实用选择
[Rajeswaran et al. (2019)](references.md#rajeswaran2019meta).

### 每次新题后重新适应还是接着适应

数学上有两种实现。

1. 每到第 \(t\) 步，都从同一全局初始化 \(\mu\) 出发，对前 \(t\) 个观测走 \(K\)
    步。这样每次的适应映射清晰、与 MAML task adaptation 一致。
1. 保留上一步局部参数，再用新题增量更新。这样测试时更便宜，但计算图和隐式正则
    不同。

论文描述强调从 \(\gamma\) 取 \(K\) 步，官方训练代码为每批次维护可适应 meta parameter，
再对所选 mask 的训练损失更新。复现时应以具体代码路径为准，并明确是否重置。

### 一维 IRT 的两步演示

取 \(\mu=0\)，题难 \(b=0\)，学生答对 \(y=1\)，学习率 \(\alpha=0.4\)。
第一步已经算过：

\[
\theta^{(1)}=0.2.
\]

第二步先算新概率

\[
p^{(1)}=\sigma(0.2)\approx0.5498,
\]

梯度为 \(p^{(1)}-1=-0.4502\)，于是

\[
\theta^{(2)}
=0.2-0.4(-0.4502)
\approx0.3801.
\]

每一步都重新在当前参数处计算概率和梯度，不能把第一步梯度重复使用两次。

## 怎样更新全局响应模型

### 外层希望初始化适合快速个体化

对一个 mini-batch 学生集合 \(\mathcal B\)，外层响应模型更新为

\[
\gamma
\leftarrow
\gamma
-\frac{\eta_1}{|\mathcal B|}
\sum_{i\in\mathcal B}
\nabla_\gamma
\mathcal L\!\left(
\theta_i^{(K)}(\gamma,\phi),\Gamma_i
\right).
\]

\(\mathcal B\) 是当前小批次学生，\(|\mathcal B|\) 是批次人数，
\(\eta_1\) 是外层响应模型学习率。

这个更新让“从 \(\gamma\) 出发适应后的局部参数”在 meta 题上取得较低损失；选中训练题
通过内层适应间接影响该目标。

### 精确 meta-gradient 穿过 K 步

先只看适应初始化 \(\mu\)。第 \(k\) 步内层 Hessian 记为

\[
H_i^{(k)}
=\nabla_\theta^2
\mathcal L_i^{\mathrm{inner}}(\theta_i^{(k)}).
\]

对初始化的 Jacobian 递推为

\[
\frac{\partial\theta_i^{(k+1)}}{\partial\mu}
=
\left(I-\alpha H_i^{(k)}\right)
\frac{\partial\theta_i^{(k)}}{\partial\mu}.
\]

初始 Jacobian 为 \(I\)，所以

\[
\frac{\partial\theta_i^{(K)}}{\partial\mu}
=
\prod_{k=0}^{K-1}
\left(I-\alpha H_i^{(k)}\right),
\]

乘积顺序按计算图从后向前理解。meta-gradient 是

\[
\nabla_\mu\mathcal L_i^{\mathrm{meta}}
=
\left(
\frac{\partial\theta_i^{(K)}}{\partial\mu}
\right)^{\mathsf{T}}
\nabla_{\theta_i^{(K)}}\mathcal L_i^{\mathrm{meta}}.
\]

### 一阶近似

若把每个 \(I-\alpha H_i^{(k)}\) 近似为 \(I\)，就得到

\[
\nabla_\mu\mathcal L_i^{\mathrm{meta}}
\approx
\nabla_{\theta_i^{(K)}}\mathcal L_i^{\mathrm{meta}}.
\]

直觉上，它让全局初始化朝“适应后参数应当移动的方向”更新，却忽略初始化变化对内层
梯度路径的二阶影响。

### 共享题目参数的直接和间接梯度

若 \(\gamma\) 还含共享参数 \(\psi\)，例如题目难度和神经网络权重，meta 预测
\(g(j;\theta_i,\psi)\) 直接依赖 \(\psi\)。内层适应梯度也可能依赖 \(\psi\)。因此

\[
\frac{\mathrm d\mathcal L_i}{\mathrm d\psi}
=
\underbrace{\frac{\partial\mathcal L_i}{\partial\psi}}_{\text{直接改变 meta 预测}}
+
\underbrace{
\frac{\partial\mathcal L_i}{\partial\theta_i^{(K)}}
\frac{\partial\theta_i^{(K)}}{\partial\psi}
}_{\text{改变内层适应结果}}.
\]

实际实现选择哪些参数允许内层更新、哪些只在外层更新，是模型设计的一部分。

## 原论文式（7）：选题器梯度为何困难

### 把整条选题序列当作随机变量

简写

\[
j_i^{(1:n)}
=\left(j_i^{(1)},\ldots,j_i^{(n)}\right),
\]

表示学生 \(i\) 的整条选题序列。由于每一步都从策略中抽样，这个序列是离散随机变量。
给定它以后，内层适应结果可写成

\[
\theta_i^*(\gamma,j_i^{(1:n)}).
\]

对一个学生，策略参数的目标梯度是

\[
\nabla_\phi
\mathcal L\!\left(\theta_i^*(\gamma,\phi),\Gamma_i\right)
=
\nabla_\phi
\mathbb{E}_{j_i^{(1:n)}\sim\Pi(\cdot;\phi)}
\left[
\mathcal L\!\left(
\theta_i^*(\gamma,j_i^{(1:n)}),\Gamma_i
\right)
\right].
\tag{7}
\]

### 为什么不能对题号求普通导数

若策略输出概率向量 \((0.2,0.5,0.3)\)，抽样结果可能是题号 2。将某个网络权重稍微改变，
概率会连续变化成 \((0.21,0.49,0.30)\)，但抽到的离散题号不会以“2.01”的方式连续变化。
题号对参数没有普通意义下的局部导数。

因此链条

\[
\phi\to\text{概率}\to\text{离散题号}\to\theta_i^*\to\mathcal L_i
\]

在“概率到离散题号”处断开。式（7）的后续工作就是为这处断点构造梯度估计。

### 两条路线的总览

**表：BOBCAT 的两种选题器梯度**

| 比较项 | 无偏估计，式（8） | 近似估计，式（9）至式（11） |
| --- | --- | --- |
| 核心工具 | score-function / REINFORCE | 连续权重松弛、隐式微分、影响函数、straight-through |
| 利用哪些候选题 | 主要由实际选中轨迹提供信号 | 可以让当前所有可用训练题提供梯度信号 |
| 统计性质 | 期望等于目标梯度，但方差可很大 | 有偏，不保证等于精确梯度，经验方差较低 |
| 官方实现 | actor-critic 与 PPO | hard sample 前向、softmax 梯度反向 |

!!! warning "容易误解"
    “无偏”只说明在正确采样和期望下，梯度估计的平均值等于目标梯度。它不说明单次估计
    接近真梯度，也不说明训练一定更快。高方差无偏估计在有限训练预算下可能比稳定的有偏
    估计表现更差。

## 原论文式（8）：无偏策略梯度

### 先从有限动作的期望开始

暂时只选一道题。令题 \(j\) 被选的概率为 \(\Pi_\phi(j)\)，选后得到的 meta 损失为
\(L(j)\)。期望损失是

\[
\mathbb{E}[L]
=\sum_j \Pi_\phi(j)L(j).
\]

假设 \(L(j)\) 给定离散动作后不直接含 \(\phi\)，求导：

\[
\nabla_\phi\mathbb{E}[L]
=\sum_j \nabla_\phi\Pi_\phi(j)L(j).
\]

利用

\[
\nabla_\phi\Pi_\phi(j)
=\Pi_\phi(j)\nabla_\phi\log\Pi_\phi(j),
\]

得到

\[
\nabla_\phi\mathbb{E}[L]
=
\sum_j\Pi_\phi(j)L(j)\nabla_\phi\log\Pi_\phi(j)
=
\mathbb{E}\!\left[L(j)\nabla_\phi\log\Pi_\phi(j)\right].
\]

### 多步轨迹的概率为何是连乘

第 \(t\) 步动作概率条件于当前状态。整条轨迹的策略概率为

\[
p_\phi(j_i^{(1:n)})
=
\prod_{t=1}^{n}
\Pi\!\left(
j_i^{(t)}\mid x_i^{(t)};\phi
\right).
\]

取对数，连乘变求和：

\[
\log p_\phi(j_i^{(1:n)})
=
\sum_{t=1}^{n}
\log
\Pi\!\left(
j_i^{(t)}\mid x_i^{(t)};\phi
\right).
\]

再求梯度：

\[
\nabla_\phi\log p_\phi(j_i^{(1:n)})
=
\sum_{t=1}^{n}
\nabla_\phi
\log\Pi\!\left(
j_i^{(t)}\mid x_i^{(t)};\phi
\right).
\]

### 把 baseline 加进去

于是式（8）为

\[
\begin{aligned}
&\nabla_\phi
\mathbb{E}_{j_i^{(1:n)}\sim\Pi_\phi}
\left[
\mathcal L(\theta_i^*,\Gamma_i)
\right]
\\
&\quad=
\mathbb{E}\left[
\left(\mathcal L(\theta_i^*,\Gamma_i)-b_i\right)
\nabla_\phi
\log\prod_{t=1}^{n}
\Pi\!\left(j_i^{(t)}\mid x_i^{(t)};\phi\right)
\right]
\\
&\quad=
\mathbb{E}\left[
\left(\mathcal L(\theta_i^*,\Gamma_i)-b_i\right)
\sum_{t=1}^{n}
\nabla_\phi
\log
\Pi\!\left(j_i^{(t)}\mid x_i^{(t)};\phi\right)
\right].
\end{aligned}
\tag{8}
\]

### 损失低于 baseline 时为什么提高概率

设某条轨迹损失小于基线，所以
\(\mathcal L-b_i<0\)。训练最小化损失，参数更新为

\[
\phi\leftarrow\phi-\eta_2\widehat{\nabla_\phi\mathcal J}.
\]

估计梯度含一个负系数乘 \(\nabla_\phi\log\Pi\)。减去该梯度等于沿
\(+\nabla_\phi\log\Pi\) 移动，因此增加这条轨迹中动作的 log 概率。若损失高于基线，
方向相反。

### 为什么方差大

一次采样只告诉算法“抽到的这条轨迹结果如何”。没有抽到的题对本次 REINFORCE 梯度
没有直接贡献。更麻烦的是，终点 meta 损失同时归因给 \(n\) 个动作，很难分辨哪一步
真正有用。动作空间 \(Q\) 大、轨迹长度 \(n\) 增加时，可能轨迹数迅速膨胀。

### critic 估计什么

actor 是策略网络，输出动作概率。critic 读取状态并预测从该状态继续选择后可能得到的
损失或回报。这个预测可用作 \(b_i\) 或更细的状态相关 baseline。优势量可写为

\[
A_t=R-V(x_i^{(t)}),
\]

其中 \(V\) 是 critic 估计的价值。论文官方代码把同一个终点结果复制给多个动作时刻，
再用 critic 值形成 advantage，并使用 PPO 截断更新。

## 原论文式（9）至式（11）：近似梯度

### 第一步是普通链式法则

meta 损失对 \(\phi\) 的影响通过局部参数传递：

\[
\nabla_\phi
\mathcal L(\theta_i^*(\gamma,\phi),\Gamma_i)
=
\nabla_{\theta_i^*}
\mathcal L(\theta_i^*,\Gamma_i)
\,
\nabla_\phi\theta_i^*(\gamma,\phi).
\tag{9}
\]

第一因子回答“局部参数改变一点，meta 损失怎样变”；第二因子回答“策略改变一点，局部
参数怎样变”。困难集中在第二因子。

### 把一次离散选择写成 one-hot 权重

在第 \(t\) 步，对每个当前可用题 \(j\in\Omega_i^{(t)}\) 定义

\[
w_j=
\begin{cases}
1,&j=j_i^{(t)},\\
0,&j\neq j_i^{(t)}.
\end{cases}
\]

于是本步只有被选题进入内层损失。把此前 \(t-1\) 道题与当前选择分开：

\[
\begin{aligned}
\theta_i^*
=\operatorname*{arg\,min}_{\theta_i}\Bigg[
&\sum_{\tau=1}^{t-1}
\ell\!\left(
Y_{i,j_i^{(\tau)}},
g(j_i^{(\tau)};\theta_i)
\right)
+R(\gamma,\theta_i)
\\
&+
\sum_{j\in\Omega_i^{(t)}}
w_j(\phi)\,
\ell\!\left(Y_{i,j},g(j;\theta_i)\right)
\Bigg].
\end{aligned}
\tag{10}
\]

第二行虽然对所有候选题求和，但 one-hot \(w_j\) 使前向数值只保留一题。这种写法的价值
是可以追问：若把某道题的权重从 0 稍微增加，内层最优解和 meta 损失会怎样变化？

### 隐式求局部最优参数对题目权重的导数

把式（10）括号内的整体记为 \(\mathcal L_i'(\theta_i,w)\)。最优点满足

\[
\nabla_{\theta_i}\mathcal L_i'(\theta_i^*,w)=0.
\]

对 \(w_j\) 求导：

\[
\nabla_{\theta_i}^2\mathcal L_i'
\frac{\mathrm d\theta_i^*}{\mathrm dw_j}
+
\nabla_{\theta_i}
\ell\!\left(Y_{i,j},g(j;\theta_i^*)\right)
=0.
\]

若 Hessian 可逆，

\[
\frac{\mathrm d\theta_i^*}{\mathrm dw_j}
=-
\left(\nabla_{\theta_i}^2\mathcal L_i'\right)^{-1}
\nabla_{\theta_i}
\ell\!\left(Y_{i,j},g(j;\theta_i)\right)
\Big|_{\theta_i=\theta_i^*}.
\]

### 三个向量如何相乘

设 \(\theta_i\) 是 \(d\) 维列向量。

- meta 梯度 \(\nabla_{\theta_i}\mathcal L(\theta_i,\Gamma_i)\) 可看成 \(d\) 维列向量；
- Hessian 是 \(d\times d\) 矩阵；
- 候选题梯度 \(\nabla_{\theta_i}\ell_{i,j}\) 是 \(d\) 维列向量。

为了得到标量影响分数，应写成

\[
-\nabla_{\theta_i}\mathcal L(\theta_i,\Gamma_i)^{\mathsf{T}}
\left(\nabla_{\theta_i}^2\mathcal L_i'\right)^{-1}
\nabla_{\theta_i}\ell_{i,j}.
\]

论文省略了转置符号，按行梯度记号理解。

### 影响函数分数

把局部最优参数对题目权重的导数代入链式法则，得到

\[
\mathcal I_i(j)
:=
-
\nabla_{\theta_i}\mathcal L(\theta_i,\Gamma_i)^{\mathsf{T}}
\left(\nabla_{\theta_i}^2\mathcal L_i'\right)^{-1}
\nabla_{\theta_i}
\ell\!\left(Y_{i,j},g(j;\theta_i)\right)
\Big|_{\theta_i=\theta_i^*}.
\tag{11}
\]

新符号 \(\mathcal I_i(j)\) 是题 \(j\) 对学生 \(i\) 的 influence score。它近似表示把题
\(j\) 在内层中的权重稍微增加，会让 meta 损失怎样变化：

\[
\mathcal I_i(j)
\approx
\frac{\partial
\mathcal L(\theta_i^*,\Gamma_i)}
{\partial w_j}.
\]

若 \(\mathcal I_i(j)<0\)，稍微加大这道题的内层权重会降低 meta 损失，通常是好信号。
若为正，则会提高 meta 损失。

### “梯度相似”为什么还隔着逆 Hessian

若忽略曲率，两个梯度内积为负或正可以表示方向是否一致。但参数空间不同方向的尺度和
曲率不同。逆 Hessian 对候选题梯度做预条件，近似换算“该梯度真正会把最优参数推到哪里”。
因此影响函数包含 gradient alignment 与局部曲率两部分信息。

一维时最直观：

\[
\mathcal I_i(j)
=-
\frac{
g_{\mathrm{meta}}\,
g_{j}
}{H},
\]

其中 \(g_{\mathrm{meta}}\) 是 meta 损失对能力的导数，\(g_j\) 是候选题损失梯度，
\(H>0\) 是内层曲率。若两梯度同号，增加题 \(j\) 的权重会沿负梯度方向移动参数，从而
降低 meta 损失，所以影响分数为负。

### 从 one-hot 到概率的近似

\(w_j\) 仍是离散 one-hot。论文用

\[
w_j(\phi)
\approx
\Pi(j\mid x_i^{(t)};\phi)
\]

替代它。于是近似策略梯度为

\[
\nabla_\phi\mathcal L_i
\approx
\sum_{j\in\Omega_i^{(t)}}
\mathcal I_i(j)
\nabla_\phi
\Pi(j\mid x_i^{(t)};\phi).
\]

现在所有可用题都可以贡献梯度，而不只抽中的题。

### straight-through 如何让前向硬、反向软

官方代码先算 softmax 概率 \(y_{\mathrm{soft}}\)，再取最大项生成 one-hot
\(y_{\mathrm{hard}}\)，然后构造

\[
y
=y_{\mathrm{hard}}
-\operatorname{stopgrad}(y_{\mathrm{soft}})
+y_{\mathrm{soft}}.
\]

前向计算时，后两项数值抵消，所以 \(y=y_{\mathrm{hard}}\)。反向求导时，
\(\operatorname{stopgrad}\) 的导数是 0，而最后一项保留 softmax 导数，所以

\[
\frac{\partial y}{\partial\phi}
\approx
\frac{\partial y_{\mathrm{soft}}}{\partial\phi}.
\]

这就是 straight-through estimator 的典型实现
[Bengio et al. (2013)](references.md#bengio2013estimating)。

### 为什么它有偏

真实前向函数在 argmax 边界之外对参数几乎处处不变，真实局部导数通常为 0；反向却故意
使用 softmax 的非零导数。因此估计不等于真实离散算子的导数。它优化的是一个人为设计的
surrogate gradient。经验上，低方差和所有候选题的密集信号可能抵消偏差带来的问题。

!!! warning "容易误解"
    式（11）严格使用内层最优点和可逆 Hessian 的影响函数推导，而代码又采用有限步内层适应
    和 straight-through 自动微分。二者在思想上相连，但不能把代码梯度称为式（11）的精确
    数值实现。复现论文时应把“理论近似”和“工程近似”分别记录。

## Algorithm 1 的完整计算顺序

### 先列出三种学习率

算法初始化三种学习率。

- \(\alpha\)：学生局部参数的内层学习率，出现在式（6）。
- \(\eta_1\)：全局响应模型参数 \(\gamma\) 的外层学习率。
- \(\eta_2\)：选题器参数 \(\phi\) 的外层学习率。

三者控制不同变量，数值不必相同。官方仓库给出的搜索范围中，inner learning rate 大约
在 \(0.05,0.1,0.2\)，meta response learning rate 为 \(10^{-4}\)，policy learning
rate 在 \(2\times10^{-4}\) 或 \(2\times10^{-3}\) 附近。这些数值是论文实现的搜索范围，
换用数据集时需要重新调参。

### 一个 outer iteration

下面把一次外层训练迭代拆成可执行动作。设 mini-batch 为 \(\mathcal B\)。

#### 步骤 1：为每个学生建立两个题集

对每个 \(i\in\mathcal B\)，从该学生已观测题中划分

\[
\Omega_i^{(1)}\quad\text{和}\quad\Gamma_i,
\]

前者是 training 候选集，后者是 meta 集。二者不相交。

#### 步骤 2：清空短测状态

令

\[
x_i^{(1)}=\bm 0,\qquad S_i^{(0)}=\varnothing.
\]

局部适应参数初始化为全局适应块：

\[
\theta_i^{(0)}=\mu.
\]

#### 步骤 3：进入第 \(t\) 个选题时刻

对于 \(t=1,\ldots,n\)，对每个学生做：

1. 把当前状态 \(x_i^{(t)}\) 输入选题器；
1. 对不可用题 mask，得到可用题概率；
1. 抽样或 hard 选择 \(j_i^{(t)}\)；
1. 从历史矩阵读取 \(Y_{i,j_i^{(t)}}\)；
1. 更新已选集合、候选集合与状态向量；
1. 用截至当前的已选作答，对 \(\theta_i\) 走 \(K\) 步内层 GD；
1. 用 \(\theta_i^{(K)}\) 在 \(\Gamma_i\) 上计算 meta 损失。

#### 步骤 4：更新选题器

选择下列一种梯度：

\[
\widehat g_{\phi,i}^{\mathrm{unbiased}}
=
\left(\mathcal L_i-b_i\right)
\sum_{\tau=1}^{t}
\nabla_\phi\log
\Pi(j_i^{(\tau)}\mid x_i^{(\tau)};\phi),
\]

或者

\[
\widehat g_{\phi,i}^{\mathrm{approx}}
\approx
\sum_{j\in\Omega_i^{(t)}}
\mathcal I_i(j)\nabla_\phi
\Pi(j\mid x_i^{(t)};\phi).
\]

再对批次平均：

\[
\phi
\leftarrow
\phi-\frac{\eta_2}{|\mathcal B|}
\sum_{i\in\mathcal B}\widehat g_{\phi,i}.
\]

论文 Algorithm 1 把 \(\phi\) 更新放在每个选题步内部。这让策略逐步学习各阶段该选什么。
实现若在完整 \(n\) 步后统一更新，也必须正确保存各步计算图或轨迹。

#### 步骤 5：更新全局响应模型

完成 \(n\) 个选题步以后，计算

\[
\gamma
\leftarrow
\gamma
-\frac{\eta_1}{|\mathcal B|}
\sum_{i\in\mathcal B}
\nabla_\gamma
\mathcal L(\theta_i^{(K)}(\gamma,\phi),\Gamma_i).
\]

然后进入下一批学生，直到验证指标不再改善或达到训练预算。

### 伪代码

**代码：与论文符号一致的概念伪代码**

```python
initialize global response parameters gamma
initialize policy parameters phi

while not converged:
    B = sample_student_minibatch()

    for each student i in B:
        Omega[i], Gamma[i] = split_observed_items(i)
        state[i] = zeros(Q)
        selected[i] = empty_set()

    for t in 1,...,n:
        for each student i in B:
            probs = policy(state[i], available=Omega[i], phi=phi)
            item = sample_or_hard_select(probs)
            answer = historical_response[i, item]
            selected[i].add(item)
            Omega[i].remove(item)
            state[i][item] = +1 if answer == 1 else -1

            theta_i = initialize_from(gamma)
            theta_i = K_gradient_steps(
                selected_responses=selected[i],
                learning_rate=alpha
            )
            meta_loss_i = loss(theta_i, Gamma[i])

        policy_gradient = unbiased_or_approximate_gradient()
        phi = phi - eta2 * average(policy_gradient)

    response_meta_gradient = differentiate_meta_loss_through_adaptation()
    gamma = gamma - eta1 * average(response_meta_gradient)
```

### 张量级数据流

若批次大小为 \(B=|\mathcal B|\)，题数为 \(Q\)，局部参数维度为 \(d\)，常见张量形状是

\[
\begin{array}{c|c}
\text{对象} & \text{形状}\\ \hline
\text{状态矩阵 }X^{(t)} & B\times Q\\
\text{可用题 mask} & B\times Q\\
\text{策略 logits 与概率} & B\times Q\\
\text{每人动作题号} & B\\
\text{局部参数矩阵 }\Theta & B\times d\\
\text{响应模型对全部题的 logits} & B\times Q\\
\text{meta mask} & B\times Q
\end{array}
\]

官方代码用 mask 把不同学生拥有的 training/meta 题压进统一 \(B\times Q\) 矩阵，再用
逐元素 binary cross-entropy 和 mask 求和。

### 训练时和部署时的计算差别

**表：训练与部署的输入和计算**

| 比较项 | 训练阶段 | 新学生部署阶段 |
| --- | --- | --- |
| 答案来源 | 历史响应矩阵，模拟选题后读取 | 学生实际作答后实时获得 |
| 是否有 meta 答案 | 有，用于外层损失 | 通常没有，也不需要 |
| 是否更新 \(\gamma,\phi\) | 是 | 通常固定 |
| 是否必须更新 \(\theta_i\) 才能选下一题 | 论文称学习后的 \(\Pi\) 可直接由状态选题 | 若还需最终能力报告，可另行更新局部参数 |
| 主要成本 | 双层反向传播、策略学习 | 一次策略网络前向传播 |

### 为什么论文说测试时更快

传统 IRT-Active 每答一道题都要更新当前能力估计，再对大量候选题计算信息。BOBCAT
部署选题时只把状态向量输入已训练的 \(\Pi\)，一次前向传播即可得到下一题。训练成本被
提前支付。若系统仍要报告 IRT 能力，局部估计步骤仍可能需要，但它不再是选题器每次
决策的必经输入。

!!! tip "读到这里应当记住"
    一次训练迭代有三种参数运动：\(\theta_i\) 在内层按 \(\alpha\) 为每个学生适应；
    \(\phi\) 按 \(\eta_2\) 学怎样选题；\(\gamma\) 按 \(\eta_1\) 学一个能快速适应并预测
    meta 题的全局响应模型。
