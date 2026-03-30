#!/usr/bin/env python3
"""doc-maintainer: 初始化项目文档结构

Usage:
    python init_docs.py <project-root>

功能：
    1. 检测项目类型（Go/Python/Node/Rust/Java）
    2. 创建 docs/ 目录结构
    3. 生成文档模板文件（不覆盖已有文件）
    4. 在 CLAUDE.md 中生成文档索引
"""

import sys
from pathlib import Path

# ============================================================
# 固定目录结构
# ============================================================

DIRS = [
    "docs/design-docs",
    "docs/exec-plans/active",
    "docs/exec-plans/completed",
    "docs/generated",
    "docs/product-specs",
    "docs/references",
]

# ============================================================
# 模板定义
# ============================================================

CORE_TEMPLATES = {
    "docs/ARCHITECTURE.md": """\
# 架构文档

## 系统概览
{project_name} — {project_desc}

## 技术栈
| 层次 | 技术 | 版本 |
|------|------|------|
{tech_stack_rows}

## 模块结构
```
{module_tree}
```

## 数据流
[核心数据如何在系统中流动]

## API 概览
| 方法 | 路径 | 功能 |
|------|------|------|
[待根据代码填写]

## 关键设计决策
详见 docs/design-docs/
""",
    "docs/DESIGN.md": """\
# 设计文档

## 设计原则
1. [原则 1]
2. [原则 2]

## 设计模式
- [项目中使用的设计模式]

## 代码组织规范
### 目录结构约定
[目录命名和文件组织方式]

### 命名规范
[变量、函数、文件的命名约定]

## 错误处理策略
[错误处理的统一方式]

## 测试策略
[测试层级和覆盖率要求]
""",
    "docs/PLANS.md": """\
# 项目计划

## 当前阶段
[当前所处的开发阶段]

## 路线图
| 阶段 | 目标 | 状态 |
|------|------|------|
| Phase 1 | [目标] | 规划中 |

## 里程碑
- [ ] **M1**: [里程碑描述]
""",
    "docs/SECURITY.md": """\
# 安全文档

## 安全策略
[整体安全方针]

## 认证与授权
当前状态：[待实现 / 已实现]

## 数据保护
- 输入校验：[当前策略]
- HTTPS：[状态]

## 威胁模型
| 威胁 | 当前状态 | 应对措施 |
|------|----------|----------|
| SQL 注入 | 未评估 | 参数化查询 |
| XSS | 未评估 | 输入输出转义 |
| 未授权访问 | 未评估 | 认证中间件 |

## 合规要求
暂无特定合规要求。
""",
    "docs/RELIABILITY.md": """\
# 可靠性文档

## 可靠性目标
- API 可用性：[目标]%
- API 响应时间 P99：< [目标]ms

## 监控体系
待建立。

## 故障响应
待建立。

## 容灾方案
待建立。
""",
    "docs/QUALITY_SCORE.md": """\
# 质量评分文档

## 质量标准
| 维度 | 权重 | 标准 |
|------|------|------|
| 测试覆盖率 | 30% | > 80% |
| 代码复杂度 | 20% | 圈复杂度 < 10 |
| 类型安全 | 20% | strict mode |
| 文档完整度 | 15% | 公共 API 有注释 |
| 安全合规 | 15% | 无高危漏洞 |

## 评估指标
| 维度 | 指标 | 当前值 | 目标值 |
|------|------|--------|--------|
| 测试覆盖率 | 行覆盖率 | 0% | > 80% |

## CI/CD 质量门禁
待建立。
""",
    "docs/design-docs/index.md": """\
# 设计文档索引

> 每个设计决策一个独立文件，本文件作为索引。

## 设计决策列表

| 决策 | 文件 | 状态 | 日期 |
|------|------|------|------|
""",
    "docs/exec-plans/tech-debt-tracker.md": """\
# 技术债务跟踪

## 活跃债务

| 债务 | 影响 | 优先级 | 计划处理时间 |
|------|------|--------|-------------|

## 已解决债务

| 债务 | 解决方式 | 解决日期 |
|------|----------|----------|
""",
    "docs/product-specs/index.md": """\
# 产品规格索引

> 每个功能/特性一个独立文件，本文件作为索引。

## 功能列表

| 功能 | 文件 | 状态 | 优先级 |
|------|------|------|--------|
""",
}

