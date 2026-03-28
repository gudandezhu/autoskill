---
name: generate-baseline
description: "Generate evaluation tasks and rubrics for a skill role. Usage: /generate-baseline <role>"
---

# Baseline Generator

You generate evaluation baselines (tasks + rubrics) for an autoskill role.
The user invoked: `/generate-baseline $ARGUMENTS`

## Phase 0: Validate Input

1. Parse `$ARGUMENTS` to extract the role name.
2. If no role provided, stop and tell the user: `Usage: /generate-baseline <role>`
3. Verify `roles/$ROLE/SKILL.md` exists. If not, stop and suggest creating it first.
4. Check if tasks for this role already exist in `roles/$ROLE/tasks.md`.
   - If the file exists, warn the user and ask: "Tasks for **$ROLE** already exist at `roles/$ROLE/tasks.md`. Overwrite? (y/n)"
   - If the user says no, stop.
5. Check if a rubric for this role already exists in `roles/$ROLE/rubric.md`.
   - If the file exists, warn the user and ask: "Rubric for **$ROLE** already exists at `roles/$ROLE/rubric.md`. Overwrite? (y/n)"
   - If the user says no, stop.
6. Confirm with the user: "Generate evaluation baselines for **$ROLE**? This will create `roles/$ROLE/tasks.md` (3 tasks) and `roles/$ROLE/rubric.md` (10 checklist items + 5 quality dimensions)."

## Phase 1: Analyze Skill

Read `roles/$ROLE/SKILL.md` and all files listed in its `references` frontmatter field.

Extract these characteristics:

### 1.1 Output Type
Classify the skill's primary output into ONE of these categories:

| Category | Description | Examples |
|----------|-------------|---------|
| `code` | Produces executable code | backend, frontend, devops |
| `document` | Produces design/plan documents | architect |
| `test` | Produces test code or test plans | qa |
| `interactive` | Multi-turn dialogue with structured output | explorer |
| `hybrid` | Combines multiple output types across phases | agile |

### 1.2 Domain Keywords
Extract domain-specific terms from the skill's Process, Output Format, and Principles sections.
These will inform task scenarios and checklist items.

### 1.3 Core Concerns
Identify which of these concerns the skill explicitly addresses:
- Security (auth, validation, encryption)
- Performance (latency, throughput, optimization)
- Correctness (types, validation, error handling)
- UX (accessibility, responsiveness, state management)
- Maintainability (naming, structure, modularity)
- Scalability (growth, distribution, sharding)
- Reliability (error handling, retries, fallbacks)
- Observability (logging, metrics, tracing)

### 1.4 Required Process Steps
List the numbered steps from the skill's Process section. These are mandatory behaviors that checklist items should verify.

### 1.5 Key Principles
Extract the bullet points from the skill's Principles section. These express values that quality dimensions should measure.

## Phase 2: Generate Rubric

Based on the Phase 1 analysis, generate a rubric with 10 checklist items and 5 quality dimensions.

### 2.1 Checklist Generation

**Step 1 — Extract from skill content (5-7 items):**

- Convert each Process step into a binary checklist item.
  Example: Process step "Validate ALL inputs at the boundary" → Checklist item "**Input validation**: All inputs are validated before processing"
- Convert key Principles into checklist items where they can be judged as present/absent.
  Example: Principle "Prefer simplicity over cleverness" → Checklist item "**Justified choices**: Technology/architecture choices include reasoning, not just listing"

**Step 2 — Add domain-specific items from the catalog below (3-5 items):**

Pick items that match the skill's core concerns and output type. Ensure no overlap with Step 1 items.

#### Code-type catalog
- **Input validation**: All function/service inputs validated before processing
- **Error responses**: Errors return specific, actionable messages
- **No secrets in code**: No hardcoded passwords, API keys; uses env vars/config
- **Structured code**: Code organized into functions/modules, not monolithic
- **Clear naming**: Functions and variables have descriptive, consistent names
- **Edge case handling**: Handles null, empty, boundary, unexpected inputs
- **No security vulnerabilities**: No injection, XSS, or OWASP issues
- **Resource handling**: Connections, file handles properly managed
- **Correct types**: Function signatures use appropriate types (not all `any`)
- **Appropriate status codes**: Uses correct HTTP status codes where applicable

#### Document-type catalog
- **Structured output**: Markdown with clear section headers
- **Overview/summary**: 2-3 sentence executive summary at the top
- **Concrete types**: Specifies actual data types (uuid, varchar(255), int64) not vague terms
- **Error handling**: Explicitly addresses error handling strategy
- **Security considerations**: Addresses at least 2 security concerns
- **Alternatives analyzed**: Compares at least 2 approaches with trade-offs
- **Risks section**: Has a "Risks" or "Assumptions" section
- **Justified choices**: Technology/architecture choices include reasoning
- **Scalability**: Addresses how design handles growth
- **Consistent naming**: All terms use consistent, unambiguous naming

