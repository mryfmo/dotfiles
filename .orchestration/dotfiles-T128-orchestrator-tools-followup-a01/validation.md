---
task_id: dotfiles-T128-orchestrator-tools-followup-a01
seat: claude-standard-dot-a003
commit: d414e86c
---

# Validation: dotfiles-T128-orchestrator-tools-followup-a01

## 1. Task copy, premises and base

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md
ae208befe121d754018f311d42c0be996942264e5348b34440dd9c88c522d910  .orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md
(rc=0)
$ git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md | shasum -a 256
ae208befe121d754018f311d42c0be996942264e5348b34440dd9c88c522d910  -
(rc=0)
$ cmp <(git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md) .orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md && echo identical
identical
(rc=0)
$ git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md && echo present
present
(rc=0)
$ git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md && echo present
present
(rc=0)
$ git merge-base HEAD origin/main; git rev-parse --short origin/main
727180dbc33f50b8934c2f2ed229d1c6a744ce0d
04590ae9
(rc=0)
```

- **The task copy** hashes to the TASK's `task_sha256`, `ae208bef…`, and is byte-identical to `origin/main`'s task file. It holds no home path.
- **Both premises replay** as `present`.
- **The base** is `727180db`, boundary (15).

## 2. The owned rows

Item 1 reads the section `## Owned by dotfiles-T128-orchestrator-tools-followup-a01` of the a02 acceptance record from `origin/main`. The section is the last one in the file, so it runs from line 17 to the end. A row is a line of exactly two tab-separated fields whose first field has no space, the record's own `id<TAB>class` grammar:

```text
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md | shasum -a 256
942e02b42b4129f82fc6555eb70168237b1ae478ae4528ea21900b53a1f06da3  -
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md | /usr/bin/grep -n '^## '
17:## Owned by dotfiles-T128-orchestrator-tools-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md | sed -n '17,$p' | awk -F'\t' 'NF == 2 && $1 !~ / / {n++; print n": "$0} END {print "rows=" n}'
1: local:9ad0c15:3	advisory-p2
2: local:9ad0c15:4	advisory-p2
3: 4260535916	deleted-path-handling
4: 4260535924	deleted-path-handling
5: local:7b574d3:1	advisory-p2
6: audit:7b574d3:1	trust-boundary-dispositions
7: audit:7b574d3:2	trust-boundary-dispositions
8: audit:7b574d3:3	stale-evidence
9: audit:7b574d3:4	deleted-path-handling
10: audit:7b574d3:5	deleted-path-handling
11: audit:7b574d3:6	search-procedure
12: audit:7b574d3:7	evidence-claim
13: local:8576645:1	advisory-p2
14: local:8576645:2	advisory-p2
15: audit:8576645:2	disposition-key
16: local:046901b:1	advisory-after-last-round
17: local:046901b:2	advisory-after-last-round
18: audit:046901b:1	trust-boundary-dispositions
19: audit:046901b:2	disposition-key
20: local:f48593d:2	advisory-p2
21: audit:6847aa9:1	path-shim-discovery
22: audit:a235637:1	trap-restores-on-refusal
rows=22
(rc=0)
```

The section holds 22 rows; boundary (15), `727180db`, added the last three (`local:f48593d:2`, `audit:6847aa9:1`, `audit:a235637:1`; the `git log -S` lines above). The TASK note says 23 after boundary (15); no line under the heading matches the grammar beyond these 22, so this task works on the 22 and leaves the count to the orchestrator.

## 3. What each row names

The local reviews and the audits, as `origin/main` holds them (the row id `<source>:<head>:<n>` is the n-th finding of that file):

