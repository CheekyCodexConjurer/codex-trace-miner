---
name: debug-autopsy
description: Diagnose failures and turn them into reusable prevention patterns. Use after a failed test, broken hook, bad implementation, missed requirement, flaky validation, backtest anomaly, cache inconsistency, live/simulation confusion, or any repeated Codex failure that should produce a durable lesson.
---

# Debug Autopsy

Find the failure mechanism before proposing fixes.

## Workflow

1. Reproduce or cite the exact failure evidence.
2. Identify expected behavior, actual behavior, and first bad assumption.
3. Trace source to sink with the smallest useful context.
4. Fix only after the cause is understood.
5. Add or update a regression test, guard, or ledger rule.
6. Record the prevention pattern without blaming the model or user.

## Output

```markdown
Failure:
Expected:
Actual:
Root cause:
Fix:
Regression check:
Prevention pattern:
Remaining risk:
```