# 按项目类型可选创建的模板
OPTIONAL_TEMPLATES = {
    "frontend": {
        "docs/FRONTEND.md": """\
# 前端文档

## 技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
{frontend_tech_rows}

## 目录结构
```
[前端代码目录结构]
```

## 组件体系
待建立。

## 状态管理
待建立。

## 路由结构
待建立。

## 样式规范
待建立。
""",
    },
    "product": {
        "docs/PRODUCT_SENSE.md": """\
# 产品感知文档

## 目标用户
[用户画像和使用场景]

## UX 原则
1. [原则 1]
2. [原则 2]

## 用户反馈洞察
项目刚启动，尚无用户反馈。
""",
    },
    "database": {
        "docs/generated/db-schema.md": """\
# 数据库 Schema

> ⚠️ 此文档由 doc-maintainer skill 自动维护，请勿手动编辑。

## 表结构

[待根据 model 定义生成]

## 索引

[待生成]

## 关系图

[待生成]
""",
    },
    "agents": {
        "docs/AGENTS.md": """\
# Agent 配置文档

## Agent 角色
[AI Agent 角色定义]

## 工作流
[触发条件、执行流程]

## 工具配置
[可用工具及权限]
""",
    },
}

# ============================================================
# 项目类型检测
# ============================================================

def detect_project_info(root: Path) -> dict:
    """检测项目类型和基本信息"""
    info = {
        "name": root.name,
        "desc": "",
        "types": set(),
        "tech_stack": [],
        "has_frontend": False,
        "has_database": False,
        "module_tree": "",
    }

    # Go
    go_mod = root / "go.mod"
    if go_mod.exists():
        info["types"].add("go")
        content = go_mod.read_text()
        info["name"] = _extract_go_module(content) or info["name"]
        info["tech_stack"].append(("后端", "Go", _extract_go_version(content)))
        info["desc"] = "Go 后端项目"

    # Node.js / 前端
    pkg_json = root / "package.json"
    if pkg_json.exists():
        import json
        try:
            pkg = json.loads(pkg_json.read_text())
            info["types"].add("node")
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                info["tech_stack"].append(("前端框架", "Next.js", deps["next"]))
                info["has_frontend"] = True
            if "react" in deps:
                info["tech_stack"].append(("UI 库", "React", deps["react"]))
                info["has_frontend"] = True
            if "vue" in deps:
                info["tech_stack"].append(("前端框架", "Vue", deps["vue"]))
                info["has_frontend"] = True
            if "typescript" in deps:
                info["tech_stack"].append(("语言", "TypeScript", deps["typescript"]))
        except Exception:
            pass

    # Python
    pyproject = root / "pyproject.toml"
    requirements = root / "requirements.txt"
    if pyproject.exists() or requirements.exists():
        info["types"].add("python")
        version = _extract_python_version(root)
        info["tech_stack"].append(("后端", "Python", version))
        if pyproject.exists():
            info["name"] = _extract_pyproject_name(pyproject) or info["name"]

    # Rust
    cargo = root / "Cargo.toml"
    if cargo.exists():
        info["types"].add("rust")
        info["tech_stack"].append(("后端", "Rust", ""))
        info["name"] = _extract_cargo_name(cargo) or info["name"]

    # Java
    pom = root / "pom.xml"
    gradle = root / "build.gradle"
    if pom.exists() or gradle.exists():
        info["types"].add("java")
        info["tech_stack"].append(("后端", "Java", ""))

    # 数据库检测
    db_indicators = ["lib/pq", "gorm", "sqlalchemy", "prisma", "sequelize", "drizzle", "knex"]
    for indicator in db_indicators:
        # 检查 go.mod 和 package.json 中的依赖
        for f in [go_mod, pkg_json]:
            if f.exists() and indicator in f.read_text().lower():
                info["has_database"] = True
                break
        if info["has_database"]:
            break

    # Web 目录检测前端
    for web_dir in ["web", "frontend", "client", "app"]:
        if (root / web_dir).is_dir():
            info["has_frontend"] = True
            break

    # 生成简化模块树
    info["module_tree"] = _generate_module_tree(root)

    return info


def _extract_go_module(content: str) -> str:
    import re
    m = re.search(r'^module\s+(\S+)', content, re.MULTILINE)
    return m.group(1).split("/")[-1] if m else ""


def _extract_go_version(content: str) -> str:
    import re
    m = re.search(r'go\s+(\d+\.\d+)', content)
    return m.group(1) if m else ""


def _extract_python_version(root: Path) -> str:
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        import re
        content = pyproject.read_text()
        m = re.search(r'requires-python\s*=\s*"(.+?)"', content)
        if m:
            return m.group(1)
    return ""


