#!/usr/bin/env python3
"""Deny orchestrator/worker Bash commands that violate agmsg-orchestration rules.

PreToolUse command hooks receive JSON on stdin with (at least) `tool_name`,
`tool_input`, `session_id`, and `cwd`; exit 2 with a stderr message denies the
call, exit 0 allows it, and a `hookSpecificOutput.permissionDecision` JSON
payload on stdout is also accepted for an advisory allow-with-warning.
See: https://docs.claude.com/en/docs/claude-code/hooks (PreToolUse).

Role comes from the HERDR_AGENTS_ROLE env var herdr-agents sets on each pane
it creates (orchestrator|worker); a missing value is treated as "unknown" and
enforces none of the role-specific rules below. An operator can bypass one
rule for one command with GUARDRAILS_ALLOW=G1,G3 (comma-separated ids); the
bypass is logged to stderr.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

_WORKTREE_RE = re.compile(r"\.claude/worktrees/([\w.-]+)")
_WRITE_PATTERNS = [
    re.compile(r"\bcd\b"),
    re.compile(r">"),
    re.compile(r"\btee\b"),
    re.compile(r"\b(?:cp|mv|rm)\b"),
    re.compile(r"git\s+-C\b"),
    re.compile(r"\bsed\s+-i\b"),
]
_MERGE_RE = re.compile(r"gh\s+pr\s+merge\b")
_MERGE_NUMBER_RE = re.compile(r"gh\s+pr\s+merge\s+(\d+)")
_UPGRADE_RE = re.compile(r"\bmake\s+upgrade\b|scripts/upgrade-tools\.sh")
_BROAD_SEARCH_RE = re.compile(r"\brg\b|\bgrep\b[^\n]*-r\b|\bfind\b[^\n]*-name")
_SCOPED_RE = re.compile(r"\.orchestration|\.agents")


def check_g1(command: str, cwd: str) -> str | None:
    if re.search(
        r"herdr\s+(agent\s+list|pane\s+list|pane\s+peek|agent\s+explain)\b", command
    ):
        return (
            "G1 no-status-inference: do not infer worker state from herdr agent/pane "
            "commands; use AGMSG-PING/PONG — completion arrives as AGMSG-RESULT."
        )
    return None


def check_g2(command: str, cwd: str) -> str | None:
    if "agmsg/scripts/send.sh" in command and "agmsg-dispatch" not in command:
        return (
            "G2 no-bare-send: do not call agmsg/scripts/send.sh directly; use "
            "agmsg-dispatch (or the upstream poke after T19)."
        )
    return None


def check_g3(command: str, cwd: str) -> str | None:
    targets = [
        name for name in _WORKTREE_RE.findall(command) if name != "orchestrator-review"
    ]
    if not targets:
        return None
    if any(pattern.search(command) for pattern in _WRITE_PATTERNS):
        # ponytail: regex/token heuristic, not a shell AST — bypassable by deliberate
        # obfuscation; upgrade path is shlex-based argv inspection if that becomes a
        # real incident rather than a hypothetical one.
        return (
            "G3 worker-tree-isolation: do not cd/write into a worker's worktree from "
            "the orchestrator; reads (git show/cat/grep/diff) are fine, cd/writes are not."
        )
    return None


def check_g4(command: str, cwd: str) -> str | None:
    if not _MERGE_RE.search(command):
        return None
    number_match = _MERGE_NUMBER_RE.search(command)
    if not number_match:
        return "G4 merge-gate: gh pr merge requires an explicit PR number."
    number = number_match.group(1)
    root = Path(cwd) if cwd else Path.cwd()
    validation_dir = root / ".orchestration" / "validation"
    feedback_files = (
        sorted(validation_dir.glob("*-pr-feedback*.json"))
        if validation_dir.is_dir()
        else []
    )
    needles = (f'"number": {number}', f'"number":{number}', f"pr={number}")
    has_feedback = any(
        any(needle in feedback_file.read_text() for needle in needles)
        for feedback_file in feedback_files
    )
    receipt = (
        root / ".agents" / "worklog" / "claude" / "crit" / f"pr-{number}-receipt.md"
    )
    if not has_feedback or not receipt.exists():
        return (
            f"G4 merge-gate: PR #{number} is missing pr-feedback validation "
            f"(.orchestration/validation/*-pr-feedback*.json) and/or the crit receipt "
            f"({receipt})."
        )
    if "--delete-branch" in command:
        head = _resolve_pr_head(number, root)
        if head:
            worktree = _worktree_checked_out(head, root)
            if worktree:
                return (
                    f"G4 merge-gate: --delete-branch would remove branch {head!r} still "
                    f"checked out at worktree {worktree}."
                )
    return None


def _resolve_pr_head(number: str, cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["gh", "pr", "view", number, "--json", "headRefName", "-q", ".headRefName"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip()


def _worktree_checked_out(branch: str, cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    current_path = None
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            current_path = line[len("worktree ") :]
        elif line.startswith("branch ") and line.endswith(f"refs/heads/{branch}"):
            return current_path
    return None


def check_g5(command: str, cwd: str) -> str | None:
    if _UPGRADE_RE.search(command):
        return (
            "G5 no-make-upgrade-in-tasks: make upgrade/scripts/upgrade-tools.sh is "
            "operator-run at a session boundary in the canonical clone."
        )
    return None


def check_g6(command: str) -> str | None:
    if _BROAD_SEARCH_RE.search(command) and not _SCOPED_RE.search(command):
        return (
            "G6 no-self-exploration: broad repo-root search; delegate to "
            "express-explorer instead."
        )
    return None


RULES: list[tuple[str, str, object]] = [
    ("G1", "orchestrator", check_g1),
    ("G2", "orchestrator", check_g2),
    ("G3", "orchestrator", check_g3),
    ("G4", "orchestrator", check_g4),
    ("G5", "worker", check_g5),
]


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        print(f"failed to parse Claude hook input: {error}", file=sys.stderr)
        return 0

    if payload.get("tool_name") != "Bash":
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    command = tool_input.get("command")
    if not isinstance(command, str) or not command:
        return 0

    cwd = payload.get("cwd") or "."
    role = os.environ.get("HERDR_AGENTS_ROLE", "unknown")
    override = {
        rule_id
        for rule_id in os.environ.get("GUARDRAILS_ALLOW", "").split(",")
        if rule_id
    }

    for rule_id, required_role, check in RULES:
        if role != required_role:
            continue
        if rule_id in override:
            print(f"GUARDRAILS_ALLOW override used for {rule_id}", file=sys.stderr)
            continue
        reason = check(command, cwd)
        if reason:
            print(reason, file=sys.stderr)
            return 2

    if role == "orchestrator" and "G6" not in override:
        warning = check_g6(command)
        if warning:
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "allow",
                            "permissionDecisionReason": warning,
                        }
                    }
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
