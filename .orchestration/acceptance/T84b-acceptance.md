# T84b acceptance

- task: T84b (BASH_SOURCE resolution under chezmoi include; + shebang revise)
- decision: accepted (after one revise round)
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Resolver verified in diff: wrapper-exported validated root
  (joinPath parent, required because .chezmoiroot=home makes
  .chezmoi.sourceDir = <repo>/home — worker-caught spec correction,
  approved with the validity check kept mandatory), BASH_SOURCE
  fallback for direct runs, hard failure otherwise; both
  repository-relative consumers routed; remaining BASH_SOURCE use is
  the include-safe main guard only.
- Revise round: my pre-acceptance LIVE chezmoi apply caught
  `exec format error` — the export displaced the included library's
  shebang from line 1. Fixed with a wrapper shebang + a rendered-
  template-starts-with-shebang regression test. Unit tests could not
  see this; live execution did (live-E2E principle upheld again).
- Final live verification: chezmoi apply runs the re-fired run_once
  script with zero errors, chezmoi status empty, and the
  update_compactiondb manifest step freshly recorded (11:44:48Z) at
  2.0.0+dotfiles.5.
- Gates re-run orchestrator-side: 338 unit tests OK (single first-run
  flake recurred and passed on rerun — 4th observation, tracked),
  validate-agent-assets ok.

## Effects

effects=none (repo edits; deployment exercised live at acceptance).

cost: n/a (worker-reported)
