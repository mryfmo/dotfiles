# AGMSG-TASK dotfiles-T100-compactiondb-claude-symlink-note-a01

Drafted 2026-10-05 06:50Z by the orchestrator seat (dispatched to `codex-security-dot-a007`, worker-e) from the orchestrator's T81b review observation. Kind: vendor documentation and one unit test; no boundary source.

## Objective

Since 2.0.0+dotfiles.9, `ProjectPaths.ensure()` opens every storage directory with `O_NOFOLLOW`, including the project's `.claude` directory itself. A project whose `.claude` is a symlink therefore fails storage construction, and because the SessionEnd/compaction hooks swallow exceptions, CompactionDB silently records nothing there (no health log can be constructed either). Make this behaviour explicit and tested:

1. `vendor/compactiondb/README.md` ("Storage directory safety" section) and `CHANGELOG.md` (one line under the `2.0.0+dotfiles.9` entry, no version bump: .9 is still the unreleased pin): a project's `.claude` directory must be a real directory; a symlinked `.claude` (or any symlinked storage directory) is refused and the hooks then record nothing. Name the remedy (replace the symlink with a real directory, or opt in from the real path).
2. `vendor/compactiondb/tests/test_paths.py`: add `.claude` itself to the symlink-refusal coverage (a symlinked `.claude` raises `OSError`/`ValueError` from `project_paths(explicit=root)` and leaves the link target untouched).
3. Regenerate `MANIFEST.sha256`; the project copy is unaffected (no runtime code change), state that in the report.

Forbidden: runtime code changes; version bump; touching anything outside `vendor/compactiondb/**`; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T100 (orchestrator 2026-10-05): CompactionDB refuses a symlinked `.claude` project directory by design (no-follow construction) and documents that the hooks then record nothing; the refusal is covered by the vendor path tests.

## Repo / branch

- Work ONLY in your own worktree (worker-e). `git fetch origin`; `git switch -c docs/compactiondb-claude-symlink-note --no-track origin/main` (main at 64167825 or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `vendor/compactiondb/README.md`, `vendor/compactiondb/CHANGELOG.md`, `vendor/compactiondb/tests/test_paths.py`, `vendor/compactiondb/MANIFEST.sha256`.
- Artifacts in your worktree at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T100-compactiondb-claude-symlink-note-a01.md` plus `.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-worker-crit.json` and `-worker-review-receipt.md`; the orchestrator copies them into the main checkout.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -5
make -C vendor/compactiondb test 2>&1 | tail -3
uv run --no-project python -m unittest discover -s vendor/compactiondb/tests 2>&1 | tail -3
(cd vendor/compactiondb && sha256sum -c MANIFEST.sha256 --quiet; echo "rc=$?")
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check vendor/compactiondb/README.md vendor/compactiondb/CHANGELOG.md 2>&1 | tail -3
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL Worker Playbook step 15 (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB: say in the report that the orchestrator records the decision (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T100` via `agmsg-dispatch dotfiles codex-security-dot-a007 claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=20.
