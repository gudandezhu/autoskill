# autoskill

This is an autonomous skill training system. It iteratively improves
Claude Code skills by running tasks, scoring outputs, and keeping
or discarding changes -- similar to how autoresearch trains models.

## Setup

To set up a new training run, work with the user to:

1. **Agree on a target skill**: the user specifies which skill to train
   (one of: `architect`, `backend`, `frontend`, `qa`). This is the ONLY
   skill that will be trained during this run.
2. **Agree on a run tag**: propose a tag based on today's date (e.g. `mar27`).
   The branch `autoskill/<tag>-<skill>` must not already exist.
3. **Create the branch**: `git checkout -b autoskill/<tag>-<skill>` from current master.
4. **Read the in-scope files** for full context:
   - `roles/<skill>/tasks.md` -- fixed task suite. Do not modify.
   - `roles/<skill>/rubric.md` -- fixed scoring rubrics. Do not modify.
   - `roles/<skill>/SKILL.md` -- the file you modify.
   - `experience/patterns.md` -- accumulated best practices.
5. **Initialize results.tsv**: Create with header row if not present:
   ```
   commit	task	score	delta	lines	status	description
   ```
6. **Establish baseline**: For each task of the target skill, execute the task
   using the current SKILL.md and score it. Record these as baseline entries.
7. **Confirm and go**.

Once you get confirmation, kick off the experimentation.

## Experimentation

Each experiment evaluates a single SKILL.md modification against a single task.

**What you CAN do:**
- Modify `roles/<skill>/SKILL.md` -- this is the only file you edit for the skill itself.
- Read `experience/patterns.md` for inspiration when proposing changes.
- Add to `experience/patterns.md` when a kept change reveals a new generalizable pattern.
- Prune `experience/patterns.md` when it exceeds 200 lines.

**What you CANNOT do:**
- Modify `roles/<skill>/tasks.md` or `roles/<skill>/rubric.md`. These are read-only.
- Modify `autoskill.md`. This is human-controlled.
- Install packages or add dependencies.
- Make the evaluation easier by leaking rubric specifics into the skill prompt.

**The goal: maximize the average rubric score across all tasks for the target skill.**

**Simplicity criterion**: All else being equal, simpler is better. A skill that is 10 lines shorter with equal score is strictly better. Prefer concise, actionable instructions over verbose explanations. A skill over 200 lines should be pruned. When evaluating whether to keep a change, weigh the score improvement against any added complexity. A 3-point improvement that adds 20 lines of filler is probably not worth it. A 3-point improvement from deleting code is definitely worth it.

## Evaluation Protocol

For each experiment:

1. **Select task**: Pick the next task for the target skill from `roles/<skill>/tasks.md`.
   Prefer tasks with fewer experiments. Track which tasks have been tested.

2. **Modify**: Make one experimental change to `roles/<skill>/SKILL.md`.
   Keep changes small and targeted. One idea per experiment.

3. **Commit**: `git commit -m "hypothesis: ..."` describing what you expect to improve.

4. **Execute**: Run the task using the modified skill.
   - Generate the output as if you were the agent following the skill instructions.
   - Save the output to a temporary file or keep it in context.

5. **Score**: Evaluate the output against the rubric in `roles/<skill>/rubric.md`.
   - Use a fresh evaluation context. Do NOT let the scoring process see the SKILL.md.
   - Apply the rubric strictly and mechanically.
   - Score = checklist_score (0-50) + quality_score (10-50, = sum_of_5_dimensions * 2) = total (10-100).

6. **Record**: Log the result in `results.tsv`.

7. **Decide**:
   - If score >= baseline_for_this_task + 3: KEEP. The branch advances.
   - If score < baseline + 3: DISCARD. `git reset`.
   - If crash: investigate, fix if trivial, skip if fundamental.

## Output Format

Each evaluation produces a structured score:

```
Task: <task-id>
Checklist: X/10 items passed = Y points (range 0-50)
Quality: (A+B+C+D+E) = Z (range 5-25) → Z * 2 = W points (range 10-50)
Total: Y + W = T points
```

