# Hugging Face Transformers

## 1. 它解决的核心问题

不同论文的 Transformer 在层数、注意力、位置编码、tokenizer 和输出头上各不相同。Transformers 用统一接口封装大量架构，使研究者可以从模型仓库读取配置、tokenizer 和权重，并完成推理、评测或训练。

典型加载过程是：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

`Auto*` 类先读取 `config.json` 中的 `model_type`，再选择对应的具体 Python 类。它并未创造一个新的通用架构，而是把“配置到实现类”的映射自动化。

## 2. 一套模型资产包含什么

| 文件或对象 | 作用 |
|---|---|
| `config.json` | 层数、hidden size、head 数、RoPE 等结构参数 |
| tokenizer 文件 | 词表、合并规则、normalizer 与特殊 token |
| `tokenizer_config.json` | tokenizer 行为与聊天模板 |
| SafeTensors shards | 模型权重张量 |
| generation config | 默认采样和停止设置 |
| model card | 训练、能力、限制、许可与使用说明 |

`from_pretrained()` 会下载并缓存这些资产，也可以从本地目录读取。生产环境应固定 `revision`，避免同一个 model ID 的仓库内容更新后结果变化。

## 3. chat template

聊天消息是结构化对象：

```python
messages = [
    {"role": "system", "content": "回答要简洁。"},
    {"role": "user", "content": "解释 Fisher 信息。"},
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
)
```

不同模型使用不同控制 token。模板承担：

\[
\{
\text{role},\text{content}
\}
\longrightarrow
\text{训练时见过的 token 序列}.
\]

错误模板会导致角色混淆、异常续写或工具调用格式失败。复制网页上肉眼相似的 `[INST]` 字符串不能替代模型自带模板。

## 4. `pipeline` 与底层 API

`pipeline` 把预处理、模型前向和后处理组合起来：

```python
from transformers import pipeline

generator = pipeline(
    task="text-generation",
    model=model_id,
)
result = generator("CAT 的目标是", max_new_tokens=80)
```

它适合快速验证。需要精细控制批处理、KV cache、logits processor、token-level 分数或训练循环时，应直接使用 tokenizer 与 model API。

## 5. 生成参数的作用

模型输出 logits \(z\)，temperature \(T\) 改变概率分布：

\[
p_i=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)}.
\]

- \(T<1\)：分布更尖锐；
- \(T>1\)：分布更平坦；
- greedy decoding：直接取最大 logit；
- top-p：只在累计概率达到 \(p\) 的最小候选集合中采样。

`max_new_tokens` 限制新生成长度，通常比把输入和输出混在一起计数的 `max_length` 更容易解释。

## 6. 量化与设备放置

Transformers 可以与 Accelerate、bitsandbytes、AWQ、GPTQ 等工具配合，使用低精度权重和自动 device map。量化配置改变的是权重表示与部分算子：

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

quant = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quant,
    device_map="auto",
)
```

量化会降低显存，可能引入任务相关误差。必须在最终量化版本上做评测，而非用全精度分数替代。

## 7. 训练能力

Transformers 的重要边界在于它不仅做推理，还支持：

- 预训练或继续预训练；
- supervised fine-tuning；
- 分类、标注、问答等任务微调；
- 与 PEFT 配合训练 LoRA；
- 保存、加载和上传新 checkpoint。

llama.cpp 的核心目标是高效推理；若研究重点是修改模型结构、计算训练梯度或进行大规模微调，Transformers/PyTorch 生态通常更直接。

## 8. 主要限制

- 通用抽象会带来 Python 与框架开销；
- 支持某架构不表示所有量化、工具调用和多模态路径都成熟；
- `trust_remote_code=True` 允许执行模型仓库代码，应只对可信 revision 使用；
- 单进程 `generate()` 适合实验，不等于高并发生产 serving；
- 模型权重许可证与 Transformers 库的 Apache 2.0 许可证是两件事。

