import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import changed_files, is_git_repo, load_ledger, read_event, workspace_from, write_json


RESOLVED_RISK_STATES = {"resolved", "accepted", "not_applicable", "deferred_with_reason"}


def _ledger_has_validation(ledger: dict) -> bool:
    validations = ledger.get("validation", [])
    if not isinstance(validations, list):
        return False
    for item in validations:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "")).lower()
        if status in {"pass", "passed", "skipped_with_reason", "blocked_with_reason"}:
            return True
    return False


def _unresolved_risks(ledger: dict) -> list[str]:
    risks = ledger.get("risks", [])
    unresolved = []
    if not isinstance(risks, list):
        return ["risks field is not a list"]
    for risk in risks:
        if not isinstance(risk, dict):
            unresolved.append("malformed risk entry")
            continue
        status = str(risk.get("status", "")).lower()
        if status not in RESOLVED_RISK_STATES:
            unresolved.append(str(risk.get("id") or risk.get("description") or "unnamed risk"))
    return unresolved


def evaluate_stop(event: dict, workspace=None) -> dict:
    if event.get("stop_hook_active"):
        return {"action": "allow", "reason": "stop guard already continued once"}

    workspace_path = workspace_from(event, workspace)
    if not is_git_repo(workspace_path):
        return {
            "action": "allow",
            "reason": "workspace is not a git repository; changed-file proof is unavailable, so the stop guard will not block",
        }

    changes = changed_files(workspace_path)
    if not changes:
        return {"action": "allow", "reason": "no changed-file signal detected"}

    ledger, ledger_error = load_ledger(workspace_path)
    if ledger_error:
        return {
            "action": "block",
            "reason": (
                f"Trace Miner final guard found changed files but {ledger_error}. "
                "Create .trace-miner/ledger.json with requirements, validation, and risks before finalizing."
            ),
        }

    if not _ledger_has_validation(ledger):
        return {
            "action": "block",
            "reason": "Trace Miner final guard found changed files but no passing or justified validation entry in the ledger.",
        }

    unresolved = _unresolved_risks(ledger)
    if unresolved:
        return {
            "action": "block",
            "reason": "Trace Miner final guard found unresolved risks: " + ", ".join(unresolved[:5]),
        }

    return {"action": "allow", "reason": "ledger, validation, and risks are closed"}


def to_hook_output(result: dict) -> dict:
    if result["action"] == "block":
        return {"decision": "block", "reason": result["reason"]}
    return {"continue": True}


def main() -> int:
    write_json(to_hook_output(evaluate_stop(read_event())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
