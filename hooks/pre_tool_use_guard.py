import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import read_event, workspace_from, write_json


DENY_PATTERNS = [
    (r"\brm\s+(-[^\s]*r[^\s]*f|-[^\s]*f[^\s]*r)\b", "destructive recursive removal"),
    (r"\bRemove-Item\b.*\b-Recurse\b", "destructive recursive removal"),
    (r"\bgit\s+reset\s+--hard\b", "destructive git reset"),
    (r"\bgit\s+clean\b.*\s-[^\s]*[fdx]", "destructive git clean"),
    (r"\bgit\s+(checkout|restore)\b.*\s(--\s*)?(\.|\*)\s*$", "broad destructive git restore"),
    (r"\bgit\s+push\b.*--force", "force push"),
    (r"\bgit\s+(rebase|merge|stash)\b", "history or state changing git command"),
    (r"\bgit\s+add\s+(\.|-A|--all)\b", "broad staging command"),
    (r"\b(curl|wget)\b.*\|\s*(sh|bash|zsh|pwsh|powershell)\b", "remote script execution"),
    (r"\b(iwr|Invoke-WebRequest)\b.*\|\s*(iex|Invoke-Expression)\b", "remote PowerShell execution"),
    (r"\b(npm|pnpm|yarn)\s+publish\b", "package publishing"),
    (r"\b(twine|python\s+-m\s+twine)\s+upload\b", "package publishing"),
    (r"\bterraform\s+(apply|destroy)\b", "cloud infrastructure mutation"),
    (r"\bkubectl\s+(delete|apply|replace|scale|rollout)\b", "cluster mutation"),
    (r"\b(drop\s+database|truncate\s+table|delete\s+from)\b", "database mutation"),
    (r"\b(live|prod|production)\b.*\b(order|trade|execute|deploy|destroy|delete)\b", "production or live trading risk"),
    (r"\*\*\*\s+Delete File:", "patch deletes a file"),
]

SECRET_PATTERNS = [
    (r"(^|\s)(cat|type|Get-Content)\s+.*(\.env|id_rsa|id_ed25519|credentials|secrets?)\b", "secret file read"),
    (r"\b(printenv|Get-ChildItem\s+Env:|env)\b.*(KEY|TOKEN|SECRET|PASSWORD)", "secret environment exposure"),
]


def _command_from(event: dict) -> str:
    tool_input = event.get("tool_input") or {}
    if isinstance(tool_input, dict):
        for key in ("command", "cmd", "script"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def evaluate(event: dict, workspace: Path | None = None) -> dict:
    command = _command_from(event)
    if not command:
        return {"action": "allow", "reason": "no shell command found"}

    checks = DENY_PATTERNS + SECRET_PATTERNS
    for pattern, reason in checks:
        if re.search(pattern, command, flags=re.IGNORECASE | re.DOTALL):
            return {
                "action": "deny",
                "reason": f"Blocked destructive or risky command: {reason}. Ask the user for an explicit safer path.",
            }

    workspace_path = workspace_from(event, workspace)
    if re.search(r"\b(Remove-Item|rm|del|erase|move|mv|cp|copy)\b", command, re.IGNORECASE):
        if ".." in command and str(workspace_path) not in command:
            return {
                "action": "deny",
                "reason": "Blocked file mutation with parent-directory traversal outside the proven workspace.",
            }

    return {"action": "allow", "reason": "no risky pattern matched"}


def to_hook_output(result: dict) -> dict:
    if result["action"] == "deny":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": result["reason"],
            }
        }
    return {}


def main() -> int:
    result = evaluate(read_event())
    output = to_hook_output(result)
    if output:
        write_json(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
