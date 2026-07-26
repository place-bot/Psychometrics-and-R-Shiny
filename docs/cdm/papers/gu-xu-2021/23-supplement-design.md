# Experiment：补充材料共同设计

## 1. 七组 Study

| Study | 模型 | 目的 |
| --- | --- | --- |
| I | DINA | 核验 A/B/C 的充分性 |
| II | DINA | 核验违反 C 时的泛识别 |
| III | DINA | 展示局部泛识别失败 |
| IV | DINA | 构造违反完整性的等价分布 |
| V | G-DINA | 核验 D/E 的充分性 |
| VI | G-DINA | 展示严重非识别的似然表现 |
| VII | G-DINA | 构造违反 C 的无穷多替代参数 |

## 2. \(5\times2\) 候选集

Studies I--III、V--VI 使用作者文件 `Q_aa.mat` 中的 121 张候选 Q。每行排除 \((0,0)\)，并把整体交换两列的矩阵视为同一属性标签类。

对每张真 Q：

1. 生成 \(N=10^5\) 名被试的数据；
2. 对候选 Q 分别拟合模型；
3. 比较最大化后的对数似然；
4. 检查真 Q 是否达到最大值。

图中：

- 蓝三角：候选 Q；
- 红星：生成数据的真 Q；
- 紫方块：似然最大的候选 Q。

## 3. 参数生成

### DINA

官方代码设：

\[
\boldsymbol p\sim\operatorname{Dirichlet}(5,\ldots,5),
\]

\[
c_j\sim U(0.7,0.9),
\qquad
g_j\sim U(0.1,0.3).
\]

每个候选 Q 用 5 个随机初值运行 EM。

### G-DINA

代码把潜类比例设为均匀：

\[
p_{\boldsymbol\alpha}=2^{-K}.
\]

每题基线概率随机落在约 \(0.15\) 到 \(0.25\)，全掌握概率约为 \(0.75\) 到 \(0.85\)，各阶增量按所需属性模式生成。每个候选 Q 同样使用 5 个随机初值。

## 4. G-DINA 的过滤

作者拟合全部候选 Q，但图中只展示估计参数满足更强单调限制的候选：

\[
\theta_{j,\boldsymbol\alpha}>
\theta_{j,\boldsymbol\alpha'}
\quad
\text{当}\quad
\boldsymbol\alpha\odot\boldsymbol q_j
\succ
\boldsymbol\alpha'\odot\boldsymbol q_j.
\]

官方代码用所有非零 G-DINA 增量均为正作为强检查：

```matlab
is_mono_str = all(delta(delta ~= 0) > 0);
```

它比“能力类概率高于所有非能力类”更严格。

## 5. 穷举似然的证据边界

单次大样本中真 Q 得到最大似然，与识别理论方向一致。它仍受以下因素影响：

- 有限样本随机性；
- EM 局部最优；
- 候选集是否完整；
- G-DINA 候选过滤；
- 每个场景展示的数据集数量。

所以图形构成数值说明，识别定理本身由代数证明建立。

## 6. Studies IV 与 VII

这两组不依赖“真 Q 是否最大”：

- Study IV 直接枚举全部 \(2^{20}\) 种反应模式并比较概率；
- Study VII 直接构造 70 组替代参数并比较完整反应分布。

它们对必要性反例提供更直接的机器精度核验。
