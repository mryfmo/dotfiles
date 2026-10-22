#!/usr/bin/env bash
# @file local-review.sh
# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
# @description
#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` whose `head:` is
#   this head is reused and re-reported; one that records another head is refused. Otherwise the clean review
#   worktree (`$ORCH_REVIEW_WORKTREE`, else `.claude/worktrees/orchestrator-review`), a path with its own `.git`
#   entry, is checked out detached at the head and left there, and the review binary runs in it as `--profile review
#   -s read-only review --base main`. The binary is `$CODEX_BIN`, else codex as `mise which` answers it under `env
#   -i` in the root, else `command -v`; it is resolved before the checkout, and a path under a `shims` directory is
#   refused. When its first line is an env shebang (`#!/usr/bin/env NAME` or `env -S NAME ARG…`), NAME is resolved the
#   same way and runs with the `-S` form's ARG words, then the binary, so no interpreter comes from PATH in the PR
#   worktree. A `-S` string holding a quote, a backslash, a `$` or a word starting with `#` is refused, since env -S
#   splits those differently. When the
#   binary fails, no file is written. Otherwise the file gets the front matter, the unique `-
#   [P0-3]` findings of the transcript's final message, and that message with the worktree prefix stripped; the
#   findings are printed, then `local-review: <n> findings (<file>)`.
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 string The PR head commit, a local one, 40 hex characters.
# @arg $3 int PR number.
# @exitcode 0 No finding.
# @exitcode 2 A precondition failed: a malformed task id or head, a review file of another head, the head is not a
#   local commit, the review worktree is not a worktree root or not clean, no review binary outside a shims
#   directory, or an env -S shebang the script does not split.
# @exitcode 3 One or more findings.
# @exitcode 4 The review binary failed; no file is written, and its transcript stays in `$TMPDIR`.
# @example
#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
set -euo pipefail
task=$1 head=$2 pr=$3
# Both name the review file, so a / in either would write outside the validation directory (the audit of b6ce4ff).
[[ $task =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && $head =~ ^[0-9a-f]{40}$ ]] || {
    echo "local-review: usage: local-review.sh <task> <40-hex head> <pr>"
    exit 2
}
R="$(git rev-parse --show-toplevel)"
cd -- "$R"
W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
if [ -s "$out" ]; then
    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again. The name keeps
    # seven characters of the head, so the recorded head must be this one (PR #357 thread 4270918140).
    [ "$(sed -n 's/^head: //p' "$out" | head -1)" = "$head" ] || {
        echo "local-review: $out records another head; not reused"
        exit 2
    }
    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    printf '%s\n' "$findings"
    echo "local-review: $n findings (existing $out)"
    [ "${n:-0}" = 0 ] || exit 3
    exit 0
fi
git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    exit 2
}
# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
[ -e "$W/.git" ] || {
    echo "local-review: $W is not a worktree root"
    exit 2
}
[ -z "$(git -C "$W" status --porcelain)" ] || {
    echo "local-review: $W is not clean"
    exit 2
}
# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
# binary from the PR head. A mise shim would pick its binary from the PR worktree it runs in, so a name comes from
# mise which under env -i, as orch-gate.sh resolves gh, and a shims path is refused (the audit of b6ce4ff). Sets
# found; a refusal exits here, before the checkout.
resolve() { # <name> <what> [<found by command -v alone>]
    if [ -n "${3:-}" ]; then
        found=$(command -v "$1") || found=
    else
        found=$(env -i PATH="$PATH" HOME="$HOME" UV_CACHE_DIR="${UV_CACHE_DIR:-}" mise which "$1" 2> /dev/null || command -v "$1") || found=
    fi
    [ -n "$found" ] || {
        echo "local-review: no $2 $1"
        exit 2
    }
    [[ $found == /* ]] || found=$R/$found
    [[ $found != */shims/* ]] || {
        echo "local-review: the $2 $found is under a shims directory; refused"
        exit 2
    }
}
resolve uv "binding interpreter launcher"
uv=$found
python=$(/usr/bin/env -i PATH="$PATH" HOME="$HOME" UV_CACHE_DIR="${UV_CACHE_DIR:-}" "$uv" python find)
gh=$(/usr/bin/env -i PATH="$PATH" HOME="$HOME" UV_CACHE_DIR="${UV_CACHE_DIR:-}" "$python" -I "$R/scripts/pr-feedback.py" --gh-binding) || exit 2
[[ -n ${GH_TOKEN:-} ]] || {
    echo 'refused: gh binding' >&2
    exit 2
}
gh_environment=(HOME="$HOME" LANG=C.UTF-8 LC_ALL=C UV_CACHE_DIR="$UV_CACHE_DIR" "GH_TOKEN=$GH_TOKEN" GH_CONFIG_DIR=/var/empty
    GH_PROMPT_DISABLED=1 GH_NO_UPDATE_NOTIFIER=1 GH_NO_EXTENSION_UPDATE_NOTIFIER=1 NO_COLOR=1 TERM=dumb GH_PAGER=cat)
bin=$(mktemp -d "${TMPDIR:-/tmp}/local-review-gh.XXXXXX")
trap 'rm -rf -- "$bin"' EXIT
ln -s -- "$gh" "$bin/gh"
resolve git "review descendant"
ln -s -- "$found" "$bin/git"
resolve "${CODEX_BIN:-codex}" "review binary" "${CODEX_BIN:-}"
run=("$found")
# An env shebang would find its interpreter on PATH at exec time, in the PR worktree (the audit of c45f9b5).
first=
IFS= read -r first < "${run[0]}" || true
if [[ $first =~ ^\#![[:space:]]*[^[:space:]]*/env[[:space:]]+(-S[[:space:]]+)?([^[:space:]-][^[:space:]]*)(.*)$ ]]; then
    interpreter=${BASH_REMATCH[2]} split=${BASH_REMATCH[1]} rest=${BASH_REMATCH[3]}
    # env -S splits the rest of the line into the interpreter's own arguments (the local review of 850fc54e).
    words=()
    if [ -n "$split" ]; then
        # env -S quotes, escapes, expands and comments where read -a does not: refuse, never split wrongly (audit:2e3ff49:1).
        if [[ $interpreter$rest == *[\"\'\\\$]* || " $interpreter$rest" =~ [[:space:]]# ]]; then
            echo "local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment the script does not split; refused"
            exit 2
        fi
        read -r -a words <<< "$rest"
    fi
    resolve "$interpreter" "review binary's interpreter"
    run=("$found" ${words[@]+"${words[@]}"} "${run[0]}")
fi
git -C "$W" checkout -q --detach "$head"
base=$(git -C "$W" merge-base main HEAD)
t0=$(date -u +%FT%TZ)
tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
rc=0
(cd "$W" && /usr/bin/env -i PATH="$bin" "${gh_environment[@]}" "${run[@]}" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || rc=$?
if [ "$rc" != 0 ]; then
    # A failed review is no sample: no file, so the next run reviews again (PR #357 thread 4270918132).
    echo "local-review: codex exited $rc; no review file written (transcript $tmp)"
    exit 4
fi
final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp")
# Stripped as a literal, so no character of the worktree path acts as sed syntax (the audit of b6ce4ff); the pattern
# is a quoted variable, which bash 3.2 also reads literally.
prefix="$W/"
final=${final//"$prefix"/}
findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
{
    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
    printf '%s\n\n' "$findings"
    echo '```text'
    printf '%s\n' "$final" | cut -c1-2000
    echo '```'
} > "$out"
rm -f "$tmp"
printf '%s\n' "$findings"
echo "local-review: $n findings ($out)"
[ "$n" = 0 ] || exit 3
