# Report: dot-worker-kind-guard-T14-a01 — revision round 1 ready_for_review

- Worker: claude-standard-dot-a003
- Worktree: `.claude/worktrees/env-converge-T10`, branch `fix/worker-kind-guard` from origin/main c78f232
- **PR: https://github.com/mryfmo/dotfiles/pull/180**, head aa17407, CI all green (nix skipped as on main), not merged
- **Commits:**
  - `3be8b86` fix(validate): constrain worker_kind and keep README in step with the manifest
  - `3326e83` fix(herdr-agents): refuse a same-type worker that would share the orchestrator agmsg identity
- Evidence: `.orchestration/validation/dot-worker-kind-guard-T14-a01.md`
- **Push authorization:** the operator's earlier STOP ("no more pushes") reached this session directly, so before pushing I asked the operator in-session. They answered "Push and open PR".

## Preparation

- The uncommitted bats fixture fix was committed on the parked branch `feat/claude-sandbox-manifest` as `3857331` `test(install): capture the fake sudo log on stderr in bwrap_apparmor.bats`, touching only that file.
- **Not pushed:** origin/feat/claude-sandbox-manifest is still `b729f54`, so PR #179 does not contain the fix yet.
- `git switch -c fix/worker-kind-guard origin/main` was run inside the nested worktree. The main checkout stayed on `main`.

## 1.2 validator and README

