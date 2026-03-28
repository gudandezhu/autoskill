# Architect Rubric

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

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Completeness** (1=misses major requirements, 3=covers most, 5=all requirements addressed thoroughly)
2. **Clarity** (1=confusing, needs clarification, 3=understandable, 5=a developer can implement without asking questions)
3. **Practicality** (1=blue-sky/theoretical, 3=implementable with effort, 5=production-ready design)
4. **Trade-off awareness** (1=presents single solution dogmatically, 3=mentions alternatives, 5=mature analysis of costs and benefits)
5. **Conciseness** (1=verbose with filler, 3=adequate detail, 5=every sentence is necessary and actionable)
