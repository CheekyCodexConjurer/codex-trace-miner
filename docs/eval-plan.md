# Eval Plan

The eval asks whether Trace Miner improves Codex behavior on the same task, not whether it imitates another model.

## Method

1. Select a task prompt and a small repo fixture.
2. Run baseline Codex without Trace Miner.
3. Run Codex with Trace Miner skills and hooks available.
4. Score both outputs with `eval/before-after-scorecard.md`.
5. Record commands, files changed, validation evidence, and reviewer notes.

## Task Classes

- risky implementation with missing requirements
- backtest or research change with bias risk
- debugging failure with unclear root cause
- final review before handoff
- context-heavy refactor with possible over-read

## Pass Bar

Trace Miner is useful only if the after run improves total score without adding unsafe behavior, unsupported claims, or large runtime bloat.

Minimum target: +20 percent total score and no regression in safety, evidence, or validation categories.
