# AGMSG-TASK dotfiles-T90b-ruleset-sole-merger-a01

Drafted 2026-10-05 by the orchestrator seat from the T90 audit (P1/P2 on 507e9c15): required approval alone neither makes the orchestrator the sole merger nor lets orchestrator-authored boundary PRs merge. Depends on T90 (PR #262). Codex `security` seat (trust-boundary work). Shares `README.md` and `scripts/require-crit-review.py` with T90; dispatch after #262 merges.

## Objective

Make "only the orchestrator merges to `main`" mechanical on GitHub, and keep the `.orchestration` boundary PR path working, without weakening the existing checks.

1. **Ruleset design (README payload, operator-applied):** keep the `pull_request` rule with `required_approving_review_count: 1`, `dismiss_stale_reviews_on_push: true`, `require_last_push_approval: false`, and the seven required status checks (strict). Add an `update` rule (`update_allows_fetch_and_merge: false`) so no one can push to or merge into `main` by default, and list the orchestrator account as the only bypass actor with `bypass_mode: pull_request`, so the orchestrator can merge pull requests (its own boundary PRs included, without self-approval) while a worker account can neither push, merge nor approve its own PR. VERIFY against the GitHub rulesets reference: that `update` blocks PR merges by non-bypass actors, that `pull_request` bypass mode is limited to PR merges (no direct pushes), and what the bypass does to required status checks (if a PR-mode bypass also skips required checks, say so and keep the local gate as the enforcing step; the gate already requires CI-green feedback). Paste the sources.
2. **Gate (`scripts/require-crit-review.py`):** the role check's activation condition becomes "worker `hosts.yml` exists **and** the effective `main` rules contain an `update` rule or a `pull_request` rule with `required_approving_review_count >= 1`"; when active and the current login is the sole bypass actor, approval of a worker PR by the current login remains required (process evidence); an orchestrator-authored PR (author == current login) passes the role check without approval only when the diff is `.orchestration`-only (reuse the existing boundary exemption). Tests for both authorships and both rule shapes.
3. **README operator phase:** the activation order after T90's doctor step: apply the payload with `gh api -X PUT repos/mryfmo/dotfiles/rulesets/<id> --input <payload.json>`; on a scratch PR authored by the worker account verify (a) self-approval refused, (b) `gh api --method PUT …/merge` returns 405 before and after the orchestrator's approval (the `update` rule), (c) the orchestrator merges it; on an orchestrator-authored `.orchestration` scratch PR verify `gh pr merge --squash` succeeds without approval. Record the expected responses.
4. **SKILL step 10 / boundary bullet:** the boundary PR path (`gh pr merge --squash --auto` by the orchestrator) stays valid under the bypass; say so in one sentence where the boundary procedure is described.

Forbidden: applying the ruleset (operator); creating accounts or tokens; any launcher change; merging.

[memory:decision] dotfiles-T90b (orchestrator 2026-10-05, from the T90 audit): the `main` ruleset gains an `update` restriction with the orchestrator account as the sole `pull_request`-mode bypass actor, so a worker account can neither push, merge nor self-approve, while the orchestrator merges reviewed worker PRs and its own `.orchestration` boundary PRs; the local gate's role check mirrors that shape.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/ruleset-sole-merger --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.

## Allowed files

- `README.md` (ruleset section and operator phase), `scripts/require-crit-review.py`, `tests/unit/test_require_crit_review.py`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (one sentence), `home/dot_config/claude/rules/agmsg-orchestration.md` (the boundary bullet, one clause)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T90b-ruleset-sole-merger-a01.md` plus `-worker-crit.json` / `-worker-review-receipt.md` (in your worktree; the orchestrator transfers them)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_require_crit_review 2>&1 | tail -3
make unit-test 2>&1 | tail -3
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY sources.
4. The main-checkout CompactionDB is outside your writable roots: the orchestrator records the `[memory:decision]` at acceptance; say so in the report.
5. `AGMSG-RESULT v1 task_id=dotfiles-T90b` via `agmsg-dispatch dotfiles codex-security-dot-a007 claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

## Dispatch

- 2026-10-05 03:30Z to `codex-security-dot-a007` (worker-e, wT:p8) after its T90 acceptance (PR #262 merged as 4c38dea0). Branch from `origin/main` 4c38dea0 or later with `--no-track`. Artifacts in your worktree; the orchestrator transfers them. Bot wait on the diff head only.

### PONG decision (orchestrator, 2026-10-05 03:45Z) — split payload authorized

Authorized: two rulesets on `main`, documented as two payloads in the README with the activation order.

1. **Integrity ruleset (no bypass actors):** `deletion`, `non_fast_forward`, `required_status_checks` (the seven contexts, strict), `pull_request` with `required_review_thread_resolution: true` and `required_approving_review_count: 0`. Nobody, the orchestrator included, merges without green required checks and resolved threads; the `.orchestration`-only boundary PR keeps working because the `changes` job's skipped matrix is accepted as today.
2. **Merge-control ruleset (orchestrator account the sole bypass actor, `pull_request` mode):** `update` (`update_allows_fetch_and_merge: false`) plus `pull_request` with `required_approving_review_count: 1`, `dismiss_stale_reviews_on_push: true`, `require_last_push_approval: false`. A worker account can neither push, merge nor self-approve; the orchestrator merges reviewed worker PRs and its own boundary PRs without self-approval.
3. VERIFY and paste: that bypass applies per ruleset (so ruleset 1 still binds the orchestrator), and that two rulesets with `pull_request` rules combine as the stricter of each parameter. If GitHub combines them differently, say so and propose the smallest adjustment.
4. Gate: the local role check activates when the effective rules for `main` contain an `update` rule or a `pull_request` rule with `required_approving_review_count >= 1` (either ruleset), as the task says; the gate keeps requiring green feedback regardless of any bypass.

### PONG decision 2 (orchestrator, 2026-10-05 03:55Z) — merge command under the bypass

Authorized. Since `gh pr merge` refuses a `BLOCKED` PR without `--admin` and auto-merge completion ignores ruleset bypass (cli/cli#13388, github/docs#45265), the orchestrator's merge becomes the synchronous REST call once the integrity ruleset is satisfied (required checks green, threads resolved): `gh api --method PUT repos/mryfmo/dotfiles/pulls/<pr>/merge -f merge_method=squash -f sha=<head> -f commit_title='<title> (#<pr>)'`, for both the boundary PR and normal acceptance. Edit accordingly: the SKILL step-10 merge sentence, the rule's boundary clause (`--auto` is gone; the boundary PR waits for green checks, then the same PUT), the README boundary/acceptance mentions and the scratch-PR expected path (worker PUT → 405 before and after approval; orchestrator PUT → 200 with the `sha` guard). Until the merge-control ruleset is applied, `gh pr merge --squash` keeps working and the documents may say so in one clause ("before activation"). Keep the no-bypass integrity ruleset as decided.

### PONG decision 3 (orchestrator, 2026-10-05 04:05Z)

Authorized: qualify the two remaining `--auto` mentions in the SKILL (the boundary bullets around lines 67 and 69) with "before activation" and a pointer to the step-10 REST merge after activation, so the runbook has no internal contradiction. Nothing else.

### PONG decision 4 (orchestrator, 2026-10-05 04:10Z)

Authorized: in `home/dot_config/claude/rules/agmsg-orchestration.md` (already an allowed file), replace the one `gh pr merge --squash` command reference in the integration-order sentence (line 9) with a pointer to the SKILL step-10 merge procedure (REST merge after activation; `gh pr merge --squash` before). Then commit, CI, Bot wait on the diff head, RESULT.
