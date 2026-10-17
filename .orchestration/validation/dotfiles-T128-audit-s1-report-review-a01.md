---
task_id: dotfiles-T128-audit-s1-report-review-a01
seat: claude-standard-dot-a003
reviewed: .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
reviewed_sha256: 8a4bf6e1ff8ff85950ebbaf6b46cd75937a20403a7d01ba9136034cf43c0d071
brief_sha256: 9bc14fe393b900bd343955cad9acb8c1e596da8ac1ee8366ad1047f8af123db1
origin_main: f7847616
---

# Review: dotfiles-T128-audit-s1-report-a01 (review seat, one round)

Read-only. Sources: AGENTS.md's Audit section and `scripts/orchestrator/orch-audit.sh` on `origin/main` (`f7847616`), `scripts/orchestrator/ledger-check.py`, `scripts/orchestrator/acceptance-front-matter.py`, `scripts/require-crit-review.py` (the gate's ledger check), `tests/unit/test_chain_glue.py`, `tests/unit/test_orchestrator_tools.py` and `tests/unit/test_agmsg_orchestration_docs.py` on the branch head, the `after:` task `dotfiles-T128-rules-s1-replan-a01.md` (main checkout; not yet on `origin/main`), and `.orchestration/templates/task-short.md` (main checkout, the 2026-10-17 clause).

## Checks run

```text
$ shasum -a 256 .orchestration/tasks/dotfiles-T128-audit-s1-report-review-a01.md .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
9bc14fe393b900bd343955cad9acb8c1e596da8ac1ee8366ad1047f8af123db1  .orchestration/tasks/dotfiles-T128-audit-s1-report-review-a01.md
8a4bf6e1ff8ff85950ebbaf6b46cd75937a20403a7d01ba9136034cf43c0d071  .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
$ git show origin/main:AGENTS.md | /usr/bin/grep -c "count on the record"          # premise 1, from a worktree with origin/main fetched (f7847616)
0
$ git show origin/main:scripts/orchestrator/orch-audit.sh | /usr/bin/grep -c "ledger classes"   # premise 2
0
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
dotfiles-T128-audit-s1-report-a01.md: OK
$ validate-agent-assets.py --mask-secrets <a copy of the file>; cmp <copy> <file>
masked 0 match(es) in audit-s1-copy.md
copy unchanged
```

Stop condition 3: the five generic rows (task-file copy, evidence records, task metadata, metadata separators, the three orchestrator effects) match the template verbatim, one row stands for each `allowed_files` entry, and the Completion clause is the template's 2026-10-17 clause with the S1 sentence; the only difference is "the outputs above" for "the Check's outputs", which fits this task's `## Validation` heading. Stop condition 4 holds as pasted above. The re-plan line's form (`re-plan: <class> -> ` with the four words) agrees with the `after:` task's item 1, and S1 over non-advisory rows agrees with it; the task names that task in `after:` and states no unlanded mechanism as present.

## Findings

