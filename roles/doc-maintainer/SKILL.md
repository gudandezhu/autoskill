---
name: doc-maintainer
description: >
  项目文档自动维护工具。每当完成代码编写、功能开发、bug修复、重构、配置变更后，
  自动分析变更内容并增量更新项目文档体系。CLAUDE.md 仅作为文档索引（map），
  具体文档存放在 docs/ 目录下的固定结构中。包括架构文档、设计文档、产品规格、
  执行计划、安全文档、可靠性文档等完整体系。


  TRIGGER 强制触发场景（在以下任何情况完成后必须立即使用此 skill）：
  - 完成任何代码编写、修改、重构（即使没有明确要求更新文档）
  - 添加新功能、新模块、新 API 端点
  - 修复 bug
  - 数据库 schema 变更
  - 配置文件（docker、CI/CD、环境变量等）变更
  - 依赖项变更（新增/升级/移除）
  - 用户提到"更新文档"、"同步文档"、"维护文档"、"记录变更"
  - 用户要求记录架构变更、设计决策、产品规格

  此 skill 应在每次代码变更后主动触发，无需用户明确要求。如果你刚刚完成了代码编写，
  你应该立即调用此 skill 来维护文档，而不是等用户提醒。
---

# 项目文档维护

你的任务是在每次代码变更后，自动分析变更影响并增量更新项目文档，保持文档与代码同步。

## 核心原则

- **CLAUDE.md 是索引，不是文档** — 只存放指向 docs/ 的 map，不放具体内容
- **增量更新** — 只修改受影响的章节，不重写整个文件
- **文档写清楚比写漂亮重要** — 给人和 AI 看的，准确性第一
- **保持引用一致** — 文档间的互相引用必须指向实际存在的文件

## 脚本工具

本 skill 包含两个脚本，处理确定性操作：

| 脚本 | 用途 | 调用时机 |
|------|------|----------|
| `scripts/init_docs.py` | 创建目录结构 + 生成模板文件 + 生成索引 | 新项目无 docs/ 时 |
| `scripts/refresh_index.py` | 扫描 docs/ 并刷新 CLAUDE.md 索引 | 文档增删改后 |

用法：
```bash
python <skill-path>/scripts/init_docs.py <project-root>
python <skill-path>/scripts/refresh_index.py <project-root>
```

## 工作流

每次触发后严格按以下顺序执行。

### Step 1: 分析变更

```bash
git diff --stat HEAD~1     # 文件变更概览
git diff HEAD~1            # 详细 diff
git status                 # 未提交变更
```

无 git 历史时根据上下文推断。需要确定：
- **变更文件**：哪些被修改、新增、删除
- **变更性质**：新功能 / bug 修复 / 重构 / 配置变更
- **影响范围**：前端 / 后端 / 数据库 / 基础设施

### Step 2: 映射到受影响的文档

| 变更类型 | 应更新的文档 |
|----------|-------------|
| 新增/修改/删除模块或组件 | `docs/ARCHITECTURE.md`, `docs/DESIGN.md` |
| 新增/修改 API 端点 | `docs/ARCHITECTURE.md`, `docs/product-specs/` |
| 数据库 schema 变更 | `docs/generated/db-schema.md`, `docs/ARCHITECTURE.md` |
| 前端组件/页面/路由变更 | `docs/FRONTEND.md`, `docs/DESIGN.md` |
| 安全相关（认证/授权/加密） | `docs/SECURITY.md` |
| 新的设计决策 | `docs/design-docs/` |
| 新功能完整开发 | `docs/product-specs/`, `docs/PRODUCT_SENSE.md`, `docs/ARCHITECTURE.md` |
| Bug 修复 | 对应模块的文档 + `docs/exec-plans/tech-debt-tracker.md` |
| 执行计划推进 | `docs/exec-plans/`（active → completed） |
| 可靠性/监控/基础设施 | `docs/RELIABILITY.md` |
| 代码质量/规范/CI 变更 | `docs/QUALITY_SCORE.md` |
| Agent 配置变更 | `docs/AGENTS.md` |
| 依赖或外部工具变更 | `docs/references/` |
| 项目规划/路线图变更 | `docs/PLANS.md` |

### Step 3: 增量更新文档

对每个需要更新的文档：
1. **先读取**当前内容
2. **定位**受影响的章节
3. **只 Edit** 必要部分，保持未受影响内容不变
4. 文档不存在时先创建（参考 Step 5 初始化流程）

### Step 4: 刷新索引

文档增删后执行索引刷新：
```bash
python <skill-path>/scripts/refresh_index.py <project-root>
```

### Step 5: 新项目初始化

检测到项目无 `docs/` 目录时：
1. 运行初始化脚本创建骨架：`python <skill-path>/scripts/init_docs.py <project-root>`
2. 脚本会自动检测项目类型（Go/Python/Node/Rust/Java）、生成目录和模板
3. 脚本生成的模板是骨架，**你需要读取项目源码后填充具体内容**（架构、API 端点、数据模型等）
4. 填充内容后运行 `refresh_index.py` 确保索引完整

### Step 6: 检查引用一致性

确保文档间的交叉引用指向实际存在的文件。如 ARCHITECTURE.md 提到"详见 docs/design-docs/auth-flow.md"，确认该文件存在。

## 注意事项

- `docs/generated/` 下的文档由 skill 自动维护，提醒用户不要手动编辑
- `docs/references/` 存放外部参考文档，通常不随代码变更更新
- `docs/exec-plans/active/` 中的计划完成后应移到 `docs/exec-plans/completed/`
- `docs/design-docs/` 中每个设计决策一个文件，通过 index.md 建立索引
