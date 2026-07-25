# Study 2：无约束 G-DINA

## 设计变化

Study 2 保留 Study 1 的：

- \(N=2000,J=30,K=5\)；
- 高阶属性结构；
- 正确 Q；
- 7/8 个随机 entry 翻转；
- 100 replications；
- \(\varepsilon=.95\)。

唯一核心变化是数据由无约束 G-DINA 生成。

## 成功概率生成

每道题的零属性组与全掌握组：

\[
p_0\sim\operatorname{Unif}(.1,.3),
\]

\[
p_1\sim\operatorname{Unif}(.7,.9).
\]

它们的期望分别为 \(.2\) 和 \(.8\)。中间潜在组的成功概率从

\[
\operatorname{Unif}(p_0,p_1)
\]

中生成，并满足单调性：

\[
\boldsymbol\alpha\succeq\boldsymbol\alpha'
\Longrightarrow
P_j(\boldsymbol\alpha)
\ge
P_j(\boldsymbol\alpha').
\]

## Table 5 完整结果

| 层级 | 错误被纠正 | 错误仍存在 | 正确被改变 | 正确保留 |
| --- | ---: | ---: | ---: | ---: |
| entry | 80.4 | 19.6 | 2.0 | 98.0 |
| vector | 74.4 | 25.6 | 9.7 | 90.3 |

## 和 Study 1 比较

无约束 G-DINA 下：

- 错误 vector 纠正率降到 74.4%；
- 正确 vector 保留率降到 90.3%；
- 正确 entry 保留率仍为 98.0%。

复杂成功概率剖面会产生更多接近的候选 GDI，整行决策尤其敏感。

## chance-adjusted improvement

论文报告：

\[
42.8\%
\quad\text{at entry level},
\]

\[
39.4\%
\quad\text{at vector level}.
\]

二者低于 Study 1 最差条件的 72.1% 和 71.1%。方法仍改善 Q，但改善幅度随反应结构复杂度下降。

## 实质解释

若某个属性只在少数交互模式中产生小幅影响，漏掉它造成的 GDI 损失可能很小。固定 \(.95\) 阈值更容易把这种候选视为足够好。无约束 G-DINA 允许这种局部、非均匀效应，因而比 DINA/DINO 更难验证。

## 设计上的重要缺口

论文只改变生成模型，没有同时系统改变：

- 样本量；
- 属性数；
- 题目数；
- 属性相关强度；
- 错误 Q 的集中方式；
- \(\varepsilon\)。

因此 Study 2 展示了复杂度影响的一个切面，还不能形成全面的边界图。
