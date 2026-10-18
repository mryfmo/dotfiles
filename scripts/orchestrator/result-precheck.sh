#!/usr/bin/env bash
# @file result-precheck.sh
# @brief Run the repository's own checks on a seat's head before its AGMSG-RESULT and record them as evidence.
# @description
#   Plan 024 P1-5. From the worktree root, on a tree with no change outside `.orchestration/<task>/`, each check's
#   output goes to `.orchestration/<task>/precheck-<name>.log` (masked) and the check to `{name, ok, exit,
#   output_sha256}`: `unit-test` (`make unit-test` or `uv run python -m unittest <modules> -v`), `render-check`,
#   `format` (Amendment 1: CI's formatting commands in CI's scopes, below), `shellcheck` (`-x`, the diff's `*.sh` and
#   bash or sh shebang files), `secrets` (the diff from origin/main masked as a copy; a difference is a match, counted,
#   never printed) and `local-review` (under `PRECHECK_LOCAL_REVIEW=seat`; else `{ok: null, deferred: orchestrator}`).
#   CI's scopes (`.github/workflows/test.yaml`; a change there is a one-line change in check_format):
#     Run `shfmt`: git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
#     Check Python and Markdown formatting: git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
#     Check Python and Markdown formatting: git ls-files -z "*.md" | xargs -0 prettier --check
#   A `--check` selector (`uv run python -m unittest tests.unit.<module> -k <name>`) must fail in a detached worktree of
#   `--previous-head` and pass here (`selectors[]`); the worktree is removed with `git worktree remove --force`, never
#   pruned. `precheck.json` (`{head, tree, generated_at, checks, selectors}`) and `result.txt` (the RESULT line) are
#   written and `precheck=<sha256>` printed last; the seat commits them and the logs last and sends the RESULT with
#   `head=` set to that commit. A masker failure removes the logs instead. `--secrets <file>` (the pre-push hook) and
#   `--staged` (`format` and `shellcheck` on the staged files, the pre-commit hook) run only those checks.
# shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)
# shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)
# @arg $1 string Task id: letters, digits, `.`, `_` and `-`.
# @option --tests <module>... Unittest modules to run instead of `make unit-test`.
# @option --previous-head <sha40> The `previous_head=` of a `status=revise` ACCEPTANCE; needs `--check`.
# @option --check <selector> A `tests/unit/<module>.py::<name>` selector (the ACCEPTANCE's `check=`), repeatable.
# @option --secrets <diff-file> Run only the secrets check on the file.
# @option --staged Run only `format` and `shellcheck` on the staged files.
# @env PRECHECK_LOCAL_REVIEW `orchestrator` (the default) or `seat`.
# @exitcode 0 Every check and selector that ran is ok (a deferred check is neither).
# @exitcode 1 A check or a selector failed, or the masker failed.
# @exitcode 2 Usage error, or the tree has changes outside the evidence directory.
# @example
#   scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests/unit/test_result_precheck.py
set -euo pipefail

