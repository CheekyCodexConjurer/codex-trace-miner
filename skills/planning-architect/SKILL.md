---
name: planning-architect
description: Risky implementation planning and architecture for multi-file Codex changes before editing. Use when a task touches multiple files, financial research correctness, backtests, data pipelines, caches, live execution, persistence, security, or needs requirements, risks, validation gates, and a bounded implementation plan.
---

# Planning Architect

Create the smallest safe plan that can actually be validated.

## Workflow

1. Read repo instructions and task-specific docs first.
2. State the goal, non-goals, assumptions, and risk class.
3. Identify the minimum context needed and hand off to `context-router` if context is unclear.
4. Break work into one bounded implementation slice.
5. Define acceptance gates, validation commands, and expected evidence before editing.
6. State how final review will compare the diff against the intended behavior.
7. For AERA work, explicitly check data consistency, lookahead risk, cache behavior, simulation/live separation, rollback, and observability.

## Output

```markdown
Goal:
Non-goals:
Assumptions:
Risk:
Context to read:
Implementation slice:
Acceptance gates:
Validation:
Rollback:
Stop conditions:
```
