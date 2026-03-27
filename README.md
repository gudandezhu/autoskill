# AutoSkill

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
- **rubrics.md** (fixed): Scoring criteria (0-100)
- **results.tsv**: Experiment log tracking all attempts

Improvements are kept via git commits. Failures are discarded with git reset.

## File Structure

```
autoskill/
├── autoskill.md           # Training instructions (the "program")
├── evaluate/
│   ├── tasks.md           # Fixed task suite (12 tasks, 3 per role)
│   └── rubrics.md         # Fixed scoring rubrics
├── skills/
│   ├── architect/SKILL.md # Trainable skill
│   ├── backend/SKILL.md
│   ├── frontend/SKILL.md
│   └── qa/SKILL.md
├── experience/
│   └── patterns.md        # Accumulated best practices
└── results.tsv            # Experiment log (untracked)
```

## Deploy Trained Skills

Copy improved skills to your Claude Code skills directory:

```bash
cp skills/architect/SKILL.md ~/.claude/skills/architect/SKILL.md
cp skills/backend/SKILL.md ~/.claude/skills/backend/SKILL.md
cp skills/frontend/SKILL.md ~/.claude/skills/frontend/SKILL.md
cp skills/qa/SKILL.md ~/.claude/skills/qa/SKILL.md
```

## Adding New Tasks

Edit `evaluate/tasks.md` to add tasks for a role. Follow the existing format:
task ID, context, requirements, and expected output format.

Then add corresponding checklist items to the rubric in `evaluate/rubrics.md`.

## Adding New Roles

1. Create `skills/<role>/SKILL.md` with initial skill definition
2. Add tasks in `evaluate/tasks.md` under a new `## <Role> Tasks` section
3. Add a rubric in `evaluate/rubrics.md` under a new `## <Role> Rubric` section