```text
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-local-review-9ad0c15.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P1] Do not auto-dismiss all CI failures — scripts/orchestrator/fill_sweep.py:23-24
- [P1] Require hashes for tab-delimited TASK messages — scripts/orchestrator/dispatch.sh:80-80
- [P2] Handle deleted orchestration files in boundary PRs — scripts/orchestrator/boundary.sh:41-44
- [P2] Preserve deleted files when fast-forwarding — scripts/orchestrator/ff-main.sh:35-38
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-local-review-7b574d3.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P2] Preserve deletions in boundary commits — scripts/orchestrator/boundary.sh:41-44
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-8576645.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P2] Handle deleted orchestration files when building the boundary PR — scripts/orchestrator/boundary.sh:41-44
- [P2] Preserve locally deleted files during fast-forward — scripts/orchestrator/ff-main.sh:35-38
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-046901b.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P1] Handle deleted orchestration files in boundary commits — scripts/orchestrator/boundary.sh:41-44
- [P1] Preserve locally deleted tracked files during fast-forward — scripts/orchestrator/ff-main.sh:35-37
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-f48593d.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P1] Align the gate invocation with the declared trust-boundary control — scripts/orchestrator/orch-gate.sh:66-67
- [P2] Restore the review worktree when setup fails — scripts/orchestrator/orch-gate.sh:55-59
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-audit-7b574d3.md.last.md | /usr/bin/grep -nE '^(- )?\[P[0-3]\]' | cut -c1-230
3:- [P1] high implementation `scripts/orchestrator/fill_sweep.py:60` — Review bodies and issue comments receive automatic `not-applicable` dispositions regardless of their findings. An in-memory replay with an actual P1 badge conf
4:- [P1] high implementation `scripts/orchestrator/fill_sweep.py:49` — Any account except the Codex bot can supply a disposition through a thread reply. A reply from an untrusted contributor successfully dismissed a P1 finding in 
5:- [P1] high implementation `scripts/orchestrator/orch-audit.sh:72` — Cleanup removes receipts from the main checkout, while Codex writes into the review checkout, where line 62 can copy the previous receipt. A rerun exiting zero
6:- [P2] high implementation `scripts/orchestrator/boundary.sh:44` — A tracked deletion reaches unconditional `cp`, which fails before the boundary commit. This known advisory remains present and assigned to the follow-up task.
7:- [P2] high implementation `scripts/orchestrator/ff-main.sh:37` — A locally deleted tracked file reaches unconditional `mv`, aborting the fast-forward and potentially leaving previously moved files aside. This known advisory rem
8:- [P2] high orchestration `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md:9` — The recorded revise has no pasted counter output or required records search, although lines 11–15 contain three `input-validation`
9:- [P2] high evidence `.orchestration/reports/dotfiles-T128-orchestrator-tools-a02.md:82` — The report claims CompactionDB identifiers here and at line 107, but neither identifier appears in validation output, and the executed co
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-8576645.md.last.md | /usr/bin/grep -nE '^(- )?\[P[0-3]\]' | cut -c1-230
3:- [P1] high implementation `scripts/orchestrator/dispatch.sh:80` — Newly accepted tab-separated or repeated-space prefixes are sent unchanged, but `regime-counters.sh:115` parses literal spaces. An in-memory reproduction showed 
4:- [P2] high implementation `scripts/orchestrator/fill_sweep.py:68` — Dispositions are keyed only by URL. `pr-feedback.py` gives every annotation in one check run the same URL. Reproduction confirmed that one TSV entry marks two 
5:- [P2] high orchestration `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:31` — The successor record contains no counter output or required repeat-finding searches, despite three `input-validation`, four `dele
6:- [P2] high evidence `.orchestration/reports/dotfiles-T128-orchestrator-tools-a05.md:74` — The claimed CompactionDB memory identifier has neither its executed command nor corresponding output in validation. The consolidation cla
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-046901b.md.last.md | /usr/bin/grep -nE '^(- )?\[P[0-3]\]' | cut -c1-230
3:- [P1] high implementation `scripts/orchestrator/fill_sweep.py:67` — A badge-free GitHub review with `level=changes_requested` is automatically dispositioned as “review object without a finding.” Memory-only reproduction confirm
4:- [P2] high implementation `scripts/orchestrator/fill_sweep.py:68` — Dispositions use the URL as their key, but annotations within one check run share a URL. Reproduction confirmed one TSV row marks two distinct findings as fixe
5:- [P2] high orchestration `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:44` — The annotation-collision finding is assigned to the follow-up, but that task’s item 1 reads exclusively the **a02** acceptance re
6:- [P2] high orchestration `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:52` — The counter evidence is truncated, still reports one RESULT before the latest revise RESULT, and leaves Bot/audit counts `unknown
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-audit-6847aa9.md.last.md | /usr/bin/grep -nE '^(- )?\[P[0-3]\]' | cut -c1-230
1:[P1] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md:41 — **The prescribed PATH still permits PR-selected code.** `orch-gate.sh:72` preserves the caller’s PATH; on this host, `gh` resolves through
3:[P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a06.md:9 — **Numeric thread IDs invalidate the counter ledger.** The three thread IDs are JSON numbers, while `scripts/regime-counters.sh:138` re
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-audit-a235637.md.last.md | /usr/bin/grep -nE '^(- )?\[P[0-3]\]' | cut -c1-230
1:[P2] high implementation scripts/orchestrator/orch-gate.sh:63 — Shims refusal does not leave the review worktree untouched: the EXIT trap unconditionally runs `checkout -qf --detach origin/main`. A clean worktree initially on an
(rc=0)
```

