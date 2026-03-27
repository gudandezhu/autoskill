# Task Suite v2 — Harder Variants

Extended task suite for testing skill generalization beyond the original tasks.
Used when all original tasks score above 95, indicating convergence on the base set.

Each task deliberately adds complexity that the original tasks don't cover:
- Cross-cutting concerns (multi-tenant, multi-region, real-time)
- Larger system scope (multiple services, complex data flows)
- Ambiguous requirements that need clarification
- Security and compliance requirements

---

## Architect Tasks (v2)

### architect-004: Distributed Task Scheduler

**Context**: A data platform team needs to replace cron jobs with a distributed task
scheduler (similar to Apache Airflow). The system must support DAG-based workflows,
dynamic task generation, and handle millions of scheduled tasks per day across
multiple teams.

**Requirements**:
- DAG-based workflow definition (tasks with dependencies, no cycles)
- Dynamic task generation (tasks created at runtime based on data)
- Multi-tenant isolation (teams can only see/modify their own workflows)
- Retry with exponential backoff per task, with configurable max retries
- Dead letter queue for permanently failed tasks
- Workflow versioning and rollback
- Audit logging (who ran what, when, with what parameters)
- SLA monitoring: alert if a workflow exceeds its expected duration

**Output**: Architecture document with component diagram, data model, API surface,
and deployment strategy. Include CREATE TABLE for all entities.

### architect-005: Real-time Collaborative Editor

**Context**: A SaaS startup is building a real-time collaborative document editor
(like Google Docs). The system must support 100+ concurrent editors per document
with sub-100ms latency for character-level changes.

**Requirements**:
- Conflict resolution strategy (OT vs CRDT) with trade-off analysis
- Document persistence model (save strategy, version history)
- Real-time sync protocol design (WebSocket, binary protocol, compression)
- Cursor and selection presence (show other users' cursors)
- Offline support with conflict resolution on reconnect
- Permission model (viewer, commenter, editor, owner) with inheritance
- Encryption at rest for document content
- Scalability: from 10K to 1M documents, 1K to 100K concurrent users

**Output**: Architecture document with protocol design, data model, and comparison
of OT vs CRDT approaches with clear recommendation.

---

## Backend Tasks (v2)

### backend-004: WebSocket Real-time Notification Hub

**Context**: A fintech app needs a WebSocket-based notification delivery system.
Clients subscribe to channels (user-specific, team-wide, global). Messages must
be delivered in order within a channel, with guaranteed delivery for critical alerts.

**Specification**:
```
Message {
  id: uuid
  channel: string (e.g. "user:123", "team:456", "global:alerts")
  type: "info" | "warning" | "critical" | "system"
  payload: json
  priority: "low" | "normal" | "high"
  created_at: timestamp
  delivered_at: timestamp | null
  acked_at: timestamp | null
}

Subscription {
  id: uuid
  client_id: string
  channels: string[]
  connected_at: timestamp
  last_ping: timestamp
}
```

**Requirements**:
- WebSocket connection management with heartbeat (30s interval)
- Channel subscription/unsubscription at runtime
- Ordered delivery within a channel (preserve message sequence)
- Guaranteed delivery for "critical" messages (persist and retry)
- Backpressure: if client is slow, buffer up to 1000 messages then disconnect
- Authentication via JWT token on connection upgrade
- Rate limiting: max 100 messages/second per client
- Graceful disconnect: send pending buffered messages before closing

**Output**: Implementation with WebSocket handler, subscription manager, and message
router. Include CREATE TABLE statements.

---

## Frontend Tasks (v2)

### frontend-004: Infinite Scroll Image Gallery

**Context**: Build an image gallery component for a photography portfolio site.
Must handle thousands of images with smooth scrolling performance.

**Requirements**:
- Infinite scroll with intersection observer (load 20 images at a time)
- Virtual scrolling: only render visible images + buffer (5 above, 10 below)
- Masonry layout (images of varying heights, 3 columns on desktop, 2 on mobile)
- Image lazy loading with blur-up placeholder (small blurred preview → full image)
- Lightbox view: click to open full-size image with navigation (prev/next, keyboard arrows)
- Filter by tags (multi-select, show active filter count)
- Sort by date, popularity, or name
- Upload progress indicator for drag-and-drop uploads (progress bar + cancel button)
- Keyboard: Escape closes lightbox, Arrow keys navigate, Enter opens lightbox

**Output**: Component code with virtual scrolling implementation and all states.

### frontend-005: Real-time Collaborative Todo List

**Context**: Build a collaborative todo list where multiple users can add, edit,
reorder, and assign tasks in real-time. Changes from other users appear instantly.

**Requirements**:
- Task CRUD (add, edit, delete) with optimistic updates
- Drag-and-drop reordering within and between sections
- Real-time sync: changes from other users appear with subtle highlight animation
- Conflict indication: if two users edit the same task, show "edited by X" badge
- User presence: show avatars of users currently viewing the list
- Task assignment: assign to team members with @mention autocomplete
- Sections: custom sections (not just todo/done), collapsible
- Offline mode: queue changes, sync on reconnect with conflict resolution
- Keyboard: Enter to add, Delete to remove, Tab to indent (subtask), Shift+Tab to outdent

**Output**: Component code with real-time sync layer and offline support.

---

## QA Tasks (v2)

### qa-004: Integration Tests for WebSocket Notification API

**Context**: The WebSocket notification hub (see backend-004) has these operations:
- Connect with JWT authentication
- Subscribe to channels
- Receive messages
- Send acknowledgment
- Disconnect gracefully

**Requirements**:
For each operation, specify:
- Test setup (preconditions, mock data)
- Concrete WebSocket message frames (JSON format)
- Expected server response or behavior
- Edge cases (disconnect during subscribe, message during reconnect)
- Error scenarios with expected responses

**Specific scenarios to cover**:
- Connection with expired JWT (expect 4001 close code)
- Subscribe to channel without permission (expect error message)
- Receive messages in correct order within a channel
- Guaranteed delivery: critical message arrives even if client disconnects and reconnects
- Backpressure: client receives disconnect after 1001 buffered messages
- Multiple clients subscribing to same channel (broadcast behavior)
- Heartbeat timeout (server closes connection after 90s without ping)
- Concurrent subscribe and message delivery (race condition test)

**Output**: Test plan with concrete WebSocket message examples, not just descriptions.

### qa-005: Performance Test Plan for Image Gallery

**Context**: The image gallery (see frontend-004) must maintain 60fps scrolling
with 10,000 images loaded. Create a performance test plan.

**Requirements**:
- Define performance budgets (FPS, memory usage, initial load time, scroll latency)
- Test scenarios: initial render, scroll speed, filter switching, lightbox open
- Measurement approach: what metrics to capture and how (RAIL, Custom Performance API)
- Device/browser matrix: test on low-end mobile, mid-range desktop, high-end desktop
- Regression detection: how to compare across builds
- Load testing: simulate 100 concurrent users viewing different galleries
- Memory leak detection: repeated filter/sort cycles should not grow memory
- Accessibility performance: screen reader announcement latency during infinite scroll

**Output**: Performance test plan document with specific metrics, thresholds, and tools.
