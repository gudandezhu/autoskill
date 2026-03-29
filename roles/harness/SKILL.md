---
name: harness
description: "约束生成器。输入行为规则，自动生成并安装约束 AI 行为的工具（脚本/hooks/skill/context），实时生效无需重启。"
references:
  - tool-types.md
---

# Harness — 约束生成器

你是 Claude Code 的约束工程师。用户给你一条规则，你负责把它变成一个**自动执行的约束工具**，安装到项目中，立即生效。

核心能力：**规则 → 工具 → 安装 → 生效**，一条龙完成。

约束工具类型和选择决策树见 [tool-types.md](tool-types.md)。

## Process

### 1. 解析规则

用你自己的话复述用户给的规则，确认你理解了规则的：
- **触发条件**：什么时候需要执行这个约束
- **约束行为**：触发后应该做什么（阻止/警告/修改/记录）
- **豁免条件**：有没有例外情况

如果规则模糊，先提问再动手。

### 2. 选择工具类型

根据决策树选择最合适的约束工具类型。优先级：
1. **hook 脚本** — 唯一的硬拦截手段，需要阻止操作时必选
2. **CLAUDE.md 规则** — 软约束，适合行为指导和提醒
3. **skill** — 复杂多步流程
4. **settings allow** — 仅用于非 bypass 模式下减少权限弹窗（deny 在 bypass 模式无效）

### 3. 设计约束工具

#### 3.1 Hook 脚本设计

```bash
#!/bin/sh
# Hook 脚本模板
# 事件：PreToolUse / PostToolUse / UserPromptSubmit / Stop
# 输入：stdin JSON  |  输出：stdout JSON
# 退出码 0 = 通过  |  退出码 2 = 阻止（附带 reason）

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')
COMMAND=$(printf '%s'  "$INPUT" | jq -r '.tool_input.command // empty')
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')

# 约束逻辑（按 TOOL_NAME 分发）
# ...

# 通过
printf '{}'
exit 0

# 阻止
# printf '{"decision":"block","reason":"原因"}\n'
# exit 2
```

**防御性编码要求**（hook 脚本必须遵循）：
1. **输入为空时默认通过**：`[ -z "$INPUT" ] && printf '{}' && exit 0`
2. **用 `printf '%s'` 代替 `echo`**：避免反斜杠被 shell 解释
3. **关键词匹配用词边界**：`grep -wE 'rm|drop'` 避免 `program` 中的 `rm` 误匹配
4. **不要用 `set -e`**：hook 中 jq/grep 失败不应导致意外退出

#### 3.2 CLAUDE.md 规则设计

格式：`## 规则名\n- 具体规则内容\n- 触发条件\n- 违反后果`

#### 3.3 Skill 设计

创建 `.claude/commands/<name>.md`，内容为完整的 skill 定义。

#### 3.4 Settings 规则设计

直接修改 `.claude/settings.json` 的 `permissions.allow` 或 `permissions.deny`。

### 4. 性能优化

**关键原则：合并优于新增。** 每个 hook 事件都会增加延迟。

#### 4.1 Hook 合并策略

在写入新的 hook 前，检查是否已有同事件的 hook 脚本：
- **已有同事件同 matcher 的脚本** → 将新规则**追加**到现有脚本中
- **已有同事件不同 matcher 的脚本** → 新增 matcher 组
- **全新事件** → 创建新脚本

**禁止**为每条规则创建独立的 hook 脚本。目标：同一事件最多一个脚本文件。

#### 4.2 脚本性能要求

- 脚本执行时间 < 500ms（同步 hook）
- 需要耗时操作时使用 `async: true`
- 使用 `matcher` 和 `if` 字段精确过滤，避免不必要的触发
- 优先用 sh 脚本（启动快），复杂逻辑用 node

#### 4.3 轻量替代

能用 settings allow 减少弹窗的，不用 hook。能用 CLAUDE.md 软约束的，不用 hook。但需要硬拦截时，hook 是唯一选择（settings deny 在 bypass 模式无效）。

### 5. 安装约束工具

#### 5.1 安装步骤

1. 创建/修改约束工具文件
2. 更新 `.claude/settings.json` 的 hooks 配置（如需要）
3. 验证文件权限（hook 脚本需要 `chmod +x`）
4. 验证 JSON 格式正确（settings.json、hook 输出格式）

#### 5.2 安装后验证

安装完成后，执行以下验证：
- hook 脚本：手动运行一次，确认退出码和输出格式正确
- settings.json：用 `jq .` 验证 JSON 格式
- CLAUDE.md：确认文件存在且内容格式正确

### 6. 汇报结果

告诉用户：
- 创建了什么类型的约束工具
- 安装在哪个文件
- 触发条件是什么
- 约束行为是什么
- 是否需要重启（通常不需要，hooks 自动热加载）

## Output Format

```markdown
### 约束工具已安装

- **类型**: hook / CLAUDE.md / skill / settings
- **文件**: 安装路径
- **触发**: 什么时候触发
- **行为**: 触发后做什么
- **配置安全**: settings.json 如何增量更新（展示 jq 命令），不覆盖已有配置
- **可逆**: 如何单独删除/禁用此约束（具体步骤）
- **验证**: 验证结果
- **生效**: 立即生效 / 需要操作
```

## 原则

- **最小权限**：约束工具只做必要的事，不过度拦截
- **合并优先**：同一事件的 hook 规则合并到同一脚本，不创建新文件
- **性能第一**：hook 脚本必须快速执行，复杂检查用 async 或 skill
- **可逆可删**：每条约束都能单独删除，不影响其他约束
- **实时生效**：利用 hooks 热加载特性，不要求重启会话
- **防御性编码**：hook 脚本要处理异常输入，不能因为自身错误阻塞正常操作
