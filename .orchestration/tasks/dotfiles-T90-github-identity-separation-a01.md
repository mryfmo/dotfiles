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

## Dispatch

- 2026-10-04 (queued for `codex-security-dot-a007`, the Codex security-profile seat in `.claude/worktrees/worker-e`, once PR #253 (T69) has merged, because both edit `home/dot_agents/skills/agmsg-orchestration/SKILL.md`; `scripts/require-crit-review.py` is free since T93 merged). Branch from the commit that merged #253 or later. The second GitHub account's `gh auth login` into the worker gh config dir is the operator's; the task delivers the launcher, doctor, gate and ruleset payload and documents the login step. Routing: `GH_CONFIG_DIR` for worker panes and the gate's author/approver check are trust-boundary work for the security profile; they are not a seat's sandbox or permission source.

## Scope addition from T97 (orchestrator, 2026-10-04 19:25Z) — sandbox-readable worker credential

T97 proved that a Claude seat's `gh` cannot use the host keyring inside the Linux sandbox (AF_UNIX socket creation denied; `allowUnixSockets` grants no path there). The worker gh configuration this task introduces must therefore work without the keyring:

- `GH_CONFIG_DIR=<worker gh dir>` (default `~/.config/gh-worker`, operator-created) holds the write-only account's credentials in gh's file storage (`gh auth login --insecure-storage` into that dir, or `gh auth login` with `GH_CONFIG_DIR` set and insecure storage forced), mode 0600, owned by the user; the Claude sandbox must be able to read that directory (check `claude.sandbox` read denies; the dir must not fall under a denied pattern) and the Codex sandbox likewise.
- The orchestrator keeps its own default gh config (keyring, the merging account) and never exports it to a seat.
- Doctor: besides "two different logins", verify the worker dir's `hosts.yml` carries a token (file storage) and that its mode is 0600.
- Document the operator step once in README's operator phase: create the dir, run the login for the write account with insecure storage, confirm `GH_CONFIG_DIR=… gh auth status`.
- Security review of this change is this seat's own profile; the orchestrator still accepts.

This supersedes any wording in the objective that assumed keyring storage for the worker account.

## Dispatch 2 (orchestrator, 2026-10-05 01:50Z) — to `codex-security-dot-a007`

- T69 (04bce61b) and T97's final text are settled; PR #258 (T97, two sentences in SKILL step 4 and the rule's worker-commands bullet) merges within the hour, before this PR. Branch from the current `origin/main` (the T77 merge or later) with `git switch -c feat/github-identity-separation --no-track origin/main`, push with `git push origin <branch>`, open with `gh pr create --head <branch>`; after #258 merges, `gh pr update-branch` and keep your SKILL edit to the acceptance step (step 10) only.
- **Gate check must not strand acceptance.** Until the operator has provisioned the second account (`gh auth login --insecure-storage` into the worker gh dir) and applied the ruleset, every seat still shares one login. Make the new author/approver check in `scripts/require-crit-review.py` active only when the worker gh configuration exists (`WORKER_GH_CONFIG_DIR`'s `hosts.yml` present) **and** the ruleset reports `required_approving_review_count >= 1` for `main`; otherwise print one `notice:` line naming what is missing and pass. Document that activation condition in README and the rule bullet. Tests cover both states.
- `make doctor` likewise: the two-login check is a required failure only once the worker gh dir exists; a missing dir is a `warn_optional` naming the operator step.
- Artifacts: write the five files plus `-worker-crit.json` / `-worker-review-receipt.md` under your worktree's `.orchestration/`; the orchestrator transfers them. Bot wait per SKILL on the diff head only (no repeated wait on update-branch heads). RESULT via `agmsg-dispatch dotfiles codex-security-dot-a007 claude-remediation-dot wT:p1 "<line>"`.

### PONG decision (orchestrator, 2026-10-05 02:05Z) — launcher env hand-offs and the Codex env policy

1. **Authorized:** a narrow adapter in `executable_herdr-agents` so `GH_CONFIG_DIR=<worker gh dir>` reaches both worker hand-offs: the pair worker pane's boot environment and spawn-seated workers (`--add-worker`, upstream `spawn.sh` with the herdr terminal driver, where `workspace create --env` reaches only the root pane; the same gap the T89 follow-up recorded for `AGMSG_RESOLVE_PROJECT`/`AGMSG_CC_MONITOR_KEEP_ALIVE`/`HERDR_AGENTS_LAYOUT`). Keep it to the smallest mechanism that carries a fixed list of variables (reuse it for those three if that costs nothing extra; otherwise leave them for the follow-up), covered by fake-CLI tests. No raw herdr topology changes beyond what the existing code already issues.
2. **Authorized as identity routing:** for Codex worker launches only, `-c shell_environment_policy.additional_include=["GH_CONFIG_DIR"]` on the worker command line in `herdr-agents` (next to the existing `-c sandbox_workspace_write.writable_roots=…`), because `inherit=core` drops the variable. Not in any profile TOML, not for the orchestrator or audit lanes, no change to `sandbox_workspace_write`, `approval_policy` or network. The seat-capability rule concerns sandbox, approval and permission sources; an environment-variable allow-list for identity routing is outside it, and this decision records that classification. Claude worker panes need no equivalent (the pane environment is inherited).
3. Record both in the report's design section with the test names.

### PONG decision 2 (orchestrator, 2026-10-05 02:30Z) — main held for PR 262

The boundary commit #263 (8cd66881) was the orchestrator's; nothing else merges to `main` until PR 262 does. Run `gh pr update-branch 262` once onto 8cd66881, wait for CI, and send the RESULT; the Bot already reviewed your diff head, so no further Bot wait on update-branch heads (round-1 addendum rule of T97 applies here too).

## Revise round 1 (orchestrator, 2026-10-05 03:00Z) — task-level audit of 507e9c15 is `incorrect` (3)

The orchestrator revises the objective (audit P1): this task delivers role separation (worker credentials in a dedicated `GH_CONFIG_DIR`, two-login doctor, approval-gated local gate, documented procedure); the *mechanical* "only the orchestrator merges" guarantee moves to **T90b**, a ruleset design task: an `update` restriction on `main` with the orchestrator account as the sole bypass actor in `pull_request` mode (so workers cannot push or merge to `main` at all, and the orchestrator merges its own boundary PRs without self-approval), plus the activation order. Two edits in this PR, one commit:

1. **README (ruleset section and operator phase, audit P1/P2):** keep the payload as the *draft*, and replace "After both identities work, the operator applies the payload …" with: do **not** apply it yet; the required-approval payload alone (a) still lets a worker merge its PR by API once the orchestrator has approved, and (b) blocks orchestrator-authored `.orchestration` boundary PRs because GitHub refuses author self-approval. T90b designs the ruleset (update restriction + orchestrator bypass actor, `pull_request` mode) and the activation order; the operator phase stops after `make doctor` until then. The gate's role check stays inactive until a ruleset requires approvals, so nothing regresses before T90b.
2. **Report:** completion item 4 (audit P2): state that the main-checkout CompactionDB is outside this seat's writable roots and that the orchestrator records the decision at acceptance (it does; the `memory add` output lands in the acceptance record, not in your validation). No command to run.

Then push, CI, RESULT (no repeated Bot wait on update-branch heads; the Bot already reviewed the diff). `main` stays held for this PR.
