# TF--IDF 题目向量

## 1. 目标

筛选 top-\(k\) 词后，需要把每道题变成数值向量：

\[
\boldsymbol x_j
=
(x_{j1},\ldots,x_{jk}).
\]

论文使用 term frequency--inverse document frequency。

## 2. Term Frequency

设特征 \(r\) 在题 \(j\) 中出现 \(c_{jr}\) 次。最简单的词频为

\[
\operatorname{tf}_{jr}=c_{jr}.
\]

也可使用对数缩放：

\[
\operatorname{tf}_{jr}
=
\begin{cases}
1+\log c_{jr},&c_{jr}>0,\\
0,&c_{jr}=0.
\end{cases}
\]

论文没有说明具体版本。

## 3. Inverse Document Frequency

设训练集有 \(n\) 道题，特征 \(r\) 出现在 \(df_r\) 道题中。常见定义为

\[
\operatorname{idf}_r
=
\log\frac{n}{df_r}.
\]

scikit-learn 默认带平滑：

\[
\operatorname{idf}_r
=
\log\frac{1+n}{1+df_r}+1.
\]

## 4. TF--IDF 权重

\[
x_{jr}
=
\operatorname{tf}_{jr}
\operatorname{idf}_r.
\]

频繁出现在当前题、较少出现在其他题的特征获得较高权重。

## 5. 向量归一化

scikit-learn 常对每道题做 L2 归一化：

\[
\widetilde{\boldsymbol x}_j
=
\frac{\boldsymbol x_j}
{\|\boldsymbol x_j\|_2}.
\]

这会让长题与短题具有相近的整体向量尺度。

## 6. 与信息增益的职责差异

| 组件 | 回答的问题 |
| --- | --- |
| 信息增益 | 哪些词对类别区分最有用？ |
| TF--IDF | 某个保留词在当前题中应占多大权重？ |

信息增益利用标签；TF--IDF 利用词频和文档频率。

## 7. 拟合范围

词表与 IDF 应只由训练集确定：

\[
\widehat{\operatorname{idf}}_r
=
\log
\frac{1+n_{\mathcal T}}
{1+df_{r,\mathcal T}}
+1.
\]

验证集和测试集只调用 `transform`。

## 8. 论文没有报告的细节

- `TfidfVectorizer` 还是手工计算；
- `smooth_idf`；
- `sublinear_tf`；
- `norm`；
- `min_df/max_df`；
- 未登录词处理；
- 先做 IG 还是先做 TF--IDF。

这些缺口使逐数值复现无法完成。
