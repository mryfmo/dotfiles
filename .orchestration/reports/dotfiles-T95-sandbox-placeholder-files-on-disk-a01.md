# Report: dotfiles-T95-sandbox-placeholder-files-on-disk-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `fix/sandbox-placeholder-ignores` from `origin/main` f2b5c115. `fix/gate-masked-feedback-bodies` (T93) is untouched.
- **task_rev:** `sha256:29acc4dc…2d65`, matched.
- **PR:** #252, https://github.com/mryfmo/dotfiles/pull/252.
- **Commits:**
  - `d0515ddd`: the change.
  - `5cac2493`: Codex P2 4177021586; only the file form is ignored.
  - `b9beca20`: `gh pr update-branch`, merging `main` febd0cb7 (#243).
- **Final head:** `b9beca20`. CI, branch and bot state are in the validation file.
- **Status:** ready_for_review.

## 1. What changed

- **`.gitignore`:** ignores the 19 paths, root-anchored (`/<path>`), with a comment naming the cause. Each path is followed by `!/<path>/`, which re-includes a real directory of that name. Only the empty placeholder file is ignored, and a genuine `.claude/agents/` (or `.idea/`, `.vscode/`, `.claude/skills/`, …) and its contents stay visible to `git status` and the stop gate. This is the Codex P2 fix.
  - `.claude/settings.json` and `.claude/settings.local.json` are not ignored.
  - None of the 19 paths is tracked (`git ls-files` per path).
- **`scripts/agent-stop-gate.sh`:** two header comment lines say that host-persisted placeholders are plain empty files, not mounts, and that `.gitignore` hides them. The mount logic is untouched.
- **`tests/unit/test_gitignore_sandbox_placeholders.py`** (4 tests) copies the tracked `.gitignore` into a fresh `git init` repository with `core.excludesFile=/dev/null`. The main checkout's `.git/info/exclude` already lists the 19 paths (the orchestrator's stopgap) and worktrees share it, so a check against the real repository would pass even without this change. The four checks:
  - each path is ignored at the root but not under `home/`;
  - real 0444 empty files at all 19 paths leave `git status` clean;
  - a real directory's file is listed;
  - both settings files are not ignored.
  - With `origin/main`'s `.gitignore` there are 20 failures; with `d0515ddd`'s there are 19 (the directory case).

## 2. Item 4: do the placeholders reappear on disk after a sandboxed command? (verbatim in the validation file)

- **In worker-c: no.** On the host, `.zshrc` is absent before (09:47:48Z) and after (09:47:54Z) a sandboxed command. Inside the sandbox at 09:47:50Z it is a character device 1,3 (`/dev/null`) on a read-only bind mount (`findmnt`). The host scan found none of the 19 in worker-c at 09:47:54Z or 09:57:01Z.
- **The main checkout held all 19 as host files:** 0-byte, mode 0444, all with mtime 09:47:35Z. That was roughly 10 s after the orchestrator dispatched this task at 09:47:25Z, and about when my own first sandboxed command ran, a `cd` into the main checkout to hash the task file.
- **Controlled check:**
  - I removed only the main checkout's `.ripgreprc` placeholder at 09:48:30Z, after confirming it was 0 bytes and untracked.
  - A sandboxed no-op from worker-c (09:48:35Z) did not recreate it, and neither did a sandboxed no-op that `cd`s into the main checkout (09:48:43Z).
  - It reappeared at 09:53:21Z while my sandboxed `make unit-test` / `validate-agent-assets` run was in progress; the orchestrator's session may also have been active. I cannot attribute that event.
- **Conclusion:** a plain sandboxed command of this worker session does not create or recreate the host files, in its worktree or in the main checkout. Something else intermittently creates them in the main checkout: another session whose cwd is the main checkout, or a longer command. The `.gitignore` handles them either way.

I left the recreated `.ripgreprc` as found; it is ignored locally by `.git/info/exclude` and, after merge, by `.gitignore`.

## 3. Codex bot and threads

| Head | Result |
|---|---|
| `d0515ddd` | P2 4177021586, "Keep real project agent directories visible": `fixed:5cac2493`. Each path gains a `!/<path>/` directory re-include, and the test proves a real directory's contents stay listed. |
| `5cac2493` | P2 4177037406, "Keep real root MCP configs visible": proposed `not-applicable` (see below). |
| `b9beca20` (final, `gh pr update-branch` merge of main febd0cb7) | 👍 at 10:10:28Z, with no new comment. |

Proposed `not-applicable` for 4177037406. A `.gitignore` pattern cannot tell a 0-byte placeholder from a real file by content, so any ignore-based fix hides a real untracked root file at these 19 paths. The task chose `.gitignore` explicitly so every clone behaves the same, and it forbids the alternative the bot suggests (detecting verified placeholders in the stop gate's mount logic). That alternative would also leave plain `git status` noisy in every clone. The impact is bounded:
- none of the 19 paths is tracked;
- this repository keeps its real agent and MCP configuration under `home/` (chezmoi source), not at the root;
- a deliberately added root file needs `git add -f`, after which it is tracked and visible.

The orchestrator can accept that ceiling or re-task a content-aware gate check.

I did not reply to or resolve any thread.

## 4. Notes

- **CI flake on the merge head.** On the first run, `public-bootstrap (ubuntu-24.04, client)` failed in `.chezmoiscripts/ubuntu/50-client-install-misc.sh`: `snap` got HTTP 408 from api.snapcraft.io. The macOS and server bootstrap jobs were then cancelled by fail-fast. I re-ran the failed jobs with `gh run rerun 37194377536 --failed`; the result is in the validation file's final CI section.
- **Ceiling (from the P2 fix):** a real file at one of these root paths, for example a committed `.mcp.json` or `.gitmodules`, is ignored while untracked, so `git add` needs `-f`. Tracked files are unaffected. All 19 are untracked today.
- I touched no `.claude/settings.json`, no gate mount logic and no `.git/info/exclude`.

## CompactionDB

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T95 (orchestrator 2026-10-04): the Claude Code sandbox'"'"'s placeholder targets that persist on disk at the repository root are ignored through `.gitignore`, so neither `git status` nor the stop gate reports them.'
672e4763-0e0b-4613-beed-1a9f1457a606
[exit 0]
```

[memory:decision] dotfiles-T95 (orchestrator 2026-10-04): the Claude Code sandbox's placeholder targets that persist on disk at the repository root are ignored through `.gitignore`, so neither `git status` nor the stop gate reports them.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md`
- learning: `.orchestration/learning/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
