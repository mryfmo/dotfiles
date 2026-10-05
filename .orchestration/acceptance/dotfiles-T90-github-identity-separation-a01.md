# Acceptance: dotfiles-T90-github-identity-separation-a01

- **Decision:** ACCEPTED (objective revised; mechanical merge restriction → T90b). PR #262 squash-merged to `main` as `4c38dea0`; final head `e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 18:22Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8, `security` profile). task_rev verified at dispatch and after each PONG-decision append.
- **Exemption declared:** acceptance and final integration; evidence sync (seven worker artifacts copied from worker-e).
- **Plan reference:** added task from the T64 audit P1 and the operator decision 「account を役で分ける」; trust-boundary work on the Codex `security` seat per the model-selection rule.

## What was accepted (PR #262, final head `e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd`; diff commits a8151c9a, 507e9c15 and e2d5c9a3, three update-branch merges; 13 files, +535/−12)

- **Manifest and renderer:** `worker_gh_config_dir` (default `~/.config/gh-worker`) rendered as `WORKER_GH_CONFIG_DIR` into `model-profiles.env`, validated as an absolute or `~/` path without control characters.
- **Launcher (`herdr-agents`):** every worker hand-off selects the worker gh config: the pair worker pane gets `unset GH_TOKEN GITHUB_TOKEN …; export GH_CONFIG_DIR=…` after its shell prompt; spawn-seated workers (`--add-worker`) go through a narrow exported `herdr` adapter in the `spawn.sh` subprocess that adds `--env` on `tab create` and prefixes the boot command on `pane run`; Codex workers also get `-c shell_environment_policy.set.GH_CONFIG_DIR=…` (worker-only, `inherit=core` drops the variable). The orchestrator pane keeps the default gh config.
- **Doctor (`scripts/check-tools.sh`):** missing worker dir → optional warning naming the operator step; existing dir → required: user-owned 0600 `hosts.yml`, active file-stored token (`gh auth status --json hosts`; supported by the deployed gh 2.101.0), worker dir distinct from the default dir, worker login distinct from the orchestrator login.
- **Gate (`scripts/require-crit-review.py`):** `github_identity_errors` is active only when the worker `hosts.yml` exists and the effective `main` rules require at least one approval; otherwise it prints a `notice:` and passes (so acceptance is not stranded before the operator provisions). When active: current login ≠ PR author, and the current login's latest decisive review must be `APPROVED` on the current head; malformed or failed GitHub responses fail closed.
- **Documents:** README ruleset payload kept as a **draft the operator must not apply yet** (e2d5c9a3: required approval alone lets an approved worker PR be merged by its author and blocks orchestrator-authored boundary PRs; T90b designs the `update` restriction with the orchestrator as sole `pull_request`-mode bypass actor and the activation order), roles section, operator phase (orchestrator login in the default config, worker login into the worker dir with `--insecure-storage`, `setup-git`, `auth status`, `make doctor`, then stop until T90b); SKILL Orchestrator step 10 approves the final head before the sweep once the role setup is active; one pr-integration rule bullet.
- Tests: launcher env propagation (fake CLI), doctor absence/security/auth cases, gate inactive/active/stale/dismissed approval; 778 unit tests pass; `make render-check` clean; shellcheck/shfmt clean per the report.

## Decisions taken during the task

- Revise round 1 (audit of 507e9c15): the objective is revised — this task delivers role separation and approval gating; the mechanical "only the orchestrator merges" guarantee becomes T90b (ruleset `update` restriction on `main` with the orchestrator account as the sole `pull_request`-mode bypass actor, which also lets orchestrator-authored boundary PRs merge without self-approval). The README keeps the required-approval payload as a draft and tells the operator not to apply it until T90b, because alone it still lets an approved worker PR be merged by its author and blocks boundary PRs.

- PONG 1: the env hand-off adapter and the worker-only Codex `shell_environment_policy` override are identity routing, not sandbox/approval/permission policy, so the Codex seat may implement them (recorded in the task file).
- PONG 2: `main` held for PR 262 after the orchestrator's boundary commit #263 moved it; one update-branch, no repeated Bot wait.
- Codex P2 4178600965 (retire the T97 sandbox exception once provisioned): not applicable at this merge — the credential is provisioned by the operator afterwards, so the exception text stays true until then; rewording it to name the operator phase and retiring it per provisioned host is T83 work. Replied and resolved by the orchestrator.
- Worker-proposed `[memory:decision]` wording accepted with the activation condition made explicit (see CompactionDB).

## Orchestrator re-derivation

- Read the launcher, doctor, gate, renderer, manifest, README, SKILL and rule diffs in full. Checked: the gate's inactive path prints a notice and returns no error (so today's acceptances keep passing: no worker `hosts.yml` exists on this host); the active path reads `rules/branches/main`, the PR author, and paginated reviews, and fails closed on malformed data; the doctor's optional/required split matches the PONG-1 instruction; `gh auth status --json` exists in gh 2.101.0.
- Residual by design: the spawn adapter intercepts the upstream agmsg Herdr driver's `herdr tab create`/`pane run` calls by an exported function; an upstream driver change that calls the binary by path would silently skip the env hand-off (the doctor's two-login check and `gh api user` in the worker pane catch that at provisioning time; the README says to confirm the worker login after restarting workers).
- CI 13/13 green on 507e9c15 and on e2d5c9a3; PR `clean`; branch on `main` 8cd66881 (no further update-branch needed).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, 507e9c15 (round-0 head) | incorrect (3) → P1/P2 answered by the objective revision and the README hold in revise round 1 (T90b carries the mechanical restriction); the CompactionDB item is recorded by the orchestrator below |
| task-level, final head e2d5c9a3 | correct (no actionable findings) |

- Sweep (head e2d5c9a3; same 9 items): see the masked copy `.orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json`; every item `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`; the worker's `…-worker-crit.json` and `…-worker-review-receipt.md` kept as task evidence.

## Operator phase (not performed by this acceptance)

1. `make update` in the canonical clone (deploys the launcher, doctor and gate), then the README operator phase: authenticate the orchestrator's default gh config with the merging account; `GH_CONFIG_DIR=$HOME/.config/gh-worker gh auth login --insecure-storage` with the write account; `chmod 600 hosts.yml`; `gh auth setup-git`; `make doctor` must report two different logins.
2. **Stop there until T90b** (do not apply the draft payload); T90b specifies the ruleset shape, the activation order and the scratch-PR checks.
3. After T90b: `herdr-agents --restart-worker` (and `--remove-worker`/`--add-worker` for the extra seats) so the running workers pick up `GH_CONFIG_DIR`; confirm `gh api user --jq .login` in a worker pane returns the worker login.
4. From then on the orchestrator approves each final head (`gh pr review <pr> --approve`) before the sweep, as SKILL step 10 now says.

## Follow-ups

- T83: reword the Worker Playbook / rule sandbox exception to "until the worker gh credential is provisioned on this host (README operator phase)" and retire it where provisioned.
- T77b (Codex seat): `enforce-uv.sh` PreToolUse contract.

## CompactionDB

- Orchestrator consolidation `9580d38f-8914-427b-a87e-7477640a265b` (the worker could not write the main-checkout DB from its worktree; its proposed text is in the report).
