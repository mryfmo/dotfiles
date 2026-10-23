"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).

`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
reads canonical GitHub design/baseline bytes (C6, C8 to C10) under --root (default: the first file's git
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
"""

import argparse
import base64
import fnmatch
import hashlib
import json
import os
import pathlib
import pwd
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from functools import cache
from urllib.parse import quote

CACHE = os.environ.get("UV_CACHE_DIR")

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


def normalise_name(value):
    if not isinstance(value, str):
        return None
    parts = value.split("/")
    if not value or pathlib.PurePosixPath(value).is_absolute() or "\0" in value or ".." in parts or "\\" in value:
        return None
    name = "/".join(p for p in parts if p not in ("", "."))
    if not name or name[0] in ":!":
        return None
    return unicodedata.normalize("NFC", name) + ("/" if value.endswith(("/", "/.")) else "")


def confined(root, rel):
    if not root.exists():
        return None
    path = (root / rel).resolve()
    return next(
        ((path, path.relative_to(p)) for p in (path, *path.parents) if p.exists() and os.path.samefile(p, root)), None
    )


def path_entry(root, value, fold=os.path.normcase):
    raw = root / value if isinstance(value, pathlib.Path) or normalise_name(value) else None
    found = confined(root, raw) if raw is not None else None
    key = fold(unicodedata.normalize("NFC", raw.relative_to(root).as_posix())) if raw is not None else None
    if key and str(value).endswith(("/", "/.")):
        key += "/"
    return raw, found[0] if found else None, key


def front(text):
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))


def trusted(path):
    raw = pathlib.Path(path)
    path = raw.resolve()
    if not raw.is_absolute() or "shims" in raw.parts or "shims" in path.parts:
        sys.exit("refused: absolute non-shim trusted path required")
    manifest = TRUST_ROOT / "home/dot_agents/agent-config.yaml"
    worker = (yaml.safe_load(manifest.read_text()) or {}).get("worker_worktree") if manifest.is_file() else None
    if ".claude/worktrees" in os.path.normpath(path).casefold() or (
        worker and confined(TRUST_ROOT / worker, path) is not None
    ):
        sys.exit("refused: worker-root trusted path")
    if not path.is_file() or not os.access(path, os.X_OK):
        sys.exit("refused: trusted executable must be an absolute regular executable file")
    return path


resolver = TRUST_ROOT / "scripts/orchestrator/trusted-interpreter.sh"
if resolver.exists() or resolver.is_symlink():
    command = ["/bin/bash", "--noprofile", "--norc", "-p", str(trusted(resolver))]
    env = {"PATH": "/usr/bin:/bin", "HOME": str(HOST_HOME), "LANG": "C.UTF-8"}
    result = subprocess.run(command, env=env, capture_output=True, text=True, check=False)
    if result.returncode:
        sys.exit("refused: interpreter resolver failed: " + result.stderr)
    selected = result.stdout.strip()
elif "TRUSTED_PYTHON" in os.environ:
    selected = os.environ["TRUSTED_PYTHON"]
else:
    selected = os.path.realpath(sys.executable)
    print("warning: interpreter fallback to real sys.executable", file=sys.stderr)
PYTHON = trusted(selected)


@cache
def executable(name):
    supplied = os.environ.get("TRUSTED_BIN_DIR")
    path = pathlib.Path(supplied) / name if supplied is not None else shutil.which(name)
    if not path or (supplied and (not os.path.isabs(supplied) or not path.is_symlink())):
        sys.exit("refused: trusted executable binding missing: " + name)
    return trusted(path)


def launch(root, binary, *args):
    binary = trusted(binary)
    if confined(pathlib.Path(root).resolve(), binary) is not None:
        sys.exit("refused: checkout executable binding")
    if CACHE is not None:
        if not os.path.isabs(CACHE):
            sys.exit("refused: UV_CACHE_DIR must be an absolute path")
        os.makedirs(CACHE, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=CACHE, prefix="checker-") as directory:
        env = {"HOME": str(HOST_HOME), "PATH": directory, "LANG": "C.UTF-8", "UV_CACHE_DIR": CACHE or directory}
        env.update(
            v.split("=", 1)
            for v in "GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1".split()
        )
        if args and args[0] == "api":
            env.update({k: os.environ[k] for k in ("GH_TOKEN", "GITHUB_TOKEN") if k in os.environ})
        return subprocess.run(
            [str(binary), *map(str, args)], cwd=root, env=env, capture_output=True, text=True, check=False
        )


def git(cwd, *args):
    root = pathlib.Path(cwd).resolve()
    if (root / ".gitmodules").exists() or (root / ".gitmodules").is_symlink():
        sys.exit("refused: .gitmodules")
    flags = ["-C", str(root), f"--git-dir={root / '.git'}", f"--work-tree={root}"]
    for setting in "core.hooksPath=/dev/null core.fsmonitor=false submodule.recurse=false protocol.allow=never protocol.https.allow=always".split():
        flags += ["-c", setting]
    binary = executable("git")
    config = launch(root, binary, *flags, "config", "--show-origin", "--get-regexp", r"^filter\.|^core\.worktree$")
    if config.returncode not in (0, 1) or config.stdout:
        sys.exit("refused: Git configuration: " + config.stdout + config.stderr)
    top = launch(root, binary, *flags, "rev-parse", "--show-toplevel")
    if top.returncode or not os.path.samefile(top.stdout.strip(), root):
        sys.exit("refused: Git toplevel mismatch")
    return launch(root, binary, *flags, *args)


@cache
def main_entry(root, name=None):
    if name is None:
        endpoint, args = "git/ref/heads/main", ("--jq", ".object.sha")
    else:
        if not normalise_name(name):
            sys.exit("refused: canonical path")
        name = pathlib.PurePosixPath(name).as_posix()
        endpoint, args = f"contents/{quote(name.rstrip('/'), safe='/')}?ref={main_entry(root)}", ()
    endpoint = "repos/mryfmo/dotfiles/" + endpoint
    result = launch(root, executable("gh"), "api", endpoint, "--hostname", "github.com", *args)
    print("api-input-sha256 " + hashlib.sha256((result.stdout + result.stderr).encode()).hexdigest(), file=sys.stderr)
    if name is None:
        sha = result.stdout.removesuffix("\n")
        if result.returncode or not re.fullmatch(r"[0-9a-f]{40}", sha):
            sys.exit("refused: canonical main SHA unavailable")
        print("canonical-main " + sha, file=sys.stderr)
        return sha
    if result.returncode:
        if "HTTP 404" in result.stderr:
            return None
        sys.exit("refused: canonical contents unavailable")
    try:
        entry = json.loads(result.stdout)
        if not isinstance(entry, (dict, list)):
            raise ValueError()
        return entry
    except ValueError:
        sys.exit("refused: invalid canonical contents response")


@cache
def main_bytes(root, name):
    entry = main_entry(root, name)
    if entry is None:
        return None
    try:
        if not isinstance(entry, dict) or entry.get("encoding") != "base64":
            raise ValueError()
        return base64.b64decode("".join(entry["content"].split()), validate=True)
    except (KeyError, AttributeError, TypeError, ValueError):
        sys.exit("refused: invalid canonical file bytes")


def main_texts(root, name):
    entry = main_entry(root, name)
    if isinstance(entry, list):
        for child in entry:
            path = child["path"]
            if not normalise_name(path) or not normalise_name(path).startswith(normalise_name(name).rstrip("/") + "/"):
                sys.exit("refused: canonical directory child")
            yield from main_texts(root, path)
    elif entry is not None:
        yield main_bytes(root, name).decode()


def main_contains(root, pattern, names, literal=False):
    texts = (text for name in names for text in main_texts(root, name))
    return any(pattern in text if literal else re.search(pattern, text, re.MULTILINE) for text in texts)


def match(name, pattern, partial=False, fold=os.path.normcase):
    names = fold(unicodedata.normalize("NFC", name)).split("/")
    parts = fold(normalise_name(pattern) + ("**" if normalise_name(pattern).endswith("/") else "")).split("/")

    @cache
    def step(i, j):
        if partial and j == len(names):
            return True
        if i == len(parts):
            return j == len(names)
        if parts[i] == "**":
            return step(i + 1, j) or (j < len(names) and step(i, j + 1))
        return j < len(names) and fnmatch.fnmatchcase(names[j], parts[i]) and step(i + 1, j + 1)

    return step(0, 0)


def files(root, pattern, fold=os.path.normcase):
    if not re.search(r"[*?\[]", pattern) and not (root / pattern).exists() and not (root / pattern).is_symlink():
        yield root / pattern
        return

    def unreadable(error):
        raise error

    for folder, dirs, names in os.walk(root, followlinks=False, onerror=unreadable):
        base = pathlib.Path(folder)
        links = [n for n in dirs if (base / n).is_symlink()]
        dirs[:] = [n for n in dirs if fold(n) != ".git" and n not in links]
        dirs[:] = [n for n in dirs if match(path_entry(root, base / n, fold)[2], pattern, True, fold)]
        for name in [*names, *links]:
            if fold(name) != fold(".git"):
                yield base / name


def tokens(control):
    return [
        token.strip(chr(96)) for token in re.findall(r"[^\s\"'(),;]+", control) if normalise_name(token.strip(chr(96)))
    ]


def hits(control, allowed, root, fold=os.path.normcase):
    prefixes = {a: re.split(r"[*?\[]", a, maxsplit=1)[0].rstrip("/") for a in allowed}
    found = set()
    for raw in tokens(control):
        _, target, token = path_entry(root, raw, fold)
        choices = [
            a
            for a, p in prefixes.items()
            if token in (fold(a), fold(p))
            or match(token, a, fold=fold)
            and ("/" in normalise_name(token) or target is not None and target.exists())
        ]
        if choices:
            found.add(max(choices, key=lambda a: (a == token, len(prefixes[a]))))
    return found


def rerun(cmd, root):
    try:
        words = shlex.split(cmd)
        syntax = shlex.shlex(cmd, posix=False, punctuation_chars=";&|<>$()" + chr(96))
        syntax.whitespace_split = True
        if any(re.fullmatch(r"[;&|<>$()\x60]+", token) for token in syntax):
            words = []
    except ValueError:
        words = []
    op = words[:2]
    ref = words[2] if len(words) == 3 and op == ["git", "rev-parse"] else ""
    if ref and not ref.startswith("-") and not re.search(r"[\s;$\x60|&<>]", ref):
        run = git(root, "rev-parse", "--verify", "--end-of-options", ref)
        return run.stdout, run.returncode, run.stderr
    if (len(words) == 3 and op in (["test", "-e"], ["test", "-f"])) or (len(words) == 4 and op == ["grep", "-c"]):
        _, path, _ = path_entry(root, words[-1])
        if path is not None:
            if words[0] == "test":
                return "", int(not (path.exists() if words[1] == "-e" else path.is_file())), ""
            if path.is_file():
                with path.open("rb") as stream:
                    return str(sum(words[2].encode() in line.removesuffix(b"\n") for line in stream)) + "\n", 0, ""
    return None, 1, "C14 unsupported or unconfined probe: " + cmd


def check(p, root, premises_sha=None):
    alias = root.with_name(root.name.swapcase())
    fold = str.casefold if alias.exists() and alias.samefile(root) else os.path.normcase
    fm = front(text := (data := p.read_bytes()).decode())
    tid = fm.get("task_id")
    suffix = tid.rsplit("-", 1)[-1]
    fails = []
    if tid != p.stem:
        fails.append(f"C1 task_id {tid} != file {p.stem}")
    allowed = []
    for a in fm.get("allowed_files") or []:
        if name := normalise_name(a):
            allowed.append(name)
        else:
            fails.append(f"C12 confinement: {a}")
    own_dir = f".orchestration/{tid}/"
    if not any(a.startswith(own_dir) for a in allowed):
        fails.append(f"C2 allowed_files lacks {own_dir}**")
    for a in allowed:
        m = re.match(r"\.orchestration/([^/]+)/", a)
        if m and m.group(1) != tid:
            fails.append(f"C2 allowed_files names another task directory: {a}")
    rows = fm.get("threat_table") or []
    rowtext = "\n".join((r.get("control") or "") + " " + (r.get("disposition") or "") for r in rows)
    controls = " || ".join((r.get("control") or "") for r in rows)
    row_paths = [path_entry(root, token, fold) for token in tokens(controls)]
    reset_of = fm.get("reset_of") or []
    for rid in reset_of + [tid] if reset_of else []:
        if not re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext):
            fails.append(f"C3 no threat_table row names {rid} task.md")
    for a in allowed:
        # a row's control names the entry only at a path boundary: scripts/foo.py.bak does not name scripts/foo.py
        named = re.compile(re.escape(fold(a).split("*")[0].rstrip("/")) + r"(?=$|[ /\"'(),*?\[])")
        if rows and not named.search(" ".join(key for _, _, key in row_paths)):
            fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
    dr = fm.get("design_review") or {}
    design = dr.get("design")
    _, design_target, _ = path_entry(root, design)
    if dr.get("design") and design_target is None:
        fails.append("C6 design path is outside the checkout")
        shown = None
    else:
        shown = main_bytes(root, design) if design else None
    dfm = front(shown.decode()) if shown is not None and shown.startswith(b"---\n") else {}
    dfm = dfm if isinstance(dfm, dict) else {}
    if dr.get("receipt") or "design_sha256" in dr:
        cur = (dfm.get("design_review") or {}).get("receipt")
        if shown is None or not cur or dr.get("receipt") != cur:
            fails.append("C6 design_review.receipt has no matching canonical design receipt")
        if "design_sha256" in dr:
            if shown is None or dr["design_sha256"] != hashlib.sha256(shown).hexdigest():
                fails.append("C6 design_sha256 does not match canonical design bytes")
        else:
            print("warning: C6 design_sha256 absent; legacy receipt comparison", file=sys.stderr)
    for r in rows:
        m = re.search(r"names the (a\d\d) file's hash", r.get("disposition") or "")
        if m and m.group(1) != suffix:
            fails.append(f"C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get('control')[:60]}")
    for name in C7_NAMES:
        if rows and name not in controls.lower():
            fails.append(f"C7 threat_table has no row named for: {name}")
    for r in rows:
        if (r.get("control") or "").lstrip('"').startswith(NONPATH):
            continue  # a non-path control may describe several files
        hit = hits(r.get("control") or "", allowed, root, fold)
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
        for scr in set(re.findall(r"scripts/[^\s\"'`,;()]+\.(?:sh|py)", sent)):
            if path_entry(root, scr)[1] is None:
                fails.append(f"C10 rule sentence names {scr}, a path outside the checkout")
                continue
            if main_entry(root, scr) is None:
                continue
            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
            if m and scr in sent[m.start() :]:
                continue  # the script is named inside its own landing clause
            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
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
        selector = re.fullmatch(r"([^:]+)::(?:[A-Za-z_]\w*::)?[A-Za-z_]\w*", load)
        _, target, path = path_entry(root, selector[1] if selector else None)
        if form == "closed: " and not (path and normalise_name(path).startswith("tests/") and target is not None):
            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load)
        owner = path_entry(root, f".orchestration/tasks/{load}.md")[1] if tid_ok else None
        if form == "out-of-scope: " and not (owner is not None and owner.is_file()):
            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
        if form == "residual: " and len(load) < 20:
            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
    resolved_names, entries, seen, collisions = [], {}, {}, set()
    for raw in fm.get("allowed_files") or []:
        _, _, a = path_entry(root, raw, fold)
        if a is None:
            continue
        for file in files(root, raw, fold):
            entry = path_entry(root, file, fold)
            name = entry[2]
            if not (match(name, a, fold=fold) or file.is_symlink() and match(name, a, partial=True, fold=fold)):
                continue
            entries[file] = raw, entry
            prior = seen.setdefault(name, file)
            if prior.parts != file.parts:
                collisions.add(name)
                fails.append(
                    f"C12 path collision: {prior.relative_to(root)} and {file.relative_to(root)} normalise to the same key"
                )
    for file, (raw, (_, target, name)) in entries.items():
        _, scope_target, a = path_entry(root, raw, fold)
        if target is None:
            fails.append(f"C12 confinement: {file.relative_to(root)}")
            continue
        resolved = path_entry(root, target, fold)[2]
        resolved_names.append(resolved)
        exempt = any(
            file.relative_to(root).as_posix().startswith(e)
            and resolved.startswith(fold(e))
            and confined(root / e, target) is not None
            for e in ("tests/fixtures/", own_dir)
        )
        named = name not in collisions and (
            not re.search(r"[*?\[]", raw)
            and scope_target is not None
            and confined(scope_target, target) is not None
            or any(
                key == name and other is not None and other.exists() and target.samefile(other)
                for _, other, key in row_paths
            )
        )
        applied = resolved in map(fold, ("AGENTS.md", "Makefile")) or resolved.endswith(APPLIED)
        applied = applied or any(
            pathlib.PurePosixPath(d) in pathlib.PurePosixPath(resolved).parents for d in APPLIED_DIRS
        )
        applied = applied or match(resolved, ".claude/skills/*/SKILL.md", fold=fold)
        if file.is_symlink() and file.is_dir() or target.is_file() and applied and not exempt and not named:
            fails.append(f"C12 the scope {a} matches unsafe or unnamed {file.relative_to(root)}")
    premises = fm.get("premises") or []
    # Only the caller's dispatched-byte digest authorizes C14; branch bytes supply no authority.
    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
        print(f"{p.name}: warning: {UNTRUSTED}", file=sys.stderr)
        premises = []
    for pre in premises:  # C14
        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
        got, code, err = rerun(cmd, root)
        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
        if got is None or code or " ".join(got.split()) != " ".join(want.split()):
            fails.append(err if got is None else f"C14 premise output differs from its rerun: {cmd}")
    mine = fm.get("invariants") if isinstance(fm.get("invariants"), dict) else {}
    present = shown is not None
    if design and not present:
        fails.append(f"C15 design {design} is not on canonical main")
    elif present:  # the design's assignment fixes the ids; a design task compares its own definitions
        canon, assigned = dfm.get("invariants") or {}, dfm.get("implementing_tasks")
        ids = (assigned.get(tid) or []) if isinstance(assigned, dict) and fm.get("kind") != "design" else None
        if ids is not None:
            fails += [f"C15 invariant {k} that {design} assigns to {tid} is missing" for k in ids if k not in mine]
            fails += [f"C15 invariant {k} is not one {design} assigns to {tid}" for k in mine if k not in ids]
        bad = [k for k, v in mine.items() if (ids is None or k in ids) and canon.get(k) != v]
        fails += [f"C15 invariant {k} is not byte-equal to {design} on origin/main" for k in bad]
    if fm.get("security") is True and (
        any(match("scripts/orchestrator", a, partial=True, fold=fold) for a in allowed)
        or any(fold(n).startswith(fold("scripts/orchestrator/")) for n in resolved_names)
    ):
        if not re.search(r"5\.14[^\n]*(?:reference|参照)", body, re.IGNORECASE):
            fails.append("C16 design 5.14 must apply by reference")
        item_rows = [re.findall(r"5\.14\s+item\s+(\d+)", r.get("control") or "", re.IGNORECASE) for r in rows]
        for i in range(11):
            count = sum(items.count(str(i)) for items in item_rows)
            if count != 1 or any(len(items) > 1 for items in item_rows):
                fails.append(f"C16 item {i}: count {count}; exactly one occurrence and one item per row required")
    return fails


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
    args = parser.parse_args()
    if args.root is None:
        start = args.tasks[0].parent.resolve()
        args.root = next(p for p in (start, *start.parents) if (p / ".git").exists())
    top = git(args.root, "rev-parse", "--show-toplevel")
    if top.returncode:
        parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
    args.root = pathlib.Path(top.stdout.strip())
    rc = 0
    for p in args.tasks:
        fails = check(p, args.root, args.premises_sha)
        print(f"{p.name}: {'FAIL' if fails else 'OK'}", *fails, sep="\n  ")
        rc |= bool(fails)
    return rc


if __name__ == "__main__":
    sys.exit(main())
