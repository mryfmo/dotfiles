"""Read-only format-2 task checks under --root; --premises-sha authorizes only fixed read-only C14 probes.

C1 task-id filename; C2 own evidence scope; C3 reset-copy rows; C4 scope rows; C5 own hash; C6 confined design receipt.
C7 non-path/effect rows; C7b one path per row; C8 new evidence inputs; C9 landed rule references; C10 literal probes.
C11 dispositions accept tests/<path>::<test> or tests/<path>::<Class>::<test>, existing owners and 20-character residuals.
C12 concrete applied glob matches; C13 disposition grammar; C14 fixed Git/test/grep probes on the same hashed bytes.
C15 design-assigned invariant ids and byte-equal sentences. Without the dispatched hash C14 warns and runs no probe.
"""

import argparse
import base64
import hashlib
import json
import os
import pathlib
import pwd
import re
import shlex
import subprocess
import sys
import tempfile
import unicodedata
from functools import cache
from urllib.parse import quote

CACHE = os.environ.get("UV_CACHE_DIR", "")
if not os.path.isabs(CACHE):
    sys.exit("refused: UV_CACHE_DIR must be set to an absolute path")
PYTHON = os.environ.get("TRUSTED_PYTHON", "")
if not os.path.isabs(PYTHON) or not os.path.isfile(PYTHON):
    sys.exit("refused: TRUSTED_PYTHON must be set to an absolute regular file")

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
TRUST_ROOT = pathlib.Path(__file__).resolve().parents[2]
HOST_HOME = pathlib.Path(pwd.getpwuid(os.getuid()).pw_dir)
FORMS = ("closed: ", "residual: ", "out-of-scope: ")
APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
UNTRUSTED = "C14: not run (no trusted sha)"  # a warning: the file is not the text --premises-sha names (revise 1)


def applied(path):
    """An executed or applied file, by its kind or its place (C12 and task-from-plan.py's concrete rows)."""
    return normalise_name(path).endswith(APPLIED) or normalise_name(path).startswith(APPLIED_DIRS)


def normalise_name(value):
    """Canonical Unicode for logical name tokens; preserve ref, separator and wildcard grammar."""
    return unicodedata.normalize("NFC", value)


def confined(root, rel):
    """The path resolved under root, or None when it leaves the checkout (PR #418's review)."""
    path = (root / rel).resolve()
    return path if any(p.exists() and os.path.samefile(p, root) for p in (path, *path.parents)) else None


def front(text):
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))


def git(cwd, *args):
    root = pathlib.Path(cwd).resolve()
    if (root / ".gitmodules").exists() or (root / ".gitmodules").is_symlink():
        sys.exit("refused: .gitmodules")
    flags = ["-C", str(root), f"--git-dir={root / '.git'}", f"--work-tree={root}"]
    for setting in (
        "core.hooksPath=/dev/null",
        "core.fsmonitor=false",
        "submodule.recurse=false",
        "protocol.allow=never",
        "protocol.https.allow=always",
    ):
        flags += ["-c", setting]
    binary = executable("git")

    def checked(extra):
        config = launch(root, binary, *flags, "config", "--show-origin", "--get-regexp", r"^filter\.|^core\.worktree$")
        if config.returncode not in (0, 1) or config.stdout:
            origins = "\n".join(
                origin + "\t" + value.split()[0]
                for line in config.stdout.splitlines()
                for origin, _, value in [line.partition("\t")]
            )
            sys.exit("refused: Git configuration: " + origins + config.stderr)
        return launch(root, binary, *flags, *extra)

    top = checked(["rev-parse", "--show-toplevel"])
    if top.returncode or not os.path.samefile(top.stdout.strip(), root):
        sys.exit(f"refused: Git toplevel {top.stdout.strip()} != {root}")
    if args[0] == "status":
        args = ("--no-optional-locks", "status", "--ignore-submodules=all", *args[1:])
    if args[0] in ("show", "diff"):
        flags += ["-c", "core.attributesFile=/dev/null", "-c", "core.sshCommand=false"]
        args = (
            args[0],
            "--no-ext-diff",
            "--no-textconv",
            *(["--ignore-submodules=all"] if args[0] == "diff" else []),
            *args[1:],
        )
    return checked(args)


