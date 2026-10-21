"""The checks behind scripts/orchestrator/pre-send.sh (T133 pre-send-check a03; D-024-51, D-024-56).

Reads one task text once as bytes; every check and the sha256 use that buffer, never a reopened path. Locations come
only from PyYAML marks, fence openers and heading indexes; the consistency checker counts by its exit status alone.
Output is fixed `<check>: refused` labels with line numbers, the fixed helper-failure line, and the digest last. It
catches mistakes; it is no boundary against a hostile same-user process.
"""

import ast
import hashlib
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import yaml

FAILED = "preflight: helper failed (exit 1)"
OPENER = re.compile(r"( {0,3})(`{3,}(?!.*`)|~{3,})(.*)")
ROW = re.compile(r"[^\t ]+\t[^\t ]|- [^ ]")  # an id-tab-class row or a bullet


def normalize(raw):
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def scan(lines):
    """One CommonMark fence pass: the fenced line numbers and each block as (opener line, is shell, body)."""
    fenced, blocks, fence = set(), [], None
    for n, line in enumerate([*lines, None], 1):
        if fence:
            mark, start, shell, indent, body = fence
            if line is None or re.fullmatch(" {0,3}" + re.escape(mark[0]) + "{" + str(len(mark)) + ",}[ \t]*", line):
                blocks.append((start, shell, body))
                fence = None
            else:
                body.append(re.sub("^ {0," + str(indent) + "}", "", line))
            fenced.add(n)
        elif line is not None and (m := OPENER.fullmatch(line)):
            fence = (m[2], n, m[3].split()[:1] in (["bash"], ["sh"]), len(m[1]), [])
            fenced.add(n)
    return fenced, blocks


def front_matter(lines):
    """The YAML mapping between the first two `---` lines, and PyYAML's marks as task line numbers on an error."""
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0) if lines[0] == "---" else 0
    try:
        return (yaml.safe_load("\n".join(lines[1:end])) if end else None), []
    except yaml.MarkedYAMLError as err:
        return None, [m.line + 2 for m in (err.context_mark, err.problem_mark) if m]
    except yaml.YAMLError:
        return None, []


