# IRT 模型

这一部分整理项目反应理论（Item Response Theory, IRT）的模型族。当前先分成二分项目模型（binary item models）和多项项目模型（polytomous item models）。

## 学习顺序

1. [二分项目模型](../binary/index.md)：先学习 1PL、2PL、3PL、正态 Ogive、多维模型等用于对错题的数据模型。
2. [多项项目模型](../polytomous/index.md)：再学习 GRM、PCM、GPCM、RSM、NRM 等用于等级评分或多类别反应的数据模型。

## 二分项目模型

二分项目模型处理 \(0/1\) 反应数据，例如答错/答对、否/是、不通过/通过。核心问题是项目难度（difficulty）、区分度（discrimination）、猜测参数（guessing）和潜在能力（latent ability）如何共同决定答对概率。

## 多项项目模型

多项项目模型处理两个以上反应类别，例如 Likert 量表、部分给分题、等级评分题和名义类别反应。核心问题是类别阈值（thresholds）、步骤参数（step parameters）和类别反应曲线（category response curves）如何解释反应过程。

## 读模型时要统一看的问题

| 问题 | 说明 |
| --- | --- |
| 数据类型 | 模型适合二分、等级、多类别还是连续反应 |
| 潜变量结构 | 单维、多维、探索性还是验证性 |
| 参数含义 | 难度、区分度、猜测、阈值或步骤参数 |
| 可解释性 | 模型参数能否服务于测验解释和项目诊断 |
| 估计要求 | 样本量、局部独立、单维性和模型拟合要求 |