def trusted(path):
    if not pathlib.Path(path).is_absolute():
        sys.exit("refused: trusted path must be absolute")
    if "shims" in pathlib.Path(path).parts:
        sys.exit(f"refused: shim trusted path: {path}")
    path = pathlib.Path(path).resolve(strict=True)
    manifest = TRUST_ROOT / "home/dot_agents/agent-config.yaml"
    worker = (yaml.safe_load(manifest.read_text()) or {}).get("worker_worktree") if manifest.is_file() else None
    if (
        ".claude/worktrees" in os.path.realpath(path).casefold()
        or "shims" in path.parts
        or (worker and (TRUST_ROOT / worker).exists() and confined(TRUST_ROOT / worker, path) is not None)
    ):
        sys.exit(f"refused: worker-root trusted path: {path}")
    if not path.is_file():
        sys.exit(f"refused: trusted file required: {path}")
    return path


PYTHON = trusted(PYTHON)
if not os.access(PYTHON, os.X_OK):
    sys.exit("refused: trusted interpreter is not executable")


@cache
def executable(name):
    directory = pathlib.Path(os.environ.get("TRUSTED_BIN_DIR", ""))
    binding = directory / name
    if not directory.is_absolute() or not binding.is_symlink() or not binding.is_file():
        sys.exit(f"refused: trusted executable binding missing: {name}")
    binary = trusted(binding)
    if not os.access(binary, os.X_OK):
        sys.exit(f"refused: trusted executable binding is not executable: {name}")
    return binary


def launch(root, binary, *args):
    binary = trusted(binary)
    if confined(pathlib.Path(root).resolve(), binary) is not None:
        sys.exit("refused: checkout executable binding")
    os.makedirs(CACHE, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=CACHE, prefix="exec-") as directory:
        for name in ("git", "uv", "gh"):
            if pathlib.Path(os.environ.get("TRUSTED_BIN_DIR", ""), name).is_symlink():
                target = executable(name)
                if confined(pathlib.Path(root).resolve(), target) is not None:
                    sys.exit("refused: checkout executable binding")
                pathlib.Path(directory, name).symlink_to(target)
        env = {
            "HOME": str(HOST_HOME),
            "PATH": directory,
            "LANG": "C.UTF-8",
            "UV_CACHE_DIR": CACHE,
            "TRUSTED_PYTHON": str(PYTHON),
            "TRUSTED_BIN_DIR": directory,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_NO_LAZY_FETCH": "1",
        }
        return subprocess.run(
            [str(trusted("/usr/bin/env")), "-i", *(f"{k}={v}" for k, v in env.items()), str(binary), *map(str, args)],
            cwd=root,
            env={},
            capture_output=True,
            text=True,
            check=False,
        )


@cache
def main_sha(root):
    result = launch(root, executable("gh"), "api", "repos/mryfmo/dotfiles/git/ref/heads/main", "--jq", ".object.sha")
    sha = result.stdout.strip()
    if result.returncode or not re.fullmatch(r"[0-9a-f]{40}", sha):
        sys.exit("refused: canonical main SHA unavailable: " + result.stderr)
    print(f"canonical-main {sha}", file=sys.stderr)
    return sha


@cache
def main_entry(root, name):
    if pathlib.PurePosixPath(name).is_absolute() or ".." in pathlib.PurePosixPath(name).parts:
        sys.exit("refused: canonical contents path")
    endpoint = f"repos/mryfmo/dotfiles/contents/{quote(name, safe='/')}?ref={main_sha(root)}"
    result = launch(root, executable("gh"), "api", endpoint)
    digest = hashlib.sha256((result.stdout + result.stderr).encode()).hexdigest()
    print(f"api-input-sha256 {endpoint} exit={result.returncode} {digest}", file=sys.stderr)
    if result.returncode:
        if "HTTP 404" in result.stderr:
            return None
        sys.exit("refused: canonical contents unavailable: " + result.stderr)
    try:
        entry = json.loads(result.stdout)
    except ValueError:
        sys.exit("refused: invalid canonical contents response")
    if not isinstance(entry, (dict, list)):
        sys.exit("refused: invalid canonical contents response")
    return entry


