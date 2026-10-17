---
task_id: dotfiles-T128-seat-launch-args-a01
status: final_local_validation_complete
c50_rounds: 4
branch: feat/seat-launch-args-check
base: b167fe0a76a2e77d262f9f556c69ba6b9f118bbe
pr: 383
---

The boundary check now reports linked seated workers whose visible launch arguments differ from the identity's rendered profile, including resumed and unlaunched seats. New executable scripts/orchestrator/seat-args.sh parses an exact profile key as literal text, never sources/evals it, accepts generator-valid underscore profile names, selects Claude by an exact -n pair for any grouped team and Codex/native npm wrapper by cwd, and chooses the lowest visible matching PID. The boundary groups each name once per type across its team rows. Existing worker/pane lines remain; the main orchestrator seat is not probed. This changes boundary diagnostics, not the live worker's model, flags or runtime.

Missing tools or failed/empty ps snapshots skip4 with unknown-probe. A failed/empty per-pid cwd lookup saves the first diagnostic and scanning continues: a successfully inspected cwd match decides ok0/differs2; no match plus unknown candidates skips4; inspected nonmatches alone are unlaunched3. Every managed flag must occur and every occurrence must carry its expected value. Conflicting duplicates in either order differ; identical duplicates remain accepted. found displays only trusted expected flag names and fixed ok/differs/missing markers once per managed name, in first observed name order; missing names append in expected order. No observed argv value, positional prompt or unmanaged flag is copied to stdout/stderr. expected retains the trusted local profile pairs. Probe diagnostics contain fixed names/status only.

Final local validation: both requested modules pass12 tests15.667s, with34 seat subcases. Initial implementation and each authorized C50 had failing regression checks before its fix; final marker/name ordering also had a failing check. ShellCheck, configured shfmt, Ruff format and source/test whitespace pass. Source changed161<=200; test additions322<=1000. Two new methods remain SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one and RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation. One new production script, no dependency/workflow/configuration change. The earlier source/cap checkpoints in validation.md are historical; these are the final local counts.

Independent reviews approved the initial four paths and each C50 delta. The final redaction design and implementation were reviewed in a new context on the manifest security tier, gpt-6-astra/high; no model/profile switch in this worker session. The final reviewer found no new issue, ran the seat test and14 additional synthetic fixture cases, and matched the tested source hashes. Full exact review transcripts are pasted in validation.md; the corrected plan report explicitly acknowledges its concurrent partial test edits and does not claim a clean baseline tree. The parent read the full records and resolved JSON evidence. The addressed receipt and worker gate cover current source bytes. This is process evidence, not reviewer authentication or task-level integration audit.

Known Bot thread dispositions proposed by the worker; the orchestrator replies/resolves:

- 4301264676, profile-name-grammar occurrence1: fixed:bfae75c14f52ff1b8083a69179bd90e91aa99458.
- 4301301556, process-visibility occurrence1: fixed:a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8 for the failed/empty-probe check; its per-candidate behavior is amended by the next fix.
- 4301342120, process-visibility occurrence2: fixed:1086570f8a8b20271ba7d7417701e1dff922e149, deferred diagnostic and continued cwd scan.
- 4301378546, duplicate-managed-flags occurrence1: fixed by the publishing commit containing this final C50; exact SHA is in RESULT after creation.
- 4301378550, argv-diagnostic-disclosure occurrence1: fixed by the same publishing commit, under the explicit04:35:12Z fixed-marker refinement.

All five known Bot review bodies/inline findings were read; no P0/P1. ACCEPTANCE04:34:17Z makes this the last pre-RESULT C50: after the next push, CI and Bot review, any further P2 is proposed advisory for the orchestrator's audit to judge. Task copy SHA256148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f is byte-identical. All nine canonical records (task, report, validation, sandbox, learning, AutoSkill, review JSON, receipt, revise.yaml) are committed before RESULT. Plan/todo and raw duplicate logs remain untracked; no untracked final-report replacement.

External results are phase-bound: the previously published head1086570f8a8b20271ba7d7417701e1dff922e149 has13 passing checks and its watcher exited0; review5556193099 on that head raised the last two P2s above. Those outputs are pasted in validation.md. This report binds current local validation to the four source hashes there. The new publishing SHA and its observed post-push CI/Bot results are supplied in RESULT and fetched again by the orchestrator; no future CI result is invented in this committed record. Shared GitHub base was58303c37a2ac7854ba7f8d4032b5ee2b9c28776e; fixed worker start base remainsb167fe0a. No worker rebase/merge.

Limits: flattened ps text cannot recover true argv boundaries, so prompt text resembling managed flags can affect classification even though observed values are redacted. A nonempty sandbox PID namespace that hides host workers cannot be distinguished from genuine absence. These are explicitly reported, with no claim of host visibility or exact live-process behavior. Tests use only temporary HOME/ps/lsof/identities fixtures and synthetic markers; no real prompts/secrets/processes, re-seat, runtime/profile generation, main-checkout write, permission escalation, local Bats, live pane E2E, Crit server/Plan Mode, AutoSkill, graph update or memory promotion. Graph was queried and found stale, so targeted rg was used; no update hook fired. The orchestrator owns final sweep/audit/dispositions/gate/merge. After hand-off the authorized queue is PR379 physical cwd/evidence revision, then PR382 ASCII word-tokenizer re-plan revision.

cost: n/a
