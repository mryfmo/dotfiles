---
task_id: dotfiles-T133-regime-ci-fixture-grammar-a02
seat: claude-standard-dot-a009
reset_of: dotfiles-T133-regime-ci-fixture-grammar-a01
continued_from: cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2
code_head: 15bc046ef0bc50476879e92cfaa42e5952f6878b
base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
---

# Validation: dotfiles-T133-regime-ci-fixture-grammar-a02

- **Where:** every block ran inside the sandbox, on `tools/regime-ci-fixture-grammar-a01`, continued from `cd47e1b0`. The a01 records keep the before-and-after evidence (16/16 OK on the unmodified module and on `15bc046e`, in `.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/validation.md` §4 and §6).
- **Placeholders:** `MAIN` is the main checkout, `T` the task id, and `~` the home directory.
- **Order:** §1 and §2 ran on the working tree before the a02 commit, whose code is identical to the final head's. §3 and §4 were measured at that commit, `d9f44faa`. The commit was then amended to add only §3 and §4 to this file, which changes no number in them. The final head's GitHub Actions results are in the RESULT.

## 1. Task copy (sha256 fd9ff212…) and the task-consistency check
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
fd9ff2123d96bebdabfea725bcc7c8412b3f1275bbaac2858da143d9a0ff1303  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md
fd9ff2123d96bebdabfea725bcc7c8412b3f1275bbaac2858da143d9a0ff1303  .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md
byte-identical
$ uv run --offline --no-project --python 3.15 --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-regime-ci-fixture-grammar-a02.md: OK
[exit 0]
```

## 2. The Check: the measured module command
```console
$ /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py
................
----------------------------------------------------------------------
Ran 16 tests in 48.187s

OK
[exit 0]
```

## 3. Caps from the branch point, at d9f44faa42609e25d4b7938948aa80cb60680a16
```console
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...d9f44faa42609e25d4b7938948aa80cb60680a16
30	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-crit.json
21	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-review-receipt.md
10	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/learning.md
67	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/report.md
31	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/sandbox.md
66	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
258	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/validation.md
6	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/learning.md
30	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/report.md
23	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/sandbox.md
76	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md
36	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/validation.md
6	5	tests/unit/test_regime_ci.py
$ (the same, summed)
outside tests/ and .orchestration/: 0 of 0
under tests/: 11 of 12
[exit 0]
```

## 4. Nothing but the five a02 files changed since cd47e1b0
```console
$ git diff --stat cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 d9f44faa42609e25d4b7938948aa80cb60680a16; git diff --quiet cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 d9f44faa42609e25d4b7938948aa80cb60680a16 -- tests .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01 && echo "implementation and a01 records unchanged"
 .../learning.md                                    |  6 ++
 .../report.md                                      | 30 +++++++++
 .../sandbox.md                                     | 23 +++++++
 .../task.md                                        | 76 ++++++++++++++++++++++
 .../validation.md                                  | 36 ++++++++++
 5 files changed, 171 insertions(+)
implementation and a01 records unchanged
[exit 0]
```
