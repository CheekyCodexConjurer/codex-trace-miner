---
name: implementation-pack
description: Implementation handoff packaging for one bounded write-capable Codex work slice. Use when work should be delegated, sliced, reviewed, or executed with clear owned files, constraints, validation commands, rollback notes, reviewer focus, and stop conditions.
---

# Implementation Pack

Create one clear package for one implementation slice.

## Workflow

1. Start from the requirements ledger or planning output.
2. Assign one write scope and avoid overlapping ownership.
3. Include exact files or directories to inspect, but do not force broad reading.
4. List included context, omitted context, limits, and the question the implementer or reviewer must answer.
5. Include constraints, acceptance gates, validation commands, and expected evidence.
6. Define stop conditions for ambiguity, failing validation, or risk expansion.

## Output

```markdown
Objective:
Owned scope:
Context:
Omitted context:
Limits:
Do not touch:
Implementation steps:
Acceptance gates:
Validation:
Rollback:
Stop and ask if:
Reviewer focus:
```
