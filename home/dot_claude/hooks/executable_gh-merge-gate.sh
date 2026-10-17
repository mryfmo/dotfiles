#!/usr/bin/env bash
# @file gh-merge-gate.sh
# @brief PreToolUse gate that lets only a pinned, accepted, green squash merge and a bare update-branch run unprompted.
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

shape='(^|[^[:alnum:]_-])(pr[[:space:]]+(merge|update-branch)|pulls/[^[:space:]]*/(merge|update-branch))([^[:alnum:]_-]|$)'
grep -Eq "${shape}" <<<"${cmd}" || exit 0

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

[[ -n ${cwd} && -d ${cwd} ]] || ask "the payload names no existing working directory"
cd "${cwd}" || ask "no working directory"
top=$(git rev-parse --show-toplevel 2>/dev/null) || ask "not in a git checkout"
gitdir=$(git rev-parse --path-format=absolute --git-dir 2>/dev/null) || ask "no git dir"
common=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || ask "no git common dir"
[[ ${gitdir} == "${common}" ]] || ask "merge only from the main checkout, not a linked worktree"

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

shopt -s nullglob
accepted=""
for record in "${top}"/.orchestration/acceptance/*.md; do
  [[ -L ${record} ]] && continue
  if grep -Eq "^[[:space:]]*\"head\":[[:space:]]*\"${sha}\"" "${record}"; then accepted=${record}; break; fi
done
[[ -n ${accepted} ]] || ask "no acceptance record pins head ${sha:0:12}"
verdict=$(grep -Eo 'AGMSG-ACCEPTANCE v1 task_id=[^[:space:]]+ status=[a-z-]+' "${accepted}" | tail -n 1 | sed 's/.*status=//')
[[ ${verdict} == accepted ]] || ask "the latest acceptance status in ${accepted##*/} is ${verdict:-missing} not accepted"
audits=("${top}"/.orchestration/validation/*-audit-"${sha:0:7}".md)
((${#audits[@]} > 0)) || ask "no audit of ${sha:0:7}"

decide allow "PR ${pr} head ${sha:0:12} accepted in ${accepted##*/} with green required checks"
