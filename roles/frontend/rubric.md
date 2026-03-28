# Frontend Rubric

### Checklist (10 items, 5 points each = 50 points)

For each item, award 5 points if clearly present, 0 if missing or inadequate.

- [ ] **Loading state**: Component shows loading indicator during async operations (not blank screen)
- [ ] **Error state**: Component displays error message with recovery action when operations fail
- [ ] **Empty state**: Component handles the case where there is no data to display
- [ ] **Semantic HTML**: Uses semantic elements (button, nav, form, label) not generic divs
- [ ] **Accessible labels**: Interactive elements have associated labels, aria-labels, or aria-describedby
- [ ] **Keyboard navigable**: Interactive elements are reachable and operable via keyboard (tab, enter, escape)
- [ ] **No layout shift**: State changes (loading → content, empty → results) don't cause jarring layout shifts
- [ ] **Responsive**: Design adapts to different screen sizes (or responsive behavior is considered)
- [ ] **Configurable**: Values that should be configurable (page size, debounce time) are not hardcoded
- [ ] **Clean event handling**: Event listeners are properly managed (no memory leaks, proper cleanup)

### Quality Dimensions (5 dimensions, scored 1-5, sum * 2 = 10-50 points)

1. **UX completeness** (1=missing specified interactions, 3=most work, 5=all specified interactions implemented)
2. **Accessibility** (1=not accessible, 3=basic a11y, 5=screen reader friendly, keyboard only usable)
3. **Component design** (1=monolithic, 3=decent separation, 5=reusable, well-encapsulated, clean API)
4. **State management** (1=spaghetti state, 3=works, 5=clean, predictable, no race conditions)
5. **Polish** (1=raw/functional, 3=decent, 5=feels production-quality with attention to detail)
