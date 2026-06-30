#!/usr/bin/env python3
"""Require native agent review for meaningful repository changes."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REVIEWED_ENV = "CRIT_REVIEWED"
NATIVE_REVIEWED_ENV = "AGENT_REVIEWED"
EVIDENCE_ENV = "REVIEW_EVIDENCE"
DISABLE_ENV = "CRIT_REVIEW"
BROAD_DIFF_FILE_LIMIT = 5
BROAD_DIFF_LINE_LIMIT = 200

IGNORED_PREFIXES = (
    ".agents/worklog/",
)

HIGH_RISK_PREFIXES = (
    ".codex/",
    ".claude/",
    "home/dot_agents/plugins/",
    "home/dot_agents/skills/",
    "home/dot_claude/",
    "home/dot_codex/",
    "home/dot_config/claude/",
    "home/dot_config/codex/",
    "scripts/",
)

HIGH_RISK_FILES = {
    "AGENTS.md",
    "README.md",
    "home/dot_agents/agent-config.yaml",
    "home/dot_agents/hermes-config-base.yaml",
    "tests/install/common/lifecycle.bats",
}

HIGH_RISK_TOKENS = (
    "ccgate",
    "crit",
    "hook",
    "hooks",
    "plugin",
    "permission",
    "ponytail",
    "superpowers",
)

LOW_RISK_SUFFIXES = (
    ".md",
    ".txt",
)

REQUIRED_EVIDENCE_FIELDS = (
    "review_surface",
    "reviewer",
    "review_outcome",
)
SELF_REVIEWER_TOKENS = (
    "agent",
    "claude",
    "codex",
    "gpt",
    "self",
)


def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_root() -> Path:
    result = run_git(["rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        print("Review guard skipped: not inside a git repository.")
        raise SystemExit(0)
    return Path(result.stdout.strip())


def changed_paths(root: Path) -> list[str]:
    paths: set[str] = set()
    commands = (
        ["diff", "--name-only"],
        ["diff", "--cached", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    )
    for command in commands:
        result = run_git(command, root)
        if result.returncode == 0:
            paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(path for path in paths if not path.startswith(IGNORED_PREFIXES))


def numstat_line_count(root: Path) -> int:
    total = 0
    for command in (["diff", "--numstat"], ["diff", "--cached", "--numstat"]):
        result = run_git(command, root)
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            fields = line.split("\t")
            if len(fields) < 3 or fields[2].startswith(IGNORED_PREFIXES):
                continue
            for count in fields[:2]:
                if count.isdigit():
                    total += int(count)
    return total


def is_low_risk_docs_only(paths: list[str]) -> bool:
    if not paths:
        return True
    return all(path.endswith(LOW_RISK_SUFFIXES) for path in paths) and len(paths) < BROAD_DIFF_FILE_LIMIT


def high_risk_reason(path: str) -> str | None:
    if path in HIGH_RISK_FILES:
        return f"tracked policy/config file changed: {path}"
    if path.startswith(HIGH_RISK_PREFIXES):
        return f"agent lifecycle path changed: {path}"
    path_parts = Path(path).parts
    token_source = " ".join(path_parts).lower().replace("_", "-")
    if any(token in token_source for token in HIGH_RISK_TOKENS):
        return f"review-sensitive path changed: {path}"
    return None


def review_reasons(root: Path, paths: list[str]) -> list[str]:
    if is_low_risk_docs_only(paths):
        return []

    reasons: list[str] = []
    for path in paths:
        reason = high_risk_reason(path)
        if reason:
            reasons.append(reason)
            break

    if len(paths) >= BROAD_DIFF_FILE_LIMIT:
        reasons.append(f"broad diff touches {len(paths)} files")

    line_count = numstat_line_count(root)
    if line_count >= BROAD_DIFF_LINE_LIMIT:
        reasons.append(f"broad diff changes {line_count} lines")

    return reasons


def resolve_evidence_path(root: Path) -> Path | None:
    evidence = os.environ.get(EVIDENCE_ENV, "").strip()
    if not evidence:
        return None
    path = Path(evidence)
    if not path.is_absolute():
        path = root / path
    return path


def evidence_errors(root: Path) -> list[str]:
    path = resolve_evidence_path(root)
    if path is None:
        return [f"{EVIDENCE_ENV} must point to a review receipt file"]
    if not path.exists():
        return [f"{EVIDENCE_ENV} file does not exist: {path}"]
    text = path.read_text()
    errors = [
        f"{EVIDENCE_ENV} file must include `{field}: ...`"
        for field in REQUIRED_EVIDENCE_FIELDS
        if f"{field}:" not in text
    ]
    if "agent_self_review: true" in text:
        errors.append(f"{EVIDENCE_ENV} must not mark agent_self_review: true")
    reviewer = evidence_field(text, "reviewer")
    if reviewer and any(token in reviewer.lower() for token in SELF_REVIEWER_TOKENS):
        errors.append(f"{EVIDENCE_ENV} reviewer must identify a human or external reviewer, not agent self-review")
    return errors


def evidence_field(text: str, field: str) -> str | None:
    prefix = f"{field}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def review_marker() -> str | None:
    if os.environ.get(REVIEWED_ENV) == "1":
        return f"{REVIEWED_ENV}=1"
    if os.environ.get(NATIVE_REVIEWED_ENV) == "1":
        return f"{NATIVE_REVIEWED_ENV}=1"
    return None


def main() -> None:
    if os.environ.get(DISABLE_ENV) == "off":
        print("Review guard disabled by CRIT_REVIEW=off.")
        return

    root = git_root()
    paths = changed_paths(root)
    reasons = review_reasons(root, paths)
    if not reasons:
        print("Review not required: no meaningful review trigger found.")
        return

    marker = review_marker()
    if marker:
        errors = evidence_errors(root)
        if not errors:
            print(f"Review requirement satisfied by {marker} with {EVIDENCE_ENV}.")
            return
        print(f"{marker} requires review evidence before completion.")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Native agent review required before completion.")
    for reason in reasons:
        print(f"- {reason}")
    print("Use the active agent's native review surface, not a browser by default:")
    print("- Codex: use `/diff` or `/review`; in the Codex app, use the Review pane with inline comments.")
    print("- Claude Code: use the IDE/desktop inline diff or plan review surface; in terminal mode, show the diff in the conversation.")
    print("Use Crit's browser review only when the user explicitly asks for Crit web UI or native review is unavailable.")
    print("Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.")
    print("The reviewer must be a human or external reviewer, not this agent's self-review.")
    print("After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
