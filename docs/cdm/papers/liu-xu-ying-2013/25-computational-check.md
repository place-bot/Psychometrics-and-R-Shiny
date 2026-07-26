# 本站可计算核验

## 固定教学设定

脚本使用

\[
Q=
\begin{pmatrix}
1&0\\
0&1\\
1&1\\
1&1
\end{pmatrix}.
\]

这个 Q 满足：

- 完整：前两行是 \(I_2\)；
- 每个属性至少被三道题要求；
- 饱和 T 包含 \(2^4-1=15\) 个题组行。

属性模式按

\[
00,\ 01,\ 10,\ 11
\]

排列，取

\[
\boldsymbol p^*
=(0.10,0.20,0.30,0.40)^\top,
\]

\[
\boldsymbol c
=(0.85,0.82,0.90,0.88)^\top,
\]

\[
\boldsymbol g
=(0.15,0.18,0.10,0.12)^\top.
\]

## 运行方法

```bash
python3 tools/liu_xu_ying_2013_theory_check.py --mode all
```

也可分项运行：

```bash
python3 tools/liu_xu_ying_2013_theory_check.py --mode structural
python3 tools/liu_xu_ying_2013_theory_check.py --mode separation
python3 tools/liu_xu_ying_2013_theory_check.py --mode counterexample
python3 tools/liu_xu_ying_2013_theory_check.py --mode finite --replicates 20
```

## 核验一：满列秩

无噪声 \(T(Q)\) 排除全零属性列，形状是

\[
15\times3.
\]

脚本结果：

```text
saturated deterministic T shape: (15, 3)
rank(T): 3 (target 3)
```

它与 Proposition 6.1 的

\[
\operatorname{rank}(T)=2^k-1=3
\]

一致。

带猜测的增广 T 保留全部四个属性模式，脚本得到

```text
rank(augmented noisy T): 4
```

与 Proposition 6.6 的满列秩结论一致。

## 核验二：猜测消去变换

脚本显式构造 D，并比较

\[
D\widetilde T_{c,g}(Q)
\]

与

\[
(0,T_{c-g}(Q)).
\]

最大逐元素误差为

```text
1.110e-16
```

这是双精度浮点舍入量级，验证了式（6.3）及归纳构造对应的矩阵恒等式。

## 核验三：列置换

交换 Q 的两列，并按相同规则交换属性模式列，最大差异为

```text
0.000e+00
```

这直接展示 \(\sim\) 等价关系对应的观测不变性。

## 核验四：总体列空间分离

每个非零 q-vector 有三种选择，四道题共有

\[
3^4=81
\]

个无全零行的候选 Q。

对每个候选，脚本在概率单纯形上剖面化 \(\boldsymbol p\)。结果为：

```text
candidate matrices: 81
matrices in the true column-permutation class: 2
candidates with numerical zero loss: 2
best inequivalent loss: 0.105301
```

只有真 Q 和交换两列后的 Q 取得数值零损失。最接近的错误等价类仍与真总体矩相距约 \(0.1053\)。

这个枚举只验证当前小例。一般结论由原文命题证明。

## 核验五：C4 失败

把全部概率质量放在全掌握模式：

\[
\boldsymbol p=(0,0,0,1)^\top,
\]

并采用无噪声模型。脚本结果：

```text
candidate matrices reproducing the moments: 81/81
every nonempty item-set moment equals 1
```

全部候选都能复制反应矩，精确重现 Remark 2.4 的反例。

## 核验六：有限样本演示

使用固定种子 `20260726`，每个样本量 20 次重复，已知 \(c,g\)，每次在 81 个候选中做全局枚举：

| \(N\) | 恢复真列置换等价类 | 平均胜出损失 |
| ---: | ---: | ---: |
| 100 | 16/20（80.0%） | 0.07807 |
| 500 | 20/20（100.0%） | 0.03290 |
| 2000 | 20/20（100.0%） | 0.01691 |

随着 \(N\) 增大，胜出损失下降，恢复率在这个简单设定中提高。

## 数值结果的解释边界

这 60 份数据属于本站教学演示，原文没有这些数字。重复次数较少，Q 很小，\(\boldsymbol p,c,g\) 条件良好。结果可以验证代码流程和定理直觉，无法给出通用样本量建议。

更严格的后续实验应系统改变：

- \(m,k\)；
- 最小属性模式概率；
- \(c_i-g_i\) 的信号强度；
- T 的截断阶数；
- Q 的冗余度；
- \(c,g\) 的已知程度；
- 全局搜索与局部搜索。

[下一页：局限、结论与未来工作](26-limitations-conclusion-future.md)
