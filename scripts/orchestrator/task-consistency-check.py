"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).

`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
resolves the design path (C6) and probes origin/main with git (C8 to C10) under --root (default: the first file's git
toplevel), prints `<file name>: OK` or `: FAIL` with one `  C<n> ...` line per finding, and exits 1 when any file fails.
C1 task_id equals the file name.
C2 allowed_files covers .orchestration/<task_id>/** and names no other task's .orchestration/<id>/ directory.
C3 when reset_of is non-empty, a threat_table row names every reset_of id's task.md and the task's own.
C4 every allowed_files entry (its path before any glob) is named in a row's control, followed by its end, a space, / " ' ( ) , or a glob.
C5 no residual binds a predecessor's hash ("names the <aNN> file's hash") instead of the task's own.
C6 design_review.receipt is the design file's current design_review.receipt.
C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit).
C7b no row other than a non-path control names two allowed_files entries (one row per entry).
C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not read yet has a threat row.
C9 (docs tasks) a quoted rule sentence naming a script, *_EVIDENCE, a check id or classes: finds it on origin/main or says once/until.
C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test.
C11 a disposition's payload has its form's shape: closed: tests/<path>::<identifier>, out-of-scope: an existing task id, residual: 20+ characters.
C12 a glob entry of an executed or applied kind (*.sh *.py *.yaml *.yml *.json *.toml, or under home/ scripts/ .githooks/ .github/) has a row per matched file.
C13 every disposition is exactly one of closed:, residual: or out-of-scope: followed by a space.
C14 every premise command, run under bash -c with pipefail, PATH <root>/bin:/usr/bin:/bin, prints its pasted output with whitespace runs
    collapsed (gh, curl and URLs skipped; a tool absent from that PATH is a `C14: tool absent <name>` warning).
C15 with invariants and design_review.design, each invariant equals the design's on origin/main byte for byte.
"""

import argparse
import os
import pathlib
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

ROW_UNIT = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal"
C7_NAMES = ROW_UNIT.split("|")
NONPATH = ("in-process effects", "task metadata", "metadata separators", "workflow and interpreter")
NONPATH += ("new or renamed scripts", "orchestrator effect")
C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
FORMS = ("closed: ", "residual: ", "out-of-scope: ")
APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
SKIPPED = "C14 skipped network premise"  # a note, never a failure
ABSENT = "C14: tool absent"  # a warning, never a failure (Amendment 1)


def front(text):
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


def rerun(cmd, cwd, path=None):
    """Run a premise or Check command as C14 does; return (stdout, exit status, stderr), stdout None on a timeout.

    The command is bash's script argument (`bash -c`, pipefail on), never spliced into another shell line; premises
    get PATH <root>/bin:/usr/bin:/bin so a rerun prints what the pasted output says, and task-from-plan.py runs its
    premises through this same function.
    """
    env = {"PATH": path or f"{cwd}/bin:/usr/bin:/bin", "HOME": os.environ.get("HOME", "/")}
    try:
        run = subprocess.run(
            ["bash", "-c", "set -o pipefail\n" + cmd],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, 124, ""
    return run.stdout, run.returncode, run.stderr


def check(p, root):
    fm = front(text := p.read_text())
    tid = fm.get("task_id")
    suffix = tid.rsplit("-", 1)[-1]
    fails = []
    if tid != p.stem:
        fails.append(f"C1 task_id {tid} != file {p.stem}")
    allowed = fm.get("allowed_files") or []
    own_dir = f".orchestration/{tid}/"
    if not any(a.startswith(own_dir) for a in allowed):
        fails.append(f"C2 allowed_files lacks {own_dir}**")
    for a in allowed:
        m = re.match(r"\.orchestration/([^/]+)/", a)
        if m and m.group(1) != tid:
            fails.append(f"C2 allowed_files names another task directory: {a}")
    rows = fm.get("threat_table") or []
    rowtext = "\n".join((r.get("control") or "") + " " + (r.get("disposition") or "") for r in rows)
    reset_of = fm.get("reset_of") or []
    for rid in reset_of + [tid] if reset_of else []:
        if not re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext):
            fails.append(f"C3 no threat_table row names {rid} task.md")
    for a in allowed:
        # a row's control names the entry only at a path boundary: scripts/foo.py.bak does not name scripts/foo.py
        named = re.compile(re.escape(a.split("*")[0].rstrip("/")) + r"(?=$|[ /\"'(),*?\[])")
        if rows and not any(named.search(r.get("control") or "") for r in rows):
            fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
    dr = fm.get("design_review") or {}
    if dr.get("design") and dr.get("receipt") and (design := root / dr["design"]).exists():
        cur = (front(design.read_text()).get("design_review") or {}).get("receipt")
        if cur and cur != dr["receipt"]:
            fails.append(f"C6 design_review.receipt {dr['receipt']} is not the design's current receipt {cur}")
    for r in rows:
        m = re.search(r"names the (a\d\d) file's hash", r.get("disposition") or "")
        if m and m.group(1) != suffix:
            fails.append(f"C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get('control')[:60]}")
    controls = " || ".join((r.get("control") or "") for r in rows)
    for name in C7_NAMES:
        if rows and name not in controls.lower():
            fails.append(f"C7 threat_table has no row named for: {name}")
    prefixes = [re.sub(r"(/\*\*|/\*|\*)$", "", e) for e in allowed if isinstance(e, str)]
    for r in rows:
        if (r.get("control") or "").lstrip('"').startswith(NONPATH):
            continue  # a non-path control may describe several files
        hit = [e for e in prefixes if e and e in (r.get("control") or "")]
        if len(hit) > 1:
            fails.append(f"C7b one row names {len(hit)} allowed_files entries ({', '.join(hit)}); one row per entry")
    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
    if fm.get("kind") == "code":
        for var in sorted(set(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_EVIDENCE\b", body))):
            # an input a script on origin/main already reads is not an added input
            added = git(root, "grep", "-q", var, "origin/main", "--", "scripts", "Makefile", "home").returncode != 0
            if added and rows and var not in controls:
                fails.append(f"C8 the task adds input {var} but no threat row controls it")
    sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
    for sent in sentences:  # C10
        for scr in set(re.findall(r"scripts/[\w./-]+\.(?:sh|py)", sent)):
            if git(root, "cat-file", "-e", f"origin/main:{scr}").returncode:
                continue
            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
            if m and scr in sent[m.start() :]:
                continue  # the script is named inside its own landing clause
            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
                if git(root, "grep", "-qF", lit, "origin/main", "--", scr, test).returncode:
                    why = f"which neither the script nor {test} carries on origin/main"
                    fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
    for sent in sentences:  # C9
        if re.search(r"\b(once|until)\b", sent):
            continue
        for n in set(re.findall(C9_NAMES, sent)):
            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
            if probe.startswith("scripts/"):
                ok = git(root, "cat-file", "-e", f"origin/main:{probe}").returncode == 0
            elif probe.endswith("_EVIDENCE"):
                ok = git(root, "grep", "-q", probe, "origin/main", "--", "scripts", "Makefile").returncode == 0
            else:
                mistakes = ("grep", "-q", "^classes:", "origin/main", "--", ".orchestration/learning/mistakes")
                ok = probe == "classes:" and git(root, *mistakes).returncode == 0
            if not ok:
                why = "it is not on origin/main and the sentence has no landing condition"
                fails.append(f'C9 rule sentence names {n} as present but {why}: "{sent[:70]}…"')
    for r in rows:  # C13, then C11 on the form it found
        d = str(r.get("disposition") or "")
        form = next((f for f in FORMS if d.startswith(f)), None)
        if form is None:
            fails.append(f"C13 disposition is not closed:, residual: or out-of-scope: and a space: {d[:60]}")
            continue
        load = d[len(form) :]
        if form == "closed: " and not re.fullmatch(r"tests/[\w./-]+::[A-Za-z_]\w*", load):
            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
        if form == "out-of-scope: " and not tid_ok:
            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
        if form == "residual: " and len(load) < 20:
            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
    for a in allowed:  # C12
        last = a.rsplit("/", 1)[-1]
        glob = re.search(r"[*?\[]", a) and not a.startswith(("tests/fixtures/", own_dir))
        if glob and (last.endswith(APPLIED) or a.startswith(("home/", "scripts/", ".githooks/", ".github/"))):
            for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
                if not any(re.search(re.escape(f) + r"(?=$|[ /\"'(),])", r.get("control") or "") for r in rows):
                    fails.append(f"C12 the glob {a} matches {f}, which no threat_table row names")
    for pre in fm.get("premises") or []:  # C14
        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
        if re.search(r"\b(?:gh|curl)\b|https?://", cmd):
            fails.append(f"{SKIPPED}: {cmd[:60]}")
            continue
        got, code, err = rerun(cmd, root)
        # bash's own line, not exit 127: under pipefail `absent | grep -c` exits with grep's 1.
        if absent := re.search(r"^bash: line \d+: ([^\s:]+): command not found$", err, re.M):
            fails.append(f"{ABSENT} {absent.group(1)}: {cmd[:60]}")
            continue
        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
        if got is None or " ".join(got.split()) != " ".join(want.split()):
            fails.append(f"C14 premise output differs from its rerun: {cmd[:60]}")
    inv, design = fm.get("invariants"), dr.get("design")
    if isinstance(inv, dict) and design:  # C15; a design task carrying its own invariants names no design
        shown = git(root, "show", f"origin/main:{design}")
        canon = (front(shown.stdout).get("invariants") or {}) if shown.returncode == 0 else None
        for k, v in inv.items():
            if canon is None or canon.get(k) != v:
                fails.append(f"C15 invariant {k} is not byte-equal to {design} on origin/main")
    return fails


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
    args = parser.parse_args()
    if args.root is None:
        top = git(args.tasks[0].parent, "rev-parse", "--show-toplevel")
        if top.returncode:
            parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
        args.root = pathlib.Path(top.stdout.strip())
    rc = 0
    for p in args.tasks:
        fails = check(p, args.root)
        bad = [f for f in fails if not f.startswith((SKIPPED, ABSENT))]
        print(f"{p.name}: {'FAIL' if bad else 'OK'}", *fails, sep="\n  ")
        rc |= bool(bad)
    return rc


if __name__ == "__main__":
    sys.exit(main())
