# 评分标准定义指南

本指南教你如何为 autoskill 定义任务（tasks）和评分标准（rubrics）。
autoskill 的训练质量完全取决于这两样东西——任务决定了"练什么"，评分标准决定了"怎么算好"。

---

## 目录

1. [核心概念](#核心概念)
2. [定义任务（tasks）](#定义任务)
3. [定义评分标准（rubrics）](#定义评分标准)
4. [设计原则](#设计原则)
5. [常见错误](#常见错误)
6. [完整示例：创建一个新角色](#完整示例)

---

## 核心概念

autoskill 的评估体系由两个固定文件组成：

| 文件 | 作用 | 类比 |
|------|------|------|
| `tasks.md` | 定义要解决的具体题目 | 考试卷 |
| `rubrics.md` | 定义评分标准 | 评分细则 |

**为什么这两个文件训练中不能改？** 因为它们是"地面真值"（ground truth）。如果你边训练边改评分标准，就无法判断分数提升是因为技能变好了还是标准变松了。

### 评分结构（100 分制）

```
总分 = 检查清单（0-50） + 质量维度（10-50）
     = 10 ~ 100 分
```

- **检查清单**：10 个二元判断（达标/不达标），每个 5 分，共 50 分
- **质量维度**：5 个维度，每个 1-5 分，求和后 ×2 换算，共 10-50 分

---

## 定义任务

### 任务格式

每个任务包含四个部分：

```markdown
### <role>-<编号>: <任务标题>

**Context**: 背景描述。给 AI 足够的业务上下文来理解问题。

**Requirements**:
- 具体要求1
- 具体要求2
- ...

**Output**: 期望的输出格式。
```

### 编写要求的原则

**1. 具体优于模糊**

```markdown
# 差 — 太模糊
设计一个用户系统

# 好 — 具体且有边界
实现 POST /api/users 注册接口：
- name: 2-100 字符，必填
- email: 合法邮箱格式，必填，唯一
- password: 8+ 字符，含大写、小写、数字
成功返回 201，验证失败返回 400（含具体字段错误）
```

**2. 包含真实世界的约束**

好的任务会给出数量级、性能要求、边界条件：

```markdown
# 好
- orders 表有 1500 万行，查询耗时 4.2 秒
- EXPLAIN 显示全表扫描
- 考虑 OFFSET 很大时的深分页问题
```

**3. 涵盖不同的考察维度**

每个角色至少需要 3 个任务，分别测试不同能力：

| 维度 | 示例 |
|------|------|
| 基础能力 | 实现 CRUD 接口、写单元测试 |
| 问题诊断 | 慢查询优化、bug 报告分析 |
| 系统设计 | 微服务拆分、实时系统架构 |

**4. 输出格式要明确**

```markdown
# 差
输出你的答案

# 好
输出一份 markdown 架构文档，包含组件图、数据模型、API 接口定义。
包含所有实体的 CREATE TABLE 语句。
```

### 任务难度阶梯

设计任务时建议分两个梯度：

- **v1 任务**（tasks.md）：考察核心能力，范围明确
- **v2 任务**（tasks-v2.md）：当 v1 全部 >90 分后使用，增加跨领域、模糊需求、安全合规等维度

---

## 定义评分标准

### 评分标准格式

```markdown
## <角色> 评分标准

### 检查清单（10 项，每项 5 分 = 50 分）

对每一项，达标给 5 分，不达标给 0 分。

- [ ] **项目名称**: 达标条件描述
...

### 质量维度（5 个维度，每个 1-5 分，求和 × 2 = 10-50 分）

1. **维度名称** (1=描述, 3=描述, 5=描述)
...
```

### 编写检查清单（Checklist）

检查清单是**二元判断**——只有"达标"和"不达标"，没有中间态。

**好的检查项特征：**

```markdown
# 好 — 可客观判断
- [ ] **输入验证**: 所有函数/服务输入在处理前都经过验证
- [ ] **无硬编码密钥**: 密码、API key 使用环境变量，不硬编码
- [ ] **正确 HTTP 状态码**: 使用 201/400/404/409/500 等正确状态码
```

**差的检查项特征：**

```markdown
# 差 — 主观模糊
- [ ] **代码质量好**: 代码写得不错  ← 什么是"不错"？
- [ ] **适当的错误处理**: 错误处理适当  ← "适当"无法判断
- [ ] **良好实践**: 遵循良好实践  ← 什么实践？
```

**编写检查项的方法论：**

1. **从反例出发**：想想你见过最差的代码，它缺什么？那些缺失的东西就是检查项。
2. **从代码审查出发**：你在 PR review 时最常要求改什么？那些就是检查项。
3. **从故障出发**：线上出过什么 bug？那个 bug 的根因就是检查项。

### 编写质量维度（Quality Dimensions）

质量维度用 **1-5 分**的描述性量表，每个级别都有具体定义：

```markdown
# 好 — 每个级别都有具体描述
1. **正确性** (1=不符合规范, 3=基本正确但有遗漏, 5=完全匹配规范要求)
2. **健壮性** (1=意外输入就崩, 3=处理大部分情况, 5=处处优雅降级)
3. **代码质量** (1=面条代码, 3=可读, 5=整洁、地道、组织良好)
4. **地道性** (1=跟框架对着干, 3=可接受, 5=完美遵循语言/框架惯例)
5. **效率** (1=不必要的复杂和冗余, 3=合理, 5=精简高效)
```

**选择维度的方法：**

问自己："这个角色最重要的质量属性是什么？"

| 角色 | 推荐维度方向 |
|------|-------------|
| 架构师 | 完整性、清晰度、实用性、权衡意识、简洁性 |
| 后端 | 正确性、健壮性、代码质量、地道性、效率 |
| 前端 | UX 完整性、无障碍、组件设计、状态管理、打磨度 |
| QA | 覆盖广度、边界深度、清晰度、可维护性、回归检测 |
| DevOps | 可重复性、安全性、可观测性、弹性、文档性 |
| 数据工程 | 数据质量、可扩展性、容错性、性能、可维护性 |

### 检查清单 vs 质量维度的分工

| 类型 | 特点 | 适用场景 |
|------|------|---------|
| 检查清单 | 二元判断，有无 | 特定实践是否落实（如"有无输入验证"） |
| 质量维度 | 渐进评分，好坏 | 整体质量的细微差别（如"验证做得有多好"） |

**经验法则**：如果一个问题可以用"有没有"来回答，放检查清单；如果需要用"好不好"来衡量，放质量维度。

---

## 设计原则

### 1. 检查项之间要独立

```markdown
# 差 — 有重叠
- [ ] **输入验证**: 验证所有输入
- [ ] **边界值处理**: 处理 null、空值、边界值  ← 这是输入验证的子集

# 好 — 独立
- [ ] **输入验证**: 所有输入在处理前验证类型和格式
- [ ] **边界值处理**: 处理 null、空字符串、零值、最大值等极端情况
```

### 2. 质量维度之间要正交

```markdown
# 差 — 有重叠
1. 代码质量
2. 代码风格      ← 跟"代码质量"大量重叠

# 好 — 正交
1. 正确性        ← 功能对不对
2. 健壮性        ← 抗不抗造
3. 代码质量      ← 好不好读
4. 地道性        ← 符不符合惯例
5. 效率          ← 有没有浪费
```

### 3. 不要泄露评分标准到 SKILL.md

SKILL.md 是被训练的对象，评分标准是裁判。如果你把"要有输入验证"直接写进 SKILL.md，那等于告诉考生答案。正确做法是让技能自己"学"到这些。

### 4. 任务要有多样性

如果三个任务都是"写 CRUD 接口"，训练出来的技能只能写 CRUD。要覆盖：
- 正常流程 vs 异常流程
- 单一组件 vs 系统集成
- 明确需求 vs 模糊需求
- 小规模 vs 大规模

### 5. 评分要严格一致

在评分标准里写明：

> Apply rubrics strictly and mechanically. Be harsh, not generous.

宽松的评分会导致技能停止进化（所有实验都轻松达标），严格的评分才能推动持续改进。

---

## 常见错误

### 1. 检查项太抽象

```markdown
# 错误
- [ ] **安全**: 代码安全

# 正确
- [ ] **无 SQL 注入**: 使用参数化查询，不拼接 SQL
- [ ] **无硬编码密钥**: 不在代码中出现密码和 API key
```

### 2. 质量维度缺少级别描述

```markdown
# 错误 — 只有名称
5. **效率**

# 正确 — 有描述性量表
5. **效率** (1=不必要的复杂和冗余, 3=合理, 5=精简高效)
```

### 3. 任务和评分标准不匹配

任务要求"写测试"，但评分标准里全是"代码组织"相关的检查项——分数无法反映任务完成质量。

**修正方法**：写完评分标准后，拿一个"完美答案"过一遍，确认它能拿满分。再拿一个"很差答案"过一遍，确认它拿不到高分。

### 4. 检查项太多或太少

- 10 个检查项 × 5 分 = 50 分，这是固定的
- 如果你的领域确实只需要关注 8 个方面，可以用 8 个 × 5 分 = 40 分，然后调整质量维度权重来补足
- 但保持总分 = 100 的结构不变

### 5. 质量维度分数全部差不多

如果每次评分 5 个维度都是 3/3/3/3/3，说明维度定义不够区分。解决方法：
- 让 1 分和 5 分的描述差异更极端
- 加上具体的判定示例

---

## 完整示例

假设我们要添加一个 **devops** 角色。

### 第一步：创建技能文件

```bash
mkdir -p roles/devops
```

`roles/devops/SKILL.md`:
```markdown
# DevOps Skill

You are a DevOps engineer. When asked to design infrastructure or write
deployment code, follow these principles:

1. Everything is code (Terraform, Docker, YAML)
2. Immutable infrastructure where possible
3. Explicit failure modes and recovery procedures
4. Least privilege for all access
5. Observable: every action produces logs and metrics
```

### 第二步：定义任务

在 `roles/devops/tasks.md` 创建：

```markdown
## DevOps Tasks

### devops-001: Docker Compose for Web Application

**Context**: A startup has a Node.js API, a PostgreSQL database, and a Redis cache.
They need a Docker Compose setup for local development.

**Requirements**:
- Multi-stage Dockerfile for the Node.js app (dev and production targets)
- docker-compose.yml with api, postgres, redis services
- Health checks for all services
- Volume mounts for development (hot reload)
- Environment variable management (.env file support)
- Network isolation (api can reach db/redis, but db/redis not exposed)
- Restart policies for production
- Database initialization with seed data

**Output**: Dockerfile and docker-compose.yml with comments explaining choices.

### devops-002: CI/CD Pipeline for Monorepo

**Context**: A monorepo has three apps: /frontend (React), /backend (Node.js), /shared (library).
They use GitHub Actions. Only changed apps should be built and deployed.

**Requirements**:
- Path-based build triggers (only build what changed)
- Separate staging and production environments
- Automated testing before deploy
- Rollback mechanism on failure
- Artifact versioning with git SHA
- Slack notification on deploy success/failure

**Output**: GitHub Actions workflow YAML with clear stage separation.

### devops-003: Infrastructure Monitoring Setup

**Context**: A team runs 5 microservices on Kubernetes. They need comprehensive
monitoring and alerting. Current problem: they find out about outages from
customers, not from their tools.

**Requirements**:
- Metrics collection strategy (what to collect, why)
- Log aggregation approach
- Alert rules with severity levels (warning, critical)
- Dashboard design for service health overview
- SLO definitions for key services
- Runbook template for on-call engineers

**Output**: Monitoring architecture document with concrete Prometheus/alertmanager
configs and a Grafana dashboard JSON example.
```

### 第三步：定义评分标准

在 `roles/devops/rubric.md` 创建：

```markdown
## DevOps Rubric

### Checklist (10 items, 5 points each = 50 points)

- [ ] **Reproducible builds**: Build outputs are deterministic, versioned,
      and can be recreated from the same commit
- [ ] **Health checks**: All services have health/readiness probes defined
- [ ] **Secret management**: No secrets in plaintext; uses env vars, vault,
      or secret references
- [ ] **Failure isolation**: One service failure does not cascade to others
      (circuit breakers, retries, timeouts)
- [ ] **Least privilege**: Containers/users have minimum required permissions
- [ ] **Infrastructure as code**: All infrastructure defined in code, not
      manual steps
- [ ] **Rollback capability**: There is a documented way to revert a failed
      deployment
- [ ] **Observability**: Logs, metrics, and traces are collected with
      meaningful labels
- [ ] **Resource limits**: CPU/memory limits defined for all containers
- [ ] **Environment parity**: Dev/staging/prod use the same base images and
      configuration approach

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Reliability** (1=fragile, single points of failure, 3=reasonable
   redundancy, 5=highly available with automated failover)
2. **Security** (1=exposed services, no auth, 3=basic auth and network
   isolation, 5=defense in depth with audit trail)
3. **Maintainability** (1=hardcoded values everywhere, 3=configurable
   via env vars, 5=fully modular with clear parameterization)
4. **Clarity** (1=needs extensive tribal knowledge, 3=documentation
   covers basics, 5=new team member can deploy confidently)
5. **Efficiency** (1=wasteful resource usage, 3=reasonable, 5=optimized
   build times and resource allocation)
```

### 第四步：验证

在开始训练之前，手动验证：

1. 拿一个"理想答案"过一遍评分标准 — 应该接近 100 分
2. 拿一个"最差答案"（比如只有半个 Dockerfile）过一遍 — 应该在 10-20 分
3. 检查检查项之间是否独立（没有重叠）
4. 检查质量维度之间是否正交（没有重叠）
5. 确认总分范围是 10-100

---

## 文件放置位置

```
roles/                       # 每个角色一个目录，内聚
├── <角色>/
│   ├── SKILL.md             # 可训练技能定义
│   ├── tasks.md             # 固定评估任务
│   └── rubric.md            # 固定评分标准
evaluate/
├── GUIDE.md                 # 本指南
└── scoring-protocol.md      # 通用评分协议
```

新增角色时：
1. 创建 `roles/<角色>/SKILL.md` 作为初始技能定义
2. 创建 `roles/<角色>/tasks.md` 定义评估任务
3. 创建 `roles/<角色>/rubric.md` 定义评分标准
4. 或直接运行 `/generate-baseline <角色>` 自动生成 tasks.md 和 rubric.md

---

## 总结

定义好的评分标准 = 写好考试 + 写好评分细则。

- **任务**要具体、有约束、覆盖多种场景
- **检查清单**要客观、二元、可独立判断
- **质量维度**要正交、有区分度、每级有描述
- **先验证再训练**：用理想答案和最差答案跑一遍评分流程
