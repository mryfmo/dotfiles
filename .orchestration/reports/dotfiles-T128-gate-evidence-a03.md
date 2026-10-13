# Report: dotfiles-T128-gate-evidence-a03

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329. a03 is a02's reset under plan 011 option F (reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a02-design-reset.md`), continued from the worker's head `61d90302` (merge head `4e2266aa`).
- Task file: amendment 1 (plan 013 option A′, TASK 01:45:59Z) at sha256 `1b8ba5b4…`, recommitted byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a03/task.md`. The first a03 copy was `686806a1…`, and a01's and a02's copies stay unchanged as history (validation §1).
- Commits:
  - a01: `7f763b7f`, `9a860c95`, `5971fffe`;
  - a02: `379845f7`, `386a71b3`, `c81c88a3`, `d5d6c9b1`, `c6cf0548`, `61d90302`;
  - a03: `b2b3db45` (the YAML front matter; made as `3c67f512` on `61d90302` and replayed onto the merge head `4e2266aa` with the same content outside `.orchestration`), `c36fcd35` (evidence), `7581d590` and `3c20b0ca` (fix round 1 and its evidence, held local under the 01:12Z PING);
  - amendment 1: `f5f980f9` (the JSON block, the task copy), then this evidence.

## What the PR does (task steps 1 to 5)

1. A disposition is `fixed:<commit>` (unchanged; a `fullmatch` of `fixed:[0-9a-f]{7,40}`) or `not-applicable:<reason>; evidence=<command>`. `parse_disposition` splits once on the literal `; evidence=` with `str.partition` and checks that both parts are non-empty. A text with more than one delimiter is refused. The work is linear: a one-million-character malformed disposition is refused in well under 0.5 s (thread 4249544794). `;evidence=` without the space is no delimiter, because the task names the literal. The error text is unchanged: `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`.
2. The acceptance-record contract, as of amendment 1. `ACCEPTANCE_EVIDENCE` is required whenever `BASE` is set and is checked right after the PR-feedback evidence:
   - `orchestration_path_error(..., "acceptance")`, then the a02 binding: the file is `<task>.md` for the task named by `<task>-pr-feedback.json`, by name and by resolved name;
   - the block between the first two `---` lines (the idiom of `validate-agent-assets.py`'s `read_frontmatter`) is one JSON object, read with the standard library: `json.loads(…, object_pairs_hook=refuse_duplicate_keys, parse_constant=refuse_non_finite)`. A duplicate key at any depth gives `acceptance record: duplicate key <k>` (thread 4250238729; plain `json.loads` keeps the last one). `NaN` or `Infinity` gives `acceptance record: non-finite number`. Text that is not JSON, or a block that is not an object, is refused. The gate has no third-party import, no `uv`, no subprocess for the record and no online retry (thread 4250238721). The prose after the block is not read (`test_acceptance_record_prose_is_not_read`);
   - the identity triple is checked together before anything else:
     - `task` equals the file's task id;
     - `head` equals the full `HEAD` sha the gate runs at (computed also without `BASE`), else `acceptance record head <x> is not HEAD <y>` (thread 4249544762);
     - `pr` equals the `pr` of `PR_FEEDBACK_EVIDENCE`, else `acceptance record pr <x> is not the swept pr <y>` (thread 4250238714). Without a feedback file, `pr` only has to be a positive int.

     When the triple fails, no other field is judged;

   - `format` is the int 1;
   - `ledger` is a list of exactly `{id, class}`. `id` is a thread id (10 or more digits) or `audit:<sha7>:<n>`, accepted as a JSON number or a string; `class` matches `[a-z0-9-]+`;
   - `searches` is a list of exactly `{class, records}`, where `records` is a list of strings; a class named twice is refused;
   - for each class at three or more ledger rows, the gate finds the files under `.orchestration/learning/mistakes/` with `pathlib` (recursively, not following symlinks) that have a line beginning with `classes:` whose rest contains the class. That is the match of `grep -rl 'classes:.*<class>'` without the `grep` subprocess. The class's `records` must equal those basenames as a set (`records: []` when there are none), otherwise `S6: class <slug> at <n> without a matching records search`. A missing records directory is refused;
   - `audit_findings`, when present, is a list of exactly `{n, reason, evidence}`, where `n` is an int of at least 1 and `reason` and `evidence` are non-empty strings. An entry with `fixed` is refused with "a fix moves HEAD, so audit the new head instead". The 20-character minimum on a reason is carried over from `AUDIT_DISPOSITIONS` (declared). When the audit verdict is `incorrect`, the entries must cover findings 1..N once each. A `reason` that quotes `not-applicable:` is just a field (thread 4249544748);
   - the record is not counted when sizing the diff (a02, thread 4248232998).

   `AUDIT_DISPOSITIONS` is retired: the gate no longer reads it. When it is still set, the gate prints one line saying so instead of refusing, because the SKILL names it until `dotfiles-T128-playbook-rules-a04` lands. The recipe's comment in `Makefile` names `audit_findings` in its place; README 427 to 428 and 1101 already name `ACCEPTANCE_EVIDENCE`.

3. Tests and fixtures (below). The module runs 86 tests, against 71 on `origin/main`: 15 more, where the task asks for at least nine (validation §2, §3). Each rule fails a test when broken: one-line mutations M2 to M20, plus the guards of `origin/main`, of a02's head `61d90302` and of the YAML form `7581d590` (validation §4).
4. `make require-crit-review` without `BASE` on a records-only tree prints the same line and exit status at the amendment's code head as at `origin/main` (validation §6).
5. Nothing else changes in the gate.

## Fixtures and the tests that read them

| Fixture                                | Read by                                                                                                                                                                           |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pr-feedback-wrong.json`               | `test_dispositions_of_2026_10_12_without_evidence_are_refused`                                                                                                                    |
| `pr-feedback-right.json`               | `test_dispositions_with_an_evidence_command_are_accepted`                                                                                                                         |
| `acceptance-stale-head.md`             | `test_acceptance_record_head_must_be_head`, `test_base_requires_an_acceptance_record_under_acceptance`                                                                            |
| `acceptance-s6-missing.md`             | `test_s6_class_at_three_without_a_searches_entry_is_refused`, `test_base_requires_an_acceptance_record_under_acceptance`                                                          |
| `acceptance-s6-present.md`             | `test_s6_class_at_three_with_the_matching_searches_entry_is_accepted`, `test_acceptance_record_prose_is_not_read`, and every other `guard_base` run as the default passing record |
| `acceptance-finding-quotes-grammar.md` | `test_audit_finding_reason_may_quote_the_grammar` (an `incorrect` audit with one finding)                                                                                         |
| `acceptance-wrong-pr.md`               | `test_acceptance_record_pr_must_be_the_swept_pr`, `test_base_requires_an_acceptance_record_under_acceptance`                                                                      |
| `acceptance-duplicate-key.md`          | `test_acceptance_record_refuses_a_duplicate_key`, `test_base_requires_an_acceptance_record_under_acceptance`                                                                      |
| `acceptance-nan.md`                    | `test_acceptance_record_refuses_a_non_finite_number`, `test_base_requires_an_acceptance_record_under_acceptance`                                                                  |

