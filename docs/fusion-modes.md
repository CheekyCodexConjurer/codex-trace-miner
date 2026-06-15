# Trace Fusion Modes

Trace Fusion is adaptive. Use the smallest mode that lowers real risk.

## none

Use for trivial or low-risk tasks.

- Route: `context-router` -> `finalguard-review`.
- No subagents.
- Parent handles the work.

## mini

Use for medium-risk planning, docs, review, or small multi-file work.

- Agents: `trace-architect`, `trace-reviewer`.
- Parent implements, or assigns one bounded write scope.
- Good for catching weak plans without slowing the task.

## full

Use for complex, multi-file, or ambiguous work.

- Agents: `trace-architect`, `trace-context-scout`, optional one `trace-implementer`, `trace-reviewer`.
- Parent compares architect and scout evidence before implementation.
- One write owner only.

## critical

Use only for high safety, financial, security, migration, data, or irreversible-risk work.

- Route: full mode + `requirements-ledger` + stricter `finalguard-review`.
- Requires explicit validation evidence or a concrete blocker.
- Parent must report unresolved risk and rollback path.

## Mode Selection

| Signal | Mode |
| --- | --- |
| Typo, small docs edit, read-only answer | none |
| Medium docs/skill/eval update | mini |
| Multi-file behavior change or unclear context | full |
| Financial, security, migration, production, or irreversible risk | critical |
