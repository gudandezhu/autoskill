# Architect Tasks

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