def main_text(root, name):
    entry = main_entry(root, name)
    if entry is None:
        return None
    if not isinstance(entry, dict) or entry.get("encoding") != "base64" or not isinstance(entry.get("content"), str):
        sys.exit(f"refused: canonical file unavailable: {name}")
    try:
        return base64.b64decode("".join(entry["content"].split()), validate=True).decode(errors="replace")
    except ValueError:
        sys.exit(f"refused: invalid canonical file encoding: {name}")


def main_texts(root, name):
    entry = main_entry(root, name)
    if isinstance(entry, list):
        for child in entry:
            if not normalise_name(child["path"]).startswith(normalise_name(name).rstrip("/") + "/"):
                sys.exit("refused: canonical directory child")
            yield from main_texts(root, child["path"])
    elif entry is not None:
        yield main_text(root, name)


def main_contains(root, pattern, names, literal=False):
    return any(
        pattern in text if literal else re.search(pattern, text, re.MULTILINE)
        for name in names
        for text in main_texts(root, name)
    )


def repository(path):
    path = pathlib.Path(path).resolve()
    return next(p for p in (path, *path.parents) if (p / ".git").exists())


def snapshot(path, expected=None):
    data = trusted(path).read_bytes()
    if expected is not None and hashlib.sha256(data).digest() != expected:
        sys.exit("refused: consumed bytes changed")
    if confined(TRUST_ROOT, pathlib.Path(path)) is None:
        sys.exit("refused: trusted content outside its root")
    fd, name = tempfile.mkstemp(dir=pathlib.Path(path).parent, suffix=pathlib.Path(path).suffix)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
    print(f"input-sha256 {pathlib.Path(path).name} {hashlib.sha256(data).hexdigest()}", file=sys.stderr)
    return pathlib.Path(name), hashlib.sha256(data).digest()


def consume(binding):
    path, digest = binding
    if hashlib.sha256(path.read_bytes()).digest() != digest:
        sys.exit("refused: consumed bytes changed")
    return path


def rerun(cmd, cwd):
    """Interpret four read-only probe forms; task text is never shell or Python code."""
    try:
        words = shlex.split(cmd)
        syntax = shlex.shlex(cmd, posix=False, punctuation_chars=";&|<>`$()")
        syntax.whitespace_split = True
        if any(re.fullmatch(r"[;&|<>`$()]+", token) for token in syntax):
            words = []
    except ValueError:
        words = []
    if (
        len(words) == 3
        and words[:2] == ["git", "rev-parse"]
        and not words[2].startswith("-")
        and not re.search(r"[\s;$`|&<>]", words[2])
    ):
        run = git(cwd, "rev-parse", "--verify", "--end-of-options", words[2])
        return run.stdout, run.returncode, run.stderr
    if (len(words) == 3 and words[:2] in (["test", "-e"], ["test", "-f"])) or (
        len(words) == 4 and words[:2] == ["grep", "-c"]
    ):
        path = confined(pathlib.Path(cwd), words[-1])
        if path is not None:
            if words[0] == "test":
                return "", int(not (path.exists() if words[1] == "-e" else path.is_file())), ""
            if len(words) == 4 and path.is_file():
                with path.open("rb") as stream:
                    return str(sum(words[2].encode() in line.removesuffix(b"\n") for line in stream)) + "\n", 0, ""
    return None, 1, f"C14 unsupported or unconfined probe: {cmd}"


