# Backend Rubric

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

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Correctness** (1=doesn't match spec, 3=mostly correct, 5=perfectly matches specification)
2. **Robustness** (1=breaks on unexpected input, 3=handles most cases, 5=graceful degradation everywhere)
3. **Code quality** (1=spaghetti, 3=readable, 5=clean, well-organized, idiomatic)
4. **Idiomatic** (1=fights the framework, 3=acceptable, 5=follows language/framework conventions perfectly)
5. **Efficiency** (1=unnecessary complexity/redundancy, 3=reasonable, 5=minimal and efficient)
