---
reviewed_at: 2026-10-12T10:44:49Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
task: dotfiles-T128-plan-007-review-a01
round: 1
files:
  - .orchestration/plans/007-mistakes-into-mechanisms.md@2d9a76be7c64ee3e13f278822a4789d235f7404a7433bfe61a0d79bb92e3dd60
  - .orchestration/plans/008-resume-a7-pr323.md@49c768f72c4a0fc38470c103fef24140c5303d9750d81174048f0839c92af49e
  - .orchestration/learning/index.yaml@290bf6120f2deaef90465cd315f5bf8697509a58dea9adc25a09f3e95f10d9e4
verdict: revise
---

# Plan review: plans 007 and 008, one independent round

Read against plan 006 (Phase 0 rules, S1 to S4, the A6 and B0 rows), plans/README.md, the design's INV-2, INV-6, INV-7, INV-12, the learning index with the M and C records, the SKILL threat-table and counters bullets on main (lines 71 and 72), and the scripts and settings the figures cite. Re-run from this seat: the C1 to C6 checker over the 13 Phase A task files (10 FAIL: process-rules a01 to a06, regime-counters a01 and a02, ci-skip a01 and a02; a07 and worker-stop-and-watch a01 and a02 OK), the interpreter figures (SQLite 3.54.0, Python 3.15.0, no enable_load_extension), require-crit-review.py line 26 and FAILURE_REASON_MIN_CHARS 20, the managed settings template (defaultMode auto, ask []), regime-counters.sh line 114 (the first RESULT is the baseline). Not re-run: the badge counts, the Bot latency and the CI median (gh is unreachable from this seat); the official sentences were not re-fetched.

## Findings

- P2 0.9 .orchestration/plans/007-mistakes-into-mechanisms.md:92 — T704 puts the ten failing task files under tests/fixtures/lessons/; they total 1027 lines (wc -l), over INV-2's 1000 added lines under tests/ before the pre-fix a05 record and the two scripts' unit tests are counted, the very cap the regime-counters a02 reset was about; the checker reads front matter only (480 lines for the ten), so the fixtures carry the front matter alone, or T704 splits.
- P2 0.9 .orchestration/plans/007-mistakes-into-mechanisms.md:67 — C-1 and C-8 (line 74) name "A7 step 15 (PR #323)" and "(A7)" as the mechanism, and the coverage row of line 118 names T708; after plan 008 decision 2 PR #323 is parked and index.yaml names T712 for both, so S5 holds on the index but not on the plan's own tables; the tables name T712.
- P3 0.9 .orchestration/plans/007-mistakes-into-mechanisms.md:82 — T700's metric and the acceptance line 138 say 10 M and 11 C; index.yaml and the directories hold 11 M (M-20261012-10, 10:42Z) and 12 C (C-12), and the tables of lines 52 to 76 omit M-9, M-10, M-20261011-1 and C-12; the counts are corrected and one line says the index is the ledger and the tables are the eight of 04:32Z, or the rows are added.
- P3 0.8 .orchestration/plans/007-mistakes-into-mechanisms.md:38 — the three-repeat procedure names "contextdb memory search <class slug>", which is not a command on this machine; the command that runs is "uv run --no-project .claude/hooks/contextdb_cli.py memory search <slug>" (verified, it returns matches), and stop condition 4 needs the name as it runs.
- P3 0.8 .orchestration/plans/008-resume-a7-pr323.md:5 — the drift check describes the state before either decision (OPEN at 3a54d340, review seat idle, no amendment sent) while Status line 9 says both decisions executed and the PR is parked at dc7edcc0; every line of the check has moved, so the check is dated "at planning time, 04:4xZ" with the post-decision-2 state added, or dropped since the plan is DONE.
- P3 0.7 .orchestration/plans/007-mistakes-into-mechanisms.md:86 — T701's row unit (each allowed_files entry plus a fixed list of orchestrator effects) is compatible with INV-12, whose in-process forgery residual lives in the acceptance record, and with the SKILL bullet on main (line 71) only if one clause says the declared test module's row carries the PR-side in-process effects and metadata separators the bullet lists, which are not allowed_files entries.
- P3 0.7 .orchestration/plans/007-mistakes-into-mechanisms.md:106 — T711 changes the Stop gate only; INV-6's revises still count every RESULT for a task_id minus one, so review tasks reach S2 by anchor RESULTs alone (ci-skip-redesign-a01 has 4, regime-counters-redesign-a01 has 5) and are silenced by pr=none records (the regime-counters a02 row); one clause says the counter side stays INV-6's and the pr=none record is its release, so T711 is not read as removing the count.

## Stop condition

1. Holds on the records: M-1 to M-8 each once with at least one C; every C names a mechanism that exists (fixtures, the counters bullet) or a plan row with an owner (T701 to T713, 006 V1); finding 2 is about the plan's tables, not the index.
2. Holds with finding 6: no task contradicts plan 006's B0, V1, V2 or V3a rows or INV-2, INV-6, INV-7, INV-12; T701 rides on B0 as the dependency rationale says.
3. Holds for every figure re-run here (the checker replay, the interpreter, the gate grammar line, the settings, the counters baseline); the GitHub figures were not re-run.
4. Holds with finding 4: the search names a command that does not exist by that name; S7's report form is plan 008's section and is executable as written.
5. Holds: the plan references INV-6, S1 to S4, the counters bullet, the permission order and merge_group by citation; Phase 0's "classes at disposition time" adds timing to the counters bullet without restating its sources.

Plan verdict: revise — edits: (1) T704 fixtures front matter only or split; (2) C-1, C-8 and coverage row 1 name T712; (3) the M and C counts and the index-is-the-ledger line; (4) the search command as it runs; (5) plan 008's drift check dated or dropped; (6) one clause in T701 for in-process effects; (7) one clause in T711 for INV-6's counter side.
