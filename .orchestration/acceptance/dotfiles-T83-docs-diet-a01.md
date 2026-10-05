# Acceptance: dotfiles-T83-docs-diet-a01

- **Decision:** ACCEPTED. PR #274 squash-merged to `main` as `61806f56`; final head `914c765c` (round 1). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two dispositions below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 04:27Z). Round 1 was dispatched 03:39Z because the Codex Bot reviewed the update-branch head d61b7c94 at 03:35:10Z, after the worker's diff-head wait, with two valid P2 findings; two lessons were folded in. Round-0 content had no defect of its own.
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev `b9933a4e…` matched at dispatch.
- **Exemption declared:** acceptance and final integration (thread replies/resolutions, sweep, audit, gate, merge).
- **Plan reference:** Phase 6, dotfiles-T83 (principle 6). Depends on T69, T77, T78, T81, T82, T86 (all merged).

## What is under acceptance (PR #274, final head `914c765c`; round-0 commits 216f6a31, 8694a97e, 4a2b1073; update-branch merge d61b7c94; round-1 commits b6431a67, 914c765c; 16 files)

- `rules/agmsg-orchestration.md`: nine invariant bullets, each pointing at the SKILL section holding the procedure; 429 words at the final head (≤ 450). The eight always-loaded rules total 1394 words (≤ 1800; orchestrator `wc -w` at 914c765c agrees). "Codex worker" removed from rule and SKILL.
- Round 1 (b6431a67, 914c765c): `uv run --no-project .claude/hooks/contextdb_cli.py …` in CLAUDE.md (12 lines), SKILL, compactiondb rule and Codex AGENTS.md, with the test forbidding both `python3` and bare `uv run` forms; the Delegation bullet carries the operator opt-out; the Permissions bullet defers to Worker Playbook step 4's gated exceptions; SKILL masking commands use `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets` (the validator is mode 100644), counted by a new test; Worker Playbook step 2 adds the `git worktree remove`-only lesson.
- Single sources: audit command (pair and headless forms) once in the SKILL's task-level audit bullet; gate command once in SKILL step 10.4; the pr-integration rule, Codex mirror, gh-first-workflow and README point to "Orchestrator Playbook step 10".
- Session lessons moved into the SKILL (WebFetch for VERIFY, in-sandbox fetch/ff, CI → sweep → audit after update-branch, Bot wait on the diff head only, Codex-seat artifact transfer with `-worker-` infix, `audit-finding:` parser format, "deferral is not a disposition").
- Stop checklist gains the CompactionDB `memory candidates`/`memory promote` review; README gains the operator-phase definition (T70) and a `codex-orchestrate` pointer.
- `python3 .claude/hooks/contextdb_cli.py` → `uv run …` in CLAUDE.md (shim preserved), SKILL, compactiondb rule, Codex AGENTS.md.
- Dead prose: plans/005 Phase 1 retired with a dated note (#260); `.gitignore` `.agents/runs/` **kept** (Bot P1: historical run artifacts may hold raw prompts and agent output) — orchestrator agrees with the deviation; Nix plans **kept** (moving them needs `tests/unit/test_aws_cli_acquisition.py:382-399`, outside `allowed_files`) — agreed, follow-up below.
- Tests: `test_agmsg_orchestration_docs.py` rewritten (invariants, SKILL mechanics, single-source counts, forbidden phrases incl. "Codex worker" and `audit review --commit`, both word budgets); `test_pr_feedback.py` parity test; 33 subtests fail against the origin/main docs (validation).

## Bot threads (orchestrator replies and resolutions)

| thread | finding | disposition |
|---|---|---|
| 4180392652 (P1, `.gitignore`) | removing `.agents/runs/` exposes historical run artifacts | `fixed:8694a97e` (line kept with a comment) |
| 4180392654 (P2, Codex AGENTS pointer) | renamed SKILL heading orphaned the pointer | `fixed:8694a97e` |
| 4180392658 (P2, rule) | "code files run serially" contradicted the SKILL | `fixed:8694a97e` |
| 4180392661 (P2, Stop checklist) | bare `memory promote` | `fixed:8694a97e` |
| 4180432881 (P2, plans/005) | retirement note claimed the ignore rule was removed | `fixed:4a2b1073` |
| 4180550064 (P2, `compactiondb.md`, on d61b7c94) | `uv run` syncs a target project's environment | `fixed:b6431a67` |
| 4180550068 (P2, rule Delegation bullet, on d61b7c94) | operator opt-out missing from the direct-mutation exception | `fixed:b6431a67` |
| 4180598121 (P2, rule Permissions bullet, on b6431a67) | invariant omitted the gated worker exceptions of Worker Playbook step 4 | `fixed:914c765c` |
| 4180598128 (P2, SKILL step 10, on b6431a67) | direct `scripts/validate-agent-assets.py` cannot run (mode 100644) | `fixed:914c765c` |
| 4180598124 (P2, CLAUDE.md, on b6431a67) | `compactiondb-install` regenerates the block from the vendor snippet, which still says `python3` | `not-applicable`: the snippet is outside T83's allowed_files and is updated with identical wording in PR #275 (T81b PONG decision 4) |

All ten threads replied to and resolved by the orchestrator after verifying each fix commit in the diff. No Bot review on the final head 914c765c after the worker's 15-minute wait (04:02–04:17Z).

## Incidents and follow-ups

- Worker incident: `git worktree prune` from the sandboxed seat tried to delete two stale admin dirs (`worker-b`, `env-converge-T10`), both failed "resource busy"; the worker then ran read-only `git worktree list`/`ls` outside the sandbox (a boundary deviation, audit finding 1). Orchestrator re-derivation 04:25Z: five live worktrees registered and intact; both stale dirs held only a 0-byte `commondir` placeholder and an empty 2026-10-02 `config.worktree`, no `gitdir`; `git worktree prune --dry-run -v` listed exactly those two; pruned by the orchestrator from the main checkout (machine-hygiene exemption). Lesson codified in round 1 (SKILL Worker Playbook step 2).
- Local `make validate-agent-assets` fails in worker-c because `validate_no_removed_claude_skill` rglobs the gitignored CompactionDB ledger; the tree is clean (CI `validate` and a clean checkout pass). Follow-up: validator skips `.claude/contextdb/state/**` (fold into T98).
- Follow-ups: vendor `snippets/CLAUDE_CONTEXTDB.md` and `recovery.py` wording (T81b PONG decision 4); Nix plans → `docs/history/` together with the AWS CLI test (new task).

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 914c765c | incorrect (2) → both about the worker's `git worktree prune` incident, not the diff; dispositions below |

audit-finding: 1 the worker's sandboxed `git worktree prune` and its unsandboxed host diagnostics exceeded the documented worker exceptions and the own-worktree boundary → not-applicable:the breach is a process incident the worker disclosed itself, not a defect of the changeset; the corrective rule ("remove scratch worktrees with `git worktree remove` only; never run `git worktree prune` from a sandboxed seat") is part of this head (Worker Playbook step 2, pinned by `test_skill_carries_the_session_lessons`), the worker's follow-up inspection was read-only, and the orchestrator records the deviation here as a worker-conduct finding rather than re-opening a round that cannot change what already happened
audit-finding: 2 the report's "no live state lost" claim has no pasted prune output or directory inspection in the validation file → not-applicable:the orchestrator re-derived the claim independently outside the sandbox on 2026-10-05 04:25Z: `git worktree list` shows the main checkout and the five live worktrees (orchestrator-review f8e22ba3, worker-c 914c765c, worker-d 9ff2ad52, worker-e 634cb327, worker-sec 10dfc10b) all registered; `.git/worktrees/worker-b` and `.git/worktrees/env-converge-T10` contained only a 0-byte read-only `commondir` placeholder and an empty `config.worktree` dated 2026-10-02 with no `gitdir` file, so both were dead entries whose worktree directories were already gone before the incident, and `git worktree prune --dry-run -v` named exactly those two ("gitdir file does not exist"); the orchestrator then pruned them from the main checkout under the machine-hygiene exemption (output in this record's incident section); the claim is therefore true, and the missing evidence is a reporting omission already captured in the worker's learning file ("paste the incident evidence")

- Sweep (head 914c765c): `.orchestration/validation/dotfiles-T83-docs-diet-a01-pr-feedback.json`, 39 items: 9 × `fixed:` (8694a97e ×4, 4a2b1073, b6431a67 ×2, 914c765c ×2), 30 × `not-applicable` (orchestrator reply comments, 14 Codex review containers, the vendor-snippet thread, CodeRabbit summary and status, 3 macOS capacity notices).
- Crit evidence `…-crit.json` (one resolved review-scope record) and receipt `…-review-receipt.md`.

## CompactionDB

- Worker decision `0f90d8a9` (main checkout, by a005). Orchestrator consolidation `7831342b-65b6-4d4a-b8e2-fe3485b2a78a`.
