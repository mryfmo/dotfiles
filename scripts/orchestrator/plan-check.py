"""Read-only plan 024 checks under --root, with optional --drift and --invariants.

F1 completion cells; F2 disjoint concrete scopes and confined globs; F3 bottleneck ids; F4 executable DoD references;
F5 bold defaults; F6 task/decision ids and, with --drift, PR existence. Drift compares each PR occurrence's head/state
and each progress row against the latest timestamped acceptance. Invariants reject valued OAuth assignments,
unsafe merge/push commands and added permissions.ask entries. Directory symlinks are never traversed.
"""

import argparse
import importlib.util
import json
import os
import pathlib
import re
import sys
from fnmatch import fnmatchcase

helper = pathlib.Path(__file__).resolve().with_name("task-consistency-check.py").resolve()
if not os.path.samefile(helper.parent, pathlib.Path(__file__).resolve().parent):
    sys.exit("refused: checker outside the trusted script directory")
spec = importlib.util.spec_from_file_location("checker", helper)
checker = importlib.util.module_from_spec(spec)
helper_data = helper.read_bytes()
spec.loader.get_code = lambda _: compile(helper_data, str(helper), "exec")
spec.loader.exec_module(checker)

try:
    import yaml
except ImportError:
    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

PLANS = ".orchestration/plans"
TASK_ID = r"\bdotfiles-T\d+(?:-[a-z0-9]+)+"
DECISION_ID = r"\bD-(?!W\d)[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
GLOB = re.compile(r"[*?[]")
STATES = {"CLEAN": ("mergeStateStatus", "CLEAN"), "BEHIND": ("mergeStateStatus", "BEHIND"), "draft": ("isDraft", True)}
STATES |= {"merged": ("state", "MERGED"), "closed": ("state", "CLOSED")}
FORBIDDEN = {
    "ANTHROPIC_OAUTH_TOKEN with a value": r"ANTHROPIC_OAUTH_TOKEN=(?:\"[^\"\n]+\"|'[^'\n]+'|[^\s`'\")<])",
    "git push origin main": r"git push origin main\b",
    "gh pr merge --admin or --auto": r"gh pr merge\b[^\n]*?--(?:admin|auto)\b",
}


def run(root, *args):
    return (
        checker.git(root, *args[1:])
        if args[0] == "git"
        else checker.launch(root, checker.executable(args[0]), *args[1:], "--repo", "mryfmo/dotfiles")
    )


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_rows(lines):
    """(line number, cells) of every table data row: not a header (the row above a separator) nor a separator."""
    rows = []
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.startswith("|") and not re.match(r"\|\s*-{3}", line) and not re.match(r"\|\s*-{3}", nxt):
            rows.append((i + 1, cells(line)))
    return rows


