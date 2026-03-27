# Task Suite

This file defines the fixed task suite for evaluating each skill role.
Do NOT modify this file during training. It serves the same purpose as
`prepare.py` in autoresearch -- a fixed evaluation harness.

Each task defines a scenario, requirements, and expected output format.
Tasks are designed to test different dimensions of a skill's capability.

---

## Architect Tasks

### architect-001: API Design for URL Shortener

**Context**: A SaaS product team needs a URL shortener service as part of their
analytics platform. The service must handle 10K shortens/minute and support
custom aliases for enterprise clients.

**Requirements**:
- RESTful API design with all endpoint definitions (method, path, request/response)
- Error handling strategy with specific status codes
- Rate limiting approach (different tiers: free, pro, enterprise)
- Database schema outline (tables, key relationships, indexes)
- Caching strategy for redirect lookups

**Output**: A design document in markdown with clear sections.

### architect-002: System Design for Real-time Notifications

**Context**: A fintech application needs to push real-time notifications to
users across web and mobile: price alerts, transaction confirmations, security
alerts. Requirements: < 500ms delivery latency, 100K concurrent connections,
guaranteed delivery for security alerts.

**Requirements**:
- Component architecture (ASCII diagram)
- Message flow for each notification type
- Technology choices with justification
- Failure handling and retry strategy
- Scalability plan from 10K to 1M users

**Output**: Architecture document with diagram, data flow, and trade-off analysis.

### architect-003: Refactoring Plan for Monolith to Microservices

**Context**: A 3-year-old e-commerce monolith (Node.js) has these modules:
catalog, cart, checkout, payments, users, notifications, admin. The checkout
module is the bottleneck during sales events. The team wants to extract
payments and checkout into separate services.

**Requirements**:
- Service boundary definition with rationale
- Data ownership and migration strategy
- Inter-service communication protocol
- Deployment strategy (zero-downtime migration)
- Rollback plan if something goes wrong
- Risk assessment with mitigations

**Output**: Step-by-step refactoring plan with timeline and risk matrix.

---

## Backend Tasks

### backend-001: REST API Endpoint - User Registration

**Context**: Implement a user registration endpoint for a SaaS application.

**Specification**:
```
POST /api/users
Content-Type: application/json

Request Body:
{
  "name": "string (2-100 chars, required)",
  "email": "string (valid email, required, unique)",
  "password": "string (8+ chars, at least 1 uppercase, 1 lowercase, 1 digit)"
}

Success Response (201):
{
  "id": "uuid",
  "name": "...",
  "email": "...",
  "created_at": "ISO8601"
}

Validation Error (400):
{
  "errors": [
    { "field": "name", "message": "Name must be between 2 and 100 characters" },
    { "field": "email", "message": "Invalid email format" }
  ]
}

Conflict (409):
{
  "error": "Email already registered"
}
```

**Additional requirements**:
- Hash password with bcrypt before storing
- Handle database connection errors (return 503 with retry-after header)
- Validate all inputs before any database operation
- Use parameterized queries (no SQL injection)

**Output**: Implementation code in a language of your choice (TypeScript/Node.js preferred).

### backend-002: Database Query Optimization

**Context**: An order management system has a slow query:
```sql
SELECT o.id, o.user_id, o.status, o.total, o.created_at,
       u.name, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status IN ('pending', 'processing')
  AND o.created_at > '2025-01-01'
ORDER BY o.created_at DESC
LIMIT 50 OFFSET ?;
```
The orders table has 15M rows. The query takes 4.2 seconds. EXPLAIN shows
a full table scan on orders.

**Requirements**:
- Analyze why the query is slow
- Propose index strategy with CREATE INDEX statements
- Rewrite the query if needed
- Show expected EXPLAIN output before and after
- Consider: what if OFFSET becomes very large (deep pagination)?

**Output**: SQL statements with explanations. Include EXPLAIN analysis.

### backend-003: Job Queue Worker with Retry Logic

**Context**: An email service needs a background job queue. Jobs can fail due to
temporary issues (SMTP timeout, rate limiting) or permanent issues (invalid email).

**Specification**:
```
Job {
  id: uuid
  type: "email" | "webhook" | "report"
  payload: json
  status: "pending" | "processing" | "completed" | "failed"
  attempts: int (max 3 for temporary, 0 for permanent)
  next_retry_at: timestamp
  error: string (last error message)
}
```

**Requirements**:
- Pick up pending jobs (FIFO, respect next_retry_at)
- Process with exponential backoff: 1min, 5min, 15min for retries
- Classify errors as temporary (retry) or permanent (fail immediately)
- Job timeout: 30 seconds, then mark as failed and retry
- Concurrency limit: 5 parallel workers
- Dead letter queue: jobs that failed 3 times go to a DLQ table

**Output**: Worker implementation with clear error handling and retry logic.

