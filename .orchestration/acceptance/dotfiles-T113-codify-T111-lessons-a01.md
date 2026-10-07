# Acceptance: dotfiles-T113-codify-T111-lessons-a01

- **Decision:** ACCEPTED. PR #302 head `9311c6cb` (round 2, on the update-branch merge head `d0fa723a` over main `a5edf2b7`). Gate passed at that head in the orchestrator-review worktree with the PR-feedback, audit and crit evidence (`BASE=origin/main … make require-crit-review` rc=0). Squash-merged to `main` as `262eaabb` (2026-10-07 06:18Z) with `gh pr merge 302 --squash --match-head-commit 9311c6cb…`. Earlier: REVISE ROUND 2 dispatched 06:00Z (audit of d0fa723a: the stated guarantee was wider than the predicate; claim narrowed, predicate kept). Earlier: `gh pr update-branch 302` by the orchestrator at 05:4xZ (branch was behind a5edf2b7), then CI → sweep → audit on d0fa723a. Earlier: REVISE ROUND 1 dispatched 05:05Z (Codex Bot 4203015529 on the orchestrator's own project-map body wording; a unit test for the new boundary line). RESULT received 04:51Z (head `f0a6f42b`), round 1 at 05:28Z (`3f7c2e13`), round 2 at 06:14Z (`9311c6cb`).
- **Worker:** `claude-standard-dot-a005` (worker-c, w1A:p2), dispatched at T112's RESULT on a fresh branch (files disjoint from T112).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread replies and resolution (orchestrator-side).
- **Origin:** codifies the three T111 failures (acceptance record of T111, "Notes for the operator"): a second project-map implementation applied to the host from the canonical clone outside the regime; the orchestrator's `cd`-based checkout that moved the main checkout; a rule stated in two places that drifted. The operator asked on 2026-10-07 that the orchestrator carry this out end to end.

## What is under acceptance (PR #302, head `9311c6cb`)

- New `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`: a full `chezmoi apply` is refused when `home/`, `install/` or `scripts/` differ from the last-fetched `origin/main` (then `@{upstream}`, then HEAD), when the index has unmerged entries, or when a non-ignored untracked file exists under those trees; skipped for a non-git source, `CI=true` or `CHEZMOI_ALLOW_DIRTY_SOURCE=1`; git-ignored untracked files are declared out of scope. `Makefile` `update` fetches `origin/main` first. README documents it (user-visible change: `make update` on a tree with unmerged edits now stops at the apply instead of applying them).
- Rule (Delegation) and SKILL (canonical clone pull/apply/upgrade only; step 3 contradiction check and single statement; step 10 `git -C` and HEAD verification).
- `scripts/check-regime-boundary.sh`: `orchestrator seat is not on main: …` for a seated main checkout off `main`; two unit tests in `tests/unit/test_herdr_agents.py`; surfaced as WARN only by the validator, so CI stays green.
- `project-map`: the agent body refers to the skill in full without restating rules; the skill's Writes section forbids browsers, screenshots and other processes that write elsewhere (Amendment 1, from the first live run).

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, d0fa723a (update-branch head over round-1) | incorrect (1): P2 the README and the thread disposition claimed that only merged changes reach the host while `--exclude-standard` lets a git-ignored untracked file through → revise round 2 (claim narrowed; predicate kept by the task's design, boundary written into the task file) |
| task-level, 9311c6cb (round-2 head) | correct (no findings: all changes within the amended allowlist, artifacts present, guard / seated-checkout detection / agent body / procedure text match the amended requirements, six Bot findings dispositioned with resolved threads, the three claimed fixes match their commits) |

audit-finding: 1 (d0fa723a) `--exclude-standard` permits git-ignored files that chezmoi still applies while the README and disposition claim a merged-only guarantee → fixed:9311c6cb685b46585e2e1c52b40015ab0d0a66ea (the guard description and the README now state that git-ignored untracked files are not checked; the predicate is unchanged by design: such files never travel by pull request and including them would refuse every apply because of `__pycache__`), re-audited at 9311c6cb

- Sweep (re-run at every head; final at 9311c6cb): `.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-pr-feedback.json`, every item dispositioned: Codex Bot threads 4202957457 and 4202957466 `fixed:f0a6f42b`, 4203015529 `fixed:3f7c2e13`, 4202957461 / 4203015512 / 4203015540 `not-applicable` with pasted probes (targeted apply runs no run_ script; the guard is a rail, not an operator boundary; ignored files are out of declared scope); all six replied to and resolved by the orchestrator; Codex review headers, the orchestrator's empty reply-review objects, quota notice, CodeRabbit summary and status, macOS capacity notices `not-applicable`. Crit evidence `…-crit.json` (3 orchestrator review records) / `…-review-receipt.md`; worker-side `…-worker-crit.json` (three passes, approve) / `…-worker-review-receipt.md`.
- Accepted deviations from the task text: `origin/main` compared first (the task's purpose over its literal order); README names committed, unpushed, unmerged and not-yet-pulled trees (the original "uncommitted" would be false).

## Deploy

- `make update` in the canonical clone at `262eaabb` (2026-10-07 06:2xZ): rc=0 from a clean tree (the new guard ran and passed); `~/.claude/agents/project-map.md` is byte-identical to the source, the applied project-map skill carries the no-browser bullet, the canonical clone's `Makefile` carries the fetch line and `scripts/check-regime-boundary.sh` the seat-off-main violation. Earlier the same day (T111/T112 deploy): the canonical clone's rejected project-map draft was backed up to the orchestrator's scratchpad and reset to `origin/main`, the `claude-deep-dot` seat registered there was retired, the host's `~/.codex/map.config.toml` leftover was removed, and the project-map agent memory gained `style: light` / `accent: #14b8a6`; the first live project-map run then drew `.project-map/` without asking for a style.

## CompactionDB

- Worker decision `d4378b55-e544-453e-828d-0be5f83bf579` and failure `40af6916-6e1d-470f-aeac-f407bad83feb` (main checkout, by a005). Orchestrator consolidation `eb4bb004-fb50-48bd-885b-00b47d5fd379`.

cost: n/a
