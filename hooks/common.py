import json
import os
import subprocess
import sys
from pathlib import Path


RISK_LEDGER = Path(".trace-miner") / "ledger.json"


def read_event() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def write_json(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")))


def workspace_from(event: dict, fallback: Path | None = None) -> Path:
    if fallback is not None:
        return fallback.resolve()
    cwd = event.get("cwd") or os.environ.get("PWD") or os.getcwd()
    return Path(cwd).resolve()


def run_git(workspace: Path, args: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout.strip()


def is_git_repo(workspace: Path) -> bool:
    code, output = run_git(workspace, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and output.lower() == "true"


def changed_files(workspace: Path) -> list[str]:
    if is_git_repo(workspace):
        code, output = run_git(workspace, ["status", "--short"])
        if code != 0 or not output:
            return []
        return [line.strip() for line in output.splitlines() if line.strip()]

    return []


def load_ledger(workspace: Path) -> tuple[dict | None, str | None]:
    path = workspace / RISK_LEDGER
    if not path.exists():
        return None, f"missing ledger at {RISK_LEDGER.as_posix()}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as exc:
        return None, f"invalid ledger JSON: {exc}"
