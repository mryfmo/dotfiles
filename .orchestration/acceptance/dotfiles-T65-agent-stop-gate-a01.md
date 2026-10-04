# Acceptance: dotfiles-T65-agent-stop-gate-a01

- **Decision:** ACCEPTED after six revise rounds. PR #237 squash-merged to `main` as `06875e4e` (final head `fd8aa360d0b1b5f942603f4a1588b5a02fcc361f`; substantive commits e11659ac, 13340185, 5a9f35f5, 775a527a, 8433a01b, a62fce9d, ea112e2e, a9a85ecf, 4dfceb6e, cb3ded43, bc636cb7, 1845139e, 3568b7e2, 8262be37, 92cad328, fd8aa360; base c6de5156, update-branch merges through `8922f13b`). Merged without `--delete-branch`; worker-e holds `feat/agent-stop-gate`.
- **Worker:** `claude-standard-dot-a007` (worker-e). task_rev chain from the dispatch through round 6 (`88744dc8…` round 5, `d5844f02…` round-4 addendum, `051ac01e…` round 4, round 6 revision) all matched. Parallel wave with T88/T68 (a006) and T75/T91/T74 (a005).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 1, dotfiles-T65 (principle 2: a seat cannot idle with work pending).

## What was accepted (3 files: `scripts/agent-stop-gate.sh`, `tests/unit/test_agent_stop_gate.py`, `.claude/settings.json`)

- Project-level Stop hook. The seat is classified from `CLAUDE_PROJECT_DIR` by Git layout (git-dir equals common-dir for the main worktree; a linked worktree under `<main>/.claude/worktrees/` whose main owns the same common dir for a worker) after unsetting every repository override and injected configuration (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`, object dirs, `GIT_CEILING_DIRECTORIES`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`).
- Orchestrator seat: blocks on uncommitted changes outside `.orchestration/` and `.agents/worklog/` (paths shell-quoted; renames checked on both endpoints; a failing `git status` blocks) unless `stop_hook_active`, and on every `AGMSG-RESULT` addressed to it without a later `AGMSG-ACCEPTANCE` or `AGMSG-TASK` from it to the same peer for that task_id, regardless of `stop_hook_active`.
- Worker seat: blocks on every `AGMSG-TASK` or `ACCEPTANCE status=revise` addressed to it without a later `AGMSG-RESULT` or `PONG status=blocked` to the dispatching peer, or a non-revise `ACCEPTANCE` from that peer.
- History is read through agmsg's storage facade without re-initializing the store (schema revision preflight, `AGMSG_BUSY_TIMEOUT=1000`); all reads share one 3 s budget inside the 5 s hook timeout via `timeout`, `gtimeout`, or a bash watchdog (private mktemp file, exit 143 → 124); a spent budget, an unreadable store or a failing identity lookup blocks. Without an agmsg install the hook passes.
- 35 gate tests; every new test fails against the script it fixes (worker validation).

## Decisions taken during the rounds

