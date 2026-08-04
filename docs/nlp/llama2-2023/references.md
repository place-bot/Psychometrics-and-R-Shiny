# 参考文献与一手资料

## 核心论文与官方材料

1. Touvron, H., et al. (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288). arXiv:2307.09288.
2. Meta. [meta-llama/llama](https://github.com/meta-llama/llama): Llama 2 最小推理代码、模型卡、许可证与 Responsible Use Guide。
3. Meta. [Llama 2 model card](https://github.com/meta-llama/llama-models/blob/main/models/llama2/MODEL_CARD.md).
4. Meta. [Llama 2 Community License](https://github.com/meta-llama/llama/blob/main/LICENSE).
5. Meta. [Llama 2 Acceptable Use Policy](https://github.com/meta-llama/llama/blob/main/USE_POLICY.md).

## 架构与训练方法

6. Touvron, H., et al. (2023). [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971).
7. Zhang, B., & Sennrich, R. (2019). [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467).
8. Shazeer, N. (2020). [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202).
9. Su, J., et al. (2021). [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864).
10. Ainslie, J., et al. (2023). [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245).

## 对齐方法

11. Ouyang, L., et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](https://arxiv.org/abs/2203.02155).
12. Stiennon, N., et al. (2020). [Learning to Summarize from Human Feedback](https://proceedings.neurips.cc/paper/2020/hash/1f89885d556929e98d3ef9b86448f951-Abstract.html).
13. Schulman, J., et al. (2017). [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347).
14. Bai, Y., et al. (2022). [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862).

## 核查约定

- 模型配置、实验数字、RLHF 公式与安全流程均按论文正文及附录记录；
- 代码章节以官方 Llama 2 推理仓库的 `model.py`、`generation.py` 与 `tokenizer.py` 为依据；
- 发布性质使用“开放权重”，许可条件以官方许可证原文为准；
- 论文的 34B 研究结果与公开下载模型范围分别表述。
