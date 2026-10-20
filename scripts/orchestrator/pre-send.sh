#!/usr/bin/env bash
# @file pre-send.sh
# @brief Check a task text's final bytes before each send, with every machine check CI or the regime applies to it.
# @description
#   Promoted from the orchestrator's glue (C-100, C-102, M-20261020-01, M-20261020-03). It reads the one task text it
#   is given as data: it never edits the file and never runs its prose. Every check runs even after another refuses:
#   the task-consistency checker, the validator's own SECRET_PATTERN (line numbers only, never the matched text),
#   literal home paths by the validator's own home pattern, the text's self cap (`at or under N lines` against
#   `wc -l`), `/bin/bash -n` over every fenced bash block, and the `## Owned by <task_id>` section it reads. Each
#   refusal prints one named line, and a readable text's sha256 is printed last. Python runs as the pinned 3.15
#   interpreter with -I: the checks run as one helper under the checker's own `uv run --no-config --offline --with
#   pyyaml`, which reads task_id from the parsed front matter. It catches mistakes; it is no hostile-user boundary.
# @arg $1 string The task text to check.
# @exitcode 0 Every check passes.
# @exitcode 1 A check refuses, or the argument is missing or unreadable.
set -u
root="$(cd -- "$(dirname -- "$0")/../.." && pwd)"
py="${HOME}/.local/share/mise/installs/python/3.15.0/bin/python3"
if [[ $# -ne 1 ]]; then
    echo "input: refused (usage: pre-send.sh <task.md>)"
    exit 1
fi
task="$1"
if [[ ! -f ${task} || ! -r ${task} ]]; then
    echo "input: refused (not a readable file: ${task})"
    exit 1
fi
# SECRET_PATTERN and the home pattern come from the validator's syntax tree, neither imported nor copied (its
# compiled_home_path_pattern runs alone, with no host home); fenced blocks are parsed, never run; every refusal is
# printed with SECRET_PATTERN matches redacted, the checker's diagnostics too.
uv run --no-config --no-project --offline --python "${py}" --with pyyaml python -I - "${root}" "${task}" << 'PY'
import ast, pathlib, re, subprocess, sys, yaml
root, task = sys.argv[1], sys.argv[2]
tree = ast.parse(open(f"{root}/scripts/validate-agent-assets.py", encoding="utf-8").read())
calls = [n.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SECRET_PATTERN"]
try:
    pattern = re.compile(*map(ast.literal_eval, calls[0].args))
except (IndexError, ValueError, TypeError, re.error):
    sys.exit(print("secret-pattern: refused (no literal SECRET_PATTERN in the validator)") or 1)
text, rc = open(task, encoding="utf-8", errors="replace").read(), 0
def refuse(name, why):
    global rc
    rc = print(f"{name}: refused ({pattern.sub('[redacted]', why)})") or 1
run = subprocess.run([sys.executable, "-I", f"{root}/scripts/orchestrator/task-consistency-check.py", "--root", root, task], capture_output=True, text=True)
if run.returncode:
    refuse("consistency", f"exit {run.returncode}: " + " ".join((run.stdout + run.stderr).split()))
hits = [str(i) for i, line in enumerate(text.split("\n"), 1) if pattern.search(line)]
if hits:
    refuse("secret-pattern", f"{len(hits)} match(es) on line(s) {','.join(hits)}")
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compiled_home_path_pattern")
fn.decorator_list, scope = [], {"re": re, "Path": pathlib.Path}
exec(compile(ast.Module([fn], []), "validate-agent-assets.py", "exec"), scope)
home = scope[fn.name](pathlib.Path(root), "")
if homes := [str(i) for i, line in enumerate(text.split("\n"), 1) if home.search(line)]:
    refuse("literal-home", f"line(s) {','.join(homes)}")
fence = r"^ {0,3}((`|~)\2{2,})[ \t]*(?:bash|sh)[ \t]*\n(.*?)(?:^ {0,3}\1\2*[ \t]*$|\Z)"  # CommonMark: ``` or ~~~, open to the end
blocks = [m[2] for m in re.findall(fence, text, re.DOTALL | re.MULTILINE)]
if bad := [str(n) for n, b in enumerate(blocks, 1) if subprocess.run(["/bin/bash", "-n"], input=b, text=True, capture_output=True).returncode]:
    refuse("bash-syntax", f"block(s) {','.join(bad)}")
lines, cap = open(task, "rb").read().count(b"\n"), re.search(r"at or under \*{0,2}(\d+) lines", text)
if cap and lines > int(cap[1]):
    refuse("self-cap", f"{lines} lines over the cap of {cap[1]}")
try:  # the checker's own reading of the front matter
    front = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n")) if text.startswith("---") else None
except yaml.YAMLError:
    front = None
me = str(front.get("task_id") or "") if isinstance(front, dict) else ""
if me and f"## Owned by {me}" in text:  # the named record resolves from the root; its section ends at the next ##
    rec, head = re.search(r"\.orchestration/acceptance/[A-Za-z0-9._-]+\.md", text), f"## Owned by {me}"
    path, rows, found, inside = pathlib.Path(root, rec[0]) if rec else None, 0, False, False
    for line in path.read_text(errors="replace").split("\n") if path and path.is_file() else []:
        if line == head or line.startswith(head + " "):
            found = inside = True
            continue
        inside = inside and not line.startswith("## ")
        rows += inside and bool(re.match(r"[^\t ]+\t[^\t ]|- [^ ]", line))
    if not (path and path.is_file()):
        refuse("owner-section", f"record {rec[0] if rec else '<none named>'} missing")
    elif not found:
        refuse("owner-section", f"no '{head}' section in {rec[0]}")
    elif not rows and len(re.findall(r"^## Item", text, re.MULTILINE)) <= 1:
        refuse("owner-section", f"no row under '{head}' in {rec[0]}, and no other Item")
sys.exit(rc)
PY
rc=$?
[[ ${rc} -le 1 ]] || { echo "consistency: refused (uv, PyYAML or the pinned interpreter is unavailable: exit ${rc})" && rc=1; }
echo "sha256: $("${py}" -I -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "${task}")"
exit "${rc}"
