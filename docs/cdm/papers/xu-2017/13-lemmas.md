# 两个技术引理

主证明多次把若干差值相乘。要保证选择行真正留下一个可用的非零元素，就必须排除某些“跨两套参数”的意外相等。引理 1 和引理 2承担这项工作。

## 引理 1

若主定理条件成立且式 (3.5) 成立，对任意 \(k\) 与任意
\(\boldsymbol\alpha^*\succeq\boldsymbol e_k\)：

\[
\theta_{k,\boldsymbol0}
\ne
\bar\theta_{k,\boldsymbol\alpha^*},
\qquad
\theta_{k,\boldsymbol\alpha^*}
\ne
\bar\theta_{k,\boldsymbol0},
\]

\[
\theta_{K+k,\boldsymbol0}
\ne
\bar\theta_{K+k,\boldsymbol\alpha^*},
\qquad
\theta_{K+k,\boldsymbol\alpha^*}
\ne
\bar\theta_{K+k,\boldsymbol0}.
\]

### 证明逻辑

假设

\[
\theta_{k,\boldsymbol0}
=
\bar\theta_{k,\boldsymbol\alpha^*}.
\]

第 \(k\) 题是单属性题。由单调限制，在无横线参数中

\[
\theta_{k,\boldsymbol\alpha}
\ge
\theta_{k,\boldsymbol0}
\quad\forall\boldsymbol\alpha,
\]

并且有正比例落在严格更高的能力充分类，所以

\[
\sum_{\boldsymbol\alpha}
\theta_{k,\boldsymbol\alpha}p_{\boldsymbol\alpha}
>
\theta_{k,\boldsymbol0}.
\]

带横线参数的
\(\bar\theta_{k,\boldsymbol\alpha^*}\) 是该题的最高概率，因此

\[
\sum_{\boldsymbol\alpha}
\bar\theta_{k,\boldsymbol\alpha}
\bar p_{\boldsymbol\alpha}
<
\bar\theta_{k,\boldsymbol\alpha^*}.
\]

代入假设的相等值后，两套模型的第 \(k\) 题边际成功率无法相等，与式 (3.5) 矛盾。

其余三个不等式按相同对称论证得到。

## 引理 2

对任意 \(1\le k\ne h\le K\)：

\[
\theta_{k,\boldsymbol e_h}
\ne
\bar\theta_{k,\boldsymbol1},
\qquad
\theta_{k,\boldsymbol1}
\ne
\bar\theta_{k,\boldsymbol e_h},
\]

\[
\theta_{K+k,\boldsymbol e_h}
\ne
\bar\theta_{K+k,\boldsymbol1},
\qquad
\theta_{K+k,\boldsymbol1}
\ne
\bar\theta_{K+k,\boldsymbol e_h}.
\]

这里第 \(k\) 道单属性题要求属性 \(k\)，而
\(\boldsymbol e_h\) 没有属性 \(k\)。

## 引理 2 为什么更难

引理 1 比较某题的跨模型最低值与最高值，可直接用边际均值的严格夹逼。

引理 2 比较的是：

- 一套模型中能力不足类 \(\boldsymbol e_h\) 的概率；
- 另一套模型中能力充分类 \(\boldsymbol1\) 的概率。

仅看一题边际无法完成同样的夹逼。论文还要借用：

1. 第二个 \(I_K\) 块对应的 \(T\)-子矩阵；
2. 平移后该子矩阵的三角结构与满秩；
3. 一个线性组合，选出某个潜在类列；
4. C2 在剩余题中提供的 \(\boldsymbol0/\boldsymbol e_k\) 对比；
5. 模型内最高概率严格大于能力不足概率。

这些结构共同把假设的跨模型相等转化为模型内部次序矛盾。

## 满秩子矩阵的角色

第二个 \(I_K\) 块形成一个

\[
2^K\times2^K
\]

的 \(T\)-子矩阵。适当平移并重排列后，它呈三角形，对角元由严格概率差构成，因此非零并满秩。

满秩意味着可以找到一个行向量 \(\boldsymbol m\)，使

\[
\boldsymbol m
T(Q_1,\bar\Theta_{K+1:2K})
\]

只在指定属性列取值 1，其余列为 0。这个“列选择器”让证明能够追踪原本混在一起的潜在类。

## 两个引理的共同作用

证明中出现的关键系数形如

\[
\prod_k
\left(
\theta_{k,\boldsymbol\alpha}
-\bar\theta_{k,\boldsymbol\beta}
\right).
\]

只要一个因子为零，原计划隔离的列就会消失。引理给出了恰好需要的非零保证，使每次比值或消元都合法。

## 假设依赖

引理依赖：

- 每个 \(p_{\boldsymbol\alpha}>0\)；
- 单属性题的严格分离式 (2.3)；
- C1 的两个单位块；
- 引理 2 还使用 C2 形成的剩余题对比。

因此不能在允许结构零、无严格单调或缺少第二锚定块的模型里直接照搬。
