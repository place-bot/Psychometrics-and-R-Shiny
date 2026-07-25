# 符号表

| 符号 | 含义 |
| --- | --- |
| \(N\) | 学生数 |
| \(J\) | 题目数 |
| \(K\) | 属性总数 |
| \(j\) | 题目索引 |
| \(i\) | 学生索引 |
| \(l\) | 完整属性模式索引 |
| \(Y_{ij}\) | 学生 \(i\) 对题目 \(j\) 的二分反应 |
| \(\boldsymbol\alpha_l\) | 第 \(l\) 个完整属性模式 |
| \(\alpha_{lk}\) | 模式 \(l\) 对属性 \(k\) 的掌握状态 |
| \(\boldsymbol q_j\) | Q 矩阵第 \(j\) 行 |
| \(q_{jk}\) | 题目 \(j\) 是否需要属性 \(k\) |
| \(K_j^*\) | 题目 \(j\) 所需属性数 |
| \(\boldsymbol\alpha^*_{lj}\) | 题目 \(j\) 的约化属性模式 |
| \(\delta_{j0}\) | identity-link G-DINA 截距 |
| \(\delta_{jk}\) | 属性主效应 |
| \(\delta_{jkk'}\) | 属性交互效应 |
| \(P_j(\boldsymbol\alpha)\) | 模式 \(\boldsymbol\alpha\) 对题目 \(j\) 的成功概率 |
| \(w_i(\boldsymbol\alpha)\) | 学生 \(i\) 的属性模式后验 |
| \(w(\boldsymbol\alpha)\) | 总体属性模式权重 |
| \(p_j(\boldsymbol\alpha)\) | 完整模式条件成功概率 |
| \(\bar p_j\) | 题目总体加权成功率 |
| \(\varsigma_j^2(\boldsymbol q)\) | 候选 q-vector 的 GDI |
| \(\widehat{\varsigma}_j^2\) | 样本估计 GDI |
| \(\operatorname{PVAF}_j(\boldsymbol q)\) | 候选 GDI 占饱和 GDI 的比例 |
| \(\varepsilon\) | PVAF cutoff |
| \(Q_0\) | provisional Q-matrix |
| \(Q^*\) | 真实 Q-matrix |
| \(\widehat Q\) | 数据建议 Q-matrix |
| \(\tau_{il}\) | 学生 \(i\) 属于模式 \(l\) 的后验概率 |
| \(\theta_i\) | 模拟中的高阶连续能力 |
| \(\lambda_{0k}\) | 属性 \(k\) 的高阶位置参数 |
| \(\lambda_{1k}\) | 属性 \(k\) 的高阶斜率 |
| \(p_0\) | 零属性组成功概率 |
| \(p_1\) | 全掌握组成功概率 |

## 三个容易混淆的星号与上标

\[
K_j^*
\]

表示题目真正或当前定义下的所需属性数。

\[
\boldsymbol q^*
\]

表示正确 q-vector。

\[
\widehat{\varsigma}_{\max}^2
\]

表示全属性候选产生的样本最大 GDI。

## 四个概率层次

| 概率 | 条件 | 用途 |
| --- | --- | --- |
| \(P(Y_j=1\mid\boldsymbol\alpha)\) | 完整模式 | 原始反应函数 |
| \(P(Y_j=1\mid\boldsymbol\alpha_{\boldsymbol q})\) | 候选约化模式 | 折叠后的成功率 |
| \(P(\boldsymbol\alpha_i=\boldsymbol\alpha\mid\boldsymbol Y_i)\) | 学生全部反应 | 后验软分类 |
| \(P(\alpha_{ik}=1\mid\theta_i)\) | 高阶能力 | 模拟属性生成 |
