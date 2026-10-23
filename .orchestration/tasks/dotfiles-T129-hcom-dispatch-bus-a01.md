---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a01
kind: code
security: true
previous_sha256: 1fed50618ef0815e290115b6e9f85820dcb66376011a9e28fb1f20a194924631
allowed_files:
  - home/dot_local/bin/common/executable_hcom-dispatch
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - scripts/orchestrator/bus-read.sh
  - scripts/regime-counters.sh
  - tests/unit/test_hcom_dispatch.py
  - tests/unit/test_orchestrator_tools.py
  - tests/unit/test_regime_counters.py
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a01/**
after: [dotfiles-T129-audit-inherit-replan-json-a01]
threat_table:
  - control: home/dot_local/bin/common/executable_hcom-dispatch (new; sends one bus line as agmsg-dispatch does today)
    disposition: "residual: the line is passed to hcom as one argument after `--` and never evaluated; the sender, recipient and team are checked against the identity grammar agmsg-dispatch uses; a fake hcom and a fake herdr on PATH record every argv in the tests"
  - control: scripts/orchestrator/bus-history.sh (new; the one read of hcom's history for every orchestrator script)
    disposition: "residual: read-only (hcom's own read command, or sqlite3 -readonly with a schema guard that refuses an unknown revision and never initialises a store); rows are data, parsed field by field with jq downstream; the tests run it on a fixture store under $TMPDIR and assert the store's bytes are unchanged"
  - control: the PR edits scripts/orchestrator/dispatch.sh only for items 3 and 4
    disposition: "residual: every current refusal stays and each new refusal (previous_head=, check=, the counters run, the record argument) has a red-then-green fixture; the line still reaches the sender byte for byte"
  - control: the PR edits scripts/orchestrator/bus-read.sh only for item 5
    disposition: "residual: the history source changes, the jq that classifies rows does not; the five bus_read tests re-run on the new seam"
  - control: the PR edits scripts/regime-counters.sh only for item 6
    disposition: "residual: the gate reads its S1 line, so the count rule is widened only in the direction the plan names (the larger of two counts); --history-file keeps the 20 seam tests unchanged"
  - control: tests/unit/test_hcom_dispatch.py (new)
    disposition: "residual: fake hcom and herdr on PATH in a temporary directory; nothing reaches a live bus"
  - control: tests/unit/test_orchestrator_tools.py
    disposition: "residual: fixtures only; the AGMSG_SCRIPTS stub of history.sh becomes a stub of the new reader; one fixture per new refusal"
  - control: tests/unit/test_regime_counters.py
    disposition: "residual: fixtures only; two new count fixtures, the seam tests untouched"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-hcom-dispatch-bus-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-hcom-dispatch-bus-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: "bus rows as a trust boundary (worker-written RESULT and PONG bodies, PR-controlled text quoted in them)"
    disposition: "residual: as today, every reader tokenises `key=value` fields with jq and never evals a body; the new refusals read tokens of the orchestrator's own line, not a worker's"
  - control: in-process effects
    disposition: "residual: the tests run the scripts as subprocesses with stub hcom, herdr, uv, gh and the reader on PATH in a temporary repository; nothing touches a live bus, pane or PR"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run bash, jq, sqlite3 and hcom; HCOM_DIR is honoured and never set by a script"
  - control: new or renamed scripts
    disposition: "residual: two new scripts, both named in allowed_files; agmsg-dispatch stays until PR E removes it (.chezmoiremove); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'dispatch.sh hands its line to agmsg-dispatch today (two call sites)'
    command: '/usr/bin/grep -c "agmsg-dispatch" scripts/orchestrator/dispatch.sh'
    output: |-
      4
  - claim: 'bus-read.sh and regime-counters.sh read the agmsg store through history.sh or storage.sh'
    command: '/usr/bin/grep -c "history.sh" scripts/orchestrator/bus-read.sh; /usr/bin/grep -c "storage.sh" scripts/regime-counters.sh'
    output: |-
      2
      1
  - claim: 'replay.sh reads no bus at all, so the plan''s file list is corrected: it is not in this task'
    command: '/usr/bin/grep -c "history.sh\|storage.sh\|sqlite3" scripts/orchestrator/replay.sh'
    output: |-
      0
  - claim: 'no hcom-dispatch exists yet'
    command: '/bin/ls home/dot_local/bin/common/executable_hcom-dispatch 2>&1'
    output: |-
      ls: home/dot_local/bin/common/executable_hcom-dispatch: No such file or directory
  - claim: 'the counters define revises as RESULTs minus one today'
    command: '/usr/bin/grep -n "revises = AGMSG-RESULTs - 1" scripts/regime-counters.sh'
    output: |-
      11:#   1; revises = AGMSG-RESULTs - 1, whatever their status; questions = PONGs of
  - claim: 'hcom is installed by the operator''s make update of 2026-10-18 08:1x JST (pin 0.7.30); `~/.local/bin/hcom --version` printed `hcom 0.7.30` at dispatch'
    command: '/bin/ls ~/.local/bin/hcom 2>&1 | sed "s#$HOME#~#"'
    output: |-
      ~/.local/bin/hcom
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a01 — plan 023 PR C, stage 1: hcom-dispatch and the bus readers

Written 2026-10-18 by the orchestrator seat from plan 023 (`.orchestration/plans/023-omp-hcom-migration.md`, "## Pull requests" item C and the classification table). Stage 1 of PR C: the dispatcher sends over hcom, the three readers read hcom, the dispatcher's line-level refusals land. The launcher half (`herdr-agents` seating `hcom omp`, the launch record, the seat check, the live-process refusal, the worker-side hcom hook) is stage 2, see "Deferred".

**Wave conflicts (serial, not concurrent):** `scripts/regime-counters.sh`, `tests/unit/test_regime_counters.py` and `tests/unit/test_orchestrator_tools.py` are in the `allowed_files` of `dotfiles-T129-audit-inherit-replan-json-a01` (PR #390), hence `after:`, and of its `-followup-a01`, which runs before this task if it is dispatched at all. Stage 2's `home/dot_local/bin/common/executable_herdr-agents` and `tests/unit/test_herdr_agents.py` are in `dotfiles-T129-integration-seat-result-gate-cap-a01`'s list, and `scripts/check-agent-runtime.py` in `dotfiles-T129-pstack-asset-a01`'s. `home/dot_agents/agent-config.yaml` is not touched.

**Unverified at drafting (hcom absent, `~/.hcom` absent, no wheel cached):** every hcom flag below comes from plan 023 "Facts read today" (`hcom send -b @name -- "<text>"`, `hcom list`, `hcom events --wait`, `--tag <team>`, `HCOM_DIR`), not from a run. Item 0 verifies each before it is used; nothing unverified goes into code or a test.

## Goal

`scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> [record]` sends over hcom and records the read marker from hcom's history; `bus-read.sh` and `regime-counters.sh` count from the same history; a revise line without `previous_head=`, without `check=`, without a record, or whose counters run fails is refused before anything is sent; the round count is the larger of RESULTs minus one and the revise lines. All tests green with the agmsg store absent.

## Work items (each with its test; one fixture per item, red before and green after)

0. Facts first, pasted into report.md before any code (hcom 0.7.30 is installed at `~/.local/bin/hcom` since 08:1x JST; a missing hcom is still a `AGMSG-PONG v1 status=blocked`): `~/.local/bin/hcom --version`; `hcom --help` and the `--help` of `send`, `list`, `events` (or whatever the top-level help names for reading history); the store: the default `HCOM_DIR`, the SQLite file name, `sqlite3 -readonly <db> '.schema'` (the message table and its id, time, sender, recipient, body and read-marker columns), and `PRAGMA user_version`; whether `hcom send` lets a non-seat process name the sender (`<from>`) and how a tag scopes delivery; whether an `hcom` read command prints every message of a tag with id, time, from, to and body in a machine form. Decision rule, written in report.md: the reader (item 1) uses hcom's read command when one prints those five fields for a whole tag; otherwise it reads the SQLite file with `sqlite3 -readonly` behind a guard on `user_version` (or the exact table shape) that exits 1 on a mismatch and never writes.
1. `scripts/orchestrator/bus-history.sh <team> [--limit <n>]`: prints `id<TAB>at<TAB>from<TAB>to<TAB>body` rows, chronological, `at` as ISO-8601 UTC (what `bus-read.sh`'s `fromdateiso8601` and `regime-counters.sh`'s `read_history` consume today); honours `HCOM_DIR`; exit 1 with one stderr line when the store is unreadable or at another revision. shdoc header. Test (test_orchestrator_tools.py): a fixture store built by the test from item 0's schema under `$TMPDIR` gives the rows; a store with another `user_version` gives exit 1 and unchanged bytes (sha256 before and after); the `hcom` route, if chosen, runs against a fake `hcom` on PATH.
2. `home/dot_local/bin/common/executable_hcom-dispatch <team> <from> <to> <pane> <words…>`: agmsg-dispatch's argument form (its `@arg` lines 16 to 20) so every caller keeps its call; joins the words with spaces; sends with the `hcom send` form item 0 verified, the text as one argument after `--`; confirms receipt the way item 0 found (a read marker in the history, or the events wait), within agmsg-dispatch's deadline discipline (its polling block from line 88); when unconfirmed, nudges once with `herdr pane run "<pane>" "hcom: new message for <to>"` (the current wake path, line 84) and exits with the same non-zero status agmsg-dispatch documents for an unconfirmed send. shdoc header with `@arg`, `@exitcode`. Test (`tests/unit/test_hcom_dispatch.py`, the `test_agmsg_dispatch.py` pattern, 12 tests there today): argv order and the `--` separator; a line starting with `-` reaches hcom unparsed; a line with tabs and quotes reaches hcom byte for byte; the confirmed path exits 0 without touching herdr; the unconfirmed path nudges once and exits non-zero.
3. `dispatch.sh`, the send and the window: both `agmsg-dispatch` call sites (lines 245 and 350) become `hcom-dispatch`; the two `history.sh <team> "" <N>` windows (lines 46 to 59 and 347) become `bus-history.sh <team> --limit <N>` through one env seam `BUS_HISTORY` (default: the script beside dispatch.sh) that replaces the `AGMSG_SCRIPTS` seam; read markers come from item 0's column. Every current refusal and the record block logic stay byte-identical in behaviour (the existing dispatch tests re-run on the new seam, `test_dispatch_reads_a_bounded_history_window` included).
4. `dispatch.sh`, the revise refusals (the rows `audit:4460d52:3 revise-line-contract` and `audit:4460d52:4 counters-not-pasted` of `.orchestration/acceptance/dotfiles-T128-s1-replan-gate-a01.md` lines 107 to 108, which plan 023 moves here from the discarded tools a04 owner task). For an `AGMSG-ACCEPTANCE v1` line whose `verdict=revise`: (a) `previous_head=` present once, 40 lowercase hex; (b) `check=` present once, non-empty (the test selector the seat runs); (c) a record argument present, else exit 1 naming it (the counters paste needs a home); (d) `scripts/regime-counters.sh <task_id> --team <team> --history-only` run before the send; a non-zero exit refuses with its stderr; its stdout lines are appended to the record's JSON block as one string in a `counters` list (`"<task_id> <ISO time> <lines joined by '; '>"`, the block written as today: `sort_keys`, `indent=2`, key created when absent), so the paste the counters bullet requires is made by the tool, not recalled. Test: one fixture per refusal (a) to (d) plus one green revise line whose record gains the `counters` entry; a `verdict=accept` line is untouched by (a) to (d).
5. `bus-read.sh`: line 49's `history.sh` read becomes `bus-history.sh <team> --limit <limit>` through the same `BUS_HISTORY` seam; the jq is unchanged. Test: the five `test_bus_read_*` fixtures re-run on the new seam.
6. `regime-counters.sh`: `read_history()` (lines 88 to 102) calls `bus-history.sh "$1"` and drops the `storage.sh` source; the round count becomes the larger of (RESULTs minus one) and (ACCEPTANCE lines of this task with `verdict=revise`), the header comment at line 11 and the `revises=` output unchanged in form. Test: two fixtures through `--history-file`: 2 RESULTs and 3 revise lines give `revises=3`; 4 RESULTs and 1 revise line give `revises=3`; the 20 seam tests untouched.
7. Not touched, with the reason in report.md: `scripts/orchestrator/replay.sh` (no bus read, premise 3; its only `agmsg` hit is a SKILL path in an example); `scripts/agent-stop-gate.sh` (the Claude Stop hook keeps the current seats working; its rule becomes the hcom hook in stage 2 and PR E removes it); the agmsg-orchestration SKILL and rule text (PR E; no text where a check exists); `agmsg-dispatch` itself and `.chezmoiremove` (PR E).

## Deferred to dotfiles-T129-hcom-dispatch-bus-a02 (the orchestrator writes it after this PR merges; listed so nothing is lost)

`herdr-agents --add-worker` seats a worker with `hcom omp --tag <team> --dir <worktree>` (the model from `MODEL_PROFILE_<NAME>_OMP_MODEL`, PR B stage 1; the omp flag that sets the model is a VERIFY there) in place of `spawn.sh` (lines 1870 to 1873); it writes `<run dir>/<seat>.launch.json` `{argv, pid, started_at}` at spawn; `--attach` prints the live-arguments line from it; the seat check (`scripts/check-regime-boundary.sh` `seat_pane_state`, `scripts/check-agent-runtime.py`) compares the live process against the record; `dispatch.sh` refuses a line to a seat whose live process differs (the `C-60:1` row of the tools a04 task, per `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md` line 81); the worker-side hcom hook: a seat cannot end its turn on an S1 revise without a `re-plan:` line (today `scripts/agent-stop-gate.sh`); `herdr-agents --remove-worker` and `--stale` against hcom's member list. Sources: PR #383 (unmerged, `seat-args.sh` kept on its branch), the seat-liveness a02 and seat-launch-args follow-up owner tasks (their records `dotfiles-T128-seat-liveness-followup-a01.md` and `dotfiles-T128-seat-launch-args-a01.md` hold no `## Owned by` rows today: VERIFY with the plan's author which rows are meant), 111 of `test_herdr_agents.py`'s 193 tests touch seating.

## Validation (outputs pasted in validation.md)

- `uv run python -m unittest tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py tests/unit/test_hcom_dispatch.py -v`, then `make unit-test` once on the final head (`test_agmsg_orchestration_docs.py` and `test_check_regime_boundary.py` reference these scripts by name and must stay green).
- `shellcheck` on `dispatch.sh`, `bus-read.sh`, `bus-history.sh`, `regime-counters.sh` and `executable_hcom-dispatch`; `make format`; `make render-check` (nothing generated may drift); `git status --porcelain` showing only this task's files.
- Caps, from `git diff --numstat origin/main...HEAD`: at most 260 changed lines outside `tests/` and `.orchestration/`, at most 700 under `tests/`.

## Forbidden

Any hcom flag, table or column not pasted under item 0; writing to hcom's store or setting `HCOM_DIR` inside a script; reading the agmsg store anywhere in the five scripts after this change (`/usr/bin/grep -c 'agmsg' <the five files>` is pasted and explained line by line in validation.md; the remaining hits must be the argument-form sentence and the PR E note); editing `herdr-agents`, `agent-stop-gate.sh`, `replay.sh`, the SKILL, the rules, `.chezmoiremove` or any file outside `allowed_files`; sending to a live bus from a test; retrying an unconfirmed send as a second send (one send per route, agmsg-dispatch line 75).

## Completion

One PR from a fresh branch off `origin/main` now. PR #390 (`dotfiles-T129-audit-inherit-replan-json-a01`, accepted, in the merge queue) edits `scripts/regime-counters.sh`, `tests/unit/test_regime_counters.py` and `tests/unit/test_orchestrator_tools.py` too; its worker is finished, so the edits are not concurrent (the D-D-overlap-394 reading), and this branch rebases onto `origin/main` after #390 merges and before its RESULT; a textual conflict is a `PONG status=blocked`, never a hand merge. Under the morning merge-gate policy the worker opens its own draft PR with the plain create form (explicit `--base main` and `--head`, `--title`, `--body-file`, `--draft`; one command, no shell metacharacters) and marks it ready with the plain ready form once CI is green. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-hcom-dispatch-bus-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-hcom-dispatch-bus-a01/task.md>` in the RESULT. Until this PR merges, its own rounds run through the agmsg chain (plan 023 "Order").

## RESULT contents

Head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=`, the evidence paths; item 0's facts (hcom version, the send form, the history route chosen and why, the schema or command it rests on, the read-marker column); the `grep -c agmsg` table of the five files; the list of a02 items with anything item 0 changed about them (the member list command, the hook surface for the worker-side gate).

## Amendments

1. (2026-10-22, `previous_sha256` above; resumes this text from its 2026-10-18 parking under plan 024, D-024-79) Re-anchored to main d06d94fd: the six premises hold with the outputs in the Checks block (generated by `checks-paste.sh`, every line one command with its exit status); the line anchors of items 3, 5 and 6 are `dispatch.sh` 245 and 350, history windows 46 to 59 and 347, `bus-read.sh` 49, and `regime-counters.sh` `read_history()` now at line 94 (was 88) with the header rule still at line 11. `after:` is satisfied by the lineage's a02, PR #423 merged as b22a5580 (PR #390 closed as superseded), so the "Wave conflicts" and "Completion" paragraphs that name #390 read as done. hcom stays at the manifest pin 0.7.30 (`~/.local/bin/hcom`; 0.7.31 is upstream and not adopted here); omp is installed at `~/.local/bin/omp`. Continue on PR #407's branch `tools/hcom-dispatch-bus-a01` after merging `origin/main` into it (its two item-0 files stay), or start a fresh branch and close #407 in the RESULT; the worker is the Claude seat a009 (worker-c), which sends RESULT and PONG with `agmsg-dispatch` (macOS, socket allowlisted) or `send.sh … --body-file`. Amendments to this text travel as `AGMSG-ACCEPTANCE status=revise` lines carrying `task_sha256` (C-119). Every `env -i` contract of this task, in the Checks block and in the worker's own commands, carries an absolute private `UV_CACHE_DIR` and refuses when it is absent (design 5.14 item 9). Nothing else changes.

## Checks (pasted by the orchestrator before each send)

```text
observed 2026-10-22T04:39Z by the orchestrator (sandboxed Bash); every executable below is absolute and every command runs under the enumerated environment printed with it
canonical main: clone (gh-free): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home /Library/Developer/CommandLineTools/usr/bin/git -c http.proxyAuthMethod=basic -c credential.http://localhost:49680.helper= clone -q --bare https://github.com/mryfmo/dotfiles.git <private>/dotfiles.git ` -> `` (exit 0)
canonical main: ref: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git rev-parse refs/heads/main ` -> `d06d94fd8eedcd0770c1c80c2b1596ec36109ef8` (exit 0)
canonical main: remote: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --get remote.origin.url ` -> `https://github.com/mryfmo/dotfiles.git` (exit 0)
canonical main: config origins: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --list --show-origin ` -> `file:<private>/dotfiles.git/config	core.repositoryformatversion=0 file:<private>/dotfiles.git/config	core.filemode=true file:<private>/dotfiles.git/config	core.bare=true file:<private>/dotfiles.git/config	core.ignorecase=true file:<private>/dotfiles.git/config	core.precomposeunicode=true file:<private>/dotfiles.git/config	remote.origin.url=https://github.com/mryfmo/dotfiles.git` (exit 0)
design digest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git show refs/heads/main:.orchestration/plans/024-design-quality.md | /usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 ` -> `a027b0210981ca4c4d4e832dc849af6a03cd71c408801f74d098c3b778dd9dbe`
hcom version: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 ~/.local/bin/hcom --version ` -> `→ hcom v0.7.31 available — run `hcom update` hcom 0.7.30` (exit 0)
omp path: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -la ~/.local/bin/omp ` -> `lrwxr-xr-x@ 1 <user>  staff  57 Oct 18 08:01 ~/.local/bin/omp -> ../lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js` (exit 0)
premise 1: agmsg-dispatch in dispatch.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c agmsg-dispatch ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `4` (exit 0)
premise 2a: history.sh in bus-read.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `2` (exit 0)
premise 2b: storage.sh in regime-counters.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c storage.sh ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `1` (exit 0)
premise 3: bus reads in replay.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c -e history.sh -e storage.sh -e sqlite3 ~/Workspace/dotfiles/scripts/orchestrator/replay.sh ` -> `0` (exit 1)
premise 4: hcom-dispatch absent: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch ` -> `ls: ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch: No such file or directory` (exit 1)
premise 5: revises rule: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n revises = AGMSG-RESULTs - 1 ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `11:#   1; revises = AGMSG-RESULTs - 1, whatever their status; questions = PONGs of` (exit 0)
anchor: dispatch.sh call sites: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n agmsg-dispatch "${team}" ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `245:[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" 350:agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?` (exit 0)
anchor: bus-read.sh history read: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `5:#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team> 49:history="$("${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}")" || {` (exit 0)
anchor: regime-counters.sh read_history: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n read_history() ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `94:read_history() {` (exit 0)
after: audit-inherit-replan-json lineage on main: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /Library/Developer/CommandLineTools/usr/bin/git -C ~/Workspace/dotfiles log -1 --format=%h%x20%s b22a5580 ` -> `b22a5580 fix(orchestrator): the F1 lineage's owned rows: the gate's re-plan schema in the counters, no inherited unusable audit, one count per audit id (T129 audit-inherit replan-json followup a02) (#423)` (exit 0)
```