---

## Frontend Tasks

### frontend-001: Search Component with Debounce

**Context**: Build a product search component for an e-commerce site.

**Requirements**:
- Text input with debounced search (300ms after last keystroke)
- Loading spinner during search (no full-page loader)
- Results list showing product name, price, thumbnail placeholder
- Empty state: "No products found for 'query'"
- Error state: "Something went wrong. Please try again."
- Result count: "Showing 5 of 23 results"
- Keyboard accessible: Escape clears input, Arrow keys navigate results
- Minimum query length: 2 characters (show hint below 2)
- Click outside or Escape closes results dropdown

**Output**: Component code with markup, styles, and state management.
Framework-agnostic or React/Vue preferred.

### frontend-002: Registration Form with Validation

**Context**: Build a user registration form for a web application.

**Fields**:
- Full Name (text, required, 2-100 chars)
- Email (email, required, valid format)
- Password (password, required, 8+ chars)
- Confirm Password (password, must match)
- Terms checkbox (required)

**Requirements**:
- Inline validation errors appear on blur (not on every keystroke)
- Password strength indicator (weak/medium/strong) with color
- Submit button disabled until all fields valid
- Error messages specific to each field (not generic)
- Accessible: labels, error announcements via aria-live
- Loading state on submit button (spinner + "Creating account...")
- Success state: show confirmation message

**Output**: Component code with validation logic and accessibility features.

### frontend-003: Data Table with Sort and Pagination

**Context**: Build a data table for an admin dashboard.

**Data**: List of users with columns: Name, Email, Role (admin/editor/viewer),
Status (active/inactive/suspended), Last Login, Actions.

**Requirements**:
- Column headers clickable to sort (asc/desc, show arrow indicator)
- Client-side pagination: configurable page size (10/25/50)
- Show "Showing 1-10 of 156 users"
- Row actions: Edit (navigates), Delete (shows confirmation dialog)
- Status column: colored badges (green/yellow/red)
- Responsive: on mobile, show card view instead of table
- Select rows with checkboxes (bulk actions toolbar appears)
- Filter by status (dropdown above table)

**Output**: Component code. Handle all states (loading, empty, error).

---

## QA Tasks

### qa-001: Unit Tests for Input Validator

**Context**: Write comprehensive unit tests for this validation function:

```typescript
interface CreateUserInput {
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'editor' | 'viewer';
}

function validateUser(input: CreateUserInput): string[]
// Returns array of error messages. Empty array = valid.
// Rules:
//   - name: required, 2-100 characters
//   - email: required, valid email format
//   - age: required, 18-120
//   - role: required, one of 'admin' | 'editor' | 'viewer'
```

**Requirements**:
- Test each validation rule independently
- Test boundary values (age=18, age=120, name=2chars, name=100chars)
- Test multiple violations simultaneously
- Test edge cases: null, undefined, empty string, wrong types
- Test each specific error message is returned correctly
- Test valid input returns empty array

**Output**: Test file with descriptive test names following the pattern
"should [expected behavior] when [condition]".

### qa-002: Integration Test Plan for Shopping Cart API

**Context**: An e-commerce platform has these cart API endpoints:
- POST /api/cart/items (add item)
- PUT /api/cart/items/:id (update quantity)
- DELETE /api/cart/items/:id (remove item)
- POST /api/cart/apply-discount (apply discount code)
- GET /api/cart (get cart with calculated total)
- POST /api/cart/checkout (place order)

**Requirements**:
For each endpoint, specify:
- Request format (method, path, headers, body)
- Expected success response (status + body)
- Error scenarios with expected responses
- Edge cases to test
- Dependencies on other endpoints (test order matters)

**Specific scenarios to cover**:
- Add item when cart is empty
- Add duplicate item (should merge/increment)
- Update quantity to 0 (should remove item)
- Apply expired discount code
- Apply discount code that exceeds cart total
- Checkout with empty cart
- Concurrent modifications (two users updating same cart)
- Cart persistence across sessions

**Output**: Test plan document with clear test cases, not just test code.

### qa-003: Bug Report Improvement and Triage

**Context**: A junior developer submitted this bug report:

```
The login page doesn't work on mobile. It shows an error when I try
to log in. Please fix ASAP. This is blocking our mobile users.
```

**Requirements**:
1. Improve this bug report to be actionable:
   - Reproduction steps (specific and reproducible)
   - Expected vs actual behavior
   - Environment details (device, OS, browser, app version)
   - Screenshots/logs if applicable
   - Severity and priority assessment with justification

2. Write triage notes:
   - Initial investigation steps
   - Possible root causes (rank by likelihood)
   - Questions to ask the reporter
   - Suggested assignee and timeline

3. Define a bug report template for the team based on this analysis.

**Output**: Improved bug report, triage notes, and a reusable bug report template.
