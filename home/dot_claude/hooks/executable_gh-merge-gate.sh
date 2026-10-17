#!/usr/bin/env bash
# @file gh-merge-gate.sh
# @brief PreToolUse gate that lets only a pinned, accepted, green squash merge, a bare update-branch and a gated
#   `gh pr create` run unprompted.
# @description
#   The `gh pr merge` and `gh pr update-branch` ask rules are replaced by this hook (a hook's allow cannot lift an ask
#   rule, so the rules themselves are dropped). Every other merge-shaped command gets `ask`, and so does any failure
#   of this script: no path here falls through to the sandbox's auto-allow.
#   `gh pr update-branch <n> [--repo o/r]` is allowed as is (it adds a merge commit; the new head re-runs CI and needs
#   its own acceptance before it can merge).
#   `gh pr merge <n> --squash --match-head-commit <40-hex> [--repo o/r]` is allowed only when all hold:
#     1. the command is one simple command (no separator, substitution, redirect, quote or newline) and carries no
#        other flag, so `--admin`, `--auto`, `--merge`, `--rebase`, `--body` and the rest all ask;
#     2. it runs from the repository's main checkout (not a linked worker worktree);
#     3. the PR is open, not a draft, targets the repository's default branch, and its head is exactly that sha;
#     4. the default branch's rules require status checks, and every required context is `success` on that sha;
#     5. the main checkout holds an orchestrator acceptance record `.orchestration/acceptance/*.md` whose front matter
#        `"head"` is that sha and whose latest `AGMSG-ACCEPTANCE v1` line says `status=accepted`, and the audit of that
#        head `.orchestration/validation/*-audit-<sha7>.md` exists.
#   GitHub's ruleset still enforces 3 and 4 on its side; this hook adds 1, 2 and 5 before the call is made.
#   `gh pr create` (its ask rule is dropped too) passes only as one plain command (quotes allowed, no `$`, backtick,
#   backslash, operator or newline) using only --base/--head/--title/--body/--body-file/--draft/--fill*/--repo, with an
#   explicit --base that is the default branch or the head branch of an open PR (a stack), and an explicit --head that
#   is pushed. Then: with --draft any non-default head passes (task branches open drafts); otherwise, from the main
#   checkout only, the head must be an `orchestration/` branch whose diff against the base touches only
#   `.orchestration/` (boundary records), or its pushed tip must have an acceptance record as in 5 above.
# @stdin json The PreToolUse payload.
# @stdout json A hookSpecificOutput permission decision, or nothing for unrelated commands.
# @set ${XDG_STATE_HOME:-~/.local/state}/claude/gh-merge-gate.log One line per decision (UTC time, decision, reason).
# @exitcode 0 Always.

decide() {
  local reason=${2//[^[:alnum:][:space:]._:\/=#-]/_}
  local log=${XDG_STATE_HOME:-${HOME}/.local/state}/claude/gh-merge-gate.log
  { mkdir -p "${log%/*}" && printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "${reason}" >>"${log}"; } 2>/dev/null || true
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"gh-merge-gate: %s"}}\n' "$1" "$reason"
  exit 0
}
ask() { decide ask "$1"; }
trap 'ask "internal error"' ERR

command -v jq >/dev/null 2>&1 || {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"gh-merge-gate: jq missing"}}\n'
  exit 0
}
input=$(cat)
cmd=$(jq -r '.tool_input.command // empty' <<<"${input}" 2>/dev/null) || ask "unreadable payload"
cwd=$(jq -r '.cwd // empty' <<<"${input}" 2>/dev/null) || ask "unreadable payload"

shape='(^|[^[:alnum:]_-])(pr[[:space:]]+(merge|update-branch|create)|pulls/[^[:space:]]*/(merge|update-branch))([^[:alnum:]_-]|$)'
grep -Eq "${shape}" <<<"${cmd}" || exit 0

# Require the payload's cwd to be the repository's main checkout; sets top.
main_checkout() {
  [[ -n ${cwd} && -d ${cwd} ]] || ask "the payload names no existing working directory"
  cd "${cwd}" || ask "no working directory"
  top=$(git rev-parse --show-toplevel 2>/dev/null) || ask "not in a git checkout"
  local gitdir common
  gitdir=$(git rev-parse --path-format=absolute --git-dir 2>/dev/null) || ask "no git dir"
  common=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || ask "no git common dir"
  [[ ${gitdir} == "${common}" ]] || ask "$1 only from the main checkout, not a linked worktree"
}

