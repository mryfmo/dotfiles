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
#   interpreter with -I, and uv runs with --no-config --offline. This preflight catches mistakes; it is no trust
#   boundary against a hostile same-user process.
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
rc=0
refuse() {
    echo "$1: refused ($2)"
    rc=1
}

checker="${root}/scripts/orchestrator/task-consistency-check.py"
out="$(uv run --no-config --no-project --offline --python "${py}" --with pyyaml python -I "${checker}" --root "${root}" "${task}" 2>&1)" ||
    refuse consistency "$(printf '%s' "${out}" | tr -s '\n ' ' ')"

# SECRET_PATTERN and the home pattern come from the validator's syntax tree, neither imported nor copied (its
# compiled_home_path_pattern runs alone, with no host home); fenced blocks are parsed, never run.
"${py}" -I - "${root}" "${task}" << 'PY' || rc=1
import ast, pathlib, re, subprocess, sys
tree = ast.parse(open(f"{sys.argv[1]}/scripts/validate-agent-assets.py", encoding="utf-8").read())
calls = [n.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SECRET_PATTERN"]
try:
    pattern = re.compile(*map(ast.literal_eval, calls[0].args))
except (IndexError, ValueError, TypeError, re.error):
    sys.exit(print("secret-pattern: refused (no literal SECRET_PATTERN in the validator)") or 1)
text, rc = open(sys.argv[2], encoding="utf-8", errors="replace").read(), 0
hits = [str(i) for i, line in enumerate(text.split("\n"), 1) if pattern.search(line)]
if hits:
    rc = print(f"secret-pattern: refused ({len(hits)} match(es) on line(s) {','.join(hits)})") or 1
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compiled_home_path_pattern")
fn.decorator_list, scope = [], {"re": re, "Path": pathlib.Path}
exec(compile(ast.Module([fn], []), "validate-agent-assets.py", "exec"), scope)
home = scope[fn.name](pathlib.Path(sys.argv[1]), "")
homes = [str(i) for i, line in enumerate(text.split("\n"), 1) if home.search(line)]
if homes:
    rc = print(f"literal-home: refused (line(s) {','.join(homes)})") or 1
fence = r"^ {0,3}(`{3,})[ \t]*(?:bash|sh)[ \t]*\n(.*?)^ {0,3}\1`*[ \t]*$"  # CommonMark: longer or indented fences
blocks = [m[1] for m in re.findall(fence, text, re.DOTALL | re.MULTILINE)]
bad = [str(n) for n, b in enumerate(blocks, 1) if subprocess.run(["/bin/bash", "-n"], input=b, text=True, capture_output=True).returncode]
if bad:
    rc = print(f"bash-syntax: refused (block(s) {','.join(bad)})") or 1
sys.exit(rc)
PY

lines="$(wc -l < "${task}" | tr -d ' ')"
cap="$(/usr/bin/grep -oE 'at or under [*]{0,2}[0-9]+ lines' "${task}" | head -n 1 | tr -dc '0-9')"
[[ -z ${cap} || ${lines} -le ${cap} ]] || refuse self-cap "${lines} lines over the cap of ${cap}"

# The record a text reads its `## Owned by <task_id>` rows from resolves from the root; its section ends at the next ##.
self="$(sed -n '1,/^---$/s/^task_id:[[:space:]]*//p' "${task}" | head -n 1 | tr -d "\"' ")"
if [[ -n ${self} ]] && /usr/bin/grep -qF "## Owned by ${self}" "${task}"; then
    rec="$(/usr/bin/grep -oE '\.orchestration/acceptance/[A-Za-z0-9._-]+\.md' "${task}" | head -n 1)"
    items="$(/usr/bin/grep -c '^## Item' "${task}")"
    rows="$(awk -v h="## Owned by ${self}" '$0 == h || index($0, h " ") == 1 { p = f = 1; next }
        p && /^## / { p = 0 } p && (/^[^\t ]+\t[^\t ]/ || /^- [^ ]/) { n++ } END { print f ? n + 0 : "none" }' \
        "${root}/${rec:-/nonexistent}" 2> /dev/null)"
    if [[ -z ${rec} || ! -f "${root}/${rec}" ]]; then
        refuse owner-section "record ${rec:-<none named>} missing"
    elif [[ ${rows} == none ]]; then
        refuse owner-section "no '## Owned by ${self}' section in ${rec}"
    elif [[ ${rows} -eq 0 && ${items} -le 1 ]]; then
        refuse owner-section "no row under '## Owned by ${self}' in ${rec}, and no other Item"
    fi
fi

echo "sha256: $("${py}" -I -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "${task}")"
exit "${rc}"
