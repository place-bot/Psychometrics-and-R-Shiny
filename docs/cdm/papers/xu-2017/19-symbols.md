# 符号表

## 基础对象

| 符号 | 维度或取值 | 含义 |
| --- | --- | --- |
| \(N\) | 正整数 | 被试数 |
| \(J\) | 正整数 | 题目数 |
| \(K\) | 正整数 | 二分属性数 |
| \(i\) | \(1,\ldots,N\) | 被试索引 |
| \(j\) | \(1,\ldots,J\) | 题目索引 |
| \(k\) | \(1,\ldots,K\) | 属性索引 |
| \(R_j\) | \(\{0,1\}\) | 第 \(j\) 题反应 |
| \(\boldsymbol R\) | \(\{0,1\}^J\) | 完整反应向量 |
| \(\boldsymbol r\) | \(\{0,1\}^J\) | 一个反应模式或题目子集指标 |
| \(\boldsymbol\alpha\) | \(\{0,1\}^K\) | 属性模式 |
| \(\boldsymbol0,\boldsymbol1\) | 二分向量 | 全零与全一向量 |
| \(\boldsymbol e_k\) | 单位向量 | 只含第 \(k\) 个属性的模式 |

## Q 与偏序

| 符号 | 含义 |
| --- | --- |
| \(Q\) | \(J\times K\) 题目—属性矩阵 |
| \(q_{jk}\) | 第 \(j\) 题是否要求属性 \(k\) |
| \(\boldsymbol q_j\) | Q 的第 \(j\) 行 |
| \(\boldsymbol\alpha\succeq\boldsymbol q_j\) | \(\boldsymbol\alpha\) 具备该题全部所需属性 |
| \(\boldsymbol\alpha\nsucceq\boldsymbol q_j\) | 至少缺失一项所需属性 |
| \(I_K\) | \(K\times K\) 单位矩阵 |
| \(Q'\) | C1 中两个单位块之后的剩余行 |

## 参数

| 符号 | 维度 | 含义 |
| --- | ---: | --- |
| \(\theta_{j,\boldsymbol\alpha}\) | 标量 | 类 \(\boldsymbol\alpha\) 在题 \(j\) 上的成功概率 |
| \(\Theta\) | \(J\times2^K\) | 全部项目成功概率 |
| \(p_{\boldsymbol\alpha}\) | 标量 | 属性模式 \(\boldsymbol\alpha\) 的群体比例 |
| \(\boldsymbol p\) | \(2^K\times1\) | 全部属性比例 |
| \(\bar\Theta,\bar{\boldsymbol p}\) | 同上 | 与原参数产生相同分布的候选参数 |
| \(s_j\) | 标量 | DINA/DINO slipping probability |
| \(g_j\) | 标量 | DINA/DINO guessing probability |

## 分布与矩阵

| 符号 | 含义 |
| --- | --- |
| \(\pi_{\boldsymbol r,\boldsymbol\alpha}(Q,\Theta)\) | 给定属性类时 exact response pattern 的概率 |
| \(T(Q,\Theta)\) | \(2^J\times2^K\) 边际矩阵 |
| \(t_{\boldsymbol r,\boldsymbol\alpha}\) | \(P(\boldsymbol R\succeq\boldsymbol r\mid\boldsymbol\alpha)\) |
| \(T_{\boldsymbol r,\cdot}\) | \(T\)-矩阵的 \(\boldsymbol r\) 行 |
| \(T_{\cdot,\boldsymbol\alpha}\) | \(T\)-矩阵的 \(\boldsymbol\alpha\) 列 |
| \(\odot\) | 行向量的逐元素乘积 |
| \(\widehat{\boldsymbol\gamma}\) | 全部题目子集的经验全对比例 |

## 证明工具

| 符号 | 含义 |
| --- | --- |
| \(\boldsymbol\theta^*\) | 每题一个平移常数 |
| \(\boldsymbol\theta^*\boldsymbol1^\top\) | 每行重复相应平移常数的矩阵 |
| \(D(\boldsymbol\theta^*)\) | 命题 3 的可逆下三角行变换 |
| \(\boldsymbol u_k\) | C2 产生的零类/单属性类对比行向量 |
| \(b_k\) | \(\boldsymbol u_k\) 在 \(\boldsymbol e_k\) 向量上留下的非零值 |
| \(\boldsymbol m\) | 从满秩 \(T\)-子矩阵构造的列选择器 |

## 条件与结论

| 名称 | 数学内容 |
| --- | --- |
| complete Q | Q 含一个 \(I_K\) |
| C1 | Q 含两个不重叠的 \(I_K\) |
| C2 | \(Q'\) 上每个 \(\boldsymbol e_k\) 与 \(\boldsymbol0\) 的概率向量不同 |
| strict identifiability | 相同观测分布蕴含参数逐项相同 |

## 维数速查

\[
\begin{array}{c|c}
\text{对象}&\text{维数}\\\hline
Q&J\times K\\
\Theta&J\times2^K\\
\boldsymbol p&2^K\times1\\
T(Q,\Theta)&2^J\times2^K\\
D(\boldsymbol\theta^*)&2^J\times2^J
\end{array}
\]

理论中的 \(D\) 很大，但证明只需它的代数存在性。实现时可以直接按所需题目子集构造行，无需为大型测验显式保存整个 \(2^J\times2^J\) 矩阵。
