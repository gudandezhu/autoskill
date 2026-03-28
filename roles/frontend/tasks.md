# Frontend Tasks

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