The two Bot threads of PR #346 (gated `gh` call 1 of sandbox.md):

```text
$ for id in 4260535916 4260535924; do gh api "repos/mryfmo/dotfiles/pulls/comments/${id}" --jq '"--- \(.id) \(.user.login) \(.path):\(.original_line // .line) commit \(.original_commit_id[0:8])\n\(.body)"'; done
--- 4260535916 chatgpt-codex-connector[bot] scripts/orchestrator/boundary.sh:44 commit 1287af34
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Preserve deletions in boundary commits**

When a tracked `.orchestration` file is deleted, `git status` includes its path in `files`, but the copy loop then runs `cp` on that nonexistent source and aborts under `set -e`. Thus the boundary tool cannot create a PR containing deletions; it needs to distinguish deleted entries and remove those paths in the new worktree rather than attempting to copy them.

AGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/1287af3435e4847ef819e43972b0da4bfe156e60/AGENTS.md#L78-L78)

Useful? React with 👍 / 👎.
--- 4260535924 chatgpt-codex-connector[bot] scripts/orchestrator/ff-main.sh:38 commit 1287af34
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Handle locally deleted files during fast-forward**

When a locally modified tracked path is a deletion, `git diff --name-only` adds it to `modified`, but this unconditional `mv` fails because the working-tree path no longer exists. The script therefore aborts before fast-forwarding, despite promising to preserve every local edit; deleted entries need an explicit representation rather than being moved like existing files.

AGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/1287af3435e4847ef819e43972b0da4bfe156e60/AGENTS.md#L78-L78)

Useful? React with 👍 / 👎.
```

## 4. The rows already fixed on `origin/main`, and the two orchestration rows

```text
$ git log --format='%h %s' -S 'BADGE = re.compile' origin/main -- scripts/orchestrator/fill_sweep.py | cut -c1-110
c586f20d feat(orchestrator): the second slice's scripts and the first slice's residual fixes (T718 a02, PR-A) 
(rc=0)
$ git log --format='%h %s' -S 'ignored-reply' origin/main -- scripts/orchestrator/fill_sweep.py | cut -c1-110
c586f20d feat(orchestrator): the second slice's scripts and the first slice's residual fixes (T718 a02, PR-A) 
(rc=0)
$ git log --format='%h %s' -S '-newer "${start}"' origin/main -- scripts/orchestrator/orch-audit.sh | cut -c1-110
c586f20d feat(orchestrator): the second slice's scripts and the first slice's residual fixes (T718 a02, PR-A) 
(rc=0)
$ git show origin/main:scripts/orchestrator/orch-audit.sh | /usr/bin/grep -nE 'out\}"\*|rm -f -- "\$\{out\}"|-newer'
60:    [[ -f ${f} && ${f} != "${out}"* ]] || continue
66:rm -f -- "${out}" "${out}.last.md" "${review}/${out}" "${review}/${out}.last.md"
71:if ((rc == 0)) && [[ -s ${review}/${out}.last.md && -n $(find "${review}/${out}.last.md" -newer "${start}") ]]; then
(rc=0)
$ git log --format='%h %s' -G '^trap ' origin/main -- scripts/orchestrator/orch-gate.sh | cut -c1-110
5ec86052 fix(orchestrator): orch-gate.sh runs the gate with a private PATH of resolved gh and git (T128 gate-w
28eec93c feat(orchestrator): acceptance-front-matter.py and orch-gate.sh (T718 a05, PR-B) (#350)
(rc=0)
$ git show 28eec93c:scripts/orchestrator/orch-gate.sh | /usr/bin/grep -nE '^trap|checkout -q --detach "\$\{head\}"'
60:trap 'git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main' EXIT
61:git -C "${review}" checkout -q --detach "${head}"
(rc=0)
$ git log --format='%h %s' -S 'mise which' origin/main -- scripts/orchestrator/orch-gate.sh | cut -c1-110
5ec86052 fix(orchestrator): orch-gate.sh runs the gate with a private PATH of resolved gh and git (T128 gate-w
(rc=0)
$ git show origin/main:tests/unit/test_orchestrator_tools.py | /usr/bin/grep -nE 'def test_(fill_sweep_leaves_a_badged|fill_sweep_ignores_a_disposition_reply|orch_audit_refuses_a_run_that_leaves|orch_gate_restores_the_review_worktree_when_setup)'
782:    def test_fill_sweep_ignores_a_disposition_reply_from_another_login(self):
828:    def test_fill_sweep_leaves_a_badged_review_body_a_gap(self):
860:    def test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt(self):
1105:    def test_orch_gate_restores_the_review_worktree_when_setup_fails(self):
(rc=0)
$ git show origin/main:tests/unit/test_orch_gate_path.py | /usr/bin/grep -nE 'def test_'
80:    def test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries(self):
96:    def test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory(self):
106:    def test_orch_gate_removes_the_private_bin_on_exit(self):
(rc=0)
$ git log --format='%h %s' -S 'class counts over this record' origin/main -- .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md | cut -c1-110
df044557 chore(orchestration): boundary commit 2026-10-13 (13): plan 020 step 5 (T703 #328 and T702 #329 merge
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md | /usr/bin/grep -nE 'regime-counters.sh dotfiles-T128-orchestrator-tools-a02|class counts over this record|grep -rl'
41:$ scripts/regime-counters.sh dotfiles-T128-orchestrator-tools-a02 --pr 346
43:$ class counts over this record's rows (non-advisory)
46:$ /usr/bin/grep -rl 'classes:.*input-validation' .orchestration/learning/mistakes/
48:$ /usr/bin/grep -rli -- 'input-validation' .orchestration/learning/mistakes/ | wc -l
(rc=0)
$ git show origin/main:.orchestration/reports/dotfiles-T128-orchestrator-tools-a02.md | /usr/bin/grep -nE '9ac653b5|b4cc3273'
82:`memory add` in the main checkout printed `9ac653b5-177d-4119-b321-4f98b0e2a802`.
107:- CompactionDB: the revise round's `memory add` in the main checkout printed `b4cc3273-c3ab-4825-a861-d97628fe909e`.
(rc=0)
$ cd "$(git rev-parse --path-format=absolute --git-common-dir)/.." && uv run --no-project .claude/hooks/contextdb_cli.py memory list --limit 2000 | /usr/bin/grep -cE '9ac653b5|b4cc3273'
contextdb: [Errno 1] Operation not permitted
0
(rc=1)
```

