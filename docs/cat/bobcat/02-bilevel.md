# BOBCAT 的双层优化

## 先把 level 和 optimization 分开理解

### level 是决策层级

bilevel optimization 直译为双层优化。bi 表示 two，level 表示层级。一个双层问题包含
两个优化任务，外层任务选择一个决策，内层任务在给定外层决策以后做出自己的最优反应。
外层必须预见这个反应，才能知道自己的决策好不好。

最一般的无约束形式可以写成

\[
\begin{aligned}
\min_{u}\quad &F(u,v^*(u)), \\
\text{subject to}\quad
&v^*(u)\in\operatorname*{arg\,min}_v f(u,v).
\end{aligned}
\]

现在只引入四个对象。

- \(u\) 是外层选择的变量。
- \(v\) 是内层选择的变量。
- \(f(u,v)\) 是内层目标函数。
- \(F(u,v)\) 是外层目标函数。

符号 \(v^*(u)\) 强调内层最优解依赖 \(u\)。星号表示“内层求解后得到的值”，括号中的
\(u\) 表示它是 \(u\) 的函数。把这个函数代入外层以后，外层实际优化的是复合函数
\[
\widetilde F(u)=F(u,v^*(u)).
\]

### 为什么不能把两个损失直接相加

一个常见误解是把双层问题改写成
\[
\min_{u,v} F(u,v)+f(u,v).
\]
这个相加问题改变了原目标。相加形式允许外层和内层同时妥协；双层形式要求内层对于给定
的 \(u\) 先遵守自己的最优性条件。外层只能在“内层会怎样反应”的前提下优化。

!!! example "小例子：超参数选择是最容易理解的双层问题"
    令 \(u=\lambda\) 是正则化强度，\(v=w\) 是模型权重。内层在训练集上拟合
    \[
    w^*(\lambda)=\operatorname*{arg\,min}_w
    \left\{L_{\mathrm{train}}(w)+\lambda\|w\|_2^2\right\}.
    \]
    外层在验证集上选 \(\lambda\)：
    \[
    \min_\lambda L_{\mathrm{valid}}(w^*(\lambda)).
    \]
    验证损失的好坏必须在“用该 \(\lambda\) 训练出的 \(w^*(\lambda)\)”上评价。若把训练
    损失与验证损失简单相加，就改变了训练和验证的角色。

### BOBCAT 中谁对应 u，谁对应 v

在 BOBCAT 中，外层变量是一组全局量：
\[
u=(\gamma,\phi).
\]
\(\gamma\) 是全局响应模型参数，\(\phi\) 是选题器参数。内层变量是每个学生的局部参数：
\[
v=\{\theta_1,\ldots,\theta_N\}.
\]
给定 \(\gamma\) 与 \(\phi\)，选题器先决定每个学生看到哪些训练题，内层再根据这些作答
得到 \(\theta_i^*(\gamma,\phi)\)。外层用 meta 题判断这些局部参数好不好。

### 为什么局部最优参数同时依赖全局响应模型和选题器

依赖 \(\gamma\) 容易理解：局部参数从全局初始化出发，或者被正则项拉向全局值。依赖
\(\phi\) 稍隐蔽：内层损失使用哪些作答，是选题器决定的。即使 \(\phi\) 没有直接写进
响应概率 \(g(j;\theta_i)\)，它也通过选中的题号改变内层训练数据。

可把依赖链写成
\[
\phi
\longrightarrow
\{j_i^{(1)},\ldots,j_i^{(n)}\}
\longrightarrow
\mathcal L_i^{\mathrm{inner}}
\longrightarrow
\theta_i^*
\longrightarrow
\mathcal L_i^{\mathrm{meta}}.
\]
外层训练 \(\phi\) 的梯度必须沿这条链返回。

### leader-follower 是理解嵌套结构的比喻

双层规划有时用 leader-follower 博弈解释：leader 先做决策，follower 再最优反应。
BOBCAT 没有两个有独立利益的真实行动者。这里的“内层”是学生参数适应算法，“外层”
是全局训练准则。leader-follower 只帮助理解嵌套结构，不应引出学生在与系统博弈的误解。

## 双层问题怎么求导

### 真正困难的是 solution map

回到一般形式
\[
\widetilde F(u)=F(u,v^*(u)).
\]
对 \(u\) 求导时，链式法则给出

\[
\frac{\mathrm d\widetilde F}{\mathrm du}
=
\frac{\partial F}{\partial u}
+
\frac{\partial F}{\partial v^*}
\frac{\mathrm dv^*}{\mathrm du}.
\]

第一项是外层目标对 \(u\) 的直接依赖。第二项经过
\(\mathrm dv^*/\mathrm du\)，描述外层变量怎样改变内层最优解，再怎样影响外层损失。
整个导数常叫 hypergradient 或 meta-gradient。

### 路线一：展开有限步优化

若内层采用从 \(v^{(0)}(u)\) 出发的 \(K\) 步截断优化，
\[
v^{(k+1)}
=v^{(k)}-\alpha\nabla_v f(u,v^{(k)}),
\]
就可以把 \(K\) 步全部保留在计算图中，然后反向传播。这叫 unrolling 或
differentiating through optimization。

