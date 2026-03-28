# QA Tasks

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