- **`audit:7b574d3:1`, `audit:7b574d3:2` and `audit:7b574d3:3` are fixed on `origin/main` by `c586f20d` (PR #346, a05 items 7 to 9):**
  - the badge rule leaves a badged review body or issue comment a gap, under `test_fill_sweep_leaves_a_badged_review_body_a_gap`;
  - a reply by any login other than `--orchestrator-login` is printed as `ignored-reply`, under `test_fill_sweep_ignores_a_disposition_reply_from_another_login`;
  - orch-audit.sh excludes and removes this head's audit files and requires a `.last.md` newer than the run's start, under `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt`.
- **`local:f48593d:2` is fixed by `28eec93c` (PR #350).** At that commit the trap is line 60, and the head's checkout follows it at line 61. The test is `test_orch_gate_restores_the_review_worktree_when_setup_fails`.
- **`audit:6847aa9:1` is fixed by `5ec86052` (PR #355).** The gate's PATH is a private directory of `gh` and `git` resolved by `mise which` under `env -i`. The tests are the three in `tests/unit/test_orch_gate_path.py`.
- **`audit:7b574d3:6`** names the a02 acceptance record, which is outside `allowed_files`. The counter output and the records search it asked for were pasted by `df044557`, boundary (13), at the record's lines 41 to 48.
- **`audit:7b574d3:7`** names the a02 report, which is outside `allowed_files`. The two identifiers it claims are at the report's lines 82 and 107. This seat's sandbox cannot read the main checkout's CompactionDB (`Operation not permitted`). Only `memory add` is a sanctioned out-of-sandbox case there, so no lookup was made outside the sandbox.

## 5. Tests and linters

The lineage's test module, `tests/unit/test_orchestrator_tools.py`, with the six new tests and the changed fixture's test named. Then the neighbouring modules, among them `test_orch_gate_path.py`, which also runs orch-gate.sh:

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest -v tests.unit.test_orchestrator_tools 2>&1 | /usr/bin/grep -E 'deletes_a_deleted|newline_one_path|keeps_a_local_deletion|fills_only_a_commented|shared_url_key|as_it_was_on_a_refusal|badged_review|^Ran |^OK|FAILED'
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path) ... ok
test_boundary_keeps_a_name_with_a_newline_one_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_keeps_a_name_with_a_newline_one_path) ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_a_local_deletion_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_a_commented_review (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_a_commented_review) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id) ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout) ... ok
Ran 46 tests in 30.915s
OK
(rc=0)
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_orch_gate_path tests.unit.test_regime_counters tests.unit.test_chain_github_scripts 2>&1 | tail -3
Ran 33 tests in 9.949s

