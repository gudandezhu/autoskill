# Skill 核心流程对比分析

## 概览

在 `roles/` 目录下共有 **8 个 skill**，每个 skill 的 SKILL.md 都定义了一个面向特定角色的结构化工作流程。以下对每个 skill 的核心流程（Process / Workflow / Core Process）进行步骤统计和模式分析。

---

## 步骤数量统计

| Skill | 流程名称 | 核心步骤数 | 阶段划分 |
|-------|----------|-----------|---------|
| **architect** | Process | 6 | 无显式阶段，6 个连续步骤 |
| **backend** | Process | 8 | 无显式阶段，8 个连续步骤 |
| **frontend** | Process | 5 | 无显式阶段，5 个连续步骤 |
| **qa** | Process | 7 | 无显式阶段，7 个连续步骤 |
| **explorer** | Core Process | 3 (含子步骤) | 3 个显式阶段：Clarify (3-5 questions) -> Explore (2-4 rounds) -> Synthesize (3 steps) |
| **agile** | Workflow | 4 phases (23 sub-steps) | 4 个显式阶段：Design (6) -> Implement API (8) -> Build UI (7) -> Test (7)，共约 28 子步骤 |
| **devops** | Process | 6 | 无显式阶段，6 个连续步骤 |
| **loop** | 循环流程 | 3 | 3 个显式阶段：PLAN (4 sub-steps) -> EXECUTE (4 sub-steps) -> EVALUATE (2 sub-steps) |

---

## 详细步骤分解

### architect (6 步)

1. 理解需求，量化容量指标
2. 列举 2-3 种方案及权衡
3. 选择推荐方案并给出理由
4. 指定具体的数据类型、模式和协议
5. 处理横切关注点（错误处理、安全、可扩展性、监控）
6. 重构/迁移：比较至少 2 种迁移策略

### backend (8 步)

1. 解析需求，识别输入/输出/约束/边界
2. 先设计函数/服务签名
3. 在业务逻辑前实现输入验证
4. 显式处理所有错误情况
5. 保持函数单一职责，使用早返回
6. 使用具体 TypeScript 类型，禁止 `any`
7. 数据库任务：包含 CREATE TABLE
8. 查询优化：包含 EXPLAIN ANALYZE 前后对比

### frontend (5 步)

1. 识别所有状态：default, loading, error, empty, success
2. 设计组件 API（props, events, slots）
3. 用语义化 HTML 实现骨架，再加交互和样式
4. 确保所有交互元素的键盘可访问性
5. 测试不同内容长度

### qa (7 步)

1. 确定测试范围：需求、边界、错误路径、集成点
2. 按预期行为命名每个测试用例
3. 结构化测试：Arrange -> Act -> Assert
4. 覆盖：happy path、边界值、无效输入、并发场景
5. 确保测试独立且确定性
6. 集成测试：包含具体的请求/响应示例
7. Bug 报告：包含复现步骤、环境详情、严重级别

### explorer (3 阶段)

| 阶段 | 名称 | 内容 |
|------|------|------|
| Phase 1 | Clarify | 3-5 个聚焦问题，每次只问 1-2 个 |
| Phase 2 | Explore | 2-4 轮迭代探索，每轮：结构化分析 + 非显而易见的角度 + 用户反馈 |
| Phase 3 | Synthesize | 总结 -> 用户纠正 -> 生成最终文档 |

### agile (4 阶段，28 子步骤)

| 阶段 | 角色 | 子步骤数 |
|------|------|---------|
| Phase 1 | Architect - Design | 6 |
| Phase 2 | Backend - Implement API | 8 |
| Phase 3 | Frontend - Build UI | 7 |
| Phase 4 | QA - Test & Validate | 7 |

### devops (6 步)

1. 先理解部署目标和约束
2. 确保可复现构建
3. 添加健康检查和就绪探针
4. 最小权限原则
5. 实现每次部署的回滚能力
6. 使基础设施可观测

### loop (3 阶段)

| 阶段 | 名称 | 子步骤数 |
|------|------|---------|
| Phase 1 | PLAN | 4（理解任务、定义成功标准、拆解子任务、记录迭代信息） |
| Phase 2 | EXECUTE | 4（逐步执行、更新进度、记录新信息、处理阻塞） |
| Phase 3 | EVALUATE | 2（逐项检查、循环决策） |

---

## 共同模式分析

### 模式 1：先理解，后执行

**所有 skill 的第一步都是"理解需求/约束/上下文"。**

| Skill | 第一步内容 |
|-------|-----------|
| architect | "Understand requirements fully before designing" |
| backend | "Parse requirements carefully. Identify all inputs, outputs, constraints, and edge cases" |
| frontend | "Identify all states: default, loading, error, empty, success" |
| qa | "Identify what to test: requirements, edge cases, error paths" |
| explorer | Phase 1 Clarify: 聚焦问题锚定探索 |
| agile | Phase 1 Architect: "Parse requirements" |
| devops | "Understand the deployment target and constraints before writing any config" |
| loop | Phase 1 PLAN: "理解任务" |

### 模式 2：方案先行，实施在后

大部分 skill 在动手之前要求先设计/规划。

| Skill | 设计先行体现 |
|-------|------------|
| architect | 步骤 2-3：先列举方案、选方案，再进入细节设计 |
| backend | 步骤 2："Design the function/service signature first" |
| frontend | 步骤 2："Design the component API before implementing" |
| qa | 步骤 1-3：先确定范围和命名，再写测试体 |
| explorer | Phase 1 Clarify -> Phase 2 Explore |
| agile | Phase 1 Design -> Phase 2-4 实施 |
| devops | 步骤 1：先理解约束 |
| loop | Phase 1 PLAN -> Phase 2 EXECUTE |

