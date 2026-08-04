# 完整手算：BPE 与 WordPiece

## 1. 小语料

使用带频数的五个词：

| 词 | 频数 |
|---|---:|
| `hug` | 10 |
| `pug` | 5 |
| `pun` | 12 |
| `bun` | 4 |
| `hugs` | 5 |

为了突出合并标准，这里暂不加词尾 token。

## 2. BPE 初始化

```text
hug  ×10 → h u g
pug  × 5 → p u g
pun  ×12 → p u n
bun  × 4 → b u n
hugs × 5 → h u g s
```

相邻 pair 频数：

| Pair | 计算 | 频数 |
|---|---|---:|
| `(h,u)` | 10 + 5 | 15 |
| `(p,u)` | 5 + 12 | 17 |
| `(b,u)` | 4 | 4 |
| `(u,g)` | 10 + 5 + 5 | 20 |
| `(u,n)` | 12 + 4 | 16 |
| `(g,s)` | 5 | 5 |

最高频 pair 是 `(u,g)`，第一轮：

```text
u + g → ug
```

新切分：

```text
h ug   ×10
p ug   × 5
p u n  ×12
b u n  × 4
h ug s × 5
```

## 3. BPE 第二轮

主要 pair 频数：

| Pair | 频数 |
|---|---:|
| `(h,ug)` | 15 |
| `(p,ug)` | 5 |
| `(p,u)` | 12 |
| `(b,u)` | 4 |
| `(u,n)` | 16 |
| `(ug,s)` | 5 |

最高为 `(u,n)`：

```text
u + n → un
```

得到：

```text
h ug   ×10
p ug   × 5
p un   ×12
b un   × 4
h ug s × 5
```

## 4. BPE 第三轮

`(h,ug)` 频数为 15，是当前最高：

```text
h + ug → hug
```

得到：

```text
hug    ×10
p ug   × 5
p un   ×12
b un   × 4
hug s  × 5
```

前三条 merge rules 是：

```text
rank 0: u g
rank 1: u n
rank 2: h ug
```

## 5. 用这套 BPE 编码 `hugs`

```text
h u g s
→ h ug s       # 使用 rank 0
→ hug s        # 使用 rank 2
```

如果还没有学到 `hug + s`，最终输出 `hug | s`。

## 6. WordPiece 初始化

用 `##` 标记非词首位置：

```text
h ##u ##g       ×10
p ##u ##g       × 5
p ##u ##n       ×12
b ##u ##n       × 4
h ##u ##g ##s   × 5
```

各单位频数：

| 单位 | 频数 |
|---|---:|
| `h` | 15 |
| `p` | 17 |
| `b` | 4 |
| `##u` | 36 |
| `##g` | 20 |
| `##n` | 16 |
| `##s` | 5 |

## 7. 计算常见 WordPiece Score

对 `(##u, ##g)`：

\[
\frac{20}{36\times20}=\frac{1}{36}.
\]

对 `(h, ##u)`：

\[
\frac{15}{15\times36}=\frac{1}{36}.
\]

对 `(##g, ##s)`：

\[
\frac{5}{20\times5}=\frac{1}{20}.
\]

虽然 `(##g, ##s)` 只出现 5 次，它的 score 最高，因此常见的 WordPiece trainer 重构会先合并：

```text
##g + ##s → ##gs
```

BPE 第一轮选择了绝对频数 20 的 `u+g`，二者已经产生不同 merge history。

## 8. 运行时切分也可能不同

假设最终 WordPiece vocabulary 含：

```text
hug, ##s, hu, ##gs
```

longest-match-first 编码 `hugs`：

```text
hugs → hug | ##s
```

若一套 BPE merge order 先形成 `hu` 和 `gs`，它可能编码为：

```text
hugs → hu | gs
```

最终结果由各自真实词表和规则决定。这个例子展示算法机制，不代表 BERT 或 GPT-2 的真实词表一定这样切分。

## 9. 手算结论

1. BPE 训练比较 pair 的绝对频数；
2. 常见 WordPiece score 会考虑组成部分的边际频率；
3. BPE 编码重放 merge priority；
4. WordPiece 编码对最终 vocabulary 做最长前缀匹配；
5. 训练标准和运行时算法都可能让二者产生不同 token 序列。

