#!/usr/bin/env python3
"""Require native agent review for meaningful repository changes."""

from __future__ import annotations

import json
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
    "home/dot_config/herdr/",
    "scripts/",
)

HIGH_RISK_FILES = {
    "AGENTS.md",
    "home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl",
    "home/dot_agents/agent-config.yaml",
    "home/dot_local/bin/common/executable_agent-fanout",
    "home/dot_local/bin/common/executable_herdr-agents",
    "home/dot_local/bin/common/executable_start-cognee-mcp",
    "home/dot_zshrc",
    "tests/install/common/lifecycle.bats",
}

HIGH_RISK_TOKENS = (
    "ccgate",
    "crit",
    "agmsg",
    "herdr",
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
AGENT_REVIEWERS = {
    "claude",
    "claude-code",
    "codex",
}
CRIT_DATA_REVIEW_SURFACE = "crit-data"
CRIT_DATA_SOURCE_FIELD = "review_source"
CRIT_DATA_REQUIRED_FIELDS = ("id", "body", "scope")
AGENT_REVIEW_OUTCOMES = {"approved", "addressed"}


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
    untracked = run_git(["ls-files", "--others", "--exclude-standard"], root)
    if untracked.returncode == 0:
        for path in untracked.stdout.splitlines():
            if path.startswith(IGNORED_PREFIXES):
                continue
            file_path = root / path
            if file_path.is_file():
                total += len(file_path.read_bytes().splitlines())
    return total


def is_low_risk_docs_only(paths: list[str]) -> bool:
    if not paths:
        return True
    return (
        all(path.endswith(LOW_RISK_SUFFIXES) for path in paths)
        and len(paths) < BROAD_DIFF_FILE_LIMIT
        and not any(high_risk_reason(path) for path in paths)
    )


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
    reasons: list[str] = []
    for path in paths:
        reason = high_risk_reason(path)
        if reason:
            reasons.append(reason)
            break

    if not reasons and is_low_risk_docs_only(paths):
        return []

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


def evidence_errors(root: Path, marker: str) -> list[str]:
    path = resolve_evidence_path(root)
    if path is None:
        return [f"{EVIDENCE_ENV} must point to a review receipt file"]
    if not path.exists():
        return [f"{EVIDENCE_ENV} file does not exist: {path}"]
    text = path.read_text()
    parsed_fields = {field: evidence_field(text, field) for field in REQUIRED_EVIDENCE_FIELDS}
    errors = [
        f"{EVIDENCE_ENV} file must include non-empty `{field}: ...`"
        for field, value in parsed_fields.items()
        if not value
    ]
    if "agent_self_review: true" in text:
        errors.append(f"{EVIDENCE_ENV} reviewer must not be bare agent self-attestation")
    reviewer = parsed_fields["reviewer"]
    if reviewer and is_agent_reviewer(reviewer):
        errors.extend(agent_review_errors(root, text, parsed_fields, marker))
    elif reviewer and marker == f"{NATIVE_REVIEWED_ENV}=1":
        errors.append(f"{NATIVE_REVIEWED_ENV}=1 requires an agent reviewer")
    elif reviewer and any(token in reviewer.lower() for token in SELF_REVIEWER_TOKENS):
        errors.append(f"{EVIDENCE_ENV} reviewer must not be bare agent self-attestation")
    return errors


def is_agent_reviewer(reviewer: str) -> bool:
    return reviewer.strip().lower() in AGENT_REVIEWERS


def agent_review_errors(root: Path, text: str, parsed_fields: dict[str, str | None], marker: str) -> list[str]:
    if marker != f"{NATIVE_REVIEWED_ENV}=1":
        return [f"{EVIDENCE_ENV} agent reviewer is only valid with {NATIVE_REVIEWED_ENV}=1"]

    errors: list[str] = []
    if parsed_fields["review_surface"] != CRIT_DATA_REVIEW_SURFACE:
        errors.append(f"{EVIDENCE_ENV} agent reviewer requires `review_surface: {CRIT_DATA_REVIEW_SURFACE}`")
    if parsed_fields["review_outcome"] not in AGENT_REVIEW_OUTCOMES:
        errors.append(f"{EVIDENCE_ENV} agent reviewer requires `review_outcome: approved` or `review_outcome: addressed`")
    source = evidence_field(text, CRIT_DATA_SOURCE_FIELD)
    if not source:
        errors.append(f"{EVIDENCE_ENV} agent reviewer requires non-empty `{CRIT_DATA_SOURCE_FIELD}: ...`")
    else:
        errors.extend(crit_data_errors(root, source))
    return errors


def crit_data_errors(root: Path, source: str) -> list[str]:
    path = Path(source)
    if not path.is_absolute():
        path = root / path

    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return [f"{CRIT_DATA_SOURCE_FIELD} must point to a repo-local JSON evidence file"]

    if not path.is_file():
        return [f"{CRIT_DATA_SOURCE_FIELD} JSON evidence file does not exist: {path}"]

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        return [f"{CRIT_DATA_SOURCE_FIELD} must be valid JSON: {error}"]

    if not isinstance(data, list) or not data:
        return [f"{CRIT_DATA_SOURCE_FIELD} JSON must be a non-empty Crit comment list"]

    errors: list[str] = []
    has_review_record = False
    for index, comment in enumerate(data):
        if not isinstance(comment, dict):
            errors.append(f"{CRIT_DATA_SOURCE_FIELD} comment {index} must be an object")
            continue
        for field in CRIT_DATA_REQUIRED_FIELDS:
            if not isinstance(comment.get(field), str) or not comment[field].strip():
                errors.append(f"{CRIT_DATA_SOURCE_FIELD} comment {index} requires non-empty string `{field}`")
        if comment.get("resolved") is not True:
            errors.append(f"{CRIT_DATA_SOURCE_FIELD} comment {index} must have `resolved: true`")
        scope = comment.get("scope")
        has_review_record |= scope == "review" or (
            scope in {"line", "file"} and isinstance(comment.get("path"), str) and bool(comment["path"].strip())
        )
    if not has_review_record:
        errors.append(f"{CRIT_DATA_SOURCE_FIELD} requires a review-scope or path-bound line/file comment")
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
        errors = evidence_errors(root, marker)
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
    print("Use the active agent's review path, not a browser by default:")
    print("- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.")
    print("- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.")
    print("- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.")
    print("Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.")
    print("For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.")
    print("Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.")
    print("This local evidence is process evidence, not reviewer authentication.")
    print("Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.")
    print("After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
