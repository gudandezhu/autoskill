# DevOps Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Reproducible builds**: Build outputs are deterministic, versioned, and can be recreated from the same commit (no floating tags like `latest` in FROM statements)
- [ ] **Health checks**: All services have health/readiness probes defined with specific endpoints and thresholds
- [ ] **No secrets in code**: No passwords, API keys, or tokens in plaintext; uses env vars, secret references, or vault integration
- [ ] **Rollback capability**: There is a documented or automated way to revert a failed deployment
- [ ] **Resource limits**: CPU and memory limits defined for all containers/services
- [ ] **Environment parity**: Dev/staging/prod use the same base images and configuration approach (only values differ)
- [ ] **Structured code**: Config files are organized, not one monolithic blob; uses overlays, includes, or separate files where appropriate
- [ ] **Failure isolation**: One service failure does not cascade to others (network policies, circuit breakers, or resource boundaries)
- [ ] **Clear naming**: Services, containers, and resources have descriptive, consistent names following a convention
- [ ] **Explicit failure handling**: Pipeline/manifest includes specific error handling steps (retry logic, timeout, failure notifications)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **Correctness** (1=configs don't match spec, 3=mostly correct with minor gaps, 5=perfectly matches all requirements)
2. **Reliability** (1=fragile with single points of failure, 3=reasonable redundancy, 5=highly available with automated failover and rollback)
3. **Security** (1=exposed services with no auth, 3=basic network isolation and secret management, 5=defense in depth with RBAC, network policies, and audit trail)
4. **Maintainability** (1=hardcoded values everywhere, 3=configurable via env vars, 5=fully parameterized with clear structure a new team member can understand)
5. **Clarity** (1=needs extensive tribal knowledge to deploy, 3=documentation covers basics, 5=new team member can deploy confidently from the output alone)
