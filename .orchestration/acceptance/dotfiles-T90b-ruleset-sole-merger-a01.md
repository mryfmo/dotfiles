# Acceptance: dotfiles-T90b-ruleset-sole-merger-a01

- **Decision:** ACCEPTED. PR #265 squash-merged to `main` as `b13132d0`; head `5db320019d4c63f31eed9bfc1cea88ddade0a7cb`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 19:03Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8, `security` profile). task_rev verified at dispatch and after each of the four PONG-decision appends.
- **Exemption declared:** acceptance and final integration; evidence sync (seven worker artifacts copied from worker-e).
- **Plan reference:** follow-up from the T90 audit (P1/P2 on 507e9c15): the mechanical "only the orchestrator merges" guarantee and the boundary-PR path.

## What was accepted (PR #265, head `5db320019d4c63f31eed9bfc1cea88ddade0a7cb`; one commit on `main` 4c38dea0; 5 files, +345/−60)

- **README:** two `main` rulesets as payloads plus activation order and a verification table. Integrity ruleset (updates the existing "main integration gate"): no bypass actors, strict seven required checks, review-thread resolution, deletion and non-fast-forward protection, zero approvals (so the orchestrator's `.orchestration` boundary PR still merges). Merge-control ruleset: `update` (`update_allows_fetch_and_merge: false`) plus one required approval; sole bypass actor the orchestrator User in `pull_request` mode (numeric id to be verified with `gh api user`). Rule layering: the stricter requirement wins, so workers face approval plus threads and cannot update `main` at all, while the orchestrator bypasses only the merge-control rules and still faces the integrity checks.
- **Merge command after activation:** the synchronous REST merge with the head-sha guard, for worker PRs and the orchestrator's own boundary PRs, because `gh pr merge` refuses a `BLOCKED` PR without `--admin` and auto-merge completion does not engage bypass (sources cited). `gh pr merge --squash` keeps working before activation.
- **Gate (`scripts/require-crit-review.py`):** the role check activates on an `update` rule or a required approval; when active it requires the current user's numeric id to be the sole `User` bypass actor in `pull_request` mode of every restricting ruleset (fail closed), the orchestrator's approval on a worker PR's current head, and exempts only a non-empty `.orchestration`-only PR authored by the orchestrator (diff inspected over `base_sha...head`, worklogs included).
- **SKILL step 10 and the rule:** approve-then-REST-merge after activation; the two boundary `--auto` mentions qualified "before activation"; the rule's integration-order sentence points at the SKILL procedure.
- Tests: 783 full, 76 focused on the gate (inactive/active, bypass-actor shape, author exemption); CI 13/13 green; no Bot review within the window; no threads.

## Decisions taken during the task

- PONG 1: two rulesets (integrity without bypass; merge-control with the orchestrator as sole `pull_request`-mode bypass actor), because a bypass covers every rule in its own ruleset.
- PONG 2: the REST merge call replaces `gh pr merge --auto` after activation (gh refuses `BLOCKED` without `--admin`; auto-merge completion ignores bypass).
- PONG 3 and 4: the two remaining SKILL `--auto` mentions and the rule's command reference made consistent with the step-10 procedure.

## Orchestrator re-derivation

- Read the gate diff in full: the activation set, the per-ruleset bypass-actor check against `gh api user` id, the approval check, and the boundary exemption; confirmed the inactive path still prints a notice and passes (no worker `hosts.yml` on this host, so today's gate runs are unchanged).
- Read the README payloads against the decisions: integrity ruleset `bypass_actors: []`, `required_approving_review_count: 0`; merge-control ruleset `update` + approval 1 + one User bypass in `pull_request` mode; both target `refs/heads/main`.
- Residual (documented, operator-verified at activation): the behaviour of the `update` rule against PR merges by non-bypass actors and of PR-only bypass is a design inference from GitHub's documentation; the README's verification table is to be executed live during activation, and the rollout stops if a prohibited merge succeeds.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 5db32001 | correct (no actionable findings) |

- Sweep (head 5db32001): see the masked copy `.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-pr-feedback.json`; five items, all `not-applicable` (CodeRabbit summary/status, three capacity notices; the Codex review on this head carried no inline finding).
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`; worker `…-worker-crit.json` / `…-worker-review-receipt.md` kept.

## Operator phase (not performed by this acceptance)

1. Complete the T90 operator phase (worker login into `~/.config/gh-worker` with `--insecure-storage`, `make doctor` with two logins), deploy the launcher and restart workers, confirm the worker login in a worker pane.
2. Apply the integrity payload to the existing ruleset id (PUT), then create the merge-control ruleset (POST) with the verified orchestrator user id; read both back; inspect `rules/branches/main`.
3. Run the scratch-PR table and record the actual responses in the README; stop the rollout if a prohibited merge succeeds.
4. From activation on, the orchestrator merges with the REST call after the integrity checks pass.

## CompactionDB

- Orchestrator consolidation `8cda8d6c-8388-41bd-8551-17a273310324` (the Codex seat cannot write the main-checkout DB).
