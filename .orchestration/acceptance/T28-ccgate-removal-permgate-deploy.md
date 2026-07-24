# T28 acceptance: ccgate removal and permgate live deployment

- Task: `.orchestration/tasks/T28-ccgate-removal-permgate-deploy.md`
- Result: PR [#93](https://github.com/mryfmo/dotfiles/pull/93), head
  `0dc4ef1098da4c832ad38fe4c71e8a2d03eaf2fe` (`chore/remove-ccgate`).
- Verdict: **accepted** (next_action=merge).

## Verification performed

- Independent full-diff read (5 files, +6/−33): mise pin dropped;
  `CCGATE_MISE_TOOL`/`ensure_ccgate_cli`/call site removed; README reworded;
  policy `known-version-check` regex no longer auto-allows the removed
  binary while the `metrics` provenance block and pattern source counts are
  preserved; lifecycle.bats positive assertions inverted to absence.
- Resurrection guards confirmed untouched: `MANAGED_PERMISSION_EXECUTABLES`
  ccgate entry, codex/claude merge regression tests, validator prohibitions,
  `.chezmoiremove` entries.
- Scope item 3 (reference docs) needs no PR change:
  `docs/reference/scripts/update-agent-assets.md` is gitignored generated
  output (`make docs` regenerates from shdoc comments, which no longer
  mention ccgate) — verified via `git ls-files`/`check-ignore`.
- Live state verified first-hand by the orchestrator, not from the report:
  `command -v ccgate` fails; `mise ls`, live mise config, and
  `~/.local/share/mise/installs` all free of ccgate; `~/.local/bin/common/
permgate` executable; live Claude settings carry exactly the managed
  PermissionRequest hook; live Codex config contains the permgate
  `[[hooks.PermissionRequest]]`; `decisions.jsonl` holds six redacted
  records (hash + bounded summary only) — deterministic allow and deny at
  0 ms for both providers, ambiguous fixture ended in shadow ask
  (claude timeout, codex rejected) and shadow never allowed.
- CI at head `0dc4ef1`: all GitHub Actions jobs SUCCESS (nix skipped),
  CodeRabbit SUCCESS, merge state CLEAN/MERGEABLE.

## Next action (delegated to worker)

Squash-merge PR #93 with branch deletion, verify clean tracked tree, ff-only
sync of local `main`, remove the T28 worktree, run `chezmoi apply` once from
merged main and confirm it is a no-op against the already-deployed live
state, reply AGMSG-RESULT v1 task_id=T28 status=merged with the merge
commit hash.
