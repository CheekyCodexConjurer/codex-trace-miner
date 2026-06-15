---
name: requirements-ledger
description: Maintain a compact requirements, validation, changed-files, and risk ledger for non-trivial Codex work. Use when a task has multiple requirements, unresolved risks, test obligations, handoffs, backtest/data/live-trading safety concerns, or when a stop guard needs durable evidence before final answer.
---

# Requirements Ledger

Use `.trace-miner/ledger.json` as durable task state when chat memory is not enough.

## Required Fields

```json
{
  "requirements": [{"id": "REQ-1", "text": "", "status": "open|done|deferred", "evidence": ""}],
  "validation": [{"command": "", "status": "pass|fail|skipped_with_reason|blocked_with_reason", "evidence": ""}],
  "changed_scope": [{"path": "", "reason": ""}],
  "risks": [{"id": "R-1", "description": "", "status": "open|resolved|accepted|not_applicable|deferred_with_reason", "owner": ""}],
  "next_action": ""
}
```

## Workflow

1. Add every user requirement as a ledger row.
2. Keep risk rows explicit; for AERA include bias, data, cache, sim/live, recovery, and rollback risks when relevant.
3. Record validation commands or exact blockers.
4. Close requirements only with evidence.
5. Before final answer, ensure no open risks remain unless accepted or deferred with a concrete reason.
