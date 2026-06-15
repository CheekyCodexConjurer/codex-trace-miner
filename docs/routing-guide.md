# Routing Guide

Use `skill-router` first when the task is ambiguous or could involve multiple Trace Miner skills.

| User intent | Route | Stop condition |
| --- | --- | --- |
| Research/source study | `skill-router` -> `trace-researcher` | Source license/provenance is unclear or raw trace content would be needed. |
| Multi-agent Fusion | `skill-router` -> `fusion-orchestrator` -> selected mode -> `finalguard-review` | Fusion would add ceremony without reducing risk, or write ownership is unclear. |
| Risky implementation | `skill-router` -> `planning-architect` -> `context-router` -> `requirements-ledger` | Requirements, risks, or validation cannot be stated. |
| Simple implementation | `context-router` -> `finalguard-review` | Context is unknown or final validation is missing. |
| Handoff | `implementation-pack` | Owned scope or validation command is unclear. |
| Debugging | `debug-autopsy` -> `finalguard-review` | Failure cannot be reproduced or root cause is unknown. |
| Final answer after changes | `finalguard-review` | Open requirements, missing validation, or unresolved risks remain. |

## Tool Route

| Evidence need | Tool route | Fallback |
| --- | --- | --- |
| Repo map, symbols, callers, impact | CodeGraph | Bounded `rg` and targeted reads |
| Precise Python/code understanding or symbol-aware edit prep | Serena | CodeGraph context, then targeted direct edit |
| Current third-party docs | Context7 | Official docs or bounded web search |
| Trace Miner docs, patterns, scorecard | Fable Mode MCP | Local docs and `patterns/patterns.jsonl` |

Keep this guide out of runtime unless the router needs clarification.
