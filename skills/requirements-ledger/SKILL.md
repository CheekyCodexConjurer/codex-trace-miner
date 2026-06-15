---
name: requirements-ledger
description: Requirements ledger tracking for multi-step, risk-heavy, or validation-heavy Codex work. Use when a task has multiple requirements, unresolved risks, tests, handoffs, backtest/data/live-trading safety concerns, changed-scope tracking, or when a stop guard needs durable evidence before final answer.
---

# Requirements Ledger

Use `.trace-miner/ledger.json` as durable task state when chat memory is not enough.

Use a file ledger for large, delegated, multi-session, high-risk, or validation-heavy work. For small work, an inline checklist is enough unless a repo instruction requires the ledger.

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

1. Choose file ledger, inline checklist, or no ledger based on task risk and repo instructions.
2. Add every user requirement as a ledger row when using the file ledger.
3. Keep risk rows explicit; for AERA include bias, data, cache, sim/live, recovery, and rollback risks when relevant.
4. Record validation commands or exact blockers.
5. Close requirements only with evidence.
6. Before final answer, ensure no open risks remain unless accepted or deferred with a concrete reason.
