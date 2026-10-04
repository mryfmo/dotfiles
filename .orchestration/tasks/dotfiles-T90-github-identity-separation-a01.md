# AGMSG-TASK dotfiles-T90-github-identity-separation-a01

Drafted 2026-10-04 by the orchestrator seat from the operator decision 「account を役で分ける」 (T64 audit P1). Trust-boundary work: run it with a **Codex worker on the `security` profile** (`herdr-agents --add-worker <worktree> --kind codex --profile security`, identity `codex-security-dot-aNNN`) after T64 is deployed (`make update`). Dispatch condition: T64 merged and deployed; T89 merged if the operator wants the worker pane inside the pair workspace.

## Objective

Principle 1 on the GitHub side: "only the orchestrator merges" must be mechanical. Today every seat (orchestrator, Claude workers, and Codex workers after T64) shares the operator's gh credentials, so a worker can merge through `gh api --method PUT repos/<o>/<r>/pulls/<n>/merge` and the ruleset cannot tell the roles apart. Separate the identities by role and let GitHub enforce it:

1. **Role accounts.** Worker seats authenticate as the write-only account (today `moriya-fumio-thd`); the orchestrator seat authenticates as a different account (`mryfmo`, or a dedicated bot account the operator creates; the task does not create accounts). With the ruleset's `required_approving_review_count: 1`, GitHub refuses a self-approval by the PR author, so a worker (author) cannot merge its own PR even via the API, while the orchestrator (different login) approves and merges.
2. **Per-seat gh configuration.** `herdr-agents` gives worker panes (pair worker and `--add-worker`, both kinds) `GH_CONFIG_DIR=<worker gh dir>` (manifest key `worker_gh_config_dir`, default `~/.config/gh-worker`, rendered into `model-profiles.env`), so `gh` and the `gh auth setup-git` credential helper resolve the worker account inside those panes only; the orchestrator pane keeps the default `~/.config/gh`. VERIFY: gh honours `GH_CONFIG_DIR` for both `gh` commands and the git credential helper it installs; `gh auth status` inside a worker pane shows the worker login. Document the operator phase step: `GH_CONFIG_DIR=~/.config/gh-worker gh auth login` once per machine with the worker account, and `gh auth setup-git` in that config dir.
3. **Doctor.** `scripts/check-tools.sh` (or `check-agent-runtime.py`, whichever already checks gh) verifies that the default gh config and the worker gh config are both authenticated and name **different** logins; a required failure when they are the same login (the boundary would be void).
4. **Ruleset.** README ruleset payload: `required_approving_review_count: 1` (keep `require_last_push_approval: false`); note that the operator applies it with `gh api -X PUT repos/mryfmo/dotfiles/rulesets/<id>`. Acceptance procedure (SKILL orchestrator step): `gh pr review <n> --approve` then `gh pr merge <n> --squash` from the orchestrator account. Keep `dismiss_stale_reviews_on_push: true` (a new push by the worker invalidates the approval, which is the intended behaviour).
5. **Gate.** `scripts/require-crit-review.py --base`: verify that the PR author login differs from the current `gh api user` login (orchestrator) and that an approving review by the current login exists on the head; otherwise fail. One small check, reusing the existing gh helpers.
6. Tests for the launcher env, the doctor check and the gate check; README (operator phase, roles) and SKILL text (acceptance step) in the same PR, since they are the contract of this change.

VERIFY: gh multi-account/`GH_CONFIG_DIR` semantics (docs); GitHub's refusal of author self-approval with `required_approving_review_count`; whether `gh api --method PUT .../merge` is indeed blocked for the author under the updated ruleset (test on a scratch PR after the operator applies the ruleset: the worker account's merge attempt returns 405 with the "review required" reason).

[memory:decision] dotfiles-T90 (operator 2026-10-04): GitHub identities are separated by role: worker seats use the write account through a dedicated `GH_CONFIG_DIR`, the orchestrator approves and merges with a different account, and the ruleset requires one approving review so a worker cannot merge its own PR by any API path.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/github-identity-separation origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`, `home/dot_agents/agent-config.yaml` (the `worker_gh_config_dir` key only), `scripts/generate-agent-configs.py` (rendering the key to `model-profiles.env`), rendered `home/dot_agents/model-profiles.env`
- `scripts/check-tools.sh` or `scripts/check-agent-runtime.py` (the gh login check), `scripts/require-crit-review.py` (the author/approver check)
- `tests/unit/test_herdr_agents.py`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_require_crit_review.py`, the doctor tests
- `README.md` (ruleset payload, roles, operator phase), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (acceptance step), `home/dot_config/claude/rules/pr-integration.md` (one bullet)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T90-github-identity-separation-a01.md` (main checkout)

## Forbidden actions

- Creating GitHub accounts or tokens; writing any credential into the repository; applying the ruleset (operator); `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check; grep -n WORKER_GH_CONFIG_DIR home/dot_agents/model-profiles.env
uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_generate_agent_configs tests.unit.test_require_crit_review 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents scripts/check-tools.sh; shellcheck home/dot_local/bin/common/executable_herdr-agents scripts/check-tools.sh
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/pr-integration.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: wait for the Codex Bot review of that head; fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, VERIFY results with sources; the operator steps (gh login for the worker config dir, ruleset PUT) listed in the report.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=40.
