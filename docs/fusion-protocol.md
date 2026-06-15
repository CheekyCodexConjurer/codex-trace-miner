# Trace Fusion Protocol

Trace Fusion is a local Codex-only workflow for coordinating multiple GPT-5.5 Codex agents with different roles. It is agentic fusion, not model-level fusion.

## Boundaries

- No OpenRouter.
- No external model API.
- No hosting requirement.
- No fine-tuning.
- No copied Fable prompts.
- No raw trace rows.
- No copied chain-of-thought.

Use only Codex App capabilities: skills, project-scoped custom agents, read-only local MCP, hooks, docs, evals, and parent synthesis.

## Roles

| Role | Default access | Purpose |
| --- | --- | --- |
| `trace-architect` | read-only | mode selection, risks, acceptance gates, validation plan |
| `trace-context-scout` | read-only | independent context routing and evidence gathering |
| `trace-implementer` | write-explicit-only | one bounded implementation scope when explicitly assigned |
| `trace-reviewer` | read-only | independent review before final synthesis |

## Protocol

1. Parent chooses a fusion mode with `fusion-orchestrator`.
2. Architect defines risk, scope, acceptance gates, and validation.
3. Context scout gathers independent evidence and names skipped context.
4. Parent synthesizes disagreements before any write.
5. One write owner implements: either parent or one explicitly assigned `trace-implementer`.
6. Reviewer checks requirements, changed scope, evidence, validation, and unresolved risk.
7. Parent runs `finalguard-review` and reports residual risk.

## Consensus Rule

Consensus requires evidence. Agreement without inspected sources, validation, or explicit uncertainty is not consensus.

## Stop Conditions

- More than one agent would edit overlapping files.
- The mode would add ceremony without reducing risk.
- Required validation is unknown.
- Source evidence depends on raw trace rows, prompts, chain-of-thought, secrets, or proprietary content.
- The task would require OpenRouter, external model APIs, hosting, or fine-tuning.
