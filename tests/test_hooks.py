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


def test_pre_tool_guard_denies_broad_staging_commands():
    guard = load_module("hooks/pre_tool_use_guard.py")

    for command in ("git add .", "git add -- .", "git add -A", "git add --all", "git stage ."):
        result = guard.evaluate(
            {"tool_name": "Bash", "tool_input": {"command": command}},
            workspace=ROOT,
        )
        assert result["action"] == "deny", command
        assert "broad staging" in result["reason"].lower()


def test_pre_tool_guard_denies_recursive_removal_commands():
    guard = load_module("hooks/pre_tool_use_guard.py")

    commands = (
        "Remove-Item .\\build -Recurse -Force",
        "rm -rf build",
        "rm -fr build",
        "rm -r build",
        "rm -Recurse -Force build",
        "rmdir /s /q build",
        "rmdir build -Recurse",
    )
    for command in commands:
        result = guard.evaluate(
            {"tool_name": "Bash", "tool_input": {"command": command}},
            workspace=ROOT,
        )
        assert result["action"] == "deny", command
        assert "recursive removal" in result["reason"].lower()


def test_pre_tool_guard_denies_structured_patch_file_delete():
    guard = load_module("hooks/pre_tool_use_guard.py")
    event = {
        "tool_name": "apply_patch",
        "tool_input": {"patch": "*** Begin Patch\n*** Delete File: README.md\n*** End Patch\n"},
    }

    result = guard.evaluate(event, workspace=ROOT)

    assert result["action"] == "deny"
    assert "patch deletes" in result["reason"].lower()


def test_stop_guard_blocks_dirty_work_without_ledger(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "block"
    assert "ledger" in result["reason"].lower()


def test_stop_guard_blocks_dirty_work_with_stale_ledger(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")
    ledger = workspace / ".trace-miner" / "ledger.json"
    ledger.parent.mkdir()
    ledger.write_text(
        json.dumps(
            {
                "requirements": [{"id": "REQ-1", "status": "done"}],
                "validation": [{"command": "python -m pytest", "status": "pass"}],
                "risks": [{"id": "R-1", "status": "resolved"}],
                "workspace_state": {"changed_files": [" M old-file.md"]},
            }
        ),
        encoding="utf-8",
    )

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "block"
    assert "workspace_state.changed_files" in result["reason"]


def test_stop_guard_blocks_dirty_work_without_change_snapshot(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")
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

    assert result["action"] == "block"
    assert "workspace_state.changed_files" in result["reason"]


def test_stop_guard_blocks_dirty_work_with_invalid_ledger(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")
    ledger = workspace / ".trace-miner" / "ledger.json"
    ledger.parent.mkdir()
    ledger.write_text("{not-json", encoding="utf-8")

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "block"
    assert "invalid ledger" in result["reason"].lower()


def test_stop_guard_allows_dirty_work_with_current_ledger(tmp_path):
    guard = load_module("hooks/stop_guard.py")
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
    (workspace / "README.md").write_text("changed\n", encoding="utf-8")
    ledger = workspace / ".trace-miner" / "ledger.json"
    ledger.parent.mkdir()
    ledger.write_text("{}", encoding="utf-8")
    current_changes = guard.changed_files(workspace)
    ledger.write_text(
        json.dumps(
            {
                "requirements": [{"id": "REQ-1", "status": "done"}],
                "validation": [{"command": "python -m pytest", "status": "pass"}],
                "risks": [{"id": "R-1", "status": "resolved"}],
                "workspace_state": {"changed_files": current_changes},
            }
        ),
        encoding="utf-8",
    )

    result = guard.evaluate_stop({"stop_hook_active": False}, workspace=workspace)

    assert result["action"] == "allow"


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
    assert {
        "get_source_index",
        "get_eval_scorecard",
        "get_patterns",
        "get_tool_automation",
        "get_fusion_protocol",
        "get_fusion_modes",
        "get_fusion_scorecard",
    } <= names


def test_mcp_config_command_starts_server():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    }
    config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = config["mcp_servers"]["fable-mode"]
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
    assert "get_patterns" in names
    assert "get_tool_automation" in names
    assert "get_fusion_protocol" in names
    assert "get_fusion_modes" in names
    assert "get_fusion_scorecard" in names


def test_mcp_config_uses_fable_mode_name():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
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
    assert response["result"]["serverInfo"]["name"] == "Fable Mode"


def test_mcp_parse_error_returns_json_rpc_error():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "trace_miner_server.py"), "--once"],
        input="not-json\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    response = json.loads(completed.stdout)
    assert response["error"]["code"] == -32700


def test_mcp_non_object_request_returns_invalid_request():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "trace_miner_server.py"), "--once"],
        input="[]\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    response = json.loads(completed.stdout)
    assert response["error"]["code"] == -32600