OK
(rc=0)
```

```text
$ shellcheck scripts/orchestrator/boundary.sh scripts/orchestrator/ff-main.sh scripts/orchestrator/orch-gate.sh
(rc=0)
$ w="${PWD}"; cd "${TMPDIR}" && "$(command -v shfmt)" --indent 4 --space-redirects -d "${w}"/scripts/orchestrator/{boundary,ff-main,orch-gate}.sh
(rc=0)
$ uv run --no-project ruff check scripts/orchestrator/fill_sweep.py tests/unit/test_orchestrator_tools.py
All checks passed!
(rc=0)
$ uv run --no-project ruff format --check scripts/orchestrator/fill_sweep.py tests/unit/test_orchestrator_tools.py
2 files already formatted
(rc=0)
```

## 6. Mutation proofs

Each mutant is applied to the working file, the named test runs, and the file is restored byte for byte. M1, M2 and M5 are `origin/main`'s script, the defect as the rows found it; M12 and M13 undo the fix round (M13 is the first head `4b15fab0`'s boundary.sh):

```text
M1 scripts/orchestrator/boundary.sh -> test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path: killed (FAILED (failures=1))
M2 scripts/orchestrator/ff-main.sh -> test_ff_main_keeps_a_local_deletion_across_the_fast_forward: killed (FAILED (failures=1))
M3 scripts/orchestrator/fill_sweep.py -> test_fill_sweep_fills_only_a_commented_review: killed (FAILED (failures=1))
M4 scripts/orchestrator/fill_sweep.py -> test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id: killed (FAILED (failures=1))
M5 scripts/orchestrator/orch-gate.sh -> test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout: killed (FAILED (failures=1))
M6 scripts/orchestrator/boundary.sh -> test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path: killed (FAILED (failures=1))
M7 scripts/orchestrator/ff-main.sh -> test_ff_main_keeps_a_local_deletion_across_the_fast_forward: killed (FAILED (failures=1))
M8 scripts/orchestrator/fill_sweep.py -> test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id: killed (FAILED (failures=1))
M9 scripts/orchestrator/orch-gate.sh -> test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout: killed (FAILED (failures=1))
M10 scripts/orchestrator/fill_sweep.py -> test_fill_sweep_fills_only_a_commented_review: killed (FAILED (failures=1))
M11 scripts/orchestrator/boundary.sh -> test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path: killed (FAILED (failures=1))
M12 scripts/orchestrator/fill_sweep.py -> test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id: killed (FAILED (failures=1))
M13 scripts/orchestrator/boundary.sh -> test_boundary_keeps_a_name_with_a_newline_one_path: killed (FAILED (failures=1))
mutants 13/13 killed; tree restored
```

## 7. Size (INV-2)

```text
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/autoskill.md
23	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/learning.md
171	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/report.md
29	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/sandbox.md
104	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md
308	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/validation.md
26	12	scripts/orchestrator/boundary.sh
22	9	scripts/orchestrator/ff-main.sh
22	9	scripts/orchestrator/fill_sweep.py
5	3	scripts/orchestrator/orch-gate.sh
126	2	tests/unit/test_orchestrator_tools.py
(rc=0)
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '$3 !~ /^tests\// {a += $1; f++} $3 ~ /^tests\// {t += $1; f++} END {print "files outside .orchestration: " f "; added outside tests/: " a "; added under tests/: " t}'
files outside .orchestration: 5; added outside tests/: 75; added under tests/: 126
(rc=0)
```

5 files outside `.orchestration/` (cap 15), 75 added lines outside `tests/` (cap 500), 126 under `tests/` (cap 1000).

## 8. The repository validator

```text
$ UV_OFFLINE=1 uv run --no-project --with pyyaml scripts/validate-agent-assets.py 2>&1 | tail -1  # on d414e86c, before the commit
agent asset validation ok
(rc=0)
```

## 9. PR #361: the Bot's review of the first head `4b15fab0`, and the fix round `d414e86c`

PR #361 was marked ready at 2026-10-15T00:50:41Z with head `4b15fab0`. The Bot's one review came at 00:53:46Z, with two P1 inline comments and no finding in its body. CI passed on that head (every check; the main-checkout copy holds the final head's).

```text
$ scratchpad/wait-ci-bot.sh 361 4b15fab096fb00138badc0cb966804e4c2001531 <out> <ready epoch>  # bot.txt, from its first line to the issue comments
bot-wait end 2026-10-15T00:54:24Z asked=0
# reviews of the head
5526640758	4b15fab096fb00138badc0cb966804e4c2001531	2026-10-15T00:53:46Z	COMMENTED
# review bodies
--- review 5526640758 4b15fab096fb00138badc0cb966804e4c2001531

