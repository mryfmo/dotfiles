#!/usr/bin/env bash
# @file pre-send.sh
# @brief Check a task text's final bytes before each send, with every machine check CI or the regime applies to it.
# @description
#   Promoted from the orchestrator's glue (C-100, C-102, M-20261020-01, M-20261020-03), reset as T133 a02. It reads one
#   task text as data, never edits or runs it, and runs every check: the task-consistency checker, the validator's
#   SECRET_PATTERN over the whole text and its home pattern, the self cap (`at or under N lines`, `wc -l`), `bash -n`
#   over every bash or sh fence, and the `## Owned by <task_id>` section, as one helper under the checker's `uv run
#   --no-config --offline --with pyyaml` on the pinned 3.15 interpreter with -I. Each refusal is a fixed `<check>:
#   refused` label with task line numbers at most, and the sha256 is printed last; no text of the task, the checker or
#   a tool reaches either stream. It catches mistakes; it is no boundary against a hostile same-user process.
# @arg $1 string The task text to check.
# @exitcode 0 Every check passes.
# @exitcode 1 A check refuses, or the argument is missing or unreadable.
set -u
root="$(cd -- "$(dirname -- "$0")/../.." && pwd)"
py="${HOME}/.local/share/mise/installs/python/3.15.0/bin/python3"
if [[ $# -ne 1 || ! -f ${1-} || ! -r ${1-} ]]; then
    echo "input: refused"
    exit 1
fi
task="$1"
read -r -d '' helper << 'PY' || true
import ast, pathlib, re, subprocess, sys, yaml
root, task = sys.argv[1:3]
text, out = open(task, encoding="utf-8", errors="replace").read(), []
lines, nr = text.split("\n"), lambda offset: text.count("\n", 0, offset) + 1
def refuse(name, nums=()):  # a fixed label and numbers only: nothing of the text or a tool is ever printed
    nums = sorted({int(n) for n in nums})
    out.append(f"{name}: refused" + (f" line(s) {','.join(map(str, nums))}" if nums else ""))
run = subprocess.run([sys.executable, "-I", f"{root}/scripts/orchestrator/task-consistency-check.py", "--root", root, task], capture_output=True, text=True)
if run.returncode:  # a YAML mark counts lines of the front matter, which starts after the first ---: one more in the task
    refuse("consistency", [int(n) + 1 for n in re.findall(r"line (\d+), column \d+", run.stdout + run.stderr)])
tree = ast.parse(open(f"{root}/scripts/validate-agent-assets.py", encoding="utf-8").read())
try:  # the validator's assignment from its syntax tree, its module never run; matched over the complete text
    call = next(n.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SECRET_PATTERN")
    pattern = re.compile(ast.literal_eval(call.args[0]), (ast.literal_eval(call.args[1]) if call.args[1:] else 0) | re.MULTILINE)
    hits = [n for m in pattern.finditer(text) for n in range(nr(m.start()), nr(m.end()) + 1)]
    hits += [i for i, line in enumerate(lines, 1) if pattern.search(line)]
except Exception:
    hits = [0]
if hits: refuse("secret-pattern", [n for n in hits if n])
try:  # its compiled_home_path_pattern runs alone, with no host home
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compiled_home_path_pattern")
    fn.decorator_list, scope = [], {"re": re, "Path": pathlib.Path}
    exec(compile(ast.Module([fn], []), "validate-agent-assets.py", "exec"), scope)
    homes = [i for i, line in enumerate(lines, 1) if scope[fn.name](pathlib.Path(root), "").search(line)]
except Exception:
    homes = [0]
if homes: refuse("literal-home", [n for n in homes if n])
cap = re.search(r"at or under \*{0,2}(\d+) lines", text)
if cap and open(task, "rb").read().count(b"\n") > int(cap[1]): refuse("self-cap", [nr(cap.start())])
bad, fence, body = [], None, []  # one CommonMark-style pass over every fence; bash or sh by the info string's first word
for i, line in enumerate(lines + [None], 1):
    if fence and (line is None or re.fullmatch(rf" {{0,3}}{re.escape(fence[0][0])}{{{len(fence[0])},}}[ \t]*", line)):
        if fence[2] and subprocess.run(["/bin/bash", "-n"], input="\n".join(body) + "\n", text=True, capture_output=True).returncode:
            bad.append(fence[1])
        fence = None
    elif fence:
        body.append(re.sub(rf"^ {{0,{fence[3]}}}", "", line))
    elif line is not None and (m := re.match(r"( {0,3})(`{3,}(?!.*`)|~{3,})(.*)", line)):
        fence, body = (m[2], i, m[3].split()[:1] in (["bash"], ["sh"]), len(m[1])), []
if bad: refuse("bash-syntax", bad)
try:  # the checker's own reading of the front matter
    front = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n")) if text.startswith("---") else None
except yaml.YAMLError:
    front = None
me = str(front.get("task_id") or "") if isinstance(front, dict) else ""
if me and (ref := text.find(f"## Owned by {me}")) >= 0:  # the named record resolves from the root; ends at the next ##
    rec, head = re.search(r"\.orchestration/acceptance/[A-Za-z0-9._-]+\.md", text), f"## Owned by {me}"
    path = pathlib.Path(root, rec[0]) if rec else None
    rows, found, inside = 0, False, False
    for line in path.read_text(errors="replace").split("\n") if path and path.is_file() else []:
        if line == head or line.startswith(head + " "):
            found = inside = True
            continue
        inside = inside and not line.startswith("## ")
        rows += inside and bool(re.match(r"[^\t ]+\t[^\t ]|- [^ ]", line))
    if not found or not rows and len(re.findall(r"^## Item", text, re.MULTILINE)) <= 1:
        refuse("owner-section", [nr(ref)])
print("\n".join(out))
sys.exit(1 if out else 0)
PY
out="$(uv run --no-config --no-project --offline --python "${py}" --with pyyaml python -I -c "${helper}" "${root}" "${task}" 2> /dev/null)"
rc=$?
[[ ${rc} -le 1 ]] || { out="consistency: refused" && rc=1; }
[[ -z ${out} ]] || printf '%s\n' "${out}"
echo "sha256: $("${py}" -I -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "${task}" 2> /dev/null)"
exit "${rc}"
