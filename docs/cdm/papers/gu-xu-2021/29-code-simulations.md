# 官方模拟代码精读

## 1. 主文 Figure 1

`id_Q_DINA_basis_Q42.m` 和 `get_Q24_nonid.m` 构造四题两属性的多个等价 DINA 参数，计算 16 个反应模式的边际概率，并绘制参数和概率对照。

代码固定随机种子，可重现构造路径。

## 2. 主文 Figures 2--3

`get_Q24_single_MSE.m` 是核心函数：

- 100 组真参数；
- 每组 200 次重复；
- 每次 10 个 EM 初值；
- 最大似然初值获胜；
- 返回 \(\boldsymbol p,\boldsymbol c,\boldsymbol g\) 的平均逐元素 MSE。

`Q24_MSE_main.m` 更接近分析草稿：

- 先调用仓库中不存在的 `get_MSE`；
- 在加载结果文件前使用 `p_mse100` 等工作区变量；
- 后半段再加载 `MSE_*.mat`；
- 这些预计算 MSE 文件没有收入仓库。

`get_Q24_final_MSE.m` 的函数签名没有参数，却在函数体中使用未定义的 `N`。直接运行需要把签名改为

```matlab
function [] = get_Q24_final_MSE(N)
```

或在函数内定义样本量。

## 3. DINA 穷举

`exhaus_dina.m`：

1. 从 `Q_aa.mat` 取真 Q；
2. 生成 Dirichlet 潜类比例和 \(c,g\)；
3. 生成 \(N=10^5\) 数据；
4. 对 121 张 Q 分别做 5 次随机初值 EM；
5. 保存每张 Q 的最佳对数似然。

`get_cg.m` 实现 DINA EM。停止条件只检查参数差：

```matlab
while (max(abs(old_c-c_i))+max(abs(old_g-g_i)))>1e-6
```

没有最大迭代数保护。极端数据或数值停滞时可能长时间运行。

`exhaus_dina_main.m` 负责读入预计算 `.mat` 并绘图。仓库没有收入这些输出文件，默认文件名也需要用户按场景修改。

## 4. G-DINA 穷举

`exhaus_gdina.m` 的流程与 DINA 类似：

- 5 个随机初值；
- G-DINA EM 最多 5000 次；
- 收敛阈值为 \(\Theta\) 元素绝对变化和 \(10^{-5}\)；
- 拟合结束后检查单调性；
- 保存强单调候选标记。

`get_GDINAprob_mono.m` 先执行无约束 EM，再检查结果是否满足单调性。它没有在每个 M-step 中施加单调约束，所以“未通过”的候选会被绘图程序过滤。

## 5. Study VII

`id_Q_GDINA_attr2_K3.m` 和 `id_Q_GDINA_attr2_K5.m`：

- 构造真 Q 与替代 \(\bar Q\)；
- 以随机种子编号产生扰动；
- 检查概率范围和单调性；
- 取前 70 个合法种子；
- 枚举完整反应概率并计算最大差。

K=3 文件末尾把结果保存为含 `K5` 的文件名，属于命名笔误。文件顶部的 Figure 编号也保留了早期版本号，与最终补充材料的 Figures 11--12 不一致。

## 6. 复现门槛

代码依赖：

- MATLAB；
- Statistics and Machine Learning Toolbox 中的 `gamrnd`；
- 多个脚本之间共享当前目录和 `.mat` 文件；
- 预计算结果文件和手动选择的绘图入口。

仓库足以精读算法和重跑核心函数，尚未形成一个从零执行全部七组 Study 的单命令流水线。
