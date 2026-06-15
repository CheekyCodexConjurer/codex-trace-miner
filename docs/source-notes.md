# Source Notes

Checked on: 2026-06-15.

These notes summarize public source metadata, safe observations, and aggregate-only dataset scans. They intentionally do not store raw trace rows, prompts, chain-of-thought, secrets, private data, or proprietary code. Dataset viewers may expose row-level content by default; this study used schema, tags, counts, README/card text, file lists, repository-level behavior, and in-memory aggregate metrics only.

## Phase 2 Safe Aggregate Method

- Processed public dataset rows only in memory.
- Printed and retained only counts, key names, type summaries, list/string length stats, safe category counts, and source-level reports.
- Did not write row payloads, prompts, messages, reasoning text, tool outputs, file contents, or private paths.
- Treated training/distillation notes as rejected provenance, not runtime guidance.
- Treated metadata-only or unrun-eval findings as docs/eval candidates, not automatic runtime rules.

## Hugging Face Sources

### Glint-Research/Fable-5-traces

- URL: https://huggingface.co/datasets/Glint-Research/Fable-5-traces
- Type: Hugging Face dataset.
- License/provenance visible: AGPL-3.0. Dataset metadata showed text/json format, 133 MB total file size, public files, and a public model/fine-tune ecosystem around the dataset.
- Inspected: dataset card, API metadata, file list, viewer/schema failure details, and every public JSONL file through an aggregate-only scanner.
- Aggregate evidence: 117 JSONL files scanned, 117 succeeded, 0 parse/fetch errors, 132,466,893 bytes read, 26,219 JSONL records seen. The aggregate found 4,665 normalized records with fields such as `context`, `cot`, `output`, and `completion`; 12,863 message objects; 4,185 tool-use content items; 4,185 tool-result content items; 2,223 reasoning-type content items; and retry/error/fallback metadata including rate-limit-like status counts. No payload values were retained.
- Accepted behavior patterns: Source Boundary Before Pattern Mining (`context gathering`, `tool discipline`), Structural Samples Only (`context gathering`, `tool discipline`), Aggregate-Only Dataset Mining (`context gathering`, `tool discipline`, `validation`), Tool-Loop Density Drives Eval Focus (`tool discipline`, `validation`, `debugging/recovery`), Truncation-Aware Context Claims (`context gathering`, `review`, `validation`), Recovery Signals Are Aggregate Evidence (`debugging/recovery`, `tool discipline`), Model-Independent Behavior Extraction (`routing/orchestration`, `review`).
- Destination: `trace-researcher` safety rule, `patterns/patterns.jsonl`, source hygiene eval checks, optional MCP pattern context.
- Rejected: row-level prompts, reasoning text, task examples, private paths, tool outputs, and model-training/fine-tuning use.
- Confidence: high for structural/tool/recovery aggregate evidence; low for semantic conclusions about task quality or model reasoning.

### armand0e/claude-fable-5-claude-code

- URL: https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code
- Type: Hugging Face agent-trace dataset.
- License/provenance visible: no license label found in the inspected page output. Public metadata identifies json/traces format, agent-trace tags, 63 rows, and public notes about extraction/normalization tooling.
- Inspected: dataset card, API metadata, README, file list, public tool-schema snapshot presence, and all 63 rows through the Hugging Face rows API in aggregate-only mode. Task titles, row messages, prompts, tool schema body, and trace payloads were deliberately excluded from notes.
- Aggregate evidence: 63 rows; all expected columns present (`harness`, `session_id`, `prompt`, `messages`, `tools`, `metadata`, `sent_at`, `num_user_messages`, `num_tool_calls`, `trace`, `file_path`). `num_tool_calls` ranged from 0 to 376 with median 35 and mean 66.14. Message-list length ranged from 2 to 878 with median 78. Tool-list length ranged from 16 to 27. Trace-list length ranged from 8 to 1,720. This supports tool-discipline and context-packing evals, not semantic model imitation.
- Accepted behavior patterns: Structural Samples Only (`context gathering`, `tool discipline`), Aggregate-Only Dataset Mining (`context gathering`, `tool discipline`, `validation`), Tool-Loop Density Drives Eval Focus (`tool discipline`, `validation`, `debugging/recovery`), Decision Pack For External Review (`handoff`, `context gathering`, `tool discipline`), Source Boundary Before Pattern Mining (`context gathering`, `tool discipline`).
- Destination: `trace-researcher` sample boundary, `context-router` evidence selection rule, eval check for "no raw trace rows".
- Rejected: distillation/fine-tuning recommendations, task text, prompts, long tool schema copying, tool output details, and any attempt to imitate model style.
- Confidence: high for aggregate tool-density evidence; medium for provenance because license was not visible; low for behavior quality conclusions.