- Round 1-2: per-task_id tracking, full history through the facade, PONG `alive` is not completion, revise reopens, both rename endpoints, fail closed on lookup failure, `jq` parsing (Codex P1/P2 threads).
- Round 3: inherited `GIT_DIR`/`GIT_WORK_TREE` ignored; any non-revise ACCEPTANCE addressed to the worker closes its task (withdrawal path); missing store stays "no messages" (not-applicable, agmsg's own semantics).
- Round 4: peer correlation (P1), all Git overrides including `GIT_INDEX_FILE` (the round-3 "keep it" was the orchestrator's error), `--separate-git-dir` layouts, `gtimeout`; addendum: coreutils is not in the Brewfile, so a bash watchdog replaces the uncapped fallback.
- Round 5: injected Git configuration cleared (the test uses `core.excludesFile`, since `--untracked-files=all` overrides `status.showUntrackedFiles`).
- Round 6: the header states exactly what the hook writes; the report's "no shellcheck disable" claim corrected (SC1091 is intended).
- Waived: the ≤150-line target (final 245 lines; every line past 150 came from the six review rounds). Not-applicable: protocol-version validation (v1 is the only contract; senders are authenticated peers), bounding `git status`/`identities.sh`, quoting the operator's own project path, failing closed on unreadable Git metadata, escaping task ids (jq `@tsv` escapes control characters), keeping merge-directed workers pending.

## Orchestrator re-derivation

- Read the final script end to end and every round's diff; confirmed the peer-correlation awk transitions, the override unset list, the layout-based seat test, and the watchdog's 143 → 124 mapping against the auditor's reproduction notes.
- Reporting defect found and corrected: the round-3 RESULT claimed no Bot response on cb3ded43 while reviews existed at 02:21Z and 02:46Z (unpaginated listings); six threads were undispositioned. Round 4 corrected the procedure (paginated listings, every thread named).
- Pre-merge: the `dot-claude-sandbox-T13-a01` closure had been sent to a005 although its RESULT came from a003; under peer correlation only an ACCEPTANCE to a003 closes it, so it was re-sent to a003 with `send.sh --force` (a003 has left the team). The worker's live check then showed the orchestrator seat clean of historical items.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head fd8aa360 | correct |
| task-level, 92cad328 | incorrect (4) → 2 corrected in fd8aa360, 2 not-applicable/waived |
| per-commit e11659ac, a62fce9d, ea112e2e, a9a85ecf, cb3ded43, bc636cb7, 1845139e | incorrect, each fixed by a later commit in the PR |
| per-commit 13340185, 5a9f35f5, 775a527a, 8433a01b, 4dfceb6e, 3568b7e2, 8262be37 | correct |

- audit-finding: 1 (92cad328) protocol version ignored → not-applicable:v1 is the only protocol contract and senders are authenticated team members; the gate is a completion check, not a message validator (same as Bot thread 4176012060)
- audit-finding: 2 (92cad328) "never writes" claim → corrected in fd8aa360 (header names the watchdog's private mktemp file)
- audit-finding: 3 (92cad328) 243 lines against ≤150 → not-applicable:the orchestrator waives the line target; every line past 150 came from the six review rounds it required
- audit-finding: 4 (92cad328) report claimed no shellcheck disable → corrected in the report (SC1091 is intended for the runtime-resolved facade path)
- Codex Bot: reviews on every push; 31 threads in total, 23 fixed in-PR and the rest not-applicable with recorded reasons, all replied and resolved by the orchestrator; "no major issues" on 92cad328 and fd8aa360. Sweep (head fd8aa360): 180 items, 0 failure/warning, all dispositioned. Gate at fd8aa360 exit 0 with evidence copies, copies removed.

## Consequences and follow-ups

- The gate is live on `main` from this merge: the orchestrator seat cannot end a turn with a RESULT awaiting acceptance, and a worker seat cannot end one with a TASK unanswered. Audit waits now happen inside the orchestrator's turn.
- `scripts/check-regime-boundary.sh` still resolves the main checkout with `${common%/.git}` (parity gap for a `--separate-git-dir` layout); candidate for T77 or a small follow-up.
- NUL bytes in an artifact make `read_scannable_text()` skip the whole file (found by the T91 audit); the validator should fail on NUL in `.orchestration` text rather than skip. Follow-up task candidate.

## CompactionDB

- Worker decision (round 0) cited; the orchestrator adds the acceptance decision below.

## Post-merge incident (2026-10-04 05:40Z)

- With the hook live, the orchestrator's Stop was blocked on 19 "uncommitted changes" that do not exist outside the sandbox (`.zshrc`, `.bashrc`, `.claude/agents`, `.mcp.json`, …). Inside the Claude Code sandbox these are 0-byte 0444 bind-mounted placeholders for protected paths, and the Stop hook runs inside that mount namespace, so `git status --untracked-files=all` lists them. Not caught before merge because the review probes ran unsandboxed (`dangerouslyDisableSandbox`) or saw the placeholders only as `ugrep` permission warnings.
- Follow-up dispatched as `dotfiles-T92-stop-gate-sandbox-placeholders-a01` to a007: skip untracked entries that are mount points in the hook's own namespace.
- Lesson for the SKILL (T69/T83): probe a hook from the sandbox too, because hooks may run there.
