---
task_id: dotfiles-T133-verdict-audit-pool-a01
seat: claude-standard-dot-a008
branch: tools/verdict-audit-pool-a01
base: 99a4a80f
pr: 410
parked_pr: 407
head_code: f6adaea8
commits: [beb0b0c7, fada8070, 2ff92578, f2d1ffd2, be70b5c8, f6adaea8]
task_sha256: 2919563b9f8d47825cf13e251055c7955f5fc975b28896058acd5568ba2d6f59
---

# Report: dotfiles-T133-verdict-audit-pool-a01

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`; AGMSG-TASK 2026-10-18T04:21:59Z (`task_sha256=6576f136…`), Amendment 1 at 04:41:38Z (`task_sha256=2919563b…`, the cap decision below), which the branch copy `task.md` matches byte for byte; the task-consistency check passes on it and the four premises replay on `origin/main` (validation §1, §1a, §2).
- Item 0: `tools/hcom-dispatch-bus-a01` at `dfa9001b` (already pushed) opened as draft PR #407 with the task's exact command; `AGMSG-PONG v1 task_id=dotfiles-T129-hcom-dispatch-bus-a01 status=alive note=parked-draft-pr-407-head-dfa9001b858431751faeab3b779b71eb0da01c2f` sent (message 2089). Then `git switch -c tools/verdict-audit-pool-a01 --no-track origin/main` at `99a4a80f`.
- PR #410 (draft), opened with the plain create form.

## The cap (Amendment 1)

My PONG of 04:37Z asked for the D-cap-F2 form: `.schemas/classes.yaml` is 140 lines of data (137 classes) and the two schemas 62, so data alone was 202 of 500. Amendment 1 decided it: the three files under `.schemas/` leave the count, the scripts stay within 500 on their own, and the Check carries both counts (validation §11).

## What changed

1. `scripts/orchestrator/verdict.sh` (item 1): the nine conditions, each `{id, ok, evidence}`, accept (exit 0) when all hold, hold (20) when (6) or (7) fails or any input is missing, unreadable or fails its schema, revise (10) otherwise with the revise line; the verdict JSON is checked against `.schemas/verdict.json` before the script reports it. `--apply` (accept only: dispatch.sh, then `gh pr merge --squash --match-head-commit`), `--shadow` (the machine column only), `--loop`; an argument containing `--admin` or `--auto` anywhere is refused before any read (exit 2).
   - Condition 1: `precheck.json` cannot carry its own commit's sha, so it names the code commit and the head adds only `.orchestration/<task>/` files on top (the evidence-only ancestor rule of item 1).
   - Condition 5: the Check sentence's caps, and every backticked path the sentence lists after "outside" (up to "(" or ", <n> under") leaves the outside count, so Amendment 1's `.schemas/` and D-cap-F2's data files are read from the task itself; without such a list `tests/` and `.orchestration/` are the default.
   - Fail-closed details found by my own runs: a missing record holds (the `--shadow` run on #410 first exited 2 on it), a head this checkout lacks is fetched as `pull/<n>/head` or holds, a failed merge-base diff can no longer pass condition 5 with an empty numstat, and condition 8 fails when the front matter is unreadable (fix commit 2ff92578, tests red at fada8070, validation §5a).
2. `scripts/orchestrator/audit-pool.sh` (item 2): the queue under `.orchestration/validation/audit-queue/`, the pick under fcntl's exclusive lock on `<queue>/.lock` (python -I: macOS ships no `flock` command, `/usr/bin/lockf` and `/usr/bin/shlock` only, and Linux no `lockf`), one review worktree per slot (slot 2 created detached at `origin/main` before its run starts), `.done` only for a zero exit whose JSON passes `orch-audit.sh --validate`, `.rejected` plus `.blocked` otherwise, the 429 retries after 60, 120 and 240 seconds, the differential gate on two zero-difference rows of `audit-shadow.tsv` (its last field is the finding difference).
3. `scripts/orchestrator/orch-audit.sh` (item 3): `--head <sha40>` (a commit of this checkout), `--json <out>`, `--previous-head`/`--previous-findings`, `ORCH_REVIEW_WORKTREE`, `--validate <schema> <json>`, on a failed run only the marker `the codex transcript mentions 429` (the pool's retry signal; no transcript text leaves, f2d1ffd2); every pre-existing refusal is unchanged and the original header lines are kept with a T133 paragraph appended. One deliberate deviation from item 3's text: the auditor is asked for the json block just before the Verdict line, not after it, because `scripts/require-crit-review.py` (out of scope) reads the verdict from the `.last.md`'s last non-blank line; the extractor then refuses a block whose head, task_id or verdict differs from this audit and its Verdict line. The review worktree's cleanup now also cleans `.schemas`, so a copied schema never leaves it dirty.
4. `.schemas/audit.json`, `.schemas/verdict.json` (JSON Schema 2020-12, `additionalProperties: false` at the top and in the item objects; the class enum generated from the classes file) and `.schemas/classes.yaml` (item 4): 137 classes, the 134 ledger classes of the main checkout's records (a superset of the 121 of the tracked ones) plus `string-form-comparison`, `ps-output-parsing` and `records-form` (the other five named extras are ledger classes already), each with a remedy sentence and blast_radius globs (validation §4).
5. Tests (item 5): the six `test_verdict.py` and seven `test_audit_pool.py` tests the task names.

## re-plan

`re-plan: fail-open-on-error -> after the worker review of 2ff92578 (three P1 of one class: empty gh checks passed condition 2, condition 6 could not see S1 under --history-only, a blocked or incorrect audit without findings passed condition 3) every condition was re-read against one rule, that it is ok only from a positive check of parsed, non-empty, validated input; the specification reading changed where the task's literal text allowed a vacuous pass (blocked holds, incorrect needs an unfixed finding, the record needs sha256 lines and a ledger, the counters run with --pr), the design moved the --apply safety into code (the trusted-checkout comparison with origin/main and the Q-C four-PR gate), the implementation added one red-then-green case per finding, and the verification ran each new case against the scripts before the fix (validation §5a to §5c).`

