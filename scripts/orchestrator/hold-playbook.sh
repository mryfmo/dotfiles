#!/usr/bin/env bash
# @file hold-playbook.sh
# @brief Expand a class's corrective procedure into a replan skeleton, and record a pending decision when it needs files
#   outside the task's allowed_files.
# @description
#   Plan 024 P1-13 (item (13) of 024-design-programs.md, the class playbook of 024-design-quality.md 5.13). Reads the
#   class's `remedy:` and `blast_radius:` from `.orchestration/learning/classes.yaml` and the task's `allowed_files`
#   from the first YAML front-matter document of `.orchestration/tasks/<task>.md`, both with yaml.safe_load, and
#   creates `.orchestration/tasks/<task>-replan.md`: the cause class, the remedy, each blast-radius glob with the
#   allowed_files entries that cover it (or marked outside allowed_files), a Completion sentence and a four-field
#   `re-plan:` line of `<fill>` placeholders for the orchestrator. The root is the checkout this script lives in.
#   A glob is covered by an entry when every path the glob can name, existing or not, matches the entry under
#   regime-ci.py's allowed(): a trailing `/**` takes any path under its literal prefix, and elsewhere `*` and `?`
#   stay within one path segment. When a glob is uncovered, one six-column row `D-<task>-replan` (basis
#   `hold-playbook`, result `pending`, no default) is appended to `.orchestration/decisions.tsv`.
#   Record text is only read and written as data; the script never edits the task text and never dispatches.
#   With `--check-vocabulary`, it lists every class slug in the `classes:` front-matter lists of `M-*.md` in the
#   mistakes directory that the class file lacks.
# @arg $1 string Task id, matching `^[A-Za-z0-9][A-Za-z0-9._-]*$`.
# @arg $2 string Class slug, a key of classes.yaml's `classes` mapping.
# @option --check-vocabulary <classes.yaml> <mistakes-dir> Check the class file against the mistake records instead.
# @exitcode 0 The replan is written and every glob is inside allowed_files; or the vocabulary covers the records.
# @exitcode 2 Usage error, an invalid task id, a class not in classes.yaml, malformed or missing records; nothing is
#   written. With --check-vocabulary, also a class slug of the records that the class file lacks.
# @exitcode 3 The replan is written and the pending decision row is appended: a glob is outside allowed_files.
# @exitcode 4 The replan destination already exists (a file, a directory or a link); nothing is written.
# @example
#   scripts/orchestrator/hold-playbook.sh dotfiles-T133-hold-playbook-a01 records-form
#   scripts/orchestrator/hold-playbook.sh --check-vocabulary .orchestration/learning/classes.yaml \
#       .orchestration/learning/mistakes
set -euo pipefail

