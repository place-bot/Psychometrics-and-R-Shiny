# 论文、官方代码与参考资料

## BPE

- Gage, P. (1994). [A New Algorithm for Data Compression](https://www.derczynski.com/papers/archive/BPE_Gage.pdf). *The C Users Journal*, 12(2), 23–38.
- Sennrich, R., Haddow, B., & Birch, A. (2016). [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/). *ACL 2016*, 1715–1725.
- Sennrich et al. [subword-nmt official repository](https://github.com/rsennrich/subword-nmt).

## WordPiece 与 BERT

- Schuster, M., & Nakajima, K. (2012). [Japanese and Korean Voice Search](https://doi.org/10.1109/ICASSP.2012.6289079). *ICASSP 2012*, 5149–5152.
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423/).
- Google Research. [BERT official repository](https://github.com/google-research/bert).
- Google Research. [BERT `tokenization.py`](https://github.com/google-research/bert/blob/master/tokenization.py).

## Byte-level BPE 与 GPT-2

- Radford, A. et al. (2019). [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).
- OpenAI. [GPT-2 official repository](https://github.com/openai/gpt-2).
- OpenAI. [GPT-2 `encoder.py`](https://github.com/openai/gpt-2/blob/master/src/encoder.py).

## 现代实现与相邻方法

- Kudo, T., & Richardson, J. (2018). [SentencePiece: A Simple and Language Independent Subword Tokenizer and Detokenizer for Neural Text Processing](https://aclanthology.org/D18-2012/).
- Google. [SentencePiece official repository](https://github.com/google/sentencepiece).
- Hugging Face. [Tokenizers official repository](https://github.com/huggingface/tokenizers).
- Hugging Face. [Tokenization algorithms summary](https://huggingface.co/docs/transformers/main/tokenizer_summary).
- Hugging Face. [WordPiece training reconstruction](https://huggingface.co/learn/llm-course/chapter6/6).

!!! note "关于 WordPiece 训练细节"
    BERT 官方仓库没有发布当年 WordPiece vocabulary trainer。Hugging Face 的教学实现明确标注为根据文献进行的重构。本专题因此把 likelihood 原理、常见 pair score 与 BERT 已公开的 runtime tokenizer 分开描述。