## Worker review (two rounds; the record and the receipt name every finding)

- Round 1 on `origin/main..2ff92578`: `Verdict: incorrect`, three P1, seven P2 and P3s; fixed in f2d1ffd2 and be70b5c8 after the re-plan above.
- Round 2 on `2ff92578..f2d1ffd2`: `Verdict: incorrect`, two P2 (the `--apply` guard compared with HEAD, so a checkout of the PR's code commit `head~1` passed; condition 6 had no S1 source when the record carried no ledger) and P3s; it confirmed the three P1 and five P2 closed and accepted the declared residuals. Fixed in f6adaea8 with cases red at f2d1ffd2 (§5c). No third worker round: the orchestrator's task-level audit and the security-profile review run on the final head.

## Residuals (each fails closed)

- `audit-pool.sh`: a killed pool's `.running-<n>` files keep their slots until removed; `--once` names them when requests wait (no PID reclaim).
- The stdlib checker accepts a date-only `generated_at` for `format: date-time` and ignores keywords the schemas do not use.
- A stop-path hold (no head, no record naming the PR) writes no verdict JSON or shadow row, since there is no head or task to name it by.
- `--apply` sends the ACCEPTANCE line before the merge (the task's order); it does not run the step-10 gate (`require-crit-review`, out of scope), so the threat row's "after the gate" stays a procedure.
- The differential prompt file is a one-line statement of the differential audit, not the full prompt orch-audit would send.
- The json block sits just before the Verdict line (item 3 says after): the gate reads the verdict from the last line; the extractor refuses a block whose verdict differs from that line.

## Red before this task, not this task's

- `make format`'s shfmt step fails on 12 tracked files under `.orchestration/tasks/*-input/`, exactly as on `origin/main` (validation §9); ruff format and prettier, the steps after it, pass on their own.
- `make unit-test` in this seat's sandbox fails in nine modules (`test_require_crit_review`, `test_herdr_agents`, `test_agent_stop_gate`, `test_ua_symbol_coverage`, `test_update_agent_assets`, `test_runtime_health`, `test_gh_auth`, `test_supply_chain_policy`, `test_aws_cli_acquisition`) with the same counts on a scratch worktree at `origin/main` (validation §7, §7a: e.g. `--base 'main' does not resolve to a commit`, keychain and network tests); none is a module this PR touches, and the PR's CI `test` jobs, which run the same suite, are green.

## Caps (Amendment 1; validation §11)

- Scripts (outside `tests/`, `.orchestration/`, `.schemas/`): 500 of 500 (verdict.sh 255, audit-pool.sh 132, orch-audit.sh 102 added and 11 deleted).
- `tests/`: 493 of 500. `.schemas/` (data, outside the count): audit.json 33, classes.yaml 140, verdict.json 29.

## The Check's --shadow run (validation §12)

`scripts/orchestrator/verdict.sh 410 --task dotfiles-T133-verdict-audit-pool-a01 --shadow` at f6adaea8: hold (exit 20), as the Check expects before the audit exists; the record, the task file and the feedback JSON live in the orchestrator's checkout, so this seat's run also holds on them.

## Bot

(after `gh pr ready 410`)

CompactionDB: the `memory add` runs at the RESULT, and its command goes into this report then.

cost: n/a
