# Accumulated Patterns

This file stores generalizable patterns discovered during training.
Patterns are tagged with priority [P1] (critical) through [P5] (nice-to-have).
Maximum 200 lines. Prune lowest-priority stale patterns when exceeded.

## Format

Each pattern is a single line:
```
- [PX] Role: specific, actionable description
```

Priority guide:
- [P1] Must always follow. Violation causes clear score drops.
- [P2] Should almost always follow. Violation causes moderate score drops.
- [P3] Generally good practice. Violation causes minor score drops.
- [P4] Nice to have. Minor positive impact.
- [P5] Edge case or niche pattern. Situation-dependent.

## architect

- [P1] architect: For service design tasks, include CREATE TABLE statements with actual column types, constraints, and indexes for each service's database
- [P1] architect: Always include a dedicated Security section addressing inter-service auth, data encryption, and compliance scope
- [P1] architect: Each of error handling, security, scalability, monitoring must have a dedicated section — not just mentioned in passing
- [P1] architect: For refactoring/migration tasks, explicitly compare migration strategies (strangler fig vs big-bang vs parallel-run) and address migration-specific security (data integrity during transfer, auth during transition)
- [P2] architect: Require each technology choice to name the tool and explain why it beats the next-best alternative — forces concrete justification instead of vague reasoning
- [P2] architect: Include message/data flow diagrams showing happy path AND failure path — the failure path is what distinguishes a great design from a good one
- [P2] architect: Quantify capacity requirements (QPS, storage, concurrent users) before making design decisions — anchoring in numbers forces concrete reasoning over vague statements
- [ANTI] architect: Adding "avoid repetition" or "use cross-references" guidance causes format/rendering issues in output — LLM struggles with self-referencing, keep each section self-contained

## backend

- [P1] backend: Validate ALL external/untrusted inputs including nested payload fields, not just top-level request body
- [P1] backend: Define TypeScript interfaces for all data structures — never use `any`
- [P2] backend: Always include graceful shutdown handling for long-running processes (SIGTERM/SIGINT)

## frontend

- [P1] frontend: Build component skeleton from semantic HTML elements (section, form, nav, article, header) not generic divs
- [P2] frontend: Use mobile-first responsive: mobile styles as default, min-width media queries for larger screens

## harness

- [P1] harness: Output format must include explicit "配置安全"（showing jq incremental update command with tmp file + mv）and "可逆"（specific steps to remove/disable each constraint）sections — evaluators consistently score these as missing; adding them boosted HARNESS-003 from 71.7 to 94
- [P1] harness: Hook template must include 5 defensive coding rules: (1) empty input defaults to pass-through, (2) printf '%s' instead of echo, (3) word-boundary grep matching, (4) no set -e, (5) config points (keywords, paths) as variables at script top — rule 5 boosted HARNESS-001 from 98 to 100 (可维护性 4→5)
- [P2] harness: Use function-based dispatch (fn_check_xxx + case) in hook scripts instead of flat if blocks — improves 可维护性 from 4/5 to 5/5, boosted HARNESS-003 from 94 to 96

## role-structure

- [P1] role-structure: SKILL.md 必须在 roles/$ROLE/ 根目录单独存在，所有引用文件放在 roles/$ROLE/references/ 子目录中。目录结构为：`roles/$ROLE/{SKILL.md, tasks.md, rubric.md, references/*.md}`。SKILL.md 的 frontmatter `references` 字段路径应为 `references/xxx.md`

## qa

(no patterns yet)

## run

- [P1] run: EVALUATE 阶段必须实际验证（编译运行/curl测试/pytest），不能只做代码审查 — 只做代码审查会导致评估严格度低分
- [P2] run: EVALUATE 加入负面检查（主动找运行时错误、边界输入、环境依赖问题），可提升评估严格度得分
- [P2] run: PLAN 阶段加入环境/依赖/技术风险预判，可减少执行中因环境问题导致的迭代浪费
- [P3] run: EXECUTE 阶段开始前先做环境自检（编译器/运行时是否存在），比执行中途发现问题更高效
- [P2] run: ASCII 流程图与文字描述重复，删图不影响执行质量，精简 SKILL.md 优先删冗余可视化
- [P2] run: 示例代码块（成功标准示例、评估结果示例）删掉不影响理解，指令本身足够清晰
- [P3] run: "与用户沟通"section 对执行质量无影响，可安全删除；安全阀和原则可压缩为一行一条
