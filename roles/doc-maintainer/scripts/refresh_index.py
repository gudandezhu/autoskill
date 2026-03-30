#!/usr/bin/env python3
"""doc-maintainer: 刷新 CLAUDE.md 文档索引

Usage:
    python refresh_index.py <project-root>

功能：
    扫描 docs/ 目录，根据实际存在的文件重新生成 CLAUDE.md 中的文档索引。
    不修改 docs/ 下的任何文件，只更新 CLAUDE.md 的索引章节。
"""

import sys
from pathlib import Path


# 索引配置：文档分类与描述
INDEX_SECTIONS = [
    {
        "title": "核心文档",
        "entries": [
            ("架构文档", "docs/ARCHITECTURE.md", "系统架构、模块关系、数据流"),
            ("设计文档", "docs/DESIGN.md", "设计原则、模式、决策记录"),
            ("前端文档", "docs/FRONTEND.md", "前端架构、组件体系、状态管理"),
            ("Agent 配置", "docs/AGENTS.md", "Agent 角色和工作流配置"),
        ],
    },
    {
        "title": "产品与质量",
        "dir_entries": [
            ("产品规格", "docs/product-specs/", "功能规格、用户故事", "docs/product-specs"),
        ],
        "entries": [
            ("产品感知", "docs/PRODUCT_SENSE.md", "UX 原则和用户洞察"),
            ("质量评分", "docs/QUALITY_SCORE.md", "代码质量指标和标准"),
            ("可靠性", "docs/RELIABILITY.md", "可靠性策略、监控、告警"),
            ("安全", "docs/SECURITY.md", "安全策略、威胁模型"),
        ],
    },
    {
        "title": "设计与计划",
        "dir_entries": [
            ("设计文档集", "docs/design-docs/", "详细设计决策记录", "docs/design-docs"),
            ("执行计划", "docs/exec-plans/", "活跃和已完成的执行计划", "docs/exec-plans"),
        ],
        "entries": [
            ("计划文档", "docs/PLANS.md", "项目规划和路线图"),
        ],
    },
    {
        "title": "自动生成与参考",
        "dir_entries": [
            ("数据库 Schema", "docs/generated/db-schema.md", "数据库表结构（自动维护）", "docs/generated"),
            ("参考资料", "docs/references/", "第三方文档、SDK 参考", "docs/references"),
        ],
    },
]


def scan_docs(root: Path) -> list[dict]:
    """扫描 docs/ 并返回每个分类中实际存在的条目"""
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return []

    result = []
    for section in INDEX_SECTIONS:
        valid_entries = []

        # 检查目录类型条目
        for name, path, desc, check_dir in section.get("dir_entries", []):
            dir_path = root / check_dir
            if dir_path.exists() and any(
                f for f in dir_path.iterdir()
                if f.name != ".gitkeep"
            ):
                valid_entries.append((name, path, desc))

        # 检查文件类型条目
        for name, path, desc in section.get("entries", []):
            if (root / path).exists():
                valid_entries.append((name, path, desc))

        if valid_entries:
            result.append({"title": section["title"], "entries": valid_entries})

    # 检查 docs/ 下有没有不在标准列表中的 .md 文件
    standard_paths = set()
    for section in INDEX_SECTIONS:
        for _, path, _, *_ in section.get("dir_entries", []):
            standard_paths.add(path)
        for _, path, _ in section.get("entries", []):
            standard_paths.add(path)

    extra = []
    for f in sorted(docs_dir.glob("*.md")):
        rel = f"docs/{f.name}"
        if rel not in standard_paths:
            extra.append((f.name, rel, ""))
    for f in sorted((docs_dir / "design-docs").glob("*.md")):
        if f.name != "index.md":
            rel = f"docs/design-docs/{f.name}"
            if rel not in standard_paths:
                extra.append((f.name, rel, "设计决策"))

    if extra:
        result.append({"title": "其他文档", "entries": extra})

    return result


def generate_index(sections: list[dict]) -> str:
    """生成索引 markdown"""
    lines = ["## 项目文档索引\n"]
    lines.append("> 以下为项目文档地图，具体内容请查看对应文件。")

    for section in sections:
        lines.append(f"\n### {section['title']}\n")
        lines.append("| 文档 | 路径 | 说明 |")
        lines.append("|------|------|------|")
        for name, path, desc in section["entries"]:
            lines.append(f"| {name} | {path} | {desc} |")

    return "\n".join(lines) + "\n"


def update_claude_md(root: Path, index_content: str):
    """更新 CLAUDE.md 中的索引"""
    claude_md = root / "CLAUDE.md"
    marker = "## 项目文档索引"

    if claude_md.exists():
        content = claude_md.read_text()
        if marker in content:
            # 替换已有索引（从 marker 开始到文件末尾）
            idx = content.index(marker)
            new_content = content[:idx] + index_content
            if new_content != content:
                claude_md.write_text(new_content)
                print("已更新 CLAUDE.md 文档索引")
            else:
                print("CLAUDE.md 索引无变化")
        else:
            # 追加索引
            claude_md.write_text(content.rstrip() + "\n\n" + index_content)
            print("已追加文档索引到 CLAUDE.md")
    else:
        claude_md.write_text(f"# {root.name}\n\n{index_content}")
        print("已创建 CLAUDE.md 并生成索引")


def main():
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <project-root>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"错误: {root} 不是目录")
        sys.exit(1)

    # 扫描并生成
    sections = scan_docs(root)
    if not sections:
        print("未找到 docs/ 目录或无文档文件")
        sys.exit(1)

    index_content = generate_index(sections)
    update_claude_md(root, index_content)


if __name__ == "__main__":
    main()
