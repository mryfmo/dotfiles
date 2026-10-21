---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01
seat: claude-standard-dot-a009
kind: review
design_sha256: 0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380
verdict: accept
---

# Review: the redesign dotfiles-T133-trusted-exec-contract-tests-a02 (INV-6 reset anchor of a01, PR #436)

Read-only, from this worktree inside the sandbox. The subject is the main checkout's `.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md`; the record is `.orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md`. The task copy of this review is the dispatched file, sha256 `861ccdec…`.

## Hash

```console
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md
0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md
```

It equals the expected `0b1923a6…`. The file is not yet on `origin/main` `f7f38067`.

## Items

1. **The hash: ok.** As above.
2. **Front matter, History, Item 1, threat table, Check, and no widening: ok, with three advisory notes below.**
   - **Front matter:** `reset_of: [dotfiles-T133-trusted-exec-contract-tests-a01]` (a02:4). `retained_predecessor_directories: [.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/]` (a02:15–16).
   - **History** (a02:86), checked against the record:
     - **The first two RESULTs are recorded:** round 1 at 01:48:10Z and `revise=1` at 03:27:48Z.
     - **The PR was audited twice:** `…-audit-9545e59.md` and `…-audit-a561e64.md`, both incorrect.
     - **Amendment 1 fixed the orchestration P2:** that is `audit:a561e64:3` (unhashed-text-change), fixed by amendment 1.
     - **The two P3 are fixed:** `audit:a561e64:4` by the records commit, and `:5` by the sweep row `issuecomment-6281175171`.
     - **The two advisory P2 stay with their owner:** `:1` and `:2` remain owned by followup-a01.
     - **The commits match:** `612f75f5` is a commit whose parent is `a561e640` (`git rev-parse 612f75f5^`), titled "amendment 1 task copy and literal validation commands". PR #436's live head is `9cc6c96ba32027a6378951f878f84e83a00eda25` (`gh pr view 436`).
     - Not re-measured here: the `S2: revises 2 >= 2` line, which the History attributes to `make check-regime-boundary` at 14:01Z.
   - **Item 1** (a02:131–143) is records-only:
     - It commits only the a02 task copy; `report.md` and the RESULT record stay uncommitted.
     - The three frozen files and their hashes match `612f75f5` exactly: `tests/unit/trusted_exec_contract.py` `86409898…`, `tests/unit/test_trusted_exec_contract.py` `bab55334…`, and the a01 task copy `f9f09083…`, each via `git show 612f75f5:<path> | shasum -a 256`.
     - `git diff --stat 612f75f5 9cc6c96b -- tests` is empty, so the code is unchanged.
     - The Check requires `git diff --stat 612f75f5..HEAD` to show only the copy (a02:191).
   - **Threat table:** every a01 control is kept with its disposition unchanged (a set comparison of the controls, plus a diff of the rows: only additions). It adds the two copy rows: the predecessor copy (`reset_of`) at a02:19–20, and the a02 task copy at a02:21–22.
   - **Check:** it names `612f75f57748df9962f7c5dc768ed23c37666842` as the measurement base (a02:191, :203).
   - **No widening:**
     - `allowed_files` is a01's two test modules plus the task's own evidence directory. a01's directory moves to `retained_predecessor_directories`, for retention and not edits (a02:20).
     - `security: false`, as in a01.
     - Worker Playbook step 4 applies with no exception for gh, push, directory-service commands, messaging, publication or memory writes (a02:113–115).
     - No production, settings, hook, permission, workflow, pin or dependency file is touched (a02:96).
3. **Read only: ok.** This review changed no tracked file and dispatched nothing. Its only output is this uncommitted file in this worktree, with no commit, PR or push.

## Advisory notes (P3, non-blocking)

- **The allowlist count:** a02:30 ("the four-entry a02 allowlist") and a02:205 ("exactly the four declared allowed_files entries") say four, while the front matter declares three (a02:11–13), and a02:41 says "three allowed_files entries". The a01 text's own size sentence said four as well, so this is an inherited wording slip. It widens nothing, because the front matter decides.
- **A third added row:** the threat table also adds an `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a02/**` row (a02:29–30), the directory row that pairs with a01's. Beyond the two copy rows the item names, it is the per-`allowed_files`-entry row the threat-table rule expects.
- **The third RESULT is not yet in the record:** the History's records-only amendment-1 round at `612f75f5` appears only as the anticipated sha in the amendment-1 disposition (record: "the commit sha is written here at its RESULT"). The record does not contradict the History; the orchestrator may add that line.

## Verdict

`verdict: accept`.
