#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path


ROOT = Path(os.environ.get("TRACE_MINER_ROOT", Path(__file__).resolve().parents[1])).resolve()

TOOLS = {
    "get_source_index": {
        "description": "Read the Trace Miner public source index.",
        "path": ROOT / "docs" / "source-index.md",
    },
    "get_extracted_patterns": {
        "description": "Read reusable trace-derived operating patterns.",
        "path": ROOT / "docs" / "extracted-patterns.md",
    },
    "get_operating_protocol": {
        "description": "Read the Codex operating protocol used by Trace Miner.",
        "path": ROOT / "docs" / "codex-operating-protocol.md",
    },
    "get_eval_scorecard": {
        "description": "Read the before/after eval scorecard.",
        "path": ROOT / "eval" / "before-after-scorecard.md",
    },
    "get_fusion_scorecard": {
        "description": "Read the Trace Fusion eval scorecard.",
        "path": ROOT / "eval" / "fusion-scorecard.md",
    },
    "get_tool_automation": {
        "description": "Read Trace Miner Codex App tool routing for CodeGraph, Serena, Context7, and MCP.",
        "path": ROOT / "docs" / "tool-automation.md",
    },
    "get_fusion_protocol": {
        "description": "Read the local Codex-only Trace Fusion protocol.",
        "path": ROOT / "docs" / "fusion-protocol.md",
    },
    "get_fusion_modes": {
        "description": "Read Trace Fusion adaptive mode guidance.",
        "path": ROOT / "docs" / "fusion-modes.md",
    },
    "get_patterns": {
        "description": "Read structured Trace Miner behavior patterns as JSONL.",
        "path": ROOT / "patterns" / "patterns.jsonl",
    },
}


def response(request_id, result):
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def request_id_from(payload):
    if isinstance(payload, dict):
        return payload.get("id")
    return None


def tool_list():
    return {
        "tools": [
            {
                "name": name,
                "description": meta["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            }
            for name, meta in TOOLS.items()
        ]
    }


def call_tool(name: str):
    meta = TOOLS.get(name)
    if not meta:
        raise KeyError(f"unknown tool: {name}")
    path = meta["path"]
    if not path.exists():
        raise FileNotFoundError(f"missing context file: {path.relative_to(ROOT)}")
    return {
        "content": [
            {
                "type": "text",
                "text": path.read_text(encoding="utf-8"),
            }
        ]
    }


def handle(payload: dict) -> dict | None:
    if not isinstance(payload, dict):
        return error_response(None, -32600, "invalid request: JSON-RPC payload must be an object")

    method = payload.get("method")
    request_id = payload.get("id")

    if method == "initialize":
        return response(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "Fable Mode", "version": "0.3.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return response(request_id, tool_list())
    if method == "tools/call":
        name = (payload.get("params") or {}).get("name")
        try:
            return response(request_id, call_tool(name))
        except (KeyError, FileNotFoundError) as exc:
            return error_response(request_id, -32000, str(exc))
        except Exception as exc:
            return error_response(request_id, -32603, f"internal error: {exc}")

    return error_response(request_id, -32601, f"method not found: {method}")


def serve_once() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    try:
        payload = json.loads(line)
    except json.JSONDecodeError as exc:
        result = error_response(None, -32700, f"parse error: {exc.msg}")
    else:
        try:
            result = handle(payload)
        except Exception as exc:
            result = error_response(request_id_from(payload), -32603, f"internal error: {exc}")
    if result is not None:
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()
    return 0


def serve_loop() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            result = error_response(None, -32700, f"parse error: {exc.msg}")
        else:
            try:
                result = handle(payload)
            except Exception as exc:
                result = error_response(request_id_from(payload), -32603, f"internal error: {exc}")
        if result is not None:
            sys.stdout.write(json.dumps(result) + "\n")
            sys.stdout.flush()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Trace Miner read-only MCP skeleton")
    parser.add_argument("--once", action="store_true", help="Handle one JSON-RPC request and exit")
    args = parser.parse_args()
    return serve_once() if args.once else serve_loop()


if __name__ == "__main__":
    raise SystemExit(main())