def section(lines, number):
    start = next((i for i, l in enumerate(lines) if l.startswith(f"## {number}.")), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return [""] * (start + 1) + lines[start + 1 : end]  # keeps the file's line numbers


def scope(root, entries):
    """(paths, globs) of an allowed_files list: its literals and the tree files each glob matches, and its globs."""
    globs = {e for e in entries if GLOB.search(e)}
    paths = {e.rstrip("/") for e in entries if e not in globs}
    for g in globs:
        parts = pathlib.PurePath(g).parts
        if pathlib.Path(g).is_absolute() or ".." in parts:
            raise ValueError(f"F2 outside-root glob: {g}")
        prefix = root.joinpath(*parts[: next(i for i, p in enumerate(parts) if GLOB.search(p))])
        if any(p.is_symlink() for p in (prefix, *prefix.parents) if p.is_relative_to(root)):
            raise ValueError(f"F2 outside-root or directory-symlink glob: {g}")
        for directory, dirs, files in os.walk(prefix, followlinks=False):
            dirs[:] = [d for d in dirs if not pathlib.Path(directory, d).is_symlink()]
            for name in files:
                path = pathlib.Path(directory, name)
                rel = path.relative_to(root).as_posix()
                if glob_matches(parts, pathlib.PurePosixPath(rel).parts):
                    if checker.confined(root, path) is None:
                        raise ValueError(f"F2 outside-root glob match: {g}")
                    paths.add(rel)
    return paths, globs


def glob_matches(pattern, names):
    if not pattern:
        return not names
    if pattern[0] == "**":
        return glob_matches(pattern[1:], names) or bool(names and glob_matches(pattern, names[1:]))
    return bool(names and fnmatchcase(names[0], pattern[0]) and glob_matches(pattern[1:], names[1:]))


def shared(a, b):
    (pa, ga), (pb, gb) = a, b
    out = {x for x in pa for y in pb if x == y or x.startswith(y + "/")}
    out |= {y for x in pa for y in pb if y.startswith(x + "/")}
    # A literal not yet in the tree still uses the same component grammar as enumerated files.
    out |= {x for x in pa for g in gb if glob_matches(pathlib.PurePosixPath(g).parts, pathlib.PurePosixPath(x).parts)}
    out |= {y for y in pb for g in ga if glob_matches(pathlib.PurePosixPath(g).parts, pathlib.PurePosixPath(y).parts)}
    return sorted(out)


def latest(text, tid):
    """The status of tid's latest AGMSG-ACCEPTANCE event, or none."""
    events, carried, stamp = [], "", r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?"
    for i, line in enumerate(text.splitlines()):
        for m in re.finditer(r"AGMSG-ACCEPTANCE v1 (.*?)(?=AGMSG-ACCEPTANCE v1 |$)", line):  # one event at a time
            status = re.search(r"\bstatus=([\w-]+)", m[1])
            if status and re.search(rf"\btask_id={re.escape(tid)}(?![\w-])", m[1]):
                stamps = re.findall(stamp, line[: m.start()])
                events.append((stamps[-1] if stamps else carried, i, m.start(), status[1]))
        carried = max([carried, *re.findall(stamp, line)])
    return max(events)[3] if events else "none"


def form(root, files):
    out = []
    todo, plan = files["024-todo.md"], files["024-omp-cutover-and-corrective-order.md"]
    for n, c in table_rows(todo):  # F1
        if not c[-1]:
            out.append(f"F1 024-todo.md:{n} {c[0][:20]} has an empty completion column")
    ids = set(re.findall(r"^\| (B\d+) \|", "\n".join(files["024-design-mechanism.md"]), re.M))
    ids |= set(re.findall(r"^\| (M\d+) \|", "\n".join(files["024-design-quality.md"]), re.M))
    for n, c in table_rows(todo):  # F3
        if c[0].startswith("P1-") and not set(re.findall(r"\b[BM]\d+\b", " ".join(c))) & ids:
            out.append(f"F3 024-todo.md:{n} {c[0].split()[0]} names no bottleneck id of 5.0 or 5.10")
    tasks = {}
    for p in sorted((root / ".orchestration/tasks").glob("*.md")):
        if checker.confined(root, p) is None:
            out.append("F2 outside-root task file")
            continue
        title = next((l for l in p.read_text().splitlines() if l.startswith("# ")), "")
        for tid in set(re.findall(r"\bP1-\d+[a-z]?\b", title)):
            allowed = (yaml.safe_load(p.read_text().split("\n---\n", 1)[0].lstrip("-\n")) or {}).get("allowed_files")
            tasks.setdefault(tid, set()).update(allowed or [])
    tasks = {tid: scope(root, entries) for tid, entries in tasks.items()}
    for n, c in table_rows(section(plan, 6)):  # F2
        wave = sorted(set(re.findall(r"\bP1-\d+[a-z]?\b", " ".join(c[1:]))) & set(tasks))
        for i, a in enumerate(wave):
            for b in wave[i + 1 :]:
                if both := shared(tasks[a], tasks[b]):
                    out.append(f"F2 024-omp-cutover-and-corrective-order.md:{n} {c[0]} {a} and {b} share {both[0]}")
    for n, c in table_rows(files["024-checklists.md"]):  # F4
        if not re.search(r"`[^`]+`|[\w.~-]*/[\w./-]+|\b\w+\.(?:md|json|tsv|ya?ml|sh|py)\b", " ".join(c[1:])):
            out.append(f"F4 024-checklists.md:{n} {c[0]} holds no backtick command or file path")
    for n, c in table_rows(section(plan, 2)):  # F5
        if re.match(r"D\d+\b", c[0]) and not re.search(r"\*\*[^*]+\*\*", c[-1]):
            out.append(f"F5 024-omp-cutover-and-corrective-order.md:{n} {c[0].split()[0]} has no bold default")
    ledger = checker.main_text(root, ".orchestration/decisions.tsv")
    if ledger is None:
        sys.exit("refused: canonical decisions.tsv unavailable")
    decisions = {l.split("\t", 1)[0] for l in ledger.splitlines()[1:]}
    for name, lines in files.items():  # F6
        for n, line in enumerate(lines, 1):
            for tid in dict.fromkeys(re.findall(TASK_ID, line)):
                if not (root / f".orchestration/tasks/{tid}.md").is_file():
                    out.append(f"F6 {name}:{n} cites {tid}, which is not a task file")
            # A family such as D-024-* names no single decision.
            ids = [m.group() for m in re.finditer(DECISION_ID, line) if line[m.end() : m.end() + 2] != "-*"]
            for did in dict.fromkeys(ids):
                if did not in decisions:
                    out.append(f"F6 {name}:{n} cites {did}, which is not a row of decisions.tsv")
    return out


def drift(root, files):
    out, live = [], {}

    def pr(number):
        if number not in live:
            got = run(root, "gh", "pr", "view", number, "--json", "headRefOid,mergeStateStatus,isDraft,state")
            live[number] = json.loads(got.stdout) if got.returncode == 0 else None
        return live[number]

    for name, lines in files.items():
        for n, line in enumerate(lines, 1):
            for number in dict.fromkeys(re.findall(r"#(\d{2,6})\b", line)):
                if pr(number) is None:
                    out.append(f"F6 {name}:{n} cites #{number}, which is not a pull request")
            found = {}
            for m in re.finditer(r"#(\d{2,6})\b([^#\n]*)", line):
                state = pr(m.group(1))
                if state is None:
                    continue
                tokens = re.finditer(r"\b([0-9a-f]{7,40}|CLEAN|BEHIND|draft|merged|closed)\b", m.group(2))
                for cited in dict.fromkeys(t.group() for t in tokens if t.start() <= 40):
                    if cited in STATES:
                        key, want = STATES[cited]
                        if state.get(key) != want:
                            found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get(key)}"] = None
                    elif not state.get("headRefOid", "").startswith(cited):
                        found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get('headRefOid', '')[:12]}"] = None
            out += found
    for n, line in enumerate(files["024-progress.tsv"][1:], 2):
        tid, *rest = line.split("\t")
        record = root / f".orchestration/acceptance/{tid}.md"
        if not rest or not (root / f".orchestration/tasks/{tid}.md").is_file():
            continue
        live = latest(record.read_text(), tid) if record.is_file() else "none"
        if len(rest) > 2 and rest[2] != live:
            out.append(f"drift: 024-progress.tsv:{n} {tid} {rest[2]} != {live}")
    return out


