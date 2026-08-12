#!/usr/bin/env python3
"""Repeatable release validation for CompactionDB.

The validator intentionally uses only the Python standard library. It does not
modify the source tree except when --report-json is explicitly supplied.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import platform
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
MIN_TESTS = 35


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str
    duration_seconds: float
    required: bool = True


class ValidationFailure(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a CompactionDB release tree")
    parser.add_argument("--report-json", help="write the full machine-readable report to this path")
    parser.add_argument("--skip-tests", action="store_true", help="skip the unittest suite")
    return parser.parse_args()


def run_check(
    results: list[CheckResult],
    name: str,
    function: Callable[[], str],
    *,
    required: bool = True,
) -> None:
    started = time.monotonic()
    try:
        detail = function()
        status = "pass"
    except Exception as exc:  # validation must report all checks, not stop at the first one
        detail = f"{type(exc).__name__}: {exc}"
        status = "fail" if required else "skip"
    results.append(
        CheckResult(
            name=name,
            status=status,
            detail=detail,
            duration_seconds=round(time.monotonic() - started, 3),
            required=required,
        )
    )


def check_python() -> str:
    if sys.version_info < (3, 10):
        raise ValidationFailure(f"Python 3.10+ required, found {platform.python_version()}")
    return f"Python {platform.python_version()} ({sys.executable})"


def source_python_files() -> list[Path]:
    ignored = {".git", ".venv", "venv"}
    return sorted(
        path
        for path in ROOT.rglob("*.py")
        if not any(part in ignored or part == "__pycache__" for part in path.parts)
    )


def check_syntax() -> str:
    files = source_python_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=str(path))
    return f"AST parsed {len(files)} Python files"


def check_json() -> str:
    files = sorted(ROOT.rglob("*.json"))
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))
    return f"parsed {len(files)} JSON files"


def _settings_documents() -> list[tuple[Path, dict[str, Any]]]:
    documents: list[tuple[Path, dict[str, Any]]] = []
    for path in (
        ROOT / ".claude" / "settings.json",
        ROOT / ".claude" / "settings.fragment.json",
        ROOT / ".claude" / "settings.windows.example.json",
    ):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValidationFailure(f"settings root must be an object: {path}")
        documents.append((path, value))
    return documents


def check_hook_settings() -> str:
    allowed_events = {
        "SessionStart",
        "UserPromptSubmit",
        "PostToolUse",
        "PostToolUseFailure",
        "PermissionDenied",
        "PreCompact",
        "PostCompact",
        "Stop",
        "StopFailure",
        "SubagentStart",
        "SubagentStop",
        "TaskCreated",
        "TaskCompleted",
        "SessionEnd",
    }
    handler_count = 0
    for path, value in _settings_documents():
        hooks = value.get("hooks")
        if not isinstance(hooks, dict) or not hooks:
            raise ValidationFailure(f"missing hooks object: {path}")
        unknown = set(hooks) - allowed_events
        if unknown:
            raise ValidationFailure(f"unknown hook events in {path}: {sorted(unknown)}")
        for event, groups in hooks.items():
            if not isinstance(groups, list) or not groups:
                raise ValidationFailure(f"{path}: {event} must contain hook groups")
            for group in groups:
                if not isinstance(group, dict):
                    raise ValidationFailure(f"{path}: {event} group must be an object")
                handlers = group.get("hooks")
                if not isinstance(handlers, list) or not handlers:
                    raise ValidationFailure(f"{path}: {event} group has no handlers")
                for handler in handlers:
                    handler_count += 1
                    if handler.get("type") != "command":
                        raise ValidationFailure(f"{path}: unsupported handler type in {event}")
                    command = handler.get("command")
                    args = handler.get("args")
                    if not isinstance(command, str) or not command:
                        raise ValidationFailure(f"{path}: empty command in {event}")
                    if not isinstance(args, list) or len(args) != 1:
                        raise ValidationFailure(f"{path}: expected one wrapper argument in {event}")
                    wrapper = str(args[0])
                    if "contextdb_" not in wrapper:
                        raise ValidationFailure(f"{path}: unexpected wrapper in {event}: {wrapper}")
                    timeout = handler.get("timeout")
                    if not isinstance(timeout, int) or timeout <= 0:
                        raise ValidationFailure(f"{path}: invalid timeout in {event}")
    if json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")) != json.loads(
        (ROOT / ".claude" / "settings.fragment.json").read_text(encoding="utf-8")
    ):
        raise ValidationFailure("settings.json and settings.fragment.json diverge")
    return f"validated 3 settings documents and {handler_count} command handlers"


def check_required_files() -> str:
    required = [
        "README.md",
        "LICENSE",
        "NOTICE.md",
        "CHANGELOG.md",
        "CLAUDE.md",
        "AGENTS.md",
        "install.py",
        "migrate_legacy.py",
        "Makefile",
        "pyproject.toml",
        "docs/ARCHITECTURE.md",
        "docs/DATA_MODEL.md",
        "docs/SECURITY.md",
        "docs/HOOKS.md",
        "docs/OPERATIONS.md",
        "docs/MIGRATION.md",
        "docs/TRACEABILITY.md",
        "docs/KNOWN_LIMITATIONS.md",
        "docs/VALIDATION_REPORT.md",
        "docs/validation-results.json",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise ValidationFailure(f"missing release files: {missing}")
    wrappers = [
        ".claude/hooks/contextdb_hook.py",
        ".claude/hooks/contextdb_recover.py",
        ".claude/hooks/contextdb_cli.py",
        ".claude/hooks/query_log.py",
    ]
    missing_wrappers = [name for name in wrappers if not (ROOT / name).is_file()]
    if missing_wrappers:
        raise ValidationFailure(f"missing wrappers: {missing_wrappers}")
    return f"required documentation and {len(wrappers)} wrappers are present"


def check_import() -> str:
    package_root = ROOT / ".claude" / "contextdb"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(package_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code = (
        "import contextdb, contextdb.cli, contextdb.hook, contextdb.recovery, "
        "contextdb.redaction, contextdb.semantic, contextdb.spool, contextdb.storage; "
        "print(contextdb.__version__)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise ValidationFailure(result.stderr.strip() or result.stdout.strip())
    version = result.stdout.strip()
    if version != "2.0.0":
        raise ValidationFailure(f"unexpected runtime version: {version}")
    return f"imported runtime version {version}"


def check_tests() -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / ".claude" / "contextdb")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "error::ResourceWarning",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    combined = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode:
        raise ValidationFailure(combined[-6000:])
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    if not match:
        raise ValidationFailure("unittest output did not report a test count")
    count = int(match.group(1))
    if count < MIN_TESTS:
        raise ValidationFailure(f"only {count} tests ran; expected at least {MIN_TESTS}")
    if not re.search(r"\nOK\s*$", combined):
        raise ValidationFailure("unittest suite did not end in OK")
    return f"{count} tests passed with ResourceWarning promoted to error"


def _run(command: list[str], *, cwd: Path, input_text: str | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CLAUDE_PROJECT_DIR"] = str(cwd)
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def check_install_and_hook_smoke() -> str:
    with tempfile.TemporaryDirectory(prefix="compactiondb-validate-") as temp:
        target = Path(temp) / "project"
        (target / ".claude").mkdir(parents=True)
        unrelated = {
            "hooks": {
                "Stop": [
                    {
                        "hooks": [
                            {"type": "command", "command": "echo", "args": ["unrelated"], "timeout": 3}
                        ]
                    }
                ]
            }
        }
        (target / ".claude" / "settings.json").write_text(
            json.dumps(unrelated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        install = [sys.executable, str(ROOT / "install.py"), "--project", str(target)]
        first = _run(install, cwd=ROOT)
        second = _run(install, cwd=ROOT)
        if first.returncode or second.returncode:
            raise ValidationFailure((first.stderr + second.stderr).strip())
        settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
        serialized = json.dumps(settings, ensure_ascii=False)
        if serialized.count("contextdb_recover.py") != 1:
            raise ValidationFailure("installer is not idempotent for recovery hook")
        if "unrelated" not in serialized:
            raise ValidationFailure("installer removed an unrelated hook")

        session = "validate-session"
        secret = "sk-ant-" + "x" * 32
        prompt_payload = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": session,
            "cwd": str(target),
            "prompt": f"[memory:decision] API v2を採用する。 token={secret}",
        }
        hook = _run(
            [sys.executable, str(target / ".claude" / "hooks" / "contextdb_hook.py")],
            cwd=target,
            input_text=json.dumps(prompt_payload, ensure_ascii=False),
        )
        if hook.returncode:
            raise ValidationFailure(hook.stderr.strip() or hook.stdout.strip())

        compact_payload = {
            "hook_event_name": "PostCompact",
            "session_id": session,
            "cwd": str(target),
            "trigger": "auto",
            "compact_summary": "API v2を採用し、認証実装を継続する。",
        }
        compact = _run(
            [sys.executable, str(target / ".claude" / "hooks" / "contextdb_hook.py")],
            cwd=target,
            input_text=json.dumps(compact_payload, ensure_ascii=False),
        )
        if compact.returncode:
            raise ValidationFailure(compact.stderr.strip() or compact.stdout.strip())

        cli = target / ".claude" / "hooks" / "contextdb_cli.py"
        drain = _run([sys.executable, str(cli), "--json", "drain"], cwd=target)
        if drain.returncode:
            raise ValidationFailure(drain.stderr.strip() or drain.stdout.strip())
        verify = _run([sys.executable, str(cli), "--json", "verify"], cwd=target)
        if verify.returncode:
            raise ValidationFailure(verify.stderr.strip() or verify.stdout.strip())
        verify_data = json.loads(verify.stdout)
        if (
            not verify_data.get("ok")
            or verify_data.get("health", {}).get("integrity") != "ok"
            or not verify_data.get("event_hashes", {}).get("ok")
        ):
            raise ValidationFailure(f"verify failed: {verify_data}")

        recovery_payload = {
            "hook_event_name": "SessionStart",
            "source": "compact",
            "session_id": session,
            "cwd": str(target),
        }
        recovery = _run(
            [sys.executable, str(target / ".claude" / "hooks" / "contextdb_recover.py")],
            cwd=target,
            input_text=json.dumps(recovery_payload, ensure_ascii=False),
        )
        if recovery.returncode:
            raise ValidationFailure(recovery.stderr.strip() or recovery.stdout.strip())
        recovery_json = json.loads(recovery.stdout)
        context = recovery_json["hookSpecificOutput"]["additionalContext"]
        if "API v2" not in context or "validate-session" not in context:
            raise ValidationFailure("recovery context omitted expected session evidence")
        if secret in context:
            raise ValidationFailure("secret leaked into recovery context")

        db = target / ".claude" / "contextdb" / "state" / "context.db"
        conn = sqlite3.connect(db)
        try:
            event_count = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
            leaked = int(conn.execute("SELECT COUNT(*) FROM events WHERE detail_json LIKE ?", (f"%{secret}%",)).fetchone()[0])
            memory_count = int(conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0])
        finally:
            conn.close()
        if event_count < 2 or memory_count < 2 or leaked:
            raise ValidationFailure(
                f"unexpected smoke data: events={event_count} memories={memory_count} leaked={leaked}"
            )
        return f"idempotent install, hook ingest, redaction, verify, and compact recovery passed ({event_count} events)"


def check_release_tree_clean() -> str:
    forbidden: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if path.is_dir() and path.name == "__pycache__":
            forbidden.append(relative + "/")
        elif path.is_file() and (path.suffix in {".pyc", ".pyo"} or path.name == ".writer.lock"):
            forbidden.append(relative)
        elif path.is_file() and path.name.startswith("context.db"):
            forbidden.append(relative)
    if forbidden:
        raise ValidationFailure("runtime/build artifacts present: " + ", ".join(sorted(forbidden)[:20]))
    return "no pycache, bytecode, SQLite runtime, or writer-lock artifacts in release tree"


def check_claude_executable() -> str:
    executable = shutil.which("claude")
    if not executable:
        raise ValidationFailure("Claude Code executable is not installed in this validation environment")
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=15, check=False)
    if result.returncode:
        raise ValidationFailure(result.stderr.strip() or "claude --version failed")
    return result.stdout.strip() or executable


def main() -> int:
    args = parse_args()
    results: list[CheckResult] = []
    run_check(results, "python_runtime", check_python)
    run_check(results, "required_release_files", check_required_files)
    run_check(results, "python_syntax", check_syntax)
    run_check(results, "json_documents", check_json)
    run_check(results, "claude_hook_settings", check_hook_settings)
    run_check(results, "runtime_import", check_import)
    if not args.skip_tests:
        run_check(results, "unittest_suite", check_tests)
    run_check(results, "installed_project_smoke", check_install_and_hook_smoke)
    run_check(results, "release_tree_clean", check_release_tree_clean)
    run_check(results, "claude_code_executable", check_claude_executable, required=False)

    required_failures = [result for result in results if result.required and result.status != "pass"]
    report = {
        "product": "CompactionDB",
        "version": "2.0.0",
        "validated_at_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "sqlite": sqlite3.sqlite_version,
        },
        "summary": {
            "status": "pass" if not required_failures else "fail",
            "passed": sum(result.status == "pass" for result in results),
            "failed": sum(result.status == "fail" for result in results),
            "skipped": sum(result.status == "skip" for result in results),
        },
        "checks": [asdict(result) for result in results],
    }

    if args.report_json:
        destination = Path(args.report_json)
        if not destination.is_absolute():
            destination = ROOT / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not required_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
