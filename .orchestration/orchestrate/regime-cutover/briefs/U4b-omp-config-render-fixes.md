# U4b omp config render: bot findings + apply-time dependency — brief

GOAL
Bring PR #406 (`tools/omp-config-render`, head 63b81a04) to mergeable: fix the three Codex bot P1 findings at root cause, remove the old regime's task-copy files from the PR, and make the chezmoi modify script work on this host where the system `python3` has no PyYAML (today the render is a silent no-op there).

SCOPE
Exclusive worktree on the existing branch `tools/omp-config-render` (fetch from origin; you are its only writer now). May write: `home/dot_omp/private_agent/modify_private_config.yml` (renamed from `home/dot_omp/agent/modify_config.yml`), `tests/unit/test_omp_config_merge.py`, `tests/unit/test_generate_agent_configs.py`, `scripts/generate-agent-configs.py` (only if the rename needs it), `home/dot_agents/README.md` (omp section), and `git rm` of `.orchestration/dotfiles-T129-omp-config-render-a01/{learning,sandbox,task}.md` from this branch. Nothing else (no `model_profiles` value changes, no `assets:`).

CONTEXT
- U4's report: `make render-check` up to date; 198 tests pass in the touched files; schema cited `src/config/model-settings.ts:109`, `src/config/settings.ts:463-469,1626-1639,672-673`, `src/config/model-roles.ts:56-67`; `express` mapped to `claude-bridge/claude-haiku-5-5`; chezmoi dry run on a scratch HOME replaced `modelRoles.default` and kept the other keys when PyYAML was present; with the host's `/usr/bin/env python3` (mise 3.15, no `yaml`) the script printed a pass-through warning and changed nothing.
- Bot P1 (1): move the modify script to `home/dot_omp/private_agent/modify_private_config.yml` so chezmoi creates `~/.omp/agent` 0700 and `config.yml` 0600 (the directory also holds omp's auth databases); the live host already has those modes. Update the test's MERGE_SCRIPT path and the shdoc `@file` line.
- Bot P1 (2)(3): the parked task copy under `.orchestration/dotfiles-T129-omp-config-render-a01/` says two providers and omits the validator from `allowed_files`; those files belong to the agmsg regime that is off for this program (D-024-131); remove them from the PR instead of amending.
- Apply-time dependency (root cause, not a guard): the modify script must not depend on the system interpreter having PyYAML. Preferred: a shell `modify_` script whose body runs `uv run --no-project --with pyyaml python3 - "$@" <<'PY' … PY` (uv is installed on this host and in CI; cite `which uv`), falling back to the pass-through warning only when `uv` is absent. Alternative if chezmoi's modify contract makes that awkward: a `#!/usr/bin/env -S uv run --no-project --with pyyaml python3` shebang, if `env -S` works on macOS and Linux (test both forms in the scratch dry run; cite `man env`). Keep the behaviour test: unrelated keys preserved, `modelRoles.default` replaced, idempotent on a second apply.
- Conventions: shdoc comments in English for the shell parts; tests via `uv run --no-project --with pytest -m pytest …` or the repo's unittest form.

ACCEPTANCE
1. `git show --stat` of your commit(s) shows the rename, the three `.orchestration/...` removals and the test/README edits only.
2. Scratch chezmoi dry run (`HOME=$TMPDIR/u4b-home` via a wrapper script if the harness refuses inline `HOME=`; a config.yml fixture with unrelated keys): the rendered `config.yml` has `modelRoles.default` replaced and every other key intact, with the system `python3` lacking PyYAML (prove it: `python3 -c 'import yaml'` fails in that environment or simulate with `PYTHONNOUSERSITE`/a shim); second apply is a no-op. Paste.
3. Tests: `uv run --no-project --with pytest -m pytest tests/unit/test_omp_config_merge.py tests/unit/test_generate_agent_configs.py -q` (paste); `make render-check` (paste).
4. Push; PR body still carries `Program-Unit: regime-cutover/U4`; reply to nothing on GitHub (the coordinator answers the bot threads with your head sha). CI green except the expected-red `regime` check (paste `gh pr checks 406`).

VERIFY
Commands above. Network: `api.github.com`, `github.com` only.

TIMEBOX
45 minutes.

FORBIDDEN
No `model_profiles` value changes, no `assets:` edits, no real `~/.omp`, no merge, no rebase, no force-push.

REPORT
≤ 150 words: head sha, PR link, CI state, the dry-run evidence (two lines), the interpreter choice and its citation, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (17 lines) before any command.
