# Domain、Task 与迁移定义

## 1. Domain

\[
\mathcal D=\{\mathcal X,P(X)\}.
\]

\(\mathcal X\) 是特征空间，\(P(X)\) 是边缘分布。两个语料即便使用相同词表，也可能因主题和表达频率不同而有

\[
P_S(X)\ne P_T(X).
\]

## 2. Task

\[
\mathcal T=\{\mathcal Y,P(Y\mid X)\}.
\]

\(\mathcal Y\) 是标签空间，\(P(Y\mid X)\) 是目标预测关系。情感分类与 NLI 的标签空间和条件规律不同，属于不同 task。

## 3. Transfer learning

使用源知识改善目标学习：

\[
(\mathcal D_S,\mathcal T_S)
\longrightarrow
f_T\text{ on }\mathcal D_T.
\]

若 domain 和 task 都完全相同，就是常规同分布学习；迁移至少涉及 domain 或 task 的变化。

## 4. 为什么预训练模型属于迁移

语言模型预训练：

\[
\mathcal T_S=\text{token prediction}.
\]

下游分类：

\[
\mathcal T_T=\text{label prediction}.
\]

任务改变，且预训练通用语料与下游领域的 \(P(X)\) 常不同。预训练参数作为可迁移知识初始化目标模型。

## 5. Survey 的历史作用

论文系统整理截至 2009 年的实例、特征、参数与关系知识迁移。现代 foundation model 规模远超其案例，但基本符号仍能清楚区分“哪里不同、转移什么、何时有害”。
