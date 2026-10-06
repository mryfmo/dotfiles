# Acceptance: dotfiles-T108-one-login-per-machine-a01

- **Decision:** ACCEPTED. PR #293 squash-merged to `main` as `c467314e` (2026-10-06 05:34Z) with `gh pr merge --squash --match-head-commit f0a5407a…`; head `f0a5407a` (round 1). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main PR_FEEDBACK_EVIDENCE=… AUDIT_EVIDENCE=…-audit-f0a5407.md AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` rc=0, 05:33Z; the role-gate notice is gone with the role gate). Earlier: REVISE ROUND 1 dispatched 05:05Z (round-0 audit: merge procedure needs `--match-head-commit`; sandbox record wording). RESULT received 04:58Z (head `b66f4297`).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev verified at dispatch (03:57Z) and at PONG decision 1.
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping.
- **Design source:** `.orchestration/validation/github-auth-design-2026-10-05.md` §14–§16 (operator decision A, 2026-10-06: every seat on a machine acts as that machine's single GitHub account; the T90/T102/T103 role separation is removed; `main` is protected by actor-independent rulesets, native denial of merge commands in worker seats, and the integration gate). Supersedes T107 (cancelled, PR #292 closed unmerged).
- **PONG decisions:** 1 (SKILL, agmsg-orchestration rule and docs test added for the two-account passages; merge procedure is `gh pr merge --squash` everywhere; the Codex execpolicy PUT/graphql ban binding a Codex orchestrator accepted).

## What is under acceptance (PR #293, head `b66f4297`; 24 files, +431/−1331)

- `herdr-agents`: worker panes inherit the machine's gh login (the `GH_CONFIG_DIR` injection, token unsetting, Codex `shell_environment_policy` override and the T102 notice removed; `spawn.sh` called directly).
- Gate: the GitHub role check removed (`github_identity_errors`, ruleset probes, approval requirement).
- Manifest/renderer: the three store keys and `*_GH_CONFIG_DIR` rendering removed.
- `scripts/gh-auth.sh` (replaces `gh-auth-stores.sh`): skip when `gh auth status` succeeds, else device-code login with gh's default storage, tty-only, token env cleared, mise shims on PATH; `make gh-auth` and `setup.sh` follow.
- Doctor: one-login finding; `check-tools.sh` identity comparison removed.
- Codex execpolicy: `gh api -X|--method PUT` and `gh api graphql` forbidden (prefix limits documented in the rule comment).
- SKILL/rule/README: one account per machine; merge with `gh pr merge --squash`; what protects `main`; the two-account passages and the `encrypted_private_hosts.yml` sentence removed.
- Tests: T90/T102/T103 tests removed or inverted; new single-login, doctor and execpolicy tests; 911 unit tests OK; CI green (16 checks) after one fix for a test that reached the runner's real `gh`.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, b66f4297 (round-0 head) | incorrect (2) → P2 the merge procedure lost the head binding the REST `sha=` carried; fix: `gh pr merge --squash --match-head-commit <audited head>` in SKILL, rule and README (+ docs test); P3 the sandbox record's "no command ran gh against the real configuration" contradicts the recorded authenticated gh use (artifact fix) → revise round 1; the auditor confirmed the allowlist, artifacts, 15 successful checks and ran the execpolicy tests, shellcheck and syntax checks |
| task-level, f0a5407a (round-1 head) | correct (no findings; the auditor confirmed the amended allowlist, the artifacts, the single-login flow, launcher cleanup, role-gate removal, the execpolicy rules, the head-bound merge instruction, 15 successful checks, and ran 19 tests, shellcheck and syntax checks) |

- Sweep (head f0a5407a, re-run after the round-1 push; the same 8 items): `.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-pr-feedback.json`, 8 items, all `not-applicable` (Codex quota notice; Codex review summary, security review completed with no findings; CodeRabbit summary comment and status; 4 macOS capacity notices). Bot coverage: Codex security review, no findings; no review threads. Crit evidence `…-crit.json` / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md`.

## Deploy

- `make update` in the canonical clone at c467314e (05:35Z): rc=0, no prompt. Deployed state on this host: `~/.codex/rules/default.rules` carries the two new `gh api` forbidden rules; `~/.agents/model-profiles.env` has no `*_GH_CONFIG_DIR`; `~/.local/bin/common/herdr-agents` has no worker gh-config plumbing; `make doctor`: WARN: GitHub login: gh holds 2 working of 2 logins; keep exactly one (gh auth logout --user <login> for any other, or run make gh-auth) Doctor summary: tools=passed; runtime=passed
- Worker panes seated from now on inherit this machine's gh login (`moriya-fumio-thd`); the pre-deploy seat a005 was already on it.

## Follow-ups recorded by the worker

- Claude worker seats have no native merge denial yet (permission prompt only) until the planned worker-worktree `settings.local.json` deny task (T109, Codex seat). Codex-seat keyring access under gh's default storage is unverified. Possible stale `fix/gh-stores-per-machine` tracking entries in worker-c's `.git/config`.

## CompactionDB

- Worker decision `8b5d314b-2b89-4602-a318-66dad566ba8a` (main checkout, by a005). Orchestrator consolidation `e22327ad-684b-4cc8-8278-1783e7e6805e`.