# Find the acceptance record pinning head $1 whose latest verdict is accepted; sets accepted.
require_accepted() {
  local record verdict
  shopt -s nullglob
  accepted=""
  for record in "${top}"/.orchestration/acceptance/*.md; do
    [[ -L ${record} ]] && continue
    if grep -Eq "^[[:space:]]*\"head\":[[:space:]]*\"$1\"" "${record}"; then accepted=${record}; break; fi
  done
  [[ -n ${accepted} ]] || ask "no acceptance record pins head ${1:0:12}"
  verdict=$(grep -Eo 'AGMSG-ACCEPTANCE v1 task_id=[^[:space:]]+ status=[a-z-]+' "${accepted}" | tail -n 1 | sed 's/.*status=//')
  [[ ${verdict} == accepted ]] || ask "the latest acceptance status in ${accepted##*/} is ${verdict:-missing} not accepted"
}

gate_create() {
  local py tokens t i n repo="" base="" head="" draft=0 nwo default head_sha files
  case "${cmd}" in
    *[\`\$\\]* | *$'\n'*) ask "create: no substitution, backslash or newline" ;;
    *) ;;
  esac
  py=$(command -v python3) || ask "create: python3 missing"
  tokens=()
  while IFS= read -r -d '' t; do tokens+=("${t}"); done < <("${py}" -c '
import shlex, sys
lexer = shlex.shlex(sys.argv[1], posix=True, punctuation_chars=True)
lexer.whitespace_split = True
try:
    words = list(lexer)
except ValueError:
    sys.exit(3)
if any(word and all(c in "();<>|&" for c in word) for word in words):
    sys.exit(4)
sys.stdout.write("".join(word + "\0" for word in words))
' "${cmd}")
  n=${#tokens[@]}
  ((n >= 3)) && [[ ${tokens[0]} == gh && ${tokens[1]} == pr && ${tokens[2]} == create ]] \
    || ask "create: not a single plain gh pr create"
  i=3
  while ((i < n)); do
    t=${tokens[i]}
    case "${t}" in
      --base | -B) base=${tokens[i + 1]:-}; ((i += 2)); continue ;;
      --head | -H) head=${tokens[i + 1]:-}; ((i += 2)); continue ;;
      --repo | -R) repo=${tokens[i + 1]:-}; ((i += 2)); continue ;;
      --title | -t | --body | -b | --body-file | -F) ((i + 1 < n)) || ask "create: ${t} needs a value"; ((i += 2)); continue ;;
      --base=*) base=${t#*=} ;;
      --head=*) head=${t#*=} ;;
      --repo=*) repo=${t#*=} ;;
      --title=* | --body=* | --body-file=*) ;;
      --draft | -d) draft=1 ;;
      --fill | -f | --fill-first | --fill-verbose) ;;
      *) ask "create: flag or argument ${t} is outside the gated form" ;;
    esac
    ((i += 1))
  done
  [[ -z ${repo} || ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || ask "create: bad --repo"
  [[ ${base} =~ ^[A-Za-z0-9._/-]+$ && ${base} != -* ]] || ask "create: needs an explicit --base"
  [[ ${head} =~ ^[A-Za-z0-9._/-]+$ && ${head} != -* ]] || ask "create: needs an explicit --head branch"
  [[ -n ${cwd} && -d ${cwd} ]] || ask "the payload names no existing working directory"
  cd "${cwd}" || ask "no working directory"
  nwo=$(gh repo view ${repo:+"${repo}"} --json nameWithOwner --jq .nameWithOwner 2>/dev/null) || ask "gh repo view failed"
  default=$(gh repo view "${nwo}" --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null) || ask "no default branch"
  [[ ${head} != "${default}" ]] || ask "create: the head is the default branch"
  head_sha=$(gh api "repos/${nwo}/branches/${head}" --jq .commit.sha 2>/dev/null) || ask "create: ${head} is not pushed"
  [[ ${head_sha} =~ ^[0-9a-f]{40}$ ]] || ask "create: ${head} is not pushed"
  if [[ ${base} != "${default}" ]]; then
    [[ $(gh pr list --repo "${nwo}" --head "${base}" --state open --json number --jq length 2>/dev/null) =~ ^[1-9] ]] \
      || ask "create: base ${base} is neither ${default} nor the head of an open PR"
  fi
  ((draft)) && decide allow "draft PR of ${head} onto ${base}"
  main_checkout "a ready PR"
  if [[ ${head} == orchestration/* ]]; then
    files=$(gh api "repos/${nwo}/compare/${base}...${head}" --jq '(.files | length), (.files[].filename)' 2>/dev/null) \
      || ask "create: cannot compare ${base}...${head}"
    (($(head -n 1 <<<"${files}") > 0 && $(head -n 1 <<<"${files}") < 300)) || ask "create: records diff empty or too large"
    tail -n +2 <<<"${files}" | grep -qv '^\.orchestration/' && ask "create: ${head} touches files outside .orchestration"
    decide allow "records PR of ${head} onto ${base}"
  fi
  require_accepted "${head_sha}"
  decide allow "PR of ${head} at ${head_sha:0:12} accepted in ${accepted##*/}"
}

[[ ${cmd} =~ ^gh[[:space:]]+pr[[:space:]]+create([[:space:]]|$) ]] && gate_create

case "${cmd}" in
  *[\;\&\|\<\>\`\$\(\)\{\}\'\"\\]* | *$'\n'*) ask "not a single simple command" ;;
  *) ;;
esac
read -ra w <<<"${cmd}"
[[ ${w[0]:-} == gh && ${w[1]:-} == pr ]] || ask "only the gh pr form can pass"
sub=${w[2]:-}
[[ ${sub} == merge || ${sub} == update-branch ]] || ask "unexpected subcommand"

repo="" pr="" sha="" squash=0 i=3
while ((i < ${#w[@]})); do
  t=${w[i]}
  case "${t}" in
    --repo | -R) repo=${w[i + 1]:-}; ((i += 2)); continue ;;
    --repo=*) repo=${t#--repo=} ;;
    --squash | -s) [[ ${sub} == merge ]] || ask "flag ${t}"; squash=1 ;;
    --match-head-commit) [[ ${sub} == merge ]] || ask "flag ${t}"; sha=${w[i + 1]:-}; ((i += 2)); continue ;;
    --match-head-commit=*) [[ ${sub} == merge ]] || ask "flag ${t}"; sha=${t#*=} ;;
    *)
      [[ -z ${pr} && ${t} =~ ^[0-9]+$ ]] || ask "argument ${t} is outside the pinned form"
      pr=${t}
      ;;
  esac
  ((i += 1))
done
[[ -n ${pr} ]] || ask "no PR number"
[[ -z ${repo} || ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || ask "bad --repo"
[[ ${sub} == update-branch ]] && decide allow "update-branch of PR ${pr}"

[[ ${squash} == 1 ]] || ask "merge must be --squash"
[[ ${sha} =~ ^[0-9a-f]{40}$ ]] || ask "merge must carry --match-head-commit with a full sha"

main_checkout "merge"
R=()
[[ -n ${repo} ]] && R=(--repo "${repo}")
nwo=$(gh repo view ${repo:+"${repo}"} --json nameWithOwner --jq .nameWithOwner 2>/dev/null) || ask "gh repo view failed"
default=$(gh repo view "${nwo}" --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null) || ask "no default branch"
view=$(gh pr view "${pr}" "${R[@]}" --json headRefOid,baseRefName,state,isDraft 2>/dev/null) || ask "gh pr view failed"
[[ $(jq -r .state <<<"${view}") == OPEN ]] || ask "PR ${pr} is not open"
[[ $(jq -r .isDraft <<<"${view}") == false ]] || ask "PR ${pr} is a draft"
[[ $(jq -r .headRefOid <<<"${view}") == "${sha}" ]] || ask "PR ${pr} head is not ${sha}"
[[ $(jq -r .baseRefName <<<"${view}") == "${default}" ]] || ask "PR ${pr} does not target ${default}"

required=$(gh api "repos/${nwo}/rules/branches/${default}" \
  --jq '[.[] | select(.type == "required_status_checks") | .parameters.required_status_checks[].context] | unique | .[]' \
  2>/dev/null) || ask "cannot read the branch rules"
[[ -n ${required} ]] || ask "${default} requires no status checks"
runs=$(gh api --paginate "repos/${nwo}/commits/${sha}/check-runs?per_page=100" \
  --jq '.check_runs[] | select(.conclusion == "success") | .name' 2>/dev/null) || ask "cannot read check runs"
statuses=$(gh api "repos/${nwo}/commits/${sha}/status" --jq '.statuses[] | select(.state == "success") | .context' \
  2>/dev/null) || ask "cannot read statuses"
while IFS= read -r ctx; do
  grep -Fxq -- "${ctx}" <<<"${runs}"$'\n'"${statuses}" || ask "required check ${ctx} is not green on ${sha:0:12}"
done <<<"${required}"

require_accepted "${sha}"
audits=("${top}"/.orchestration/validation/*-audit-"${sha:0:7}".md)
((${#audits[@]} > 0)) || ask "no audit of ${sha:0:7}"

decide allow "PR ${pr} head ${sha:0:12} accepted in ${accepted##*/} with green required checks"