def invariants(root, files):
    out = []
    for name, lines in files.items():
        for n, line in enumerate(lines, 1):
            out += [f"invariant: {name}:{n} {what}" for what, rx in FORBIDDEN.items() if re.search(rx, line)]
    path = "home/dot_agents/agent-config.yaml"
    base = checker.main_text(root, path)
    if base is None and (root / path).is_file():
        sys.exit(f"refused: canonical baseline unavailable: {path}")
    if base is not None and (root / path).is_file():

        def asks(text):
            return ((yaml.safe_load(text) or {}).get("claude") or {}).get("permissions", {}).get("ask") or []

        old = asks(base)
        out += [f"invariant: {path} permissions.ask adds {e}" for e in asks((root / path).read_text()) if e not in old]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the current git toplevel)")
    parser.add_argument(
        "--drift", action="store_true", help="compare cited PR states and progress rows with live state"
    )
    parser.add_argument("--invariants", action="store_true", help="report forbidden patterns and added ask entries")
    args = parser.parse_args()
    root = (args.root or checker.repository(".")).resolve()
    checker.git(root, "rev-parse", "--show-toplevel")
    for folder in (root / PLANS, root / ".orchestration/tasks"):
        if any(p.is_symlink() for p in (folder, *folder.parents) if p.is_relative_to(root)):
            sys.exit("F2 directory-symlink input")
    paths = sorted((root / PLANS).glob("024-*.md")) + [root / PLANS / "024-progress.tsv"]
    if any(checker.confined(root, p) is None for p in paths):
        sys.exit("F2 outside-root plan input")
    files = {p.name: p.read_text().splitlines() for p in paths}
    try:
        found = form(root, files)
    except ValueError as error:
        found = [str(error)]
    found += drift(root, files) if args.drift else []
    found += invariants(root, files) if args.invariants else []
    if found:
        print("\n".join(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
