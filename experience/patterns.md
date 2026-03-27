# Accumulated Patterns

This file stores generalizable patterns discovered during training.
Patterns are tagged with priority [P1] (critical) through [P5] (nice-to-have).
Maximum 200 lines. Prune lowest-priority stale patterns when exceeded.

## Format

Each pattern is a single line:
```
- [PX] Role: specific, actionable description
```

Priority guide:
- [P1] Must always follow. Violation causes clear score drops.
- [P2] Should almost always follow. Violation causes moderate score drops.
- [P3] Generally good practice. Violation causes minor score drops.
- [P4] Nice to have. Minor positive impact.
- [P5] Edge case or niche pattern. Situation-dependent.

## architect

- [P1] architect: For service design tasks, include CREATE TABLE statements with actual column types, constraints, and indexes for each service's database
- [P1] architect: Always include a dedicated Security section addressing inter-service auth, data encryption, and compliance scope
- [P1] architect: Each of error handling, security, scalability, monitoring must have a dedicated section — not just mentioned in passing

## backend

- [P1] backend: Validate ALL external/untrusted inputs including nested payload fields, not just top-level request body
- [P1] backend: Define TypeScript interfaces for all data structures — never use `any`
- [P2] backend: Always include graceful shutdown handling for long-running processes (SIGTERM/SIGINT)

## frontend

(no patterns yet)

## qa

(no patterns yet)