- `validate_agent_manifest` fails unless `worker_kind` ∈ {codex, claude} (so a missing key fails), and unless README.md contains ``(currently `<value>`;``. The live repo passes with `claude`.
- README L328 now matches `resolve_worker_profile`: `HERDR_AGENTS_WORKER_PROFILE`, then the deprecated `HERDR_AGENTS_CODEX_PROFILE`, then `MODEL_PROFILE_INTERACTIVE` from `~/.agents/model-profiles.env`, with `standard` only when that file does not set it.
- **Tests:**
  - Positive: the existing `test_agent_manifest_accepts_exact_security_profile_set`, whose fixture now has `worker_kind: claude` and a matching README.
  - Negative: `test_agent_manifest_rejects_invalid_or_missing_worker_kind` (banana, None) and `test_agent_manifest_requires_readme_to_state_the_worker_kind` (codex vs README claude).

## 1.3 herdr-agents guard

**New functions** (shdoc):
- `worker_agmsg_type`: codex → codex, claude → claude-code.
- `distinct_agmsg_identity_count`: counts the distinct column-2 names from `identities.sh`. A missing or failing script counts as 0, so the guard fails closed.
- `require_distinct_worker_identity`: prints the exact message from the task to stderr and exits 2 when fewer than 2 names exist.

**Where the guard runs:** once, right after the workdir and profile are resolved and before any `workspace create`, `pane split`, `agent start` or rename. That covers full mode (new and existing workspace) and `--attach`. With `worker_kind=codex` it returns immediately. `--bootstrap-agmsg` mode is not guarded, because it never starts a worker.

**`bootstrap_agmsg`:**
- With a claude worker (via `resolve_worker_kind`), it checks only `claude-code` and treats up to 2 distinct names as healthy (3 or more warns "Multiple … ambiguous").
- It skips `delivery.sh set turn codex`, so `.codex/hooks.json` is not created, and it doesn't print the "No agmsg Codex identity" hint.
- Codex-worker behaviour is unchanged (limit 1 per type).

**Tests (`tests/unit/test_herdr_agents.py`):**

| Case | Test |
|---|---|
| (a) claude kind + one claude-code identity, full and attach modes: exit 2 with the message; no workspace create, split or agent start | `test_claude_worker_sharing_the_orchestrator_identity_is_refused` |
| (b) claude kind + two identities: proceeds | `test_claude_worker_with_a_registered_worker_identity_proceeds` |
| (c) codex kind: unaffected | `test_codex_worker_is_not_subject_to_the_identity_guard` |
| (d) bootstrap, claude kind, two names → no warning; three → warning | `test_bootstrap_with_claude_worker_accepts_two_claude_identities` |
| (e) bootstrap, claude kind: no `.codex/hooks.json`, no Codex hint, no codex delivery or identity calls | `test_bootstrap_with_claude_worker_leaves_codex_hooks_alone` |

- The 7 existing claude-worker tests now call the new `register_claude_worker_identity()` helper. Three of them got `mkdir(exist_ok=True)`, because the helper already creates `~/.agents`.
- `run_agmsg_bootstrap_helper` gained `extra_env` and drops an inherited `HERDR_AGENTS_WORKER_KIND`, so the bootstrap tests don't depend on the caller's environment.
- **Mutation check:** with the guard call removed, case (a) fails in both modes. The file was restored byte for byte, with mode 100644 unchanged.
- **Bats:** no bats file covers `herdr-agents` (`grep -rln herdr-agents tests --include='*.bats'` exit 1), so no bats case was added.

**README:** one sentence in the herdr-agents paragraph documents the temporary guard, in the herdr-agents commit.

## Validation summary

- `uv run --with pyyaml scripts/validate-agent-assets.py`: ok.
- `python3 -m unittest tests.unit.test_herdr_agents tests.unit.test_validate_agent_assets tests.unit.test_generate_agent_configs -q`: 142 tests OK.
- Full suite `uv run python -m unittest discover -s tests/unit`: 417 OK, 1 skipped.
- shellcheck and shfmt: clean.
- `git diff --stat origin/main...HEAD`: 5 files, +215/−10, all within allowed_files.
- `gh pr checks 180`: every check passes, nix skipping.

## Notes for acceptance

- `worker_kind` stays `claude`. With it, **the operator's current setup is refused by `herdr-agents`** unless a second claude-code identity is registered on the project, which is the intended safety stop. Any automatic `herdr-agents --attach` from the SessionStart hook will log the refusal to `~/.config/herdr/herdr-agents.log` (that hook ends with `|| true`).
- The guard message names `remediation-plan-20260925.md`. That plan lives in the gitignored `.agents/worklog/claude/`, so readers of the public repo can't open it.
- The commit trailers use `Claude Opus 5.5`, the model this session actually runs on.

## Revision round 1 (orchestrator review of PR #180)

All three should-fix items and the nits are fixed in the same PR:
- `01b38be` fix(herdr-agents): state what the identity guard does and does not fix
- `aa17407` test(herdr-agents): compare against the resolved workdir in the bootstrap hint test

**Head:** `aa17407b680691a42f421721479d7cd14c4421fa`. **CI all green** (nix skipped), including `test (macos-14, client)`.

| Review item | Fix |
|---|---|
| (1) The message and README implied that registering a second identity gives distinct routing | The message now says registering a second identity "lifts this guard but does not give the two sessions distinct delivery until agmsg roles land; use worker_kind=codex for separate delivery now". README says both sessions still resolve to the same inbox (`whoami.sh` reports multiple identities, `check-inbox.sh` takes the first); both claims were verified in the installed scripts (validation). |
| (2) `--bootstrap-agmsg` was silent with a claude worker and one claude-code identity | New hint `No agmsg Claude Code worker identity for <workdir>; herdr-agents full and --attach modes refuse a claude worker until a second claude-code identity is registered.` New test `test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity` also asserts no hint for a codex worker. |
| (3) PR body and README must state the SessionStart consequence | README and PR body (edited) now say that with `worker_kind: claude` applied by `make update`, the SessionStart `herdr-agents --attach` hook exits 2 on every session start in a Herdr pane outside a `herdr-agents`-managed layout. It only logs to `~/.config/herdr/herdr-agents.log`, until a second identity exists or `worker_kind` is `codex`. "Outside a managed layout" is precise: `--attach` exits 0 before the guard when `HERDR_AGENTS_LAYOUT=managed` or there is no Herdr env. |
| Nits | The gitignored plan citation was removed (`remediation-plan` count 0 in the script and README); the message points to the README herdr-agents section. `join.sh` is shown as `${HOME}/.agents/skills/agmsg/scripts/join.sh`. The workdir is shell-quoted with `%q` in both places. |

**CI incident on `01b38be`:** `test (macos-14, client)` failed because the new hint test expected the unresolved temp path, while herdr-agents prints `pwd -P` (`/private/var/...` on macOS). The Ubuntu `test` jobs were cancelled by fail-fast, not failed. `aa17407` resolves the expected path (the refusal test already did), and also resolves the path in the codex-hooks test's `assertNotIn`, which was vacuous on macOS.

**Local test honesty:**
- I pushed `01b38be` after a full-suite run that reported `FAILED (failures=1)`. The push was chained after `tail`, so the failure didn't stop it; that was my mistake.
- The failure is `test_permgate.test_bench_runs_five_layer_two_fixtures` (`successful_classifications 0 != 5`). Neither permgate nor its test is touched by this PR (empty `git diff`).
- It passes 10/10 in isolation and passes together with test_herdr_agents (125 OK). It failed in 3 of 10 local full-suite runs and passed on every CI runner. That makes it a load-sensitive benchmark flake in this busy host, not a regression.
- From then on the commit gate used the suite's own exit code. The last commit was gated on the three required suites (142 tests OK).

`[memory:decision]` is unchanged (`43e60fb8-2b05-4609-bf5d-1bd6b2657060`); no new memory added.

## Durable facts

[memory:decision] worker_kind is validated to codex|claude and README must state the manifest value; a same-type claude worker is refused unless a second claude-code identity (worker role) is registered on the workdir (temporary guard until the agmsg role model, plan Phase 3)

```bash
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "worker_kind is validated to codex|claude and README must state the manifest value; a same-type claude worker is refused unless a second claude-code identity (worker role) is registered on the workdir (temporary guard until the agmsg role model, plan Phase 3)"
# → 43e60fb8-2b05-4609-bf5d-1bd6b2657060
```

cost: n/a
