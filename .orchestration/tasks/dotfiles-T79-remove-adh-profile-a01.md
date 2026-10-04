# AGMSG-TASK dotfiles-T79-remove-adh-profile-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T79; operator decision: the `adh` profile is deleted). Depends on T78 (AGENTS.md ADH section). Seat: a **Codex** worker, because `scripts/generate-agent-configs.py` is on the routing list (every emitter of a Claude seat's boundary goes to Codex or the operator, T88).

## Objective

1. `home/dot_agents/agent-config.yaml:65-71`: delete the `adh` model profile.
2. `scripts/generate-agent-configs.py`: delete `ADH_PROFILE` (~22-30) and the `model_profiles.adh` check (~134-137); the `adh` entry no longer renders into `model-profiles.env` or a Codex profile file.
3. `scripts/validate-agent-assets.py`: delete `ADH_PROFILE` (~69) and `validate_adh_profile` (~721-726 and its call); the profile-set check (~638-639) requires exactly the six base profiles.
4. `scripts/check-agent-runtime.py`: delete `ADH_PROFILE_BLOCK` (~77-83) and the adh policy check (~338-347 and its call).
5. `home/dot_codex/modify_private_adh.config.toml`: delete; add `.codex/adh.config.toml` to `home/.chezmoiremove` so existing machines drop the rendered file.
6. `home/dot_agents/model-profiles.env`: regenerate (`MODEL_PROFILE_ADH_CODEX_ARGS` disappears); `make render-check` exit 0.
7. Tests naming `adh` (none found by grep at drafting time; confirm with `grep -rn adh tests/`); README mentions of the adh profile, if any, are a one-line removal.

Forbidden: any other profile; pins; permissions/sandbox blocks.

[memory:decision] dotfiles-T79 (operator 2026-10-03): the `adh` model profile and its validators are deleted; `model_profiles` holds exactly the six base profiles, and `.codex/adh.config.toml` is retired through `.chezmoiremove`.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/remove-adh-profile origin/main` (the commit that merged T78 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the adh profile only), `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`, `home/dot_codex/modify_private_adh.config.toml` (delete), `home/.chezmoiremove`, `home/dot_agents/model-profiles.env`, `README.md` (adh mentions only), `tests/unit/**` files that name `adh`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T79-remove-adh-profile-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rn "adh\b\|ADH" home scripts tests README.md | grep -v worktrees ; echo "rc=$?"
make render-check
make validate-agent-assets
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Live acceptance (orchestrator, after merge and `make update`): `make doctor` exit 0 and `~/.codex/adh.config.toml` absent.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)` (keep this trailer even from a Codex seat; it marks agent-authored PRs in this repository). CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if a Crit plan review ran.
3. Artifacts at the exact expected paths; validation with verbatim commands and raw output, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T79` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=25.
