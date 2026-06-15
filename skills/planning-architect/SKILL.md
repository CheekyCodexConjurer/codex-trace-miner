---
name: planning-architect
description: Plan medium or risky Codex implementation work before editing. Use when a task may affect multiple files, trading or financial research correctness, backtests, data pipelines, caches, live execution, persistence, security, or any change that needs requirements, risks, validation gates, and a bounded implementation plan.
---

# Planning Architect

Create the smallest safe plan that can actually be validated.

## Workflow

1. Read repo instructions and task-specific docs first.
2. State the goal, non-goals, assumptions, and risk class.
3. Identify the minimum context needed and hand off to `context-router` if context is unclear.
4. Break work into one bounded implementation slice.
5. Define validation commands and expected evidence before editing.
6. For AERA work, explicitly check data consistency, lookahead risk, cache behavior, simulation/live separation, rollback, and observability.

## Output

```markdown
Goal:
Non-goals:
Assumptions:
Risk:
Context to read:
Implementation slice:
Validation:
Rollback:
Stop conditions:
```
