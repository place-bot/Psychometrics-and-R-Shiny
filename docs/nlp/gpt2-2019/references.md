# 参考文献与一手资料

## 核心论文与官方材料

1. Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf). OpenAI technical report.
2. OpenAI. (2019). [Better language models and their implications](https://openai.com/index/better-language-models/).
3. OpenAI. [openai/gpt-2](https://github.com/openai/gpt-2): 官方 TensorFlow 模型、tokenizer 与采样代码。
4. OpenAI. [GPT-2 model card](https://github.com/openai/gpt-2/blob/master/model_card.md).
5. OpenAI. [GPT-2 output dataset](https://github.com/openai/gpt-2-output-dataset).

## 方法来源

6. Vaswani, A., et al. (2017). [Attention Is All You Need](https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need). NeurIPS 2017.
7. Radford, A., et al. (2018). [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf).
8. Sennrich, R., Haddow, B., & Birch, A. (2016). [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/). ACL 2016.
9. Ba, J. L., Kiros, J. R., & Hinton, G. E. (2016). [Layer Normalization](https://arxiv.org/abs/1607.06450).

## 解释与复核约定

- 论文数字按 2019 年官方报告表格记录；
- 模型参数计数同时标注官方仓库后来的修正；
- 代码章节以官方 `openai/gpt-2` 仓库的 `model.py`、`encoder.py` 与 `sample.py` 为依据；
- “zero-shot” 的重新分类依据 GPT-3 论文对 zero/one/few-shot 的定义。
