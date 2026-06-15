# Trace Miner

Trace Miner is a Codex App plugin project for turning public Fable 5 trace datasets and related open-source projects into practical Codex workflows. It does not copy leaked system prompts, does not depend on raw chain-of-thought, does not store raw trace rows, and does not train or fine-tune anything.

The plugin packages routed skills, three conservative hooks, a read-only MCP context skeleton, source notes, structured behavior patterns, and a before/after eval scorecard.

## Install

Use this directory as the plugin root. For a local marketplace, point a marketplace entry at this folder or copy it under your normal Codex plugin directory.

Minimal repo-local marketplace entry:

```json
{
  "name": "local-trace-miner",
  "interface": {
    "displayName": "Local Trace Miner"
  },
  "plugins": [
    {
      "name": "codex-trace-miner",
      "source": {
        "source": "local",
        "path": "./codex-trace-miner"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

After enabling it, review and trust the bundled hooks in Codex. Plugin hooks are intentionally not trusted silently.

## Use

## Simple Usage

- `Use skill-router for this task.`
- `Use trace-researcher to study these sources and improve the skills.`
- `Use finalguard-review before final answer.`
- `Use context-router to choose CodeGraph, Serena, Context7, MCP, or fallback.`
- `Use fusion-orchestrator for this complex task.`

Recommended prompts:

- `Use $skill-router to choose the Trace Miner route for this task.`
- `Use $trace-researcher to study these public sources safely.`
- `Use $trace-miner to turn these public trace notes into reusable Codex patterns.`
- `Use $planning-architect and $requirements-ledger before implementing this risky change.`
- `Use $implementation-pack to prepare one safe handoff for a single implementer.`
- `Use $context-router to decide what context Codex should read before editing.`
- `Use $context-router to route CodeGraph, Serena, Context7, MCP, or fallback for this task.`
- `Use $finalguard-review before final answer.`
- `Use $debug-autopsy to explain why this failed and how to prevent a repeat.`
- `Use $fusion-orchestrator to choose none, mini, full, or critical Trace Fusion mode.`

## Trace Fusion

Trace Fusion is a local Codex-only workflow for coordinating multiple GPT-5.5 Codex subagents with different roles. It does not use OpenRouter, external model APIs, hosting, fine-tuning, Fable prompts, raw trace rows, or chain-of-thought.

Modes:

- `none`: `context-router` + `finalguard-review` for trivial work.
- `mini`: `trace-architect` + `trace-reviewer`; parent implements or assigns one bounded implementer.
- `full`: architect + context scout + one write owner + reviewer.
- `critical`: full mode + `requirements-ledger` + stricter finalguard and explicit validation evidence.

Project-scoped agents live in `.codex/agents/`: `trace-architect`, `trace-context-scout`, `trace-implementer`, and `trace-reviewer`. Subagents are read-only unless `trace-implementer` is explicitly assigned one bounded write scope.

## Codex App Tool Automation

Trace Miner routes Codex App tools through `context-router`:

- CodeGraph for repo architecture, symbols, callers, impact, and where-is questions.
- Serena for precise Python/code understanding or symbol-aware edits after project activation.
- Context7 for current third-party library, framework, SDK, API, CLI, or cloud-service docs.
- Fable Mode MCP for read-only source, pattern, eval, and tool-automation context.

Local indexes stay local: `.codegraph/` and `.serena/` are ignored by git.

## What Is Included

- Skills in `skills/`
- Hook config in `hooks/hooks.json`
- Hook scripts in `hooks/`
- Optional read-only MCP server in `mcp/trace_miner_server.py`
- Source and protocol docs in `docs/`
- Structured behavior records in `patterns/patterns.jsonl`
- Before/after scorecard in `eval/`

## Safety Limits

Trace Miner extracts reusable behavior only: planning, context routing, validation, tool discipline, handoff, review, and failure detection. It should not store raw proprietary traces, leaked prompts, private chain-of-thought, secrets, live trading credentials, or user data.

For AERA-style financial research, use the requirements ledger before meaningful edits and keep simulation, backtest validation, data assumptions, cache behavior, and live execution risks explicit.

## Validate

Run:

```bash
python -m pytest tests/test_hooks.py tests/test_plugin_artifacts.py -q
python C:/Users/mathe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/trace-miner
```

Repeat the skill validator for each skill folder. The Fable Mode MCP server can be smoke-tested with:

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp/trace_miner_server.py --once
```

PowerShell:

```powershell
'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp\trace_miner_server.py --once
```

On Windows, this plugin uses `python` in `.mcp.json` because `python3` may resolve to the Microsoft Store alias instead of a real interpreter.
