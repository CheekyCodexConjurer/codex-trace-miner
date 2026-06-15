---
name: trace-researcher
description: Trace research and public Fable 5 source study for dataset cards, README files, metadata, file lists, and safe high-level samples. Use when Codex must inspect Fable 5-related Hugging Face datasets, GitHub projects, source notes, licenses, provenance, or behavior evidence without copying raw traces, chain-of-thought, leaked prompts, secrets, or proprietary code.
---

# Trace Researcher

Study public sources deeply enough to extract behavior patterns, not content.

## Safe Inspection

1. Inspect public README, dataset card, metadata, file list, and license/provenance.
2. Prefer metadata, schema, file lists, and aggregate-only scans; look at small safe samples only when needed to classify structure.
3. Record URL, date checked, source type, license/provenance, and what was inspected.
4. Classify each behavior as planning, context gathering, tool discipline, task decomposition, ledger/checklist, handoff, validation, review, debugging/recovery, or routing/orchestration.
5. Decide the destination: skill rule, hook rule, MCP context, eval check, docs only, or reject.
6. Promote high-confidence patterns to runtime only when they improve wrong-edit reduction, context selection, planning, scope control, validation, review, recovery, or routing.
7. Keep medium/low-confidence or unrun-eval patterns in docs/evals until verified.
8. Do not store or print raw trace rows, raw chain-of-thought, leaked prompts, private data, secrets, or proprietary code.

## Output

```markdown
Source:
Checked:
Type:
License/provenance:
Inspected:
Behavior patterns:
Classification:
Destination:
Excluded content:
Runtime implication:
Eval implication:
Confidence:
```
