# 实现蓝图与检查清单

论文给出算法伪代码，没有提供可确认的官方公开代码仓库。本页根据初稿 Algorithm 1、网络描述和实验参数整理可复现实现，并把论文未规定的工程选择单独标出。

## 1. 推荐的模块边界

```text
AbilityEstimator
    └── responses -> state

StudentEnvironment
    └── (state, material) -> next_state

TransitionModel
    └── fit real transitions
    └── (state, material) -> predicted next_state

QNetwork
    └── state -> Q value for every material

ReplayBuffer
    └── store and sample transitions

DQNTrainer
    └── exploration, TD target, optimization
```

模块分离便于单独验证测量误差、环境误差和策略误差。

## 2. transition 数据结构

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class Transition:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    terminated: bool
    truncated: bool
```

建议区分：

- `terminated`：达到能力目标；
- `truncated`：达到最大轮数或外部中断。

两者的 bootstrap 规则可以不同。

## 3. 论文模拟环境

下面用剩余能力空间缩放 Beta 增量，对应：

\[
\Delta\theta_d=(1-\theta_d)Z_d.
\]

```python
import numpy as np

class SimulatedLearner:
    def __init__(self, rng, threshold=1e-3):
        self.rng = rng
        self.threshold = threshold
        self.state = np.zeros(2, dtype=np.float32)

    def reset(self):
        self.state = np.zeros(2, dtype=np.float32)
        return self.state.copy()

    def _g1(self, state, action):
        theta1, theta2 = state
        if action == 0:
            return 3 + 8 * theta1 - 0.2 * theta2
        if action == 2:
            return 15 + 15 * theta1 - 0.4 * theta2
        return None

    def _g2(self, state, action, delta1):
        theta1, theta2 = state
        if action == 1:
            return 10 - theta1 + 5 * theta2
        if action == 2:
            bump = np.exp(-((theta1 - 0.6) ** 2) / 0.3)
            return (
                20
                - 28 * theta1 * bump
                + 30 * theta2
                - 0.3 * delta1
            )
        return None

    def step(self, action):
        theta1, theta2 = self.state

        delta1 = 0.0
        if action in (0, 2):
            z1 = self.rng.beta(1.0, self._g1(self.state, action))
            delta1 = (1.0 - theta1) * z1

        delta2 = 0.0
        if action in (1, 2):
            z2 = self.rng.beta(
                1.0,
                self._g2(self.state, action, delta1),
            )
            delta2 = (1.0 - theta2) * z2

        next_state = np.clip(
            self.state + np.array([delta1, delta2]),
            0.0,
            1.0,
        ).astype(np.float32)

        terminated = np.max(np.abs(next_state - 1.0)) < self.threshold
        reward = 0.0 if terminated else -1.0
        self.state = next_state
        return next_state.copy(), reward, terminated
```

!!! warning "复现选择"

    论文没有明确说明 Beta 样本如何映射到 \([0,1-\theta_d]\)。上面的剩余空间缩放是一种合理实现，不能当作作者代码的已确认行为。

## 4. Q 网络

论文结构为二维输入、64 和 32 单元隐藏层、三维输出：

```python
import torch
from torch import nn

class QNetwork(nn.Module):
    def __init__(self, state_dim=2, action_dim=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim),
        )

    def forward(self, state):
        return self.net(state)
```

输出层不使用 softmax。Q 值是实数长期价值，不需要和为 1。

## 5. 经验回放

```python
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity):
        self.data = deque(maxlen=capacity)

    def add(self, transition):
        self.data.append(transition)

    def sample(self, batch_size):
        return random.sample(self.data, batch_size)

    def __len__(self):
        return len(self.data)
```

论文未报告 buffer capacity 和 warm-up 长度。复现时应在配置文件中显式记录。

## 6. epsilon 调度

```python
def epsilon_at_step(
    step,
    epsilon_start=1.0,
    epsilon_end=0.1,
    decay_steps=2000,
):
    fraction = min(step / decay_steps, 1.0)
    return (
        epsilon_start
        - (epsilon_start - epsilon_end) * fraction
    )
```

动作选择：

```python
def select_action(q_network, state, epsilon, rng, valid_mask=None):
    if rng.random() < epsilon:
        if valid_mask is None:
            return int(rng.integers(0, 3))
        candidates = np.flatnonzero(valid_mask)
        return int(rng.choice(candidates))

    state_tensor = torch.as_tensor(
        state, dtype=torch.float32
    ).unsqueeze(0)

    with torch.no_grad():
        q_values = q_network(state_tensor).squeeze(0)

    if valid_mask is not None:
        mask = torch.as_tensor(valid_mask, dtype=torch.bool)
        q_values = q_values.masked_fill(~mask, float("-inf"))

    return int(torch.argmax(q_values).item())
