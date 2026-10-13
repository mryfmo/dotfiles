#!/usr/bin/env bash
# @file regime-counters.sh
# @brief Count the INV-6 reset signals of one agmsg task from history and GitHub.
# @description
#   Plan 006 A3, the counting half of INV-6 (V3a wires it into the hook and the
#   gate). History is the whole team history, read through agmsg's storage
#   facade the way scripts/agent-stop-gate.sh read_history reads it; GitHub is
#   `gh api --paginate` on this repository. A message's task, status and verdict
#   are its first `task_id=`, `status=` and `verdict=` tokens, split on whitespace runs (tabs too) as dispatch.sh reads a line (later ones are
#   free text). Counts follow INV-6's sentence only: amendments = AGMSG-TASKs -
#   1; revises = AGMSG-RESULTs - 1, whatever their status; questions = PONGs of
#   status question; withdrawn = ACCEPTANCEs of status withdrawn, informational.
#   Bot heads are the distinct `original_commit_id` of Codex Bot
#   (`chatgpt-codex-connector[bot]`) review comments whose title line carries a
#   P0 or P1 badge, counted only for commits after the first RESULT's `head=` in
#   the PR's commit order. No PR, a gh failure, a first RESULT without `head=`,
#   that head missing from the commits, or a counted comment on a commit outside
#   them or without `original_commit_id` print `unknown`, never 0. S1 comes from
#   the task's acceptance record `.orchestration/acceptance/<task>.md` when its
#   block between the first two `---` lines is a JSON object whose `task` is the
#   counted task and whose `ledger` is a list of `{id, class}` rows, each an
#   object with a string `id` and a `[a-z0-9-]` `class` (read with jq only):
#   every class with three or more rows prints `S1: class=<slug> count=<n>
#   source=record`. Without such a record (none, or a prose one), Codex Bot
#   thread titles grouped by their first three words (badge stripped,
#   lower-cased) seen three or more times on the PR print `S1: candidate
#   class=unclassified count=<n> title=<JSON string>`: the title is data for
#   people, never a class a procedure substitutes into a command. A block that
#   is not JSON, or a ledger row of another shape, is no record either, and those
#   lines then end in `source=record-ignored:<reason>`, one of the fixed slugs
#   `block-not-json`, `ledger-row-not-object`, `id-not-string` and
#   `class-not-slug` (thread 4255079204), never text from the record.
#   Output: the count line; one `S2:` line per INV-6 threshold reached; the
#   `S1:` lines (none with --history-only); a `detail:` line (the PR: digits, `none` when
#   no RESULT carries `pr=`, `invalid` for another value; the TASK senders, every
#   counted message id and Bot head); with --reset-hash, a `reset:` line.
#   Every line ends in `source=live`, or `source=fixture` when a test seam fed it.
# @arg $1 string Task id.
# @option --team <team> agmsg team (default dotfiles-conformance).
# @option --pr <n> Pull request (default: the first `pr=` token of the task's RESULTs).
# @option --history-only Skip GitHub (`bot_p1_heads_after_result=skipped`, no S1 lines); for the Stop hook.
# @option --reset-hash <sha256> Also print who, other than the task's TASK senders, sent `AGMSG-RESULT task_id=<source> ... verdict=accept design_sha256=<sha256>`.
# @option --reset-source <task id> The task id that accept must carry (the reset record's `redesign_source`); without it nothing is accepted.
# @option --list-tasks Print each task id with an AGMSG-TASK in history instead of counting one.
# @option --history-file <tsv> Test seam: `id at from to body` rows (jq @tsv) instead of the store.
# @option --github-file <json> Test seam: `{"comments": [...], "commits": [...]}`, gh api objects, instead of gh.
# @exitcode 0 Counted (or listed).
# @exitcode 1 The agmsg history is unreadable.
# @exitcode 2 Usage error.
# @example
#   scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --pr 317
# shellcheck disable=SC2016 # single-quoted jq programs, not shell expansions
set -euo pipefail

usage() {
    echo "usage: regime-counters.sh <task id> [--team <team>] [--pr <n>] [--history-only] [--reset-hash <sha256> --reset-source <task id>] | --list-tasks [--team <team>]" >&2
    exit 2
}
# INV-6's constant for every count; changing it is a hashed design change (INV-7).
threshold=2
team=dotfiles-conformance task="" pr="" reset_hash="" reset_source="" history_only=false list=false history_file="" github_file=""
while (($#)); do
    case $1 in
    --history-only) history_only=true ;;
    --list-tasks) list=true ;;
    --team | --pr | --reset-hash | --reset-source | --history-file | --github-file)
        (($# > 1)) || usage
        name="${1#--}" && printf -v "${name//-/_}" '%s' "$2" && shift
        ;;
    -*) usage ;;
    *)
        [[ -z ${task} ]] || usage
        task=$1
        ;;
    esac
    shift
