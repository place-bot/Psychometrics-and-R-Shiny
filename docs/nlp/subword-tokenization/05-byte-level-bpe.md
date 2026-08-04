# GPT-2 的 Byte-level BPE

## 1. 为什么改到字节层

Unicode code point 数量远大于常见 32K–64K 子词词表。若把所有可能字符作为基础 alphabet，初始词表本身就会很大。UTF-8 只由 256 种字节值构成：

\[
\mathcal B=\{0,1,\ldots,255\}.
\]

因此任意有效 UTF-8 文本都能先表示为字节序列，再通过合并获得常见长片段。

## 2. GPT-2 不是直接在不可打印字节上操作

GPT-2 官方 encoder 建立可逆映射：

\[
\phi:\{0,\ldots,255\}\longrightarrow\mathcal U_{256},
\]

其中 \(\mathcal U_{256}\) 是 256 个便于正则和字符串代码处理的 Unicode 符号。可打印字符尽量保持直观；空白和控制字节映射到额外符号。

于是：

```text
文本
→ UTF-8 bytes
→ 可打印 Unicode 代理符号
→ BPE merges
→ vocabulary IDs
```

## 3. `Ġ` 到底是什么

GPT-2 的映射中，空格字节会显示成 `Ġ`。例如 token `Ġcat` 通常表示其底层字节以空格开头，后接 `cat`。

`Ġ` 不是英语词法符号，也不是原文真的含有该字符。它是字节到可打印 Unicode 映射的可视化结果。

这使：

```text
"cat"  与  " cat"
```

可以拥有不同 token。词首空格成为 token pattern 的一部分。

## 4. 正则 Pre-tokenization

GPT-2 官方实现先用正则区分：

- 常见英语缩写后缀；
- 连续字母；
- 连续数字；
- 非空白、非字母数字的符号；
- 空白。

某些分支允许片段带一个前导空格。每个 regex match 分别执行 byte mapping 和 BPE，所以 merge 不会任意跨越这些 match 边界。

## 5. 编码过程

对每个 regex 片段 \(q\)：

\[
b(q)=\operatorname{UTF8}(q),
\]

\[
u(q)=\phi(b_1)\phi(b_2)\cdots\phi(b_m),
\]

\[
s(q)=\operatorname{BPE}_{r}(u(q)),
\]

最后把每个 subtoken 查表为 ID。

## 6. 解码过程

\[
\text{IDs}
\rightarrow
\text{BPE token strings}
\rightarrow
\text{拼接代理 Unicode}
\rightarrow
\phi^{-1}
\rightarrow
\text{UTF-8 decode}.
\]

只要输入是有效文本且没有额外不可逆 normalization，整个流程可以恢复原始字节。

## 7. “没有 UNK”意味着什么

256 个基础字节始终提供 fallback，因此任意 UTF-8 字符串都可以编码。罕见字符可能拆成多个 token，例如一个 emoji 的 UTF-8 表示通常占多个字节。

覆盖保证与效率是两回事：

- 常见英文片段可能一个 token 覆盖多个字符；
- 训练中少见的文字可能每个字符占多个 token；
- 看似相同的 Unicode 字符序列若 normalization 不同，字节也可能不同。

## 8. GPT 家族的表述边界

GPT-2 明确公开了 byte-to-Unicode map、regex、merge ranks 和 vocabulary。后续 GPT tokenizer 仍采用字节级、merge-based 的核心思路，但词表规模、正则、merge list 与特殊 token 已经变化。

因此“GPT 使用 BPE”应理解成架构路线概括，不能用 GPT-2 的 `encoder.json` 直接编码所有后续 GPT 模型。

