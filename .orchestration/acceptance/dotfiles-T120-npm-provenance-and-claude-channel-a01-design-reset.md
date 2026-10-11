---
format: 2
reset_of: dotfiles-T120-npm-provenance-and-claude-channel-a01
redesign_task: dotfiles-T127-agent-cli-supply-chain-design-a01
redesign_seat: "a context other than the author of T120: a seated claude-review-dot-aNNN (review profile) or a fresh headless run, per T128 INV-6/INV-7 (the redesign profile of T124 v4 was dropped with PR #313)"
reason: "eight amendments before the first RESULT, two of them correcting premises of the task text (the orchestrator's mise probe, Anthropic's auto-updater being disabled on these hosts): the under-researched-task signal T126 INV-6 names; the task never had a reviewed design, invariant tests or an audit, so \"the work is good\" is unverified"
---

# Design reset: dotfiles-T120-npm-provenance-and-claude-channel-a01

Written 2026-10-10 by the orchestrator seat on the operator's question (「以前の過ちを引きずることをなぜ選択するのか」): the orchestrator had recommended continuing on sunk-cost grounds; the rule exists for exactly this case and applies.

- Abandoned: PR #315 `feat/npm-provenance-and-claude-channel` (worker `claude-standard-dot-a002`, worker-e), left open as a draft for reference, never merged. The worker stops after pushing its current state and sends a final `AGMSG-RESULT … status=superseded`.
- Redesign: `dotfiles-T127-agent-cli-supply-chain-design-a01`, a `kind: design` task written by a context other than T120's author (a seated `claude-review-dot-aNNN` on the review profile, or a fresh headless run) once T128 V1 merges and the validator exists; reviewed per T128 INV-7 (a Claude fresh context and a Codex read-only review); its implementing task may name PR #315's branch as material (`continuation_of: dotfiles-T120-npm-provenance-and-claude-channel-a01`), and every line it keeps is re-verified against the reviewed invariants.
- What the redesign must settle up front (the questions T120 discovered one amendment at a time): the actual update path of Claude Code on these hosts (`autoUpdates: false` is managed; `make update` is the only mover); how mise installs npm tools here (`package_manager = "npm"`: npm subprocess, `~/.npmrc` cooldown applies, `install_env` honoured); which npm packages publish provenance; the gap between apply and the native install on a host that cannot verify yet; `remove-agent-asset` safe roots; the trust anchors (Anthropic release key fingerprint, npm registry signatures, provenance attestations); the scope list (every file `git grep` names for `claude-code`, `ensure_mise_npm_agent_cli`, `claude-update`).