它的优点是概念直接，也与实际 \(K\) 步适应严格一致。缺点是需要保存中间状态，并可能
计算二阶导数。若 \(K\) 大，内存和时间都变重。

### 路线二：用内层最优性条件隐式求导

若 \(v^*(u)\) 真正满足内层一阶条件
\[
\nabla_v f(u,v^*(u))=0,
\]
对 \(u\) 求导：
\[
\nabla^2_{vv} f\,
\frac{\mathrm dv^*}{\mathrm du}
+
\nabla^2_{vu}f=0.
\]
若 Hessian \(\nabla^2_{vv} f\) 可逆，

\[
\frac{\mathrm dv^*}{\mathrm du}
=-
\left(\nabla^2_{vv}f\right)^{-1}
\nabla^2_{vu}f.
\]

这叫 implicit differentiation。它可以省去漫长优化轨迹的保存，同时需要解一个涉及
Hessian 的线性系统。实际中通常通过 Hessian-vector product 或线性方程
\(Hz=q\) 完成计算。

### BOBCAT 同时借用了两种思路

对于全局响应模型参数 \(\gamma\)，论文按 MAML 思路对少量内层 GD 步反向传播，并使用
一阶近似降低计算量。对于 Approx 选题器梯度，论文为了评价当前所有候选题的影响，使用
内层最优性条件和影响函数，式（11）中出现逆 Hessian。

官方 PyTorch 实现又用 straight-through 构造硬选题的前向传播和 softmax 的反向传播。
因此应区分三个层次：

1. 数学框架中的精确 argmin；
1. 论文推导中的截断 GD、隐式影响函数和梯度近似；
1. 代码中可高效运行的自动微分实现。

### first-order approximation 丢掉了什么

设一层适应为
\[
v'=u-\alpha\nabla f(u).
\]
精确 Jacobian 是
\[
\frac{\partial v'}{\partial u}
=I-\alpha\nabla^2f(u).
\]
first-order MAML 近似把它当作 \(I\)。于是外层梯度近似为
\[
\nabla_u F(v')\approx\nabla_{v'}F(v').
\]
它忽略了“改变初始化会怎样改变内层梯度方向”的曲率信息。近似更便宜，但不等于精确
双层梯度。

!!! warning "容易误解"
    “first-order”不表示响应模型是一阶 IRT，也不表示只走一步 GD。它表示在 meta-gradient
    中忽略某些二阶导数项。内层仍可走 \(K>1\) 步，响应模型也可为深度网络。

## 训练集、验证集、meta 集为何容易混

### 存在两个不同维度的数据划分

BOBCAT 实验至少有两类划分，不能混为一个。

1. **按学生划分**：学生被分成训练学生、验证学生和测试学生，用于评价对新学生
    的泛化。论文采用五折交叉验证，在每折中按 \(60%/20%/20%\) 划分学生。
1. **对每个学生按题划分**：该学生已作答的题再分为 training candidate 集和
    meta 集。论文训练时约按 \(80%/20%\) 划分，并在每个 epoch 重新随机产生。

第一种划分回答“策略能否泛化到没参加训练的新学生”。第二种划分制造双层任务：
training candidate 题用于模拟短测和内层适应，meta 题用于外层评价。

### 为什么 meta 题不能参与内层适应

若先用 meta 题答案更新学生参数，再在同一批题上评价预测，就会产生信息泄漏。外层损失
可能很低，却不能说明少量选题对未见题有预测力。让 training 与 meta 集不相交，保证
外层问的是“由选中训练题学到的学生表示，能否迁移到另一批题”。

### meta 不等于最终 test

meta 题是每个训练学生内部用于外层学习的 held-out 题。最终 test students 完全独立于
全局参数学习。训练过程可以反复使用训练学生的 meta 题更新 \(\gamma\) 和 \(\phi\)，
因此这些 meta 题属于训练监督数据。

```text
全部历史学生
├── 训练学生
│   ├── 学生内 training 候选题
│   └── 学生内 meta 题
├── 验证学生
└── 测试学生
```

### 稀疏响应矩阵时的实际集合

理论上题库有 \(Q\) 道题，但学生 \(i\) 可能只作答一个子集，记为
\[
\mathcal O_i=\{j:Y_{i,j}\text{ 被观测}\}.
\]
BOBCAT 对该学生的初始候选集 \(\Omega_i^{(1)}\) 和 meta 集 \(\Gamma_i\) 都从
\(\mathcal O_i\) 中产生，并要求
\[
\Omega_i^{(1)}\cap\Gamma_i=\varnothing.
\]
这里 \(\Gamma\) 读作 Gamma。它专门表示 meta 题集合。集合上标 \((1)\) 说明
\(\Omega_i^{(1)}\) 是选任何题之前的初始可选集合。

!!! tip "读到这里应当记住"
    按学生划分用于检验新学生泛化；每名学生内部按题划分用于构造双层任务。meta 题留作
    外层评价并参与外层参数更新；最终测试集由独立的 test students 构成。
