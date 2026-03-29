# 约束工具类型

根据规则的特性，选择最合适的工具类型：

| 类型 | 适用场景 | 安装位置 | 实时生效 | bypass 模式下 |
|------|---------|---------|---------|-------------|
| **hook 脚本** | 拦截/检查工具调用、文件操作 | `.claude/hooks/` + settings.json | 是 | **始终生效** |
| **CLAUDE.md 规则** | 上下文注入、行为指导 | 项目或用户级 CLAUDE.md | 是 | 软约束，AI 可能忽略 |
| **skill** | 复杂的多步骤约束流程 | `.claude/commands/` | 是 | 软约束 |
| **settings 规则** | 自动允许（减少弹窗） | `.claude/settings.json` | 是 | deny 无效 |

> **重要发现**：bypass permissions 模式下 `deny` 规则被跳过，不生效。如果需要硬拦截，必须用 hook 脚本。settings 的 `allow` 规则在非 bypass 模式下可减少弹窗，但在 bypass 模式下无意义（已全放行）。

## 选择决策树

```
规则需要硬拦截（必须阻止）？
├─ 是 → hook 脚本（唯一可靠的硬拦截方式）
│   ├─ 需要检查工具输入？ → PreToolUse hook
│   ├─ 需要检查工具输出？ → PostToolUse hook
│   ├─ 需要拦截用户输入？ → UserPromptSubmit hook
│   └─ 需要阻止完成？ → Stop hook
└─ 否 → 软约束即可
    ├─ 规则是上下文指导？ → CLAUDE.md 规则
    ├─ 规则是复杂流程？ → skill
    └─ 只是减少权限弹窗？ → settings allow（非 bypass 模式）
```
