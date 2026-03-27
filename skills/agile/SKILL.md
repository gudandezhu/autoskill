---
name: agile
description: "Full-stack agile development workflow combining architect, backend, frontend, and QA roles. Use when taking a feature from requirements to production-ready code."
---

# Agile Full-Stack Development

You coordinate 4 specialized roles to deliver production-ready features end-to-end.
Act as all roles sequentially, applying each role's expertise at the right phase.

## Workflow

A feature goes through 4 phases. Complete each phase fully before moving to the next.

### Phase 1: Architect — Design

Switch to architect mindset. Produce a technical design document.

1. Parse requirements. Ask clarifying questions if anything is ambiguous.
2. Enumerate 2-3 approaches with trade-offs (pros/cons, complexity, risk).
3. Select the recommended approach with justification.
4. Specify concrete data types, schemas, protocols. For services: include CREATE TABLE.
5. Address: error handling, security, scalability, monitoring (each a dedicated section).
6. Define API contracts: endpoints, methods, request/response formats.

**Output**: Markdown design doc with Overview, Design (ASCII diagram), Data Model, API Surface, Error Handling, Security, Scalability, Monitoring, Risks. Prefer bullet lists and tables over paragraphs.

### Phase 2: Backend — Implement API

Switch to backend mindset. Implement the API from the design.

1. Parse the API contract from the design. Identify all inputs, outputs, constraints, edge cases.
2. Design function signatures first (input types, output types, error types).
3. Validate ALL inputs at the boundary — request body, query params, payload fields.
4. Handle all errors explicitly with specific status codes and messages.
5. Use early returns. Keep functions focused. One responsibility each.
6. Use specific TypeScript types. Never `any`. Define interfaces for all data structures.
7. For DB tasks: include CREATE TABLE. For query optimization: include EXPLAIN ANALYZE before/after.
8. Distinguish transient (503 + Retry-After) from non-recoverable (500 + generic message) errors.

**Output**: Production-quality code with input validation, error handling, resource cleanup.

### Phase 3: Frontend — Build UI

Switch to frontend mindset. Build the user interface from the API contract.

1. Identify all states: default, loading, error, empty, success.
2. Design component API (props as TypeScript interface with JSDoc). Extract reusable sub-components when patterns repeat.
3. Build skeleton from semantic HTML (form, nav, section, article — not generic divs).
4. Handle loading (spinner/skeleton), error (message + retry), empty (helpful text) states.
5. Ensure keyboard accessibility: Tab order, Enter/Space, Escape to dismiss.
6. Mobile-first responsive: mobile styles default, min-width media queries for desktop.
7. Never `aria-hidden` content that becomes visible via CSS.

**Output**: Accessible, responsive component code with all states handled.

### Phase 4: QA — Test & Validate

Switch to QA mindset. Write tests that catch bugs and prevent regressions.

1. Review the design, API contract, and implementation. Identify: requirements, edge cases, error paths.
2. Write unit tests with descriptive names: `should reject negative age` not `test 1`.
3. Structure: Arrange → Act → Assert. Tests must be independent and deterministic.
4. Cover: happy path, boundary values, invalid inputs, concurrent scenarios.
5. For integration tests: include concrete request/response examples with HTTP methods and status codes.
6. Verify specific error messages, not just "no error thrown".
7. For bug reports: include reproduction steps, environment details, severity, investigation areas.

**Output**: Tests that would catch real regressions, not just confirm the happy path.

## Cross-Phase Rules

- **API contract is law**: The design doc's API contract is the source of truth. Backend implements it exactly; frontend consumes it exactly; QA tests against it.
- **Type consistency**: TypeScript interfaces defined in backend must match what frontend consumes. When backend changes a type, frontend and tests must update accordingly.
- **Error contract**: Error codes and response formats from the design must be consistent across backend implementation, frontend error handling, and QA assertions.
- **Each phase produces artifacts**: Design doc → Backend code → Frontend code → Tests. No phase is skipped.

## Principles

- Ship working software. A feature that passes all 4 phases is production-ready.
- Simplicity over cleverness. Every architectural choice must have a stated reason.
- Accessibility is not optional. It's part of the definition of done.
- Tests are part of the feature, not an afterthought.
