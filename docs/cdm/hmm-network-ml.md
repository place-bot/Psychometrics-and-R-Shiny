# HMM、网络与机器学习背景

这一页不作为 CDM 主线，但保留相关背景文献。它们帮助理解隐藏状态模型（hidden-state models）、随机块模型（stochastic block models）、聚类（clustering）和 EM 式半监督学习（EM-like semi-supervised learning）。

## 隐马尔可夫模型与概率自动机

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Cappé, Moulines & Rydén (2005). Inference in Hidden Markov Models. | `cdm/papers/cappe-moulines-ryden-2005-hmm.md` | HMM 推断、EM 和状态估计的系统背景。 |
| 主读 | Ephraim & Merhav (2002). Hidden Markov processes. | `cdm/papers/ephraim-merhav-2002-hidden-markov-processes.md` | 隐马尔可夫过程（hidden Markov processes）的理论综述。 |
| 背景 | Gilbert (1959). On the identifiability problem for functions of finite Markov chains. | `cdm/papers/gilbert-1959-markov-identifiability.md` | 早期 HMM/Markov function 识别问题。 |
| 背景 | Petrie (1969). Probabilistic functions of finite state Markov chains. | `cdm/papers/petrie-1969-probabilistic-functions.md` | 和 Gilbert 互补，读 identifiability 相关部分。 |
| 背景 | Paz (1971). Introduction to Probabilistic Automata. | `cdm/papers/paz-1971-probabilistic-automata.md` | 概率自动机（probabilistic automata）的基础背景。 |
| 背景 | Finesso (1991). Consistent estimation of the order for Markov and hidden Markov chains. | `cdm/papers/finesso-1991-markov-order.md` | 模型阶数估计（order estimation）背景。 |
| 背景 | Leroux (1992). Maximum-likelihood estimation for hidden Markov models. | `cdm/papers/leroux-1992-hmm-mle.md` | HMM 最大似然估计（maximum likelihood estimation）背景。 |
| 背景 | Chambaz & Matias (2009). Number of hidden states and memory: A joint order estimation problem for Markov chains with Markov regime. | `cdm/papers/chambaz-matias-2009-hidden-states-memory.md` | 隐状态数量和记忆阶数的联合估计。 |

## 网络、块模型与分类

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Nowicki & Snijders (2001). Estimation and prediction for stochastic blockstructures. | `cdm/papers/nowicki-snijders-2001-stochastic-blockstructures.md` | 随机块结构（stochastic blockstructures）的估计和预测。 |
| 主读 | Daudin, Picard & Robin (2008). A mixture model for random graphs. | `cdm/papers/daudin-picard-robin-2008-random-graphs.md` | 随机图 mixture model，和 latent class/block model 有交叉。 |
| 背景 | Zanghi, Ambroise & Miele (2008). Fast online graph clustering via Erdős-Rényi mixture. | `cdm/papers/zanghi-ambroise-miele-2008-graph-clustering.md` | 图聚类（graph clustering）和在线估计背景。 |
| 背景 | Frank & Harary (1982). Cluster inference by using transitivity indices in empirical graphs. | `cdm/papers/frank-harary-1982-cluster-inference.md` | 图聚类和 transitivity indices 的早期背景。 |
| 背景 | Glick (1973). Sample-based multinomial classification. | `cdm/papers/glick-1973-multinomial-classification.md` | 多项分类（multinomial classification）的经典背景。 |
| 背景 | Tallberg (2005). A Bayesian approach to modeling stochastic blockstructures with covariates. | `cdm/papers/tallberg-2005-bayesian-blockstructures.md` | 带协变量的贝叶斯块模型。 |

## 机器学习背景

| 阅读级别 | 文献 | 后续单篇笔记位置 | 读法 |
| --- | --- | --- | --- |
| 主读 | Nigam, McCallum, Thrun & Mitchell (2000). Text classification from labeled and unlabeled documents using EM. | `cdm/papers/nigam-mccallum-thrun-mitchell-2000-text-em.md` | 半监督文本分类和 EM 学习，适合和 Q 矩阵文本分类方法对照。 |

## 和 CDM 的关系

这一页的文献主要用于补方法背景，不直接决定 CDM 章节的主线。后续写作时可以按需要引用：

- HMM 文献：用于理解隐藏状态识别和动态 CDM。
- 网络文献：用于理解 latent block structure 和聚类。
- 机器学习文献：用于理解文本辅助 Q 矩阵学习和 AI 辅助 Q 矩阵开发。
