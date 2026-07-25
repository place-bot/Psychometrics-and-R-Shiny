# 本站可计算复现

## 脚本

[`tools/de_la_torre_chiu_2016_gdi_validation.py`](https://github.com/place-bot/Psychometrics-and-R-Shiny/blob/main/tools/de_la_torre_chiu_2016_gdi_validation.py) 实现：

- Table 1 的全部 16 个权重和成功概率；
- 任意候选 q-vector 的折叠权重和成功概率；
- GDI 与 PVAF；
- \(2^K-1\) 穷举；
- 阈值、最简性和平局规则；
- 论文的 \(30\times5\) Q；
- 高阶属性生成；
- Study 1 五种生成模型；
- 7/8 个随机 Q entry 错误；
- provisional G-DINA EM；
- entry 与 vector 两层恢复率。

## 精确核对

```bash
python3 tools/de_la_torre_chiu_2016_gdi_validation.py \
  --demo-only
```

输出：

```text
correct q=1110 GDI=0.029558
overspecified q=1111 GDI=0.029558
under+over q=0111 GDI=0.012524
collapsed group 000-: w=0.090, p=0.225
selected at epsilon=0.950: q=1110
```

它核对了三条理论主线：

\[
\varsigma^2(1110)
=
\varsigma^2(1111),
\]

\[
\varsigma^2(0111)
<
\varsigma^2(1110),
\]

\[
\text{并列时选择属性更少的 }1110.
\]

## 代码到公式

| Python 函数 | 数学对象 |
| --- | --- |
| `collapsed_success_profile()` | 式 (3)--(4) 的折叠 \(w,p\) |
| `gdi()` | \(\sum w(p-\bar p)^2\) |
| `exhaustive_search()` | GDI、PVAF、最简性决策 |
| `estimate_full_class_probabilities()` | \(\widehat p_{jl}\) 后验期望计数 |
| `higher_order_attributes()` | 论文高阶属性模型 |
| `simulate_study1_responses()` | 五种约化模型 |
| `randomly_misspecify_q()` | 7/8 个随机 entry 翻转 |
| `validate_one_dataset()` | provisional fit 到建议 Q |
| `q_recovery_summary()` | Tables 4--5 的四格率 |

## 快速随机检查

```bash
python3 tools/de_la_torre_chiu_2016_gdi_validation.py \
  --model DINA \
  --examinees 1200 \
  --replications 3
```

默认输出同时报告：

- EM 是否收敛；
- 平均迭代次数；
- 错误 entry 纠正率；
- 正确 entry 保留率；
- 错误 vector 纠正率；
- 正确 vector 保留率。

## 论文规模

```bash
python3 tools/de_la_torre_chiu_2016_gdi_validation.py \
  --model DINA \
  --paper-scale
```

这会使用：

\[
N=2000,\qquad R=100,
\]

前 50 份翻转 7 格，后 50 份翻转 8 格。

五个 Study 1 模型需分别运行：

```text
DINA
DINA-ACDM
ACDM
DINO-ACDM
DINO
```

## 精确复现与教学复现的边界

Table 1 是确定性精确复现。Monte Carlo 部分属于透明教学复现，数值不会逐格等于 Table 4，原因包括：

- 原文没有公开随机种子；
- 原文 Ox 初始化和收敛设置不完整；
- empirical Bayes EM 的实现细节没有全部给出；
- 随机翻转位置每次变化；
- 原文每个条件汇总 100 份数据。

脚本目前实现 Study 1。Study 2 的单调无约束概率抽样需要额外确定原文未详述的随机生成细节，因此原表应以论文 Table 5 为准。

## 数据边界

分数减法反应矩阵没有随论文公开在仓库中。本站复现其：

- Q；
- 项目文本；
- GDI/PVAF 表；
- 建议结果；
- 数字不一致记录。

没有声称重新计算 536 人原始反应数据。
