---
name: trace-miner
description: Trace mining, behavior extraction, and eval updates for public Fable 5 trace sources and related agent projects. Use when Codex must convert source links, research notes, or extracted patterns into concise Trace Miner skills, docs, hooks, MCP context, or eval criteria without copying leaked prompts or raw chain-of-thought.
---

# Trace Miner

Use this skill to turn public trace evidence into operational Codex behavior.

## Workflow

1. Confirm the source is public and record its URL, license if visible, and date checked.
2. Use metadata, schema, README evidence, and aggregate-only scans; do not copy, print, store, or depend on raw trace rows or row payloads.
3. Extract behavior patterns only: planning, evidence gathering, tool discipline, validation, review, handoff, and recovery.
4. Do not copy leaked prompts, hidden instructions, raw chain-of-thought, secrets, or proprietary code.
5. Put long notes in docs, not runtime skills.
6. Classify each accepted pattern, state confidence, and choose a destination: skill rule, hook rule, MCP context, eval check, or docs only.
7. Promote only high-confidence, measurable behavior improvements to runtime.
8. Reject patterns that only optimize model imitation, personality, or training data reuse.
9. Convert useful patterns into a skill, hook, ledger field, MCP context, or eval criterion.
10. Validate the change with the before/after scorecard when behavior changes.

## Output

```markdown
Source:
Pattern:
Evidence type:
Classification:
Destination:
Confidence:
Runtime change:
Eval criterion:
Risk or exclusion:
```
