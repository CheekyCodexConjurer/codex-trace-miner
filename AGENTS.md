# Trace Miner Agent Instructions

Keep runtime behavior concise, evidence-backed, and safe. Do not copy leaked system prompts, raw chain-of-thought, or proprietary trace contents into skills, hooks, docs, or MCP outputs.

Extract behaviors only: planning, context routing, requirements ledgers, validation, handoff, final review, and failure detection. Put long research notes in `docs/`, not in this file.

For any meaningful change, update or create `.trace-miner/ledger.json` with requirements, validation, changed scope, and unresolved risks. Do not use git-destructive commands, broad staging, commit, push, reset, stash, merge, or rebase unless the user explicitly asks.

## Routing

| Work type | Route |
| --- | --- |
| Research/source study | `skill-router` -> `trace-researcher` |
| Risky implementation | `skill-router` -> `planning-architect` -> `context-router` -> `requirements-ledger` |
| Simple implementation | `context-router` -> `finalguard-review` |
| Handoff | `implementation-pack` |
| Debugging | `debug-autopsy` -> `finalguard-review` |
| Final answer after changes | `finalguard-review` |

## Codex App Tool Routing

Use CodeGraph first for repo architecture, symbols, callers, impact, and where-is questions. Use Serena for precise Python/code understanding or symbol-aware edits after activating the project. Use Context7 only for current third-party library, framework, SDK, API, CLI, or cloud-service docs. If one of these tools is unavailable, state that briefly and use the smallest bounded fallback.
