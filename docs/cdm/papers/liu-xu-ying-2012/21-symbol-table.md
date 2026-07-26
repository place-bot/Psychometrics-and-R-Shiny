# 符号表

| 符号 | 维度或取值 | 含义 |
| --- | --- | --- |
| \(N\) | 正整数 | 学生数 |
| \(J\) | 正整数 | 题数 |
| \(K\) | 正整数 | 已知属性数 |
| \(R_i^j\) | \(\{0,1\}\) | 学生 \(i\) 对题 \(j\) 的反应 |
| \(\boldsymbol R_i\) | \(J\times1\) | 学生 \(i\) 的反应向量 |
| \(\boldsymbol\alpha_i\) | \(\{0,1\}^K\) | 学生 \(i\) 的属性模式 |
| \(p_{\boldsymbol\alpha}\) | \([0,1]\) | 属性模式总体比例 |
| \(\boldsymbol p\) | \(2^K\times1\) | 全部属性模式比例 |
| \(Q\) | \(J\times K\) | 真 Q 矩阵或上下文中的当前矩阵 |
| \(Q'\) | \(J\times K\) | 一般候选 Q |
| \(Q_0\) | \(J\times K\) | 初始专家 Q |
| \(\boldsymbol q_j\) | \(1\times K\) | 题 \(j\) 的 q-vector |
| \(\xi^j(\boldsymbol\alpha,Q)\) | \(\{0,1\}\) | DINA 理想反应 |
| \(s_j\) | \([0,1]\) | slipping 概率 |
| \(c_j=1-s_j\) | \([0,1]\) | 理想掌握组答对率 |
| \(g_j\) | \([0,1]\) | 非理想掌握组答对率 |
| \(\pi_{j\boldsymbol\alpha}\) | \([0,1]\) | 属性模式 \(\boldsymbol\alpha\) 对题 \(j\) 的答对概率 |
| \(B(j)\) | \(1\times2^K\) | 单题条件答对概率向量 |
| \(B(j_1,\ldots,j_\ell)\) | \(1\times2^K\) | 题组联合答对 B-vector |
| \(\mathcal C\) | 题组集合 | 进入 T 的行索引集合 |
| \(L\) | 正整数 | T 的行数 |
| \(T_{\boldsymbol c,\boldsymbol g}(Q)\) | \(L\times2^K\) | 模型矩设计矩阵 |
| \(\beta_A\) | \([0,1]\) | 题组 \(A\) 的样本联合答对率 |
| \(\boldsymbol\beta\) | \(L\times1\) | 选定样本矩向量 |
| \(S_{c,g,p}(Q)\) | 非负实数 | 参数给定时的欧氏距离 |
| \(S(Q)\) | 非负实数 | 对 nuisance parameters 剖面化后的距离 |
| \(\widehat S(Q)\) | 非负实数 | 插入 MLE 后的距离 |
| \(U_j(Q)\) | 矩阵集合 | 只允许第 \(j\) 行变化的邻域 |
| \(Q^{(m)}\) | \(J\times K\) | 第 \(m\) 轮搜索结果 |
| \(j_*\) | \(1,\ldots,J\) | 本轮最终更新的题 |
| \(I_K\) | \(K\times K\) | 单位阵 |
| \(V_J\) | \(1\times K\) | 部分已知实验中的待校准新题 |
| \(\rho\) | \([0,1]\) | probit 潜变量共同相关 |
| \(\Phi^{-1}\) | 函数 | 标准正态分位函数 |
| \(\sim\) | 等价关系 | Q 只相差属性列置换 |

## 三个易混对象

| 对象 | 数据还是模型 | 是否依赖候选 Q |
| --- | --- | --- |
| \(\boldsymbol\beta\) | 数据 | 否 |
| \(T_{\boldsymbol c,\boldsymbol g}(Q)\) | 模型 | 是 |
| \(\boldsymbol p\) | 潜在总体参数 | 候选 Q 下重新估计 |

## 三个 Q 估计记号

| 记号 | nuisance parameters 处理 |
| --- | --- |
| \(\widehat Q\)（式 14 后） | \(c,g,p\) 已知 |
| \(\widehat Q\)（式 16） | 直接在距离中联合剖面 |
| \(\widetilde Q\)（式 18） | 先求 MLE，再代入 \(\widehat S\) |

原文重复使用 \(\widehat Q\) 表示不同上下文的估计量，阅读时需查看它对应的目标函数。
