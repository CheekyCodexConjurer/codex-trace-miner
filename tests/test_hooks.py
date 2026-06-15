import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_pre_tool_guard_denies_destructive_command():
    guard = load_module("hooks/pre_tool_use_guard.py")
    event = {
        "tool_name": "Bash",
        "tool_input": {"command": "git reset --hard HEAD"},
    }

    result = guard.evaluate(event, workspace=ROOT)

    assert result["action"] == "deny"
    assert "destructive" in result["reason"].lower()


def test_pre_tool_guard_allows_read_only_command():
    guard = load_module("hooks/pre_tool_use_guard.py")
    event = {
        "tool_name": "Bash",
        "tool_input": {"command": "rg --files"},
    }

    result = guard.evaluate(event, workspace=ROOT)

    assert result["action"] == "allow"


def test_pre_tool_guard_allows_specific_commit_command():
    guard = load_module("hooks/pre_tool_use_guard.py")
    event = {
        "tool_name": "Bash",
        "tool_input": {"command": "git commit -m \"docs: add trace miner scaffold\""},
    }

    result = guard.evaluate(event, workspace=ROOT)

    assert result["action"] == "allow"


def test_stop_guard_blocks_dirty_work_without_ledger(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "block"
    assert "ledger" in result["reason"].lower()


def test_stop_guard_allows_non_git_workspace_without_change_proof(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    (workspace / "README.md").write_text("existing fixture\n", encoding="utf-8")

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "allow"
    assert "git" in result["reason"].lower()


def test_stop_guard_allows_documented_clean_stop(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    ledger = workspace / ".trace-miner" / "ledger.json"
    ledger.parent.mkdir()
    ledger.write_text(
        json.dumps(
            {
                "requirements": [{"id": "REQ-1", "status": "done"}],
                "validation": [{"command": "python -m pytest", "status": "pass"}],
                "risks": [{"id": "R-1", "status": "resolved"}],
            }
        ),
        encoding="utf-8",
    )

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "allow"


def test_mcp_server_lists_read_only_tools():
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

    assert completed.returncode == 0
    response = json.loads(completed.stdout)
    names = {tool["name"] for tool in response["result"]["tools"]}
    assert {"get_source_index", "get_eval_scorecard"} <= names


def test_mcp_config_command_starts_server():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    }
    config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = config["mcp_servers"]["trace-miner-context"]
    args = [
        arg.replace("${PLUGIN_ROOT}", str(ROOT))
        for arg in server.get("args", [])
    ]
    env = {
        **server.get("env", {}),
        "TRACE_MINER_ROOT": str(ROOT),
    }
    env = {key: value.replace("${PLUGIN_ROOT}", str(ROOT)) for key, value in env.items()}

    completed = subprocess.run(
        [server["command"], *args, "--once"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, **env},
    )

    assert completed.returncode == 0, completed.stderr
    response = json.loads(completed.stdout)
    names = {tool["name"] for tool in response["result"]["tools"]}
    assert "get_source_index" in names
