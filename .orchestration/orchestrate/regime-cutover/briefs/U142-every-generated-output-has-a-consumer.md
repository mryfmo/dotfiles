# U142 every generated output has a consumer: the model-profiles env file goes, the statusline chain is stated as it is

GOAL
The generator renders `home/dot_agents/model-profiles.env` "for the launchers" (`home/dot_agents/agent-config.yaml:532`; `scripts/generate-agent-configs.py:1896-1912, 2371`), the validator checks the file and asks the Codex standing rules for its name (`scripts/validate-agent-assets.py:1813-1832`), the README and two rule texts send agents to it (`README.md:466`, `home/dot_config/claude/rules/codex.md:38`, `home/dot_config/claude/rules/model-selection.md:3-4`), and `lifecycle.bats:432` greps it. Nothing consumes it: no launcher under `home/dot_local` or `scripts/orchestrator` sources it or reads a `MODEL_PROFILE_` variable (measured 2026-11-03: `grep -rl 'model-profiles.env\|MODEL_PROFILE_' home/dot_local scripts/orchestrator` lists nothing). The decisions row `generated outputs:` of the store (2026-11-03, phase `truth`) decides: delete the rendering. The statusline half is a measurement, not a change: ccstatusline reads `~/.config/ccstatusline/settings.json`, which `home/dot_config/ccstatusline/symlink_settings.json.tmpl` links to the source `home/dot_ccstatusline/settings.json`, and the `.ccstatusline` ignore line (`home/.chezmoitemplates/chezmoiignore.d/common:9`) keeps only the legacy `~/.ccstatusline` path undeployed; the source has a consumer and the ignore line stays. After this unit the generator renders no env file, the validator asks for none, no rule or document names it, the deployed copy leaves every host through `.chezmoiremove`, the tests state what the generator does now, and no text describes the legacy statusline path as the consumer's path.

SCOPE
One branch `gen/retire-model-profiles-env` from `origin/main`. May write: `scripts/generate-agent-configs.py` (the render function and its output line), `scripts/validate-agent-assets.py` (the env checks and the token), `home/dot_agents/agent-config.yaml` (the comment at lines 530-532 only), `README.md:466`, `home/dot_config/claude/rules/codex.md:38`, `home/dot_config/claude/rules/model-selection.md:3-4`, `home/dot_agents/model-profiles.env` (deleted), `home/.chezmoiremove` (one line outside the generated blocks), the generated outputs the write run re-renders (`scripts/generated-agent-outputs.json`, `home/dot_codex/AGENTS.md.tmpl` and the rule copies), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `tests/install/common/lifecycle.bats:432`, `tests/unit/test_statusline_tools.py:22` (a docstring or comment only, if one calls the file undeployed). No other file; the `express` arguments that the env file carried for Claude move nowhere (the Claude settings baseline already carries the interactive profile).

CONTEXT
Data shape: one generated output, `outputs[ROOT / "home/dot_agents/model-profiles.env"]`, with zero readers. The removal is one wave (Migrate Callers Then Delete): the render function and its output line, the validator's `env_path` block and the `model-profiles.env` token of the Codex standing-rule token list, the four texts, the source file, then the generator write run so the outputs index and the rendered rule copies agree, then the tests. `home/.chezmoiremove` holds hand-written lines outside the generated blocks; `.agents/model-profiles.env` added there makes every host drop the deployed copy on the next apply (`home/dot_agents/README.md:9` describes the same mechanism for retired skill links). The statusline measurement goes into the PR body as a fact with its two paths; the only text edit is any sentence that calls `~/.ccstatusline/settings.json` the deploy target.

CHANGE
1. Remove the render function and its output line from the generator; remove the validator's env checks and token.
2. Remove the file from the manifest comment, the README sentence, the Codex rule and the model-selection rule; `git grep model-profiles.env -- home/dot_agents/agent-config.yaml README.md home/dot_config/claude/rules` prints nothing.
3. Delete `home/dot_agents/model-profiles.env`; add `.agents/model-profiles.env` to `home/.chezmoiremove` outside the generated blocks.
4. Generator write run; `make render-check` exit 0; `grep -n model-profiles scripts/generated-agent-outputs.json` prints nothing.
5. Move the tests: drop the env assertions of `test_generate_agent_configs.py`, the env grep of `lifecycle.bats:432`, any validator test pinning the token; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets` OK; `make validate-agent-assets` exit 0.
6. Statusline: `cat home/dot_config/ccstatusline/symlink_settings.json.tmpl` and `grep -n '^\.ccstatusline$' home/.chezmoitemplates/chezmoiignore.d/common` pasted into the PR body; any text calling the legacy path the deploy target corrected (`grep -rn '\.ccstatusline' home/dot_agents/agent-config.yaml tests/unit/test_statusline_tools.py README.md docs` lists only the source path or nothing).
7. Red proof: on `origin/main` the validator refuses a tree without the env file (delete the file in a scratch archive of `8227cc52` and run `uv run --with pyyaml scripts/validate-agent-assets.py`, paste the ERROR line); on this head the same validator passes with no env file.

ACCEPTANCE
1. `grep -c 'model_profiles_env\|model-profiles.env' scripts/generate-agent-configs.py scripts/validate-agent-assets.py` prints 0 for each. 2. `test ! -e home/dot_agents/model-profiles.env` and `grep -n '^\.agents/model-profiles\.env$' home/.chezmoiremove` prints one line. 3. `make validate-agent-assets` and `make render-check` exit 0. 4. The two test modules OK (paste the Ran lines) and `grep -n 'model-profiles.env' tests/install/common/lifecycle.bats` prints nothing. 5. The red proof. 6. The PR body's Contract states what is left out: the host apply (the operator's step after the merge), and that the statusline source and its symlink template are unchanged.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `prettier --check` on the changed Markdown.

CLOSURE
remove: the consumerless output and every reference to it are removed in one wave; nothing replaces it.

TRUST
TRUST: the unit trusts the measured reader search (no launcher sources the env file) and the chezmoi remove mechanism the repository already uses for retired links; it does not change what the Claude or Codex baselines render for the interactive profile.

TIMEBOX
45 minutes.

FORBIDDEN
No change to `model_profiles` or to what the Claude, Codex or omp baselines render; no `chezmoi apply` or `make update` on the host; no local bats; no edit outside SCOPE; no `gh` call; no mention of any private design directory in files, commits or the PR body.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U142-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U142-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines, the statusline measurement and the red proof), the line `Program-Unit: regime-cutover/U142`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; the store's decisions row `generated outputs:` (2026-11-03); `home/dot_agents/README.md:9, 16-21` (generated outputs and orphans).
