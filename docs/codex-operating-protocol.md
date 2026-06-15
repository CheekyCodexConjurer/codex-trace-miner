# Codex Operating Protocol

Trace Miner changes Codex behavior through small skills, auditable hooks, and evals. It does not use MCP as a prompt server and does not smuggle long instructions into runtime context.

## Default Loop

1. Read repo instructions and task-specific docs.
2. Route context with the smallest useful source set.
3. Create or update a requirements ledger for non-trivial work.
4. Plan one bounded implementation slice.
5. Use one write-capable implementer.
6. Validate with concrete commands or documented blockers.
7. Run finalguard review before final answer.
8. If a failure occurred, write a debug autopsy.

## AERA Safety Overlay

For market research or trading-grade code, explicitly check:

- data consistency and timestamp alignment
- lookahead and survivorship bias
- backtest assumptions and transaction cost modeling
- cache invalidation and reproducibility
- simulation/live execution separation
- idempotency, recovery, and rollback
- observability and unresolved operational risk

## Runtime Boundaries

Keep skills short. Put long source notes in `docs/`. Keep hooks deterministic. Keep MCP read-only and evidence-focused.

Never copy leaked prompts, raw chain-of-thought, private traces, secrets, credentials, or proprietary user data into this plugin.