- [P2] high `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:14` and `:66` — the two new wrapper tests are placed in `tests/unit/test_chain_glue.py`, which replaces `orch-audit.sh` with a stub (`SCRIPTS["orchestrator/orch-audit.sh"] = "orch-audit"`, test_chain_glue.py:65) and so cannot run the real wrapper's extraction or prompt; the real-script harness with a stub `codex` that records its argv, and the four existing `test_orch_audit_*` tests, are in `tests/unit/test_orchestrator_tools.py` (lines 1286 to 1362), which is not in `allowed_files`. Name `test_orchestrator_tools.py` (with its row) in place of, or beside, `test_chain_glue.py`.
- [P2] high `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:66` — item 2 adds a `ledger classes:` sentence and says "Nothing else changes", but the prompt's own per-finding format at orch-audit.sh:67 (`'[P0-P3] confidence dimension file:line rationale'`) stays without the class slug and the count that item 1 adds to AGENTS.md; the auditor is told to report in exactly that form, so the two new fields would conflict with, or be dropped by, the prompt it follows. Extend the format string in the same edit (for example `'[P0-P3] confidence dimension class=<slug> count=<n> file:line rationale'`, which ledger-check.py's `^\s*(?:[-*+]\s+)?\[P[0-3]\]` still counts), assert it in `test_orch_audit_prompt_lists_the_ledger_classes`, and make the orch-audit.sh row (line 20) say three places.
- [P3] medium `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:66` — "exit 2 before any codex call with the ledger-check line it prints today": ledger-check.py reads only the `<id><TAB><class>` body rows and prints nothing about the JSON block, and today's ledger refusal is exit 3 (`refuse "the ledger is incomplete" 3`, orch-audit.sh:57). Name the new refusal line (for example `orch-audit: the record's JSON block is missing or malformed; refused`) and where it sits relative to the ledger check.
- [P3] medium `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:30-31` — the workflow row says "the wrapper runs codex and git as today", but item 2 makes it run `python3 -I` by name for the extraction, a binary the template's row asks to be named with its resolution; the wrapper's existing idiom is `uv run --no-project python -I` (orch-audit.sh:53 and 57). Name the interpreter and how it is resolved, or use the existing idiom.
- [P3] medium `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:65` — the new fixture `tests/fixtures/regime/audit.md` pins the Audit section only through an entry in `PINNED_SECTIONS` (test_agmsg_orchestration_docs.py:227-240, read by `test_regime_rule_sections_are_pinned_whole`); item 1 names the fixture and two sentence tests but not that entry (for example `("audit", ROOT / "AGENTS.md", None, ("## Audit", "\n## "))`), without which the fixture is not compared with the section whole.
- [P3] low `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:66` — the prompt sentence's empty case is ambiguous: "(or none)" may apply to the re-plan list only; acceptance-front-matter.py writes an empty `ledger` list before the first audit, so state the sentence for an empty ledger (`ledger classes: none; re-plan lines: none`).

Task-file verdict: dotfiles-T128-audit-s1-report-a01: revise

## Round 2 (reviewed sha256 da4d379971c17562ac1e1da2f605a60874b3cd4eeef8963af00c0030c6e5b731, origin/main b167fe0a)

```text
$ shasum -a 256 .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
da4d379971c17562ac1e1da2f605a60874b3cd4eeef8963af00c0030c6e5b731  .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
$ premise 1; premise 2   (origin/main fetched, b167fe0a)
0
0
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <file>
dotfiles-T128-audit-s1-report-a01.md: OK
$ validate-agent-assets.py --mask-secrets <a copy>; cmp <copy> <file>
masked 0 match(es) in as1-r2.md
unchanged
```

All six round-1 findings are applied as the Change (round 4) section says: the two wrapper tests in `tests/unit/test_orchestrator_tools.py` with its `allowed_files` entry and row (line 26); the format string `class=<slug> count=<n>` and the orch-audit row at three places (line 20); the refusal line, exit 2 and its place after the ledger check; the `uv run --no-project python -I` idiom in item 2 and the workflow row (line 31); the `PINNED_SECTIONS` entry in item 1; the empty-ledger sentence. The generic rows and the Completion clause are unchanged from round 1 and still match the template.

### Findings

- [P2] high `.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:66` — the round-5 sentence names `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt` as one of "the two existing tests whose TSV-only record `4250000001\tother` reaches the extraction" and authorises "a valid JSON block … in their record fixture"; but that test (test_orchestrator_tools.py on origin/main, the method starting `# a05 item 9`) writes no `.orchestration/acceptance/t-a01.md` at all and has no `.python-version` shim, so every `uv run …` it reaches goes to the module's stub `uv` (`STUBS["uv"]`, which execs `.python-version` only when present and otherwise records its argv, prints `$CALLS/uv-output` and exits 0): the extraction never runs Python there, and a record fixture changes nothing. The TSV-only record is in the gap test (exit 3 at the ledger check, before the extraction) and in the isolation test (which has the shim and does reach the extraction, as stated). Name the no-fresh-receipt test's real dependency instead: what the wrapper does with the stub's empty extraction output (refuse as malformed, which breaks the test, or treat it otherwise), and the fixture change that test then needs (for example `uv-output` answering the extraction, or a `.python-version` shim plus a record), within the row at line 26.

Task-file verdict (round 2): dotfiles-T128-audit-s1-report-a01: revise

## Round 3 (reviewed sha256 1c9782d6b6214cb42b3068b720e51f9c3b368c0b85d81ee171012f749ede3113, origin/main b167fe0a)

```text
$ shasum -a 256 .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
1c9782d6b6214cb42b3068b720e51f9c3b368c0b85d81ee171012f749ede3113  .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
$ premise 1; premise 2   (origin/main fetched, b167fe0a)
0
0
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <file>
dotfiles-T128-audit-s1-report-a01.md: OK
$ validate-agent-assets.py --mask-secrets <a copy>; cmp <copy> <file>
masked 0 match(es) in as1-r3.md
unchanged
$ the "Cited sources" commands replayed against origin/main's copies of the five files (a scratch script); cmp with the pasted block (43 lines)
cited sources replay identically from origin/main
```

The round-2 P2 is applied: item 2 now states the extraction's contract (its exit status decides; its stdout is the sentence verbatim, an empty output an empty sentence) and each existing `test_orch_audit_*` test's actual path, which matches the module on origin/main. The isolation test reaches the extraction with real Python through its `.python-version` shim and a TSV-only record, so its fixture gains a JSON block. The no-fresh-receipt test has no shim and writes no record, so the stub `uv` answers the extraction with the empty `uv-output` the test writes, and the run proceeds unchanged. The gap test stops at the ledger check (exit 3) and the differs-from-head test before it. The test module's row (line 26) says one fixture, as item 2 does (the Codex half's round 7). The two new tests through the shim are feasible as stated: the stub `codex` records its argv, the prompt among it, before the run reaches the fixture's masker call; a malformed block passes the TSV ledger check and fails the extraction. The `## Cited sources` block replays exactly. The generic rows and the Completion clause are unchanged and still match the template; stop conditions 1 to 4 hold.

### Findings

- No finding. Justified approval: every claim item 2 makes about existing code is now backed by a cited line that replays from origin/main, and each named test has a path that pins one branch (the sentence and format string; the exit-2 refusal; the isolation test's `python -I` over the extraction).

Task-file verdict (round 3): dotfiles-T128-audit-s1-report-a01: confirm
