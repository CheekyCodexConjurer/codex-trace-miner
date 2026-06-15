---
name: finalguard-review
description: Final guard review before Codex final answers, commits, or handoffs after changed work. Use after implementation, docs changes, hooks, MCP changes, eval updates, backtest/research changes, or any task where requirements, changed files, tests, unresolved risks, rollback, or next action need one last check.
---

# Finalguard Review

Do not approve work just because the diff exists. Check evidence.

## Checklist

1. Requirements: every requested item is done, deferred with reason, or explicitly out of scope.
2. Files: changed files match the intended scope.
3. Intent: the diff matches the acceptance gates, not just the agent's claims.
4. Validation: tests, lint, smoke checks, or justified blockers are recorded.
5. Risks: no open risk remains hidden.
6. Source hygiene: source-derived work contains no raw trace rows, leaked prompts, chain-of-thought, secrets, or training instructions.
7. AERA: bias, data consistency, cache, backtest assumptions, sim/live separation, rollback, and recovery were considered when relevant.
8. Final answer: includes what changed, validation, residual risk, and next action.

## Output

```markdown
Decision: PASS | PASS_WITH_NOTES | FAIL_FIX_REQUIRED
Findings:
Validation evidence:
Residual risk:
Required next action:
```
