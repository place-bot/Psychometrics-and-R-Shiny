# 多数类基线与类别不平衡

## 1. 类别基线

O 类有 666 题，M 类有 139 题：

\[
\pi_O=\frac{666}{805}=0.827329,
\]

\[
\pi_M=\frac{139}{805}=0.172671.
\]

恒预测 O 的 accuracy 为

\[
\operatorname{Accuracy}_{\text{all-O}}
=
\pi_O
=
82.733\%.
\]

## 2. 与最佳模型比较

最佳 NB accuracy 为 85.2%，所以绝对增益为

\[
85.2-82.733
=
2.467\text{ pp}.
\]

相对错误率下降为

\[
\frac{
(1-0.82733)-(1-0.852)
}{
1-0.82733
}
\approx14.3\%.
\]

这两个量描述不同尺度，均可报告。

## 3. LR 与 SVM

最佳 LR accuracy 为 75.3%，最佳 SVM 为 74.9%。二者都低于 all-O accuracy。

这不等于模型毫无价值：它们可能牺牲多数类正确率来识别 M。缺少混淆矩阵时无法判断。

## 4. 标准 weighted F1 基线

all-O 时：

\[
\operatorname{Precision}_O
=
\frac{666}{805}=0.82733,
\]

\[
\operatorname{Recall}_O=1,
\]

\[
F1_O
=
\frac{2(0.82733)(1)}
{0.82733+1}
=0.90551.
\]

M 类 F1 为 0。按真实支持度加权：

\[
F1_{\mathrm{weighted,all-O}}
=
\frac{666}{805}\times0.90551
=74.915\%.
\]

## 5. 论文结果相对 F1 基线

| 模型最佳配置 | weighted F1 | 相对 all-O |
| --- | ---: | ---: |
| LR | 73.1% | -1.8 pp |
| SVM | 72.0% | -2.9 pp |
| NB | 85.6% | +10.7 pp |

在标准 weighted F1 定义下，NB 的优势比 accuracy 更明显。

## 6. 还需要的基线

- stratified random classifier；
- class-prior classifier；
- 只用题干长度；
- 只用是否含“整数/和/图”等少量规则；
- Multinomial NB；
- Complement NB；
- character \(n\)-gram；
- 专家之间的一致性上限。

论文没有报告这些基线。

## 7. 更合适的主指标

对于新题标注，漏掉少数属性可能很重要。建议把以下指标设为主报告：

\[
\operatorname{Recall}_M,
\quad
F1_{\mathrm{macro}},
\quad
\operatorname{BalancedAccuracy}.
\]

若模型输出置信度，还应报告：

- calibration curve；
- Brier score；
- selective accuracy；
- 在不同人工复核率下的错误率。
