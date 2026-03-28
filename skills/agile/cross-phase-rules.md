# Cross-Phase Rules

These rules govern how the 4 phases interact with each other.

## API Contract Is Law

The design doc's API contract is the source of truth. Backend implements it exactly; frontend consumes it exactly; QA tests against it.

## Type Consistency

TypeScript interfaces defined in backend must match what frontend consumes. When backend changes a type, frontend and tests must update accordingly.

## Error Contract

Error codes and response formats from the design must be consistent across backend implementation, frontend error handling, and QA assertions.

## Artifact Chain

Each phase produces artifacts that feed into the next:

```
Design Doc → Backend Code → Frontend Code → Tests
```

No phase is skipped. Each artifact is validated against the previous phase's output.
