---
{
  "audit_findings": [
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "1",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: C15 accepts a locally present design absent from origin/main); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "2",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: C12 excludes agent instruction files such as .claude/skills/*/SKILL.md); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "3",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: an out-of-checkout scope skips C12 instead of a confinement finding); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "4",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: task-from-plan.py drops explicitly named repository-root files); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "5",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: a directory scope with its child yields a C7b-rejected row); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "6",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: paths are not normalized (./scripts/new.py)); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "7",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: unavailable single-word commands are discarded); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "8",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: plan-check F1 mistakes the work cell for the completion cell); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "9",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: the edited-file test recomputes the SHA instead of rejecting changed bytes); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "uv run --no-project --with pyyaml python -I <PR checker> --root <repo> .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md (pasted in the record)",
      "n": "10",
      "reason": "not-applicable: C11 rejects the tests/<module>::<Class>::<test> selector form the regime uses everywhere (dispositions test: refutations, verdict, every task text); the grammar is the defect, not the texts: the first owned row of dotfiles-T133-task-generator-plan-check-followup-a01 widens C11 to the pytest node-id form with an optional class segment; until it lands, dispatch.sh runs the checker from main as before this PR (the orchestrator sequences the owner fix immediately after this merge)"
    },
    {
      "evidence": "grep -n '4306960626' .agents/worklog/orchestrator-glue/417-extra.tsv .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json",
      "n": "11",
      "reason": "not-applicable: corrected in the sweep input: 417-extra.tsv now dispositions thread 4306960626 as fixed:eb20d063 (the bundled-template fix), superseding fixed:b3c6b7ea (the error-message improvement); the sweep JSON regenerates on the chain re-run"
    },
    {
      "evidence": "grep -n 'search:' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md; grep -l 'parser-gap' .orchestration/learning/mistakes/*.md",
      "n": "12",
      "reason": "not-applicable: corrected in this record: the parser-gap class (four lineage rows) carries its re-plan in the JSON replans object and the pasted search line below (no mistake record carries the slug yet; M-20261019-04 is written for it)"
    }
  ],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a02 round=1 reset_of=dotfiles-T133-task-generator-plan-check-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md task_sha256=a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98 deadline=none done_signal=AGMSG-RESULT note=a009:INV-6-reset-of-a01(the-fifteen-audit-findings-as-items,the-bundled-template,the-C14-sha-gate,item-20-the-checker-hardening)"
  ],
  "format": 1,
  "head": "8a09b9365932f23b09df8aa2385a93d0b3016a3e",
  "ledger": [
    {
      "class": "evidence-integrity",
      "id": "audit:9da0ed3:1"
    },
    {
      "class": "threat-row-stale",
      "id": "audit:9da0ed3:2"
    },
    {
      "class": "replan-not-patch",
      "id": "audit:9da0ed3:3"
    },
    {
      "class": "dispatch-wiring",
      "id": "audit:9da0ed3:4"
    },
    {
      "class": "spec-gap",
      "id": "audit:9da0ed3:5"
    },
    {
      "class": "glob-classification",
      "id": "audit:9da0ed3:6"
    },
    {
      "class": "glob-intersection",
      "id": "audit:9da0ed3:7"
    },
    {
      "class": "substring-selection",
      "id": "audit:9da0ed3:8"
    },
    {
      "class": "glob-filter",
      "id": "audit:9da0ed3:9"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:10"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:11"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:12"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:13"
    },
    {
      "class": "regex-gap",
      "id": "audit:9da0ed3:14"
    },
    {
      "class": "records-form",
      "id": "audit:9da0ed3:15"
    },
    {
      "class": "trust-boundary-pr-input",
      "id": "4306960622"
    },
    {
      "class": "missing-input-crash",
      "id": "4306960626"
    },
    {
      "class": "string-form-comparison",
      "id": "4306960630"
    },
    {
      "class": "spec-gap",
      "id": "audit:8a09b93:1"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:2"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:3"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:4"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:5"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:6"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:7"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:8"
    },
    {
      "class": "test-coverage",
      "id": "audit:8a09b93:9"
    },
    {
      "class": "selector-grammar",
      "id": "audit:8a09b93:10"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:8a09b93:11"
    },
    {
      "class": "records-form",
      "id": "audit:8a09b93:12"
    }
  ],
  "pr": 417,
  "replans": {
    "decision-not-bound-to-execution": {
      "design": "design 5.14 items 2, 3 and 4 applied to task-consistency-check.py, task-from-plan.py and plan-check.py: env -i with a private PATH of absolute trusted-root binaries (never <root>/bin), realpath checks that refuse outputs or globs resolving outside the checkout, O_EXCL output creation that refuses an existing symlink, and the C11 node-id grammar",
      "implementation": "the a03 reset of P1-12 on the same branch (PR #417): the a02 implementation stays, the three security P1 and the P2 traversal become items with red-then-green tests, C11 accepts tests/<path>::<Class>::<test>; the twelve audit P2 stay with the owner dotfiles-T133-task-generator-plan-check-followup-a01",
      "specification": "the checker and the generator execute nothing from a checkout-controlled place: premise commands run only for a text whose sha256 the orchestrator supplied and under a trusted interpreter and PATH; plan commands are never executed by the generator (it records them as text); outputs are written through a symlink-checked path inside .orchestration/tasks/",
      "verification": "red against 8a09b936: a checkout bin/bash is never executed by C14; a plan command is never executed by the generator; a symlinked output path is refused; a traversal glob is refused; the a02 copy passes C11"
    },
    "parser-gap": {
      "design": "a parsing module shared by both scripts with the construct table and its fixtures; the generator and the checker consume parsed records, not lines",
      "implementation": "the P1-12 owner task dotfiles-T133-task-generator-plan-check-followup-a01 (rows audit:9da0ed3:10-13 and audit:8a09b93:7-8), after the C11 grammar row",
      "specification": "task-from-plan.py and plan-check.py parse plan and todo tables through one table-driven tokenizer with a fixture per construct (numbered items with blank lines and fenced blocks, commands with redirects or single words, acceptance events with timestamps and task ids, PR occurrences with several SHAs), never ad-hoc substring tests",
      "verification": "one red-then-green fixture per construct; plan-check.py run against the live plan 024 files reports zero parser warnings"
    }
  },
  "searches": [
    {
      "class": "parser-gap",
      "records": []
    },
    {
      "class": "decision-not-bound-to-execution",
      "records": []
    }
  ],
  "task": "dotfiles-T133-task-generator-plan-check-a02"
}
---

# Acceptance record: dotfiles-T133-task-generator-plan-check-a02

Plan 024 P1-12, the INV-6 reset of `dotfiles-T133-task-generator-plan-check-a01` (two amendments by substance, M-20261018-15; the audit of 9da0ed3: 3 P1 and 12 P2, folded in as items 5 to 19). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p112-a02.md`, prompt `p112-a02-redesign-prompt.md`); the orchestrator added item 20 (the checker hardening PR #418's review pointed here: C10 literals as `git grep -e` operands, C6 paths confined to the checkout) and the stale-premise note before the send. Seat a009 (worker-c, Claude) continues PR #417 from 9da0ed3. Owner of advisory P2: `dotfiles-T133-task-generator-plan-check-followup-a01` (written 21:0xZ).

- 2026-10-18T21:4xZ: task text installed, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a009 (the line above; the full note is in the bus history). Known stale premise 5 (test_task_checkers.py "in flight in PR #413"): #413 merged at 10:46Z; a C14 finding at acceptance, records-form.
- 2026-10-19T00:08:22Z: RESULT round 1 from a009: PR #417 head 3f12e603118b8bb1acc9005f5befcdb5b9cbd2b7 (code head 6e07d291, continued from 9da0ed3) on 3e41e36a; `task_copy=a3ab8ea6…` (the dispatched sha); first push 6da92853 (the a01 copy deleted, the a02 copy added); the three Bot threads fixed (538e60bd, eb20d063); audit items 5 to 19 fixed at eb20d063 (item 19's C12 remedy owned here) and item 20 (C10 `-e` operands, C6 confinement); one self-review round (2 P2 + 4 P3, fixed 6e07d291); 15 new or updated end-to-end tests red on 9da0ed3 by exact id; four modules 28 OK; unit baseline identical to 3e41e36a; the checker passes 29 T133 files with the C14 not-run warning ×20; plan-check exit 1 with six violations left for the orchestrator (F3 ×2, F4, F6 ×3); caps 659/700 and 657/800; dispatch.sh:238 needs `--premises-sha` (the P1-5/P1-6 lineage); INV-6 0/0/0. `status=pending-integration` sent 00:1xZ; the chain is queued after #411 and #420.

## Owned by dotfiles-T133-task-generator-plan-check-followup-a01

- `checker:C17` residual-sentence-vs-allowed-files: a threat row whose disposition claims "no <kind> file is in allowed_files" (workflow, interpreter, script) is verified by task-consistency-check.py against the front matter; PR #421 shipped a false residual (Bot P1 4309302616, local P2) copied from the narrow owner template after the task was widened to three workflow files.
- `checker:C19` inherited-caps: a task text that applies another task's Check or Completion clause by reference restates its own comparison range and caps; task-consistency-check.py resolves the reference and fails a text whose caps are only inherited (PR #423 audit:9d13a06:2: the a01 amendment's 741e242...HEAD 60/120 caps were imported into a02 and measured 1,025/1,997 there).
- 2026-10-19T03:41Z: the chain update-branched #417 onto b22a5580 (→ 63b6acae); the four `test` jobs fail on three regime tests (run 39195158133): the #418 fixtures in tests/unit/test_regime_ci.py carry pre-C13 threat-row dispositions and the regime verifier runs this task's checker on them ("C13 disposition is not closed:, residual: or out-of-scope: and a space"); a semantic conflict between two merged lineages, not a defect of either alone. Counters: tasks=1 amendments=0 results=1 revises=0. Decision: amendment 1 (fixture repair only; tests/unit/test_regime_ci.py joins allowed_files with its row; C-61: one CI-repair round) dispatched to a009 03:4xZ (sha 60d4c2db…, previous a3ab8ea6…). Root cause: the checker vocabulary changed in one lineage while another lineage's fixtures were written against the old grammar; nothing runs the full suite of main-plus-PR before the update-branch (the chain's CI does, which is where it surfaced).
- 2026-10-19T04:03:46Z: CI-repair-1 RESULT from a009: PR #417 head 8a09b936 (code head eb0b1c06, previous 63b6acae) on b22a5580; `task_copy=60d4c2db…` (amendment 1); repair in tests/unit/test_regime_ci.py only (the five fixture threat rows take the C13 grammar); regime tests red on 63b6acae, 101 tests green on eb0b1c06; CI 11/11; Bot none in 15 min; caps 659/700 and 673/800. `status=pending-integration` sent 04:0xZ; the chain re-runs after #424.
local:8a09b93:1	advisory-p2
local-finding: 8a09b93:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:2	advisory-p2
local-finding: 8a09b93:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:3	advisory-p2
local-finding: 8a09b93:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:4	advisory-p2
local-finding: 8a09b93:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:5	advisory-p2
local-finding: 8a09b93:5 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)

## Lineage ledger rows for the audit of 9da0ed3 (the a01 head; the a01 stopped at S2 and the a02 reset absorbed the fifteen findings as its items, all reported fixed in the a02 RESULT 00:08Z; the a01 record carries no rows because the task was withdrawn before disposition; the record step writes no lineage rows, the P1-6 item)

audit:9da0ed3:1	evidence-integrity
audit:9da0ed3:2	threat-row-stale
audit:9da0ed3:3	replan-not-patch
audit:9da0ed3:4	dispatch-wiring
audit:9da0ed3:5	spec-gap
audit:9da0ed3:6	glob-classification
audit:9da0ed3:7	glob-intersection
audit:9da0ed3:8	substring-selection
audit:9da0ed3:9	glob-filter
audit:9da0ed3:10	parser-gap
audit:9da0ed3:11	parser-gap
audit:9da0ed3:12	parser-gap
audit:9da0ed3:13	parser-gap
audit:9da0ed3:14	regex-gap
audit:9da0ed3:15	records-form

## Bot-thread ledger rows carried from the a01 record (PR #417 round 1 and revise 1 of the a01; fixed:b3c6b7ea and fixed:538e60bd, in 417-extra.tsv; the record step writes no Bot rows)

4306960622	trust-boundary-pr-input
4306960626	missing-input-crash
4306960630	string-form-comparison
- 2026-10-19T04:17-04:19Z: the #417 chain was started twice in the same review worktree (a guarded launch waited for the ledger rows while the orchestrator wrote them and launched again); the second run failed at its fetch step ("git checkout --detach does not take a path argument FETCH_HEAD") and the first stopped on three Bot-thread ledger gaps (4306960622/26/30, dispositioned in 417-extra.tsv but absent from the record's ledger). Rows carried from the a01 record's JSON ledger (trust-boundary-pr-input, missing-input-crash, string-form-comparison) and the chain re-run alone at 04:19Z. Hygiene: a guarded launch is never combined with a later unguarded launch of the same chain; one review worktree per PR (P1-6) removes the collision class.

## Audit of 8a09b936 (2026-10-19T04:28Z): twelve P2, no P0/P1; acceptance with owner rows

- The chain (sweep 7 items 0 gaps; local review 0; the ledger completed by hand with the 15 lineage rows of 9da0ed3 and the 3 Bot rows) ran the audit (`.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md`): `Verdict: incorrect` on twelve P2: nine implementation (C15 local-design acceptance; C12 scope and confinement gaps; task-from-plan.py root files, directory-with-child rows, unnormalized paths, discarded single-word commands; plan-check.py F1 cell), one evidence (the edited-file SHA test), three orchestration (C11 rejects the `::Class::test` selector form amendment 1 uses; the template thread's `fixed:b3c6b7ea` should be `fixed:eb20d063`; the parser-gap class lacks its search evidence). Task-copy SHA and both caps verified by the auditor.
- counters: tasks=1 amendments=1 (the CI-repair amendment) results=2 revises=0; worker rounds 2 (pre-push review, CI repair): the C-61 cap.
- decision: no worker round (the cap; no P0/P1). The nine implementation P2 and the evidence P2 are advisory rows of the P1-12 owner `dotfiles-T133-task-generator-plan-check-followup-a01`, dispatched to a009 right after this merge with the C11 grammar as its first row (the regime's selector convention is the pytest node id with an optional class; C11's narrower grammar would make dispatch.sh refuse the next texts, so the owner fix lands first and no text is dispatched through a C11-bearing checker before it). The template disposition is corrected in 417-extra.tsv. The parser-gap class (rows audit:9da0ed3:10-13, audit:8a09b93:7-8) gets its re-plan in the JSON block and the search below.

search: grep -l 'parser-gap' .orchestration/learning/mistakes/*.md → (no record; M-20261019-04 written now)

audit:8a09b93:1	spec-gap
audit:8a09b93:2	glob-classification
audit:8a09b93:3	glob-filter
audit:8a09b93:4	glob-filter
audit:8a09b93:5	glob-classification
audit:8a09b93:6	glob-filter
audit:8a09b93:7	parser-gap
audit:8a09b93:8	parser-gap
audit:8a09b93:9	test-coverage
audit:8a09b93:10	selector-grammar
audit:8a09b93:11	evidence-integrity
audit:8a09b93:12	records-form

## Owned by dotfiles-T133-task-generator-plan-check-followup-a01

- `audit:8a09b93:10` selector-grammar (first): C11 accepts the pytest node id `tests/unit/<module>.py::<Class>::<test>` and `::<test>`; red against 8a09b936 with the a02 copy itself.
- `audit:8a09b93:1` C15 requires the design on origin/main; `audit:8a09b93:2` C12 covers agent instruction files; `audit:8a09b93:3` an out-of-checkout scope is a confinement finding; `audit:8a09b93:4` root files are kept; `audit:8a09b93:5` directory-with-child rows; `audit:8a09b93:6` path normalization; `audit:8a09b93:7` single-word commands retained with their failure status; `audit:8a09b93:8` plan-check F1 reads the completion cell by header; `audit:8a09b93:9` the edited-file test rejects changed bytes against the original SHA. Plus the lineage rows audit:9da0ed3:10-13 (parser-gap) under the parser-gap re-plan.
- 2026-10-19T04:31:54Z: the chain refuses a second run for an already-audited head, so the sweep was redone by its two steps alone (`pr-feedback.py 417 --json`, the comments dump, `fill_sweep.py … 417-extra.tsv --orchestrator-login moriya-fumio-thd`): 10 items, 0 gaps; thread 4306960626 now `fixed:eb20d063`, 4306960630 `fixed:b3c6b7ea`, 4306960622 `fixed:538e60bd`. The gate reads this JSON.

## Security review of 8a09b936 (2026-10-19T04:34Z): three P1, one P2; S1 by class; a02 withdrawn, a03 reset

- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md`: `Verdict: incorrect`: (1) P1 task-from-plan.py:114 executes a committed PR HEAD's plan commands with no trusted digest; (2) P1 task-consistency-check.py:89 resolves even `bash` through `<root>/bin` first, so a checkout-controlled interpreter runs under a valid premise hash; (3) P1 task-from-plan.py:228 writes its output through an existing symlink; (4) P2 plan-check.py:86 task-controlled globs enumerate outside --root. C14's same-byte hash, the C10 fix, C6 and yaml.safe_load hold.
- class: `decision-not-bound-to-execution` (the class of P1-14's a03/a04 and of every C-80 review today); three security P1 in one mechanism text written before design 5.14 → S1 at the class level; the C-61 cap is also reached (pre-push review, CI repair). The glue guard refuses the merge (P1 lines).
- decision: a02 withdrawn (`status=withdrawn` to a009 04:3xZ; the branch and PR #417 stay); a03 (reset_of a02) applies 5.14 items 2-4 to the three scripts, folds the three P1 and the P2 as items, and the C11 node-id grammar (so the merged checker accepts the regime's selector form); the twelve audit P2 stay with the owner followup-a01, which is dispatched after a03 merges. The a03 text passes C-80 before dispatch; a009 implements on the same branch.

security:8a09b93:1	decision-not-bound-to-execution
security:8a09b93:2	decision-not-bound-to-execution
security:8a09b93:3	decision-not-bound-to-execution
security:8a09b93:4	glob-filter
- 2026-10-19T04:45:46Z: C-80 review of the a03 text (`dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md`): `Verdict: incorrect`, three P1: (1) C14 authenticates the premise command text, not its file operands (`python -I scripts/probe.py`, `source ./probe.sh` run checkout bytes under a trusted interpreter) → premises become a fixed read-only probe vocabulary the checker interprets, no shell (5.14 item 2 amended); (2) `uv run --no-project … python -I` still discovers `.venv` and uv configuration → `--no-config --python <absolute trusted interpreter> --offline` with a hostile .venv fixture (5.14 item 9 amended); (3) the sandbox claims have no deployment prerequisite (the manifest still has failIfUnavailable false and the Linux gh exclusion) → `after: [dotfiles-T133-worker-write-boundary-a01]` and the pre-P1-15 residual stated. Round 2 of the a03 text follows.
- 2026-10-19T04:5xZ: a03 round-2 text installed (C14 probe vocabulary without a shell; uv --no-config --python <abs>; after: worker-write-boundary-a01); checker OK; its C-80 review started.
- 2026-10-19T05:32:41Z: a03 round-3 text installed (the repository-local git filter check before any status or diff, with the marker regression); checker OK; its third C-80 review started 05:33Z.
- 2026-10-19T05:36Z: C-80 third review of the a03 text (`…-a03-text-security-49a7944.md`): one P1: `git config --local` misses the worktree-scoped config.worktree and includes, so a filter defined there bypasses the check → the check reads the effective configuration (`--show-origin --get-regexp`) with three fixtures; round 4 follows.
- 2026-10-19T05:44:43Z: C-80 fourth review of the a03 text (`…-a03-text-security-8ce8dba.md`): two P1: `git status` can recurse into a selected submodule whose own configuration activates filters (the preflight checks only the parent) → submodule traversal prohibited and a checkout with .gitmodules refused; lazy fetching of missing objects can run checkout-configured credential helpers → GIT_NO_LAZY_FETCH=1 on inspection reads (5.14 item 2 amended); round 5 follows.
- 2026-10-19T05:52Z: a03 round-5 text installed (submodule recursion refused, GIT_NO_LAZY_FETCH=1 on inspection reads, the two regressions); checker OK; its fifth C-80 review started.
- 2026-10-19T05:58:14Z: C-80 fifth review of the a03 text (`…-a03-text-security-5c20a6e.md`): one P2 (repository-local core.worktree can redirect reads outside the validated checkout while -C does not bind the work tree) → explicit --git-dir/--work-tree with a show-toplevel check (5.14 item 2 amended); round 6 (one change) follows since the dispatch waits for P1-15 anyway.
- 2026-10-19T06:11Z: C-80 sixth review of the a03 text (`…-a03-text-security-819bdac.md`): one P2 (the explicit --work-tree overrides a planted core.worktree, so the required refusal cannot occur) → refuse when the effective configuration defines core.worktree, then bind explicitly; round 7 follows (the dispatch waits for P1-15 anyway).
- 2026-10-19T06:15Z: a03 round-7 text installed (core.worktree refusal before binding); checker OK; the seventh C-80 review started.
- 2026-10-19T06:18:32Z: C-80 seventh review of the a03 text (`…-a03-text-security-9fe33aa.md`): one P2 (the residual still names a main-push detection; the control is the records-PR detection of 5.14 item 0 / ci:detection:1) → wording aligned by the orchestrator (a one-sentence edit, not a redesign round); the eighth C-80 runs.
- 2026-10-19T06:22Z: C-80 eighth review of the a03 text (`…-a03-text-security-8d1bf0b.md`): `Verdict: correct`. The text is ready; its dispatch waits for the P1-15 merge (after:) and goes to a009 after its A owner a03, or to another Claude seat.