### kelexine/fable-5-sft-traces

- URL: https://huggingface.co/datasets/kelexine/fable-5-sft-traces
- Type: Hugging Face dataset.
- License/provenance visible: AGPL-3.0. The card describes a cleaned, anonymized, schema-normalized derivative of upstream Fable 5 traces and says the derivative inherits the upstream license.
- Inspected: dataset card, API metadata, schema headings, row/session counts, origin/task-type summaries, `cleaning_report.json`, `analysis_report.txt`, and caveats. Row preview content and reasoning fields were not retained.
- Aggregate evidence: cleaning report shows 4,665 raw rows, 4,665 clean rows, 0 duplicates removed, 0 invalid drops, 4,121 context-truncated rows, 3,799 agentic/tool-use rows, 866 reasoning/text rows, 3,712 local-origin rows, and 953 Hugging Face-origin rows. The analysis report confirms schema version, origin-specific truncation rates, and aggregate length distributions. This supports truncation-aware conclusions and eval focus, not training use.
- Accepted behavior patterns: Source Boundary Before Pattern Mining (`context gathering`, `tool discipline`), Structural Samples Only (`context gathering`, `tool discipline`), Aggregate-Only Dataset Mining (`context gathering`, `tool discipline`, `validation`), Truncation-Aware Context Claims (`context gathering`, `review`, `validation`), Tool-Loop Density Drives Eval Focus (`tool discipline`, `validation`, `debugging/recovery`), Eval Every Workflow Claim (`validation`, `review`).
- Destination: `trace-researcher` provenance checklist, scorecard source-hygiene checks, optional MCP context.
- Rejected: all fine-tuning shapes, reasoning extraction, row reconstruction, and training-oriented usage.
- Confidence: high for provenance, schema-level evidence, truncation, and aggregate class distributions; low for semantic task-quality conclusions.

## GitHub Sources

### DanMcInerney/architect-loop

- URL: https://github.com/DanMcInerney/architect-loop
- Type: GitHub project.
- License/provenance visible: MIT license.
- Inspected: repository README, file list, install/use sections, origin/license notes, and visible design claims around architect/builder/review loops.
- Accepted behavior patterns: Acceptance Gates Before Builders (`planning`, `validation`, `review`), Scout Then Decompose Research (`context gathering`, `task decomposition`, `routing/orchestration`), One Implementer, Independent Review (`task decomposition`, `review`, `handoff`).
- Destination: `planning-architect`, `implementation-pack`, `finalguard-review`, eval checks for acceptance gates and diff intent.
- Rejected: cross-vendor model imitation and any requirement that Trace Miner depend on a specific external model.
- Confidence: high for workflow structure; medium for claims not independently validated by running the project.

### Rylaa/fable5-orchestrator

