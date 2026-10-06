# Acceptance: dotfiles-T104-pins-2026-10-06-a01

- **Decision:** ACCEPTED. PR #290 squash-merged to `main` as `50741c4d` (2026-10-06 01:12Z); head `bd0327a0` (merge of main b3f0bc61 after boundary #289; diff commit `8c4a34e6`). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two artifact-only dispositions below), `AUDIT_DISPOSITIONS` and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 01:11Z; `notice: GitHub role gate inactive: worker hosts.yml missing`). RESULT received 01:05Z; the PR diff was checked byte-identical to the exported pin diff.
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev verified at dispatch (00:39Z).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (the pin diff was exported from the canonical clone with `git diff` into `.orchestration/validation/pins-2026-10-06.diff`; the clone itself is not a repository mutation target of this task).
- **Origin:** the canonical clone `~/.local/share/chezmoi` carried a pending `make upgrade` pin diff (7 files, +57/−57), surfaced as "Applied autostash" during the T103 deploy; per the regime rule it travels as one class-pure pin PR.

## What is under acceptance (PR #290, diff commit `8c4a34e6` on main; 7 files, +57/−57, no `tests/**` change)

- Pins: mise v2026.9.14 → v2026.9.16; aws-cli 2.37.4 → 2.37.5; chezmoi 2.70.4 (bootstrap: `setup.sh`, `installer-pins.sh`, manifest) and 2.72.2 (mise) → 2.73.0; dotenvx 2.30.0 → 2.31.1; hugo-extended 0.166.0 → 0.167.0; claude-code 2.1.288 → 2.1.289; codex 0.160.0 → 0.160.1; ccusage 20.0.24 → 20.0.26; pnpm 12.7.0 → 12.8.1; `mise.lock` entries.
- Tests: no live-value assertion exists for these pins (the remaining old strings are fixtures in fake release listings and renderer samples); `make render-check` clean; 917 unit tests OK.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head bd0327a0 | incorrect (2, both artifact-only; no code defect: the auditor confirmed the patch matches the supplied diff, the seven-file scope, consistent manifest/installer/lock versions, independent test fixtures, 15 successful check runs and the completed security review) → dispositions below after the worker's corrections |

audit-finding: 1 the sandbox record listed the inbox read among the Worker Playbook step-4 exceptions, which do not include inbox reads → not-applicable:artifact-only, outside the PR diff; corrected by the worker (PONG 1918, 01:10Z): the read (`inbox.sh dotfiles claude-standard-dot-a005` from worker-c, messages 1888 and 1916) is now recorded as a disclosed deviation through the permission gate with its reason (a carried-over habit; the read works inside the sandbox since the agmsg store is a writable root, and later reads ran there); the head does not move
audit-finding: 2 no pasted output showed the PR title or description, so the English metadata and the attribution footer could not be verified → not-applicable:artifact-only, outside the PR diff; corrected by the worker (PONG 1918): the validation file now carries the verbatim `gh pr view 290 --json number,title,body,headRefOid` output (English title and body with the Claude Code attribution footer, headRefOid bd0327a0), re-read by the orchestrator; the head does not move

- Sweep (head bd0327a0): `.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-pr-feedback.json`, 8 items, all `not-applicable` (Codex quota notice; CodeRabbit summary comment and status; the Codex security review summary comment, review completed on 8c4a34e6 with no findings; 4 macOS capacity notices). Bot coverage: Codex security review of 8c4a34e6, no findings; none on the merge head. Crit evidence `…-crit.json` / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md`.

## Deploy

- Canonical clone: its dirty pin diff was re-checked byte-identical to the exported diff, discarded with `git checkout -- .`, and the clone fast-forwarded to 50741c4d. `make update` rc=0 (01:12Z); `mise install --locked` reports pnpm 12.8.1 and ccusage 20.0.26 installed; mise resolves codex 0.160.1 (`mise which codex`) and chezmoi 2.73.0 for new shells (the running panes keep their session binaries: codex 0.160.0, Claude Code 2.1.287 until restarted; `not_found_auto_install=true`).
- Codex hook trust under 0.160.1 (app-server `hooks/list` with the new binary, 01:14Z): all 8 declared keys `trusted` with `currentHash` equal to the stored `trusted_hash`, so the T82b hash algorithm holds for 0.160.1 and the comments naming rust-v0.160.0 are historical, not stale.
- Pre-existing host finding surfaced by the deploy logs: `Warning: private chezmoi source/config not found` — `~/.config/chezmoi-private/chezmoi.yaml` is absent on this host, so the private layer is skipped (design report §13; operator-side).

## CompactionDB

- Worker decision `924aedfd-d0da-4af7-916b-f136112529df` (main checkout, by a005). Orchestrator consolidation `2fbdf71a-f2fc-4451-94ed-d1d833925438`.