### 模式 3：显式处理错误/边界/异常

每个 skill 都强调不能只处理 happy path。

| Skill | 错误/边界处理体现 |
|-------|-----------------|
| architect | 步骤 5："Address cross-cutting concerns: error handling, security..." |
| backend | 步骤 3-4：输入验证 + 显式错误处理，有完整的错误处理模式 |
| frontend | 步骤 1：必须处理 loading/error/empty/success 四种状态 |
| qa | 步骤 4："Cover: happy path, boundary values, invalid inputs, concurrent scenarios" |
| explorer | "Raise non-obvious angles the user might not have considered" |
| agile | 每个阶段都继承对应角色 skill 的错误处理要求 |
| devops | 步骤 5："Implement rollback capability"，原则 "Explicit failure modes" |
| loop | EVALUATE 阶段 + 安全阀（最大 5 次迭代） |

### 模式 4：具体胜于抽象

所有 skill 都反对模糊、通用的输出，要求具体和可操作。

| Skill | 体现 |
|-------|------|
| architect | "No vague abstractions"，"include CREATE TABLE statements with actual column types" |
| backend | "Return specific error messages: 'Email format invalid' not 'Bad request'" |
| frontend | "Use semantic elements"，"Do NOT build structure from generic divs" |
| qa | "Assertions are specific (exact value or pattern, not just 'no error')" |
| explorer | "Stay concrete: Avoid abstract advice. Ground every insight in specifics" |
| agile | 继承各角色 skill 的具体化要求 |
| devops | "parameterized, no hardcoded values" |
| loop | 成功标准必须"可验证：能明确判断通过或未通过" |

### 模式 5：结构化三段式组织

每个 SKILL.md 都遵循相同的文档结构：

```
## Process / Workflow / Core Process   <- 核心流程（步骤或阶段）
## Output Format / Code Standards      <- 输出格式或代码标准
## Principles                         <- 原则
```

这说明所有 skill 共享一个统一的模板框架。

### 模式 6：验证/评估闭环

近半数 skill 包含某种形式的验证或评估机制。

| Skill | 验证机制 |
|-------|---------|
| architect | 步骤 5 的监控部分 |
| backend | 步骤 8 的 EXPLAIN ANALYZE 前后对比 |
| frontend | 步骤 5 的不同内容长度测试 |
| qa | 整个 skill 就是验证流程 |
| explorer | Phase 3 Synthesize 的用户纠正环节 |
| agile | Phase 4 QA 测试 |
| devops | 步骤 3 健康检查 + 步骤 6 可观测性 |
| loop | Phase 3 EVALUATE + 循环决策 |

---

## 综合对比表格

| 维度 | architect | backend | frontend | qa | explorer | agile | devops | loop |
|------|-----------|---------|----------|----|----------|-------|--------|------|
| **核心步骤数** | 6 | 8 | 5 | 7 | 3 阶段 | 4 阶段(28 子步骤) | 6 | 3 阶段(10 子步骤) |
| **有显式阶段划分** | 否 | 否 | 否 | 否 | 是 | 是 | 否 | 是 |
| **第一步：理解需求** | 是 | 是 | 是 | 是 | 是 | 是 | 是 | 是 |
| **方案先行** | 是 | 是 | 是 | 是 | 是 | 是 | 是 | 是 |
| **显式错误处理** | 是 | 是 | 是 | 是 | 部分 | 是 | 是 | 是 |
| **要求具体输出** | 是 | 是 | 是 | 是 | 是 | 是 | 是 | 是 |
| **含验证闭环** | 部分 | 是 | 部分 | 是 | 是 | 是 | 是 | 是 |
| **迭代循环** | 否 | 否 | 否 | 否 | 是(Explore) | 否 | 否 | 是(核心机制) |
| **含 Principles** | 是 | 否(Code Standards) | 是 | 是 | 是 | 是 | 是 | 是 |
| **含 Output Format** | 是 | 是(Response Format) | 部分(Required States) | 部分(Test Naming) | 是 | 是 | 是 | 否 |
| **语言** | 英文 | 英文 | 英文 | 英文 | 英文 | 英文 | 英文 | 中文 |

---

## 总结

1. **步骤数量范围**：单角色 skill 的核心流程在 5-8 步之间；多阶段 skill (explorer, agile, loop) 有 3-4 个阶段，子步骤 10-28 个。

2. **最大共同模式**：所有 skill 都遵循 **"理解 -> 设计 -> 实施 -> 验证"** 的四阶段范式，即使步骤编号不显式标注阶段。

3. **文档结构一致**：所有 SKILL.md 都使用 Process + Output/Standards + Principles 的三段式组织。

4. **agile 是其余角色 skill 的编排组合**：它将 architect(6步) + backend(8步) + frontend(7步) + qa(7步) 串联成 4 个阶段，本质上是一个 meta-skill。

5. **loop 是唯一的元流程 skill**：它不处理具体领域，而是提供 "PLAN -> EXECUTE -> EVALUATE" 的通用执行引擎，可以包裹任何其他 skill。

6. **explorer 和 loop 是唯二包含迭代循环机制的 skill**：explorer 的 Explore 阶段是 2-4 轮迭代对话，loop 的整个流程就是迭代循环。其余 skill 的流程是线性的。
