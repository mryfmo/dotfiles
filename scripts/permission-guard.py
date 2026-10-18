#!/usr/bin/env python3
"""Bind permission-surface changes to an exact user-approved decision row."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tomllib

import yaml


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE)


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
    parser.add_argument("--decisions", type=Path, default=Path(".orchestration/decisions.tsv"))
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
    if args.decisions.is_file():
        with args.decisions.open(newline="") as stream:
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