done
[[ ${list} == true || -n ${task} ]] || usage
[[ -z ${pr} || ${pr} =~ ^[0-9]+$ ]] || usage
[[ -z ${reset_hash} || ${reset_hash} =~ ^[0-9a-f]{64}$ ]] || usage
source=live
[[ -z ${history_file}${github_file} ]] || source=fixture
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"

# @description Print the team history as `id at from to body` rows, chronological.
#   Same guarded read as agent-stop-gate.sh: a sqlite store at another schema
#   revision is unreadable, never re-initialized. Call it only in $( ).
# @arg $1 string Team.
read_history() {
    set +e # the agmsg library is not written for errexit
    export AGMSG_BUSY_TIMEOUT=1000
    # shellcheck disable=SC1091
    source "${HOME}/.agents/skills/agmsg/scripts/lib/storage.sh" && agmsg_storage_load && storage_store_exists "$1" || return 1
    if [[ ${_AGMSG_STORAGE_LOADED:-} == sqlite ]]; then
        [[ "$(agmsg_sqlite "$(_sqlite_db "$1")" 'PRAGMA user_version;' 2> /dev/null)" == "${_AGMSG_STORAGE_SCHEMA_REV:-}" ]] || return 1
    fi
    storage_history "$1" | jq -r '[.id, .at, .from, .to, .body] | @tsv'
}

# @description Print one PR list endpoint as a JSON array, every page.
# @arg $1 int Pull request.
# @arg $2 string `comments` or `commits`.
gh_list() {
    (cd -- "${root}" && gh api --paginate "repos/{owner}/{repo}/pulls/$1/$2" --jq '.[]' 2> /dev/null) | jq -cs .
}

if [[ -n ${history_file} ]]; then
    history="$(cat -- "${history_file}")"
elif ! history="$(read_history "${team}")"; then
    echo "regime-counters: the agmsg history of ${team} is unreadable" >&2
    exit 1
