# 官方条件检查代码精读

## 1. 仓库结构

官方仓库 [`yuqigu/Identify_Q`](https://github.com/yuqigu/Identify_Q) 的 `check_conditions/` 包含：

| 文件 | 作用 |
| --- | --- |
| `check_conditions_main.m` | 6 个示例入口 |
| `check_Theorem1.m` | DINA 严格识别 A/B/C |
| `check_Theorem2.m` | DINA 两次测量的泛识别分支 |
| `check_Theorem3.m` | 一般 RLCM 的重复次数必要条件 |
| `check_Theorem4.m` | 搜索 D/E 的三块题集 |
| `check_generic_complete.m` | 用 Hall 条件检查泛完整 |
| `check_complete.m` | 搜索一套 \(I_K\) |
| `check_double_complete.m` | 搜索两套单属性题 |

仓库当前 `master` 的可见最后提交为 2019-05-04，代码使用 MATLAB。

## 2. `check_Theorem1.m`

计算链为：

```text
每列 1 的次数
   │
   ├── 搜索每个单位行 e_k
   ├── 删除选中的 I_K
   ├── unique(Qstar', 'rows') 统计不同列
   └── 三个布尔量相乘
```

核心判断等价于：

\[
I(A)\,I(B)\,I(C).
\]

### 注释偏差

代码把“每列至少三个 1”注释为 Condition B，把“\(Q^\star\) 列互异”注释为 Condition C。论文中的名称顺序为 B = distinctness，C = repetition。

### 输出边界

若发现某列计数不超过 2，函数先 `return`，没有给四个输出变量完整赋值。只作为命令调用时会打印提示；若调用者请求返回值，可能触发未赋值错误。

## 3. `check_Theorem2.m`

它先按列计数分流：

- 全部至少 3：提示改查 Theorem 1；
- 某列不超过 1：判定泛识别失败；
- 多列恰为 2：只检查双完整情形；
- 单列恰为 2：重排并读取 \(\boldsymbol v\)，检查 (a)、(b.1)、(c)。

用 `NaN` 表示“只得到局部结论或定理未覆盖”，这个设计需要调用者显式区分 `0` 与 `NaN`。

### 覆盖边界

单列恰为 2 且 \(\boldsymbol v=0\) 时，代码优先检查 \(Q^\star\) 的 A/B/C；没有在该分支单独检查 Theorem 2(b.2) 的“双 \(I_{K-1}\)”条件。部分理论可判场景会得到未覆盖或输出未赋值。

## 4. `check_Theorem4.m`

算法穷举：

\[
\binom{J}{K}
\]

个第一子矩阵，对每个再枚举

\[
\binom{J-K}{K}
\]

个第二子矩阵。找到两块泛完整矩阵后，检查剩余题是否每列非零。

最坏组合数约为

\[
\binom{J}{K}\binom{J-K}{K},
\]

所以大 \(J,K\) 时成本迅速上升。代码注释记录一个 \(18\times7\) 子矩阵搜索约需 96 秒。

## 5. `check_generic_complete.m`

代码枚举 \(2^K-1\) 个非空属性子集并执行 Hall 条件。数学逻辑准确，复杂度随属性数指数增长。

更可扩展的实现可以把 Q 看成二分图，直接求最大匹配。

## 6. 信息输出的几处偏差

- `check_Theorem3.m` 实际用 `any(attr_count <= 2)`，提示文字却写“少于 2”；
- 通过时实际要求每列至少 3，提示文字写“至少 2”；
- `check_Theorem4.m` 在 \(J<2K+1\) 时提示“Theorem 5 条件失败”，相关充分条件来自 Theorem 4；
- `check_conditions_main.m` 的 Example 2 写“scenario (a) 且全局泛识别”，Theorem 2(a) 的结论为局部泛识别失败；
- Example 5 写“全局泛识别”，Theorem 2(c) 只给局部泛识别。

这些问题集中在注释和提示层。使用官方函数时，应保存原始布尔输出，并根据论文定理重新解释。
