# Acceptance: dotfiles-T98b-runner-home-and-review-body-a01

- **Decision:** ACCEPTED. PR #280 squash-merged to `main` as `7f5b9b9d`; head `70f060e7`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two procedural dispositions below) and crit evidence (`BASE=origin/main … AUDIT_DISPOSITIONS=… make require-crit-review` rc=0, 2026-10-05 09:53Z). Bot coverage: none (Codex quota notice at PR open); the audit is the independent review.
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev verified at dispatch (09:11Z).
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** lessons of 2026-10-05 (boundary PR #279 first push failed CI on a glued runner-home literal; T98 round-1 audit found a Bot review-body finding the sweep had dismissed).

## What is under acceptance (PR #280, head `70f060e7`, one commit on main 58f7594f; 4 files, +21/−1)

- `scripts/validate-agent-assets.py`: `~` and `~` are machine-independent forms that match anywhere (no leading boundary), so a workstation's masker rewrites a glued runner path exactly as a GitHub runner's own `$HOME` backstop flags it; every other form unchanged.
- `tests/unit/test_validate_agent_assets.py`: `test_runner_homes_match_anywhere` (glued runner paths rewritten under `HOME=~`; `~`, `~` stay ordinary account forms with the boundary).
- `SKILL.md`: Orchestrator Playbook step 10.4 — a `review` sweep item whose body carries a P badge is a finding with its own disposition, never a container; Worker Playbook step 15 — read each review's body and list review-body findings alongside inline comments; fix P0/P1 findings inline or review-body. Both pinned in `tests/unit/test_agmsg_orchestration_docs.py`. Rule unedited.
- Item 3 of the task (boundary sentence) needed no change: the boundary bullet already names the masker since T98.

## Orchestrator re-derivation

- Read the whole diff; traced the compiled pattern: the runner form precedes the account form and shares the trailing `(?![\w.-])` lookahead, so `-up`/`s` suffixes fall through to the boundary form as the test asserts.
- Origin of the lesson: boundary PR #279's first push failed `validate` on the T98 task file's quoted `F~/.ssh/id`; fixed in #279 by re-masking under `HOME=~`; this task makes that re-run unnecessary.

- Sweep (head 70f060e7): `.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-pr-feedback.json`, 6 items, all `not-applicable` (Codex quota notice, CodeRabbit summary and status, 3 macOS capacity notices). Crit evidence `…-crit.json` and receipt `…-review-receipt.md`.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 70f060e7 | incorrect (2 procedural/reporting, no functional defect) → dispositions below; the auditor ran twenty in-memory pattern cases, confirmed the four allowed files, five artifacts and the zero-match re-mask log over 2,502 files |

audit-finding: 1 the sandbox record shows the artifacts were written into the main checkout and masked outside the sandbox, which Worker Playbook step 4 does not list among the gated exceptions → not-applicable:a Claude seat's worktree sandbox cannot write the main checkout's `.orchestration/`, so writing the expected artifacts there has gone through the permission gate in every Claude-seat task of this regime, the same class as the documented main-checkout CompactionDB `memory add` exception; the worker's record disclosed it; the sandbox record was corrected to name that gated write (PONG decision 1, confirmed by its corrected PONG), and the missing SKILL sentence is recorded as a follow-up for the next docs task; no code or evidence content is affected and the head does not move
audit-finding: 2 the report's `cost:` line gives commit, CI-round and turn estimates instead of observed figures or `cost: n/a` → not-applicable:reporting format only; no token or cost figures are observable for a Claude seat here, so the worker replaced the line with `cost: n/a` (PONG decision 1, confirmed by its corrected PONG); the report is a main-checkout artifact outside the PR diff and the head does not move

## CompactionDB

- Worker decision `5328b485` (main checkout, by a005). Orchestrator consolidation `9ee20055-0009-4431-8556-d8da37f3a8db`.
