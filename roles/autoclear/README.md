# CC-AutoClear: Claude Code 会话自动清理方案

## 概述

通过外部脚本模拟用户输入，向运行中的 Claude Code 会话发送 `/clear` 命令，实现程序化上下文清理。

## 背景

Claude Code 的 `/clear` 是内置命令，无法通过 hooks、MCP、API 或任何程序化接口触发。本方案采用 **hack 方式**：通过终端模拟器接口向 CC 进程注入键盘输入。

## 架构

```
┌─────────────────────────────────────────────────┐
│  cc-clear 脚本                                   │
│  ~/.claude/skills/autoclear/cc-clear             │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐    ┌──────────────┐               │
│  │ 会话识别  │───>│  定向发送     │               │
│  │          │    │              │               │
│  │ sessions/│    │ Warp 模式     │               │
│  │ {pid}.json   │ AppleScript   │               │
│  └──────────┘    │ + keystroke  │               │
│                  ├──────────────┤               │
│  识别维度:       │ tmux 模式    │               │
│  - PID          │ send-keys    │               │
│  - TTY          └──────────────┘               │
│  - CWD                       │                  │
│  - SessionID                 ▼                  │
│  - StartedAt          ┌────────────┐            │
│                       │ Claude Code │            │
│                       │ /clear     │            │
│                       └────────────┘            │
└─────────────────────────────────────────────────┘
```

## 会话识别

CC 会话信息存储在 `~/.claude/sessions/{pid}.json`：

```json
{
  "pid": 22644,
  "sessionId": "d4d4e546-...",
  "cwd": "/Users/xxx/project",
  "startedAt": 1774884147313,
  "kind": "interactive",
  "entrypoint": "cli"
}
```

| 维度 | 用途 |
|------|------|
| PID | 直接标识进程 |
| TTY (`ttys000`) | 对应终端窗口/tab |
| CWD | 按项目目录筛选 |
| SessionID | 持久唯一标识 |
| startedAt | 区分同目录的多个会话 |

## 两种发送模式

### 模式 1: Warp + AppleScript (当前验证可用)

```bash
osascript -e '
tell application "Warp"
    activate
end tell
delay 0.5
tell application "System Events"
    keystroke "/"
    keystroke "clear"
    keystroke return
end tell'
```

**优点**: 无需额外工具，直接在 Warp 中使用
**缺点**:
- 需要辅助功能权限 (系统设置 > 隐私与安全性 > 辅助功能)
- 发送时 Warp 必须在前台
- tab 定位通过 `Cmd+数字` 切换实现，依赖 TTY 排序推算，可能与实际 tab 顺序有偏差

**定向原理**: 通过 `Cmd+N` 快捷键先切换到目标 tab，再发送 `/clear`：
```bash
osascript -e '
tell application "Warp"
    activate
end tell
delay 0.3
tell application "System Events"
    keystroke "2" using command down   # 切到第2个 tab
    delay 0.3
    keystroke "/"
    keystroke "clear"
    keystroke return
end tell'
```

**tab 推算逻辑**: 脚本从 `~/.claude/sessions/` 读取所有活跃会话的 TTY，按 TTY 名称排序后映射到 tab 序号。由于 Warp 的 tab 顺序可能与 TTY 分配顺序不一致，`-p` / `-c` 模式的自动推算可能有误差，建议用 `-t` 直接指定 tab 序号。

**前置条件**:
1. macOS 系统设置 > 隐私与安全性 > 辅助功能
2. 添加 `osascript` 或你的终端应用到允许列表

### 模式 2: tmux (推荐，多会话精确控制)

```bash
# 启动时在 tmux 中运行 CC
tmux new-session -s dev -d "claude"

# 定向发送 /clear
tmux send-keys -t dev:0.0 "/clear" Enter

# 向所有运行 claude 的 pane 批量发送
for pane in $(tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}'); do
    tmux send-keys -t "$pane" "/clear" Enter
done
```

