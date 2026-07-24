# Acceptance criteria: T21 model-profiles PR

Status: accepted round 1 (2026-07-23) — next_action=merge sent; awaiting merge+sync RESULT

Round-1 adversarial verification (orchestrator, independently re-derived):

- Content parity: `git diff origin/feat/model-profiles` over all tracked paths = zero drift; 7 new files byte-identical via `git show | diff`; both ccgate.jsonnet absent on branch; 34 changed files exactly; no forbidden paths.
- CI: `gh pr checks 88` = all pass, 1 conditional skip (`nix`), 0 fail. PR #88 OPEN/CLEAN, head aee8903.
- Commits: exactly 2, Conventional English; secret scan over full branch diff clean (only policy prose / env-var name refs).
- Spot re-derivation in the PR worktree: `--check` up to date, test module OK. Worker validation log consistent (180 tests, validate ok).
- Declared deviation (empty staged patch) verified as caused by the orchestrator's earlier `git stash`/`pop`, which flattened the staged deletions into unstaged; transfer remained complete.

## Adversarial checks to run on AGMSG-RESULT (orchestrator)

1. Branch content integrity — refute "the transfer was faithful":
   - `git fetch origin && git diff origin/feat/model-profiles -- <27 tracked files>`
     against the main worktree must be empty.
   - The 7 new files exist on the branch with identical content
     (`git show origin/feat/model-profiles:<path> | diff - <local path>`).
   - Branch must NOT contain `.orchestration/`, `.agents/`, `.crit/`,
     `docs/verification/`, `plans/`, or `/tmp` paths
     (`git diff origin/main..origin/feat/model-profiles --stat`).
   - Deletions present: `home/dot_codex/ccgate.jsonnet`,
     `home/dot_claude/ccgate.jsonnet` absent on the branch.
2. CI truthfulness — refute "CI is green":
   - `gh pr checks <pr>` shows every check pass, including Bats jobs;
     re-derive from `gh run list --branch feat/model-profiles`, do not trust
     the report text alone.
3. Commit hygiene:
   - Exactly 2 commits (plus fixups if CI loops occurred — then squash plan in
     PR is acceptable); Conventional Commit English subjects; no secrets in
     diffs (`git log -p` spot check on env/config hunks: no tokens, no
     credential paths).
4. Report completeness — refute "nothing was omitted":
   - Validation artifact contains real command outputs (unit-test count 180,
     `--check` up-to-date line, validate ok line, shellcheck exit).
   - Any deviation from the task steps is explicitly declared.
5. Independent spot re-derivation: run
   `uv run --with pyyaml scripts/generate-agent-configs.py --check` and one
   unit-test module locally against the branch worktree, not sampled from the
   worker's log.

## Acceptance decision

- All checks pass → AGMSG-ACCEPTANCE status=accepted next_action=merge, then
  verify post-merge sync evidence (guarded reset only with empty diff).
- Any failure → status=revise with narrow reason + next_action.

## Final integration (orchestrator only, after merge + sync)

1. `make update` — expect: chezmoi apply clean, agent assets refreshed, herdr
   reload ok.
2. `make upgrade` — expect: exit 0, pinned http tools skipped, agent CLIs
   repaired with --allow-scripts.
3. `./scripts/check-agent-runtime.py` — expect: only the known pre-existing
   `agmsg/db-flue-pi` failure (tracked separately as W8).
4. `make require-crit-review` on the clean tree.
