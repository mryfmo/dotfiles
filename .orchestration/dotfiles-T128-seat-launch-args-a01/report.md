---
task_id: dotfiles-T128-seat-launch-args-a01
status: final
revise_round: 5
result_round: 2
---

PR https://github.com/mryfmo/dotfiles/pull/383, branch feat/seat-launch-args-check. This authorized C-59 re-plan round5 starts at3345c4d347dfe31ee1cbd59c89fee1e8f806f3c8 after the orchestrator's base update; current GitHub baseaf4f1e997f78119d5994d7d7b1966894d62bbc6a. Original worker start baseb167fe0a and earlier no-merge statements are historical. Operator decision D-S1-383-A and the process-visibility re-plan explicitly authorize the parent-PID visibility proxy plus the separate equals-form managed-flag fix.

The checker now requires its own parent PID in the PID column of a successful, nonempty ps snapshot before selecting any seat. If absent, whether the seat is listed or absent, stdout is args=unknown-probe, exit4, and stderr is exactly `seat-args: ps hides the caller's own process`. With the parent present, the existing missing-seat result is unlaunched3 and a matching seat is ok0. Failed/empty probes and the deferred per-candidate cwd behavior remain unchanged. This changes boundary diagnostics, never the live worker's runtime/model/flags.

Managed-flag comparison now reads --flag=value as the same name/value pair as --flag value. Every occurrence must still agree: a later matching occurrence cannot clear an earlier conflict, and identical duplicates pass. --effort=high after expected --effort xhigh differs; --effort=xhigh without a separated effort pair passes. Found diagnostics retain only trusted expected managed names and fixed ok/differs/missing markers; no observed argv value is emitted.

Limits are part of this result: parent visibility is the operator's specified proxy, not proof of a complete host inventory. A ps list containing the parent but hiding a worker can still produce unlaunched. This revision closes the parent-absent scenarios specified by the re-plan; it does not claim to eliminate every hidden-worker namespace scenario. The source contains the explicit shortcut comment. Flattened ps text still cannot recover true argv boundaries; prompt text resembling flags can affect classification even though diagnostic values remain redacted. Independent approval and proposed fixed dispositions are bounded to the authorized proxy, not a global visibility guarantee. Final disposition authority stays with the orchestrator.

Requested finding accounting (publishing SHA is named in RESULTround2):
- audit:3345c4d:1: fixed by this publishing commit, equals-form comparison and the two regression subcases.
- audit:3345c4d:2 and4301301556: re-fixed by this publishing commit under D-S1-383-A's parent-visibility specification. The previous a428eb5f fix covered only failed/empty snapshots; its broader root-cause fixed claim was rejected by the audit. The proxy limit above remains explicit and must not be dispositioned as complete host visibility.
- 4301342120: prior deferred cwd-scan fix1086570f8a8b20271ba7d7417701e1dff922e149 remains; this publishing revision adds the common parent-visibility prerequisite to that selection path.
- 4301264676 remains fixed:bfae75c14f52ff1b8083a69179bd90e91aa99458.
- 4301378546 and4301378550 remain fixed:7b776a30a6a5b6c0ed9e8a9284650c1c9a2373ea; conflict latching and redacted diagnostics are preserved.
- audit:3345c4d:3 is orchestrator-owned counter-evidence process handling, with the acceptance record's explicit disposition. The worker does not edit main acceptance/feedback records or reply to/resolve threads.

Only scripts/orchestrator/seat-args.sh and the two allowlisted test modules change in this incremental revision, plus this task's records. Production check-regime-boundary.sh is byte-identical to3345c4d. The existing single SeatArgsTest method adds exactly six subcases: four parent visibility combinations and two equals-effort forms. All14 original cases and existing loop/with blocks stay unchanged (AST equality check); no new method. Existing boundary cases/assertions/invocation remain unchanged; its temporary seat-args entry is an exec shim exporting PPID before exec of the byte-identical copied checker, so the ps stub can print the right parent even through an intermediate shell. Unit ps stub uses the known Python caller PID. No host ps/lsof inventory is read.

Regression and validation: the named seat test failed four subcases before source edits (two equals and two hidden-parent cases). First full-suite run then caught only the boundary resumed fixture, which had incorrectly used the outer boundary PID. Correcting the test-only shim yielded all12 required tests passing18.008s,40 seat subcases. A quote-only Ruff format fix was applied; final ShellCheck of both production scripts, configured shfmt, Ruff format and source/test whitespace pass. Fresh independent security-tier review (manifest gpt-6-astra/high, new context) found no issue, reran the named test and ShellCheck, and passed seven extra synthetic checks including conflict orders, empty/additional equals, private-value redaction and PID prefix rejection. Complete review and exact outputs are in validation.md; parent read them and all resolved JSON records before the worker gate.

Full PR scope against current GitHub base: new seat script150 lines plus boundary17 additions/1 deletion =168 changed source lines<=200; seat test305 additions plus boundary test66 additions =371<=1000. One new production script remains from the initial task; this revision adds no production script, dependency, workflow/config, interpreter, reader API, re-seat or profile setting. Prior scope161/322 and34 subcases are historical.

This final record binds to the tested hashes below and the publishing commit containing it. All13 CI checks at previous_head3345c4d passed; they do not validate this revision. The new publishing head, final-head CI watcher exit and Bot re-review are observed after push and named in RESULTround2, with raw logs in round6-visibility/. No head-changing commit is made just to embed its own future hash/external results. All nine canonical task/report/validation/sandbox/learning/autoskill/reviewJSON/receipt/revise records are committed before RESULT; worklogs and raw duplicate logs stay uncommitted.

Source SHA-256:
- scripts/orchestrator/seat-args.sh: 7b1a5040f18f4564f3bd861c498e1f7324bdb50689b57c724acabc8c53cef289
- scripts/check-regime-boundary.sh: eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423
- tests/unit/test_seat_args.py: 62b9bc0ffe97021587834486b347fee97cbd605da786c85961916f1cc2ef5954
- tests/unit/test_check_regime_boundary.py: b1feb3229e4345a8c62d9ba6496400166a8d060e9bb462365661cd98b673a08a

Task copy SHA256148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f remains byte-identical. Crit has no review file or running daemon; the explicit AGENTS.md independent-review fallback is process evidence, not reviewer authentication or the final integration audit. No Crit browser/server or human review request. No local Bats, direct live ps/lsof, real prompt/secret input, main-checkout write, permission escalation, runtime/re-seat change, Plan Mode, graph update, AutoSkill or durable memory promotion. Graph was queried and found stale; targeted rg used, no hook fired. Earlier PR375/379/382 branches and evidence remain preserved. Orchestrator owns final sweep/audit/acceptance/dispositions/gate/merge.

cost: n/a