#### Test-type catalog
- **Happy path covered**: Tests cover the main success scenario
- **Error/edge cases covered**: Tests cover invalid inputs and failure modes
- **Descriptive test names**: Each test name states expected behavior
- **Test independence**: Tests don't depend on each other
- **Clear structure**: Tests follow arrange/act/assert pattern
- **Boundary values tested**: Min, max, and just-beyond values tested
- **Negative cases tested**: Invalid inputs tested (null, wrong type, empty)
- **Error message verification**: Tests verify specific error messages
- **No test interdependencies**: No shared mutable state
- **Bug-finding potential**: Tests would catch real bugs, not just verify happy path

#### Interactive-type catalog
- **Structured output**: Final output uses clear markdown sections
- **Clarifying questions**: Asks focused questions before deep exploration
- **Concrete specifics**: Grounds advice in specifics, not abstractions
- **Multiple perspectives**: Presents 2+ viewpoints or approaches
- **Actionable outcomes**: Conclusions include concrete next steps
- **User acknowledgment**: Validates or addresses user's stated concerns
- **Appropriate depth**: Explores non-obvious angles, not just surface level
- **Logical flow**: Exploration follows a coherent progression
- **Risk awareness**: Identifies potential issues or downsides
- **Adaptive to context**: Adjusts depth and approach to the scenario

**Step 3 — Validate checklist:**
- Count: exactly 10 items
- Each item is binary (present/absent, no partial credit)
- No overlap between items (each checks a distinct thing)
- At least 3 items come from the skill's own Process/Principles
- At least 2 items relate to the skill's core concerns

### 2.2 Quality Dimensions Generation

Select 5 dimensions from the templates below based on output type. Customize the 1/3/5 descriptions to match the skill's domain.

