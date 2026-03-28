# Backend Tasks

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
