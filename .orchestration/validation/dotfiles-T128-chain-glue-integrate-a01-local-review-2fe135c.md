---
task: dotfiles-T128-chain-glue-integrate-a01
head: 2fe135c5c856a345002086df361e862232c47a58
pr: 372
base: 1d41812678366506151579ce3e2ac96b20e8d4b5
started: 2026-10-16T21:38:38Z
finished: 2026-10-16T21:42:32Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Restore the PR head after the audit changes the review checkout — scripts/orchestrator/chain-integrate.sh:177-177
- [P2] Recheck main-checkout freshness after a base move — scripts/orchestrator/chain-integrate.sh:121-126

```text
The audit leaves the checkout at the wrong head for the subsequent gate, and the base-update restart can execute stale integration scripts. Syntax checks passed; the fixture-writing unit tests were not run in the read-only environment.

Full review comments:

- [P1] Restore the PR head after the audit changes the review checkout — scripts/orchestrator/chain-integrate.sh:177-177
  `orch-audit.sh` checks its canonical review worktree out at `origin/main` and never restores its previous HEAD. Because this call also uses that worktree as the PR checkout, every successful chain leaves it at the base rather than `${head}`. A subsequent `orch-gate.sh <task> <review> <pr>` consequently reads the base as the PR head and looks for the wrong audit file, breaking the required audit-to-gate handoff ([AGENTS.md:44](AGENTS.md#L44)). Restore the saved PR head before returning, and test with an audit stub that changes HEAD.

- [P2] Recheck main-checkout freshness after a base move — scripts/orchestrator/chain-integrate.sh:121-126
  If `origin/main` advances during the checks or Bot wait, this path updates the PR and restarts without repeating the main-checkout freshness check. The chain then executes scripts from the old main checkout despite its initial refusal of stale scripts. In a linked worktree, `local-review.sh --base main` also compares against the stale local branch, including newly merged base commits in the PR review. Refuse with the existing fast-forward guidance, or refresh and revalidate the trusted checkout before continuing.
The audit leaves the checkout at the wrong head for the subsequent gate, and the base-update restart can execute stale integration scripts. Syntax checks passed; the fixture-writing unit tests were not run in the read-only environment.

Full review comments:

- [P1] Restore the PR head after the audit changes the review checkout — scripts/orchestrator/chain-integrate.sh:177-177
  `orch-audit.sh` checks its canonical review worktree out at `origin/main` and never restores its previous HEAD. Because this call also uses that worktree as the PR checkout, every successful chain leaves it at the base rather than `${head}`. A subsequent `orch-gate.sh <task> <review> <pr>` consequently reads the base as the PR head and looks for the wrong audit file, breaking the required audit-to-gate handoff ([AGENTS.md:44](AGENTS.md#L44)). Restore the saved PR head before returning, and test with an audit stub that changes HEAD.

- [P2] Recheck main-checkout freshness after a base move — scripts/orchestrator/chain-integrate.sh:121-126
  If `origin/main` advances during the checks or Bot wait, this path updates the PR and restarts without repeating the main-checkout freshness check. The chain then executes scripts from the old main checkout despite its initial refusal of stale scripts. In a linked worktree, `local-review.sh --base main` also compares against the stale local branch, including newly merged base commits in the PR review. Refuse with the existing fast-forward guidance, or refresh and revalidate the trusted checkout before continuing.
```
