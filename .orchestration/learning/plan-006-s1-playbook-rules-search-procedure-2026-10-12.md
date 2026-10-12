# STOP S1 record: class `search-procedure` reached three on the T703 artifact (PR #328 lineage a01 → a02), 2026-10-12 13:24Z

- **The three rows:** 4247933574 (Bot P2 on a01 head `9b2c02a1`, 12:20Z: the corrections grep misses `bookkeeping` and matches every record for `sources`; M-20261012-15); the worker's second question on a01 amendment 1 (12:37Z: `grep -l` on a directory exits 2 under plain grep, the `classes:` fields not on `main`; M-20261012-16); 4248319926 (Bot P2 on a02 head `375bae0f`, 13:04Z: still no `classes:` field in the PR tree, whose base `683384ea` predates boundary #330).
- **S6 search, pasted (13:24Z):**

```text
$ /usr/bin/grep -rl 'classes:.*search-procedure' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-15.md .orchestration/learning/mistakes/M-20261012-16.md 
$ grep -A1 -E '^  - id: M-20261012-1[56]$' .orchestration/learning/index.yaml | grep corrections
 corrections: [C-17]; corrections: [C-18];
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search search-procedure | wc -l
1
```

- **Matching corrections and their state:** C-17 (classes-keyed search; the `classes:` fields are on `main` since #330 at 12:48Z, the SKILL sentence is this PR's item 3) and C-18 (prescribed commands replayed with the executor's binary at `origin/main`; a02's premises were replayed that way by the review seat). Both `pending` as mechanisms until this PR and T718 land, so "a pending correction lands first" means: this PR lands with its tree updated to `main` (`gh pr update-branch`), which is exactly what the third row asks for.
- **Re-examination of the work itself:** the three rows share one cause, a search written before its data existed and tested in the wrong environment; the rule text is now right (`grep -rl`, keyed on `classes:`), the data is on `main`, and the remaining gap is the PR tree's age. No fourth round of the same thing: the next action is the update-branch, after which the Bot's own replay finds the fields (18 records).
- **What continues and what stops:** a02 continues under amendment 1 (a different class, `trigger-threshold`) and the update-branch; a fourth `search-procedure` row on this artifact, or any second class at three, is the second S1 cycle on T703 and stops for the operator (plan 007 S7).
