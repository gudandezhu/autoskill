# SKILL.md 核心流程对比分析

## 对比表格

| Skill | 核心流程步骤数 | 流程结构 | 流程类型 |
|-------|--------------|---------|---------|
| **architect** | 6 步 | 线性顺序（理解 -> 枚举方案 -> 选择 -> 细化 -> 横切关注点 -> 迁移） | 设计导向 |
| **backend** | 8 步 | 线性顺序（解析 -> 设计签名 -> 验证 -> 错误处理 -> 函数聚焦 -> 类型 -> DB -> 优化） | 实现导向 |
| **frontend** | 5 步 | 线性顺序（状态识别 -> 组件API -> HTML实现 -> 可访问性 -> 测试） | 实现导向 |
| **qa** | 7 步 | 线性顺序（识别对象 -> 命名 -> 结构 -> 覆盖范围 -> 独立性 -> 集成测试 -> Bug报告） | 验证导向 |
| **explorer** | 3 阶段（Phase 内含子步骤） | 迭代循环（Clarify -> Explore[迭代] -> Synthesize） | 探索导向 |
| **agile** | 4 阶段（共 28 步） | 顺序阶段（Architect[6] -> Backend[8] -> Frontend[7] -> QA[7]） | 全流程导向 |
| **devops** | 6 步 | 线性顺序（理解目标 -> 可复现 -> 健康检查 -> 最小权限 -> 回滚 -> 可观测） | 基础设施导向 |
| **loop** | 3 阶段（共 10 步） | 迭代循环（Plan[4] -> Execute[4] -> Evaluate[2] -> 可能回到Plan） | 元流程导向 |

## 步骤数详细拆解

### architect (6 步)
1. 理解需求，量化容量要求
2. 枚举 2-3 种方案并分析权衡
3. 选择推荐方案并给出理由
4. 指定具体数据类型、模式和协议
5. 处理横切关注点（错误、安全、可扩展、监控）
6. 针对重构/迁移比较策略

### backend (8 步)
1. 解析需求，识别输入/输出/约束/边界
2. 优先设计函数/服务签名
3. 在业务逻辑之前实现输入验证
4. 显式处理所有错误情况
5. 保持函数聚焦（单一职责）
6. 使用具体 TypeScript 类型，禁止 any
7. 数据库任务包含 CREATE TABLE
8. 查询优化包含 EXPLAIN ANALYZE 对比

### frontend (5 步)
1. 识别所有状态（默认/加载/错误/空/成功）
2. 设计组件 API（props/events/slots）
3. 语义 HTML 优先，再添加交互和样式
4. 确保键盘可访问性
5. 测试不同内容长度

### qa (7 步)
1. 识别测试对象（需求/边界/错误路径/集成点）
2. 按预期行为命名测试用例
3. 构建测试结构：Arrange -> Act -> Assert
4. 覆盖：正常路径/边界值/无效输入/并发
5. 确保测试独立且确定性
6. 集成测试包含具体请求/响应示例
7. Bug报告包含复现步骤/环境/严重度

### explorer (3 阶段)
- **Phase 1 Clarify**: 3-5 个聚焦问题（一次问 1-2 个）
- **Phase 2 Explore**: 2-4 轮迭代探索（每轮：结构化分析 + 非显而易见的角度 + 用户反馈）
- **Phase 3 Synthesize**: 总结 -> 校正 -> 生成文档

### agile (4 阶段，28 步)
- **Phase 1 Architect** (6 步): 设计阶段
- **Phase 2 Backend** (8 步): API 实现阶段
- **Phase 3 Frontend** (7 步): UI 构建阶段
- **Phase 4 QA** (7 步): 测试验证阶段

### devops (6 步)
1. 理解部署目标和约束
2. 确保可复现构建
3. 添加健康检查和就绪探针
4. 最小权限原则
5. 实现回滚能力
6. 使基础设施可观测

### loop (3 阶段，10 步)
- **PLAN** (4 步): 理解任务、定义成功标准、拆解子任务、记录迭代信息
- **EXECUTE** (4 步): 逐步执行、更新进度、记录新信息、处理阻塞
- **EVALUATE** (2 步): 逐项检查、循环决策

## 共同模式

### 1. "先理解再动手"（Understand First）
所有 skill 都将"理解需求/上下文"作为第一步。无论是 architect 的"理解需求"，backend 的"解析需求"，还是 devops 的"理解部署目标"，核心都是先搞清楚要做什么。

### 2. "设计先行"（Design Before Implement）
大多数 skill 在实际执行前都有一个设计/规划步骤：
- architect: 枚举方案、选择方案
- backend: 设计函数签名
- frontend: 设计组件 API
- loop: 定义成功标准、拆解子任务

### 3. "结构化输出"（Structured Output）
每个 skill 都定义了明确的输出格式。architect 要求特定章节的 markdown，backend 要求 JSON 响应格式，frontend 要求处理所有状态，qa 要求特定命名规范。

### 4. "防御性实践"（Defensive Practice）
多个 skill 强调防御性编码：
- backend: "Never trust the caller"、输入验证
- frontend: 处理所有状态（加载/错误/空）
- devops: 最小权限、回滚能力
- qa: 覆盖边界值和错误路径

### 5. "具体优于抽象"（Concrete Over Abstract）
几乎所有 skill 都反对模糊的抽象：
- architect: "No vague abstractions"，要具体的数据类型
- backend: "Never use any"，定义所有接口
- qa: "Assertions are specific"
- devops: "No hardcoded values"，但要求参数化

### 6. "质量内建"（Quality Built In）
质量不是事后检查，而是流程的一部分：
- qa: 测试命名规范、覆盖策略
- frontend: 可访问性是必须的
- devops: 可观测性是基础设施的一部分
- loop: 在计划阶段就锁定评估标准

### 7. "关注边界情况"（Edge Case Awareness）
所有 skill 都关注边界情况的处理方式：
- architect: 考虑失败模式
- backend: 处理瞬时故障和非恢复性故障
- frontend: 测试不同内容长度
- qa: 边界值、无效输入、并发场景

## 结构分类

根据流程结构，8 个 skill 可分为三类：

| 类型 | 特征 | Skill |
|------|------|-------|
| **线性流程** | 步骤按固定顺序执行，一步接一步 | architect, backend, frontend, qa, devops |
| **迭代流程** | 包含循环/迭代的阶段结构 | explorer, loop |
| **组合流程** | 组合多个 skill 的线性流程 | agile |

## 总结

8 个 skill 的核心流程步骤数从 5 到 28 不等，但它们共享一个核心理念：**先想清楚（理解/设计），再动手做（实现/执行），并确保质量（验证/防御）**。这是贯穿所有 skill 的元模式，与 loop skill 自身的 Plan-Execute-Evaluate 循环高度一致。
