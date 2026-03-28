# QA Rubric

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

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Coverage breadth** (1=only happy path, 3=good coverage, 5=comprehensive coverage of all dimensions)
2. **Edge case depth** (1=obvious cases only, 3=includes boundaries, 5=exhaustive edge cases including obscure ones)
3. **Clarity** (1=hard to understand what's being tested, 3=mostly clear, 5=test intent is immediately obvious)
4. **Maintainability** (1=fragile tests, 3=acceptable, 5=developer can easily understand and extend)
5. **Regression detection** (1=tests pass even with bugs, 3=catches some regressions, 5=would catch real production bugs)
