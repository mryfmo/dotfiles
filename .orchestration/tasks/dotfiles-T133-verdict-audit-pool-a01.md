---
format: 2
task_id: dotfiles-T133-verdict-audit-pool-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/verdict.sh
  - scripts/orchestrator/audit-pool.sh
  - scripts/orchestrator/orch-audit.sh
  - .schemas/audit.json
  - .schemas/verdict.json
  - .schemas/classes.yaml
  - tests/unit/test_verdict.py
  - tests/unit/test_audit_pool.py
  - .orchestration/dotfiles-T133-verdict-audit-pool-a01/**
after: []
threat_table:
  - control: "the PR adds scripts/orchestrator/verdict.sh (plan 024 programs (1): the nine conditions read from gh, the record, the audit JSON, the sweep JSON, the task file, the counters and git; accept, revise or hold written as a verdict JSON; --apply acts only on accept and refuses --admin and --auto by syntax; --shadow writes the machine column only)"
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds"
  - control: "the PR adds scripts/orchestrator/audit-pool.sh (programs (2): a flock-serialised queue under the validation directory, at most --max concurrent audits, each through the audit script of item 3; schema-failing output is rejected to a .rejected file and the request blocked; 429 retried three times)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request"
  - control: "the PR edits scripts/orchestrator/orch-audit.sh in three places (item 3: --head <sha> as an alternative to the pr-worktree positional, --json <out> with the schema-shaped final block, ORCH_REVIEW_WORKTREE for the pool's second slot; every existing refusal and the masking after a zero codex exit stay)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal"
  - control: ".schemas/audit.json (new; JSON Schema 2020-12 of the audit record, its class enum generated from the classes file)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class"
  - control: ".schemas/verdict.json (new; JSON Schema 2020-12 of the verdict record)"
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
  - control: ".schemas/classes.yaml (new; the controlled vocabulary of finding classes with remedy and blast_radius per class, seeded from every ledger class in the acceptance records)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius"
  - control: "tests/unit/test_verdict.py (new; fake gh, fake dispatch.sh and fixture records, sweeps, audits and task files in a temporary directory)"
    disposition: "residual: fakes record every argv; the --apply tests assert that nothing is called for revise or hold; no live GitHub or bus"
  - control: "tests/unit/test_audit_pool.py (new; a fake codex that prints a chosen final message, a fake git worktree layout, the schema checks)"
    disposition: "residual: fakes only; the pool's lock and queue live under a temporary validation directory"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-verdict-audit-pool-a01/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the scripts read evidence and write only under .orchestration/validation/ (verdict JSON, audit JSON, the queue, the shadow TSV); --apply's two side effects (the ACCEPTANCE send and the merge) go through dispatch.sh and gh pr merge --squash --match-head-commit, both recorded by their own tools; the schema check is stdlib Python under python -I"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; PRECHECK_REQUIRED (0 makes condition 1 a warning), ORCH_REVIEW_WORKTREE and MODEL_PROFILE_AUDIT_CODEX_ARGS are the environment inputs, each read once; codex runs as it does today, read-only and with approval_policy never"
  - control: new or renamed scripts
    disposition: "residual: 2 new scripts under scripts/orchestrator and 3 new schema files under .schemas, all named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); verdict.sh --apply stays disabled until the shadow comparison agrees four times (plan 024 5.11 Q-C), and this PR itself is merged by the orchestrator by hand"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10); the inheritance of an update-branch-only head is PR #390's, not this task's"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: orch-audit.sh takes the audited head from a PR worktree positional today, so item 3 adds --head as the alternative the pool needs
    command: "/usr/bin/grep -c 'usage: orch-audit.sh <task> <pr-worktree> <pr>' scripts/orchestrator/orch-audit.sh"
    output: |-
      1
  - claim: pr-feedback.py writes its document with --json <out>, the form verdict.sh calls for the final head's sweep
    command: uv run --no-project python scripts/pr-feedback.py --help | /usr/bin/grep -c -- '--json JSON'
    output: |-
      2
  - claim: regime-counters.sh has the --history-only mode verdict.sh reads for condition 6
    command: /usr/bin/grep -c -- '--history-only) history_only=true' scripts/regime-counters.sh
    output: |-
      1
  - claim: none of the new files exists on origin/main
    command: git ls-files .schemas scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh | wc -l
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a01 — the machine verdict and the audit pool (plan 024 P1-4a: `verdict.sh`, `audit-pool.sh`, `orch-audit.sh --json`, the schemas and the class vocabulary)

Written 2026-10-18 by the orchestrator seat from plan 024 (wave P-W0, `024-todo.md` row P1-4a, `024-design-programs.md` items (1), (2), (3), `024-design-mechanism.md` "verdict.sh の判定", `024-design-quality.md` 5.11). Seat: claude-standard-dot-a008 (worker-f). One deviation from the design's path convention: the class vocabulary lives at `.schemas/classes.yaml`, not `.orchestration/learning/classes.yaml`, because the task-consistency check's C2 refuses any `.orchestration/<dir>/` other than the task's own in `allowed_files`; P1-13 reads it there.

## Item 0 (first, about 10 minutes): park PR C stage 1 as a draft

Your worktree holds `tools/hcom-dispatch-bus-a01` at dfa9001b, clean. `git push origin tools/hcom-dispatch-bus-a01`, open the PR as a draft (`gh pr create --draft --head tools/hcom-dispatch-bus-a01 --title "docs(orchestration): hcom-dispatch bus stage 1 item 0 findings (T129 hcom-dispatch-bus a01)" --body "Plan 024 phase 2 C stage 1 item 0, parked as a draft under plan 024 0b; resumed in D-W0 after amendment 1."`), send `AGMSG-PONG v1 task_id=dotfiles-T129-hcom-dispatch-bus-a01 status=alive note=parked-draft-pr-<n>-head-dfa9001b…<sha40>`, then `git switch -c tools/verdict-audit-pool-a01 --no-track origin/main` and start item 1.

## Goal

The orchestrator's acceptance of a PR becomes one script's nine conditions with a JSON verdict, and audits run from a queue two at a time with structured JSON findings whose classes come from one controlled vocabulary, so S1 is counted by machine.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` (new, bash, `set -euo pipefail`, shdoc; `jq` for JSON, `python -I` through `uv run --offline --no-project` only for the schema check). Inputs: `gh pr view <pr> --json headRefOid,isDraft,baseRefName,state,number`; `gh pr checks <pr> --json name,state`; the task id from the acceptance record whose JSON block `pr` equals `<pr>` (or `--task <id>`); that record's block `head`; the record's prose line `precheck: <sha256>` (written by the orchestrator from the RESULT's `precheck=`, the key the gate's fixed block never holds); `.orchestration/validation/<task>-audit-<sha7>.json`; `scripts/pr-feedback.py <pr> --json <mktemp>` for the final head's items and `.orchestration/validation/<task>-pr-feedback.json` for their dispositions; `.orchestration/tasks/<task>.md` front matter (`allowed_files`, `security`) and the Check sentence's caps when present as `at most <n> changed lines outside` and `<n> under tests/`; `scripts/regime-counters.sh <task> --history-only`; `git diff --name-only $(git merge-base origin/main <head>) <head>` and `--numstat`; for `security: true` the file `.orchestration/validation/<task>-security-<sha7>.md.last.md` whose last non-blank line is the verdict. Conditions, each `{id, ok, evidence}`: (1) `git show <head>:.orchestration/<task>/precheck.json` hashes to the record's `precheck:` value and its `head` field is `<head>` or an ancestor whose diff to `<head>` is evidence-only (`.orchestration/<task>/` paths only), a warning instead of a failure while `PRECHECK_REQUIRED` is unset or `0`; (2) the ruleset's seven required checks (the names pasted below) are `SUCCESS` for the head; (3) the audit JSON validates against `.schemas/audit.json`, its `head` is `<head>`, and its verdict is `correct`, or every finding not `fixed` has `scope: records`; (4) every item of the fresh sweep has a disposition in the feedback file, matched by url, and every `not-applicable:` carries `; evidence=`; (5) every changed file matches an `allowed_files` entry and the numstat totals are within the caps; (6) the counters print no `S1:` line and `revises` below 2; (7) no audit finding of priority P0 or P1 remains `new` or `still-open`; (8) for `security: true`, the security verdict line is `Verdict: correct`; (9) every `sha256:<hex> <path>` line in the record's prose matches the file. Verdict: `accept` when all nine are ok; `hold` when (6), (7) fail, when any input is missing or unreadable or fails its schema, or on an internal error; `revise` otherwise, with `revise_line` = `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>` (the `check=` selectors are the orchestrator's). Output `.orchestration/validation/<task>-verdict-<sha7>.json` validating against `.schemas/verdict.json` (`verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at`, optional `revise_line`); exit 0 accept, 10 revise, 20 hold, 2 usage or internal (treated as hold). `--apply`: after `accept` only, write the ACCEPTANCE line `AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=verdict-<sha7> next_action=merge` to a `mktemp` file and send it with `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>` (team, from, to and pane from `--team`, `--from`, `--to`, `--pane`; the pane is the seat's `herdr:<socket>:<pane>` placement, read by the orchestrator), then `gh pr merge <pr> --squash --match-head-commit <head>`; any argument containing `--admin` or `--auto` anywhere in `$@` is refused at parse time (exit 2) before any read. `--shadow`: write the verdict JSON and append `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv` (columns pr, head, machine, human, agree, at; the orchestrator fills human and agree); never send or merge. `--loop`: list open non-draft PRs on `main` whose acceptance record exists and whose block `head` equals the PR head, run the verdict on each in PR-number order, `git fetch origin` between them.
2. `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2] [--queue <dir>]` (new, bash, shdoc). Queue: `.orchestration/validation/audit-queue/<task>-<sha7>.request`, a file of `key=value` lines (`pr`, `head`, `base`, `task`, `previous_head` optional). `flock` on `<queue>/.lock` around the pick; at most `--max` running audits, each in its own slot: slot 1 uses `.claude/worktrees/orchestrator-review`, slot 2 `.claude/worktrees/orchestrator-review-2` (created detached at `origin/main` with `git worktree add` when missing), passed to item 3 as `ORCH_REVIEW_WORKTREE`. Each run: `scripts/orchestrator/orch-audit.sh <task> --head <head> <pr> --json .orchestration/validation/<task>-audit-<sha7>.json [--previous-head <sha> --previous-findings .orchestration/validation/<task>-audit-<prev7>.json]`. Differential mode (previous head and findings) stays off until `.orchestration/validation/audit-shadow.tsv` holds two rows with zero finding difference (plan 024 5.11 Q-C); until then a request with `previous_head` is audited in full and its differential prompt is written beside the output as `<out>.differential-prompt.txt` for the comparison. A zero exit with an output file that validates against `.schemas/audit.json` keeps the file and renames the request to `.done`; anything else writes the reason to `<request>.rejected` and renames the request to `.blocked`. A codex transcript whose last message mentions `429` is retried after 60, 120 and 240 seconds, then blocked. `--loop` repeats every 30 seconds until `<queue>/.stop` exists (the orchestrator stops it at a boundary).
3. `scripts/orchestrator/orch-audit.sh`: `--head <sha40>` as an alternative to the `<pr-worktree>` positional (the head is then `<sha>`, which must exist in this checkout); `--json <out>`: the prompt asks the auditor to end with one fenced ```json block holding the record of `.schemas/audit.json` (head, task_id, auditor, generated_at, verdict, findings[{id, priority, confidence, file, line, class, scope, rationale, status}]) after the `Verdict:` line; the script extracts that block from `<out>.last.md`'s companion, validates it with a stdlib checker (`python -I`: required keys, enums, the sha pattern, the class enum read from `.schemas/audit.json`), writes it to `<out>` and fails with exit 3 when the block is missing or invalid; `--previous-head <sha> --previous-findings <json>`: the prompt also carries `git diff <prev>..<head>` and the previous findings, asking for each previous finding's `fixed` or `still-open` status and for new findings on the new hunks only; `ORCH_REVIEW_WORKTREE` (default the current path) replaces the hardcoded review worktree. Every existing refusal (this checkout at the audited head, the validator untracked or changed, the sweep with gaps, the ledger check) and the masking after a zero codex exit stay as they are.
4. `.schemas/audit.json` and `.schemas/verdict.json` (JSON Schema 2020-12, `additionalProperties: false` at the top level) as `024-design-programs.md` (3) draws them, the class enum of audit.json generated from `.schemas/classes.yaml` (a test keeps them equal). `.schemas/classes.yaml`: one entry per class, `<slug>: {remedy: <sentence>, blast_radius: [<globs>]}`; seeded with every class in any record's ledger today (`for f in .orchestration/acceptance/*.md; do uv run --no-project python -I -c 'import json,sys; t=open(sys.argv[1]).read().split("\n---\n"); b=json.loads(t[0].lstrip("-\n")) if t[0].strip("-\n").startswith("{") else {}; print("\n".join(r["class"] for r in b.get("ledger",[])))' "$f"; done | sort -u`, pasted in the validation file) plus `unbound-evidence`, `fail-open-on-error`, `argv-text-mismatch`, `json-interpolation`, `string-form-comparison`, `ps-output-parsing`, `records-form` and `advisory-p2`.
5. Tests `tests/unit/test_verdict.py`: `test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds` (a green fixture set accepts; nine variants each break one condition: 1 to 5, 8 and 9 give exit 10, 6 and 7 give 20; the JSON names the failed id), `test_verdict_holds_on_a_missing_or_schema_failing_input` (no audit file, an audit with an unknown class, an unreadable record), `test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto` (fake gh and dispatch.sh record argv; revise and hold call neither; accept calls dispatch.sh then gh pr merge with `--match-head-commit <head>`; `--admin` or `--auto` in any position exits 2 before any fake runs), `test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold`, `test_verdict_condition_1_is_a_warning_under_precheck_required_0`, `test_verdict_shadow_appends_the_machine_column_only`. `tests/unit/test_audit_pool.py`: `test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request`, `test_pool_runs_at_most_max_audits_and_the_third_request_waits`, `test_pool_retries_a_429_three_times_then_blocks`, `test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree`, `test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal`, `test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class`, `test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius`. Fixture lines count against the test cap.

The seven required check names (from `gh api repos/mryfmo/dotfiles/rulesets/24397953`, 2026-10-18 13:0x JST): `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)`, `public-bootstrap (macos-14, client)`.

## Out of scope

`dispatch.sh` (P1-5 owns it; verdict.sh is its client), the record generator (P1-6), `dispositions.py` and `--second-opinion` (P1-10), `hold-playbook.sh` (P1-13), the gate `scripts/require-crit-review.py` and `validate-agent-assets.py` (in flight in #390, #389, #396), any `make` target or CI step (the schema check runs as a unit test), `integrate-seat.sh` (P1-4).

## Check

`make unit-test`, `make render-check`, `make format`, `shellcheck` and `shfmt -d` on the three scripts clean, `uv run python -m unittest tests.unit.test_verdict tests.unit.test_audit_pool -v` green, `scripts/orchestrator/verdict.sh --shadow <this PR>` run once on your own PR with its JSON pasted (hold is the expected verdict before the audit exists), all pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 500 changed lines outside `tests/`, `.orchestration/` and `.schemas/` (Amendment 1: the three files under `.schemas/` are data in the D-cap-F2 form and leave the count; paste their line counts separately), 500 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after item 0. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-verdict-audit-pool-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears), `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md>` and `parked_pr=<the item 0 PR number>` in the RESULT. This task is `security: true`: the orchestrator runs the task-level audit and a second review on the `security` profile on the final head before the gate (plan 024 5.11 Q-A).

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-verdict-audit-pool-a01.md: OK
premises 1 to 4: outputs pasted at write time (2026-10-18 13:3x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md
```

## Amendment 1 (round 1, 2026-10-18T04:41Z)

a008's PONG (04:37:22Z): `.schemas/classes.yaml` is about 140 lines of data (134 ledger classes read from the records plus the named extras, one entry each) and the two schema files about 62, so data alone is 202 of the Check's 500 while the scripts need about 375. Decided by the orchestrator by default in the D-cap-F2 form (`.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` Amendment 2): the files under `.schemas/` are data and leave the 500 count; the scripts (`verdict.sh`, `audit-pool.sh`, the `orch-audit.sh` change) stay within it on their own; the Check sentence carries both counts. No rule, test or behaviour leaves.
