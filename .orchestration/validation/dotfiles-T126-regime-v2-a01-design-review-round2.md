---
reviewed_at: 2026-10-10T10:46:00Z
reviewer: claude-review-dot-a004
profile: review
session: 26619e82-a3a8-46c0-a37f-8eef8ba593d0
design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md@83bdfc9a261ef6cb6bef0318ac03eeea871ca78c02309e031a1ec3e42f5b1b70
design_hash_kind: canonical sha256 of invariants, threat_model and trust_anchors (validator at PR #313 head 2d2ae688); whole-file sha256 7460dd67482f55bf197da87d2c7993545a582799bf22cdf375404af874300203
task: dotfiles-T126-design-review-a01
round: 2
previous: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review.md
---

# Design review round 2: T126 regime v2

Scope as tasked: each round-1 item checked as applied in the file as it stands (the 10:38Z write, then the quoting pass; the file reviewed is the one whose hashes are above), and the front matter run through PR #313's validator at its current head `2d2ae688`. Sources are those of round 1; two new local facts: `scripts/validate-task.py:40` (`INVARIANT_ID = re.compile(r"INV-[0-9]+")`) and the receipt checks at `validate-task.py:106` and `:308`.

## Validator output (verbatim, from the worker-d worktree at 2d2ae688)

```
$ uv run --no-project scripts/validate-task.py ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md --print-design-hash
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md: invariants: ids must look like INV-n: V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md: design_review.receipt: its `design:` does not end in the design's canonical hash 83bdfc9a261ef6cb6bef0318ac03eeea871ca78c02309e031a1ec3e42f5b1b70 (re-review the design after any change to its keys)
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md: design_review.receipt: it must carry one `Design verdict: accept` line, found ['revise']
83bdfc9a261ef6cb6bef0318ac03eeea871ca78c02309e031a1ec3e42f5b1b70
rc=1

$ uv run --no-project scripts/validate-task.py … --json  (relevant keys)
  "security": true,
  "tier": "design",
  "design_hash": "83bdfc9a261ef6cb6bef0318ac03eeea871ca78c02309e031a1ec3e42f5b1b70"
```

The front matter now parses (block sequences for `supersedes`/`amends`; V3 and V6 double-quoted), the tier derives as `design`, and the canonical hash exists. The second and third failures are the expected ones: `design_review.receipt` names the round-1 receipt, whose `design:` is a whole-file hash and whose verdict is `revise`; they clear when the receipt pointer names a receipt in this form with `Design verdict: accept`. The first failure is a finding (V1).

## Invariants

V1: rejected: the file still does not pass the rule it states. The validator accepts only `INV-n` invariant ids (`validate-task.py:40`), and this design uses `V1`–`V12`. This is not cosmetic: an implementing task's ids must match the same regex and be a subset of the design's (`validate-task.py:247` and the subset check), so under the current W1 every W2–W8 task file that names this design fails the validator. The design must choose, in the hashed keys: rename `V-n` to `INV-n` (and the body's references), or amend W1 so the id pattern is `[A-Z]+-[0-9]+` with the subset rule comparing full ids. Either way the canonical hash changes and a round-3 receipt follows. The `process_tiers.json` mechanism is applied as asked.

V2: accepted. Applied as proposed: RESULT carries receipt path, receipt sha256 and canonical hash; the gate compares all three; both receipt forms accepted until W3 migrates.

V3: accepted. Applied: validator at start, tests-before-implementation checked by commit order, the worker's own Stop hook warns, enforcement map updated. One note for W5: the commit-order check applies to tasks that carry invariants; a docs-tier task has none and no `tests/` commit, so the gate exempts tasks with an empty `invariants` map.

V4: accepted. Applied: `--bare` with an API key or managed hooks with W2 showing them harmless; the Bot condition is now "a review of that head exists"; `AGMSG-AUDIT v1 task_id= head= sha256=` under an audit identity before the gate reads the JSON; `herdr-agents --audit` delegation note. See V5 for the new `not_applicable` value.

V5: rejected: v2 adds `not_applicable` to the per-invariant map in V4, and V5 refuses only `violated`. An auditor can mark every invariant `not_applicable` and the lock never engages, which is a new gaming path of the same kind as category laundering. Fix in the sentence: the gate refuses `not_applicable` for any id listed in the task file's `invariants` (a task's own invariants are applicable by construction), and V12 names "an invariant map with not_applicable for a task invariant" among the gaming paths. The sha256-in-history check, the category-by-who-fixes rule and the orchestrator-file rule are applied as asked.

V6: accepted. Applied: Codex `Stop` entry in the manifest's `codex.hooks` block rendered into `codex-config-managed.toml` (routing: Codex boundary, Claude seat); `continuation_of:` with rounds counted against the original; the scope-question count. Note for W3: `AGMSG-PONG v1 status=question` is not in the message contract today (the SKILL names `alive|blocked`, and no script matches `status=question`); W3 adds it to the contract and the counting rule names it, or the count reads blocked PONGs whose note asks a question, which is harder to parse. Still-passing modes carried from round 1: a split without `continuation_of:` is now a boundary violation, which closes the T123 case as far as a file rule can.

V7: accepted. Applied as proposed, including the `.orchestration/<task id>/` exclusion from the 15-file limit and the 5-file review reason, the Stop-hook and gate evaluation of rounds and wall time, and tokens recorded until ten tasks are measured.

V8: accepted. The four consequences are in the sentence: the gate's path rule moves, the CI filter stops skipping evidence-only changes and runs the validator and masker scan as a required check, the committed validation covers the previous head and the gate's live collection the final one. Consistent with `--match-head-commit`.

V9: accepted. Unchanged.

V10: accepted. Transcript paths and the seat-lock session id named.

V11: accepted. "Never idle" removed; dispatchable task defined with `superseded_by`.

V12: accepted. Gaming paths named; add the `not_applicable` one (V5).

## Round-1 document findings, as applied

- F1 (front matter): fixed for YAML; the id pattern remains (V1).
- F2 (waiver contradiction): fixed; "Instruction redo" now says the count did not fire under the redefinition and names this design's receipts.
- F3 (rule redefined in the beneficiary's document): recorded in the PR #313 acceptance-record sentence as visibility; consistent with the trust anchors; not decided here.
- F4 (substrate wording): fixed; herdr "stays the launch and viewing surface"; the SKILL's properties named.
- F5 (citations): fixed for the hooks page and `notify`.
- Open decision: dependencies listed for both options with a recommendation; the operator decides.
- Review record section present and accurate for round 1.
- `design_review.receipt` names the round-1 file; it must name the round-3 accepting receipt once one exists, in this canonical form.

## Earliest mandatory point, re-checked

V3's push warning now fires at the worker's own Stop; V7's rounds and wall time at the orchestrator's Stop with the gate as backstop; V4's audit anchor at the runner before the gate; V6 at the Stop hook of either orchestrator kind. No invariant is prose-only. V3, V10 and V11 say "warn" where they warn.

Design verdict: revise
