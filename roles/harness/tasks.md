# Harness Tasks

### HARNESS-001: 阻止在生产环境目录下执行危险命令

**Context**: 团队使用 Claude Code 管理多个项目，其中生产环境的部署目录 `/var/www/prod` 不允许执行 `rm -rf`、`DROP TABLE`、`truncate` 等破坏性命令。最近一位开发者在 CC 会话中不小心让 AI 执行了 `rm -rf /var/www/prod/uploads`，导致生产数据丢失。需要一个约束工具，当 CC 尝试在包含 `/var/www/prod` 路径的命令中执行危险操作时，自动拦截并拒绝。

**Requirements**:
- 创建一个 PreToolUse hook 脚本，匹配 Bash 工具调用
- 检测命令中是否包含 `/var/www/prod` 路径 且 包含 `rm`、`DROP`、`TRUNCATE`、`DELETE`、`truncate` 等关键词
- 命中时阻止执行（退出码 2），返回明确的拒绝原因，包含触发的关键词和路径
- 未命中时正常通过（退出码 0，输出 `{}`）
- 脚本执行时间 < 200ms
- 安装到 `.claude/hooks/` 目录，配置到 `.claude/settings.json`
- 验证脚本可执行权限和 JSON 格式

**Output**: 安装完成的约束工具，包含 hook 脚本文件、settings.json 配置、验证结果汇报

---

### HARNESS-002: 诊断并修复性能低下的 hook 系统

**Context**: 项目已经安装了 8 个 hook 脚本来约束 AI 行为：
1. `pre-bash-check.sh` — 检查 bash 命令安全性
2. `pre-edit-check.sh` — 检查编辑目标文件
3. `pre-write-check.sh` — 检查写入文件路径
4. `post-bash-lint.sh` — bash 执行后检查
5. `post-edit-format.sh` — 编辑后格式检查
6. `post-write-format.sh` — 写入后格式检查
7. `stop-check.sh` — 完成前检查
8. `notification.sh` — 通知处理

用户反映 Claude Code 响应变慢，每次工具调用有 2-3 秒延迟。经排查，发现每个 PreToolUse/PostToolUse hook 都是独立脚本，且每个脚本都启动了独立的 jq 进程来解析 JSON 输入。

**Requirements**:
- 分析现有 hooks 的性能问题：独立脚本数、重复逻辑、进程启动开销
- 将同事件的 hook 合并：PreToolUse 合并为一个脚本，PostToolUse 合并为一个脚本
- 合并后的脚本内部用函数组织不同规则，保持可读性
- 保持所有原有约束逻辑不变
- 更新 settings.json 配置，将多个 matcher 组指向合并后的脚本
- 合并后验证每个约束规则仍然正常工作
- 输出性能对比：合并前后的脚本数量和预期延迟

**Output**: 优化后的 hook 系统结构、合并后的脚本文件、更新后的 settings.json、性能对比报告

---

### HARNESS-003: 为大型多语言项目构建完整的约束体系

**Context**: 一个中型团队（5 人）的 monorepo 项目，包含 Node.js 后端、React 前端、Python 数据处理脚本。团队有以下约束需求：

1. **安全约束**：禁止在代码中硬编码 API 密钥、密码、token
2. **架构约束**：前端代码不能直接 import 后端内部模块（只能通过 API）
3. **代码规范约束**：所有新文件必须有模块级注释（说明文件用途）
4. **数据库约束**：涉及数据库 migration 文件的修改必须经过确认
5. **性能约束**：单个文件超过 500 行时提醒考虑拆分

团队希望这些约束对 CC 立即生效，且不会显著影响响应速度。

**Requirements**:
- 为每个约束选择最合适的工具类型（hook/CLAUDE.md/settings/skill），并解释选择理由
- 所有 hook 规则合并到最少脚本文件中（PreToolUse 最多 1 个脚本，PostToolUse 最多 1 个脚本）
- hook 脚本使用 sh 编写（除非逻辑复杂到必须用 node）
- 软约束（提醒类）和硬约束（阻止类）使用不同的 hook 退出策略
- 生成约束清单文档，列出所有约束的类型、触发条件、行为、豁免条件
- 验证整个约束体系安装后，CC 响应延迟增加 < 500ms
- 考虑约束之间的交互：比如安全约束和架构约束可能同时命中一个文件修改操作

**Output**: 完整的约束体系架构说明、所有约束工具文件、更新后的 settings.json、约束清单文档、安装验证报告

---

### HARNESS-004: 为团队添加代码审查软约束与权限配置

**Context**: 一个 3 人前端团队使用 Claude Code 开发 React 应用。团队有两个约束需求：

1. **软约束**：当 AI 修改 `src/services/` 目录下的核心业务文件时，要求 AI 先说明修改的影响范围（影响哪些模块、有哪些副作用风险），再动手改。这是一种行为指导，不需要硬拦截。
2. **权限优化**：团队在 CC 会话中频繁被 `git diff`、`git status`、`git log` 的权限弹窗打断，希望自动允许这些只读 git 命令，减少交互中断。

两个约束都不需要 hook 脚本——一个适合 CLAUDE.md 规则注入，一个适合 settings.json 权限配置。

**Requirements**:
- 为软约束选择 CLAUDE.md 规则类型，生成格式清晰的结构化规则（含规则名、触发条件、约束行为、违反后果）
- 为权限优化选择 settings 规则类型，在 `.claude/settings.json` 的 `permissions.allow` 中添加只读 git 命令
- 修改 settings.json 时必须增量更新（读取现有配置后追加），不能覆盖已有的权限条目
- 验证 CLAUDE.md 规则格式正确且语义清晰
- 验证 settings.json JSON 格式正确（用 jq 验证）
- 两个约束都应立即生效，不需要重启会话
- 输出安装结果汇报，包含每个约束的类型、文件、触发条件、行为

**Output**: CLAUDE.md 规则内容、更新后的 settings.json、安装验证结果、约束清单
