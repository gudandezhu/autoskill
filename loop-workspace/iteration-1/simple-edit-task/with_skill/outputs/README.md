# AutoSkill - 技能训练系统

Autonomous skill training system inspired by [autoresearch](https://github.com/karpathy/autoresearch).

Train Claude Code skills through an iterative keep/discard evolution loop.

## Quick Start

1. Open Claude Code in this directory
2. Run: `/autoskill <role>` (e.g., `/autoskill architect`)
3. The agent will set up a training branch, establish baselines, and begin iterating

## How It Works

```
Modify SKILL.md → Execute task → Score against rubric → Keep or discard
```

- **SKILL.md** (editable): The skill prompt being trained
- **tasks.md** (fixed): Task suite that defines the evaluation
- **rubric.md** (fixed): Scoring criteria (0-100)
- **results.tsv**: Experiment log tracking all attempts

Improvements are kept via git commits. Failures are discarded with git reset.

## File Structure

```
autoskill/
├── roles/                      # Per-role: skill + evaluation (co-located)
│   ├── architect/
│   │   ├── SKILL.md            # Trainable skill
│   │   ├── tasks.md            # Fixed evaluation tasks
│   │   └── rubric.md           # Fixed scoring rubric
│   ├── backend/
│   ├── frontend/
│   ├── qa/
│   ├── explorer/
│   └── ...
├── evaluate/
│   ├── GUIDE.md                # How to write tasks and rubrics
│   └── scoring-protocol.md     # Shared scoring protocol
├── experience/
│   └── patterns.md             # Accumulated best practices
└── results.tsv                 # Experiment log (untracked)
```

Each role directory is self-contained: skill, tasks, and rubric live together.
Adding a role = adding a directory.

## Adding New Roles

1. Create `roles/<role>/SKILL.md` with initial skill definition
2. Run `/generate-baseline <role>` to auto-generate tasks and rubric
3. Or manually create `roles/<role>/tasks.md` and `roles/<role>/rubric.md`

## Deploy Trained Skills

Copy improved skills to your Claude Code skills directory:

```bash
cp roles/architect/SKILL.md ~/.claude/skills/architect/SKILL.md
cp roles/backend/SKILL.md ~/.claude/skills/backend/SKILL.md
```