### 💡 Codex Review

Here are some automated review suggestions for this pull request.

**Reviewed commit:** `4b15fab096`
    

<details> <summary>ℹ️ About Codex in GitHub</summary>
<br/>

Codex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you
- Open a pull request for review
- Mark a draft as ready
- Comment "@codex review".

If Codex has suggestions, it will comment; otherwise it will react with 👍.




When you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".
            
</details>
# top-level review comments on the head
--- comment 4277862535 4b15fab096fb00138badc0cb966804e4c2001531 scripts/orchestrator/boundary.sh:36
**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Preserve NUL-delimited boundary paths**

When an untracked `.orchestration` filename contains a newline, converting NUL separators to newlines turns the remainder into another record, and `cut -c4-` then removes three bytes of the actual filename. For example, a nested filename whose post-newline segment is `   /tmp/x` causes `/tmp/x` to enter `copied`, after which `--mask-secrets` can rewrite that host file rather than only a boundary-worktree copy. Keep paths NUL-delimited through array iteration instead of serializing them into `files`.

AGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/4b15fab096fb00138badc0cb966804e4c2001531/AGENTS.md#L75-L78)

Useful? React with 👍 / 👎.
--- comment 4277862537 4b15fab096fb00138badc0cb966804e4c2001531 scripts/orchestrator/fill_sweep.py:80
**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Separate synthetic item IDs from URL fragments**

When a collected URL ends in `#item-N`—which a commit-status target URL can do—the synthetic index key and URL-fragment key share a namespace. An `item-0\tfixed:...` row intended for index 0 therefore also dispositions an unrelated item whose literal fragment is `item-0`; the script reports no gap, so the integration gate can accept that unrelated failure without review. Reject such collisions or give index keys a namespace that cannot be interpreted as a URL key.

AGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/4b15fab096fb00138badc0cb966804e4c2001531/AGENTS.md#L75-L78)

Useful? React with 👍 / 👎.
```

The re-check after CI shows both of the Bot's reviews completed, and no other comment:

```text
re-check 2026-10-15T01:02:00Z
# reviews of the head
5526640758	4b15fab096fb00138badc0cb966804e4c2001531	2026-10-15T00:53:46Z	COMMENTED
# top-level review comments on the head
4277862535	4b15fab096fb00138badc0cb966804e4c2001531	scripts/orchestrator/boundary.sh	36
4277862537	4b15fab096fb00138badc0cb966804e4c2001531	scripts/orchestrator/fill_sweep.py	80
# summary status
"status":"completed"
Security Review** | ✅ **Completed** <relative-time datetime="2026-10-15T00:55:44.350790Z">2026-10-15T00:55:44.350790Z</relative-time> 
```

Both P1 findings are fixed at their root in `d414e86c`, the one fix round:

- **4277862535.** boundary.sh read the NUL-delimited status through `tr '\0' '\n' | cut -c4-`, so a newline in a name split it into two records. The tail of one could then reach the masker as a path outside the repository. The entries are now read with `read -r -d ''` into an array and cut with `${entry:3}`. The copy directory is now `${f%/*}`, because `$(dirname)` would strip trailing newlines. The test is `test_boundary_keeps_a_name_with_a_newline_one_path`, which boundaries `.orchestration/d<newline>   <temp>/victim.md`; M13 (the first head's boundary.sh) dies there.
- **4277862537.** fill_sweep.py's index ids were `item-<n>`, which is also a possible URL fragment. They are now `item#<n>`. A key is the text after the URL's last `#` and so never holds one, and `item#<n>` does not start with the `#` that marks a comment line in extra.tsv. The shared-key test adds a status whose fragment is `item-0`. Rows `item#0` and `item#1` leave it a gap, and the row `item-0` fills only it. M12, the `item-<n>` namespace, dies there.
