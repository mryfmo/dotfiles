# dotfiles-T79-remove-adh-profile-a01 — report (status: ready_for_review)

- PR: #267 (https://github.com/mryfmo/dotfiles/pull/267), branch `chore/remove-adh-profile`.
- Diff commit: `c86eb99a`, on `origin/main` 36ffe6ca.
- Final head: `123bf104`, the `gh pr update-branch` merge of main 8ba3c8bc (#266).
- CI: all 13 checks pass on the final head, and `mergeable_state` is `clean`.
- Codex Bot: no review and no inline finding within the window. The connector left only a +1 reaction.

## Changes (allowed files only)

1. `home/dot_agents/agent-config.yaml`: the `model_profiles.adh` block and its two comment lines are deleted. The deleted comment referred to a `profiles/model_profiles.json` validation view that does not exist in the repository. No other profile changed.
2. `scripts/generate-agent-configs.py`: `ADH_PROFILE`, `validate_adh_profile` and its call in `parse_manifest` are deleted. The six remaining profiles render byte-identically: in `home/dot_codex` and `model-profiles.env`, only the adh source and the two `MODEL_PROFILE_ADH_*` lines change.
3. `scripts/validate-agent-assets.py`:
   - `ADH_PROFILE`, `validate_adh_profile` and its call in `main` are deleted;
   - the profile-set check is `set(profiles) != required_profiles`, with the message "must define the six base profiles and no others" (it keeps the phrase `test_agent_manifest_rejects_missing_audit_profile` pins);
   - no `MODEL_PROFILE_ADH_*` token is expected anywhere.
4. `scripts/check-agent-runtime.py`:
   - `ADH_PROFILE_BLOCK` and `manifest_policy_failures` (its regex and adh-only check) are deleted;
   - `check()` now starts from an empty failure list;
   - `re` is still used elsewhere (ruff F401 passes).
5. `home/dot_codex/modify_private_adh.config.toml` is deleted, and `home/.chezmoiremove` gains `.codex/adh.config.toml` next to the other `.codex/` entry. `test_chezmoiremove_agmsg.py::RETIRED` lists no `.codex/` path, so per the task it is unchanged.
6. `home/dot_agents/model-profiles.env` is regenerated without the `MODEL_PROFILE_ADH_*` lines, and `make render-check` is clean. No other rendered profile view exists.
7. Tests: no unit test named the profile before. New `test_agent_manifest_rejects_the_retired_adh_profile`: a manifest with an extra `adh` profile fails validation. The old predicate accepted it, the new one rejects it.
8. README and docs name no `adh` profile, so there is nothing to list for T83.

## Reporting notes

- Main moved to 8ba3c8bc (#266, the `enforce-uv.sh` contract fix) after the first CI run. `gh pr update-branch` merged it cleanly. I re-ran CI, `make render-check`, `make validate-agent-assets` and `make unit-test` on the merged head: 790 tests OK; the count includes #266's tests.
- Evidence repair: zsh `echo` turned the `\b` in my recorded grep command lines into backspace characters. I restored them to the literal `\b` that ran before pasting. The outputs are unaffected.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)
