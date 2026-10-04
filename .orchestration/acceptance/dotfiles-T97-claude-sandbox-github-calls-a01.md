# Acceptance: dotfiles-T97-claude-sandbox-github-calls-a01

- **Decision:** ACCEPTED. PR #258 squash-merged to `main` as `6534df0f`; final head `391d2b4c39f68dc34f4fe131c6fda95b82101d56` (the orchestrator's `gh pr update-branch` of the diff head efe6735e onto `main` 67451fc6 after merging T77 first). Gate passed at 391d2b4c in the orchestrator-review worktree with the refreshed PR-feedback sweep, the 391d2b4c audit (`incorrect`, one evidence disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 16:52Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8, `security` profile gpt-6-astra). task_rev verified at each re-task and addendum.
- **Exemption declared:** acceptance and final integration; evidence sync (the seven worker artifacts copied from worker-e into the main checkout, because the Codex seat's writable roots exclude it).
- **Plan reference:** follow-up to T69 item (e) and T62/T64 (Claude-seat GitHub calls), outside the numbered phases; trust-boundary investigation routed to the Codex `security` seat per the model-selection rule.

## What was accepted (PR #258, diff head `efe6735e4542029b1357d27d1e47b63a57273ed4`, final head `391d2b4c39f68dc34f4fe131c6fda95b82101d56`; commits 8ffa5547, b8f293ef update-branch, 68e19ef7, 5b6b0d9f update-branch, efe6735e, 391d2b4c update-branch; two files, two lines)

- Finding (re-task 1 evidence, kept in the worker's artifacts): inside the Claude Code Linux sandbox `gh` answers HTTP 401 because the keyring-backed credential store needs an AF_UNIX socket, whose creation the sandbox denies; `allowUnixSockets` cannot grant a path on Linux. The GitHub domain allowance is present and irrelevant to this failure.
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md` Worker Playbook step 4 and `home/dot_config/claude/rules/agmsg-orchestration.md` worker-commands bullet now say: run `git fetch`/`push` and `gh` inside the sandbox first; on Linux `gh` backed by the host keyring answers 401 there; until dotfiles-T90 provisions a sandbox-readable worker credential, a Claude seat's `gh` calls, `git push` and any authenticated `git fetch` (a private HTTPS remote; the credential helper is `gh`) are the one class of commands it runs outside the sandbox through the permission gate; every other out-of-sandbox action stays a blocked PONG. The duplicated sentence from 8ffa5547 is gone.
- Auth provisioning (the root-cause fix) moved to T90 at re-task 2, as recorded in that task file ("Scope addition from T97").

## Decisions taken during the task

- Re-task 1: branch-setup block on the Codex seat (`--no-track`, push without `-u`); re-task 2: documentation-only residual, auth provisioning to T90; PONG decision: worker-side crit/receipt under `-worker-` names.
- Revise round 1 (68e19ef7): the 8ffa5547 wording limited the exception to `gh`, although Claude pushes ran unsandboxed in T72, T76 and T95 (`git push` asks `gh` for credentials); plus the duplicated sentence. The pre-screen audit of 8ffa5547 found the same `git push` gap independently.
- Round-1 addendum: no repeated Bot wait on pure `update-branch` heads (the Bot waited out the diff head 68e19ef7 in full; `main` advanced twice during the waits); the orchestrator held `main` for PR 258 afterwards.
- Revise round 2 (efe6735e): the task-level audit of 5b6b0d9f held that a globally installed rule and SKILL cannot be scoped by this repository's visibility, so an authenticated `git fetch` (private HTTPS remote) joins the exception in both sentences. That also turns Codex thread 4178339453 (private HTTPS fetch), first dispositioned not-applicable on the public-repository argument, into `fixed:efe6735e`.
- Codex thread 4178090986 (linked-worktree fetch): not applicable, resolved by the orchestrator — Claude seats fetch inside the sandbox too (a005's T95 record); the Codex worker's own mountinfo evidence was for its seat kind only.

## Orchestrator re-derivation

- Read both final sentences at efe6735e against the re-task-2 text, the round-1 corrections and the round-2 phrase; checked `grep -c 'blocked PONG'` leaves one closing sentence in the step.
- CI green on 68e19ef7, b8f293ef, 5b6b0d9f and efe6735e (the last after two targeted reruns of a Launchpad `IncompleteRead` in the Ghostty apt step, head unchanged); PR `clean`; branch on `main` f6320f37.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, 8ffa5547 (pre-screen) | incorrect (1) → fixed in 68e19ef7 |
| task-level, 5b6b0d9f (round-1 head) | incorrect (1) → fixed in revise round 2 (authenticated `git fetch` joins the exception; the rule is installed globally, so repository visibility cannot scope it) |
| task-level, diff head efe6735e | correct (no actionable findings) |
| task-level, final head 391d2b4c (update-branch only) | incorrect (1) → disposition below |

audit-finding: 1 the feedback snapshot and the report stop at efe6735e, so CI and thread state after the update-branch merge were not evidenced → not-applicable:orchestrator evidence sequencing; the sweep was refreshed on 391d2b4c after this audit (masked copy in the validation dir, same 12 items, all resolved) and CI on 391d2b4c is 13/13 SUCCESS (recorded below); the merge commit carries no diff, so the worker's report legitimately ends at the diff head efe6735e

- CI on the final head 391d2b4c: 13/13 SUCCESS at 16:50Z (CodeRabbit, changes, validate, test ×4, public-bootstrap ×3, private-bootstrap ×3); PR `clean`.
- Sweep (head 391d2b4c; same 12 items as efe6735e): see the masked copy `.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-pr-feedback.json`; one `fixed:efe6735e` (thread 4178339453), the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`; the worker's own `…-worker-crit.json` and `…-worker-review-receipt.md` are kept as task evidence.

## Follow-ups

- T90 (Codex security seat): sandbox-readable worker `gh` credential (`GH_CONFIG_DIR` with a file-stored token) plus the account separation; closes the exception in both documents.
- T77b (Codex seat): `executable_enforce-uv.sh` PreToolUse contract, routed out of T77.

## CompactionDB

- `[memory:failure]` from the worker report recorded by the orchestrator at acceptance: `751652a2-2a97-4626-bbdd-9f12bfc05689`.
