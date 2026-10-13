# Report: dotfiles-T128-gate-evidence-a03

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329. a03 is a02's reset under plan 011 option F (reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a02-design-reset.md`), continued from the worker's head `61d90302` (merge head `4e2266aa`).
- Task file: sha256 `686806a1…` checked against the TASK (15:41:03Z) and copied byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a03/task.md`. a01's and a02's copies stay unchanged as history (validation §1).
- Commits: a01's `7f763b7f`, `9a860c95`, `5971fffe`; a02's `379845f7`, `386a71b3`, `c81c88a3`, `d5d6c9b1`, `c6cf0548`, `61d90302`; a03's `b2b3db45` (the record contract, the task copy; first made as `3c67f512` on `61d90302` and replayed onto the merge head `4e2266aa` with the same content outside `.orchestration`, validation §9), `c36fcd35` (evidence), `7581d590` (fix round 1), then this evidence.

## What the PR does (task steps 1 to 5)

1. A disposition is `fixed:<commit>` (unchanged; a `fullmatch` of `fixed:[0-9a-f]{7,40}`) or `not-applicable:<reason>; evidence=<command>`. `parse_disposition` splits once on the literal `; evidence=` with `str.partition` and checks that both parts are non-empty. A text with more than one delimiter is refused, so a second delimiter can neither empty the reason nor pad a failure-level reason past the 20-character minimum. The work is linear: a one-million-character malformed disposition is refused in well under 0.5 s (thread 4249544794; validation §3). `;evidence=` without the space is no delimiter, because the task names the literal. The error text is unchanged: `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`.
2. The acceptance-record contract. `ACCEPTANCE_EVIDENCE` is required whenever `BASE` is set and is checked right after the PR-feedback evidence:
   - `orchestration_path_error(..., "acceptance")`, then the a02 binding: the file is `<task>.md` for the task named by `<task>-pr-feedback.json`, by name and by resolved name;
   - the record starts with a YAML front matter between `---` lines, split with the idiom of `validate-agent-assets.py`'s `read_frontmatter` (`startswith("---\n")`, `find("\n---", 4)`) and loaded by a `yaml.SafeLoader` subclass. It is `safe_load`'s loader plus one rule: a duplicate mapping key is refused, where `safe_load` would keep the last one silently (a03 Bot round 1, thread 4250238729). The prose after it is not read: no regex is applied to prose anywhere (`test_acceptance_record_prose_is_not_read`);
   - `format` is the int 1, and `task` equals the file's task id;
   - `head` equals the full `HEAD` sha the gate runs at (computed also without `BASE`), else `acceptance record head <x> is not HEAD <y>` (thread 4249544762);
   - `pr` is a positive int, equal to the `pr` of `PR_FEEDBACK_EVIDENCE` when it is set, else `pr must be <n>, the pull request PR_FEEDBACK_EVIDENCE names, not <m>` (a03 Bot round 1, thread 4250238714);
   - `ledger` is a list of exactly `{id, class}`. `id` is a thread id (10 or more digits) or `audit:<sha7>:<n>`, accepted as an int or a string, because YAML reads an unquoted thread id as an int. `class` matches `[a-z0-9-]+`;
   - `searches` is a list of exactly `{class, records}`, where `records` is a list of strings; a class named twice is refused;
   - for each class at three or more ledger rows, the gate runs `grep -rl 'classes:.*<class>' .orchestration/learning/mistakes/` from the repository root, as an argument list without a shell, and requires that class's `records` to equal the basenames it found as a set (`records: []` when it finds none). Otherwise `S6: class <slug> at <n> without a matching records search`. A grep exit other than 0 or 1 is refused, and the class regex makes the slug safe as one argument;
   - `audit_findings`, when present, is a list of exactly `{n, reason, evidence}`, where `n` is an int of at least 1 and `reason` and `evidence` are non-empty strings. An entry with `fixed` is refused with "a fix moves HEAD, so audit the new head instead". The 20-character minimum on an audit reason is carried over from `AUDIT_DISPOSITIONS` (declared). When the audit verdict is `incorrect`, the entries must cover findings 1..N once each. A `reason` that quotes `not-applicable:` is just a field (thread 4249544748; `acceptance-finding-quotes-grammar.md`);
   - the record is not counted when sizing the diff (a02, thread 4248232998).

   `AUDIT_DISPOSITIONS` is retired: the gate no longer reads it. When it is still set, the gate prints one line saying so instead of refusing, because the SKILL names it until `dotfiles-T128-playbook-rules-a04` lands. The recipe's comment in `Makefile` names `audit_findings` in its place; README 427 to 428 and 1101 already name `ACCEPTANCE_EVIDENCE` and never named `AUDIT_DISPOSITIONS`.
3. Tests and fixtures (below). The module runs 83 tests, against 71 on `origin/main` (validation §2, §3). Each rule fails a test when broken: one-line mutations M2 to M19, plus the guards of `origin/main`, of a02's head `61d90302` and of a03's first code head `b2b3db45` (validation §4).
4. `make require-crit-review` without `BASE` on a records-only tree prints the same line and exit status at the a03 code head as at `origin/main` (validation §6). No record is set there, so no `uv` runs.
5. Nothing else changes in the gate.

### How the gate gets PyYAML (a runtime input; declared)

The gate runs as `./scripts/require-crit-review.py` through `/usr/bin/env python3`. That interpreter has no PyYAML on this host, and CI's `make unit-test` is a bare `uv run python` with no project (validation §5), so `import yaml` would fail in both places. The record's front matter is therefore loaded by `uv run --no-config --no-project --quiet --with pyyaml python -I -c <yaml.safe_load to JSON>`:

- it is the uv cache first (`--offline`), then the network, the pattern of `scripts/check-regime-boundary.sh`;
- the front matter goes in on stdin, `cwd` is a temporary directory, and each run has a 120-second timeout that is refused when it expires;
- `-I` and the temporary cwd keep a PR-planted `yaml.py` off `sys.path`, and `--no-config` ignores a PR-planted `uv.toml`. The closing test plants both, and the record still loads while the planted module never runs (validation §3, §4 M15);
- a YAML error is reported as data with exit 0, so only a `uv` or interpreter failure retries online.

This is a runtime interpreter and network input, not a file. It sits under the threat-table row "workflow and interpreter or environment inputs" ("none in allowed_files"). The orchestrator may want that row to name it.

## Fixtures and the tests that read them

| Fixture | Read by |
|---|---|
| `tests/fixtures/gate-evidence/pr-feedback-wrong.json` | `test_dispositions_of_2026_10_12_without_evidence_are_refused` |
| `tests/fixtures/gate-evidence/pr-feedback-right.json` | `test_dispositions_with_an_evidence_command_are_accepted` |
| `tests/fixtures/gate-evidence/acceptance-stale-head.md` | `test_acceptance_record_head_must_be_head`, `test_base_requires_an_acceptance_record_under_acceptance` (`head`) |
| `tests/fixtures/gate-evidence/acceptance-s6-missing.md` | `test_s6_class_at_three_without_a_searches_entry_is_refused`, `test_base_requires_an_acceptance_record_under_acceptance` (S6) |
| `tests/fixtures/gate-evidence/acceptance-s6-present.md` | `test_s6_class_at_three_with_the_matching_searches_entry_is_accepted`, `test_acceptance_record_prose_is_not_read`, the planted-file case, and every other `guard_base` run as the default passing record |
| `tests/fixtures/gate-evidence/acceptance-finding-quotes-grammar.md` | `test_audit_finding_reason_may_quote_the_grammar` (an `incorrect` audit with one finding) |

The six fixtures total 70 lines (validation §5); `head: HEAD` in a fixture is replaced with the test repository's HEAD by `write_record`. The wrong fixture's two dispositions are, byte for byte, the `disposition` fields of items 4244248692 and 4244378809 in `.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json`. The right fixture extends each with `; evidence=<command>`, the command that refutes the claim (validation §5). The present fixture's `records: [M-20261012-3.md]` is what the real tree's search returns. The test repositories' base commit carries one mistake record of that name.

New and rewritten tests:

- `test_base_requires_an_acceptance_record_under_acceptance`, the threat row's closing test. It covers:
  - the path: empty, outside `.orchestration/acceptance/`, another task's record, a symlink alias, the task's own record missing;
  - one case per front-matter rule: no front matter, unloadable YAML, a list instead of a mapping, `format`, `task`, `head`, `pr`, a ledger `id`, a ledger `class`, `searches` records, a class searched twice, an `audit_findings` entry citing a fix, S6;
  - the planted `yaml.py` and `uv.toml`.
- `test_acceptance_record_head_must_be_head`, `test_acceptance_record_prose_is_not_read`, `test_audit_finding_reason_may_quote_the_grammar`, `test_disposition_parsing_is_linear`, and `test_retired_audit_dispositions_is_not_read`.
- `test_s6_searches_entry_must_equal_the_recomputed_records_search` accepts the matching set, and `[]` where nothing matches. It refuses a record missing, a record too many, another class's entry and a pasted command for its records, and refuses grep exit 2 once the records directory is gone.
- `test_incorrect_audit_needs_audit_findings` (from `test_incorrect_audit_needs_not_applicable_dispositions`): no `audit_findings`, a fix, a short reason, no evidence, empty evidence, one missing, the same finding twice, out of range, and accepted.
- `test_s6_class_at_three_without_a_searches_entry_is_refused` and `test_s6_class_at_three_with_the_matching_searches_entry_is_accepted`.
- `audit_guard` writes the record at the audited head; its `findings` become `audit_findings`. `guard_base` keeps the real uv cache (`UV_CACHE_DIR`) under its fake `HOME`, as `test_check_regime_boundary.py` does.

## Bot threads (before a03)

| Thread | P | Class | Disposition |
|---|---|---|---|
| 4248232955 | P1 | skill-command-sync | proposed `not-applicable:owned by dotfiles-T128-playbook-rules-a04 item 6, and PR #328 merges before #329; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` (validation §5) |
| 4248232964 | P1 | acceptance-record-binding | `fixed:379845f7` |
| 4248232976 | P1 | threat-row-missing | `fixed:379845f7` (the row is in the a03 task copy, closed by the test above) |
| 4248232988 | P1 | acceptance-dispositions | `fixed:b2b3db45` (the record's `audit_findings`; no `audit-finding:` lines are read) |
| 4248232998 | P2 | evidence-diff-sizing | `fixed:379845f7` |
| 4248233012 | P1 | search-command-scan | `fixed:c6cf0548` (recomputed search; a03 moves it into `searches`) |
| 4248697658 | P1 | search-command-scan | `fixed:c6cf0548` |
| 4248697668 | P1 | acceptance-dispositions | `fixed:b2b3db45` (prose list items are not read; `audit_findings` is a field) |
| 4248934816 | P1 | disposition-delimiter | `fixed:c6cf0548`, kept by a03's single split |
| 4248934830 | P1 | search-command-scan | `fixed:c6cf0548` |
| 4249544748 | P1 | acceptance-dispositions | `fixed:b2b3db45` (fields, not substrings) |
| 4249544762 | P1 | acceptance-record-binding | `fixed:b2b3db45` (`head` equals HEAD) |
| 4249544794 | P2 | regex-backtracking | `fixed:b2b3db45` (one split, linear checks) |

The main-checkout copy adds the Bot rounds on the a03 head. The worker resolves no thread.

## a03 Bot round 1 (review 5493539294 on `c36fcd35`, 16:28:30Z): three P1

| Thread | P | Class | Disposition |
|---|---|---|---|
| 4250238714 | P1 | acceptance-record-binding (third on this artifact, after 4248232964 and 4249544762: an S1 candidate) | `fixed:7581d590` (the record's `pr` equals the swept PR's) |
| 4250238729 | P1 | yaml-duplicate-keys (new) | `fixed:7581d590` (the loader refuses a duplicate key, at any depth) |
| 4250238721 | P1 | threat-row-runtime-inputs (new) | the orchestrator's: the row "workflow and interpreter or environment inputs" reads `residual: none in allowed_files`, but the gate now runs `uv` (PyYAML from the cache, else the network) and `grep`. Live evidence from this session: the uv cache was pruned overnight, and the gate could not load any record offline until PyYAML was fetched again (validation §5). The task text needs a row for availability and provenance (an unpinned `pyyaml`), and for resolving the `uv` and `grep` executables. |

CI on `c36fcd35`: 12 of 12 check runs green. The question PONG (01:3xZ) proposed pushing the two fixes by default.

## Declared beyond the letter of the task

- The PyYAML subprocess and its hardening, above.
- The 20-character minimum on an `audit_findings` reason, carried over from the `AUDIT_DISPOSITIONS` rule it replaces.
- A ledger `id` read as an int or a string.
- `AUDIT_DISPOSITIONS` announced as retired rather than refused.
- README 1094 and 1104 still show `; evidence=<command>` from a01 (the same section as 1101).
- The test harness: `setUp` commits one mistake record into each test repository's base, and `write_record` writes fixtures or field sets at the current HEAD.

## For the orchestrator

- This PR's own integration is the gate's first run under the contract. `.orchestration/acceptance/dotfiles-T128-gate-evidence-a03.md` (the name the binding demands, from `dotfiles-T128-gate-evidence-a03-pr-feedback.json`) needs a front matter with:
  - `format: 1`, `task: dotfiles-T128-gate-evidence-a03`, `head: <the audited head>` and `pr: 329`;
  - the `ledger` as `{id, class}` rows;
  - a `searches` entry, with the gate's own `grep -rl` result, for every class at three (acceptance-dispositions, search-command-scan);
  - `audit_findings` if the audit is `incorrect`.

  It also needs `; evidence=<command>`, once, on every `not-applicable` in #329's sweep JSON. The gate spawns `uv` for the record, which uses the uv cache or the network.
- The old forms remain outside `allowed_files`: SKILL step 10.4 (`AUDIT_DISPOSITIONS`, no `ACCEPTANCE_EVIDENCE`), SKILL lines 167, 169 to 171 and 210, `home/dot_config/claude/rules/pr-integration.md:4`, the `scripts/pr-feedback.py` docstring and `AGENTS.md:44` (`AUDIT_DISPOSITIONS`, forbidden to edit here). They are `dotfiles-T128-playbook-rules-a04`'s, and PR #328 merges first.
- `origin/main` is at `3709a6d8` (boundary commits up to #333). They touch none of this PR's files, and `git merge-tree` merges cleanly (validation §9). `gh pr update-branch` is the orchestrator's effect.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt: the tree is clean, and the task asks for none.
- CompactionDB (main checkout): `7f2f0c0b…`, `f939c61c…`, `43f0ce26…`, `e74368c4…` under a01 and a02, and the a03 decision (validation §10), which supersedes the record format of the earlier ones.
- The main-checkout copy adds the final head, CI and the Bot wait.

cost: n/a
