"""Form, drift and invariant checks over the plan 024 group (plan 024 programs (15)), one violation per line.

`uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]`
reads the eleven `.orchestration/plans/024-*` files under --root (default: the current git toplevel), prints every
violation on its own line and exits 1 when there is one, 0 otherwise. It writes nothing.
F1 every 024-todo.md table row has a non-empty completion (last) column.
F2 the tasks one wave row of the plan's section 6 names have pairwise-disjoint allowed_files once their task files
   exist (a task file belongs to the todo id its `# ` title line names): each glob entry stands for the tree files it
   matches, a literal entry for itself, and two lists overlap where a path is in both or inside the other's directory,
   or where a literal matches the other's glob; the finding names the first shared path. Glob spellings are never
   compared with each other.
F3 every P1-<n> row names a bottleneck id: a B<n> row of 024-design-mechanism.md or an M<n> row of 024-design-quality.md.
F4 every DoD row of 024-checklists.md holds a backtick command or a file path.
F5 every decision row of the plan's section 2 has a bold default.
F6 every cited dotfiles-T<n>-... id is a task file, every D-... id a row of .orchestration/decisions.tsv, and with
   --drift every #<pr> a pull request.
--drift: every head sha or state word (CLEAN, BEHIND, draft, merged, closed) that starts within 40 characters after a
   #<pr> on its line, before the next #, each compared on its own against `gh pr view`; and every 024-progress.tsv row
   naming a task against the status of that task's latest AGMSG-ACCEPTANCE event (task_id=<task>, each event read up
   to the next one on its line) in its acceptance record, latest by the last timestamp before the event on its line (an
   untimed event carries the latest timestamp above it), then by position: `drift: <file>:<line> <cited> != <live>`.
--invariants: ANTHROPIC_OAUTH_TOKEN= with a value (bare, single- or double-quoted; an empty "" or '' is none),
   `git push origin main`, `gh pr merge` with --admin or --auto in the
   plan files, and a claude.permissions.ask entry home/dot_agents/agent-config.yaml adds against origin/main.
"""

import argparse
import glob
import json
import pathlib
import re
import subprocess
import sys
from fnmatch import fnmatchcase

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
    return subprocess.run(args, cwd=root, capture_output=True, text=True, check=False)


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
        paths |= {p for p in glob.glob(g, root_dir=root, recursive=True, include_hidden=True) if (root / p).is_file()}
    return paths, globs


def shared(a, b):
    (pa, ga), (pb, gb) = a, b
    out = {x for x in pa for y in pb if x == y or x.startswith(y + "/")}
    out |= {y for x in pa for y in pb if y.startswith(x + "/")}
    # A literal not yet in the tree overlaps a glob it matches (fnmatch's * also crosses /, which errs toward a report).
    out |= {x for x in pa for g in gb if fnmatchcase(x, g)} | {y for y in pb for g in ga if fnmatchcase(y, g)}
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
    decisions = {l.split("\t", 1)[0] for l in (root / ".orchestration/decisions.tsv").read_text().splitlines()[1:]}
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
    base = run(root, "git", "show", f"origin/main:{path}")
    if base.returncode == 0 and (root / path).is_file():

        def asks(text):
            return ((yaml.safe_load(text) or {}).get("claude") or {}).get("permissions", {}).get("ask") or []

        old = asks(base.stdout)
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
    root = args.root or pathlib.Path(run(".", "git", "rev-parse", "--show-toplevel").stdout.strip())
    paths = sorted((root / PLANS).glob("024-*.md")) + [root / PLANS / "024-progress.tsv"]
    files = {p.name: p.read_text().splitlines() for p in paths}
    found = form(root, files)
    found += drift(root, files) if args.drift else []
    found += invariants(root, files) if args.invariants else []
    if found:
        print("\n".join(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
