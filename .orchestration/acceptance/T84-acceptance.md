# T84 acceptance

- task: T84 (chezmoi drift class resolution)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Complete zsh hunk table (11 hunks + 1 identical-both-sides note, zero
  unclassified) cross-checked against post-edit `chezmoi diff` output:
  every residual diff is a justified intended source-side win (quoting
  robustness, existence guards, shdoc). Critical invariants verified in
  merged sources: shims-first PATH in .zshenv (non-interactive SSH),
  guarded `mise activate zsh --shims` in .zprofile, guarded sheldon and
  Herdr dispatch in .zshrc, Claude updater retained.
- All five profile modifiers renamed modify*private* (git mv), with
  generator/validator/runtime-map/tests updated; deep mode drift
  resolved at source, siblings get intended 0644->0600 on apply.
- Doctor drift check verified WARN-only with class hints, outside the
  REPAIR map, with focused tests.
- Gates re-run orchestrator-side: 338 unit tests OK,
  validate-agent-assets ok, `zsh -n` pass on all three sources.
- Orchestrator will apply targets and verify empty `chezmoi status` as
  Class A remediation (deployment is orchestrator-side).

## Effects

effects=none (repo edits only; deployment at acceptance below).

cost: n/a (worker-reported)
