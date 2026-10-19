#!/usr/bin/env python3
"""Bind permission-surface changes to an exact user-approved decision row."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tomllib

import yaml


def git(*args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return subprocess.check_output(["/usr/bin/git", *args], text=True, stderr=subprocess.PIPE, env=env)


def trusted_ledger(selected: Path | None) -> Path:
    anchors = re.findall(
        r"^orchestrator_checkout: (~/[^\s\x00]+)$", (Path.home() / ".agents/agent-config.yaml").read_text(), re.M
    )
    if len(anchors) != 1:
        raise ValueError("missing or ambiguous checkout anchor")
    anchor = Path(anchors[0]).expanduser().resolve(strict=True)
    top = Path(git("rev-parse", "--show-toplevel").strip()).resolve(strict=True)
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()).resolve(strict=True)
    if top != anchor or common != top / ".git" or not (top / ".git").is_dir() or (top / ".git").is_symlink():
        raise ValueError("requires canonical primary checkout")
    boot = f"{Path.home()}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
    env = dict(HOME=str(Path.home()), PATH=boot)
    found = subprocess.run(
        ["/usr/bin/env", "-i", *[f"{k}={v}" for k, v in env.items()], "mise", "which", "gh"],
        cwd=anchor,
        text=True,
        capture_output=True,
    )
    gh = found.stdout.strip() if found.returncode == 0 else shutil.which("gh", path=boot)
    if not gh or not gh.startswith("/") or "/shims/" in gh:
        raise ValueError("no trusted gh binary")
    actual = subprocess.check_output(
        [gh, "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], cwd=anchor, env=env, text=True
    ).strip()
    origin = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?",
        git("remote", "get-url", "origin").strip(),
    )
    if not origin or origin[1].lower() != actual.lower():
        raise ValueError("repository identity mismatch")
    ledger = (selected if selected is not None else anchor / ".orchestration/decisions.tsv").resolve()
    for entry in git("worktree", "list", "--porcelain", "-z").split("\0"):
        if entry.startswith("worktree "):
            tree = Path(entry[9:]).resolve()
            if tree != anchor and any(p.exists() and p.samefile(tree) for p in (ledger, *ledger.parents)):
                raise ValueError("decision ledger inside PR worktree")
    return ledger


def surface(ref: str, manifest_path: str) -> dict:
    sha = git("rev-parse", "--verify", "--end-of-options", ref + "^{commit}").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("invalid revision")
    manifest = yaml.safe_load(git("show", f"{sha}:{manifest_path}"))
    claude, codex = manifest.get("claude", {}), manifest.get("codex", {})
    hooks = claude.get("hooks", {})
    codex_keys = ("approval_policy", "sandbox_mode", "sandbox_workspace_write")
    result = {
        "orchestrator_checkout": manifest.get("orchestrator_checkout"),
        "claude": {
            "permissions": claude.get("permissions"),
            "sandbox": claude.get("sandbox"),
            "hooks": {k: v for k, v in hooks.items() if k in {"gh_merge_gate_hook", "enforce_uv_hook", "PreToolUse"}},
        },
        "codex": {k: codex.get(k) for k in codex_keys},
        "rendered": {},
    }
    for suffix, parser in (("json", json.loads), ("toml", tomllib.loads)):
        name = "claude-settings" if suffix == "json" else "codex-config"
        text = git("show", f"{sha}:home/.chezmoitemplates/{name}-managed.{suffix}")
        for os_name in ("darwin", "linux"):
            rendered = re.sub(r"\{\{/\*.*?\*/\}\}", "", text, flags=re.DOTALL)
            rendered = re.sub(
                r'\{\{ if eq \.chezmoi\.os "darwin" \}\}(.*?)\{\{ else \}\}(.*?)\{\{ end \}\}',
                lambda m: m[1] if os_name == "darwin" else m[2],
                rendered,
                flags=re.DOTALL,
            )
            data = parser(rendered)
            result["rendered"][f"{name}.{os_name}"] = {
                k: data.get(k) for k in ("permissions", "sandbox", "hooks", *codex_keys)
            }
    return result


def changed_paths(before: object, after: object, path: str = "") -> list[str]:
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        return [
            p
            for k in sorted(before.keys() | after.keys())
            for p in changed_paths(before.get(k), after.get(k), f"{path}.{k}".lstrip("."))
        ]
    return [path]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--manifest", default="home/dot_agents/agent-config.yaml")
    args = parser.parse_args()
    path = PurePosixPath(args.manifest)
    if path.is_absolute() or ".." in path.parts:
        parser.error("--manifest must name a repository-relative file")
    before, after = (surface(ref, args.manifest) for ref in (args.base, args.head))
    canonical = [json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n" for x in (before, after)]
    if canonical[0] == canonical[1]:
        print("permission surface: unchanged")
        return 0
    diff = "".join(difflib.unified_diff([canonical[0]], [canonical[1]], fromfile="base", tofile="head"))
    digest = hashlib.sha256(diff.encode()).hexdigest()
    print(diff, end="")
    print(f"permission diff sha256: {digest}")
    required = {"scope=permission", "approved_by=user", f"diff_sha256={digest}"}
    ledger = trusted_ledger(args.decisions)
    if ledger.is_file():
        with ledger.open(newline="") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                if re.fullmatch(r"D-[A-Za-z0-9_.-]+", row.get("id", "")) and any(
                    required <= set((row.get(column) or "").split()) for column in ("basis", "what")
                ):
                    print(f"permission decision: {row['id']}")
                    return 0
    for path in changed_paths(before, after):
        print(f"unapproved permission change: {path}")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, TypeError, AttributeError, OSError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"permission surface unreadable: {type(error).__name__}")
        raise SystemExit(1) from None
