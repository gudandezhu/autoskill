# Scoring Protocol

This is the shared scoring protocol used by all role rubrics.
Each role's specific checklist and quality dimensions are in `roles/<role>/rubric.md`.

## How to score

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

## Important rules

- **Be consistent**: Score the same standard across all experiments. Don't get
  more lenient over time.
- **No partial credit on checklist**: Either the criterion is met or it isn't.
- **Quality scores are integers**: Round to the nearest integer, 1-5.
- **Don't compare to other experiments**: Score each output independently against
  the rubric. The training loop handles comparison.
- **Don't read the SKILL.md**: Evaluate only the output quality against the task
  requirements and rubric. The skill that produced it is irrelevant to scoring.
