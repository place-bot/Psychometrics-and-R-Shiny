# 深度 Q-learning 完整算法

## 1. 论文算法的输入

初稿 Algorithm 1 接收：

| 参数 | 含义 |
|---|---|
| \(\gamma\) | 折扣因子 |
| \(\alpha\) | DQN 学习率 |
| \(\varepsilon_{\max}\) | 初始探索概率 |
| \(\varepsilon_{\min}\) | 最终探索概率 |
| \(\tau_\varepsilon\) | 探索衰减所需总步数 |
| \(M\) | mini-batch 大小 |
| \(E\) | episode 数，即训练学生数 |

输出是 DQN 参数 \(\mathbf w\)。

## 2. episode 与时间步

一个 episode 表示一名学生从初始能力学习到目标的完整过程。

```text
episode 1：学生 1 的完整学习路径
episode 2：学生 2 的完整学习路径
...
episode E：学生 E 的完整学习路径
```

在真实学生训练中，episode 数与学生数对应；使用转移模型时，可以反复生成虚拟 episode。

## 3. 探索率衰减

论文使用线性衰减：

\[
\varepsilon^{(t)}
=
\varepsilon_{\max}
-
\left(
\varepsilon_{\max}-\varepsilon_{\min}
\right)
\min\!\left(
\frac{\tau}{\tau_\varepsilon},
1
\right),
\tag{1}
\]

其中 \(\tau\) 是跨 episode 累计的环境步数。

于是：

- 初期 \(\varepsilon\) 高，广泛尝试材料；
- 随训练推进，随机动作比例下降；
- 衰减完成后保持 \(\varepsilon_{\min}\)。

## 4. epsilon-greedy 动作

\[
a^{(t)}
=
\begin{cases}
\text{从 }\mathcal A\text{ 随机抽取},
&
\text{概率 }\varepsilon^{(t)},
\\
\displaystyle
\arg\max_a
\widehat Q(s^{(t)},a;\mathbf w),
&
\text{概率 }1-\varepsilon^{(t)}.
\end{cases}
\tag{2}
\]

探索的作用是收集当前网络暂时不偏爱的动作结果。缺少探索时，早期误差可能让部分材料永远得不到数据。

## 5. 与学生环境交互

选出材料后：

1. 将材料 \(a^{(t)}\) 交给学生；
2. 学习结束后施测；
3. 用能力估计器获得 \(s^{(t+1)}\)；
4. 根据目标距离计算 \(r^{(t)}\)；
5. 保存 transition。

\[
\left(
s^{(t)},
a^{(t)},
r^{(t)},
s^{(t+1)}
\right)
\longrightarrow
\mathcal H.
\tag{3}
\]

\(\mathcal H\) 是经验回放池。

## 6. 经验回放

每个环境步从 \(\mathcal H\) 随机抽取 \(M\) 条转移：

\[
\mathcal M
\sim
\operatorname{UniformMiniBatch}(\mathcal H,M).
\tag{4}
\]

经验回放带来三项效果：

1. 同一条昂贵学生转移可被多次利用；
2. 随机抽样打散相邻步骤的强相关；
3. 每次更新同时覆盖不同学生和不同能力区域。

!!! warning "论文原文的表述"

    初稿称随机重采样用于减少样本导致的 bias。更准确地说，经验回放主要改善数据复用与相关性；它不能自动消除行为策略覆盖不足、测量误差或选择偏差。

## 7. 逐样本 TD target

对 mini-batch 中第 \(i\) 条转移：

\[
y_i
=
\begin{cases}
r_i,
&
\text{若 }s_i'\text{ 已终止},
\\
r_i+\gamma\max_{a'}\widehat Q(s_i',a';\mathbf w),
&
\text{若仍未终止}.
\end{cases}
\tag{5}
\]

然后最小化：

\[
\mathcal L_Q
=
\frac1M
\sum_{i=1}^M
\left(
\widehat Q(s_i,a_i;\mathbf w)-y_i
\right)^2.
\tag{6}
\]

每条转移只监督本次实际动作 \(a_i\) 对应的输出。

## 8. 终止条件

\[
\|s^{(t+1)}-\mathbf1_D\|_\infty<10^{-3}
\quad\Longrightarrow\quad
\text{episode 结束}.
\tag{7}
\]

实现中还应设置最大步数 \(T_{\max}\)，防止策略长期无法到达目标导致无限循环。

超时 transition 的处理需要明确：

- 把超时视为 truncation，并保留 bootstrap；
- 或把超时视为失败终止，并加失败惩罚。

两种处理对应不同目标。

## 9. 完整伪代码

```python
initialize online_q
initialize replay_buffer
global_step = 0

for episode in range(num_episodes):
    state = environment.reset()

    for step in range(max_steps):
        epsilon = linear_decay(global_step)
        action = epsilon_greedy(online_q, state, epsilon)

        next_state = environment.step(state, action)
        done = max_abs(next_state - target) < 1e-3
        reward = 0.0 if done else -1.0

        replay_buffer.add(
            state, action, reward, next_state, done
        )

        batch = replay_buffer.sample(batch_size)
        update_q_network(batch)

        state = next_state
        global_step += 1

        if done:
            break
```

此代码表达论文逻辑。工程版本还应加入 warm-up、target network、梯度裁剪、随机种子与检查点。

## 10. 论文模拟使用的超参数

| 项目 | 数值 |
|---|---:|
| DQN 隐藏层 | 64、32 |
| 训练 episode | 2000 |
| \(\gamma\) | 0.9 |
| \(\alpha\) | \(6\times10^{-4}\) |
| \(\varepsilon_{\max}\) | 1.0 |
| \(\varepsilon_{\min}\) | 0.1 |
| \(\tau_\varepsilon\) | 2000 个环境步 |
| mini-batch \(M\) | 256 |
| 优化器 | Adam |

## 11. 训练与部署的区别

### 训练

- 使用 \(\varepsilon\)-greedy；
- 收集和复用 transition；
- 计算 TD target；
- 更新网络参数。

### 部署

- 接收真实测量状态；
- 通常采用贪心动作；
- 不需要知道未来状态；
- 每轮学生反馈后重新决策。

若部署仍保留随机探索，应经过安全审查，且随机动作只能来自合格材料集合。

## 12. 合法动作约束

现实系统中的材料集合随状态变化：

\[
\mathcal A_{\text{valid}}(s)
\subseteq
\mathcal A.
\]

可能的硬约束包括：

- 先修知识尚未满足；
- 材料已经完成；
- 年龄或语言不适用；
- 无障碍条件不满足；
- 教师锁定或课程时间不允许。

贪心与 bootstrap 都应只在合法集合上计算：

\[
\max_{a'\in\mathcal A_{\text{valid}}(s')}
Q(s',a').
\tag{8}
\]

否则网络可能通过不可执行动作获得虚假的高目标值。

## 13. 离线数据的额外问题

论文算法按在线交互描述。若只有历史日志，数据来自旧策略 \(\mu(a\mid s)\)。未被旧策略选择的动作缺少反事实结果：

\[
\Pr_\mu(A=a\mid S=s)\approx0
\quad\Longrightarrow\quad
Q(s,a)\text{ 缺少直接证据}.
\]

部署前需要考虑：

- 行为策略覆盖；
- 保守离线 RL；
- 重要性加权或 doubly robust 评价；
- 小规模安全在线验证。
