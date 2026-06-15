# Extracted Patterns

These are reusable operational patterns. They are deliberately abstracted away from raw trace text.

## Pattern 1: Evidence Before Action

Good agents inspect repo instructions, file structure, and relevant source code before choosing an implementation. Runtime form: use `context-router` before editing, and write down what was read and skipped.

## Pattern 2: Ledger As Working Memory

Long tasks need a compact state artifact that survives context loss. Runtime form: `.trace-miner/ledger.json` tracks requirements, validation, changed scope, risks, and next action.

## Pattern 3: One Implementer, Independent Review

Complex changes benefit from one write-capable implementer and separate read-only review. Runtime form: one owner patches files; reviewers inspect requirements, risks, and validation evidence.

## Pattern 4: Handoff Packs Beat Vague Plans

Implementation handoffs should include scope, files, constraints, commands, acceptance criteria, rollback, and stop conditions. Runtime form: `implementation-pack` creates a bounded slice.

## Pattern 5: Final Guard Blocks Incomplete Work

The final answer should not happen while requirements are open, tests are missing, changed files are unknown, or risks are unresolved. Runtime form: `finalguard-review` and the `Stop` hook check the ledger.

## Pattern 6: Debug Autopsy Prevents Repeat Failures

A useful bug fix explains trigger, failed assumption, evidence, fix, prevention, and regression test. Runtime form: `debug-autopsy` turns one failure into a reusable checklist item.

## Pattern 7: Eval Every Workflow Claim

Workflow improvements must be measurable. Runtime form: run the same prompt before and after Trace Miner and score planning, context choice, safety, validation, and recovery.