def check(p, root, premises_sha=None):
    fm = front(text := (data := p.read_bytes()).decode())
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
    inside = dr.get("design") and confined(root, dr["design"])
    if dr.get("design") and not inside:
        fails.append(f"C6 design path {dr['design']} is outside the checkout")
    elif inside and dr.get("receipt") and inside.exists():
        cur = (front(inside.read_text()).get("design_review") or {}).get("receipt")
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
            added = not main_contains(root, var, ("Makefile", "scripts", "home"))
            if added and rows and var not in controls:
                fails.append(f"C8 the task adds input {var} but no threat row controls it")
    sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
    for sent in sentences:  # C10
        for scr in set(re.findall(r"scripts/[\w./-]+\.(?:sh|py)", sent)):
            if not confined(root, scr):
                fails.append(f"C10 rule sentence names {scr}, a path outside the checkout")
                continue
            if main_entry(root, scr) is None:
                continue
            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
            if m and scr in sent[m.start() :]:
                continue  # the script is named inside its own landing clause
            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
                # Canonical bytes are searched literally; option-shaped text never reaches a command line.
                if not main_contains(root, lit, (scr, test), literal=True):
                    why = f"which neither the script nor {test} carries on origin/main"
                    fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
    for sent in sentences:  # C9
        if re.search(r"\b(once|until)\b", sent):
            continue
        for n in set(re.findall(C9_NAMES, sent)):
            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
            if probe.startswith("scripts/"):
                ok = main_entry(root, probe) is not None
            elif probe.endswith("_EVIDENCE"):
                ok = main_contains(root, probe, ("Makefile", "scripts"))
            else:
                ok = probe == "classes:" and main_contains(root, "^classes:", (".orchestration/learning/mistakes",))
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
        if form == "closed: " and not re.fullmatch(r"tests/[\w./-]+::(?:[A-Za-z_]\w*::)?[A-Za-z_]\w*", load):
            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
        if form == "out-of-scope: " and not tid_ok:
            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
        if form == "residual: " and len(load) < 20:
            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
    for a in allowed:  # C12: the concrete matches decide, not what the glob spells
        if not re.search(r"[*?\[]", a) or a.startswith(("tests/fixtures/", own_dir)) or not confined(root, a):
            continue
        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
            named = any(re.search(re.escape(f) + r"(?=$|[ /\"'(),])", r.get("control") or "") for r in rows)
            if applied(f) and not f.startswith(("tests/fixtures/", own_dir)) and not named:
                fails.append(f"C12 the glob {a} matches {f}, which no threat_table row names")
    premises = fm.get("premises") or []
    # C14 executes premise commands only for the orchestrator's dispatched text, the bytes whose sha256 the caller
    # passes (dispatch.sh: the TASK line's task_sha256); a branch copy at acceptance passes none, so nothing runs.
    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
        fails.append(UNTRUSTED)
        premises = []
    for pre in premises:  # C14
        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
        got, _code, err = rerun(cmd, root)
        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
        if got is None or " ".join(got.split()) != " ".join(want.split()):
            fails.append(err if got is None else f"C14 premise output differs from its rerun: {cmd}")
    design, mine = dr.get("design"), fm.get("invariants") if isinstance(fm.get("invariants"), dict) else {}
    shown = main_text(root, design) if inside else None
    present = shown is not None
    # C15: a design main cannot give leaves a task's invariants unchecked, and a path naming no design on main or in
    # this checkout is a typo for any task; a design still in flight here assigns nothing yet to a task without any.
    if inside and not present:
        fails += [f"C15 design {design} is not on origin/main"] if mine or not (present or inside.exists()) else []
    elif present:  # the design's assignment fixes the ids; a design task compares its own definitions
        dfm = front(shown) if shown.startswith("---\n") else None
        dfm = dfm if isinstance(dfm, dict) else {}
        canon, assigned = dfm.get("invariants") or {}, dfm.get("implementing_tasks")
        ids = (assigned.get(tid) or []) if isinstance(assigned, dict) and fm.get("kind") != "design" else None
        if ids is not None:
            fails += [f"C15 invariant {k} that {design} assigns to {tid} is missing" for k in ids if k not in mine]
            fails += [f"C15 invariant {k} is not one {design} assigns to {tid}" for k in mine if k not in ids]
        bad = [k for k, v in mine.items() if (ids is None or k in ids) and canon.get(k) != v]
        fails += [f"C15 invariant {k} is not byte-equal to {design} on origin/main" for k in bad]
    return fails


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
    args = parser.parse_args()
    top = git(args.root or repository(args.tasks[0].parent), "rev-parse", "--show-toplevel")
    if top.returncode:
        parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
    args.root = pathlib.Path(top.stdout.strip())
    rc = 0
    for p in args.tasks:
        fails = check(p, args.root, args.premises_sha)
        notes = [f for f in fails if f.startswith(UNTRUSTED)]
        bad = [f for f in fails if f not in notes]
        print(f"{p.name}: {'FAIL' if bad else 'OK'}", *bad, sep="\n  ")
        # The severity is explicit: an untrusted or absent-tool premise is a warning, a network premise a skip note.
        severity = dict.fromkeys(notes, "warning")
        print(*(f"{p.name}: {severity[n]}: {n}" for n in notes), sep="\n", file=sys.stderr, end="\n" if notes else "")
        rc |= bool(bad)
    return rc


if __name__ == "__main__":
    sys.exit(main())
