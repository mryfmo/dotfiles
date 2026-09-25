# AGMSG-TASK dot-update-convergence-T1-a01 — make update convergence fixes

## Objective

Three defects surfaced by the operator's `make update` run (verbatim log excerpts below). Fix each at its root, on a fresh branch from `origin/main`, in a NEW worktree so the pending `herdr-sheldon` work is not touched.

### Defect 1 — `~/.claude/settings.json` SessionStart matcher flips on every `make update`

```
chezmoi apply --verbose
diff --git a/.claude/settings.json b/.claude/settings.json
-        "matcher": "^(startup|resume|clear|compact|fork)$",
+        "matcher": "*",
```

Cause: `home/.chezmoitemplates/claude-settings-managed.json` defines the `herdr-agent-state.sh session` SessionStart entry with `"matcher": "*"`. The herdr 0.9.1 binary (`make update` → "installed claude integration hook … ensured claude settings") rewrites the same entry with matcher `^(startup|resume|clear|compact|fork)$`. `home/dot_claude/modify_private_settings.json` replaces the managed entry wholesale, so chezmoi and herdr fight forever. The two matchers are semantically equivalent.

Fix: change the managed template matcher for that entry to `^(startup|resume|clear|compact|fork)$` so both writers converge. Update `tests/unit/test_claude_settings_merge.py` expectations accordingly.

### Defect 2 — `make update` notice is misleading when the index has unmerged files

```
Notice: local source not pulled (tracked files have staged or unstaged changes); run 'git -C /Users/mryfmo/Workspace/dotfiles pull' to fetch remote updates.
❯❯❯ git pull
error: Pulling is not possible because you have unmerged files.
```

Fix: in the `update` target of `Makefile`, before the dirty check, add one `elif` that detects `git ls-files -u` non-empty and sets reason to e.g. `index has unmerged files; resolve the conflict (git add/commit or git reset) before pulling`. Keep the existing message for the plain-dirty case. Cover it in `tests/install/common/lifecycle.bats` next to the existing "not pulled" case (see line ~95) and `tests/unit/test_runtime_health.py` if it asserts the notice text.

### Defect 3 — false "Multiple agmsg Claude Code identities" warning

```
Multiple agmsg Claude Code identities are registered for /Users/mryfmo/Workspace/dotfiles; worker identity is ambiguous.
```

Cause: `home/dot_local/bin/common/executable_herdr-agents` (~line 480-490) treats a multi-line `identities.sh` output as ambiguous, but `identities.sh` prints one `team<TAB>name` row per team. The SAME name `claude-deep-dot` registered in two teams (adh-v4, dotfiles-conformance — both live regimes) is not ambiguous. Fix: de-duplicate on the name column (second field) before the multi-line test; warn only when distinct names > 1. Add/adjust a case in `tests/unit/test_herdr_agents.py`. Do NOT change the "No agmsg Codex identity" message.

## Scope / allowed_files (all paths under the new worktree)

- Create worktree: `git -C /Users/mryfmo/Workspace/dotfiles worktree add .claude/worktrees/update-convergence -b fix/update-convergence origin/main`
- Edit only:
  - `home/.chezmoitemplates/claude-settings-managed.json`
  - `Makefile` (update target only)
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `tests/unit/test_claude_settings_merge.py`
  - `tests/unit/test_herdr_agents.py`
  - `tests/unit/test_runtime_health.py` (only if the notice text is asserted there)
  - `tests/install/common/lifecycle.bats`
  - `.orchestration/**` artifacts listed below (write them in BOTH `.claude/worktrees/update-convergence/.orchestration/` — no, write ONLY under the `herdr-sheldon` worktree `.orchestration/` paths named in the task message, which is where the orchestrator reads them)

## Forbidden actions

- no git commit, no push, no PR (orchestrator integrates)
- no local `bats` runs (CI only); unit tests via `uv run pytest tests/unit/...` are allowed
- no `make update` / `chezmoi apply` against the operator's `$HOME`; no mise config/lock changes; no changes to the `herdr-sheldon` worktree files
- no new dependencies; keep diffs minimal (Ponytail)

## Validation (paste verbatim output into the validation file)

1. `uv run pytest tests/unit/test_claude_settings_merge.py tests/unit/test_herdr_agents.py tests/unit/test_runtime_health.py -q`
2. `shellcheck home/dot_local/bin/common/executable_herdr-agents && shfmt -d home/dot_local/bin/common/executable_herdr-agents`
3. Idempotency proof for defect 1 without touching `$HOME`: render the managed template through `modify_private_settings.json` twice with a fixture settings file whose herdr entry carries the regex matcher (use `CHEZMOI_SOURCE_DIR`/`CHEZMOI_HOME_DIR` env), and show the second pass emits byte-identical output.
4. `git -C .claude/worktrees/update-convergence diff --stat`

## Durable facts

- [memory:decision] The managed Claude SessionStart matcher for herdr-agent-state.sh is the herdr canonical regex `^(startup|resume|clear|compact|fork)$`, not `*`, so chezmoi and herdr integrations converge.
- [memory:decision] herdr-agents identity ambiguity is judged on distinct identity names, not on the number of team registrations.

Run `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."` for each and paste the commands into the report.

## Artifacts (exact paths, relative to the herdr-sheldon worktree = your registered project)

- report: `.orchestration/reports/dot-update-convergence-T1-a01.md` (include `cost:` line)
- validation: `.orchestration/validation/dot-update-convergence-T1-a01.md`
- sandbox: `.orchestration/sandboxes/dot-update-convergence-T1-a01.md`
- learning: `.orchestration/learning/dot-update-convergence-T1-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-update-convergence-T1-a01.md`

max_turns=30. Reply with `AGMSG-RESULT v1` when done or blocked.
