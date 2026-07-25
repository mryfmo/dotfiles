# Orchestration task: T31 Codex profile modify\_ pattern + agmsg store allowlist

## Assignment

- Task ID: `T31-codex-profile-modify-pattern`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- The main worktree is dirty with UNRELATED changes (`home/dot_mise/*`,
  untracked T30 artifacts). Create a separate git worktree from `origin/main`
  (e.g. `git worktree add ../dotfiles-t31 -b fix/codex-profile-modify
origin/main`) and do ALL work there.

## Problem (verified by orchestrator, 2026-07-25)

`make doctor` fails with `runtime=failed` for two reasons:

1. Codex appends runtime state (`[hooks.state]` trusted-hash sections) to the
   deployed `~/.codex/standard.config.toml`. The four profile configs
   (`standard`, `deep`, `express`, `review`) are generated as PLAIN chezmoi
   files, so (a) `check-agent-runtime.py` `same_text()` exact comparison
   fails permanently once Codex records hook trust, and (b) `make update`
   (chezmoi apply) overwrites the deployed profile, wiping Codex's hook
   trust state. The repo already solves this exact problem for
   `~/.codex/config.toml` via `home/dot_codex/modify_private_config.toml`
   (managed-key merge preserving RUNTIME_PREFIXES including `hooks.state`),
   checked with `same_modified()`.
2. `check-agent-runtime.py` `AGMSG_RUNTIME_IGNORES` allowlists `agmsg/db`
   but not `agmsg/db-flue-pi`, so the rules-sanctioned cross-project
   separate store fails the shared-skill-directory check with
   "unexpected files".

## Desired behavior

1. `scripts/generate-agent-configs.py` emits each Codex profile as a chezmoi
   `modify_` script (target stays `~/.codex/<profile>.config.toml`) using
   the same managed-key-merge approach as
   `home/dot_codex/modify_private_config.toml`: managed keys (`model`,
   `model_reasoning_effort`, header comments) come from
   `agent-config.yaml`; runtime sections with prefixes at least
   `hooks.state` (reuse the existing RUNTIME*PREFIXES set for consistency)
   are preserved from the current target content. The emitted scripts must
   be self-contained executables like the existing modify script. Remove
   the plain `home/dot_codex/<profile>.config.toml` sources. Decide and
   report whether the `private*` attribute is warranted (the deployed
   standard profile is currently mode 600 after Codex rewrote it).
2. `scripts/check-agent-runtime.py` checks the four profiles via
   `same_modified()` (as for config.toml) instead of `same_text()`.
3. `AGMSG_RUNTIME_IGNORES` matching treats `agmsg/db` as a PREFIX so
   `agmsg/db-flue-pi` (and future `agmsg/db-<project>` stores) are ignored;
   keep the other entries exact. Add a brief comment naming why (separate
   stores per agmsg-orchestration rules).
4. Update every script that references the plain profile paths
   (`validate-agent-assets.py`, `update-agent-assets.sh`, others you find
   via grep) so generation, validation, doctor, and update stay coherent.
5. Tests updated FIRST in the same commit(s): extend
   `tests/unit/test_generate_agent_configs.py` (emitted modify script:
   executable, produces managed content on empty stdin, PRESERVES a
   `[hooks.state]` section fed via stdin) and the check-agent-runtime tests
   if present (db-prefix ignore; profile check via same_modified). Follow
   the files' existing mocking style. Do NOT run bats locally.

## Constraints

- allowed*files: `scripts/generate-agent-configs.py`,
  `scripts/check-agent-runtime.py`, `scripts/validate-agent-assets.py`,
  `scripts/update-agent-assets.sh`, `home/dot_codex/*` (profile sources and
  any new modify* scripts; do NOT change `modify_private_config.toml`
  behavior except extracting shared constants if truly needed),
  `tests/unit/test_generate_agent_configs.py`,
  `tests/unit/test_check_agent_runtime*.py` (if present), plus the expected
  artifact paths below (MAIN worktree). STOP if coherence requires edits
  outside this set; report the surface instead.
- forbidden_actions: `edits-outside-allowed-files; git-push (until
orchestrator authorizes); chezmoi-apply; live-herdr-mutation;
mutating-real-HOME-dotfiles; deps-or-ci-changes; local-bats; llm-calls`
- Commit(s) on `fix/codex-profile-modify` with Conventional Commit messages
  in English (suggested: `fix(agents): preserve codex runtime state via
modify profiles`).

## Validation commands (full output into the validation artifact)

- `uv run pytest tests/unit/test_generate_agent_configs.py` (plus any other
  touched test modules)
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- `uv run python scripts/generate-agent-configs.py --check` (or the
  regeneration idempotency mode the script provides — record it)
- Simulated modify run: pipe a target containing a `[hooks.state]` section
  into the emitted standard-profile modify script with
  `CHEZMOI_SOURCE_DIR`/`CHEZMOI_HOME_DIR` set to the worktree fixtures and
  show `hooks.state` is preserved and managed keys corrected
- `shellcheck` + `shfmt -d` for `scripts/update-agent-assets.sh` if edited
- `git status --short` (clean scope)

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T31-codex-profile-modify-pattern.md`
- validation: `.orchestration/validation/T31-codex-profile-modify-pattern.md`
- sandbox: `.orchestration/sandboxes/T31-codex-profile-modify-pattern.md`
- learning: `.orchestration/learning/T31-codex-profile-modify-pattern.md`
- autoskill: `.orchestration/autoskill/runs/T31-codex-profile-modify-pattern.md`

## STOP conditions

- chezmoi modify\_ semantics cannot express a generated per-profile merge
  (e.g. naming/attribute conflict with existing targets) → STOP and report.
- Coherence requires editing files outside allowed_files → STOP and report.

When done send:
`AGMSG-RESULT v1 task_id=T31-codex-profile-modify-pattern status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=... worktree=... branch=... commit=...`
Max turns: 25.