**优点**:
- 精确定向到任意 pane，不受窗口焦点限制
- 不需要辅助功能权限
- 可批量操作
- 完全脚本化，可 cron 定时执行

**缺点**: 需要在 tmux 中运行 CC

**推荐用法**: 在 Warp 的 tab 中运行 `tmux`，然后在 tmux pane 中启动 CC。这样既能用 Warp 的 UI，又能用 tmux 的程序化控制。

## 脚本使用

脚本位置: `~/.claude/skills/autoclear/cc-clear`

建议添加到 PATH：
```bash
# 在 ~/.zshrc 中添加
export PATH="$HOME/.claude/skills/autoclear:$PATH"
# 或创建软链接
ln -s ~/.claude/skills/autoclear/cc-clear /usr/local/bin/cc-clear
```

### 命令列表

```bash
cc-clear -l             # 列出所有活跃 CC 会话
cc-clear -t <N>         # 向第 N 个 Warp tab 发送 /clear
cc-clear -a             # 向所有 Warp tab 逐一发送 /clear
cc-clear -p <PID>       # 向指定 PID 发送 (自动推算 tab 序号)
cc-clear -c <CWD>       # 向匹配工作目录的会话发送

# tmux 模式
cc-clear --tmux <t>     # 向指定 tmux pane 发送 (如 dev:0.1)
cc-clear --tmux-all     # 向所有运行 claude 的 pane 发送
```

### 使用示例

```bash
# 查看当前有哪些 CC 会话
$ cc-clear -l
=== 活跃 Claude Code 会话 ===
  [0]  PID=22644  TTY=ttys000  CWD=/project-a  Started=03-30 23:22:27
  [1]  PID=23115  TTY=ttys001  CWD=/project-b  Started=03-30 23:26:33

# 按工作目录清理特定会话
$ cc-clear -c project-a

# tmux 模式清理所有 CC pane
$ cc-clear --tmux-all
```

## 定时自动清理

结合 cron 或 launchd 实现定时清理：

```bash
# 每 30 分钟自动清理所有 tmux 中的 CC 会话
# 添加到 crontab
crontab -e
# */30 * * * * ~/.claude/skills/autoclear/cc-clear --tmux-all >> /tmp/cc-clear.log 2>&1
```

## 其他终端适配

| 终端 | 方法 | 能否定向 | 需要前台 |
|------|------|:---:|:---:|
| **Warp** | AppleScript + `Cmd+N` 切换 tab + keystroke | 是 (按 tab 序号) | 是 |
| **iTerm2** | AppleScript `write text` | 是 (精确到 session) | 否 |
| **Terminal.app** | AppleScript `do script` / keystroke | 部分 | 是 |
| **tmux** | `send-keys` | 是 (精确到 pane) | 否 |
| **screen** | `stuff` 命令 | 是 (精确到 window) | 否 |

如果切换到 iTerm2，定向发送示例：

```bash
osascript -e '
tell application "iTerm2"
    tell session 1 of tab 2 of current window
        write text "/clear"
    end tell
end tell'
```

## 限制与风险

1. **tab 定位偏差**: `-p` / `-c` 模式通过 TTY 排序推算 tab 序号，可能与 Warp 实际 tab 顺序不一致。用 `-t` 直接指定更可靠
2. **竞态条件**: 发送按键时有短暂 delay，如果用户同时在输入可能冲突
3. **CC 响应延迟**: CC 处理 `/clear` 有延迟，连续发送可能丢失
4. **权限依赖**: Warp 模式依赖辅助功能权限，tmux 模式无此限制

## 结论

| 场景 | 推荐方案 |
|------|---------|
| 清理指定 tab | `cc-clear -t <N>` (最可靠) |
| 按 PID/CWD 定向 | `cc-clear -p <PID>` 或 `-c <CWD>` (tab 推算可能有偏差) |
| 清理所有 tab | `cc-clear -a` |
| tmux 环境精确控制 | `cc-clear --tmux <target>` |
| 定时自动清理 | tmux + cron `--tmux-all` |
