---
name: context-router
description: Context routing and evidence selection before Codex edits, reviews, research, or plans. Use when a task mentions repo instructions, source traces, docs, backtests, data, hooks, MCP, evals, unfamiliar modules, or when reading too much or too little context would create risk.
---

# Context Router

Route context by evidence need, not curiosity.

## Priority Order

1. User request and repo instructions.
2. Current workspace files that directly define the behavior.
3. CodeGraph first for repo architecture, symbols, callers, impact, or where-is questions.
4. Serena for precise Python/code understanding or symbol-aware edits after project activation.
5. Context7 for current third-party library, framework, SDK, API, CLI, or cloud-service docs.
6. Trace Miner docs for source patterns and eval criteria.
7. Subagents for independent read-only review when risk justifies it.
8. Safe fallback when a preferred tool is unavailable.

## Output

```markdown
Task:
Must read:
Can skip:
Tool route:
Fallback:
Reason:
Risk if wrong:
```

If CodeGraph or Serena is unavailable, say so briefly and use a bounded direct search.
If Context7 is needed, resolve the library ID before querying docs.
