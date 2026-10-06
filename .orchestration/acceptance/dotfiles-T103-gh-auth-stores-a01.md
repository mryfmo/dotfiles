# Acceptance: dotfiles-T103-gh-auth-stores-a01

- **Decision:** ACCEPTED. PR #288 squash-merged to `main` as `ca5d28ec` (2026-10-06 00:36Z); head `c4fa1c14` (round 2). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main PR_FEEDBACK_EVIDENCE=… AUDIT_EVIDENCE=…-audit-c4fa1c1.md AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` rc=0, 00:35Z; `notice: GitHub role gate inactive: worker hosts.yml missing`). Earlier: REVISE ROUND 2 dispatched 2026-10-06 00:00Z (round-1 audit: swallowed chmod failure; negative-test transcript exit status). Earlier: REVISE ROUND 1 dispatched 2026-10-05 23:30Z (round-0 audit: bootstrap PATH misses mise-installed `gh`; `~` not expanded in the duplicate-store check; hint and two artifact corrections). RESULT received 23:21Z (head `0a28eb74`, PR #288).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev verified at dispatch (21:54Z) and at both PONG decisions.
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; the orchestrator replied to and resolved the one Bot thread (thread resolution is orchestrator-side by the task rules).
- **Design source:** `.orchestration/validation/github-auth-design-2026-10-05.md` §10–§12 (operator decisions of 2026-10-05: one credential store per account, file storage for all three, prompts only in the interactive operator phase, `make update` never prompts, the keyring alternative not to be reopened).
- **PONG decisions:** 1 (drop `gh auth setup-git`; the managed git helper serves every store; `check-tools.sh` hint allowed); 2 (file storage stands; the Bot P1 is the orchestrator's disposition, not a code change).

## What is under acceptance (PR #288, head `c4fa1c14`, 6 commits on main 2d0ef943; 13 files, +585/−33)

- Manifest: `owner_gh_config_dir`, `work_gh_config_dir`, `worker_gh_config_dir` (directories only), rendered as `OWNER_/WORK_/WORKER_GH_CONFIG_DIR`; distinct directories enforced by the renderer.
- `scripts/gh-auth-stores.sh` (+ `make gh-auth`, `setup.sh` `authenticate_github` on interactive non-CI runs): per store, `gh auth status` → skip, else device-code `gh auth login --insecure-storage` + `chmod 600`; tty-only; token env cleared; no `setup-git`.
- `scripts/check-agent-runtime.py`: `found:` info lines per present store (0600, one login, login name) or WARN with the `make gh-auth` hint; never prompts, never reads a token. `scripts/check-tools.sh` hint updated.
- README operator-phase block → three-store table, no-prompt contract, chezmoi-private note.
- Rounds 1–2: mise shims on PATH before the `gh` lookup in `setup.sh` and the script; `~` expanded in the duplicate-store check; hint on the mode/owner WARN; `secure_hosts_file()` fails a store whose `hosts.yml` cannot be set to 0600 (and `mkdir -p` failure fails it); artifacts corrected.
- Tests: renderer (incl. absolute-vs-`~` duplicate), doctor (fake stores/gh), script (no-tty, pty, env token, fresh PATH with `gh` only as a shim, failing chmod), setup.sh CI skip; 917 unit tests OK.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, 0a28eb74 (round-0 head) | incorrect (5) → P2 fresh bootstrap cannot find the mise-installed `gh` (parent PATH lacks the shims) so the login step is skipped on first run (fix); P2 the duplicate-store check does not expand `~`, so `~/.config/gh` and its absolute form pass as two stores (fix); P3 the mode/owner warning lacks the `make gh-auth` hint (fix); P3 sandbox report says `check-tools.sh` was out of scope though PONG decision 1 allowed the edit (artifact fix); P3 "CI green on every head" and a ruff-check claim exceed the pasted evidence (artifact fix) → revise round 1; the auditor confirmed the amended scope, the artifacts, 15 successful final-head checks and the dispositioned security thread |
| task-level, a41a56bd (round-1 head) | incorrect (2) → P2 a failed `chmod 600` inside `ensure_store` is swallowed (errexit off in an `||` list), so a non-owned readable hosts.yml stays exposed while `make gh-auth` exits 0 (fix: explicit failure + test); P3 the round-1 negative-test transcript shows `FAILED (failures=4)` then `exit=0` (artifact fix: real wrapper command and the test exit status) → revise round 2; the auditor confirmed scope, artifacts, 15 successful checks and the resolved security thread |
| task-level, c4fa1c14 (round-2 head) | correct (no findings; the auditor confirmed the amended scope, the artifacts, permission-failure handling, renderer validation, doctor reporting, 917 passing tests and the 15 successful checks; the security P1 stays an explicitly accepted exposure with its thread resolved) |

- Sweep (head c4fa1c14, re-run after each push; the same 11 items at every head): `.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-pr-feedback.json`, 11 items, all `not-applicable`: Codex quota notice at PR open; CodeRabbit summary comment and status; two review containers; the Bot P1 thread on `scripts/gh-auth-stores.sh:45` (owner token in a file readable by worker seats) → operator-accepted exposure per the design report §12, replied (comment 4189878365) and resolved by the orchestrator, no head change; the orchestrator's own reply; 4 macOS capacity notices. Bot coverage: the security review on bb9e92ed; none on the final head. Crit evidence `…-crit.json` / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md`.

## Deploy

- `make update` in the canonical clone at ca5d28ec (2026-10-06 00:36Z): rc=0, no prompt, no login call; `~/.agents/model-profiles.env` now carries `OWNER_GH_CONFIG_DIR='~/.config/gh'`, `WORK_GH_CONFIG_DIR='~/.config/gh-work'`, `WORKER_GH_CONFIG_DIR='~/.config/gh-worker'`.
- `make doctor` afterwards (`Doctor summary: tools=passed; runtime=passed`) reports the three stores as the operator phase expects before `make gh-auth`: owner store `holds 2 working of 2 logins; keep exactly one account per store` (the work account still shares gh's default directory), work and worker stores `has no hosts.yml; run make gh-auth`. These are the operator's next step, not defects.

## CompactionDB

- Worker decision `ba9aa377-1bb6-4a41-898a-5fe622684558` (main checkout, by a005). Orchestrator consolidation `7251122f-be85-4e7c-802b-9c0bde0ae526`.
