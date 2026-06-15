---
name: context-router
description: Choose the smallest useful context set before Codex edits, reviews, or plans. Use when a task mentions repo instructions, source traces, docs, backtests, data, hooks, MCP, evals, unfamiliar modules, or when reading too much or too little context would create risk.
---

# Context Router

Route context by evidence need, not curiosity.

## Priority Order

1. User request and repo instructions.
2. Current workspace files that directly define the behavior.
3. CodeGraph or Serena when available for code mapping.
4. Primary docs for current third-party APIs.
5. Trace Miner docs for source patterns and eval criteria.
6. Subagents for independent read-only review when risk justifies it.

## Output

```markdown
Task:
Must read:
Can skip:
Tool route:
Reason:
Risk if wrong:
```

If CodeGraph or Serena is unavailable, say so briefly and use a bounded direct search.
