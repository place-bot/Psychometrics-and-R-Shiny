# 基础模型实验与证据分析

## 1. 评测分组

论文把标准 benchmark 汇总为：

- Code：HumanEval 与 MBPP 的 pass@1；
- Commonsense：PIQA、SIQA、HellaSwag、WinoGrande、ARC、OpenBookQA、CommonsenseQA；
- World Knowledge：NaturalQuestions、TriviaQA；
- Reading Comprehension：SQuAD、QuAC、BoolQ；
- Math：GSM8K 与 MATH；
- MMLU、BBH、AGI Eval。

不同组使用 0-shot、3-shot、4-shot、5-shot、7-shot 或 8-shot。表中各列不是同一种数据规模与难度。

## 2. 汇总结果

| 模型 | Code | Commonsense | World Knowledge | Reading | Math | MMLU | BBH | AGI Eval |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Llama 1 7B | 14.1 | 60.8 | 46.2 | 58.5 | 6.95 | 35.1 | 30.3 | 23.9 |
| Llama 2 7B | 16.8 | 63.9 | 48.9 | 61.3 | 14.6 | 45.3 | 32.6 | 29.3 |
| Llama 1 13B | 18.9 | 66.1 | 52.6 | 62.3 | 10.9 | 46.9 | 37.0 | 33.9 |
| Llama 2 13B | 24.5 | 66.9 | 55.4 | 65.8 | 28.7 | 54.8 | 39.4 | 39.1 |
| Llama 1 65B | 30.7 | 70.7 | 60.5 | 68.6 | 30.8 | 63.4 | 43.5 | 47.6 |
| Llama 2 70B | **37.5** | **71.9** | **63.6** | **69.4** | **35.2** | **68.9** | **51.2** | **54.2** |

同规模附近的 Llama 2 普遍优于 Llama 1，说明更多训练 token、数据更新、4K context 和架构调整共同有效。

## 3. 与当时开放模型比较

论文内部复评 MPT 与 Falcon，并在内部结果和公开结果中取较高者。Llama 2 70B 在汇总表中优于所列开放基础模型；7B 与 34B 也普遍优于相邻规模 Falcon，代码 benchmark 存在例外。

## 4. 与闭源模型比较

| Benchmark | GPT-3.5 | GPT-4 | PaLM | PaLM-2-L | Llama 2 70B |
|---|---:|---:|---:|---:|---:|
| MMLU 5-shot | 70.0 | 86.4 | 69.3 | 78.3 | 68.9 |
| TriviaQA 1-shot | — | — | 81.4 | 86.1 | 85.0 |
| Natural Questions 1-shot | — | — | 29.3 | 37.5 | 33.0 |
| GSM8K 8-shot | 57.1 | 92.0 | 56.5 | 80.7 | 56.8 |
| HumanEval 0-shot | 48.1 | 67.0 | 26.2 | — | 29.9 |
| BBH 3-shot | — | — | 52.3 | 65.7 | 51.2 |

Llama 2 70B 接近 GPT-3.5 的 MMLU/GSM8K，明显落后于 GPT-4，在代码任务也有较大差距。

## 5. 安全 benchmark：base model

| Base model | TruthfulQA ↑ | ToxiGen ↓ |
|---|---:|---:|
| Llama 1 7B | 27.42 | 23.00 |
| Llama 2 7B | 33.29 | 21.25 |
| Llama 2 13B | 41.86 | 26.10 |
| Llama 2 34B | 43.45 | 21.19 |
| Llama 2 70B | 50.18 | 24.60 |

更大 base model 的 truthfulness 通常提高，toxicity 没有随规模单调下降。70B 的基础模型仍需要安全调优。

## 6. 比较边界

- benchmark 来自不同文献，prompt 和实现可能不同；
- 内部框架重跑与公开数字取最优会带来选择优势；
- 闭源模型版本可能随时间变化；
- 分组平均掩盖子任务差异；
- 训练数据规模、许可、上下文和计算不相等；
- 数据 contamination 只能做部分审计。

这些表支持 Llama 2 base 的竞争力，不能替代任务级、部署级评估。