def _extract_pyproject_name(path: Path) -> str:
    import re
    content = path.read_text()
    m = re.search(r'name\s*=\s*"(.+?)"', content)
    return m.group(1) if m else ""


def _extract_cargo_name(path: Path) -> str:
    import re
    content = path.read_text()
    m = re.search(r'name\s*=\s*"(.+?)"', content)
    return m.group(1) if m else ""


def _generate_module_tree(root: Path, max_depth: int = 2) -> str:
    """生成简化的项目目录树"""
    lines = []
    skip = {".git", "node_modules", "__pycache__", ".next", "dist", "build", "target", "vendor", ".claude"}

    def walk(path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        except PermissionError:
            return
        for entry in entries:
            if entry.name.startswith(".") or entry.name in skip:
                continue
            if entry.is_dir():
                lines.append(f"{prefix}{entry.name}/")
                walk(entry, prefix + "  ", depth + 1)
            else:
                lines.append(f"{prefix}{entry.name}")

    walk(root)
    return "\n".join(lines[:30])  # 最多 30 行


# ============================================================
# 文档生成
# ============================================================

def create_dirs(root: Path):
    """创建目录结构"""
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    # .gitkeep for empty dirs
    for d in ["docs/exec-plans/active", "docs/exec-plans/completed"]:
        gitkeep = root / d / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()


def write_template(root: Path, rel_path: str, content: str) -> bool:
    """写入模板文件，不覆盖已有文件。返回是否创建了新文件。"""
    target = root / rel_path
    if target.exists():
        print(f"  跳过 (已存在): {rel_path}")
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"  创建: {rel_path}")
    return True


def generate_templates(root: Path, info: dict) -> list[str]:
    """根据项目类型生成模板文件，返回创建的文件列表"""
    created = []

    # 格式化技术栈表格
    tech_rows = "\n".join(
        f"| {cat} | {tech} | {ver} |"
        for cat, tech, ver in info["tech_stack"]
    ) or "| - | - | - |"

    # 核心模板
    for rel_path, template in CORE_TEMPLATES.items():
        content = template.format(
            project_name=info["name"],
            project_desc=info["desc"] or "项目描述待填写",
            tech_stack_rows=tech_rows,
            module_tree=info["module_tree"],
        )
        if write_template(root, rel_path, content):
            created.append(rel_path)

    # 前端模板
    if info["has_frontend"]:
        for rel_path, template in OPTIONAL_TEMPLATES["frontend"].items():
            frontend_rows = "\n".join(
                f"| {cat} | {tech} | {ver} |"
                for cat, tech, ver in info["tech_stack"]
                if cat in ("前端框架", "UI 库", "语言")
            ) or "| - | - | - |"
            content = template.format(frontend_tech_rows=frontend_rows)
            if write_template(root, rel_path, content):
                created.append(rel_path)

    # 产品模板
    if info["has_frontend"] or "node" in info["types"]:
        for rel_path, template in OPTIONAL_TEMPLATES["product"].items():
            if write_template(root, rel_path, template):
                created.append(rel_path)

    # 数据库模板
    if info["has_database"]:
        for rel_path, template in OPTIONAL_TEMPLATES["database"].items():
            if write_template(root, rel_path, template):
                created.append(rel_path)

    return created


# ============================================================
# CLAUDE.md 索引生成
# ============================================================

def get_doc_description(filename: str) -> str:
    """已知文档的描述映射"""
    descriptions = {
        "ARCHITECTURE.md": "系统架构、模块关系、数据流",
        "DESIGN.md": "设计原则、模式、决策记录",
        "FRONTEND.md": "前端架构、组件体系、状态管理",
        "AGENTS.md": "Agent 角色和工作流配置",
        "PLANS.md": "项目规划和路线图",
        "PRODUCT_SENSE.md": "UX 原则和用户洞察",
        "QUALITY_SCORE.md": "代码质量指标和标准",
        "RELIABILITY.md": "可靠性策略、监控、告警",
        "SECURITY.md": "安全策略、威胁模型",
    }
    return descriptions.get(filename, "")


