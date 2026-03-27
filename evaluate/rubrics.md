# Evaluation Rubrics

This file defines the fixed scoring rubrics for evaluating skill outputs.
Do NOT modify this file during training. It serves the same purpose as
`evaluate_bpb` in autoresearch -- the ground truth metric.

Each rubric has two sections:
1. **Checklist** (binary pass/fail, 50 points total)
2. **Quality** (5 dimensions scored 1-5 each, scaled to 50 points)

Total score = Checklist + Quality = 0 to 100.

Apply rubrics strictly and mechanically. Be harsh, not generous.

---

## Architect Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Structured output**: Document uses markdown with clear section headers (overview, design, data model, etc.)
- [ ] **Overview/summary**: Includes a 2-3 sentence executive summary at the top
- [ ] **Concrete types**: Specifies actual data types (uuid, varchar(255), int64) not vague terms ("appropriate type", "string")
- [ ] **Error handling**: Explicitly addresses error handling strategy (what errors, how to handle, what to return to caller)
- [ ] **Security considerations**: Addresses at least 2 security concerns (auth, input validation, encryption, etc.)
- [ ] **Alternatives analyzed**: Compares at least 2 approaches with trade-offs, not just presents one solution
- [ ] **Risks section**: Has a "Risks" or "Assumptions" section identifying potential issues
- [ ] **Justified choices**: Technology/architecture choices include reasoning, not just listing
- [ ] **Scalability**: Addresses how the design handles growth (users, data, traffic)
- [ ] **Consistent naming**: All terms, services, and data models use consistent, unambiguous naming throughout

### Quality Dimensions (5 dimensions, scored 1-5, sum * 10 = 50 points)

1. **Completeness** (1=misses major requirements, 3=covers most, 5=all requirements addressed thoroughly)
2. **Clarity** (1=confusing, needs clarification, 3=understandable, 5=a developer can implement without asking questions)
3. **Practicality** (1=blue-sky/theoretical, 3=implementable with effort, 5=production-ready design)
4. **Trade-off awareness** (1=presents single solution dogmatically, 3=mentions alternatives, 5=mature analysis of costs and benefits)
5. **Conciseness** (1=verbose with filler, 3=adequate detail, 5=every sentence is necessary and actionable)

---

## Backend Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Input validation**: All function/service inputs are validated before processing
- [ ] **Error responses**: Errors return specific, actionable messages (not generic "bad request")
- [ ] **Appropriate HTTP status codes**: Uses correct status codes (201, 400, 404, 409, 500, 503, etc.)
- [ ] **No secrets in code**: No hardcoded passwords, API keys, or credentials; uses env vars/config
- [ ] **Structured code**: Code is organized into functions/modules, not one monolithic block
- [ ] **Clear naming**: Functions and variables have descriptive, consistent names
- [ ] **Edge case handling**: Handles null, empty, boundary, and unexpected inputs
- [ ] **No security vulnerabilities**: No SQL injection, XSS, or other OWASP issues
- [ ] **Resource handling**: Connections, file handles, or other resources are properly managed
- [ ] **Correct types**: Function signatures use appropriate types (not all `any` or `string`)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 10 = 50 points)

1. **Correctness** (1=doesn't match spec, 3=mostly correct, 5=perfectly matches specification)
2. **Robustness** (1=breaks on unexpected input, 3=handles most cases, 5=graceful degradation everywhere)
3. **Code quality** (1=spaghetti, 3=readable, 5=clean, well-organized, idiomatic)
4. **Idiomatic** (1=fights the framework, 3=acceptable, 5=follows language/framework conventions perfectly)
5. **Efficiency** (1=unnecessary complexity/redundancy, 3=reasonable, 5=minimal and efficient)

---

## Frontend Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Loading state**: Component shows loading indicator during async operations (not blank screen)
- [ ] **Error state**: Component displays error message with recovery action when operations fail
- [ ] **Empty state**: Component handles the case where there is no data to display
- [ ] **Semantic HTML**: Uses semantic elements (button, nav, form, label) not generic divs
- [ ] **Accessible labels**: Interactive elements have associated labels, aria-labels, or aria-describedby
- [ ] **Keyboard navigable**: Interactive elements are reachable and operable via keyboard (tab, enter, escape)
- [ ] **No layout shift**: State changes (loading → content, empty → results) don't cause jarring layout shifts
- [ ] **Responsive**: Design adapts to different screen sizes (or responsive behavior is considered)
- [ ] **Configurable**: Values that should be configurable (page size, debounce time) are not hardcoded
- [ ] **Clean event handling**: Event listeners are properly managed (no memory leaks, proper cleanup)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 10 = 50 points)

