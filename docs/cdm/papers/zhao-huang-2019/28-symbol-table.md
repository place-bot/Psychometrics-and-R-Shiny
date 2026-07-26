# 符号表

| 符号 | 含义 |
| --- | --- |
| \(J\) | 题目数 |
| \(K\) | 认知属性数 |
| \(Q\) | \(J\times K\) 二元题目--属性矩阵 |
| \(q_{jk}\) | 题 \(j\) 是否需要属性 \(k\) |
| \(\boldsymbol q_j\) | 题 \(j\) 的 Q 行 |
| \(d_j\) | 题 \(j\) 的原始文本 |
| \(y_j\) | 题 \(j\) 的专家属性类别 |
| \(O\) | Operations of integers |
| \(M\) | Mathematical thinking |
| \(\boldsymbol x_j\) | 题 \(j\) 的 TF--IDF 特征向量 |
| \(p\) | 候选文本特征数 |
| \(k\) | 信息增益筛选后保留的特征数 |
| \(X_r\) | 第 \(r\) 个文本特征变量 |
| \(Y\) | 认知属性随机变量 |
| \(H(Y)\) | 类别熵 |
| \(H(Y\mid X)\) | 给定特征后的条件熵 |
| \(IG(X;Y)\) | 信息增益/互信息 |
| \(df_r\) | 含特征 \(r\) 的训练题数 |
| \(\operatorname{tf}_{jr}\) | 特征 \(r\) 在题 \(j\) 中的词频 |
| \(\operatorname{idf}_r\) | 特征 \(r\) 的逆文档频率 |
| \(\boldsymbol w,b\) | SVM 超平面参数 |
| \(\xi_j\) | SVM 松弛变量 |
| \(C\) | SVM 误分类惩罚强度 |
| \(\alpha,\boldsymbol\beta\) | Logistic Regression 截距与系数 |
| \(\lambda\) | L2 正则强度 |
| \(p(c)\) | NB 类别先验 |
| \(\mu_{cr},\sigma_{cr}^2\) | Gaussian NB 中类别 \(c\)、特征 \(r\) 的均值与方差 |
| \(\mathcal T\) | 训练集 |
| \(\mathcal V\) | 验证集 |
| \(\mathcal E\) | 测试集 |
| \(TP_c\) | 类别 \(c\) 的真正例数 |
| \(FP_c\) | 类别 \(c\) 的假正例数 |
| \(FN_c\) | 类别 \(c\) 的假负例数 |
| \(t_c\) | 真实类别 \(c\) 的支持度 |
| \(p_c\) | 原文中预测为类别 \(c\) 的题数 |
| \(F1_c\) | 类别 \(c\) 的 F1 |
| \(\pi_t(\boldsymbol\alpha)\) | CAT 第 \(t\) 步后的学生属性后验 |
| \(\Omega_t\) | CAT 第 \(t\) 步可选题集合 |
| \(U_t(j)\) | 第 \(t\) 步选择题 \(j\) 的测量效用 |
| \(p_\psi(\boldsymbol q_j\mid d_j)\) | 文本模型对题 \(j\) 的 Q 行分布 |

## 数据常数

\[
J_{\mathrm{raw}}=1069,
\qquad
K_{\mathrm{raw}}=9.
\]

\[
J_{\mathrm{experiment}}=805,
\qquad
K_{\mathrm{experiment}}=2.
\]

\[
n_O=666,
\qquad
n_M=139.
\]

## 实验网格

\[
\mathcal K
=
\{5,10,\ldots,300\},
\qquad
|\mathcal K|=60.
\]

\[
\mathcal A
=
\{\mathrm{LR},\mathrm{SVM},\mathrm{NB}\}.
\]

\[
\mathcal G
=
\{(1,1),(1,2),(1,3)\}.
\]