def generate_claude_md_index(root: Path) -> str:
    """扫描 docs/ 目录，生成 CLAUDE.md 文档索引内容"""
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return ""

    # 检测存在的文档
    existing = {
        "core": [],
        "product": [],
        "design": [],
        "generated": [],
    }

    # 核心文档
    core_docs = ["ARCHITECTURE.md", "DESIGN.md", "FRONTEND.md", "AGENTS.md"]
    for doc in core_docs:
        if (docs_dir / doc).exists():
            desc = get_doc_description(doc)
            existing["core"].append((doc, f"docs/{doc}", desc))

    # 产品与质量
    pq_docs = ["PRODUCT_SENSE.md", "QUALITY_SCORE.md", "RELIABILITY.md", "SECURITY.md"]
    for doc in pq_docs:
        if (docs_dir / doc).exists():
            desc = get_doc_description(doc)
            existing["product"].append((doc, f"docs/{doc}", desc))

    # 检查子目录
    if (docs_dir / "product-specs").exists() and any((docs_dir / "product-specs").iterdir()):
        existing["product"].insert(0, ("产品规格", "docs/product-specs/", "功能规格、用户故事"))
    if (docs_dir / "design-docs").exists() and any((docs_dir / "design-docs").iterdir()):
        existing["design"].append(("设计文档集", "docs/design-docs/", "详细设计决策记录"))
    if (docs_dir / "exec-plans").exists():
        existing["design"].append(("执行计划", "docs/exec-plans/", "活跃和已完成的执行计划"))
    if (docs_dir / "PLANS.md").exists():
        existing["design"].append(("计划文档", "docs/PLANS.md", "项目规划和路线图"))

    # 自动生成与参考
    if (docs_dir / "generated").exists() and any((docs_dir / "generated").iterdir()):
        existing["generated"].append(("数据库 Schema", "docs/generated/db-schema.md", "数据库表结构（自动维护）"))
    if (docs_dir / "references").exists() and any((docs_dir / "references").iterdir()):
        existing["generated"].append(("参考资料", "docs/references/", "第三方文档、SDK 参考"))

    # 生成 markdown
    sections = []

    sections.append("## 项目文档索引\n")
    sections.append("> 以下为项目文档地图，具体内容请查看对应文件。\n")

    def make_table(title, entries):
        if not entries:
            return ""
        lines = [f"\n### {title}\n"]
        lines.append("| 文档 | 路径 | 说明 |")
        lines.append("|------|------|------|")
        for name, path, desc in entries:
            lines.append(f"| {name} | {path} | {desc} |")
        return "\n".join(lines) + "\n"

    sections.append(make_table("核心文档", existing["core"]))
    sections.append(make_table("产品与质量", existing["product"]))
    sections.append(make_table("设计与计划", existing["design"]))
    sections.append(make_table("自动生成与参考", existing["generated"]))

    return "\n".join(s for s in sections if s)


def update_claude_md(root: Path, index_content: str):
    """在 CLAUDE.md 中添加或更新文档索引"""
    claude_md = root / "CLAUDE.md"
    marker_start = "## 项目文档索引"

    if claude_md.exists():
        content = claude_md.read_text()
        if marker_start in content:
            # 替换已有索引
            idx = content.index(marker_start)
            claude_md.write_text(content[:idx] + index_content)
            print(f"  更新: CLAUDE.md 文档索引")
        else:
            # 追加索引
            claude_md.write_text(content.rstrip() + "\n\n" + index_content)
            print(f"  追加: CLAUDE.md 文档索引")
    else:
        claude_md.write_text(f"# {root.name}\n\n{index_content}")
        print(f"  创建: CLAUDE.md")


# ============================================================
# 主流程
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <project-root>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"错误: {root} 不是目录")
        sys.exit(1)

    print(f"=== doc-maintainer: 初始化 {root.name} ===\n")

    # Step 1: 检测项目类型
    info = detect_project_info(root)
    print(f"项目类型: {', '.join(info['types']) or '未知'}")
    print(f"技术栈: {', '.join(t[1] for t in info['tech_stack']) or '未检测到'}")
    print(f"前端: {'是' if info['has_frontend'] else '否'}")
    print(f"数据库: {'是' if info['has_database'] else '否'}")
    print()

    # Step 2: 创建目录结构
    print("--- 创建目录结构 ---")
    create_dirs(root)
    print("  完成\n")

    # Step 3: 生成模板文件
    print("--- 生成模板文件 ---")
    created = generate_templates(root, info)
    if not created:
        print("  所有模板文件已存在，无需创建")
    print()

    # Step 4: 生成 CLAUDE.md 索引
    print("--- 生成文档索引 ---")
    index_content = generate_claude_md_index(root)
    if index_content:
        update_claude_md(root, index_content)
    print()

    print("=== 初始化完成 ===")
    print(f"提示: 模板文件内容为骨架，需要 AI 根据实际代码填充具体内容。")


if __name__ == "__main__":
    main()
