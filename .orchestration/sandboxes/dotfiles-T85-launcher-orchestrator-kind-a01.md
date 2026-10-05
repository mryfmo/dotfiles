# Sandbox: dotfiles-T85-launcher-orchestrator-kind-a01

- **Sandboxed:** edits, shfmt, ShellCheck, the unit tests, the behaviour checks, the read-only `--directive` run in the main checkout, and the commit.
- **Hook:** a PreToolUse hook refused a bare `python3 -` heredoc and pointed to `uv run`; the edit was redone with `uv run --no-project python -`.
- **Unsandboxed:** the push, `gh pr create` and `gh` polling, CompactionDB `memory add`, and these artifact writes.
- **Not done:** nothing in the main checkout changed beyond these artifacts. No profile, manifest or generator edits; no Codex seat claim; no merge, force push or thread resolution; no local bats.