All paths are under `tests/fixtures/gate-evidence/`. The nine fixtures total 118 lines (validation §5). `"head": "HEAD"` in a fixture is replaced with the test repository's HEAD by `write_record`. The wrong fixture's two dispositions are, byte for byte, the `disposition` fields of items 4244248692 and 4244378809 in `.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json`; the right fixture extends each with the command that refutes the claim (validation §5). The present fixture's `records: ["M-20261012-3.md"]` is what the real tree's search returns.

**Declared: `tests/fixtures/gate-evidence/.prettierrc` (`{ "trailingComma": "none" }`).** Prettier formats the block between the `---` lines as YAML front matter. With its default `trailingComma: "all"`, it rewrites a broken-up JSON object with trailing commas, which `json.loads` refuses (validation §5 shows the before and after). CI's `prettier --check` covers every tracked `.md`, including these fixtures, so without the directory config they would be either reformatted into invalid JSON or reported as unformatted. With it, prettier's output is valid JSON and stable. The file is in `allowed_files` (`tests/fixtures/gate-evidence/*`), but it is formatter configuration, not data the tests read, so the fixtures' threat row does not describe it. Real acceptance records live under `.orchestration/`, which `.prettierignore` excludes, so they are never reformatted.

New and rewritten tests:

- `test_base_requires_an_acceptance_record_under_acceptance`, the threat row's closing test. It covers:
  - the path: empty, outside `.orchestration/acceptance/`, another task's record, a symlink alias, the task's own record missing;
  - one case per block rule: no block, not JSON, a list instead of an object, a non-finite number, a duplicate key, `format`, `task`, `head`, `pr` missing, `pr` of another PR, a ledger `id`, a ledger `class`, `searches` records, a class searched twice, an `audit_findings` entry citing a fix, S6.