1. **UX completeness** (1=missing specified interactions, 3=most work, 5=all specified interactions implemented)
2. **Accessibility** (1=not accessible, 3=basic a11y, 5=screen reader friendly, keyboard only usable)
3. **Component design** (1=monolithic, 3=decent separation, 5=reusable, well-encapsulated, clean API)
4. **State management** (1=spaghetti state, 3=works, 5=clean, predictable, no race conditions)
5. **Polish** (1=raw/functional, 3=decent, 5=feels production-quality with attention to detail)

---

## QA Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Happy path covered**: Tests cover the main success scenario
- [ ] **Error/edge cases covered**: Tests cover invalid inputs, boundary values, and failure modes
- [ ] **Descriptive test names**: Each test name states the expected behavior (e.g., "should reject negative age")
- [ ] **Test independence**: Tests don't depend on each other; can run in any order
- [ ] **Clear structure**: Tests follow arrange/act/assert pattern clearly
- [ ] **Boundary values tested**: Minimum, maximum, and just-beyond-boundary values are tested
- [ ] **Negative cases tested**: Invalid inputs (null, wrong type, empty string, out of range) are tested
- [ ] **Error message verification**: Tests verify specific error messages, not just "error thrown"
- [ ] **No test interdependencies**: No shared mutable state between tests
- [ ] **Bug-finding potential**: Tests would catch real bugs, not just verify the happy path works

### Quality Dimensions (5 dimensions, scored 1-5, sum * 10 = 50 points)

1. **Coverage breadth** (1=only happy path, 3=good coverage, 5=comprehensive coverage of all dimensions)
2. **Edge case depth** (1=obvious cases only, 3=includes boundaries, 5=exhaustive edge cases including obscure ones)
3. **Clarity** (1=hard to understand what's being tested, 3=mostly clear, 5=test intent is immediately obvious)
4. **Maintainability** (1=fragile tests, 3=acceptable, 5=developer can easily understand and extend)
5. **Regression detection** (1=tests pass even with bugs, 3=catches some regressions, 5=would catch real production bugs)

---

## Scoring Protocol

### How to score

1. Read the task requirements carefully.
2. Read the generated output.
3. Go through each checklist item. Award 5 points if the criterion is clearly
   met in the output, 0 if not. Be strict -- partial credit is not given for
   checklist items.
4. Score each quality dimension from 1 to 5 based on the scale descriptions.
5. Calculate: `total = (checklist_points) + (sum_of_quality_scores * 2)`
6. Report the score in this format:

```
Task: <task-id>
Checklist: X/10 items passed = Y points
Quality: (A+B+C+D+E) = Z (range 5-25) → Z * 2 = W points (range 10-50)
Total: Y + W = T points
```

### Important rules

- **Be consistent**: Score the same standard across all experiments. Don't get
  more lenient over time.
- **No partial credit on checklist**: Either the criterion is met or it isn't.
- **Quality scores are integers**: Round to the nearest integer, 1-5.
- **Don't compare to other experiments**: Score each output independently against
  the rubric. The training loop handles comparison.
- **Don't read the SKILL.md**: Evaluate only the output quality against the task
  requirements and rubric. The skill that produced it is irrelevant to scoring.
