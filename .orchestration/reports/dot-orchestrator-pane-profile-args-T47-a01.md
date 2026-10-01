# Report: dot-orchestrator-pane-profile-args-T47-a01

- status: ready_for_review
- worker: claude-standard-dot-a005
- PR: https://github.com/mryfmo/dotfiles/pull/217 (`fix/orchestrator-pane-profile-args` → `main`), mergeStateStatus CLEAN, all CI checks pass (nix skipped by its path filter)
- head sha: `710379737e7969c326922789b6f38c4df24b75c3` (one commit on `origin/main` `fa5ce03`)
- cost: ~136k context tokens consumed (session budget counter; no per-task figure exposed)

## Changes

1. `home/dot_local/bin/common/executable_herdr-agents`, `start_claude_in_pane`:
   - resolves `MODEL_PROFILE_INTERACTIVE` from `~/.agents/model-profiles.env`. It is shadowed to `""` first, so the file is the only source, the same way `resolve_worker_profile` works;
   - reads `MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS`, using `tr` for the upper-casing to keep bash 3.2 compatibility;
   - appends the `HERDR_AGENTS_CLAUDE_ARGS` words after the profile args;
   - starts the agent with one `start_agent_in_pane` call using the `${arr[@]+"${arr[@]}"}` idiom, replacing the old if/else;
   - then prints `orchestrator_profile=<name|none> args=<final args|none>` to stdout.

   Both call sites (full mode and the `--attach` heal) go through this function. There is no second code path. The shdoc header updates `@arg HERDR_AGENTS_CLAUDE_ARGS` to say it is "appended after the interactive profile args" and adds one `@description` sentence naming `MODEL_PROFILE_INTERACTIVE` as the orchestrator pane's profile source.
2. `tests/unit/test_herdr_agents.py`:
   - adds the `write_deep_interactive_profile` helper;
   - `test_orchestrator_pane_uses_interactive_profile_args` pins `agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 -- --model claude-fable-5-1 --effort high --advisor fable`;
   - `test_orchestrator_pane_appends_claude_args_after_profile_args` pins the tail `… --advisor fable --model haiku --effort low`.

   Both tests also pin the exact summary line. `test_claude_agent_accepts_manifest_profile_arguments_for_e2e` is unchanged and still green, because its HOME has no env file.

## Deviations and choices (please review)

- **Subshell instead of the task's "same pattern as `start_worker_agent`".** `start_worker_agent` sources the env file into the script globals. In full mode `start_claude_in_pane` runs before `prepare_worker_seat` and `start_worker_agent`, so a global `source` there would overwrite `HERDR_AGENTS_WORKER_PROFILE` and `HERDR_AGENTS_WORKER_KIND` after they were resolved with env overrides at startup. Example: the file says `express`, the env says `deep`, and the worker would get `express`. That is exactly what `test_worker_profile_env_override_wins_over_generated_worker_profile` pins. Two small `$( … )` subshells keep the globals untouched.
- **`args=` prints the final forwarded list** (profile args plus the override), not only the profile args, so the line shows which model p1 actually got.
- **Missing key is not an error.** A profile is set but `MODEL_PROFILE_<P>_CLAUDE_ARGS` is absent. The start then gets no profile args and prints `orchestrator_profile=<p> args=none`, matching `start_worker_agent`'s `${!key:-}`. `test_codex_profile_defaults_to_generated_interactive_profile` covers this path (`INTERACTIVE=review`, no key) and stays green.
- **User-visible impact:** with the live manifest (`MODEL_PROFILE_INTERACTIVE="deep"`), the next `herdr-agents` full or `--attach`-heal start of p1 passes the `deep` profile's `--model`/`--effort`/`--advisor` args. A bare `claude` outside `herdr-agents` is unchanged, as the task scoped it.
- **Formatter churn removed.** A PostToolUse formatter hook reformatted the whole test file (a 783-line diff). I amended the commit to contain only the 43 added lines. The pre-amend commit `c333a6a` was never pushed.

## Validation

All output is verbatim in `.orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01.md`:

- `make unit-test`: 612 tests OK, 1 skipped;
- `make validate-agent-assets`: ok;
- `shellcheck`: exit 0;
- `git diff --stat`: 2 files, +74/−9;
- `gh pr view` and `gh pr checks`.

No local bats. No live pane was read or driven.

## CompactionDB

[memory:decision] T47: `herdr-agents` starts the orchestrator pane with `MODEL_PROFILE_<MODEL_PROFILE_INTERACTIVE>_CLAUDE_ARGS` from `~/.agents/model-profiles.env`, then appends `HERDR_AGENTS_CLAUDE_ARGS`; a `settings.json` model alone loses to an organization default with `override_user_selection` (observed 2026-09-30, session e7734322 on Sonnet 5.5 while settings said fable-5-1).

Command executed in worker-c (memory id `5ff92e5b-729f-4586-85b5-3534c2f6a2df`, also in the validation file):

```bash
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T47: \`herdr-agents\` starts the orchestrator pane with \`MODEL_PROFILE_<MODEL_PROFILE_INTERACTIVE>_CLAUDE_ARGS\` from \`~/.agents/model-profiles.env\`, then appends \`HERDR_AGENTS_CLAUDE_ARGS\`; a \`settings.json\` model alone loses to an organization default with \`override_user_selection\` (observed 2026-09-30, session e7734322 on Sonnet 5.5 while settings said fable-5-1)."
```

This went into the worker-c worktree DB, which is disposable. At acceptance, the orchestrator still has to consolidate the decision into the main worktree DB.

## Not done / left to the orchestrator

- No merge, no `--delete-branch`, no acceptance record.
- No CodeRabbit review was requested (automatic reviews are disabled).
- The `scripts/pr-feedback.py` sweep and `make require-crit-review` belong to the orchestrator's integration step.
- The T47 artifacts under `.orchestration/` are left uncommitted for the boundary sync. The untracked T45 sandbox record was not touched.
- Two earlier sandboxed `make validate-agent-assets` attempts failed (the sandbox blocked `files.pythonhosted.org` for `uv run --with pyyaml`). The sandbox record describes them, but their output is not in the validation file. The unsandboxed runs, before and after the artifacts were written, both passed.
- T45 (`fix/plain-start-visibility`, PR #216) is ready to resume. Worker-c is now on `fix/orchestrator-pane-profile-args`.