- `test_acceptance_record_pr_must_be_the_swept_pr`, `test_acceptance_record_refuses_a_duplicate_key`, `test_acceptance_record_refuses_a_non_finite_number`, `test_acceptance_record_head_must_be_head`, `test_acceptance_record_prose_is_not_read`, `test_audit_finding_reason_may_quote_the_grammar`, `test_disposition_parsing_is_linear`, and `test_retired_audit_dispositions_is_not_read`.
- `test_s6_searches_entry_must_equal_the_recomputed_records_search` accepts the matching set (where `M-20261012-9.md`, which names `scope` outside its `classes:` line, is not found), and `[]` where nothing matches. It refuses a record missing, a record too many, another class's entry and a pasted command for its records, and refuses a missing records directory.
- `test_incorrect_audit_needs_audit_findings`: no `audit_findings`, a fix, a short reason, no evidence, empty evidence, one missing, the same finding twice, out of range, and accepted.
- `test_s6_class_at_three_without_a_searches_entry_is_refused` and `test_s6_class_at_three_with_the_matching_searches_entry_is_accepted`.

## Bot threads

| Round (review, head)               | Thread     | P   | Class                                                    | Disposition                                                                                                                                                                                                                 |
| ---------------------------------- | ---------- | --- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| a01/a02 1 (5491066199, `5971fffe`) | 4248232955 | P1  | skill-command-sync                                       | proposed `not-applicable:owned by dotfiles-T128-playbook-rules-a04 item 6, and PR #328 merges before #329; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` (validation §5) |
| 1                                  | 4248232964 | P1  | acceptance-record-binding                                | `fixed:379845f7`                                                                                                                                                                                                            |
| 1                                  | 4248232976 | P1  | threat-row-missing                                       | `fixed:379845f7` (the row is in the a03 task copy)                                                                                                                                                                          |
| 1                                  | 4248232988 | P1  | acceptance-dispositions                                  | `fixed:f5f980f9` (`audit_findings`; no `audit-finding:` lines are read)                                                                                                                                                     |
| 1                                  | 4248232998 | P2  | evidence-diff-sizing                                     | `fixed:379845f7`                                                                                                                                                                                                            |
| 1                                  | 4248233012 | P1  | search-command-scan                                      | `fixed:f5f980f9` (the gate's own pathlib search)                                                                                                                                                                            |
| 2 (5491635781, `386a71b3`)         | 4248697658 | P1  | search-command-scan                                      | `fixed:f5f980f9`                                                                                                                                                                                                            |
| 2                                  | 4248697668 | P1  | acceptance-dispositions                                  | `fixed:f5f980f9` (prose is not read)                                                                                                                                                                                        |
| 3 (5491920865, `d5d6c9b1`)         | 4248934816 | P1  | disposition-delimiter                                    | `fixed:c6cf0548`, kept by a03's single split                                                                                                                                                                                |
| 3                                  | 4248934830 | P1  | search-command-scan                                      | `fixed:f5f980f9`                                                                                                                                                                                                            |
| 4 (5492641317, `4e2266aa`)         | 4249544748 | P1  | acceptance-dispositions                                  | `fixed:f5f980f9` (fields, not substrings)                                                                                                                                                                                   |
| 4                                  | 4249544762 | P1  | acceptance-record-binding                                | `fixed:f5f980f9` (`head` equals HEAD)                                                                                                                                                                                       |
| 4                                  | 4249544794 | P2  | regex-backtracking                                       | `fixed:f5f980f9` (one split, linear checks)                                                                                                                                                                                 |
| a03 1 (5493539294, `c36fcd35`)     | 4250238714 | P1  | acceptance-record-binding (third; the S7 stop, plan 013) | `fixed:f5f980f9` (`pr` equals the swept pr)                                                                                                                                                                                 |
| a03 1                              | 4250238721 | P1  | threat-row-runtime-inputs                                | `fixed:f5f980f9` (the standard library only; the amended row)                                                                                                                                                               |
| a03 1                              | 4250238729 | P1  | yaml-duplicate-keys                                      | `fixed:f5f980f9` (`object_pairs_hook` refuses a duplicate key)                                                                                                                                                              |

`7581d590` (fix round 1, held local under the 01:12Z PING) is in the branch history; amendment 1 keeps its two fixes in the JSON form. The main-checkout copy names the shas and adds the Bot rounds on the amendment's head. The worker resolves no thread.

## Declared beyond the letter of the task

- `tests/fixtures/gate-evidence/.prettierrc`, above.
- The 20-character minimum on an `audit_findings` reason, carried over from the `AUDIT_DISPOSITIONS` rule it replaces.
- A ledger `id` read as a JSON number or a string.
- `AUDIT_DISPOSITIONS` announced as retired rather than refused.
- README 1094 and 1104 still show `; evidence=<command>` from a01 (the same section as 1101).
- The test harness: `setUp` commits one mistake record into each test repository's base, and `write_record` writes fixtures or field sets at the current HEAD.

## For the orchestrator

- This PR's own integration is the gate's first run under the contract. `.orchestration/acceptance/dotfiles-T128-gate-evidence-a03.md` starts with a JSON block containing:
  - `"format": 1`, `"task": "dotfiles-T128-gate-evidence-a03"`, `"head": "<the audited head>"` and `"pr": 329`;
  - the `ledger` as `{"id", "class"}` objects;
  - a `searches` entry, with the gate's own search result, for every class at three (acceptance-dispositions, search-command-scan, acceptance-record-binding);
  - `audit_findings` if the audit is `incorrect`.

  It also needs `; evidence=<command>`, once, on every `not-applicable` in #329's sweep JSON. The file is under `.orchestration/`, so prettier leaves the block alone.

- The old forms remain outside `allowed_files`: SKILL step 10.4 (`AUDIT_DISPOSITIONS`, no `ACCEPTANCE_EVIDENCE`), SKILL lines 167, 169 to 171 and 210, `home/dot_config/claude/rules/pr-integration.md:4`, the `scripts/pr-feedback.py` docstring and `AGENTS.md:44`. They are `dotfiles-T128-playbook-rules-a04`'s, and PR #328 merges first.
- `origin/main` is at `ce0af5d0`, and `git merge-tree` merges it cleanly (validation §9). The diff counts 14 files outside `.orchestration/` (the cap is 15): ten under `tests/fixtures/gate-evidence/` (nine fixtures and `.prettierrc`) plus the gate, its tests, the Makefile and the README. `gh pr update-branch` is the orchestrator's effect.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt: the tree is clean, and the task asks for none.
- CompactionDB (main checkout): `7f2f0c0b…`, `f939c61c…`, `43f0ce26…`, `e74368c4…`, `00b54b12…`, and the amendment-1 decision (validation §10), which supersedes the YAML record format of `00b54b12…`.
- The main-checkout copy adds the final head, CI and the Bot wait.

## Final head, CI and the Bot (main-checkout copy)

- Final head: `82e86e50057d25493a06943c8c8e65a7b217e54a` (the evidence commit for the code head `f5f980f9`). No `update-branch` merge head exists yet: the PR head is `82e86e50`, and `origin/main` (`ce0af5d0`) merges cleanly.
- CI: 12 of 12 check runs green on `c36fcd35` and on `82e86e50` (validation §11).
- Bot (validation §12):
  - a03 round 1, review 5493539294 on `c36fcd35`: three P1, answered by amendment 1 (`f5f980f9`, after `7581d590`), see the thread table.
  - a03 round 2, review 5498081103 on `82e86e50` (02:24:39Z): one P1, below.
- Bot rounds under a03: two. Fix rounds: one (`7581d590`), plus amendment 1. Questions: one (PONG 782, 01:0xZ). No a03 RESULT before this one, so no INV-6 Bot-P1 head is counted yet.
- The Bot wait listed the comments of round 2 in the second the review was submitted and printed none. The re-listing in validation §12 shows 4254092805.

| Thread     | P   | Class                     | State and proposal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------- | --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4254092805 | P1  | ledger-completeness (new) | `open:4254092805`. Real: S6 counts only the classes in the record's own `ledger`, and nothing requires the ledger to list the swept findings. A record that omits rows (or has `ledger: []`) keeps every class under three and skips the search. A completeness rule is task text (which sweep items are findings, how review-body findings are keyed, the audit's N), so it is yours. Proposed rule: every sweep item from the Codex Bot that carries a `P0`–`P3` badge has its thread id (the `discussion_r<id>` of its url, or `review-<id>` for a review-body finding) as a ledger `id`, and every `audit:<sha7>:<n>` of the task-level audit of HEAD is one; `check=tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance`. |

## Precision notes (main-checkout copy)

- Validation §5's broader pattern `yaml|"uv"|…` counts 1 on the gate. The match is the file name `home/dot_agents/agent-config.yaml` in `HIGH_RISK_FILES`, not an import. The precise command finds nothing: no PyYAML import, no `"uv"`, no `["grep"` (validation §13).
- The records search skips symlinked files (`not path.is_symlink()`). Whether `Path.rglob` descends into a symlinked directory depends on the Python version (it does not from 3.13).
- A record or mistake file that is not UTF-8 makes `read_text()` raise. The gate then exits non-zero with a traceback, which fails closed and is not a bypass.

## RESULT

`AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a03 status=ready_for_review pr=329 head=82e86e50057d25493a06943c8c8e65a7b217e54a bot_rounds=2 fix_rounds=1 open:4254092805 …` (the dispatched line names the five main-checkout paths, the dispositions and the memory ids).

cost: n/a
