---
task_id: dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01
seat: claude-standard-dot-a009
kind: review
design_sha256: 661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4
verdict: accept
---

# Review: the redesign dotfiles-T133-worker-cap-hookspath-a02 (INV-6 reset anchor of a01)

Read-only, from this worktree inside the sandbox. The subject is the main checkout's `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md`; the record is `.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md`. The task copy of this review is the dispatched file, sha256 `ff1e91c3…`.

## Hash

```console
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md
661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md
$ git show origin/main:.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md | shasum -a 256
661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4  -
```

Both equal the expected `661c44fd…`.

## Items

1. **The hash: ok.** As above.
2. **`reset_of`, the findings, and no widening: ok.**
   - **`reset_of`:** the front matter has `reset_of: [dotfiles-T133-worker-cap-hookspath-a01]` (a02:13). `format`, `kind: code`, `security: true` and `after: []` are as in a01.
   - **The findings that forced the reset** (the record's "Audit of c96697ae" section):
     - **Audit finding 1 (P1, orchestration):** amendments after S2, and no independent redesign. a02 is a redesign by a Codex review-profile context other than a01's author (a02:68, :127). It keeps a01's history stopped and its counters unrewritten, and counts every worker-side fix round toward INV-6 under C-61 (a02:70, :112).
     - **Audit finding 2 (P2, herdr-agents:1832):** the lock path assumed a `.git` directory. Item 6 derives the lock from `git -C "${workdir}" rev-parse --path-format=absolute --git-common-dir`, never from a literal `${workdir}/.git`. Its test `test_add_worker_uses_git_common_dir_for_the_seat_lock` uses a real `git init --separate-git-dir` checkout, is red on `c96697ae` and green after the fix (a02:90).
     - **Audit finding 3 (P2):** advisory row `4305808095` was wrongly dispositioned to `is_main_checkout`. Item 7 assigns it to a02 through item 6. The predecessor owner withdraws its item, and the record correction stays orchestrator-side with a read-only record check (a02:92).
     - **Audit finding 4 (P2):** the stale PR #408 description. Item 8 puts the final scope in `report.md` and issues no `gh pr edit`, API or browser edit under the live ask rule. The acceptance record acknowledges the stale description and the condition for correcting it, with a red-then-green evidence assertion (a02:94, :118, :120).
   - **The carried rows:**
     - `4305767690` (race-unserialized-count) is item 2's one exclusive lock through registration, with item 5's concurrency test (a02:82, :88).
     - `4305767694` (threat-row-missing) is the full threat table (a02:14–44).
     - `4305769826` (unbound-evidence) is item 4: no Git configuration write, and `test_add_worker_writes_no_git_configuration` red on `982eeee0` (a02:86, :88).
     - `4305808095` is item 6.
   - **No widening of permissions or trust boundaries:**
     - `allowed_files` is a01's four code, test and doc files plus the task's own evidence directory.
     - Among a02's added lines there is no new exclusion, sandbox, permission, bypass or ask-rule term.
     - a02 removes a01's superseded `extensions.worktreeConfig`, `config --worktree` and `core.hooksPath` Git configuration writes (a01:79; a02:76, :86), which narrows the boundary.
     - "Permission or hook defaults" stay out of scope (a02:98).
     - The live launcher changes only at the operator's `make update` (a02:120).
3. **Read only: ok.** This review changed no tracked file and dispatched nothing. Its only output is this uncommitted file in this worktree, with no commit, PR or push.

## Verdict

`verdict: accept`.

Scope of this judgment: whether the redesign's front matter, its coverage of the reset findings and carried rows, and its permission surface meet items 1 to 3. It is not the final-head task-level audit or security review that a02:116 assigns to the orchestrator.
