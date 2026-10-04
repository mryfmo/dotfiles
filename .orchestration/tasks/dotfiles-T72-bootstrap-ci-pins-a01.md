# AGMSG-TASK dotfiles-T72-bootstrap-ci-pins-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 3, dotfiles-T72). Depends on T71 (`render:` lists and `declare -r`, PR #249). Dispatch after #249 merges.

## Objective

Principle 3: every version literal that bootstrap and CI use is rendered from `home/dot_agents/agent-config.yaml`.

1. **New asset `chezmoi-bootstrap`** in `agent-config.yaml`: `source: github-release`, `upstream: twpayne/chezmoi`, `pin: 2.70.4` (the current `setup.sh` value; the CI job currently hard-codes 2.70.5, which is the drift this task removes, and the next `make upgrade` moves the single pin), `verify: release-shasums`, render list → `setup.sh` (`CHEZMOI_VERSION`, `declare -r`) and `scripts/lib/installer-pins.sh` (`CHEZMOI_BOOTSTRAP_PIN_VERSION`). Extend `homebrew-installer`'s `render:` to a list that also writes `setup.sh:32-33` (`HOMEBREW_INSTALL_COMMIT`, `HOMEBREW_INSTALL_SHA256`, `declare -r`).
2. **`scripts/upgrade-tools.sh` `bump_release_asset_pins`** (~589): also bumps `chezmoi-bootstrap.pin` from the latest release.
3. **CI**: `.github/workflows/test.yaml:145-156` installs chezmoi from the literal `2.70.5`; source `scripts/lib/installer-pins.sh` and use `CHEZMOI_BOOTSTRAP_PIN_VERSION` (same tarball method for the macOS job at ~140 instead of `brew install chezmoi`, so both platforms run the pinned version). Where workflows pin mise (`mise-action` `version:` or `MISE_PIN`), supply it from `install/common/mise.sh`'s rendered `MISE_VERSION` with a step that writes `MISE_PIN` to `$GITHUB_ENV` (`sed -n 's/^readonly MISE_VERSION="v\(.*\)"$/MISE_PIN=\1/p' install/common/mise.sh`); check `docs.yml`, `ubuntu.yaml`, `macos.yaml` for the same literals.
4. **`Dockerfile`**: `ARG CHEZMOI_VERSION` without a default; `Makefile` `docker` target passes `--build-arg CHEZMOI_VERSION="$(sed -n 's/^declare -r CHEZMOI_VERSION="\(.*\)"$/\1/p' setup.sh)"` (or sources installer-pins.sh).
5. **Validator**: `scripts/validate-agent-assets.py` adds `setup.sh` and `scripts/lib` to the scanned roots now that their literals are rendered (T71 deliberately left them out).
6. Tests: `tests/unit/test_generate_agent_configs.py` (asset renders into two files), `tests/unit/test_validate_agent_assets.py` (setup.sh scanned), the workflow-token tests in `tests/unit/test_supply_chain_policy.py` if they pin the literal.

Forbidden: changing any pin value other than making the chezmoi pin single (2.70.4); `home/dot_mise/config.toml`, `mise.lock`; macOS awscli brew version (declared unpinnable exception).

[memory:decision] dotfiles-T72 (operator 2026-10-03): the chezmoi bootstrap version, the Homebrew installer commit/sha, and the mise version used by setup.sh, the Dockerfile and every CI workflow render from `agent-config.yaml` assets; no workflow or bootstrap script holds a version literal of its own.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/bootstrap-ci-pins origin/main` (the commit that merged #249 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the two assets only), `setup.sh` (the three rendered lines), `scripts/lib/installer-pins.sh`, `scripts/upgrade-tools.sh`, `scripts/validate-agent-assets.py`, `.github/workflows/test.yaml`, `.github/workflows/docs.yml`, `.github/workflows/ubuntu.yaml`, `.github/workflows/macos.yaml`, `Dockerfile`, `Makefile` (docker target), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_supply_chain_policy.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T72-bootstrap-ci-pins-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rn "2\.70\.[0-9]\|2026\.9\.1[0-9]\|c7952e40" setup.sh .github Dockerfile | grep -v installer-pins ; echo "rc=$?"
make render-check
make validate-agent-assets
bash -n setup.sh
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head (test, docs, ubuntu, macos workflows), branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T72` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 17:05Z to `claude-standard-dot-a005` (worker-c, wT:p2) after its T93 acceptance (PR #251 merged as 2e2e1e09; T71 merged as 65915b93). Branch from `origin/main` 2e2e1e09 or later; keep the earlier branches untouched. `scripts/validate-agent-assets.py` is free (T93 merged); T69 (a006) touches only prose files and `executable_herdr-agents`'s one string, so stay out of README prose beyond the task's named lines. Routing: the validator scan roots and the manifest `assets:` block are neither seat's execution boundary, so a Claude seat is fine.
