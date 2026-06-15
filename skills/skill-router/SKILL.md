---
name: skill-router
description: Skill routing and Trace Miner task classification for research, planning, implementation, debugging, handoff, and final review. Use when Codex must decide which Trace Miner skills to apply before doing source study, repo inspection, multi-step work, risky implementation, debugging, or final answer validation.
---

# Skill Router

Classify the task, then choose the smallest useful skill route.

## Routes

| Task type | Route |
| --- | --- |
| Research or source study | `trace-researcher` |
| Risky or multi-file implementation | `planning-architect` -> `context-router` -> `requirements-ledger` |
| Simple non-significant implementation | `context-router` -> `finalguard-review` |
| Multi-agent Fusion | `fusion-orchestrator` -> selected mode -> `finalguard-review` |
| Handoff or execution plan | `implementation-pack` |
| Failure, regression, or broken validation | `debug-autopsy` -> `finalguard-review` |
| Final answer after changes | `finalguard-review` |

## Workflow

1. Classify task type and risk.
2. Select only the skills needed for that task.
3. Put broad source study through `trace-researcher`; put source-derived behavior changes through `trace-miner` and `finalguard-review`.
4. Keep medium/low-confidence source findings in docs/evals; route only high-confidence behavior changes into runtime skills or hooks.
5. Add `requirements-ledger` when repo instructions require it, or when work has meaningful changes, multiple requirements, validation obligations, delegation, multi-session state, or unresolved risk.
6. Use `fusion-orchestrator` only when Codex subagents reduce real risk; use none, mini, full, or critical mode.
7. Use `context-router` when the task depends on repo files, source evidence, CodeGraph, Serena, Context7, MCP, or safe fallbacks.
8. End changed-work sessions with `finalguard-review`.

## Output

```markdown
Task type:
Risk:
Selected skills:
Skipped skills:
Reason:
Next action:
```
