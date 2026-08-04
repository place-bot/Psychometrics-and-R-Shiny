# LangChain：模型、工具、检索与 agent 编排

## 1. LangChain 在哪一层

LangChain 主要管理“模型调用前后发生什么”。它通过统一接口连接云端模型或本地服务，并把模型与 prompt、检索器、工具、结构化输出和状态组合起来。

它通常不负责执行模型内部的 Transformer 矩阵乘法。实际 forward pass 可以发生在 llama.cpp、Transformers、vLLM 或某个远程 API 中。

## 2. 基本模型接口

LangChain 把不同供应商或本地服务封装成消息接口：

```python
response = model.invoke([
    {"role": "system", "content": "你是 CAT 研究助手。"},
    {"role": "user", "content": "解释项目曝光控制。"},
])
```

这种抽象方便替换 provider，但“统一接口”不表示底层模型能力相同。工具调用格式、上下文、结构化输出和错误处理仍需按 provider 验证。

## 3. RAG 流水线

一个两阶段 RAG 可以写成：

```text
文档 → 切分 → embedding → vector store
                              ↑
问题 → query embedding → 检索 top-k
                              ↓
              prompt + retrieved context
                              ↓
                            LLM
```

检索阶段：

\[
D_k=\operatorname{TopK}_{d\in\mathcal D}
\operatorname{sim}(e(q),e(d)).
\]

生成阶段：

\[
y\sim p_\theta(y\mid q,D_k).
\]

LangChain 提供 document loaders、splitters、embeddings、vector stores 和 retrievers 的接口。它减少连接代码，不会自动选出正确的 chunk size、embedding 模型或 top-\(k\)。

## 4. Tool calling

工具由名称、描述、输入 schema 和可执行函数组成：

```python
from langchain.tools import tool

@tool
def item_statistics(item_id: str) -> dict:
    """读取指定题目的校准参数。"""
    return {"item_id": item_id, "difficulty": 0.42}
```

模型输出的是“调用哪个工具、填什么参数”的请求，框架负责实际执行函数，再把结果返回模型。安全边界必须由代码建立：

- 工具最小权限；
- schema 校验；
- 网络与文件沙箱；
- 高风险操作人工确认；
- 超时、重试、幂等与审计日志。

## 5. Agent 循环

当前 LangChain agent 建立在 LangGraph 运行时上。简化循环为：

\[
s_{t+1}=
\begin{cases}
\operatorname{ExecuteTool}(a_t,s_t),&a_t\text{ 是工具调用},\\
\operatorname{Finish}(a_t),&a_t\text{ 是最终回答}.
\end{cases}
\]

循环在模型给出最终回答、达到迭代上限或触发中止条件时停止。框架可以加入 middleware，用于日志、重试、模型路由、PII 检测、人类审批与输出格式化。

## 6. Memory 与模型上下文

短期 memory 通常是同一任务内的消息和状态；长期 memory 是跨任务保存的用户或应用信息。保存信息和把信息放进本次 prompt 是两个动作：

```text
持久化存储
   ↓ 查询 / 筛选 / 摘要
本轮上下文
   ↓
模型调用
```

把全部历史无条件塞进上下文会增加延迟、费用和干扰。memory 策略需要删除、摘要或检索旧信息，并明确用户隐私与数据保留规则。

## 7. LangChain 何时显得过重

如果程序只做一次本地文本生成，直接调用 Transformers 或 llama-server 更清楚。LangChain 在以下场景更有价值：

- 需要切换多种模型 provider；
- 有检索、工具与多步 agent；
- 需要 durable state、streaming 或 human-in-the-loop；
- 希望统一 tracing、重试与 middleware。

框架抽象会增加依赖、升级成本和调试层级。应用设计应从最小直接调用开始，在出现明确编排需求时再加入相应组件。

