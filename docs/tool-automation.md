# Tool Automation

Checked on: 2026-06-15.

Trace Miner routes Codex App tools by evidence need. These tools are optional accelerators, not hard dependencies; if a tool is unavailable, say so briefly and use the smallest safe fallback.

## Automatic Route

| Need | Preferred route | Fallback |
| --- | --- | --- |
| Repo architecture, symbols, callers, impact, or where-is questions | CodeGraph first | Bounded `rg` and targeted file reads |
| Precise Python/code understanding or symbol-aware edits | Serena after reading its initial instructions and activating this project | CodeGraph context, then targeted direct edits |
| Current third-party library, framework, SDK, API, CLI, or cloud-service docs | Context7: resolve library ID, then query docs | Official primary docs or bounded web search |
| Trace Miner source/pattern/eval context | Fable Mode MCP read-only tools | Local docs and `patterns/patterns.jsonl` |

## Repo Setup

- CodeGraph is initialized locally with `codegraph init` and indexed with `codegraph index`.
- `.codegraph/` is ignored because it is a local index, not source.
- `.serena/` is ignored because Serena project state is local.
- Context7 needs no repo files; it is selected by `context-router` when current third-party docs are relevant.

## Runtime Rule

Use `context-router` to name the chosen tool route and fallback before risky edits. Do not block ordinary work just because one optional tool is unavailable.
