---
task_id: dotfiles-T129-integration-seat-result-gate-cap-a01
seat: claude-standard-dot-a006
branch: tools/integration-seat-result-gate-cap
base: 59db77bb
code_commits: [6c994f2c, e260d89b, 522cc4b8, ec4a300d]
fix_commits: [ff9bb7c1, 1c29ec0d]
task_sha256: 4e00bf122f578a9dbbde8ac36feb025d68cb828009a2e9f009606ad760879081
---

# Report: dotfiles-T129-integration-seat-result-gate-cap-a01

- Seat: `claude-standard-dot-a006` in `.claude/worktrees/worker-f`, on a fresh branch `tools/integration-seat-result-gate-cap` from `origin/main` `ce032e14`, rebased before any push onto `59db77bb` (#386). The PR #390 branch stays in the worktree for its integration.
- Task file: amendment 2, sha256 `4e00bf12…`, copied byte-identical; the checker passes; the four premises replay equal (validation §1, §2). One question, the caps (PONG 13:13:41Z), answered by amendment 2 (D-cap-F4: the cap is 260).

## What landed

| File | What it does |
|---|---|
| `home/dot_agents/agent-config.yaml` (+3) | `worker_cap: 4` beside `worker_kind`, with its comment. |
| `home/dot_local/bin/common/executable_herdr-agents` (+18) | `--add-worker` reads `worker_cap` from the deployed `~/.agents/agent-config.yaml` (sed, a top-level integer), counts the repository's `.claude/worktrees/` worktrees that hold an agmsg identity of either type (`identities.sh <worktree> claude-code` and `codex`, as the Stop checklist counts them) and refuses a new seat that would exceed it: `herdr-agents: worker_cap is <n> and <m> worker seats are registered; remove one with --remove-worker first.`, exit 2, before any worktree, identity, workspace or spawn. Re-seating a seated worktree adds none. No manifest, or no key: one stderr line `no worker_cap in <path>; no cap enforced.` and the seat goes on. |
| `scripts/orchestrator/integrate-seat.sh` (new, 123) | Item 1, run by the integration seat in its own worktree at `origin/main` with that worktree's scripts: update-branch when the base moved (the merged head polled), the CI wait (restarted on `no checks reported`), the Bot wait on the diff head (its review, or a receipt comment naming it; 15 minutes at most; the one optional step), the sweep, the local review in a private review worktree under `$TMPDIR` (removed on exit) with `local-advisory.sh` for its P2/P3 under `--owner`, the dispositions from the task's latest RESULT `threads=` (`fixed:<sha>` kept; a P2/P3 otherwise `not-applicable:advisory <P> owned by <owner>; evidence=…`; a P0/P1 without `fixed:` stops the chain), `resolve-threads.sh`, the sweep again with `fill_sweep.py`, the crit-data receipt (its body the diff's `--shortstat`) and the record block by `acceptance-front-matter.py` on the main checkout's record, copied in first. Each step's command, status and output goes to `.orchestration/validation/<task>-integration-<sha7>.md`; it sends `AGMSG-RESULT v1 task_id=<task> kind=integration status=ready_for_audit head=<sha> record=<file>` with `agmsg-dispatch`, or `status=blocked step=<name> rc=<n>` at the first failing step. It has no audit, gate or merge command. |
| `scripts/orchestrator/result-precheck.sh` (new, 113) | Item 2. `run <task> <pr> <head>` writes `.orchestration/<task>/precheck-<sha7>.md` with checks (a) to (i), each `ok`, `missing` or (for (h) and (i)) `unavailable (<reason>)`, and exits 1 naming each `missing`; its last stdout line is `precheck=<sha256> <path>`. `verify <task> <RESULT line>` finds, in the tree of the line's `head=`, the receipt whose sha256 is its `precheck=`, refuses a code change after the receipt's own head and any `missing` check, and prints `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise reason=precheck:<…> next_action=run-result-precheck-and-resend`, exit 1; exit 0 otherwise. |
| SKILL, rule (text) | The two seat-count sentences say "at most `worker_cap` workers (4 in the manifest today)"; the delegation sentence names the integration seat and `integrate-seat.sh`; the exemption bullet and the rule's Delegation bullet keep the acceptance judgment with the audit and its dispositions and the final gate and merge with the orchestrator; the rule's Acceptance bullet names the integration seat for the sweep, the local review and the thread resolution; step 10 points sub-steps 1 and 3 at `integrate-seat.sh`; step 15's thread sentence names the integration seat as the resolver. |

Both new scripts export `CLICOLOR_FORCE=0 FORCE_COLOR=0 NO_COLOR=1` after `set -euo pipefail` (amendment 1); `|| true` appears only in the Bot wait, in `line()`'s no-match grep, in the cleanup trap and in verify's fetch.

## The tests, by closed row

| Closed row | Test |
|---|---|
| manifest, herdr-agents | `test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap`: without a manifest the add goes on with the no-cap line; with `worker_cap: 4` and four seat worktrees (real `git worktree add`, a path-keyed `identities.sh` stub), the fifth add is refused with the line, no worktree, join, workspace or spawn; once one seat's identity is gone the fifth add passes the cap and creates its workspace. |
| SKILL, rule | `test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat`: the manifest's value in both seat-count sentences with `worker_cap`, no "three workers" left, the exemption and Delegation bullets with the integration seat and the three orchestrator steps and without "final integration", the Acceptance bullet, the step-15 sentence. |
| integrate-seat.sh | `test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges`: the exact script order, the RESULT line, the dispositions TSV, the record's steps, the record block on the copied main record, the receipt; no merge call and no audit, gate or merge command in the script text; a failing CI, a failing `resolve-threads.sh` and an unfixed P1 each send `status=blocked step=<name>` and stop before the record; malformed arguments and a missing TASK refuse with exit 2 and run nothing. `test_integrate_seat_reads_plain_gh_output_under_clicolor_force` (amendment 1): with `CLICOLOR_FORCE=1` inherited and a stub gh that colours its output then, the comments JSON the sweep fill reads parses and the RESULT is ready_for_audit. |
| result-precheck.sh, its inputs | `test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt`: all ok (seven ok, (h) and (i) unavailable); verify accepts the receipt committed after the head and refuses a wrong sha256 (`receipt`), a code change after the receipt (`code-after-receipt`) and a receipt naming a missing check; each of (a), (c), (d), (e), (e) with another head on GitHub, (f), (g), (h) broken alone is the one `missing`; (b) with a file outside `allowed_files`; malformed task id, PR number, head and RESULT line exit 2. |

Red: the two herdr tests fail on `origin/main`'s four files, the integration-seat module without the two scripts (validation §4), and the fix round's cases on `194e0bde`'s scripts (§10). Mutants: 17, each caught by its test, then a passing baseline (§6, §10). The `CLICOLOR_FORCE` export of `result-precheck.sh` has no test of its own; the amendment's one test is `integrate-seat.sh`'s.

## CI and the Bot

- **The first head, `194e0bde`:** CI's `test` jobs failed at ShellCheck on every runner (SC2015, `A && B || C`, at `integrate-seat.sh:25`); this host's ShellCheck 0.11.0 did not report it. The Bot's review `5558018807` (13:44:47Z, after `gh pr ready` at 13:42:29Z) left three P1, all fixed in the one fix round, `ff9bb7c1` (validation §10):
  - `4302868172:P1:fixed:ff9bb7c1` (`result-precheck.sh:32`): `verify` took a matching receipt with no status lines; it now requires one status line for each of (a) to (i), else `incomplete-receipt`.
  - `4302868177:P1:fixed:ff9bb7c1` (`integrate-seat.sh:117`): the main record was copied in after `local-advisory.sh` had added its rows, overwriting them; the copy now comes before the local review.
  - `4302868180:P1:fixed:ff9bb7c1` (`integrate-seat.sh:97`): review-body findings, `review-<id>` in a RESULT's thread list (the Message Contract's `open:review-<id>` form), are written as the sweep's `pullrequestreview-<id>` key.
  - ShellCheck: no `A && B || C` is left outside `[[ ]]` and loop bodies in either script.
- `1c29ec0d` shortens both headers so the code stays under the 260 cap (257).
- The re-review on `@codex review`, CI on the final head and the precheck receipt are in the RESULT.

## Readings, declared

- **`worker_cap` is read by sed from the deployed `~/.agents/agent-config.yaml`.** `herdr-agents` has no YAML reader (its manifest values come from the generated `model-profiles.env`), and the generator is outside `allowed_files`. A missing file or key means no cap and one stderr line (amendment 2 confirms). The first version exited 1 silently without the file (`pipefail` on the failed `sed`); 34 existing add-worker tests, which run without a manifest, showed it, and `ec4a300d` fixed it.
- **The exemption list.** Item 3 lists what the orchestrator does directly; the integration exemption ("final integration, including merging…") is replaced by "the acceptance judgment with the audit and its dispositions, and the final gate and merge", and the control-plane, bookkeeping and machine-hygiene exemptions, which are not integration, stay.
- **Where `integrate-seat.sh` works.** It runs the seat worktree's own scripts (trusted, at `origin/main`) with that worktree as the repository, so the sweep, local review, receipt and integration file land in the seat's worktree, as a Codex seat's artifacts do, for the orchestrator to move. The record block is written onto a fresh copy of the main checkout's record, never the stale one at `origin/main`, and the orchestrator moves it back. The local review uses a private review worktree under `$TMPDIR`, never the orchestrator's canonical one. The seat's identity and team come from `whoami.sh`, the orchestrator is the sender of the task's latest AGMSG-TASK, its pane is that member's `team.sh` pane in `agmsg-dispatch`'s `<workspace>:<pane>` form, and the dispositions are the latest RESULT's `threads=`. gh needs the machine's credentials, so the seat runs it outside its sandbox.
- **The precheck's mechanical definitions.** (a) `task_sha256=` of the task's latest TASK line on the bus; (b) `allowed_files` read by sed as plain `  - ` items (the task-consistency check reads them with PyYAML before dispatch), each changed file matched as a glob; (c) `at most <n> changed lines` and `<m> added lines under` from `## Check`, excluding `tests/`, `.orchestration/` and the backticked paths after `excluding`; (d) each backticked span of `## Check` that starts with `uv`, `shellcheck`, `shfmt`, `make` or `git` is a substring of the validation file; (e) the PR's head is `<head>` and `gh pr checks --required` passes; (f) a Bot review of the head, a Bot receipt comment naming it, or `bot: none` with its sha7 in the report; (g) every Bot top-level thread of the PR in the report as the RESULT's token `<id>:<P>:<disposition>`, a P0/P1 with `fixed:<sha>` or `open:`; (h) the local review file of the head without a P0/P1, else `unavailable` when there is none (a Claude seat cannot run codex review); (i) `codex exec --sandbox read-only` when codex runs here, else `unavailable`. `verify` binds the receipt to its head: only `.orchestration/<task>/` may change between the receipt's `head:` and the RESULT's `head=`.
- **`shfmt -d`** is run with the repository's flags (`-i 4 -sr`, `make format`'s), since `.editorconfig` sets no `indent_style` and bare `shfmt -d` asks for tabs everywhere.
- **The test environment.** The Check's two modules ran outside the sandbox (its `mktemp` denial fails 31 add-worker tests inside it on `origin/main` too); there, one test fails, `test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude`, identically with `origin/main`'s script (validation §7).

## Not done, or outside scope

- The merge queue, a cap of about six, seating the integration seat, F3's amendment, `validate-agent-assets.py`, the audit and the ruleset are untouched (Out of scope).
- The project-map subagent was not run: `.project-map/` is outside `allowed_files`.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- CompactionDB: `memory add` in the worktree's own database, entry `253b4a23-f87d-4604-8049-e476ade55790` (validation §9).
- cost: n/a (the runtime exposes no session figures to the seat).