usage() {
    echo "usage: result-precheck.sh <task> [--tests <m>...] [--previous-head <sha40> --check <s>...] | --secrets <f> | --staged" >&2
    exit 2
}
task='' previous='' secrets='' staged='' tests=() selectors=()
while (($#)); do
    case $1 in
    --tests)
        while (($# > 1)) && [[ $2 != --* ]]; do
            tests+=("$2")
            shift
        done
        ;;
    --previous-head | --check | --secrets)
        (($# > 1)) || usage
        case $1 in
        --previous-head) previous=$2 ;;
        --check) selectors+=("$2") ;;
        *) secrets=$2 ;;
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

# @description Mask secrets and home paths in place with the repository masker.
mask() {
    uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets "$@"
}
# @description Mask a copy of a file and compare: exit 1 and print `secrets: <n> match(es)` on a difference, never the text.
# @arg $1 path The file.
secrets_in() {
    local out
    cp -- "$1" "${work}/copy"
    out="$(mask "${work}/copy" 2>&1)" || out='masker failed'
    if [[ ${out} != 'masker failed' ]] && cmp -s -- "$1" "${work}/copy"; then
        echo "secrets: 0 match(es)"
        return 0
    fi
    [[ ${out} =~ masked\ ([0-9]+)\ match ]] && echo "secrets: ${BASH_REMATCH[1]} match(es)" || echo "secrets: ${out}"
    return 1
}
# @description List the tracked (or `staged`) files of some pathspecs into the scope file; exit 1 when there is none.
# @arg $1 string `tracked` or `staged`; then the pathspecs.
scope() {
    local list=(git ls-files -z --)
    [[ $1 != staged ]] || list=(git diff --cached --name-only -z --diff-filter=ACMR --)
    shift
    "${list[@]}" "$@" > "${work}/scope"
    [[ -s ${work}/scope ]]
}
# @description Run a command on the scope file's files, naming the command when it fails.
on_scope() {
    xargs -0 "$@" < "${work}/scope" || {
        echo "failed: $*"
        return 1
    }
}
# @description CI's three formatting commands in CI's scopes (the header's three lines).
# @arg $1 string `tracked` or `staged`.
check_format() {
    local rc=0
    ! scope "$1" ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' || on_scope shfmt --indent 4 --space-redirects --diff || rc=1
    ! scope "$1" '*.py' || on_scope ruff format --config ruff.toml --check || rc=1
    ! scope "$1" '*.md' || on_scope prettier --check || rc=1
    return "${rc}"
}
# @description shellcheck the `*.sh` and bash or sh shebang files of the diff from origin/main (or of the `staged` files).
check_shellcheck() {
    local f first
    if [[ $1 == staged ]]; then
        scope staged || true
    else
        git diff --name-only -z origin/main...HEAD > "${work}/scope"
    fi
    while IFS= read -r -d '' f; do
        first=''
        [[ ! -f ${f} ]] || IFS= read -r first < "${f}" || true
        [[ -f ${f} && (${f} == *.sh || ${first} =~ ^#!.*[/[:blank:]](ba)?sh([[:blank:]]|$)) ]] && printf '%s\0' "${f}"
    done < "${work}/scope" > "${work}/shell" || true
    mv -- "${work}/shell" "${work}/scope"
    [[ ! -s ${work}/scope ]] || on_scope shellcheck -x
}

if [[ -n ${secrets} || -n ${staged} ]]; then
    [[ -z ${task}${previous} && ${#tests[@]} -eq 0 && ${#selectors[@]} -eq 0 && -z ${secrets:+${staged}} ]] || usage
    if [[ -n ${secrets} ]]; then
        [[ -f ${secrets} ]] || usage
        secrets_in "${secrets}"
        exit
    fi
    rc=0
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
mkdir -p -- "${evidence}"
rm -f -- "${evidence}"/precheck-*.log

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
    git diff origin/main...HEAD > "${work}/diff"
    secrets_in "${work}/diff"
}
# shellcheck disable=SC2329 # run through run_check
check_local_review() {
    bash scripts/orchestrator/local-review.sh "${task}" "$(git rev-parse HEAD)" "$(gh pr view --json number --jq .number)"
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
        (cd -- "${work}/previous" && uv run python -m unittest "tests.unit.${module}" -k "${s##*::}") > "${before}" 2>&1 || prc=$?
        uv run python -m unittest "tests.unit.${module}" -k "${s##*::}" > "${after}" 2>&1 || hrc=$?
        printf '%s\t%s\t%s\t%s\t%s\n' "${s}" "${prc}" "${before}" "${hrc}" "${after}" >> "${work}/selectors"
        echo "result-precheck: ${s} previous head exit ${prc}, this head exit ${hrc}"
    done
fi

logs=("${evidence}"/precheck-*.log)
mask "${logs[@]}" > /dev/null || {
    rm -f -- "${logs[@]}"
    echo "result-precheck: the masker failed; the logs are removed and no record is written" >&2
    exit 1
}
read -r -d '' writer << 'PY' || true
import hashlib, json, os, sys
from datetime import UTC, datetime

task, evidence, head, tree, rows, sel_rows = sys.argv[1:7]
def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
checks = [
    {"name": n, "ok": None, "deferred": "orchestrator"} if rc == "deferred"
    else {"name": n, "ok": rc == "0", "exit": int(rc), "output_sha256": digest(log)}
    for n, rc, log in (line.rstrip("\n").split("\t") for line in open(rows))
]
selectors = [
    {"selector": s, "ok": p != "0" and h == "0", "previous_head_exit": int(p),
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
