# Trace Miner

Trace Miner is a Codex App plugin project for turning public Fable 5 trace datasets and related open-source projects into practical Codex workflows. It does not copy leaked system prompts, does not depend on raw chain-of-thought, and does not train or fine-tune anything.

The plugin packages seven skills, three conservative hooks, a read-only MCP context skeleton, source notes, and a before/after eval scorecard.

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

Recommended prompts:

- `Use $trace-miner to turn these public trace notes into reusable Codex patterns.`
- `Use $planning-architect and $requirements-ledger before implementing this risky change.`
- `Use $implementation-pack to prepare one safe handoff for a single implementer.`
- `Use $context-router to decide what context Codex should read before editing.`
- `Use $finalguard-review before final answer.`
- `Use $debug-autopsy to explain why this failed and how to prevent a repeat.`

## What Is Included

- Skills in `skills/`
- Hook config in `hooks/hooks.json`
- Hook scripts in `hooks/`
- Optional read-only MCP server in `mcp/trace_miner_server.py`
- Source and protocol docs in `docs/`
- Before/after scorecard in `eval/`

## Safety Limits

Trace Miner extracts reusable behavior only: planning, context routing, validation, tool discipline, handoff, review, and failure detection. It should not store raw proprietary traces, leaked prompts, private chain-of-thought, secrets, live trading credentials, or user data.

For AERA-style financial research, use the requirements ledger before meaningful edits and keep simulation, backtest validation, data assumptions, cache behavior, and live execution risks explicit.

## Validate

Run:

```bash
python -m pytest tests/test_hooks.py -q
python C:/Users/mathe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/trace-miner
```

Repeat the skill validator for each skill folder. The MCP skeleton can be smoke-tested with:

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp/trace_miner_server.py --once
```

PowerShell:

```powershell
'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp\trace_miner_server.py --once
```

On Windows, this plugin uses `python` in `.mcp.json` because `python3` may resolve to the Microsoft Store alias instead of a real interpreter.