fi
rows='def tok($k): [.toks[] | select(startswith($k + "="))][0] // null | if . then .[($k | length) + 1:] else null end;
def rows: inputs | split("\t") | {id: .[0], at: .[1], from: .[2], body: (.[4:] | join("\t"))}
  | .toks = [.body | gsub("\\\\(?<c>[tnr\\\\])"; {t: "\t", n: "\n", r: "\r"}[.c] // "\\") | splits("\\s+") | select(. != "")] | .task = (tok("task_id") // "") | select(.toks[1] == "v1");'
if [[ ${list} == true ]]; then
    jq -nrR --arg s "${source}" "${rows}"'[rows | select(.toks[0] == "AGMSG-TASK" and .task != "") | .task] | unique[] | "\(.) source=\($s)"' <<< "${history}"
    exit 0
fi
counts="$(jq -ncR --arg t "${task}" --arg pr "${pr}" --arg hash "${reset_hash}" --arg src "${reset_source}" "${rows}"'[rows] as $all | [$all[] | select(.task == $t)] as $m
  | def kind($k): [$m[] | select(.toks[0] == $k)];
  kind("AGMSG-TASK") as $tasks | kind("AGMSG-RESULT") as $results | ([$tasks[].from] | unique) as $authors
  | {tasks: [$tasks[].id], results: [$results[].id], authors: $authors,
     questions: [kind("AGMSG-PONG")[] | select(tok("status") == "question") | .id],
     withdrawn: [kind("AGMSG-ACCEPTANCE")[] | select(tok("status") == "withdrawn") | .id],
     head: ($results[0] // null | if . then tok("head") else null end | if . and test("^[0-9a-f]{7,40}$") then . else null end),
     pr: (if $pr != "" then $pr else [$results[] | tok("pr") | select(.)][0] | if . == null or test("^[0-9]+$") then . else "invalid" end end),
     first: $tasks[0].at, last: $results[-1].at,
     accepted_by: [$all[] | select($hash != "" and $src != "" and .task == $src and .toks[0] == "AGMSG-RESULT" and tok("verdict") == "accept" and tok("design_sha256") == $hash)
       | .from | select(. as $f | any($authors[]; . == $f) | not)] | unique}' <<< "${history}")"

# {rec: the record's JSON block}, {why: <slug>} for a block it ignores, or null for no record, a prose one or another task's.
record=null
if [[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && -f ${root}/.orchestration/acceptance/${task}.md ]]; then
    record="$(jq -cRs 'split("\n") | if .[0] == "---" then .[1:] | index("---") as $e | if $e then .[:$e] | join("\n")
      | (try {rec: fromjson} catch {why: "block-not-json"})
      | if has("why") then . elif (.rec | type) == "object" and (.rec.ledger | type) == "array" and .rec.task == $t then
          [.rec.ledger[] | if type != "object" then "ledger-row-not-object" elif (.id | type) != "string" then "id-not-string"
            elif (.class | type) != "string" or (.class | test("^[a-z0-9-]+$") | not) then "class-not-slug" else empty end][0] as $why
          | if $why then {why: $why} else . end
        else null end
      else null end else null end' --arg t "${task}" "${root}/.orchestration/acceptance/${task}.md")"
fi

github=null state=skipped
if [[ ${history_only} == false ]]; then
    state=unknown
    pr="$(jq -r '.pr // empty' <<< "${counts}")"
    if [[ -n ${github_file} ]]; then
        github="$(cat -- "${github_file}")" && state=ok
    elif [[ ${pr} =~ ^[0-9]+$ ]] && comments="$(gh_list "${pr}" comments)" && commits="$(gh_list "${pr}" commits)"; then
        github="$(printf '{"comments":%s,"commits":%s}' "${comments}" "${commits}")" && state=ok
    fi
fi

jq -r --argjson c "${counts}" --argjson rec "${record}" --arg state "${state}" --arg t "${task}" --arg s "${source}" --arg hash "${reset_hash}" --arg src "${reset_source}" --argjson limit "${threshold}" '. as $gh
  | def title: (.body // "") | split("\n")[0]; def codex: .user.login == "chatgpt-codex-connector[bot]";
  def bot: if $state != "ok" then $state elif $c.head == null then "unknown" else
      [$gh.commits[].sha] as $shas | [range(0; $shas | length) | select($shas[.] | startswith($c.head))][0] as $i
      | [$gh.comments[] | select(codex and (title | test("!\\[P[01] Badge\\]")))] as $p
      | if $i == null or any($p[]; .original_commit_id as $o | $o == null or (any($shas[]; . == $o) | not)) then "unknown"
        else [$p[].original_commit_id | select(. as $o | any($shas[$i + 1:][]; . == $o))] | unique end end;
  def hm: (. / 60 | floor) as $m | "\($m / 60 | floor):\($m % 60 | tostring | if length < 2 then "0" + . else . end)";
  def list: if length > 0 then join(",") else "-" end;
  bot as $b | ($b | if type == "array" then length else . end) as $n
  | ([($c.tasks | length) - 1, 0] | max) as $amendments | ([($c.results | length) - 1, 0] | max) as $revises
  | "task=\($t) tasks=\($c.tasks | length) amendments=\($amendments) questions=\($c.questions | length) results=\($c.results | length) withdrawn=\($c.withdrawn | length) revises=\($revises) first_result_head=\($c.head // "none") bot_p1_heads_after_result=\($n) audits=unknown wall=\($c.first // "none")..\($c.last // "none") (\(if $c.first and $c.last then ($c.last | fromdateiso8601) - ($c.first | fromdateiso8601) | hm else "-" end)) source=\($s)",
    ([["revises", $revises], ["amendments", $amendments], ["questions", ($c.questions | length)], ["bot_p1_heads", $n]][]
      | select((.[1] | type) == "number" and .[1] >= $limit) | "S2: \(.[0]) \(.[1]) >= \($limit) source=\($s)"),
    (if $state == "skipped" then empty
      elif $rec.rec != null then [$rec.rec.ledger[].class] | group_by(.)[] | select(length >= 3)
        | "S1: class=\(.[0]) count=\(length) source=record"
      elif $state == "ok" then [$gh.comments[] | select(codex and .in_reply_to_id == null) | title
        | gsub("!\\[[^\\]]*\\]\\([^)]*\\)|</?sub>|\\*\\*"; "") | sub("^\\s+"; "") | sub("\\s+$"; "")
        | {key: (ascii_downcase | [splits("\\s+") | select(. != "")][0:3] | join(" ")), title: .} | select(.key != "")]
      | group_by(.key)[] | select(length >= 3) | "S1: candidate class=unclassified count=\(length) title=\(.[0].title | tojson) source=\(if $rec.why then "record-ignored:\($rec.why)" else $s end)"
      else empty end),
    "detail: pr=\($c.pr // "none") authors=\($c.authors | list) tasks=\($c.tasks | list) results=\($c.results | list) questions=\($c.questions | list) withdrawn=\($c.withdrawn | list) bot_heads=\(if ($b | type) == "array" then $b | list else "-" end) source=\($s)",
    (if $hash != "" then "reset: design_sha256=\($hash) redesign_source=\(if $src != "" then $src else "none" end) accepted_by=\($c.accepted_by | if length > 0 then join(",") else "none" end) source=\($s)" else empty end)' <<< "${github}"
