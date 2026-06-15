---
name: fusion-orchestrator
description: Trace Fusion orchestration and adaptive Codex subagent routing for multi-agent planning, context scouting, one-owner implementation, independent review, and parent synthesis. Use when a task benefits from Codex-only agentic fusion without OpenRouter, external model APIs, hosting, fine-tuning, raw traces, leaked prompts, or chain-of-thought.
---

# Fusion Orchestrator

Coordinate Codex subagents by role, not by external models.

## Mode Gate

| Mode | Use when | Agents |
| --- | --- | --- |
| none | trivial or low-risk work | parent + `context-router` + `finalguard-review` |
| mini | medium-risk planning or review | `trace-architect`, `trace-reviewer` |
| full | complex or multi-file work | architect, context scout, one implementer, reviewer |
| critical | safety, financial, security, migration, or irreversible risk | full + `requirements-ledger` + strict validation |

## Rules

1. Use only Codex App capabilities: skills, local custom agents, hooks, read-only MCP, docs, and evals.
2. Do not use OpenRouter, external model APIs, hosting, fine-tuning, Fable prompts, raw trace rows, or chain-of-thought.
3. Keep one write owner. Subagents are read-only unless the parent explicitly assigns `trace-implementer` one bounded write scope.
4. Require independent evidence before consensus.
5. Parent synthesizes disagreements, acceptance gates, validation evidence, and residual risk.

## Workflow

1. Choose mode by risk and expected value.
2. Assign roles with bounded context and stop conditions.
3. Collect independent findings before implementation.
4. Give one implementer one owned scope, or keep implementation in the parent.
5. Run reviewer after changes.
6. Finish with `finalguard-review`.

## Output

```markdown
Mode:
Reason:
Agents:
Write owner:
Evidence required:
Consensus:
Validation:
Residual risk:
Next action:
```
