# dot-ubuntu-parity-T9-a01 — learning triage

## Reusable rule candidate

Fourth occurrence in this branch of the "works on any real, already-set-up
machine, fails on a genuinely fresh/isolated one" pattern (T5:
script-ordering vs. file-application; T7/T8: zed.sh mkdir-after-mv; T9:
temp-destDir apply vs. real systemd config path). The specific new lesson
here: chezmoi's run_once/run_onchange _ordering_ controls apply the writes
into whatever `$HOME` the current apply targets, but any command in such a
script that has effects scoped to the _real_ user session (`systemctl
--user`, `dbus-send`, anything reading `$XDG_RUNTIME_DIR`/`$XDG_CONFIG_HOME`
outside the apply's own `$HOME` override) can silently diverge from where
chezmoi just wrote files, in CI's temp-destDir apply mode. The fix pattern
is general: guard such a command on the actual, real-environment path it
will read/act on being present — not on chezmoi's own completion signal
(ordering, run_once markers, etc.) — since those two things can disagree
whenever `$HOME` during apply isn't the real session's `$HOME`. Recorded as
CompactionDB `[memory:decision]` `90f10560-425a-4dd8-9cb9-19bee270ef73`.

Worth flagging to the orchestrator as a candidate written rule (not just a
CompactionDB entry) if any more `.chezmoiscripts` are added that call
`systemctl --user` or similar real-session commands — this is now the
second time (T5, T9) the same script needed two separate, non-overlapping
fixes for the same visible symptom.

## Tooling note

`chezmoi execute-template -S <path>` is the correct way to render a
`.chezmoiscripts` template against a _specific_ worktree's source rather
than whatever the machine's live chezmoi config points at (which, in this
multi-worktree setup, defaults to the main checkout, not this task's
worktree) — confirmed via `{{ .chezmoi.sourceDir }}`. Useful for any future
task that needs to validate a chezmoi template's rendered output without
running `chezmoi apply` (forbidden in every task in this regime anyway).

Not promoting either item to `skills/candidates/` — project-specific
chezmoi/systemd interaction facts, not a reusable Claude/Codex workflow.
