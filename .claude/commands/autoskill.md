---
name: autoskill
description: "Autonomous skill training. Usage: /autoskill <role> (any role under roles/)"
---

# Autoskill Training Runner

You are an autonomous skill trainer. Your job is to iteratively improve a Claude Code skill by modifying its SKILL.md, running evaluation tasks, scoring the output, and keeping or discarding changes via git.

The user invoked: `/autoskill $ARGUMENTS`

## Phase 0: Validate Input

1. Parse `$ARGUMENTS` to extract the role. Valid roles: any directory name under `roles/` that contains `SKILL.md`, `tasks.md`, and `rubric.md`.
2. If no role provided or the directory/files don't exist, stop and tell the user to run `/autoskill <role>` with a valid role.
3. Confirm with the user: "Start training **$ROLE**? This will create branch `autoskill/<date>-<role>` and run experiments autonomously."
4. Auto proceeding

## Phase 1: Setup

Read these files for full context:
- `autoskill.md` — the training program (follow it exactly)
- `roles/$ROLE/tasks.md` — fixed task suite for this role (NEVER modify)
- `roles/$ROLE/rubric.md` — fixed scoring rubric for this role (NEVER modify)
- `roles/$ROLE/SKILL.md` — the trainable skill (this is the primary file you edit)
- `roles/$ROLE/*.md` — reference files listed in SKILL.md's `references` frontmatter (read for context, can also edit)
- `experience/patterns.md` — accumulated best practices

Then execute these steps:

1. **Create run tag**: Use today's date as tag (e.g. `mar28`). The branch name is `autoskill/<tag>-<role>`.
2. **Create branch**: `git checkout -b autoskill/<tag>-<role>` from current main. If branch already exists, fail and ask user to delete it or pick another tag.
3. **Initialize results.tsv**: If `results.tsv` does not exist, create it with this header:
   ```
   commit	task	score	delta	lines	status	direction	description
   ```
4. **Establish baseline**: For EACH task of the target role in `roles/$ROLE/tasks.md`:
   a. Read the task description.
   b. Execute the task **3 times** by generating output as if you are an agent following `roles/$ROLE/SKILL.md`. Each run must be independent — do not reuse output from a previous run.
   c. Score each run against the rubric in `roles/$ROLE/rubric.md` using a fresh evaluation context:
      - Go through each of the 10 checklist items. Award 5 if clearly present, 0 if not.
      - Score each of the 5 quality dimensions from 1 to 5.
      - Calculate: `total = checklist_points + (sum_of_quality_scores * 2)`
   d. The baseline for this task is the **average** of the 3 scores.
   e. Record all 3 runs in `results.tsv` with delta=`baseline`, status=`baseline`.
5. Report the baseline scores to the user in a summary table showing each task's 3 runs and average.
6. Ask the user to confirm to start the experiment loop.

## Phase 2: Experiment Loop

Once confirmed, run the loop up to the agreed experiment budget. Do NOT pause to ask the user to continue.

LOOP (up to experiment budget):

1. **Check git state**: Verify we are on the training branch. Get current commit hash.
2. **Review history**: Read `results.tsv` to see what has been tried. Avoid repeating exact ideas that were discarded.
3. **Select task**: Pick the task with the fewest experiments. Track experiment counts per task.
4. **Direction health check**: Check the `direction` column from recent results.tsv entries. If the same direction has 3+ consecutive DISCARDs, exclude that direction. Pick a different direction for this experiment.
5. **Form hypothesis**: Based on patterns.md, past results, reference files, and rubric criteria, form a specific hypothesis:
   "Adding/Removing/Changing X should improve score on <task-id> because Y."
   Tag it with a direction family (e.g. `security`, `structure`, `conciseness`, `error-handling`).
6. **Modify SKILL.md or reference files**: Make one small, targeted change to `roles/$ROLE/SKILL.md` or one of its reference files. Keep it minimal — one idea per experiment.
7. **Validate SKILL.md**: After modification, verify:
   - YAML frontmatter parses correctly (name, description, references fields)
   - All files listed in `references` exist in the same directory
   - Markdown structure is intact (no broken headers, lists, or links)
   If validation fails, fix or skip the experiment.
8. **Commit**: `git add roles/$ROLE/ && git commit -m "hypothesis: <your hypothesis>"` with a clear message. Commit only SKILL.md and its reference files.
9. **Execute task**: Generate output as if you are the agent following the modified SKILL.md.
   Produce a complete, production-quality response. Do not think about scoring while
   generating — focus only on following the skill instructions.
