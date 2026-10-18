#!/usr/bin/env bash
# @file result-precheck.sh
# @brief Run the repository's own checks on a seat's head before its AGMSG-RESULT and record them as evidence.
# @description
#   Plan 024 P1-5. From the worktree root, on a tree with no change outside `.orchestration/<task>/`, each check's
#   output goes to `.orchestration/<task>/precheck-<name>.log` (masked) and the check to `{name, ok, exit,
#   output_sha256}`: `unit-test` (`make unit-test` or `uv run python -m unittest <modules> -v`), `render-check`,
#   `format` (Amendment 1: CI's formatting commands in CI's scopes, below), `shellcheck` (`-x`, the diff's `*.sh` and
#   bash or sh shebang files), `secrets` (each blob the diff from origin/main changes, scanned alone by scan_one) and
#   `local-review` (under `PRECHECK_LOCAL_REVIEW=seat`; else `{ok: null, deferred: orchestrator}`). A command a check
#   needs that fails, or cannot run, fails that check.
#   CI's scopes (`.github/workflows/test.yaml`; a change there is a one-line change in check_format):
#     Run `shfmt`: git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
#     Check Python and Markdown formatting: git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
#     Check Python and Markdown formatting: git ls-files -z "*.md" | xargs -0 prettier --check
#   A `--check` selector (`uv run python -m unittest tests.unit.<module> -k <name>`) must pass here and fail in a
#   detached worktree of `--previous-head` that runs this head's copy of the module: exit 1 after `Ran <n>` tests with
#   n > 0 and `FAILED (failures=…)` without errors, so an import error or no test run is no proof (`selectors[]`); the
#   worktree is removed with `git worktree remove --force`, never pruned. `precheck.json` (`{head, tree, generated_at, checks, selectors}`) and `result.txt` (the RESULT line) are
#   written and `precheck=<sha256>` printed last; the seat commits them and the logs last and sends the RESULT with
#   `head=` set to that commit. A masker failure removes the logs instead. `--secrets <file>`, `--blob <commit>:<path>`
#   (the pre-push hook) and `--staged` (`format` and `shellcheck` on the staged blobs, the pre-commit hook) run only that.
# shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)
# shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)
# @arg $1 string Task id: letters, digits, `.`, `_` and `-`.
# @option --tests <module>... Unittest modules to run instead of `make unit-test`.
# @option --previous-head <sha40> The `previous_head=` of a `status=revise` ACCEPTANCE; needs `--check`.
# @option --check <selector> A `tests/unit/<module>.py::<name>` selector (the ACCEPTANCE's `check=`), repeatable.
# @option --secrets <file> Scan only that file, unchanged, with scan_one; --blob <commit>:<path> only that blob.
# @option --staged Run only `format` and `shellcheck` on the staged blobs (the index exported to a temporary tree).
# @env PRECHECK_LOCAL_REVIEW `orchestrator` (the default) or `seat`.
# @exitcode 0 Every check and selector that ran is ok (a deferred check is neither).
# @exitcode 1 A check or a selector failed, or the masker failed.
# @exitcode 2 Usage error, or the tree has changes outside the evidence directory.
# @example
#   scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests/unit/test_result_precheck.py
set -euo pipefail

usage() {
    echo "usage: result-precheck.sh <task> [--tests <m>...] [--previous-head <sha40> --check <s>...] | --secrets <f> | --blob <c>:<p> | --staged" >&2
    exit 2
}
task='' previous='' secrets='' staged='' blob='' tests=() selectors=()
while (($#)); do
    case $1 in
    --tests)
        while (($# > 1)) && [[ $2 != --* ]]; do
            tests+=("$2")
            shift
        done
        ;;
    --previous-head | --check | --secrets | --blob)
        (($# > 1)) || usage
        case $1 in
        --previous-head) previous=$2 ;;
        --check) selectors+=("$2") ;;
        --secrets) secrets=$2 ;;
        *) blob=$2 ;;
        esac
        shift
        ;;
    --staged) staged=1 ;;
    -*) usage ;;
    *)
        [[ -z ${task} ]] || usage
        task=$1
        ;;
    esac
    shift
