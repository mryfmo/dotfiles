# Acceptance: dotfiles-T95-sandbox-placeholder-files-on-disk-a01

- **Decision:** ACCEPTED. PR #252 squash-merged to `main` as `6de95167`; final head `b9beca207c2674b73dbd5f8a5633b2fc4cbc3bc5` (substantive commits d0515ddd, 5cac2493; update-branch merge b9beca20 onto febd0cb7). Merged without `--delete-branch`; worker-c holds `fix/sandbox-placeholder-ignores`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev matched. Dispatched after its T93 RESULT; T93 round 1 ran on the same seat afterwards.
- **Exemption declared:** acceptance and final integration; the orchestrator's `.git/info/exclude` entries and the deletion of the 19 host-persisted placeholder files in the main checkout were control-plane hygiene recorded in the T65 and T92 records.
- **Plan reference:** T92 follow-up (stop gate and the Claude Code sandbox), outside the numbered phases.

## What was accepted (`.gitignore`, one header sentence in `scripts/agent-stop-gate.sh`, `tests/unit/test_gitignore_sandbox_placeholders.py`)

- The 19 paths the Claude Code sandbox leaves behind as empty read-only files at the repository root are ignored, root-anchored, in their file form only (`!/<path>/` re-includes a real directory of each name); `.claude/settings.json` and `.claude/settings.local.json` stay visible. The gate header says host-persisted placeholders are handled by `.gitignore`. The test runs `git check-ignore` for every path and asserts the settings file is not ignored.
- Worker observation (item 4): worker-c never holds host placeholders (inside its sandbox they are read-only `/dev/null` binds); a removed main-checkout `.ripgreprc` reappeared at 09:53Z without a sandboxed command in worker-c, which is consistent with the orchestrator's sandbox creating its targets in its own cwd.

## Orchestrator re-derivation

- Read the ignore list against the 19 names observed on disk on 2026-10-04 (identical set); confirmed the directory re-include pattern and the settings exclusion; CI green on b9beca20 after one snapcraft HTTP 408 rerun; Bot thumbs-up; mergeable CLEAN after the two threads.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head b9beca20 | incorrect (2) → dispositions below |

audit-finding: 1 the worker deleted a 0-byte `.ripgreprc` in the main checkout for its item-4 experiment, outside its worktree and allowed files → not-applicable:recorded as a worker scope deviation with no repository effect, since the file was a host-persisted sandbox placeholder already removed and excluded by the orchestrator earlier the same day and is reproduced by the sandbox on demand; the worker is told that observations never justify touching the main checkout
audit-finding: 2 validation runs labelled verbatim omit the unittest tracebacks, setup commands, the formatter check and the HTTP 408 rerun output → not-applicable:evidence-only finding with no code defect; CI, Bot and mergeable state are re-derived from the sweep JSON and the orchestrator ran `git check-ignore` itself; the worker pastes the raw outputs as an artifact correction that does not move the head

- Codex Bot: two threads, one fixed in 5cac2493, one not-applicable (a real root `.mcp.json` would be hidden; `git add -f` for a deliberate file), both replied and resolved. Sweep (head b9beca20): 12 items, 0 failure/warning, all dispositioned. Gate at b9beca20 with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed.

## Follow-ups

- The orchestrator removed its now-redundant `.git/info/exclude` lines after the merge.
- Why the sandbox persists its mount targets on the host (observed only in the orchestrator's cwd) is an upstream Claude Code question; no task.

## CompactionDB

- Worker decision `672e4763-0e0b-4613-beed-1a9f1457a606`; cited.
