# Explorer Tasks

### explorer-001: Product Exploration for Fitness App

**Context**: A solo developer wants to build a fitness tracking app. Their idea: "An app that
uses AI to create personalized workout plans." They have no clear target audience defined,
no competitor analysis, and a budget of $5K. They have 6 months before they need to launch
or find a job.

**Requirements**:
- Clarify the core problem: who specifically has this problem and why existing solutions
  (Fitbit, Nike Training, Strong) don't solve it for them
- Identify 2-3 concrete approaches with trade-offs (e.g., AI-first vs template-based,
  niche audience vs broad)
- Define an MVP scope with explicit in/out items
- Assess technical feasibility and risks
- Provide prioritized next steps

**Output**: A markdown document following Product mode format, covering Problem, Solution,
Key Decisions, MVP Scope, Risks & Mitigations, and Next Steps.

### explorer-002: Market Analysis for Developer Tool

**Context**: A startup built a CLI tool that automatically generates API documentation from
code comments. After 3 months: 200 GitHub stars, 12 paying customers ($29/mo each), 5%
monthly churn. The founder says "developers love it but don't pay." They're considering
pivoting to an enterprise plan ($499/mo) with SSO and audit logs.

**Requirements**:
- Diagnose why self-serve isn't converting — analyze the pricing, value prop, and
  competitive landscape
- Evaluate the enterprise pivot: what evidence supports or contradicts this move?
- Identify at least 3 real competitors (named, with URLs if possible) and how this tool
  differentiates
- Assess the 5% monthly churn rate: is this normal for dev tools? What's the likely cause?
- Recommend: pivot, persevere, or something else — with specific reasoning

**Output**: A markdown document following Market mode format, covering Summary, Market
Landscape, Competitive Dynamics, Opportunities & Gaps, Risks, and Recommendations.

### explorer-003: Learning Exploration for Event-Driven Architecture

**Context**: A backend developer with 3 years of REST API experience wants to understand
event-driven architecture (EDA). They know Kafka exists but don't understand when to use it
vs a message queue vs a webhook. Their team is considering EDA for their order processing
system (currently REST-based, ~500 orders/day, occasional duplicate processing issues).

**Requirements**:
- Build a mental model for EDA: what problem does it solve that REST doesn't?
- Explain the key patterns (event sourcing, CQRS, saga) with concrete examples tied to
  the order processing context
- Compare: message queue (RabbitMQ) vs event stream (Kafka) vs simple webhooks — when
  to use each, with trade-offs
- Address the duplicate processing issue: how would EDA help or not help?
- Identify common pitfalls for teams transitioning from REST to EDA
- Provide a learning path with specific resources and exercises

**Output**: A markdown document following Learn mode format, covering Core Concepts, Mental
Models, Common Pitfalls, How It Works, Practical Examples, and Further Learning.