```

## 7. 批量 TD 更新

现代稳定版使用 target network：

```python
import torch.nn.functional as F

def dqn_update(
    online_q,
    target_q,
    optimizer,
    batch,
    gamma=0.9,
):
    states = torch.as_tensor(
        np.stack([x.state for x in batch]),
        dtype=torch.float32,
    )
    actions = torch.as_tensor(
        [x.action for x in batch],
        dtype=torch.long,
    )
    rewards = torch.as_tensor(
        [x.reward for x in batch],
        dtype=torch.float32,
    )
    next_states = torch.as_tensor(
        np.stack([x.next_state for x in batch]),
        dtype=torch.float32,
    )
    terminated = torch.as_tensor(
        [x.terminated for x in batch],
        dtype=torch.float32,
    )

    predicted = online_q(states).gather(
        1, actions[:, None]
    ).squeeze(1)

    with torch.no_grad():
        next_value = target_q(next_states).max(dim=1).values
        target = rewards + gamma * (1.0 - terminated) * next_value

    loss = F.mse_loss(predicted, target)

    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(online_q.parameters(), 10.0)
    optimizer.step()
    return float(loss.item())
```

复刻论文同网 bootstrap 时，可用 `online_q` 计算 `next_value`；应把这个差异写入实验报告。

## 8. 转移模型

```python
class TransitionModel(nn.Module):
    def __init__(self, state_dim=2, action_dim=3):
        super().__init__()
        self.action_dim = action_dim
        self.net = nn.Sequential(
            nn.Linear(state_dim + action_dim, 32),
            nn.ReLU(),
            nn.Linear(32, state_dim),
            nn.Sigmoid(),
        )

    def forward(self, state, action):
        one_hot = F.one_hot(
            action,
            num_classes=self.action_dim,
        ).float()
        inputs = torch.cat([state, one_hot], dim=-1)
        return self.net(inputs)
```

训练损失：

\[
\mathcal L_{\text{transition}}
=
\frac1H
\sum_{i=1}^{H}
\|
\psi_v(s_i,a_i)-s_i'
\|_2^2.
\]

若要强制单调，可让网络输出非负增量，并裁剪到剩余能力空间。

## 9. 真实系统的能力估计接口

```python
class AbilityEstimator:
    def fit_or_update(self, responses, item_bank):
        """
        Return:
            mean: posterior/MAP/EAP ability estimate
            uncertainty: covariance or standard error
        """
        raise NotImplementedError
```

建议保存：

- 能力点估计；
- 标准误或后验协方差；
- 测试题数；
- 模型拟合状态；
- 能力尺度版本。

只保存一个浮点向量会丢失关键测量信息。

## 10. 训练日志

每个 episode 至少记录：

| 字段 | 用途 |
|---|---|
| episode reward | 策略性能 |
| episode length | 目标到达效率 |
| epsilon | 探索状态 |
| TD loss | 优化诊断 |
| Q 均值与范围 | 过估计和发散检查 |
| 动作频率 | 材料覆盖 |
| 终止率 | 是否经常超时 |
| 状态覆盖 | 外推风险 |
| 转移模型 \(R^2\)/RMSE | 模型拟合 |
| 多步 rollout error | 长轨迹可靠性 |

## 11. 最低限度测试

### 数学测试

- 目标状态奖励为 0；
- 非目标状态奖励为 \(-1\)；
- terminal target 无 bootstrap；
- epsilon 衰减端点正确；
- mask 后无法选到非法动作。

### 环境测试

- 状态始终位于 \([0,1]^D\)；
- 在单调假设下 \(s_{t+1}\ge s_t\)；
- 随机种子可复现；
- 每个 episode 有最大步数。

### 策略测试

- 全随机策略是可复现 baseline；
- 手工环境中的最优动作与解析结果一致；
- target network 同步频率正确；
- 保存后加载的策略输出一致。

## 12. 论文复刻与工程增强要分开

建议报告两套配置：

| 配置 | 目的 |
|---|---|
| Paper-like | 尽量遵循论文同网 target、网络和超参数 |
| Stable DQN | target network、Double DQN、梯度裁剪、明确 truncation |

先复刻论文结论，再判断工程增强是否改善结果，可以避免把算法差异误当作复现误差。

## 13. 现实部署门槛

上线前还需：

1. 经过内容专家审核的合法动作集合；
2. 离线覆盖与反事实评价；
3. 转移模型不确定性监控；
4. 教师覆写和安全回退；
5. 学生退出、负荷和公平性指标；
6. 版本化的能力尺度与材料库；
7. 受控在线试验。
