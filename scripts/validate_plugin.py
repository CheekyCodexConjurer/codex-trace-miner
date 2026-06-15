#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILLS = {
    "trace-miner",
    "trace-researcher",
    "skill-router",
    "planning-architect",
    "requirements-ledger",
    "implementation-pack",
    "context-router",
    "finalguard-review",
    "debug-autopsy",
}
REQUIRED_DOCS = {
    "docs/source-index.md",
    "docs/extracted-patterns.md",
    "docs/codex-operating-protocol.md",
    "docs/eval-plan.md",
    "docs/behavior-study.md",
    "docs/routing-guide.md",
    "docs/source-notes.md",
    "docs/tool-automation.md",
    "eval/before-after-scorecard.md",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(relative: str) -> dict:
    path = ROOT / relative
    if not path.exists():
        fail(f"missing {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest() -> None:
    manifest = load_json(".codex-plugin/plugin.json")
    if manifest.get("name") != "codex-trace-miner":
        fail("plugin name must be codex-trace-miner")
    for key in ("skills", "hooks", "mcpServers"):
        target = manifest.get(key)
        if not isinstance(target, str) or not target.startswith("./"):
            fail(f"manifest {key} must be a ./ relative path")
        if not (ROOT / target[2:]).exists():
            fail(f"manifest path does not exist: {target}")
    if manifest.get("interface", {}).get("displayName") != "Trace Miner":
        fail("displayName must be Trace Miner")


def validate_skill(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail(f"missing frontmatter: {path}")
    frontmatter = match.group(1)
    fields = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    name = fields.get("name")
    description = fields.get("description")
    if path.parent.name != name:
        fail(f"skill name mismatch: {path}")
    if not description or "TODO" in description:
        fail(f"missing useful description: {path}")

    openai_yaml = path.parent / "agents" / "openai.yaml"
    if openai_yaml.exists():
        metadata = openai_yaml.read_text(encoding="utf-8")
        if f"${name}" not in metadata:
            fail(f"agents/openai.yaml default prompt should mention ${name}: {openai_yaml}")


def validate_skills() -> None:
    actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if actual != REQUIRED_SKILLS:
        fail(f"skill set mismatch: {sorted(actual)}")
    for skill in REQUIRED_SKILLS:
        validate_skill(ROOT / "skills" / skill / "SKILL.md")


def validate_docs() -> None:
    for relative in REQUIRED_DOCS:
        path = ROOT / relative
        if not path.exists():
            fail(f"missing {relative}")
        text = path.read_text(encoding="utf-8")
        if "TODO" in text:
            fail(f"TODO remains in {relative}")


def validate_hooks_and_mcp() -> None:
    hooks = load_json("hooks/hooks.json")
    for event in ("SessionStart", "PreToolUse", "Stop"):
        if event not in hooks.get("hooks", {}):
            fail(f"missing hook event {event}")
    mcp = load_json(".mcp.json")
    if "trace-miner-context" not in mcp.get("mcp_servers", {}):
        fail("missing trace-miner-context MCP server")


def validate_patterns() -> None:
    path = ROOT / "patterns" / "patterns.jsonl"
    if not path.exists():
        fail("missing patterns/patterns.jsonl")
    required = {
        "id",
        "name",
        "behavior",
        "sources",
        "evidence_type",
        "runtime_rule",
        "target_skills",
        "eval_check",
        "risk",
        "confidence",
        "classification",
        "destination",
    }
    count = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        record = json.loads(line)
        missing = required - record.keys()
        if missing:
            fail(f"pattern line {line_number} missing fields: {sorted(missing)}")
        if not isinstance(record["sources"], list):
            fail(f"pattern line {line_number} sources must be a list")
        if not isinstance(record["target_skills"], list):
            fail(f"pattern line {line_number} target_skills must be a list")
        if not isinstance(record["classification"], list) or not record["classification"]:
            fail(f"pattern line {line_number} classification must be a non-empty list")
        if not isinstance(record["destination"], list) or not record["destination"]:
            fail(f"pattern line {line_number} destination must be a non-empty list")
        if record["confidence"] not in {"low", "medium", "high"}:
            fail(f"pattern line {line_number} has invalid confidence")
        count += 1
    if count < 7:
        fail("patterns.jsonl should contain at least 7 records")


def main() -> int:
    try:
        validate_manifest()
        validate_skills()
        validate_docs()
        validate_hooks_and_mcp()
        validate_patterns()
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    print("Trace Miner plugin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
