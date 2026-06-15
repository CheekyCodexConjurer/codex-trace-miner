---
name: finalguard-review
description: Run a final safety review before Codex claims completion. Use after implementation, docs changes, hooks, MCP changes, eval updates, backtest/research changes, or any task where requirements, changed files, tests, unresolved risks, or rollback need one last check.
---

# Finalguard Review

Do not approve work just because the diff exists. Check evidence.

## Checklist

1. Requirements: every requested item is done, deferred with reason, or explicitly out of scope.
2. Files: changed files match the intended scope.
3. Validation: tests, lint, smoke checks, or justified blockers are recorded.
4. Risks: no open risk remains hidden.
5. AERA: bias, data consistency, cache, backtest assumptions, sim/live separation, rollback, and recovery were considered when relevant.
6. Final answer: includes what changed, validation, residual risk, and next action.

## Output

```markdown
Decision: PASS | PASS_WITH_NOTES | FAIL_FIX_REQUIRED
Findings:
Validation evidence:
Residual risk:
Required next action:
```
