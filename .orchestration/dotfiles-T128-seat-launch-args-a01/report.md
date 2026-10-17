---
task_id: dotfiles-T128-seat-launch-args-a01
status: final
revise_round: 6
result_round: 3
---

The checker now requests full-width process commands with -axww -o pid=,command=. Required managed flags and the Claude session marker beyond the display-width cutoff remain available for comparison, preventing false unlaunched/differs results. This C50 ps-truncation correction changes exactly one production invocation. It preserves the absolute default probe, quoted test seam, headerless PID/command format, stderr suppression, exit capture, selection, comparison and diagnostic output. It changes no live seat runtime, model, profile or launch flags.

PR https://github.com/mryfmo/dotfiles/pull/383, branch feat/seat-launch-args-check; acceptance round6/RESULTround3 starts at8b210af3b9f151cef63776f63a74904115cef8b9, GitHub baseaf4f1e997f78119d5994d7d7b1966894d62bbc6a. Full task copy remains byte-identical SHA256 148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f. Only seat-args.sh, its existing unit-test method and task records change in this incremental revision. Both boundary source and boundary test remain byte-identical to8b210af3.

Requested accounting and named regression:

- local:8b210af:1: fixed by this publishing commit, named in RESULTround3. tests/unit/test_seat_args.py::SeatArgsTest::test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one adds one long-command subcase. Its stub records argv and cuts fixture command lines to64 unless ww is present; the caller PID marker stays visible. Before the fix only this new subcase fails, exit3 instead of0. With full width it selects process200, args=ok, and records exactly -axww -o pid=,command=. Ordinary stub is restored before existing visibility/cwd/failure controls.
- audit:3345c4d:1: earlier fixed:8b210af3b9f151cef63776f63a74904115cef8b9, equals-form pairs and every-occurrence conflict latching retained.
- audit:3345c4d:2 and4301301556: earlier re-fixed:8b210af3b9f151cef63776f63a74904115cef8b9 under D-S1-383-A's parent-visibility specification only. This is not a complete-host-visibility disposition.
- 4301342120: fixed:1086570f8a8b20271ba7d7417701e1dff922e149, deferred cwd failures/continue-to-match retained with common parent prerequisite.
- 4301264676: fixed:bfae75c14f52ff1b8083a69179bd90e91aa99458, generator-valid underscore profile grammar retained.
- 4301378546 and4301378550: fixed:7b776a30a6a5b6c0ed9e8a9284650c1c9a2373ea, conflict latching and fixed-marker diagnostic redaction retained.
- audit:3345c4d:3 and acceptance/counter dispositions stay orchestrator-owned. Worker neither edits main acceptance/feedback nor replies to/resolves threads.

All12 required seat/boundary methods pass in29.022s, including41 seat subcases. ShellCheck of both scripts, configured shfmt, Ruff format of both modules and scoped whitespace pass. Independent read-only security-profile Codex review found no issue, reran the named fixture test and ShellCheck, verified boundary files unchanged and final task/source hashes. Parent read the entire121-line focused transcript and all12 resolved JSON records before the passing worker review gate. Full outputs and review are preserved in validation.md.

Whole-PR caps againstaf4f1e99: new seat script150 lines plus boundary17 additions/1 deletion=168 changed source lines/200; seat test320 additions plus boundary66=386/1000. One production script belongs to the original task; this correction adds no script/dependency/workflow/config/interpreter/reader API. Both boundary files stay unchanged in this correction.

Limits remain explicit: parent visibility is the approved proxy, not proof that every host worker is visible. Parent-visible/worker-hidden output can still produce unlaunched. Failed/empty/parent-hidden probes still return unknown-probe4 with fixed stderr. Flattened ps text cannot recover exact argv boundaries; prompt-like flag tokens can affect classification. Wider capture brings more command text into comparisons but creates no raw argv output sink; diagnostics still expose only expected managed names and fixed states. This change does not claim immunity to every platform argument-reporting limit.

This committed phase binds local validation/review to these tested source hashes:

- scripts/orchestrator/seat-args.sh: 3ad4242874eeeb1edfe06fed8c179273ab609c9c1f121316f9432ff80150fdbb
- scripts/check-regime-boundary.sh: eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423
- tests/unit/test_seat_args.py: 98b0580f2c8662e22d71b6efa2be6e36ff39801bc93271b5ad6a82188beaaef1
- tests/unit/test_check_regime_boundary.py: b1feb3229e4345a8c62d9ba6496400166a8d060e9bb462365661cd98b673a08a

task.md/report.md/validation.md/sandbox.md/learning.md/autoskill.md/revise.yaml/seat-args-worker-crit.json/seat-args-worker-review-receipt.md are committed before RESULT. Worklogs and duplicate observer logs stay uncommitted. Previous8b210af3 CI is historical context only. Final publishing head, its fresh CI watcher exit and Bot re-review are observed after push in RESULTround3 and round6-ps-width/ raw files; no self-referential head or future check is falsely claimed here.

No local Bats, real ps/lsof inventory, real prompts/secrets, main write, escalation, re-seat/runtime change, Plan Mode, Crit browser/server/human request, graph update, AutoSkill or memory promotion. Graph was queried, found stale and targeted rg used; no graph hook fired. Crit data is unavailable; independent review/receipt is local process evidence, not authentication or final task audit. PR379 e234 handoff is complete/pending integration; PR375 evidence-only follows this handoff. Orchestrator owns final sweep/audit/acceptance/dispositions/gate/merge.

cost: n/a
