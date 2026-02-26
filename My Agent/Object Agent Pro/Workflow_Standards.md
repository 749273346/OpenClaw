# Workflow Standards (工作流标准与模板)

本文件定义了 Meta-Agent 在执行任务时必须遵守的通用标准、日志管理规范以及文档模板。

---

## 1. 项目日志管理 (Log Management)

Meta-Agent 必须严格维护项目的状态可见性。

### 目录结构
```text
.project_log/
├── project_status.md  # 项目整体进度看板
└── Meta_Agent_log.md  # 详细工作流水日志
```

### 操作规范
1.  **Action Pre-check (行动前)**:
    - 读取 `project_status.md`，确认当前阶段（Phase）和待办事项（Todo）。
2.  **Action Post-update (行动后)**:
    - 在 `Meta_Agent_log.md` 中追加本次操作的详细记录（时间、角色、内容、结果）。
    - 更新 `project_status.md` 中的进度条、当前阶段和下一步计划。

---

## 2. 文档模板 (Document Templates)

Meta-Agent 在产出文档时，应参考以下标准结构。

### 2.1 产品需求文档 (PRD)
**文件路径**: `docs/prd.md`
**负责角色**: PM

```markdown
# [项目名称] PRD

## 1. 项目背景
- 目标：...
- 核心问题：...

## 2. 用户角色与场景
- 角色A：...
- 角色B：...

## 3. 功能清单
- [ ] 功能模块1
- [ ] 功能模块2

## 4. 非功能性需求
- 性能：...
- 安全：...

## 5. 业务流程图 (Mermaid)
...

## 6. 用户故事
- As a [Role], I want to [Action], so that [Benefit].
```

### 2.2 设计规范
**文件路径**: `docs/design_spec.md`
**负责角色**: Designer

```markdown
# 设计规范

## 1. 布局结构 (Layout)
- Header: ...
- Sidebar: ...

## 2. 关键组件 (Components)
- 按钮样式：...
- 卡片样式：...

## 3. 交互逻辑 (Interaction)
- 点击反馈：...
- 异常提示：...
```

### 2.3 系统架构文档
**文件路径**: `docs/architecture.md`
**负责角色**: Architect

```markdown
# 系统架构

## 1. 架构概览 (Mermaid Graph)
...

## 2. 技术栈选型
- 前端：... (理由：...)
- 后端：... (理由：...)
- 数据库：...

## 3. 核心数据模型 (ER Diagram)
...
```

### 2.4 API 接口文档
**文件路径**: `docs/api.md`
**负责角色**: Architect

```markdown
# API 规范

## GET /resource
- Request: ...
- Response: ...

## POST /resource
...
```

### 2.5 测试计划
**文件路径**: `docs/test_plan.md`
**负责角色**: QA

```markdown
# 测试计划

## 1. 测试范围
- 功能测试：...
- 边界测试：...

## 2. 测试用例
| ID | 描述 | 前置条件 | 步骤 | 预期结果 |
|----|------|----------|------|----------|
| 1  | ...  | ...      | ...  | ...      |

## 3. Bug 记录
- [ ] Bug 1: ...
```

---

## 3. 文件系统规范

- **保持整洁**: 在阶段转换时，主动清理不再需要的临时文件。
- **结构化**:
    - `src/`: 源代码
    - `docs/`: 所有文档
    - `tests/`: 测试代码
    - `.project_log/`: 日志
