import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_behavior_system_skills_exist():
    for skill in ("skill-router", "trace-researcher", "fusion-orchestrator"):
        skill_path = ROOT / "skills" / skill / "SKILL.md"
        assert skill_path.exists(), f"missing {skill_path}"
        content = skill_path.read_text(encoding="utf-8")
        assert f"name: {skill}" in content
        assert "description:" in content


def test_fusion_skill_has_front_loaded_trigger_description():
    skill_path = ROOT / "skills" / "fusion-orchestrator" / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    description_line = next(line for line in content.splitlines() if line.startswith("description:"))
    assert "Trace Fusion orchestration" in description_line
    assert "Codex subagent" in description_line
    assert "OpenRouter" in description_line


def test_trace_fusion_custom_agents_exist_and_are_scoped():
    expected = {
        "trace-architect": "read-only",
        "trace-context-scout": "read-only",
        "trace-implementer": "write-explicit-only",
        "trace-reviewer": "read-only",
    }
    for name, permission in expected.items():
        agent_path = ROOT / ".codex" / "agents" / f"{name}.toml"
        assert agent_path.exists(), f"missing {agent_path}"
        data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        assert data["name"] == name
        assert data["permission"] == permission
        assert "OpenRouter" in data["instructions"]


def test_patterns_jsonl_is_valid_and_structured():
    patterns_path = ROOT / "patterns" / "patterns.jsonl"
    assert patterns_path.exists(), "missing patterns/patterns.jsonl"

    records = [
        json.loads(line)
        for line in patterns_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert len(records) >= 7
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
    for record in records:
        assert required <= record.keys()
        assert isinstance(record["sources"], list)
        assert isinstance(record["target_skills"], list)
        assert isinstance(record["classification"], list)
        assert isinstance(record["destination"], list)
        assert record["confidence"] in {"low", "medium", "high"}
        assert record["classification"], record["id"]
        assert record["destination"], record["id"]
        if record["confidence"] != "high":
            assert "skill rule" not in record["destination"], record["id"]


def test_patterns_jsonl_does_not_store_raw_trace_markers():
    patterns_path = ROOT / "patterns" / "patterns.jsonl"
    text = patterns_path.read_text(encoding="utf-8").lower()

    forbidden_markers = [
        "<think>",
        "</think>",
        "user:",
        "assistant claude-fable",
        "local-command-caveat",
    ]

    for marker in forbidden_markers:
        assert marker not in text


def test_trace_fusion_patterns_exist():
    patterns_path = ROOT / "patterns" / "patterns.jsonl"
    records = [
        json.loads(line)
        for line in patterns_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    names = {record["name"] for record in records}
    assert {
        "Adaptive Fusion Mode",
        "One Write Owner",
        "Independent Challenge Before Execution",
        "Consensus Requires Evidence",
        "Fusion Budget Gate",
    } <= names


def test_mcp_get_patterns_returns_jsonl_content():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "get_patterns", "arguments": {}},
    }

    completed = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "trace_miner_server.py"), "--once"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    response = json.loads(completed.stdout)
    text = response["result"]["content"][0]["text"]
    first_record = json.loads(text.splitlines()[0])
    assert first_record["id"].startswith("PAT-")


def test_mcp_lists_fusion_tools():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    }

    completed = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "trace_miner_server.py"), "--once"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    response = json.loads(completed.stdout)
    names = {tool["name"] for tool in response["result"]["tools"]}
    assert {"get_fusion_protocol", "get_fusion_modes", "get_fusion_scorecard"} <= names


def test_mcp_get_fusion_scorecard_returns_content():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "get_fusion_scorecard", "arguments": {}},
    }

    completed = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "trace_miner_server.py"), "--once"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    response = json.loads(completed.stdout)
    assert "Trace Fusion Scorecard" in response["result"]["content"][0]["text"]