done
review=${PRECHECK_LOCAL_REVIEW:-orchestrator}
[[ ${review} == orchestrator || ${review} == seat ]] || usage
cd -- "$(git rev-parse --show-toplevel)"
work="$(mktemp -d "${TMPDIR:-/tmp}/result-precheck.XXXXXX")"
trap 'if [[ -e "${work}/previous" ]]; then git worktree remove --force "${work}/previous" || true; fi; rm -rf -- "${work}"' EXIT

# The repository detector on one file, as validate_no_obvious_secrets reads a tracked one: read_scannable_text (UTF-8,
# or UTF-16 with a BOM; a NUL or UTF-16 under .orchestration/ is refused), json_strings, the allowed placeholders and
# SECRET_PATTERN, plus home_path_pattern for a path under .orchestration/ only. argv: validator, scan root, path.
read -r -d '' detector << 'PY' || true
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("validator", sys.argv[1])
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
root, rel = Path(sys.argv[2]), sys.argv[3]
real, v.ROOT = v.ROOT, root  # read_scannable_text judges a path relative to ROOT: the blob's own path here
try: text = v.read_scannable_text(root / rel)
except SystemExit: text = None  # its refusal of a NUL or UTF-16 under .orchestration/
v.ROOT = real
if text is None: sys.exit(print(f"decoding: {rel} cannot be decoded") or 1)
strings = v.json_strings(text) or [text]
count = sum(len(v.SECRET_PATTERN.findall(v.strip_allowed_secret_placeholders(s))) for s in strings)
home = rel.startswith(".orchestration/") and any(v.home_path_pattern().search(s) for s in (text, *strings))
print(f"secrets: {count} match(es)" + (f"\nhome-path: {rel} names a home directory" if home else ""))
sys.exit(1 if count or home else 0)
PY
# @description Scan one input alone with the detector, unchanged, at its repository-relative path under a fresh
#   directory: a blob (`<commit> <path>`, read with `git show --no-textconv`) or a file (`- <path> <file>`). Prints
#   counts and paths only. Exit 0 clean; 1 a finding, an unreadable or undecodable input, or a detector failure.
scan_one() {
    local dir
    dir="$(mktemp -d "${work}/scan.XXXXXX")" && mkdir -p -- "$(dirname -- "${dir}/$2")" || return
    if [[ $1 == - ]]; then cp -- "$3" "${dir}/$2"; else git show --no-textconv "$1:$2" > "${dir}/$2"; fi || {
        echo "unreadable: ${1:0:7}:$2 cannot be read"
        return 1
    }
    uv run --no-project python -I -c "${detector}" scripts/validate-agent-assets.py "${dir}" "$2"
}
# @description Run a command on the tracked (or `staged`) files of some pathspecs; nothing runs when none matches, and
#   a listing that fails fails the call (errexit is off in a function run through `||`, so every failure is explicit).
# @arg $1 string `tracked` or `staged`; then the pathspecs, `--` and the command.
on_files() {
    local list=(git ls-files -z --) specs=()
    [[ $1 != staged ]] || list=(git diff --cached --name-only -z --diff-filter=ACMR --)
    shift
    while [[ $1 != -- ]]; do
        specs+=("$1")
        shift
    done
    shift
    "${list[@]}" "${specs[@]}" > "${work}/scope" || {
        echo "failed: ${list[*]} ${specs[*]}"
        return 1
    }
    [[ -s ${work}/scope ]] || return 0
    xargs -0 "$@" < "${work}/scope" || {
        echo "failed: $*"
        return 1
    }
}
# @description CI's three formatting commands in CI's scopes (the header's three lines).
# @arg $1 string `tracked` or `staged`.
check_format() {
    local rc=0
    on_files "$1" ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' -- shfmt --indent 4 --space-redirects --diff || rc=1
    on_files "$1" '*.py' -- ruff format --config ruff.toml --check || rc=1
    on_files "$1" '*.md' -- prettier --check || rc=1
    return "${rc}"
}
# @description shellcheck the `*.sh` and bash or sh shebang files of the diff from origin/main (or of the `staged` files).
check_shellcheck() {
    local f first files=() list=(git diff --name-only -z origin/main...HEAD)
    [[ $1 != staged ]] || list=(git diff --cached --name-only -z --diff-filter=ACMR)
    "${list[@]}" > "${work}/names" || return
    while IFS= read -r -d '' f; do
        first=''
        [[ ! -f ${f} ]] || IFS= read -r first < "${f}" || true
        [[ ! -f ${f} || (${f} != *.sh && ! ${first} =~ ^#!.*[/[:blank:]](ba)?sh([[:blank:]]|$)) ]] || files+=("${f}")
    done < "${work}/names"
    ((${#files[@]})) || return 0
    shellcheck -x "${files[@]}" || {
        echo "failed: shellcheck -x ${files[*]}"
        return 1
    }
}
mode=${secrets:+secrets}${staged:+staged}${blob:+blob}
if [[ -n ${mode} ]]; then
    [[ ${mode} =~ ^(secrets|staged|blob)$ && -z ${task}${previous} && ${#tests[@]}${#selectors[@]} == 00 ]] || usage
    if [[ ${mode} != staged ]]; then
        [[ -f ${secrets} || ${blob} == ?*:?* ]] || usage
        set -- - "${secrets##*/}" "${secrets}"
        [[ -z ${blob} ]] || set -- "${blob%%:*}" "${blob#*:}"
        scan_one "$@"
        exit
    fi
    rc=0
    # Thread 4305945406: the checks read the staged blobs, the whole index exported with every tracked config.
    GIT_DIR="$(git rev-parse --absolute-git-dir)" GIT_WORK_TREE=${PWD} GIT_INDEX_FILE="$(git rev-parse --path-format=absolute --git-path index)"
    export GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE # a hook's GIT_INDEX_FILE may be relative to the root
    git checkout-index -a --prefix="${work}/index/" || exit 1
    cd -- "${work}/index"
    check_format staged || rc=1
    check_shellcheck staged || rc=1
    exit "${rc}"
fi
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || usage
[[ -z ${previous} && ${#selectors[@]} -eq 0 || ${previous} =~ ^[0-9a-f]{40}$ && ${#selectors[@]} -gt 0 ]] || usage
for s in ${selectors[@]+"${selectors[@]}"}; do
    [[ ${s} =~ ^tests/unit/[A-Za-z_][A-Za-z0-9_]*\.py::[A-Za-z_][A-Za-z0-9_]*$ ]] || usage
done
evidence=".orchestration/${task}"
while IFS= read -r -d '' entry; do
    [[ ${entry:3} == "${evidence}/"* ]] || {
        echo "result-precheck: the tree has changes outside ${evidence}/ (${entry:3}); commit them first" >&2
        exit 2
    }
done < <(git status --porcelain=v1 -z --untracked-files=all --no-renames)
mkdir -p -- "${evidence}" && rm -f -- "${evidence}"/precheck-*.log
# @description Run one check (name, then command) with its output in its log; record `name<TAB>exit<TAB>log`.
run_check() {
    local name=$1 rc=0 log="${evidence}/precheck-$1.log"
    shift
    "$@" > "${log}" 2>&1 || rc=$?
    printf '%s\t%s\t%s\n' "${name}" "${rc}" "${log}" >> "${work}/rows"
    echo "result-precheck: ${name} exit ${rc}"
}
# shellcheck disable=SC2329 # run through run_check
check_secrets() {
    local f type out bad=''
    git diff --name-only -z --no-renames --diff-filter=d origin/main...HEAD > "${work}/changed" || return
    while IFS= read -r -d '' f; do
        type="$(git cat-file -t "HEAD:${f}")" || return
        [[ ${type} != blob ]] || out="$(scan_one HEAD "${f}")" || bad+="${f}: ${out//$'\n'/; }"$'\n'
    done < "${work}/changed"
    printf '%s' "${bad}"
    [[ -z ${bad} ]]
}
# shellcheck disable=SC2329 # run through run_check
check_local_review() {
    local head pr
    head="$(git rev-parse HEAD)" || return
    pr="$(gh pr view --json number --jq .number)" || return
    [[ ${pr} =~ ^[0-9]+$ ]] || {
        echo "local-review: no PR number for this branch: ${pr}"
        return 1
    }
    bash scripts/orchestrator/local-review.sh "${task}" "${head}" "${pr}"
}

touch "${work}/rows" "${work}/selectors"
unit=(make unit-test)
((${#tests[@]} == 0)) || unit=(uv run python -m unittest "${tests[@]}" -v)
run_check unit-test "${unit[@]}"
run_check render-check make render-check
run_check format check_format tracked
run_check shellcheck check_shellcheck diff
run_check secrets check_secrets
if [[ ${review} == seat ]]; then
    run_check local-review check_local_review
else
    printf 'local-review\tdeferred\t-\n' >> "${work}/rows"
fi
if ((${#selectors[@]})); then
    git worktree add --detach -q "${work}/previous" "${previous}"
    for s in "${selectors[@]}"; do
        n=$((${n:-0} + 1)) module=${s#tests/unit/} && module=${module%%.py::*}
        before="${evidence}/precheck-selector-${n}-previous.log" after="${evidence}/precheck-selector-${n}-head.log" prc=0 hrc=0
        # The previous code runs this head's test source (the selector's test may be new), so its own failure counts.
        { mkdir -p -- "${work}/previous/tests/unit" && cp -- "tests/unit/${module}.py" "${work}/previous/tests/unit/"; } \
            > "${before}" 2>&1 || prc=$?
        ((prc)) || (cd -- "${work}/previous" && uv run python -m unittest "tests.unit.${module}" -k "${s##*::}") > "${before}" 2>&1 || prc=$?
        uv run python -m unittest "tests.unit.${module}" -k "${s##*::}" > "${after}" 2>&1 || hrc=$?
        printf '%s\t%s\t%s\t%s\t%s\n' "${s}" "${prc}" "${before}" "${hrc}" "${after}" >> "${work}/selectors"
        echo "result-precheck: ${s} previous head exit ${prc}, this head exit ${hrc}"
    done
fi
logs=("${evidence}"/precheck-*.log)
uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets "${logs[@]}" > /dev/null || {
    rm -f -- "${logs[@]}"
    echo "result-precheck: the masker failed; the logs are removed and no record is written" >&2
    exit 1
}
read -r -d '' writer << 'PY' || true
import hashlib, json, os, re, sys
from datetime import UTC, datetime
task, evidence, head, tree, rows, sel_rows = sys.argv[1:7]
digest = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()
def red(code, log):
    # An executed test failing by assertion; an import or runner error, or no test run, proves no regression.
    text = open(log, errors="replace").read()
    ran, summary = re.search(r"^Ran (\d+) tests? in ", text, re.M), re.search(r"^FAILED \(([^)]*)\)$", text, re.M)
    return code == "1" and bool(ran and int(ran[1]) and summary) and "failures=" in summary[1] and "errors=" not in summary[1]
checks = [
    {"name": n, "ok": None, "deferred": "orchestrator"} if rc == "deferred"
    else {"name": n, "ok": rc == "0", "exit": int(rc), "output_sha256": digest(log)}
    for n, rc, log in (line.rstrip("\n").split("\t") for line in open(rows))
]
selectors = [
    {"selector": s, "ok": red(p, before) and h == "0", "previous_head_exit": int(p),
     "previous_head_output_sha256": digest(before), "head_exit": int(h), "head_output_sha256": digest(after)}
    for s, p, before, h, after in (line.rstrip("\n").split("\t") for line in open(sel_rows))
]
when = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
document = {"head": head, "tree": tree, "generated_at": when, "checks": checks, "selectors": selectors}
with open(f"{evidence}/precheck.json", "w") as f:
    f.write(json.dumps(document, indent=2) + "\n")
ok = all(c["ok"] is not False for c in checks) and all(s["ok"] for s in selectors)
total = digest(f"{evidence}/precheck.json")
fields = [f"task_copy={digest(f'{evidence}/task.md')}"] if os.path.isfile(f"{evidence}/task.md") else []
fields += [f"{k}={evidence}/{k}.md" for k in ("report", "validation", "sandbox", "learning")]
with open(f"{evidence}/result.txt", "w") as f:
    state = "ready_for_review" if ok else "blocked"
    f.write(f"AGMSG-RESULT v1 task_id={task} status={state} head={head} precheck={total} {' '.join(fields)}\n")
print(f"precheck={total}")
sys.exit(0 if ok else 1)
PY
# Not exec: the EXIT trap still removes the work directory and the selector worktree.
python3 -I -c "${writer}" "${task}" "${evidence}" "$(git rev-parse HEAD)" "$(git rev-parse 'HEAD^{tree}')" \
    "${work}/rows" "${work}/selectors"
