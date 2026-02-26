# Agent Factory 操作手册 (V1.0)

## 1. 简介
本手册指导用户如何使用 **Agent Factory 团队**，根据特定业务需求孵化出定制化的 AI 智能体团队。
如果说 `Object Agent` 是为了**生产软件**，那么 `Agent Factory` 就是为了**生产“生产软件的工具”**。

## 2. 核心模式：工厂流水线
这是一个**元编程 (Meta-Programming)** 过程。
**Factory-Lead-Agent** (原 Mother-Lead) 是你的**工厂厂长**，他负责协调整个生产线：
1.  **定义 (Define)**: 搞清楚你要什么样的 Agent。
2.  **设计 (Design)**: 规划 Agent 的职责和交互。
3.  **制造 (Build)**: 编写 Prompt 文件。
4.  **质检 (Verify)**: 评估生成的 Agent 是否合格。

## 3. 团队成员名录
| 角色 | 智能体名称 | 职责 | 产出物 |
| :--- | :--- | :--- | :--- |
| **厂长/顾问** | **Factory-Lead-Agent** | **总指挥，与用户直接对话，理解需求** | 生产计划 |
| 架构师 | Agent-Architect-Agent | 设计 Agent 团队拓扑结构 | `docs/agent_system_design.md` |
| 工程师 | Prompt-Engineer-Agent | 编写 Markdown 提示词文件 | `*-Agent.md` |
| 质检员 | Evaluator-Agent | 模拟运行，审查逻辑漏洞 | `docs/agent_evaluation_report.md` |

## 4. 标准作业程序 (SOP)

### 阶段 0: 启动需求
1.  在 Trae 侧边栏打开 Chat。
2.  输入：`@Mother-Lead-Agent 我想创建一个[你的需求]...`。
    *   *示例*: "我想创建一个专门写科幻小说的团队，要有一个负责构思大纲的，一个负责写正文的。"
3.  Factory-Lead (Mother-Lead) 会进行初步分析，并建议下一步。

### 阶段 1: 架构设计 (Design Phase)
1.  **Architect**: 根据 Factory-Lead 的指令，呼叫 `@Agent-Architect-Agent`。
2.  **输入**: 用户的自然语言需求。
3.  **产出**: `docs/agent_system_design.md`。包含角色定义、工具需求和交互流程图。
4.  **用户确认**: 检查设计文档是否符合你的预期。

### 阶段 2: 提示词工程 (Engineering Phase)
1.  **Engineer**: 呼叫 `@Prompt-Engineer-Agent`。
2.  **任务**: "请根据设计文档生成所有的 Agent 文件。"
3.  **产出**: 一系列 `.md` 文件（如 `SciFi-Plotter-Agent.md`, `SciFi-Writer-Agent.md`）。

### 阶段 3: 质量验收 (Evaluation Phase)
1.  **Evaluator**: 呼叫 `@Evaluator-Agent`。
2.  **任务**: "请对新生成的 Agent 进行模拟测试和评估。"
3.  **产出**: `docs/agent_evaluation_report.md`。
4.  **决策**:
    *   **评分 > 90**: 验收通过，可以将文件复制到你的工作目录中使用。
    *   **评分 < 90**: 根据建议，让 Prompt-Engineer 修改文件，或让 Architect 调整设计。

## 5. 最佳实践
- **Prompt 即代码**: 把生成的 `.md` 文件当成代码来看待。它们也需要版本控制，也需要 Code Review。
- **少即是多**: 初次设计时，Agent 的数量越少越好。能用一个 Agent 解决的，不要拆成两个。
- **明确边界**: 在设计阶段，务必明确每个 Agent 的**输入**是什么，**输出**是什么。这能避免 Agent 之间互相甩锅。
- **测试驱动**: 让 Evaluator 模拟一些边缘情况（例如：“如果用户输入了乱码怎么办？”），看看 Agent 是否够稳健。