- URL: https://github.com/Rylaa/fable5-orchestrator
- Type: GitHub plugin/project.
- License/provenance visible: MIT license.
- Inspected: repository README, file list, hook/instruction/script layout, requirements-ledger explanation, proportional workflow comparison, and guard-hook behavior description.
- Accepted behavior patterns: Proportional Ledger Discipline (`ledger/checklist`, `routing/orchestration`), Guard Hooks Fence Skipped Rules (`tool discipline`, `validation`, `review`), Final Guard Blocks Incomplete Work (`review`, `validation`, `ledger/checklist`).
- Destination: `requirements-ledger`, stop/pre-tool hook philosophy, `finalguard-review`, hook tests, eval checks for proportional ledger use.
- Rejected: model-tier ceremony as a hard runtime dependency, aggressive delegation rules, and broad hook enforcement beyond deterministic safety/completion checks.
- Confidence: high for ledger/hook design; medium for model-specific routing claims.

### ryu-tada/agent-operating-protocol

- URL: https://github.com/ryu-tada/agent-operating-protocol
- Type: GitHub protocol/template project.
- License/provenance visible: MIT license. README explicitly frames the project as public, vendor-neutral, and not a leaked or reconstructed vendor prompt.
- Inspected: README, file list, positioning/safety sections, operating-protocol behaviors, license notes.
- Accepted behavior patterns: Capability Manifest Before Tool Use (`tool discipline`, `context gathering`, `debugging/recovery`), Model-Independent Behavior Extraction (`routing/orchestration`, `review`), Evidence Before Action (`context gathering`, `routing/orchestration`).
- Destination: `context-router`, `debug-autopsy`, `skill-router`, eval checks for tool fallback and source/context selection.
- Rejected: any vendor-prompt reconstruction, jailbreak framing, or style/personality mimicry.
- Confidence: high for protocol boundaries and reusable behavior categories.

### kei99-web3/codex-claude-fable-5-consult-skill

- URL: https://github.com/kei99-web3/codex-claude-fable-5-consult-skill
- Type: GitHub Codex skill/project.
- License/provenance visible: MIT license.
- Inspected: repository README, file list, local-account boundary, prompt-packing behavior, cost/safety controls, read-only review defaults, and license notes.
- Accepted behavior patterns: Decision Pack For External Review (`handoff`, `context gathering`, `tool discipline`), Read-Only Audit Produces Executable Plans (`review`, `task decomposition`, `handoff`), Capability Manifest Before Tool Use (`tool discipline`, `context gathering`, `debugging/recovery`).
- Destination: `implementation-pack`, `context-router`, `trace-researcher`, eval checks for selected/omitted context and safety filters.
- Rejected: sending raw workspace noise, secrets, private context, or unverified external recommendations directly into implementation.
- Confidence: high for packet/safety behavior; low for any external-model quality claim.

### zakarya526/fable-skill

- URL: https://github.com/zakarya526/fable-skill
- Type: GitHub skill/project.
- License/provenance visible: MIT license and attribution to an MIT-licensed original project.
- Inspected: repository README, file list, usage modes, audit/vet/prioritize/plan flow, guarantees, and credits/license section.
- Accepted behavior patterns: Read-Only Audit Produces Executable Plans (`review`, `task decomposition`, `handoff`), Acceptance Gates Before Builders (`planning`, `validation`, `review`), One Implementer, Independent Review (`task decomposition`, `review`, `handoff`).
- Destination: `planning-architect`, `implementation-pack`, `finalguard-review`, eval checks for executable plan quality and evidence-backed review.
- Rejected: generated backlog sprawl, personality/model split as a required dependency, and any plan that cannot be tied to validation gates.
- Confidence: high for audit-to-plan workflow; medium for implementation outcomes not reproduced locally.

## Rejected Pattern Classes

- Fine-tuning, distillation, or model-training workflows: out of scope and explicitly prohibited.
- Raw trace rows, prompt examples, task titles, reasoning fields, and private paths: unsafe or unnecessary for runtime behavior.
- Leaked or reconstructed system prompts: prohibited and not needed for behavior extraction.
- Personality/style imitation: not measurable against Trace Miner goals.
- Heavy fixed ceremony: rejected unless proportional to risk, size, delegation, or multi-session work.
- Broad hooks with subjective judgment: kept in skills/review instead of enforced mechanically.

## Research Rule

When a source requires raw trace rows to prove a point, stop. Record the gap instead of copying the row.
