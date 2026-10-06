# Acceptance: dotfiles-T110-gh-auth-file-storage-a01

- **Decision:** ACCEPTED. PR #297 squash-merged to `main` as `8bbe8d44` (2026-10-06 10:49Z) with `gh pr merge --squash --match-head-commit a431fd46…`; head `a431fd46` (round 3). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one artifact-only disposition below), `AUDIT_DISPOSITIONS` and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 10:46Z). Earlier: REVISE ROUND 3 dispatched 10:12Z (round-2 audit: the file check must run even when gh auth status fails). Earlier: REVISE ROUND 2 dispatched 09:40Z (round-1 audit: mode check must stat the configured hosts.yml directly; evidence pastes). Earlier: REVISE ROUND 1 dispatched 09:08Z (round-0 audit: doctor coverage with two accounts or an auth error; Bot-wait evidence; the orchestrator's stale sweep). RESULT received 08:59Z (PR #297, head `80cc3e3d`); the Bot P1 thread (comment 4193168336) was replied to (4193420593) and resolved by the orchestrator with the decision-A disposition.
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev verified at dispatch (08:05Z).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread reply and resolution (orchestrator-side).
- **Origin:** defect found by the orchestrator on 2026-10-06 while verifying decision A: T108's `gh-auth.sh` used gh's default storage, which a Linux Secret Service turns into the keyring; inside the Claude Bash sandbox the keyring-stored account failed `gh auth status` while the file-stored one worked (the sandbox denies unix sockets). Design source: `.orchestration/validation/github-auth-design-2026-10-05.md` §12, §16 (file storage is the operator's decision).

## What is under acceptance (PR #297, head `80cc3e3d`)

- `scripts/gh-auth.sh`: skips when the active login's `tokenSource` is gh's `hosts.yml` (and sets it to 0600), otherwise, on a tty, `gh auth login --insecure-storage` then `chmod 600` (failing with a message when chmod fails); the message names the reason (no login, or a keyring login the Claude sandbox cannot reach).
- Doctor: storage checked before the working count (keyring → WARN with the `make gh-auth` hint; non-0600 or unreadable file → WARN); `CLICOLOR_FORCE` stripped for plain JSON.
- README: the reason sentence restored. Tests for the script and the doctor cases.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, 80cc3e3d (round-0 head) | incorrect (3) → P2 the doctor's storage and mode checks run only with exactly one authenticated account, so a second account or an auth error hides a keyring login or a 0644 token file (fix: independent checks + tests); P2 the sweep JSON still showed the Bot thread unresolved because the sweep preceded the orchestrator's reply and resolution (orchestrator: re-sweep after the round-1 push); P3 the Bot-wait evidence shows a label and empty results (artifact fix) → revise round 1; the auditor confirmed the allowed files, artifacts, saved CI agreement, syntax/ShellCheck/whitespace checks |
| task-level, 449fa66d (round-1 head) | incorrect (2) → P2 the mode check keys on gh's `tokenSource`, so a 0644 `hosts.yml` behind a keyring-sourced active account is never stat'ed (fix: check the configured file directly + test); P3 an elided live-verification command and two claimed outputs without paste (artifact fix) → revise round 2; the auditor confirmed scope, artifacts, the 12 matching checks and the 921 s Bot wait |
| task-level, 1d4d2e44 (round-2 head) | incorrect (1) → P2 a `gh auth status` timeout, a missing `gh` or invalid JSON returns before the configured `hosts.yml` is checked (fix: collect the status warnings, then always run the file check + test) → revise round 3; the auditor confirmed scope, artifacts, 60 focused and 920 unit tests, 12 matching checks, the 924 s Bot wait and the resolved security thread |
| task-level, a431fd46 (round-3 head) | incorrect (1, artifact-only; no code finding: the auditor confirmed the five-file scope, the artifacts, eight in-memory doctor scenarios, syntax/ShellCheck/whitespace checks, the 12 matching CI results and the 924 s Bot wait) → disposition below after the worker's correction |

audit-finding: 1 the sandbox record claimed a Ruff run that the validation file did not show → not-applicable:artifact-only, outside the PR diff; corrected by the worker (PONG 2086, 10:45Z): the exact Ruff commands and their verbatim output at a431fd46, with the origin/main baseline, are appended to the validation file (section "Ruff (PONG decision 1)") and the sandbox record points to it; re-read by the orchestrator; the head does not move

- Sweep (head a431fd46, re-run after every push and after the orchestrator's thread resolution): `.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-pr-feedback.json`, 9 items, all `not-applicable`: the Codex security review P1 on `scripts/gh-auth.sh` (keep the token out of sandbox-readable storage) → operator decision A, design report §12/§16, with the verified fact that the keyring is unreachable from the Claude sandbox; replied (comment 4193420593) and resolved by the orchestrator; the orchestrator's reply; Codex quota notice; Codex review summary and container; CodeRabbit summary and status; 2 macOS capacity notices. Crit evidence `…-crit.json` (4 review records) / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md`.

## Deploy

- `make update` in the canonical clone at 8bbe8d44 (10:49Z): rc=0; the deployed `scripts/gh-auth.sh` logs in with `--insecure-storage`; `make doctor` reports no keyring warning for the active login (it is file-stored) and `~/.config/gh/hosts.yml` is `600 moriya`; the only remaining GitHub finding is the pre-existing two-login WARN that the operator's `gh auth logout --user mryfmo` clears.

## CompactionDB

- Worker decision `a2df6c5d-654c-43d1-96ea-97735606bd9b` (main checkout, by a005). Orchestrator consolidation `c5b12978-2663-4977-b524-dcc81c1299ee`.
