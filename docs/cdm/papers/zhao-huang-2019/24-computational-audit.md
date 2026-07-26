# 本站数值核验及其输出

## 1. 文件与目标

[`tools/zhao_huang_2019_audit.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_audit.py) 只依赖 Python 标准库，用于核验：

- 九类题量；
- O/M 比例；
- all-O 基线；
- Tables 1--3 的特征选择增益；
- \(k\) 搜索规模；
- 85.2% 的可能测试分母；
- Wilson 区间；
- Equation (9) 与标准 weighted F1。

## 2. 运行

```bash
python3 tools/zhao_huang_2019_audit.py
```

JSON：

```bash
python3 tools/zhao_huang_2019_audit.py --json
```

## 3. 核验输出

```text
Nine-category total: 1069; O+M subset: 805
O share: 82.733%; all-O accuracy: 82.733%
All-O standard support-weighted F1: 74.915%
All-O F1 under printed Equation (9): 90.551%
Best reported accuracy gain over all-O: 2.467 percentage points
```

## 4. 特征选择增益

程序逐格相减得到：

| 表征 | 模型 | accuracy 增益 | F1 增益 |
| --- | --- | ---: | ---: |
| unigram | LR | +1.6 | +4.0 |
| unigram | SVM | +3.2 | +4.7 |
| unigram | NB | +62.7 | +62.3 |
| unigram+bigram | LR | +1.9 | +2.8 |
| unigram+bigram | SVM | +3.8 | +3.9 |
| unigram+bigram | NB | +15.5 | +17.9 |
| unigram+bigram+trigram | LR | +2.8 | +3.7 |
| unigram+bigram+trigram | SVM | +3.6 | +3.7 |
| unigram+bigram+trigram | NB | +16.3 | +18.4 |

## 5. \(k\) 网格

\[
\{5,10,\ldots,300\}
\]

包含 60 个候选。

## 6. 测试分母

程序在 805 的 10% 附近搜索整数分母。唯一能把正确率四舍五入为 85.2% 的近邻组合是：

\[
n_{\mathrm{test}}=81,
\qquad
\text{correct}=69.
\]

## 7. 不确定性

```text
one item = 1.235 percentage points
Wilson 95% interval = [75.9%, 91.3%]
```

## 8. 与 85.6% F1 相容的混淆表

程序找到两种接近总体比例的候选：

```text
O->O 60, O->M 7, M->O 5, M->M 9
O->O 61, O->M 7, M->O 5, M->M 8
```

它们的标准 weighted F1 都四舍五入为 85.6%，Equation (9) 则约为 84.8%。

## 9. 自动断言

脚本数据结构使以下恒等式可直接核对：

\[
\sum_{c=1}^{9}n_c=1069,
\]

\[
n_O+n_M=805,
\]

\[
|\mathcal K|=60.
\]

## 10. 证据边界

该程序检查论文已发表数字之间的一致性，不拟合分类器，也不声称复现作者预测。
