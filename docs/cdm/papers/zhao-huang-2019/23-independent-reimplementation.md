# 独立代码重构：训练、验证、测试严格分离

## 1. 文件

本站提供：

[`tools/zhao_huang_2019_reimplementation.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/zhao_huang_2019_reimplementation.py)

它是根据论文描述重建的现代可重复管线，未使用作者数据或源码。

## 2. 输入格式

UTF-8 CSV：

```csv
text,label
"计算 38 与 17 的和","O"
"根据图表选择正确的数量关系","M"
```

至少需要两类和 20 道题。

## 3. 数据划分

代码先做：

```python
train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=seed,
    stratify=labels
)
```

再把 20% 临时集等分为验证集和测试集。这样得到接近 80/10/10 的分层划分。

## 4. 中文分词

```python
" ".join(jieba.lcut(text))
```

分词后的空格串交给 `TfidfVectorizer`。显式设置：

```python
tokenizer=str.split
lowercase=False
ngram_range=(1, ngram_max)
```

## 5. 防泄漏 TF--IDF

```python
x_train = vectorizer.fit_transform(train_x)
x_validation = vectorizer.transform(validation_x)
x_test = vectorizer.transform(test_x)
```

词表与 IDF 只由训练集拟合。

## 6. 信息增益重构

论文把 IG 解释为离散变量之间的信息。本站先把 TF--IDF 转成出现矩阵：

\[
z_{jr}=\mathbb I(x_{jr}>0),
\]

再用：

```python
mutual_info_classif(
    occurrence,
    y_train,
    discrete_features=True,
    random_state=seed
)
```

排序也只使用训练标签。

## 7. 模型映射

| 论文名称 | 本站实现 |
| --- | --- |
| LR + L2 | `LogisticRegression(penalty="l2", solver="liblinear")` |
| C-SVM | `LinearSVC(C=1, loss="squared_hinge")` |
| Gaussian NB | `GaussianNB()` |

Gaussian NB 需要 dense 输入。由于筛选后最多保留 300 维，内存规模可控。

## 8. \(k\) 的选择

对

\[
k=5,10,\ldots,300
\]

计算验证集 standard weighted F1，保留分数最高的 \(k\)。

若词表少于 300，搜索在全部可用特征处停止。

## 9. 最终输出

每个模型报告：

- `selected_k`；
- validation weighted F1；
- test accuracy；
- test weighted F1；
- test macro-F1；
- test balanced accuracy；
- 每类 precision/recall/F1；
- top 30 互信息特征。

## 10. 运行方式

```bash
python -m pip install jieba numpy scipy scikit-learn
python tools/zhao_huang_2019_reimplementation.py items.csv \
  --seed 2019 \
  --output zhao_huang_report.json
```

## 11. 相对论文的改进

- 所有随机步骤有种子；
- 所有模型参数显式；
- train/validation/test 处理严格分离；
- 增加类别不平衡指标；
- 保存机器可读 JSON；
- 输出最终 \(k\) 和关键词；
- 可替换为自己的多类数据。

## 12. 仍需数据层面工作

该脚本可以运行，但无法生成论文 Tables 1--3 的原始数字，因为 805 道题及其标签没有公开。
