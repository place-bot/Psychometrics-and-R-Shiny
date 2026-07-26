# 本站可计算核验与代码审查

## 1. 独立实现

本站提供零第三方依赖脚本：

```bash
python tools/gu_xu_2021_identifiability_check.py
```

它实现：

- Theorem 1 的 A/B/C；
- 泛完整性的属性--题目匹配；
- Theorem 4 的两块泛完整子矩阵和剩余覆盖搜索；
- \(5\times2\) 非零行 Q 空间枚举；
- \(K=8,J=12\) 论文构造核验。

## 2. 论文示例输出

```text
Q5_generic_DINA     A=1 B=1 C=0 strict=0 generic-complete=1 D+E=0
Q15_strict_DINA     A=1 B=1 C=1 strict=1 generic-complete=1 D+E=1
Q18_strict_DINA     A=1 B=1 C=1 strict=1 generic-complete=1 D+E=1
Q27_generic_GDINA   A=0 B=0 C=1 strict=0 generic-complete=1 D+E=1
Q54_generic_GDINA   A=1 B=0 C=1 strict=0 generic-complete=1 D+E=1
Q81_generic_GDINA   A=0 B=0 C=1 strict=0 generic-complete=1 D+E=1
```

这里 D+E 是一般 RLCM 的泛识别充分条件，不能用来替代 DINA Theorem 2 的判定。

## 3. \(K=8,J=12\)

脚本核验论文矩阵：

```text
A=1 B=1 C=1 strict=1
counts=(3, 3, 3, 4, 4, 4, 4, 5)
```

所以 12 道题同时满足三条结构要求。

## 4. 独立枚举 \(5\times2\)

每行只能取

\[
(0,1),(1,0),(1,1),
\]

共有

\[
3^5=243
\]

张有序矩阵。按整体列交换取等价类，Burnside 计数为

\[
\frac{243+1}{2}=122.
\]

本站枚举结果：

```text
column-swap classes: 122
Theorem 1 candidates: 45; row/column forms: 2
Theorem 4 candidates: 71; row/column forms: 6
```

这核验了论文所说的两种严格识别结构形状，以及 Study V 的六种 D/E 结构形状。

## 5. 对官方 `Q_aa.mat` 的核对

可追加作者文件路径：

```bash
python tools/gu_xu_2021_identifiability_check.py \
  --author-mat path/to/Identify_Q/simulations/Q_aa.mat
```

官方文件实际存 121 张互不重复的列交换代表。按论文文字“排除全零行，只合并列交换”，组合计数应为 122。

缺少的有序代表可写为

\[
\begin{pmatrix}
1&1\\
1&1\\
1&1\\
1&1\\
0&1
\end{pmatrix}.
\]

它与 \(Q^{81}\) 具有相同的行多重集合，只差题目行次序。因此：

- “121 覆盖全部有序候选”的字面陈述少一类；
- Study V 的六种结构形状仍全部有代表；
- 对固定题目顺序的逐候选似然穷举，候选集合并非组合意义上的完整 122 类。

## 6. 与官方检查器的交叉核验

本站实现用论文名称固定：

- B = \(Q^\star\) 列互异；
- C = 每列至少三个 1。

它还为输入做矩形和二元检查，并在每条路径返回完整结果，避免官方函数部分早退时输出未赋值。

## 7. 本站核验的范围

脚本复核离散结构条件和候选空间计数，没有重跑 800,000 次主文 EM，也没有重跑 \(N=10^5\) 的全部 G-DINA 穷举。原文的概率相等数值来自作者 MATLAB 实验，本站在 notes 中按补充材料逐项记录。
