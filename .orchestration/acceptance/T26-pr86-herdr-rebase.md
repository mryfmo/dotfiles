# T26 acceptance: PR #86 herdr rebase

- Task: `.orchestration/tasks/T26-pr86-herdr-rebase.md`
- Result: PR [#86](https://github.com/mryfmo/dotfiles/pull/86), rebased head
  `b098ddeb6e1cee836d879621d7fe64aef14e1d14` on `origin/main` (`4e761ba`).
- Verdict: **accepted** (next_action=merge).

## Verification performed

- Independent diff read (both files). PR intent preserved: codex launched via
  launcher-resolved absolute path (fail-closed error if unresolvable) so the
  daemon's stale PATH snapshot cannot pick a shadowed version;
  `remove_shadowing_node_global` purges stray node-global copies only when
  npm, mise, AND the dedicated mise tool install all exist (never deletes the
  only copy), best-effort (`|| true`) so startup never blocks.
- Main-side behavior preserved in the same hunks: manifest-driven
  `--profile "${HERDR_AGENTS_CODEX_PROFILE:-standard}"` launch, two-pane
  repair, and file-viewer behavior.
- Tests: three new fake-npm/mise tests pin purge-on-stray,
  skip-without-stray, and keep-without-mise-tool; 56 herdr tests and 226
  total unit tests green; scope confirmed limited to the two allowed files.
- Live E2E (validation artifact): disposable named session `t26-pr86-e2e`,
  fresh two-pane layout with codex argv showing the resolved mise path
  (0.145.0), client detach/reattach and server stop/attach both restore the
  layout; operator workspace w1C untouched and intact afterwards.
- CI at head `b098dde`: all GitHub Actions jobs SUCCESS (nix skipped as
  designed), CodeRabbit SUCCESS, merge state CLEAN/MERGEABLE.

## Next action (delegated to worker)

Squash-merge PR #86 with branch deletion, verify clean tracked tree, ff-only
sync of local `main`, remove the T26 worktree, reply
AGMSG-RESULT v1 task_id=T26 status=merged with the merge commit hash.
