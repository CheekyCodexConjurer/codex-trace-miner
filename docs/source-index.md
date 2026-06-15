# Source Index

Checked on: 2026-06-15.

This index records public sources that Trace Miner can study for reusable operating patterns. It is not a prompt library and must not be used to copy private prompts, leaked system messages, or raw chain-of-thought into runtime instructions.

## Primary Trace Sources

| Source | Type | Checked | License or provenance status | Safe use |
| --- | --- | --- | --- | --- |
| [Glint-Research/Fable-5-traces](https://huggingface.co/datasets/Glint-Research/Fable-5-traces) | Hugging Face dataset | 2026-06-15 | Dataset card observed with AGPL-3.0 metadata and 4.67k train rows. | Use aggregate workflow, tool-order, validation, and failure-mode patterns. Do not copy trace text or chain-of-thought. |
| [armand0e/claude-fable-5-claude-code](https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code) | Hugging Face agent traces | 2026-06-15 | Public agent-traces dataset observed; license not visible in inspected page output. | Use schema/metadata only and do not reuse content unless license/provenance is clarified. |
| [armand0e/fable-5-claude-code-preview](https://huggingface.co/datasets/armand0e/fable-5-claude-code-preview) | Hugging Face preview dataset | 2026-06-15 | Public preview pages observed; use canonical dataset when both exist. | Treat as comparison evidence only. |
| [kelexine/fable-5-sft-traces](https://huggingface.co/datasets/kelexine/fable-5-sft-traces) | Hugging Face dataset | 2026-06-15 | Dataset card observed with AGPL-3.0 inherited from upstream derivative. | Use provenance/schema notes only. No fine-tuning in this project. |

## Related GitHub Projects

| Source | Type | Checked | Safe use |
| --- | --- | --- | --- |
| [DanMcInerney/architect-loop](https://github.com/DanMcInerney/architect-loop) | Architect/builder loop project | 2026-06-15 | Compare planning and handoff patterns. |
| [Rylaa/fable5-orchestrator](https://github.com/Rylaa/fable5-orchestrator) | Orchestration plugin | 2026-06-15 | Compare routing, requirements ledger, and guard hook ideas. |
| [ryu-tada/agent-operating-protocol](https://github.com/ryu-tada/agent-operating-protocol) | Agent protocol templates | 2026-06-15 | Compare protocol framing, safety limits, and non-affiliation language. |
| [kei99-web3/codex-claude-fable-5-consult-skill](https://github.com/kei99-web3/codex-claude-fable-5-consult-skill) | Codex skill | 2026-06-15 | Compare consultation handoff patterns. |
| [zakarya526/fable-skill](https://github.com/zakarya526/fable-skill) | Planning/audit skill | 2026-06-15 | Compare audit and executable-plan patterns. |

## Optional Comparison Sources

Use only for comparison after checking current repository state, license, and provenance: `deo-harness`, `guardian-runtime`, `awesome-claude-fable-5`, `v-Fable`, `Vibe-Coding-Claude-Fable-5`, and distilled-model repositories. Some names may resolve to different owners or may be unavailable; record exact URLs before using them.

Distilled-model repos are ecosystem evidence only. This project must not train, fine-tune, merge adapters, or produce model weights.

## Extraction Rules

1. Record source URL, date checked, license or unknown license, and evidence type.
2. Extract only behavior patterns: context gathering, planning, handoff, validation, review, recovery, and measurable eval criteria.
3. Do not paste trace messages longer than short identifiers or metadata needed for audit.
4. Do not preserve chain-of-thought, hidden prompts, private user data, secrets, or proprietary code.
5. Prefer docs and eval artifacts over runtime skill bloat.