## Logging Results

The TSV has 8 columns (tab-separated, NOT comma-separated):

```
commit	task	score	delta	lines	status	description
```

1. git commit hash (short, 7 chars)
2. task identifier (e.g. `architect-001`)
3. score achieved (10-100, use 0 for crashes)
4. delta from baseline for this task (e.g. `+7` or `-2`, use `baseline` for first run)
5. SKILL.md line count (track complexity, like memory_gb in autoresearch)
6. status: `keep`, `discard`, or `crash`
7. short text description of the experimental change

Example:

```
commit	task	score	delta	lines	status	description
a1b2c3d	architect-001	72	baseline	39	baseline	baseline
b2c3d4e	architect-001	81	+9	42	keep	add "enumerate 3 alternatives" rule
c3d4e5f	architect-002	68	baseline	42	baseline	baseline
d4e5f6g	architect-002	65	-3	55	discard	add verbose explanation template
e5f6g7h	architect-001	0	crash	42	crash	rename section (invalid markdown)
```

## The Experiment Loop

The experiment runs on a dedicated branch (e.g. `autoskill/mar27-architect`).

LOOP FOREVER:

1. Look at the git state: current branch/commit.
2. Read `results.tsv` for experiment history. Avoid repeating failed ideas.
3. Select the next task (prefer tasks with fewer experiments).
4. Read current SKILL.md, experience/patterns.md, and the task description.
5. Form a hypothesis: "Adding/Removing/Changing X should improve score on Y because Z."
6. Modify SKILL.md with the experimental change. Keep it small and targeted.
7. `git commit -m "hypothesis: ..."`
8. Execute the task with the modified skill. Generate output.
9. Score the output against the rubric (fresh context, mechanical application).
10. Record in results.tsv (do NOT commit results.tsv -- leave it untracked).
11. If score >= baseline + 3: KEEP. Extract any new patterns into patterns.md.
12. If score < baseline + 3: DISCARD. `git reset`.
13. If crash: read the error, fix if trivial, skip if fundamental. Log `crash` status.

The idea is that you are a completely autonomous skill trainer trying out prompt
improvements. If they work, keep. If they don't, discard. The branch advances
with each improvement so you can iterate on top of the best known version.

**Timeout**: Each experiment should take ~2-5 minutes (task execution + scoring).
If an experiment stalls for more than 10 minutes, skip it and move on.

**Crashes**: If the task execution fails, use your judgment. If it's something
trivial (a formatting error in SKILL.md), fix it and re-run. If the experimental
change itself is fundamentally broken, skip it, log `crash`, and move on.

**Avoiding repeats**: Before proposing a change, check results.tsv for the same
task. Do not repeat an exact idea that was already discarded. Try a variation
or a different angle instead.

**Pattern extraction**: When you KEEP a change, ask yourself:
"What general principle made this work?" If it's not already in
experience/patterns.md, add it with a priority tag [P1]-[P5].

**Pattern pruning**: If experience/patterns.md exceeds 200 lines, remove the
lowest-priority patterns that have not contributed to a kept change in the
last 10 experiments.

**Task evolution**: Every 50 experiments, review results.tsv. If ALL tasks
score above 90, the skill has plateaued. Consider proposing harder task
variants to the human (but do NOT modify tasks.md yourself).

**NEVER STOP**: Once the experiment loop has begun (after the initial setup),
do NOT pause to ask the human if you should continue. Do NOT ask "should I keep
going?" or "is this a good stopping point?". The human might be asleep or gone
and expects you to continue working *indefinitely* until manually stopped. You
are autonomous. If you run out of ideas, think harder -- re-read patterns.md,
try combining previous near-misses, try removing instructions that might be
redundant, try more radical restructuring. The loop runs until the human
interrupts you, period.

As a use case, a user might leave you running overnight. If each experiment
takes ~3 minutes, that's ~20/hour, or ~160 experiments over 8 hours. The user
wakes up to a significantly improved skill.
