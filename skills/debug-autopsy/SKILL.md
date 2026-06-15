---
name: debug-autopsy
description: Debug autopsy and regression prevention for failed tests, broken hooks, missed requirements, and unexpected behavior. Use after a failure, bad implementation, flaky validation, backtest anomaly, cache inconsistency, live/simulation confusion, or repeated Codex failure that should produce a durable lesson.
---

# Debug Autopsy

Find the failure mechanism before proposing fixes.

## Workflow

1. Reproduce or cite the exact failure evidence.
2. Identify expected behavior, actual behavior, and first bad assumption.
3. Trace source to sink with the smallest useful context.
4. If a preferred tool failed or is unavailable, name the safe fallback and retry boundary.
5. Fix only after the cause is understood.
6. Add or update a regression test, guard, or ledger rule.
7. Record the prevention pattern without blaming the model or user.

## Output

```markdown
Failure:
Expected:
Actual:
Root cause:
Fallback:
Fix:
Regression check:
Prevention pattern:
Remaining risk:
```