class Task:
    def __init__(self, root, name, raw):
        self.root, self.name, self.raw = root, name, raw
        self.text = normalize(raw)
        self.lines = self.text.split("\n")
        self.fenced, self.blocks = scan(self.lines)
        self.front, self.marks = front_matter(self.lines)
        self.out = []
        self._tree = None

    def refuse(self, label, nums=()):
        nums = sorted({int(n) for n in nums if n})
        self.out.append(f"{label}: refused" + (f" line(s) {','.join(map(str, nums))}" if nums else ""))

    def line_of(self, offset):
        return self.text.count("\n", 0, offset) + 1

    def tree(self):  # the validator parsed once, its module never imported or run
        if self._tree is None:
            try:  # an unreadable validator is a helper failure, not a temp-file one
                source = pathlib.Path(self.root, "scripts/validate-agent-assets.py").read_text("utf-8")
            except OSError as err:
                raise ValueError from err
            self._tree = ast.parse(source)
        return self._tree

    def consistency(self):  # the checker reads a byte-identical snapshot with the same file name; exit status only
        with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as snap:
            copy = pathlib.Path(snap, self.name)
            copy.write_bytes(self.raw)
            checker = f"{self.root}/scripts/orchestrator/task-consistency-check.py"
            cmd = [sys.executable, "-I", checker, "--root", self.root, "--", str(copy)]
            rc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False).returncode
        if rc or self.marks:
            self.refuse("consistency", self.marks)

    def secrets(self):  # the validator's SECRET_PATTERN from its syntax tree, over the complete text and each line
        call = next(
            n.value
            for n in self.tree().body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SECRET_PATTERN"
        )
        flags = ast.literal_eval(call.args[1]) if call.args[1:] else 0
        pattern = re.compile(ast.literal_eval(call.args[0]), flags | re.MULTILINE)
        hits = [
            n for m in pattern.finditer(self.text) for n in range(self.line_of(m.start()), self.line_of(m.end()) + 1)
        ]
        hits += [i for i, line in enumerate(self.lines, 1) if pattern.search(line)]
        if hits:
            self.refuse("secret-pattern", hits)

    def homes(self):  # the validator's compiled_home_path_pattern, run alone with no host home
        fn = next(
            n for n in self.tree().body if isinstance(n, ast.FunctionDef) and n.name == "compiled_home_path_pattern"
        )
        fn.decorator_list, scope = [], {"re": re, "Path": pathlib.Path}
        exec(compile(ast.Module([fn], []), "validate-agent-assets.py", "exec"), scope)  # noqa: S102 (a02 rule: that function alone)
        pattern = scope[fn.name](pathlib.Path(self.root), "")
        hits = [i for i, line in enumerate(self.lines, 1) if pattern.search(line)]
        if hits:
            self.refuse("literal-home", hits)

    def self_cap(self):  # both spellings; wc -l counts the raw buffer's newlines
        cap = re.search(r"at or under \*{0,2}(\d+) lines", self.text)
        if cap and self.raw.count(b"\n") > int(cap[1]):
            self.refuse("self-cap", [self.line_of(cap.start())])

    def shell_syntax(self):  # bash -n on a temporary file under TMPDIR; parsed, never run
        bad = []
        for start, shell, body in self.blocks:
            if not shell:
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".sh", dir=os.environ["TMPDIR"]) as script:
                script.write("\n".join(body) + "\n")
                script.flush()
                cmd = ["/bin/bash", "-n", script.name]
                if subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False).returncode:
                    bad.append(start)
        if bad:
            self.refuse("bash-syntax", bad)

    def owner(self):  # the named record's exact `## Owned by <task_id>` section, up to the next level-two heading
        me = str(self.front.get("task_id") or "") if isinstance(self.front, dict) else ""
        head = f"## Owned by {me}"
        ref = self.text.find(head)
        if not me or ref < 0:
            return
        named = re.search(r"\.orchestration/acceptance/[A-Za-z0-9._-]+\.md", self.text)
        try:
            record = normalize(pathlib.Path(self.root, named[0]).read_bytes()).split("\n") if named else []
        except OSError:
            record = []
        fenced, found, rows, inside = scan(record)[0], False, 0, False
        for n, line in enumerate(record, 1):
            if n in fenced:
                continue
            if line == head or line.startswith(head + " "):
                found = inside = True
                continue
            inside = inside and not re.match(r" {0,3}##(?:[ \t]|$)", line)
            rows += inside and bool(ROW.match(line))
        items = sum(
            1 for n, line in enumerate(self.lines, 1) if n not in self.fenced and re.match(r" {0,3}## Item", line)
        )
        if not found or not rows and items <= 1:
            self.refuse("owner-section", [self.line_of(ref)])


def main(args):
    if len(args) != 2:
        print("input: refused")
        return 1
    root, name = args
    try:
        raw = pathlib.Path(name).read_bytes()
    except OSError:
        print("input: refused")
        return 1
    try:
        task = Task(root, pathlib.Path(name).name, raw)
        for check in (task.consistency, task.secrets, task.homes, task.self_cap, task.shell_syntax, task.owner):
            try:
                check()
            except OSError:
                label = "tempfile: refused"
                task.out += [] if label in task.out else [label]
            except Exception:  # noqa: BLE001 (any other failure prints only the fixed helper line)
                task.out += [] if FAILED in task.out else [FAILED]
        out = task.out
    except Exception:  # noqa: BLE001 (the fixed helper line, never a traceback)
        out = [FAILED]
    print("\n".join([*out, f"sha256: {hashlib.sha256(raw).hexdigest()}"]))
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
