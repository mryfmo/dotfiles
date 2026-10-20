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
- **Order:** §1 and §2 ran on the working tree before the a02 commit, whose code is identical to the final head's. §3 and §4 are measured at the final head, named `HEAD` in their commands so they can be re-run there. Because this file is one of the files counted, the blocks were re-pasted and re-measured until the pasted numbers equal the head that contains them (the a02 revise of 07:56Z). The RESULT gives the final head's hash and its GitHub Actions results.

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

## 3. Caps from the branch point, at the final head HEAD, over tests/ and the five a02 files
```console
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD -- tests .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02; (the same, summed)
6	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/learning.md
31	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/report.md
23	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/sandbox.md
76	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md
70	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/validation.md
6	5	tests/unit/test_regime_ci.py
a02 records: 206 added lines
under tests/: 11 of 12
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD -- . ':(exclude)tests' ':(exclude).orchestration' | wc -l
0
(0 files: 0 changed lines outside tests/ and .orchestration/)
[exit 0]
```

## 4. Nothing but the five a02 files changed since cd47e1b0 apart from the merge of main
```console
$ git diff --stat cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 HEAD -- tests .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01 .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02; git diff --quiet cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 HEAD -- tests .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01 && echo "implementation and a01 records unchanged"; git diff --name-only cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 HEAD -- . ':(exclude).orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02' ':(exclude).orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01' | sed -n 1,3p
 .../learning.md                                    |  6 ++
 .../report.md                                      | 31 +++++++++
 .../sandbox.md                                     | 23 +++++++
 .../task.md                                        | 76 ++++++++++++++++++++++
 .../validation.md                                  | 70 ++++++++++++++++++++
 5 files changed, 206 insertions(+)
implementation and a01 records unchanged
(the other changed paths come from the merge of main; the first three:)
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
.orchestration/tasks/dotfiles-T133-loop-limits-a01.md
[exit 0]
```