usage() {
    echo "usage: hold-playbook.sh <task> <class> | hold-playbook.sh --check-vocabulary <classes.yaml> <mistakes-dir>" >&2
    exit 2
}
if (($# == 3)) && [[ $1 == --check-vocabulary ]]; then
    set -- vocabulary "$2" "$3"
elif (($# == 2)); then
    [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || {
        echo "hold-playbook: invalid task id; refused" >&2
        exit 2
    }
    set -- plan "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)" "$1" "$2"
else
    usage
fi
exec uv run --no-project --with pyyaml python -I - "$@" << 'PY'
import csv
import datetime
import functools
import os
import sys
from pathlib import Path

import yaml

STAR, QMARK, ANY = object(), object(), object()


def fail(message, code=2):
    print(f"hold-playbook: {message}; refused", file=sys.stderr)
    sys.exit(code)


def load(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        fail(f"cannot read {path}: {error.__class__.__name__}")


def front(path):
    """The first YAML front-matter document: the lines between the file's first `---` line and the next."""
    lines = load(path).split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        fail(f"{path} has no front matter")
    try:
        return yaml.safe_load("\n".join(lines[1 : lines.index("---", 1)]))
    except yaml.YAMLError:
        fail(f"{path}: the front matter is not YAML")


def vocabulary_of(path):
    try:
        classes = yaml.safe_load(load(path))
    except yaml.YAMLError:
        fail(f"{path} is not YAML")
    classes = classes.get("classes") if isinstance(classes, dict) else None
    if not isinstance(classes, dict):
        fail(f"{path} has no classes mapping")
    return classes


def paths(value):
    """Whether value is a list of non-empty strings without tab, newline or carriage return."""
    return isinstance(value, list) and all(isinstance(v, str) and v and not set(v) & set("\t\n\r") for v in value)


def tokens(glob):
    if glob.endswith("/**"):
        return (*glob[:-2], ANY)
    return tuple(STAR if c == "*" else QMARK if c == "?" else c for c in glob)


def covers(entry, glob):
    """Whether every path glob can name matches entry: each token of glob is absorbed by an entry token whose set holds
    it. shortcut: sound but not complete (`?*` under `*?` reads as outside), so the orchestrator decides such a glob."""
    a, g = tokens(entry), tokens(glob)

    @functools.cache
    def absorbs(i, j):
        if i == len(a):
            return j == len(g)
        if a[i] is ANY:
            return True
        if a[i] is STAR:
            return absorbs(i + 1, j) or (j < len(g) and g[j] is not ANY and g[j] != "/" and absorbs(i, j + 1))
        if j == len(g):
            return False
        if a[i] is QMARK:
            return (g[j] is QMARK or isinstance(g[j], str) and g[j] != "/") and absorbs(i + 1, j + 1)
        return isinstance(g[j], str) and g[j] == a[i] and absorbs(i + 1, j + 1)

    return absorbs(0, 0)


def plan(root, task, cls):
    o = Path(root) / ".orchestration"
    classes = vocabulary_of(o / "learning/classes.yaml")
    if cls not in classes:
        fail(f"class {cls!r} is not in .orchestration/learning/classes.yaml")
    entry = classes[cls] if isinstance(classes[cls], dict) else {}
    remedy, radius = entry.get("remedy"), entry.get("blast_radius")
    if not isinstance(remedy, str) or not remedy.strip() or not paths(radius):
        fail(f"class {cls!r} has no remedy string or no blast_radius list of globs")
    meta = front(o / f"tasks/{task}.md")
    allowed = meta.get("allowed_files") if isinstance(meta, dict) else None
    if not paths(allowed):
        fail(f".orchestration/tasks/{task}.md has no allowed_files list of paths")
    ledger = o / "decisions.tsv"
    if not load(ledger).startswith("id\twhen\twhat\twhy\tbasis\tresult\n"):
        fail(".orchestration/decisions.tsv does not start with its six-column header")
    scope = [(glob, [a for a in allowed if covers(a, glob)]) for glob in radius]
    outside = [glob for glob, by in scope if not by]
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    unknown = remedy == "unknown"
    lines = [
        f"# Re-plan skeleton: {task}",
        "",
        f"Written by `scripts/orchestrator/hold-playbook.sh {task} {cls}` at {now}. It is a proposal until the"
        f" orchestrator replaces every `<fill>`; the task text `.orchestration/tasks/{task}.md` is unchanged.",
        "",
        "## Cause",
        "",
        f"- class: `{cls}`",
        "- remedy: unknown (classes.yaml records no corrective procedure for this class)" if unknown else f"- remedy: {remedy}",
        "",
        "## Scope",
        "",
        *(
            f"- `{glob}`: inside allowed_files ({', '.join(f'`{a}`' for a in by)})" if by else f"- `{glob}`: outside allowed_files"
            for glob, by in scope
        ),
        *([] if scope else ["- none: the class's blast_radius is empty"]),
        "",
        "## Completion",
        "",
        "<fill: the observable result>, verified by <fill: test selectors>, with the evidence in <fill: evidence paths>.",
        "",
        "re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>",
        "",
    ]
    dest = o / f"tasks/{task}-replan.md"
    try:
        fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # O_EXCL refuses any entry, a link included
    except FileExistsError:
        fail(f".orchestration/tasks/{task}-replan.md exists", 4)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))
    report = f"hold-playbook: wrote .orchestration/tasks/{task}-replan.md for class {cls}"
    if unknown:
        report += " (remedy: unknown, blast_radius: [])"
    if not outside:
        print(f"{report}; every blast_radius glob is inside allowed_files")
        return 0
    row = [
        f"D-{task}-replan",
        now,
        f"the re-plan of {task} needs files outside its allowed_files: " + ", ".join(f"`{g}`" for g in outside),
        f"the blast_radius of class `{cls}` (classes.yaml) reaches beyond the task's allowed_files",
        "hold-playbook",
        "pending",
    ]
    try:
        tail = ledger.read_bytes()[-1:]
        with ledger.open("a", encoding="utf-8", newline="") as out:
            out.write("" if tail == b"\n" else "\n")
            csv.writer(out, delimiter="\t", lineterminator="\n").writerow(row)
    except BaseException:
        dest.unlink()  # a replan without its decision row would make every rerun exit 4 with no decision recorded
        raise
    print(f"{report}; outside allowed_files: {', '.join(outside)}; appended D-{task}-replan (pending) to decisions.tsv")
    return 3


def vocabulary(path, mistakes):
    known = vocabulary_of(Path(path))
    records = sorted(Path(mistakes).glob("M-*.md"))
    if not records:
        fail(f"{mistakes} holds no M-*.md record")
    found = {}
    for record in records:
        meta = front(record)
        slugs = meta.get("classes", []) if isinstance(meta, dict) else None
        if not paths(slugs):
            fail(f"{record.name}: classes is not a list of slugs")
        for slug in slugs:
            found.setdefault(slug, []).append(record.name)
    missing = sorted(set(found) - set(known))
    for slug in missing:
        print(f"hold-playbook: class {slug} of {', '.join(found[slug])} is not in {path}", file=sys.stderr)
    if missing:
        return 2
    print(f"hold-playbook: {path} holds the {len(found)} classes of {len(records)} mistake records")
    return 0


sys.exit(plan(*sys.argv[2:]) if sys.argv[1] == "plan" else vocabulary(*sys.argv[2:]))
PY
