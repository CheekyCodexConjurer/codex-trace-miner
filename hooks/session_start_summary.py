import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import changed_files, is_git_repo, load_ledger, read_event, workspace_from, write_json


def build_summary(event: dict) -> str:
    workspace = workspace_from(event)
    ledger, ledger_error = load_ledger(workspace)
    git_state = "git repository" if is_git_repo(workspace) else "not a git repository"
    changes = changed_files(workspace)

    if ledger:
        req_count = len(ledger.get("requirements", []))
        validation_count = len(ledger.get("validation", []))
        risk_count = len(ledger.get("risks", []))
        ledger_state = f"ledger present: {req_count} requirements, {validation_count} validations, {risk_count} risks"
    else:
        ledger_state = ledger_error or "ledger not checked"

    change_state = "no git changes detected" if not changes else f"{len(changes)} change signal(s) detected"
    return (
        "Trace Miner active. Use public trace sources only as behavioral evidence; "
        "do not copy leaked prompts or raw chain-of-thought. "
        f"Workspace is {git_state}; {ledger_state}; {change_state}. "
        "Tool route: CodeGraph for repo map/impact, Serena for precise code understanding, "
        "Context7 for current third-party docs. "
        "For meaningful changes, maintain .trace-miner/ledger.json and run explicit validation."
    )


def main() -> int:
    context = build_summary(read_event())
    write_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
