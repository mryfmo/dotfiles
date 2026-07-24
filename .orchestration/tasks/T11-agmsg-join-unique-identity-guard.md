# Orchestration task: T11 agmsg join.sh unique-identity guard

## Assignment

- Task ID: `T11-agmsg-join-unique-identity-guard`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles` (work in the current working tree; do NOT create a worktree)
- Base: current `main` working tree. Pre-existing dirty files `home/dot_mise/config.toml` and `home/dot_mise/mise.lock` are NOT yours — do not touch or revert them.

## Background

agmsg identities are stored in `teams/*/config.json` under the skill directory.
The single write path is `join.sh`. Today it enforces nothing: joining an
`agent_id` that already exists in another team silently succeeds. This allowed
an identity-name collision (`codex-gpt56sol-high` reused across ai-ops-platform
and dotfiles-conformance for two different physical agents) that had to be
repaired by rename. Registry best practice (A2A / CSA Agent Registry spec,
2026): agent identity must be authoritative and enforced at the registry write
path, not by operator discipline.

The chezmoi source of the deployed script `~/.agents/skills/agmsg/scripts/join.sh`
is `home/dot_agents/skills/agmsg/scripts/executable_join.sh`. Edit the SOURCE
only. Do not run `chezmoi apply` (orchestrator handles deployment).

## Objective

Make `join.sh` refuse cross-team identity-name reuse by default.

Required behavior (smallest correct diff, ponytail full rules apply):

1. Before adding/extending a registration, scan sibling team configs
   (`$TEAMS_DIR/*/config.json`) for the same `agent_id`.
2. If `agent_id` exists in one or more OTHER teams and the new flag
   `--same-agent` was NOT passed: print to stderr the team(s) where it exists
   and a two-option instruction — (a) choose a project-suffixed unique name
   for a different physical agent, or (b) re-run with `--same-agent` if this
   is genuinely the same physical agent joining another team — then `exit 1`.
   Nothing may be written in this case.
3. With `--same-agent`, or when the name exists only in the SAME team
   (registration extension), behavior is exactly as today.
4. `--same-agent` may appear anywhere in argv; keep the existing positional
   contract `join.sh <team> <agent_id> <type> <project_path>` intact for all
   existing callers (grep callers of join.sh under home/ and .claude/ first
   and confirm none breaks).
5. Update the usage line in the script header comment.

## Test requirement

Add ONE Python unit test file `tests/unit/test_agmsg_join_unique_guard.py`
following the conventions of existing tests in `tests/unit/` (plain pytest,
run with `uv run pytest`). Strategy: copy `executable_join.sh` into a tmp_path
skeleton (`scripts/join.sh` + empty `teams/`), chmod +x, invoke via
`subprocess.run(["bash", ...])`. Cover at minimum:

- join into a new team succeeds (config.json created with the agent).
- second join of the SAME name into a DIFFERENT team fails with exit 1, writes
  nothing to the second team config, and stderr names the conflicting team.
- same scenario with `--same-agent` succeeds.
- re-join of the same name into the SAME team still succeeds (extension path).

Write the failing test first, then the guard. Do not run Bats locally.

## Constraints

- allowed_files:
  - `home/dot_agents/skills/agmsg/scripts/executable_join.sh`
  - `tests/unit/test_agmsg_join_unique_guard.py`
  - the expected artifact paths below
- forbidden_actions: `git-commit-push; chezmoi-apply; deps-or-ci-changes;
edits-outside-allowed-files; network-installs; llm-calls; touching-dot-mise-dirty-files`
- Do not modify the deployed copy under `~/.agents/`.

## Validation commands (record full output in the validation artifact)

- `uv run pytest tests/unit/test_agmsg_join_unique_guard.py -v`
- `uv run pytest tests/unit -q` (no regressions)
- `shellcheck home/dot_agents/skills/agmsg/scripts/executable_join.sh` (if shellcheck is available; record availability either way)
- `git diff --stat` (must show only the two allowed files)

## Expected artifacts

- report: `.orchestration/reports/T11-agmsg-join-unique-identity-guard.md`
- validation: `.orchestration/validation/T11-agmsg-join-unique-identity-guard.md`
- sandbox: `.orchestration/sandboxes/T11-agmsg-join-unique-identity-guard.md`
- learning: `.orchestration/learning/T11-agmsg-join-unique-identity-guard.md`
- autoskill: `.orchestration/autoskill/runs/T11-agmsg-join-unique-identity-guard.md`

## STOP conditions

- Any existing caller of join.sh relies on extra positional args after
  `<project_path>` (flag parsing would break it) → STOP and report.
- The guard cannot be implemented without touching files outside allowed_files → STOP and report.

When done send: `AGMSG-RESULT v1 task_id=T11-agmsg-join-unique-identity-guard status=ready_for_review ...` with all artifact paths.

## Revision 1 (orchestrator review finding — spec defect, task-file authority)

The original spec wrongly mandated pytest. This repository's unit tests run ONLY
via `make unit-test` = `uv run python -m unittest discover -s tests/unit -v`
(see `Makefile:113`). Your pytest-style test (bare functions, `tmp_path`
fixture) is invisible to `unittest discover`: the suite reports green while the
new test never executes — vacuous evidence. Revise:

1. Rewrite `tests/unit/test_agmsg_join_unique_guard.py` as
   `unittest.TestCase` classes (use `tempfile.TemporaryDirectory` /
   `setUp`/`tearDown` instead of pytest fixtures), matching the style of the
   existing `tests/unit/test_require_crit_review.py`. Same four scenarios;
   keep the exact-match/deny assertions.
2. Confirm executability of the guard under macOS `/bin/bash` 3.2: run the
   deny path, the `--same-agent` path, and a zero-argument invocation with
   `/bin/bash` explicitly. Note: `set -- "${POSITIONAL[@]}"` with an empty
   array errors under `set -u` on bash 3.2 — if the zero-arg usage error
   message degrades, guard the expansion (e.g. `${POSITIONAL[@]+"${POSITIONAL[@]}"}`).
3. Replace the validation commands with:
   - `uv run python -m unittest tests.unit.test_agmsg_join_unique_guard -v`
   - `make unit-test` (full suite, no regressions; confirm the new tests appear in the -v listing by name)
   - `/bin/bash --version` + the three bash-3.2 probes above (record output)
   - `shellcheck home/dot_agents/skills/agmsg/scripts/executable_join.sh` (record availability)
   - `git diff --stat`
4. Update report/validation artifacts in place. Then send
   `AGMSG-RESULT v1 task_id=T11-agmsg-join-unique-identity-guard status=ready_for_review ...` again.