#### Code-type template
1. **Correctness** (1=doesn't match spec, 3=mostly correct, 5=perfectly matches specification)
2. **Robustness** (1=breaks on unexpected input, 3=handles most cases, 5=graceful degradation everywhere)
3. **Code quality** (1=spaghetti, 3=readable, 5=clean, well-organized, idiomatic)
4. **Idiomatic** (1=fights the framework, 3=acceptable, 5=follows language/framework conventions perfectly)
5. **Efficiency** (1=unnecessary complexity/redundancy, 3=reasonable, 5=minimal and efficient)

#### Document-type template
1. **Completeness** (1=misses major requirements, 3=covers most, 5=all requirements addressed thoroughly)
2. **Clarity** (1=confusing, needs clarification, 3=understandable, 5=a developer can implement without asking questions)
3. **Practicality** (1=blue-sky/theoretical, 3=implementable with effort, 5=production-ready design)
4. **Trade-off awareness** (1=single solution dogmatically, 3=mentions alternatives, 5=mature analysis of costs and benefits)
5. **Conciseness** (1=verbose with filler, 3=adequate detail, 5=every sentence is necessary and actionable)

#### Test-type template
1. **Coverage breadth** (1=only happy path, 3=good coverage, 5=comprehensive coverage of all dimensions)
2. **Edge case depth** (1=obvious cases only, 3=includes boundaries, 5=exhaustive edge cases including obscure ones)
3. **Clarity** (1=hard to understand what's being tested, 3=mostly clear, 5=test intent is immediately obvious)
4. **Maintainability** (1=fragile tests, 3=acceptable, 5=developer can easily understand and extend)
5. **Regression detection** (1=tests pass even with bugs, 3=catches some regressions, 5=would catch real production bugs)

#### Interactive-type template
1. **Depth of insight** (1=surface level only, 3=goes beyond obvious, 5=reveals non-obvious insights and connections)
2. **Relevance** (1=tangential to user's needs, 3=mostly relevant, 5=every point directly serves the user's goal)
3. **Clarity** (1=confusing or jargon-heavy, 3=understandable, 5=immediately clear and actionable)
4. **Actionability** (1=vague advice, 3=specific directions, 5=precise steps someone could execute today)
5. **Adaptiveness** (1=rigid script regardless of input, 3=adjusts somewhat, 5=tailored response that fits the specific scenario)

#### Hybrid-type template
Use the dominant output type's template as a base, then replace 1-2 dimensions with ones from the secondary type.

### 2.3 Rubric Format

Generate the rubric in this exact format (matching existing rubrics like `roles/architect/rubric.md`):

```
## $ROLE Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Item name**: Description
- [ ] **Item name**: Description
... (10 items total)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Dimension** (1=poor description, 3=adequate description, 5=excellent description)
... (5 dimensions total)
```

## Phase 3: Generate Tasks

Generate 3 tasks that test different dimensions of the skill.

### Task Design Rules

1. **Each task must have**: Context, Requirements (3-8 items), and Output format.
2. **Context must include**: Real-world business scenario with specific constraints (numbers, scale, performance targets).
3. **Requirements must be specific**: Not "design a system" but "design REST endpoints with request/response formats".
4. **Output format must be explicit**: State what format, what sections, what level of detail.
5. **Tasks must be diverse**: Each task tests a different capability dimension.

### Task 1: Basic Capability (straightforward application)

- Tests: Core process execution with clear requirements
- Difficulty: Direct application of skill's primary workflow
- Context: A well-defined scenario where all requirements are explicit
- Should be solvable by correctly following the skill's Process steps

### Task 2: Problem Diagnosis (analytical thinking)

- Tests: Ability to analyze, diagnose, and improve
- Difficulty: Requires identifying issues in existing work
- Context: A problematic situation — slow query, bad code, unclear design, vague requirements
- Must present concrete evidence of the problem (error logs, metrics, user feedback)

### Task 3: Complex/Integrated Scenario (synthesis)

- Tests: Ability to handle ambiguity, scale, or conflicting requirements
- Difficulty: Real-world complexity — incomplete info, trade-offs, multiple stakeholders
- Context: A larger-scope scenario with realistic constraints
- Should require balancing competing concerns

### Task Format

```markdown
### $ROLE-<NNN>: <Title>

**Context**: <Business scenario with specific numbers and constraints>

**Requirements**:
- <Specific requirement 1>
- <Specific requirement 2>
...

**Output**: <Expected format and deliverables>
```

Task numbering starts from 001. If existing tasks exist for other roles, continue numbering from the next available number (but use `$ROLE-001` format regardless).

## Phase 4: Validate

Run this self-check before writing output. If any check fails, revise the generated content and re-validate.

### Validation Checklist

- [ ] **Checklist independence**: No two checklist items test the same thing
- [ ] **Quality orthogonality**: No two quality dimensions overlap significantly
- [ ] **Task diversity**: Tasks cover different capability dimensions (basic/diagnostic/complex)
- [ ] **Concrete requirements**: Every requirement in every task is specific and measurable
- [ ] **Score range**: Minimum possible score is 10, maximum is 100
- [ ] **Format compliance**: Matches the exact format of existing rubrics and tasks
- [ ] **Skill alignment**: Checklist items reflect the skill's actual Process and Principles
- [ ] **No rubric leakage**: Checklist items don't reveal evaluation criteria that would trivially boost scores without genuine quality improvement

### Sanity Check

Mentally simulate two extremes:
1. **Perfect output** (follows every Process step, addresses every Principle): Should score 90-100
2. **Terrible output** (ignores Process, generic response): Should score 10-25

If the perfect output can't reach 90+, the rubric is too strict. If the terrible output can reach 40+, it's too lenient.

## Phase 5: Output

### 5.1 Create roles directory

Create `roles/$ROLE/` directory if it does not exist.

### 5.2 Write Tasks

Write the generated tasks to `roles/$ROLE/tasks.md`.

```markdown
# $ROLE Tasks

### $ROLE-001: <Title>
... (full task content)

### $ROLE-002: <Title>
... (full task content)

### $ROLE-003: <Title>
... (full task content)
```

### 5.3 Write Rubric

Write the generated rubric to `roles/$ROLE/rubric.md`.

```markdown
# $ROLE Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Item name**: Description
... (10 items total)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Dimension** (1=poor, 3=adequate, 5=excellent)
... (5 dimensions total)
```

Note: The rubric file does NOT include the shared scoring protocol. That lives in `evaluate/scoring-protocol.md`.

### 5.4 Summary Report

Print this summary for the user:

```
=== Baseline Generation Complete ===

Role: $ROLE
Skill type: <code|document|test|interactive|hybrid>
Files created:
  - roles/$ROLE/tasks.md (3 tasks)
  - roles/$ROLE/rubric.md (10 checklist items + 5 quality dimensions)

Tasks generated:
  1. $ROLE-001: <title> (basic capability)
  2. $ROLE-002: <title> (problem diagnosis)
  3. $ROLE-003: <title> (complex scenario)

Rubric generated:
  Checklist: 10 items, 50 points
  Quality: 5 dimensions, 10-50 points
  Total range: 10-100

Core concerns addressed: <list>
Key dimensions: <list 5 quality dimensions>

Next step: Run `/autoskill $ROLE` to start training.
```
