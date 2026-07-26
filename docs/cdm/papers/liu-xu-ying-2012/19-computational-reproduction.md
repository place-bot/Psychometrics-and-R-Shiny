# 本站可计算复现

## 运行全部检查

```bash
python3 tools/liu_xu_ying_2012_q_learning.py \
  --mode all \
  --examinees 1200
```

## T-matrix 精确核对

```bash
python3 tools/liu_xu_ying_2012_q_learning.py --mode toy
```

关键输出：

```text
T(Q), Equation (9):
[[0 1 0 1]
 [0 0 1 1]
 [0 0 0 1]]

T(Q'), Equation (10):
[[0 1 0 1]
 [0 0 1 1]
 [0 1 0 1]]

T(Q) with item-pair row, Equation (13):
[[0 1 0 1]
 [0 0 1 1]
 [0 0 0 1]
 [0 0 0 1]]
```

脚本用 `numpy.testing.assert_array_equal` 检查三块矩阵，任一元素不符都会失败退出。

## 正式表值核对

```bash
python3 tools/liu_xu_ying_2012_q_learning.py --mode tables
```

输出会列出 Tables 1--3，并提示：

```text
editorial discrepancy: Table 1 reports Q1/N=500 as 94; prose reports 98
```

## 小型 Q 恢复

```bash
python3 tools/liu_xu_ying_2012_q_learning.py \
  --mode simulate \
  --examinees 1200 \
  --seed 20260725
```

固定种子下，演示从一行错误开始：

```text
iteration=1 item=6 S=0.130560->0.029598 drop=77.33% accepted=True
iteration=2 item=- S=0.029598->0.029598 drop=0.00% accepted=False
exact recovery: True
```

数值路径展示：

1. 每个候选下重新运行 EM；
2. 首轮把第 6 题从 `10` 改回 `11`；
3. \(S\) 大幅下降；
4. 下一轮没有更优单行邻居，算法停止。

## 改变样本量

```bash
python3 tools/liu_xu_ying_2012_q_learning.py \
  --mode simulate \
  --examinees 500 \
  --seed 7
```

不同种子或较小 N 可能停在其他 Q，这正是有限样本与局部搜索问题的可观察版本。

## 精确复现边界

本站没有声称重新生成 Tables 1--4 的原始 100 次频数，原因包括：

- 原始种子缺失；
- EM 初值、容差和局部解处理缺失；
- 4 阶与 \(K+1\) 阶 T 描述存在歧义；
- 同阶题组选择方式未列；
- 全零 q-vector 与平局规则未交代；
- 早停实现细节未完整给出。

脚本的价值是把论文每个数学对象变成可单独测试的函数，并为后续理论论文提供计算底座。
