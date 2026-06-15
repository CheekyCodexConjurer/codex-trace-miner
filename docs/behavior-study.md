# Behavior Study

Checked on: 2026-06-15.

Trace Miner studies public Fable 5-related sources for behavior, not content. The system converts source links into source notes, source notes into structured patterns, patterns into concise runtime skills, and skills into eval checks.

## Source-To-Behavior Flow

1. `skill-router` classifies the request and sends source work to `trace-researcher`.
2. `trace-researcher` inspects public metadata: README, dataset card, license/provenance, file list, safe schema-level samples, and aggregate-only scans when needed.
3. Source observations are recorded in `docs/source-notes.md`.
4. Accepted behaviors are normalized into `patterns/patterns.jsonl`.
5. Runtime rules stay concise inside affected skills.
6. Eval checks are recorded in `eval/before-after-scorecard.md`.

## Phase 2 Aggregate Findings

- `Glint-Research/Fable-5-traces`: scanned 117 public JSONL files in memory, 26,219 records, 0 parse/fetch errors. Aggregate evidence supports tool-loop density, recovery/fallback signals, truncation/capped-context uncertainty, and strict no-row-retention rules.
- `armand0e/claude-fable-5-claude-code`: scanned all 63 rows through the public rows API in aggregate-only mode. Tool-call counts are high enough to justify tool-discipline evals, but license/provenance remained unclear, so no content reuse is allowed.
- `kelexine/fable-5-sft-traces`: used public cleaning and analysis reports. The dataset reports 4,665 clean rows, 4,121 context-truncated rows, 3,799 agentic/tool-use rows, and 866 reasoning/text rows. This supports truncation-aware context claims and eval focus, not training use.
- GitHub project review was read-only and README-level. It supports workflow patterns, but not claims about implementation correctness unless code is later audited.

## Accepted Runtime Patterns

| Pattern | Classification | Runtime destination | Eval check |
| --- | --- | --- | --- |
| Source Boundary Before Pattern Mining | context gathering, tool discipline | `trace-researcher`, `trace-miner` | Source note records URL, date, type, license/provenance, inspected surfaces, exclusions, confidence. |
| Structural Samples Only | context gathering, tool discipline | `trace-researcher`, `context-router`, MCP context | Research output uses metadata/schema evidence and contains no raw trace rows. |
| Aggregate-Only Dataset Mining | context gathering, tool discipline, validation | `trace-researcher`, `trace-miner` | Research report lists files or rows scanned, aggregate metrics, excluded payload classes, and confidence. |
| Truncation-Aware Context Claims | context gathering, review, validation | `trace-researcher`, `context-router`, `finalguard-review` | Agent reports truncation/capped-context risk and avoids overclaiming from incomplete traces. |
| Tool-Loop Density Drives Eval Focus | tool discipline, validation, debugging/recovery | `context-router`, `debug-autopsy`, `finalguard-review` | Eval covers wrong-tool, missing-validation, and recovery cases. |
| Recovery Signals Are Aggregate Evidence | debugging/recovery, tool discipline | `debug-autopsy`, `context-router` | Failure eval includes an unavailable or rate-limited tool with bounded fallback. |
| Confidence Gating For Runtime Rules | review, routing/orchestration, validation | `trace-miner`, `trace-researcher`, `skill-router` | Medium/low-confidence patterns stay docs/eval-only until verified. |
| Proportional Ledger Discipline | ledger/checklist, routing/orchestration | `skill-router`, `requirements-ledger`, hooks | Agent chooses file ledger, inline checklist, or no ledger based on risk. |
| Acceptance Gates Before Builders | planning, validation, review | `planning-architect`, `implementation-pack`, `finalguard-review` | Plan includes acceptance gates and final review checks diff intent. |
| Capability Manifest Before Tool Use | tool discipline, context gathering, debugging/recovery | `context-router`, `debug-autopsy` | Agent names preferred tool, fallback, and unavailable-tool recovery. |
| Model-Independent Behavior Extraction | routing/orchestration, review | `trace-miner`, `trace-researcher`, `skill-router` | Each accepted pattern maps to measurable Codex behavior, not style. |
| Guard Hooks Fence Skipped Rules | tool discipline, validation, review | hooks, `finalguard-review`, `requirements-ledger` | Hook tests prove safe commands pass and risky/incomplete states block conservatively. |

## Docs/Eval-Only Or Conditional Patterns

| Pattern | Status | Reason |
| --- | --- | --- |
| Ledger As Working Memory | docs/eval-only | Superseded by proportional ledger discipline. |
| Eval Every Workflow Claim | eval check | Correct adoption gate, not a runtime workflow step. |
| Scout Then Decompose Research | docs/eval-only | Useful for broad research, too heavy for ordinary tasks. |
| Decision Pack For External Review | conditional skill/eval | Use only for explicit handoff, delegation, or external review. |
| Read-Only Audit Produces Executable Plans | docs/eval-only | Good research/review mode, not mandatory before ordinary implementation. |

The first scaffold patterns remain useful, but phase 2 narrows their scope. The runtime system should promote only patterns with high-confidence evidence and measurable impact.

## Rejected Patterns

| Rejected class | Reason |
| --- | --- |
| Fine-tuning, distillation, model training | Explicitly out of scope; improves model imitation, not Codex runtime behavior. |
| Raw row examples and task titles | Unsafe and unnecessary; may contain prompts, private paths, or copyrighted/user content. |
| Raw reasoning fields | Explicitly prohibited; runtime skills need behavior rules, not chain-of-thought. |
| Leaked or reconstructed system prompts | Prohibited and not required for any accepted pattern. |
| Personality or style mimicry | Not tied to fewer wrong edits, better validation, or better recovery. |
| Fixed heavy ceremony | Adds latency and ritual compliance; accepted only when proportional to risk. |
| Broad subjective hooks | Hooks should enforce deterministic safety/completion checks; judgment stays in skills/review. |
| External review as authority | External advice is input only; Codex must verify locally before applying. |

## Skill Implications

- `skill-router` should route research first and add ledgers only when risk, size, validation, or delegation justifies them.
- `trace-researcher` should classify every extracted behavior and record its destination before accepting it.
- `context-router` should name preferred tools and fallbacks, especially when CodeGraph, Serena, MCP, or source browsing may be unavailable.
- `planning-architect` and `implementation-pack` should define acceptance gates before implementation.
- `requirements-ledger` should stay proportional, not mandatory for trivial tasks.
- `finalguard-review` should compare changed files against intent and validate unresolved risks, not just summarize.
- `debug-autopsy` should treat missing or failed tools as recoverable routing problems when a bounded fallback exists.

## Runtime Design Decision

Trace Miner should stay easy to use:

- `skill-router` is the front door.
- `trace-researcher` handles source study.
- Existing skills remain small and task-specific.
- MCP is optional and read-only.
- Long source notes stay in docs.
