# 符号表

| 符号 | 含义 |
| --- | --- |
| \(N\) | 被试数 |
| \(J\) | 题目数 |
| \(K\) | 二元潜在属性数 |
| \(\boldsymbol R\) | \(J\) 维二元反应向量 |
| \(\boldsymbol r\) | 一个具体反应模式 |
| \(\boldsymbol\alpha\) | \(K\) 维属性模式 |
| \(p_{\boldsymbol\alpha}\) | 属性模式 \(\boldsymbol\alpha\) 的总体比例 |
| \(\boldsymbol p\) | 全部 \(2^K\) 个潜类比例 |
| \(Q\) | \(J\times K\) 题目--属性设计矩阵 |
| \(\boldsymbol q_j\) | Q 的第 \(j\) 行 |
| \(q_{jk}\) | 题 \(j\) 是否要求属性 \(k\) |
| \(\Theta\) | \(J\times2^K\) 题目反应概率矩阵 |
| \(\theta_{j,\boldsymbol\alpha}\) | 潜类 \(\boldsymbol\alpha\) 对题 \(j\) 的正反应概率 |
| \(\Gamma_{j,\boldsymbol\alpha}\) | DINA 理想反应 \(I(\boldsymbol\alpha\succeq\boldsymbol q_j)\) |
| \(s_j\) | DINA 失误概率 |
| \(c_j=1-s_j\) | DINA 能力类正反应概率 |
| \(g_j\) | DINA 非能力类猜对概率 |
| \(I_K\) | \(K\times K\) 单位矩阵 |
| \(Q^\star\) | 删除指定结构块后的剩余 Q |
| \(Q_1,Q_2\) | Theorem 4 中两块泛完整子矩阵 |
| \(T(Q,\Theta)\) | \(2^J\times2^K\) 可观测联合正反应矩矩阵 |
| \(\vartheta_Q\) | 给定 Q 的自由参数空间 |
| \(\vartheta_{\mathrm{non}}\) | 不可识别参数子集 |
| \(\sim\) | Q 的列置换等价 |
| \(\succeq\) | 逐元素偏序 |
| \(\odot\) | 逐元素乘积 |
| \(B\) | G-DINA 效应系数构成的稀疏矩阵 |
| \(\mathcal S_0\) | 真 \(B^0\) 的非零支撑 |
| \(h^2(\eta^0,\eta)\) | 两个反应分布的平方 Hellinger 距离 |
| \(C_{\min}(\eta^0)\) | 真结构与错误支撑之间的最小分离常数 |
| A | 完整性：含 \(I_K\) |
| B | \(Q^\star\) 的列互异性 |
| C | 重复性：每列至少三个 1 |
| D | 两块互不重叠的泛完整 \(K\times K\) 子矩阵 |
| E | 剩余 \(Q^\star\) 每列至少一个 1 |

## 三个“完整”概念

| 名称 | 要求 |
| --- | --- |
| 完整 | 含一套 \(I_K\) |
| 双完整 | 含两套互不重叠的 \(I_K\) |
| 泛完整 | 存在属性到不同题的全匹配；相应方阵对角线可置换为全 1 |

## 三个识别层次

| 名称 | 含义 |
| --- | --- |
| 严格识别 | 每个合法参数点均唯一 |
| 全局泛识别 | 除零测集外，在整个参数空间唯一 |
| 局部泛识别 | 除零测集外，在真参数邻域唯一 |
