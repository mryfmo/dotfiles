# dot-ubuntu-parity-T3-a01 — learning triage

Reusable, validated facts from this task (also registered as CompactionDB
`[memory:decision]` records — see the report and validation artifacts for
the exact commands and IDs):

1. **chezmoi `include`/template relative-path resolution is anchored to the
   chezmoiroot-adjusted source dir, not the calling file's directory.**
   This repo sets `.chezmoiroot=home`, so `home/` is the effective source
   root. A call like `{{ include "../install/ubuntu/server/setup_timezone.sh" }}`
   from _any_ file under `home/.chezmoiscripts/**` resolves relative to
   `home/`, not relative to that file's own subdirectory — verified
   empirically with `chezmoi execute-template`. Anyone adding a new
   `.chezmoiscripts/**/*.tmpl` that includes an `install/**` script should
   write the relative path as if starting from `home/`, regardless of how
   deeply nested the calling template is.
   → CompactionDB decision `caa48801-c710-49c9-916e-8075a992929d`.

2. **`run_onchange_*` scripts only re-trigger on their own rendered content
   changing.** If a run_onchange script's job is to react to a _different_
   managed file changing (e.g. enabling a systemd unit whenever that unit's
   content changes), the script must embed that file's hash
   (`{{ include "path" | sha256sum }}`) as a comment in its own body. This
   is now a reusable pattern for any future "install once per file-set,
   re-run when that file-set changes" chezmoiscript in this repo.
   → CompactionDB decision `20114ee0-f0a9-4be1-930d-b1f3fdf8922b`.

3. **Editing a `.py` file in this session through the `Edit` tool triggers an
   automatic full-file reformat (black/ruff-style) via a PostToolUse hook —
   editing the same file through `Bash`/`sed` does not.** For a task that
   needs a single precise line change in a Python test file (as B2b did),
   prefer `sed`/sed-equivalent edits over the `Edit` tool to avoid an
   unrelated, oversized diff. This is environment/session behavior, not a
   repo convention (the repo has no `pyproject.toml`/black/ruff config and
   `make format` never touches `.py` files), so it's worth remembering for
   any future task in this same session/environment rather than promoting
   it as a repo-wide rule.

## Not promoted to `skills/candidates/`

None of the above rise to the level of a new reusable skill; they are
task-specific chezmoi/mise facts and one session-environment quirk, all
already captured as CompactionDB decisions or noted here for the next
worker turn.