10. **Score output via subagent** (structural isolation):
    Spawn a fresh subagent using the Agent tool with `subagent_type: "general-purpose"`.
    The subagent prompt must:
    - Instruct it to read `roles/$ROLE/rubric.md` and `roles/$ROLE/tasks.md`
    - Provide the generated output to score
    - Explicitly forbid reading any file under `roles/$ROLE/` except `tasks.md` and `rubric.md`
    - Instruct it to apply the rubric mechanically and follow the scoring anchoring rules
    - Return the score in the standard format (checklist points + quality sum * 2)
    The subagent has a clean context — it genuinely does not know what SKILL.md
    contains or what experiment is being run. This is structural isolation.
11. **Record result**: Append to `results.tsv` (modify file, do NOT commit yet):
    ```
    <7-char-hash>	<task-id>	<score>	<+N or -N>	<line-count>	<keep|discard>	<direction>	<description>
    ```
    Where delta = score - baseline_for_this_task, and line-count = wc -l of SKILL.md.
12. **Decide**:
    - If score >= baseline + 3: **KEEP**. The branch advances. Extract any new generalizable pattern into `experience/patterns.md` with priority tag [P1]-[P5].
      Then commit results: `git add results.tsv && git commit -m "result: keep <task-id> <score>"`
    - If score < baseline + 3: **DISCARD**. Run `git reset HEAD~1` to undo the SKILL.md commit (results.tsv modification stays in working tree).
      Then commit results: `git add results.tsv && git commit -m "result: discard <task-id> <score>"`
    - If crash: `git reset HEAD~1` to undo the broken SKILL.md commit. If trivial formatting issue, fix and re-run. If fundamentally broken, log as `crash`, commit results, and move on.
14. **Reference maintenance**: After a KEEP, check SKILL.md body line count. If it exceeds 150 lines, extract a self-contained section into a new reference file. Add the file to the `references` frontmatter field and replace the inline content with a link. This is mandatory.
15. **Regression check**: Every 5 experiments, re-score ALL tasks for the target role using the current SKILL.md (execute in-session, score via subagent). If any task's score has dropped more than 5 points from its baseline, roll back to the last commit where all tasks were within 5 points of their baselines.
16. **Anti-pattern extraction**: When a direction family accumulates 3+ consecutive DISCARDs, add an anti-pattern to `experience/patterns.md`:
    `[ANTI] $ROLE: Adding/improving <X> shows diminishing returns — stop pursuing this direction.`
17. **Pattern pruning**: If `experience/patterns.md` exceeds 200 lines, remove lowest-priority stale patterns.
18. **Task evolution**: Every 10 experiments, check if ALL tasks score above 90. If so, notify the user that the skill has plateaued and suggest harder tasks (but do NOT modify tasks.md yourself).
19. **Budget check**: If experiment count reaches the agreed budget, report final summary (best scores per task, improvement totals, kept/discarded ratio) and stop.
20. Continue to the next iteration.

## Constraints

- **NEVER** modify `roles/$ROLE/tasks.md` or `roles/$ROLE/rubric.md`.
- **NEVER** modify `autoskill.md`.
- **NEVER** install packages or add dependencies.
- **NEVER** leak rubric specifics into SKILL.md (e.g., don't add "must have 10 checklist items" to the skill).
- **NEVER** stop the loop to ask if you should continue (except at budget exhaustion). You are autonomous.
- Only edit `roles/$ROLE/SKILL.md` and its reference files for the skill being trained.
- Only edit `experience/patterns.md` to add/prune patterns.
- Simplicity criterion: Prefer shorter, more concise SKILL.md. A 10-line reduction with equal score is a strict improvement. SKILL.md body over 150 lines must have content extracted to reference files.
- Each experiment should take ~2-5 minutes. If an experiment stalls for >10 minutes, skip it.

## Reporting

At the start of each loop iteration, briefly report:
```
--- Experiment #<N>/<budget> ---
Task: <task-id> (baseline: <score>, experiments so far: <count>)
Current SKILL.md: <lines> lines, commit: <hash>
Hypothesis: <one-line hypothesis> [direction: <tag>]
```

After scoring:
```
Result: <score> (<delta>) → KEEP/DISCARD
Checklist: <X>/10 = <Y>pts | Quality: <A>+<B>+<C>+<D>+<E> = <Z> → <W>pts
SKILL.md: <new-lines> lines
```

After budget exhaustion:
```
=== Training Complete ===
Experiments: <total> (kept: <N>, discarded: <N>, crashed: <N>)
Best scores: <task-id>: <best-score> (<improvement> from baseline), ...
SKILL.md: <lines> lines, <N> reference files
Patterns learned: <N> new patterns, <N> anti-patterns
```
