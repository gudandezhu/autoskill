# 性能优化与安装

## 1. Hook 合并策略

**关键原则：合并优于新增。** 每个 hook 事件都会增加延迟。

在写入新的 hook 前，检查是否已有同事件的 hook 脚本：
- **已有同事件同 matcher 的脚本** → 将新规则**追加**到现有脚本中
- **已有同事件不同 matcher 的脚本** → 新增 matcher 组
- **全新事件** → 创建新脚本

**禁止**为每条规则创建独立的 hook 脚本。目标：同一事件最多一个脚本文件。

合并脚本必须在文件头注释中列出所有原脚本名，每条规则用注释分隔：
```sh
# 合并自: pre-bash-check.sh + pre-edit-check.sh + pre-write-check.sh
# --- 原始脚本: pre-bash-check.sh ---
# ...该脚本的规则...
# --- 原始脚本: pre-edit-check.sh ---
# ...该脚本的规则...
```

## 2. 脚本性能要求

- 脚本执行时间 < 500ms（同步 hook）
- 需要耗时操作时使用 `async: true`
- 使用 `matcher` 和 `if` 字段精确过滤，避免不必要的触发
- 优先用 sh 脚本（启动快），复杂逻辑用 node

## 3. 轻量替代

能用 settings allow 减少弹窗的，不用 hook。能用 CLAUDE.md 软约束的，不用 hook。但需要硬拦截时，hook 是唯一选择（settings deny 在 bypass 模式无效）。

## 4. 安装步骤

1. 创建/修改约束工具文件
2. 更新 `.claude/settings.json` 的 hooks 配置（如需要）
3. 验证文件权限（hook 脚本需要 `chmod +x`）
4. 验证 JSON 格式正确（settings.json、hook 输出格式）

## 5. 安装后验证

安装完成后，执行以下验证：
- hook 脚本：手动运行一次，确认退出码和输出格式正确
- settings.json：用 `jq .` 验证 JSON 格式
- CLAUDE.md：确认文件存在且内容格式正确
