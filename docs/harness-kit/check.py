#!/usr/bin/env python3
"""Check the THAK design documents under docs/harness-kit for internal consistency.

Run from the repository root: `python3 -I docs/harness-kit/check.py [--holds-today]`. Standard library only.
Default mode: research titles and sources headings, the ADRs the PRD names and their sections, requirement ids
against scenario tags, one of @holds-today or @target per scenario, the decisions.tsv columns, and that the
@holds-today scenarios and HOLDS_TODAY name the same titles. `--holds-today` also runs each HOLDS_TODAY command.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = "home/dot_agents/agent-config.yaml"
VALIDATOR = "scripts/validate-agent-assets.py"
AUDIT = "home/dot_local/bin/common/executable_pr-audit.sh"
MERGE = "home/dot_local/bin/common/executable_pr-merge.sh"
SEAT = "home/dot_local/bin/common/executable_hcom-seat"
POLICIES = "home/dot_agents/omp/policies"
SEARCHED = "home scripts install"
Check = tuple[str, int | str]  # a shell command run from the repository root, and its expected exit code or stdout


def has(path: str, *texts: str) -> Check:
    """PATH holds every literal TEXT (basic grep syntax; a single quote is not usable in TEXT)."""
    return " && ".join(f"grep -q '{text}' {path}" for text in texts), 0


def absent(pattern: str, where: str = SEARCHED) -> Check:
    """No file under WHERE matches the extended, case-insensitive regex PATTERN."""
    return f"! grep -rqiE '{pattern}' {where}", 0


# Scenario title -> check. Every @holds-today scenario of bdd/*.feature has one row here, and no other row exists.
HOLDS_TODAY: dict[str, Check] = {
    "Every shared skill directory has an audience entry": (
        f'for d in home/dot_agents/skills/*/; do n=$(basename "$d"); grep -q "^    $n: \\[" {MANIFEST} || exit 1; done',
        0,
    ),
    "The manifest declares no MCP server today": (f"grep -o 'mcp_servers: {{}}' {MANIFEST}", "mcp_servers: {}"),
    "The validator refuses an enabled MCP server": has(VALIDATOR, "must be disabled by default in the shared manifest"),
    "A Claude plugin without a version is pinned by content digest": (
        f'grep -q "frontend-design@claude-plugins-official: {{marketplace: anthropics/claude-plugins-official, pin: \'sha256:" {MANIFEST}',
        0,
    ),
    "The validator refuses a Claude-targeted MCP server": has(
        VALIDATOR, "cannot target claude: add it with `claude mcp add --scope user`"
    ),
    "The knowledge-work-plugins engineering plugin is not pinned": absent(
        "knowledge-work-plugins", f"{SEARCHED} Makefile setup.sh"
    ),
    "The Claude Bash sandbox is strict and fails closed": (
        has(MANIFEST, "^    failIfUnavailable: true", "^    allowUnsandboxedCommands: false")[0]
        + f" && grep -A2 '^    excludedCommands:' {MANIFEST}",
        "excludedCommands:\n      - git push *\n      - gh *",
    ),
    "No Unix socket switch is set in the Claude sandbox": (f"! grep -qE '^ *allow(All)?UnixSockets:' {MANIFEST}", 0),
    "A seat starts only after its sandbox canary holds": has(
        SEAT, "canary", "sandbox-runtime", "no uncontained fallback"
    ),
    "Seat approval is not containment": (
        f"grep -q 'Approval is not containment' {POLICIES}/orchestrator.yml"
        f" && grep -q 'Approval is not containment' {POLICIES}/worker.yml",
        0,
    ),
    "The Codex audit runs under Codex's own permission profile, never under srt": (
        has(AUDIT, "permission profile `audit`", "scratch HOME")[0] + f" && ! grep -qw srt {AUDIT}",
        0,
    ),
    "Sandboxed commands cannot read the SSH keys": has(MANIFEST, "^        - path: ~/.ssh$"),
    "The merge lever refuses without a correct verdict row": (
        has(MERGE, "records as `correct`")[0] + f" && grep -q -- '--match-head-commit' {MERGE}",
        0,
    ),
    "The audit rules come from the main branch, never from the head": has(AUDIT, "main:AGENTS.md", "scratch HOME"),
    "The audit profile is read-only at the pinned model and effort": has(
        VALIDATOR, '("model", "gpt-6-astra"),', '("model_reasoning_effort", "xhigh"),', '("sandbox_mode", "read-only"),'
    ),
    "Every audit ends with one verdict line": has(
        "AGENTS.md", "exactly one verdict line: `Verdict: correct` or `Verdict: incorrect`, or `Verdict: blocked`"
    ),
    "A trust-boundary change carries a threat table": has(
        "AGENTS.md", "carries a `## Threat table` section in its body"
    ),
    "The fourth audit round needs a closing decision": has(AUDIT, "rounds-check.py"),
    "Every third-party asset declares its pin and verification": has(
        VALIDATOR, "^def validate_assets(manifest", "Require one complete declaration per asset"
    ),
    "A vendored skill tree is pinned by commit and archive digest": (
        f"block() {{ sed -n '/^  pstack:$/,/^  [a-z-]*:$/p' {MANIFEST}; }}; block | grep -q '^    upstream: cursor/plugins$'"
        " && block | grep -qE '^    pin: [0-9a-f]{40}$' && block | grep -qE '^    sha256: [0-9a-f]{64}$'",
        0,
    ),
    "The validator admits only the Agent Skills frontmatter fields": has(
        VALIDATOR,
        'SKILL_FIELDS = frozenset({"name", "description", "license", "compatibility", "metadata", "allowed-tools"})',
    ),
    "The cybersecurity skills pack is not installed or referenced": absent("Anthropic-Cybersecurity-Skills"),
    "The committed-secret scan covers every tracked file": has(
        VALIDATOR, "^def validate_no_obvious_secrets", "^SECRET_RULES = ("
    ),
    "No graphify entry exists in the managed trees": absent("graphify"),
    "A manifest MCP server must be exposed to Codex only": has(
        VALIDATOR, "must be exposed to Codex, the one agent whose MCP config this repo renders"
    ),
    "No DeepSeek or Ollama route exists today": absent("deepseek|ollama"),
    "Model ids live in model_profiles only": has(
        VALIDATOR, "must keep model settings in model_profiles only", "must define the six base profiles and no others"
    ),
    "The superagent prototype is not deployed": absent("superagent"),
    "tester-army/e2e is not a dependency of the kit": absent(
        "tester-army|@e2e-dev", f"{SEARCHED} Makefile mise.toml .github"
    ),
    "The bootstrap is run end to end in CI": has(".github/workflows/ubuntu.yaml", "bash ./setup.sh", "run_bats"),
    "The apply check runs offline in a container": ("grep -q -- '--network none' Makefile", 0),
    "Bats runs in CI, not on the operator's host": has("AGENTS.md", "Do not run `bats` tests locally"),
    "The unit-test workflow is never path-filtered at the workflow level": (
        has(".github/workflows/test.yaml", "Required checks must always report a final status")[0]
        + " && ! sed -n '1,12p' .github/workflows/test.yaml | grep -q 'paths:'",
        0,
    ),
}

ADR_SECTIONS = ("## Context", "## Decision", "## Alternatives considered", "## Consequences", "## Verification")
RESEARCH_TITLE = re.compile(r"^# [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
REQUIREMENT_ROW = re.compile(r"^\| (R-\d{2}) +\|")
ADR_NAME = re.compile(r"ADR-(\d{3})")
SCENARIO_TAG = re.compile(r"@R-\d{2}")
Scenario = tuple[str, str, list[str]]  # feature file, title, tags


def check_research(errors: list[str]) -> None:
    for path in sorted((HERE / "research").glob("*.md")):
        lines = path.read_text().splitlines()
        if not lines or not RESEARCH_TITLE.match(lines[0]):
            errors.append(f"{path.name}: first line is not `# <owner>/<repo>`")
        if not any(line.startswith("#") and "Source" in line for line in lines):
            errors.append(f"{path.name}: no heading containing `Source`")


def check_adrs(prd: str, errors: list[str]) -> None:
    for number in sorted(set(ADR_NAME.findall(prd))):
        matches = list((HERE / "adr").glob(f"ADR-{number}-*.md"))
        if len(matches) != 1:
            errors.append(f"ADR-{number}: expected one file under adr/, found {len(matches)}")
            continue
        text = matches[0].read_text()
        if not text.startswith(f"# ADR-{number}: "):
            errors.append(f"{matches[0].name}: title line is not `# ADR-{number}: <title>`")
        if not re.search(r"^Status: (accepted|proposed)$", text, re.MULTILINE):
            errors.append(f"{matches[0].name}: no `Status: accepted|proposed` line")
        if not re.search(r"^Date: \d{4}-\d{2}-\d{2}$", text, re.MULTILINE):
            errors.append(f"{matches[0].name}: no `Date: YYYY-MM-DD` line")
        errors.extend(f"{matches[0].name}: missing section `{s}`" for s in ADR_SECTIONS if f"\n{s}\n" not in text)


def scenarios() -> list[Scenario]:
    found: list[Scenario] = []
    for path in sorted((HERE / "bdd").glob("*.feature")):
        tags: list[str] = []
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("@"):
                tags.extend(stripped.split())
            elif stripped.startswith("Scenario:"):
                found.append((path.name, stripped[len("Scenario:") :].strip(), tags))
                tags = []
            elif stripped and not stripped.startswith("#"):
                tags = []
    return found


def check_requirements(prd: str, found: list[Scenario], errors: list[str]) -> None:
    table_ids = {match.group(1) for line in prd.splitlines() if (match := REQUIREMENT_ROW.match(line))}
    if not table_ids:
        errors.append("PRD.md: no requirement rows `| R-nn |` found")
    tagged = {tag[1:] for _, _, tags in found for tag in tags if SCENARIO_TAG.fullmatch(tag)}
    errors.extend(f"PRD.md: requirement {missing} has no scenario tag" for missing in sorted(table_ids - tagged))
    errors.extend(f"bdd: scenario tag @{unknown} is not in the PRD table" for unknown in sorted(tagged - table_ids))
    for name, title, tags in found:
        kinds = [tag for tag in tags if tag in ("@holds-today", "@target")]
        if len(kinds) != 1:
            errors.append(f"{name}: `{title}` must carry exactly one of @holds-today and @target, has {kinds}")
        if not any(SCENARIO_TAG.fullmatch(tag) for tag in tags):
            errors.append(f"{name}: `{title}` carries no @R-nn tag")
    holds = {title for _, title, tags in found if "@holds-today" in tags}
    errors.extend(
        f"check.py: @holds-today scenario `{t}` has no HOLDS_TODAY row" for t in sorted(holds - set(HOLDS_TODAY))
    )
    errors.extend(
        f"check.py: HOLDS_TODAY row `{t}` names no @holds-today scenario" for t in sorted(set(HOLDS_TODAY) - holds)
    )


def check_decisions(errors: list[str]) -> None:
    rows = (HERE / "decisions.tsv").read_text().splitlines()
    if not rows or rows[0] != "ts\tphase\tdecision\twhy\tevidence\tresult":
        errors.append("decisions.tsv: header is not the six columns ts, phase, decision, why, evidence, result")
    for number, row in enumerate(rows[1:], start=2):
        if row and len(row.split("\t")) != 6:
            errors.append(f"decisions.tsv:{number}: {len(row.split(chr(9)))} cells, expected 6")


def run_holds_today() -> int:
    failures = 0
    for title, (command, expected) in HOLDS_TODAY.items():
        result = subprocess.run(["sh", "-c", command], cwd=ROOT, capture_output=True, text=True)
        ok = result.returncode == expected if isinstance(expected, int) else result.stdout.strip() == expected
        print(f"{'pass' if ok else 'FAIL'}: {title}")
        if not ok:
            failures += 1
            detail = result.stdout.strip() or result.stderr.strip()
            print(f"      exit {result.returncode}, expected {expected!r}" + (f": {detail}" if detail else ""))
    return failures


def main(argv: list[str]) -> int:
    errors: list[str] = []
    prd = (HERE / "PRD.md").read_text()
    check_research(errors)
    check_adrs(prd, errors)
    found = scenarios()
    check_requirements(prd, found, errors)
    check_decisions(errors)
    for error in errors:
        print(f"ERROR: {error}")
    holds = sum("@holds-today" in tags for _, _, tags in found)
    print(f"{len(found)} scenarios ({holds} holds-today, {len(found) - holds} target), {len(errors)} errors")
    failures = run_holds_today() if "--holds-today" in argv else 0
    if failures:
        print(f"{failures} holds-today scenario(s) failed")
    return 1 if errors or failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
