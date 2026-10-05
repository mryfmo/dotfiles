# Sandbox: dotfiles-T84-orchestrator-kind-a01

- **Sandboxed:**
  - edits (through `uv run --no-project python -`, since bare `python3 -` heredocs are hook-blocked);
  - the generator run, `make render-check`, `make validate-agent-assets`, `make unit-test`, ruff and prettier;
  - the commit and the push. The push landed (`git ls-remote` shows `25f5079f`); only the upstream-tracking config write failed on the read-only `.git/config` stub.
- **Unsandboxed:**
  - `gh pr create`, `gh pr checks --watch` and the bot-wait polling (`gh` gets 401 in the sandbox);
  - CompactionDB `memory add`;
  - `agmsg-dispatch`.
- **Generator scope:** `expected_outputs` writes only under the repository root (`ROOT / …`). Nothing under `$HOME` or `~/.codex/**` was written.
- **Not done:**
  - no edits to `executable_herdr-agents`, profiles or hooks;
  - no `make update`/`apply`/`upgrade`;
  - no merge, force push or thread resolution;
  - no local bats.
  - The main checkout received only these five artifacts.
