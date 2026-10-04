# dotfiles-T69-protocol-docs-unification-a01 — sandbox

- Isolation: dedicated git worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-d`, branch `docs/protocol-unification` from `origin/main` febd0cb7 (#243, T88), later merged with main 6de95167 (#252) through `gh pr update-branch`. Worker identity: `claude-standard-dot-a006` (Claude Code, `standard`). The earlier branches (`docs/parallel-execution-rule`, `feat/gate-audit-evidence`, `chore/permgate-dead-lanes`, `fix/make-update-unattended`) are kept and untouched.
- Edits, the docs, `herdr-agents` and `pr-feedback` unit tests, `make unit-test`, `make validate-agent-assets`, prettier and ruff ran in the Claude Code Bash sandbox. These ran unsandboxed through the permission gate:
  - `git fetch`/`push`, `gh pr create`/`checks`/`update-branch`/`api`;
  - WebFetch of the two GitHub REST docs pages (`pulls/reviews`, `pulls/comments`) for the item-4 field check;
  - `python3 .claude/hooks/contextdb_cli.py memory add` in the main checkout;
  - `agmsg-dispatch`.
- Code changes are limited to the one stderr string in `executable_herdr-agents` (`bash -n` clean) and its pinned expectation in `tests/unit/test_herdr_agents.py`. No `scripts/require-crit-review.py` change; README only at the named lines; the T88 parallel, routing and step-14 text is cited, not rewritten. No `make update`/`make apply`, no local bats, no merge.
- No Plan Mode was used, so no Crit plan server was started; `plan-mode-used` does not apply.
